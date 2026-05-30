---
type: analysis
summary: "label refinement 実験は現行実装のまま採用せず、ラベル品質改善をユースケース契約、上流入力 sampling、代表例 artifact、judge 較正、UI 表示責務に分けて仕切り直す。今回の refinement は polish-only で中身を見ず、全体傾向把握と少数重要論点発見のどちらを良くするかも未固定だった"
sources:
  - slack-label-algorithm-improvement-2026-05-30.md
  - source-code.md
  - label-refinement-input-scope-2026-05-29.md
  - label-coverage-policy-2026-05-29.md
  - label-quality-rubric-evaluation-2026-05-29.md
  - label-refinement-judge-bundle-2026-05-25.md
---

label refinement 実験から始まった一連の調査は、現行 `hierarchical_label_refinement` 実装をそのまま育てるより、**ラベル品質改善の問題設定を仕切り直すべき**という結論に寄っている。

## Use Case Gate

2026-05-30 の Slack で ohki-shingo は、良くしたい出力が `全体傾向の把握` なのか `少数だが重要そうな論点の発見` なのかで、適切な処理と評価が変わると指摘した。[[slack-label-algorithm-improvement-2026-05-30]]より

この指摘を踏まえると、次の実験は algorithm choice から始めるべきではない。まず run ごとに「この出力は何を成功とするか」を固定する必要がある。全体傾向モードなら高頻度トピックの安定カバーと sibling distinction が主眼になる。一方、少数重要論点モードなら label の短さよりも、minority / boundary / residual evidence を失わない artifact が必要になる。

## Current Judgment

`codex/remaining-experiment-wip` の label refinement は、現時点では「良い改善」として main 昇格を目指す段階ではない。理由は次の通り。

- refinement は rep args を入力に取らず、上流 label / description / children label だけを polish する。中身と照らして誤ラベルを直せない。[[label-refinement-input-scope-2026-05-29]]より
- ラベル付けそのものの入力 sampling は、API 経由で最大 30 件、analysis-core default で 10 件の random sample であり、大規模クラスタでは上流ラベルがランダムに引っ張られる。[[label-coverage-policy-2026-05-29]]より
- UI の個別データ表示は representative selection ではなく配列先頭 10 件なので、ユーザが見る例もラベル品質 judge が見る例も設計された代表例ではない。[[source-code]]より
- rubric judge v0 は過去出力 4 候補を再評価してもほぼ満点になり、人間 / Claude judge が見つけたズレを十分に検出できていない。[[label-quality-rubric-evaluation-2026-05-29]]より

したがって「今回の label refinement をもう少し磨く」より、ラベル品質を作る入力、表示する証拠、判定する judge を分けて設計し直す方が筋がよい。

## Reset The Problem

次の 5 レイヤを別々に扱う。

1. **ユースケース契約**: `全体傾向把握` / `少数重要論点発見` / `公開 UI の説明責務` のどれを成功条件にするかを run metadata と judge prompt に明示する
2. **ラベル生成入力**: cluster 内 N 件から LLM に何を見せるか。まずは sampling を外して全件を渡す実験を先にやる。ダメなら max coverage / FPS / k-medoids / subtopic coverage を比較する
3. **ラベル生成 / refinement**: 既存 label の polish ではなく、元 arguments または設計された rep args を見て label / description を再生成できる責務にするかを決める
4. **代表例 artifact**: UI と judge が使う rep args を、配列先頭や典型例だけにしない。`典型例 / 幅を見せる例 / 境界例` を分ける
5. **judge**: rubric は方向性として良いが、現行 v0 は甘い。criteria を厳格化する前に、judge が見る evidence を固定し、人間判断と照合する

## Low-Cost Improvements Before Refinement

今回見つかった低コスト改善候補は、refinement より先に試す価値がある。

- ラベル生成時の `sampling_num` を十分大きくして全件入力に近づける
- UI / judge 用 rep args を `典型例 2 + 幅 2 + 境界 1` のように固定し、配列先頭依存をやめる
- judge 入力も同じ rep args artifact を使い、human review と同じ材料を見るようにする
- rubric judge には「材料にない軸」と「見える重要軸の欠落」をもっと厳しく採点させる

これらは、LLM prompt polish よりも構造的な改善で、かつ実験として切り出しやすい。

## Implication For Issue / PR Strategy

既存の label refinement PR / branch は、採用候補というより「問題を発見した実験」として扱う。次の PR は refinement そのものではなく、より小さい slice に分ける。

- sampling 全件入力実験
- rep args artifact 生成
- UI 表示の rep args 差し替え
- judge 入力 / rubric 較正

この順にすると、どこで品質が上がったか、どこでコストが増えたか、どこで judge が外したかを追跡しやすい。

## Open Questions

- `全件入力` はどの規模まで現実的か。cluster size ごとの token / cost を先に見積もるべきか
- `全体傾向把握` と `少数重要論点発見` を同じ pipeline option で扱うべきか、別 analysis mode / judge mode として切るべきか
- rep args artifact は aggregation step に入れるべきか、独立 step にするべきか
- `典型例 / 幅 / 境界` の分類は embedding だけで足りるか、LLM の短い説明を付けるべきか
- 現行 `hierarchical_label_refinement` は破棄するか、`polish-only` と明記して実験用に残すか

## Updates

- 2026-05-30: ohki-shingo の「全体傾向把握か、少数重要論点発見かで処理・評価が変わる」という Slack 指摘を受け、仕切り直しレイヤの先頭に `ユースケース契約` を追加。sampling / rep args / judge の前に成功条件を固定する方針へ補正
- 2026-05-30: 初版作成。今回の label refinement 実験はそのまま採用せず、上流 sampling、rep args artifact、judge 較正、UI 表示責務を分けて仕切り直す方針として整理
