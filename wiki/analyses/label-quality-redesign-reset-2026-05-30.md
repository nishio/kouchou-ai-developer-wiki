---
type: analysis
summary: "label refinement 実験は現行実装のまま採用せず、ラベル品質改善をユースケース契約、上流入力 sampling、代表例 artifact、judge 較正、UI 表示責務に分けて仕切り直す。今回の refinement は polish-only で中身を見ず、全体傾向把握と少数重要論点発見のどちらを良くするかも未固定だった"
sources:
  - slack-label-algorithm-improvement-2026-05-30.md
  - slack-stance-discussion-2026-05-30.md
  - source-code.md
  - label-refinement-input-scope-2026-05-29.md
  - label-coverage-policy-2026-05-29.md
  - label-quality-rubric-evaluation-2026-05-29.md
  - label-refinement-judge-bundle-2026-05-25.md
---

label refinement 実験から始まった一連の調査は、現行 `hierarchical_label_refinement` 実装をそのまま育てるより、**ラベル品質改善の問題設定を仕切り直すべき**という結論に寄っている。

## ユースケース契約 (確定: 全体傾向把握ユースケース 一本)

2026-05-30 の Slack で ohki-shingo は、良くしたい出力が `全体傾向の把握` なのか `少数だが重要そうな論点の発見` なのかで、適切な処理と評価が変わると指摘した。[[slack-label-algorithm-improvement-2026-05-30]]より

同日の nishio との対話で、契約構造は次のように確定した。

- **「全体傾向把握ユースケース」** を Web UI / 標準 run の **唯一のユースケース契約** とする。Web UI には契約の選択肢自体を露出しない。tokoroten の operational 言い換えでは「デカい見落とし / デカい違和感を見つける」装置と表現できる。[[slack-stance-discussion-2026-05-30]]より
- **「少数重要論点ユースケース」 (少数だが重要な論点を見つける) は契約として並列に置かない**。理由は、(1) 「重要」が確率的事象で「こうすればできます」とツール側が保証できない、(2) 「重要」の定義は分析者の責務であり prompt に書き込む必要があり、データサイエンティストの素養を要する。一般ユーザに露出する概念ではない
- 少数重要論点系の経路は CLI / `analysis-core` でのカスタム prompt として残す。CLI docs にも「重要を言語化する責務」を強く educate する必要はない (priority 低)
- 全体傾向把握 run の副産物として minority residual artifact を作らない。serendipity で少数重要論点の発見が起きることはあるが、それを product として約束しない

この確定により、下流 4 レイヤは全体傾向把握ユースケース最適化で揃う。FPS / 境界保存 / minority preservation 系の道具は少数重要論点系のためのものなので、全体傾向把握最適化の標準パイプラインには入れない。

全体傾向把握ユースケースは **構造把握スタンス** で実現することが前提である。「上位 N トピックの頻度を見るだけ」(定量分析スタンス) ではない。詳細は [[analysis-stance]] を参照。これにより sampling / rep args / judge の最適化指針も、頻度カバレッジだけでなく「ユーザが構造を読める rep / label / judge」として絞る必要がある。

`analysis_mode` (アルゴリズム選択) はユースケース契約と直交する。Web UI に `hierarchical_default` 以外の mode (`llm_grouping` 等) を出しても、それは「同じ全体傾向把握ユースケースをどう実現するか」の選択であって契約レイヤを増やすわけではない。[[usage-modes]]より

## Current Judgment

`codex/remaining-experiment-wip` の label refinement は、現時点では「良い改善」として main 昇格を目指す段階ではない。理由は次の通り。

- refinement は rep args を入力に取らず、上流 label / description / children label だけを polish する。中身と照らして誤ラベルを直せない。[[label-refinement-input-scope-2026-05-29]]より
- ラベル付けそのものの入力 sampling は、API 経由で最大 30 件、analysis-core default で 10 件の random sample であり、大規模クラスタでは上流ラベルがランダムに引っ張られる。[[label-coverage-policy-2026-05-29]]より
- UI の個別データ表示は representative selection ではなく配列先頭 10 件なので、ユーザが見る例もラベル品質 judge が見る例も設計された代表例ではない。[[source-code]]より
- rubric judge v0 は過去出力 4 候補を再評価してもほぼ満点になり、人間 / Claude judge が見つけたズレを十分に検出できていない。[[label-quality-rubric-evaluation-2026-05-29]]より

したがって「今回の label refinement をもう少し磨く」より、ラベル品質を作る入力、表示する証拠、判定する judge を分けて設計し直す方が筋がよい。

## 仕切り直しレイヤ (全体傾向把握ユースケース前提)

最上位の契約が全体傾向把握ユースケース 一本に固まったので、下流 4 レイヤはそれに最適化で揃える。

1. ~~**ユースケース契約**~~ → 確定 (全体傾向把握ユースケース 一本)。run metadata に明示する必要すらない (Web UI = 全体傾向把握、CLI のカスタムは分析者の prompt 側)
2. **ラベル生成入力**: cluster 内 N 件から LLM に何を見せるか。全体傾向把握なら方向は「高頻度トピックの安定カバー」。まず sampling を外して全件を渡す実験を先にやる。ダメなら max coverage / k-medoids / subtopic coverage を比較する (FPS は外れ値保存なので少数重要論点系の道具、全体傾向把握用には外す)
3. **ラベル生成 / refinement**: 既存 label の polish ではなく、元 arguments または設計された rep args を見て label / description を再生成できる責務にするかを決める。全体傾向把握なら判定軸は「カバレッジを示す要約として整っているか」
4. **代表例 artifact**: UI と judge が使う rep args を `典型例 + 幅` を主軸にする。「境界例」は全体傾向把握の主入力ではない (少数重要論点系の道具)。配列先頭依存はやめる
5. **judge**: 全体傾向把握用の rubric として、coverage と sibling distinction を重く配点する。minority residual の検出ペナルティは入れない (少数重要論点系の judge の仕事)。criteria 厳格化の前に、judge が見る evidence を rep args artifact に固定し、人間判断と照合する

## refinement より先に試す低コスト改善

今回見つかった低コスト改善候補は、refinement より先に試す価値がある。

- ラベル生成時の `sampling_num` を十分大きくして全件入力に近づける
- UI / judge 用 rep args を `典型例 2 + 幅 2 + 境界 1` のように固定し、配列先頭依存をやめる
- judge 入力も同じ rep args artifact を使い、human review と同じ材料を見るようにする
- rubric judge には「材料にない軸」と「見える重要軸の欠落」をもっと厳しく採点させる

これらは、LLM prompt polish よりも構造的な改善で、かつ実験として切り出しやすい。

## Issue / PR 戦略への含意

既存の label refinement PR / branch は、採用候補というより「問題を発見した実験」として扱う。次の PR は refinement そのものではなく、より小さい slice に分ける。

- sampling 全件入力実験
- rep args artifact 生成
- UI 表示の rep args 差し替え
- judge 入力 / rubric 較正

この順にすると、どこで品質が上がったか、どこでコストが増えたか、どこで judge が外したかを追跡しやすい。

## Open Questions

- `全件入力` はどの規模まで現実的か。cluster size ごとの token / cost を先に見積もるべきか
- rep args artifact は aggregation step に入れるべきか、独立 step にするべきか
- `典型例 + 幅` の選び方は embedding だけで足りるか、LLM の短い説明を付けるべきか
- 現行 `hierarchical_label_refinement` は破棄するか、`polish-only` と明記して実験用に残すか
- 全体傾向把握用 rubric criteria の具体形 (何点配点で何を fatal とするか)

## Updates

- 2026-05-30: 用語を descriptive な日本語に揃え直した。`contract A` を `全体傾向把握ユースケース`、`contract B / B 系` を `少数重要論点ユースケース系`、`β スタンス` を `構造把握スタンス`、`α 定量分析` を `定量分析スタンス` に置換。略号は時間が経つと文脈なしには読めなくなるため、内容で読める表現に統一
- 2026-05-30: nishio との対話で「広聴AI は構造把握スタンスのツールであり定量分析ツールではない」が core stance として確定 ([[analysis-stance]] 新規)。全体傾向把握ユースケースも定量分析ではなく構造把握スタンスで実現することを明示。これにより sampling / rep args / judge は単なる頻度カバレッジ最適化ではなく「構造を読める材料」として設計する必要がある
- 2026-05-30: nishio との対話でユースケース契約を確定。**「全体傾向把握ユースケース」一本** を Web UI / 標準 run の唯一の契約とし、「少数重要論点ユースケース」は契約として並列に置かず CLI 分析者の prompt 責務に寄せる。「重要を言語化する責務」は product として educate しない (Web UI 完全非露出、CLI docs も priority 低)。全体傾向把握 run の副産物として minority residual artifact も作らない (約束しない)。これにより下流 4 レイヤは全体傾向把握最適化で揃い、`仕切り直しレイヤ` 節を全体傾向把握前提で書き換えた
- 2026-05-30: ohki-shingo の「全体傾向把握か、少数重要論点発見かで処理・評価が変わる」という Slack 指摘を受け、仕切り直しレイヤの先頭に `ユースケース契約` を追加。sampling / rep args / judge の前に成功条件を固定する方針へ補正
- 2026-05-30: 初版作成。今回の label refinement 実験はそのまま採用せず、上流 sampling、rep args artifact、judge 較正、UI 表示責務を分けて仕切り直す方針として整理
