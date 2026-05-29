---
type: analysis
summary: "label 設計の人間判断: ラベルは『目次』ではなく『要約』として、上位 2〜3 軸まではカバーする方向で整える。1 キーワードでクラスタ全体を覆うのは不可能なので、最頻トピック A + 残差を覆う B の greedy max-coverage 的な発想を取る。ラベルから dimension が落ちる根本原因の一つは、上流ラベリング入力が API 経由では最大30件、CLI/defaultでは10件のランダムサンプリングであることにもある"
sources:
  - source-code.md
  - label-refinement-judge-bundle-2026-05-25.md
---

[[label-refinement-input-scope-2026-05-29]] で Claude judge が「人間に当てるべき論点」として 3 件出した結果に対して、2026-05-29 の Slack 議論で複数人から人間判断が返ってきた。あわせて、tokoroten が上流の sampling 制約を指摘し、コード確認で「ラベルから軸が落ちる根本原因」が refinement 以前にもあることが分かった。本ページはその判断と方針を product 文脈で整理する。[[label-refinement-judge-bundle-2026-05-25]]より

## 論点 1: 「短いが欠落」vs「長いが冗長」

**人間判断: カバレッジ優先、冗長は許容する。**

`balanced` の `AIによる持続可能な社会構築` のように `災害対応` 軸が脱落する書き方は、scan しやすくなる代わりに、ユーザにとっては「クラスタ内に label 外の話題が混ざっている」ように見える。tokoroten の言葉では「カテゴリ外が含まれてるほうが気持ち悪い」。したがって、`none` 系のように長くても全 dimension が label に出ている方が安全側である。[[label-refinement-judge-bundle-2026-05-25]]より

これは、ラベルを「一覧 UI 上の目次見出し」ではなく「クラスタの要約」として扱う、という product 定義の選択である。

## 論点 2: 何件まで脱落 OK か

**人間判断: 1 キーワードでの完全包括は無理。上位 2〜3 キーワードで「AとB」程度まで広げる方向で妥協する。**

クラスタ内 26 件全部を 1 キーワード A で表現できることはレアであり、「何一つ捨てない」は不可能。ただし損失は最小化したい。具体的な発想は次:

- まず最頻のトピック A を取る
- A でカバーできなかった残差の中で次に最頻の B を取る
- ラベルを `A と B` 形式にする
- `A と B と C と D` のように 4 軸以上は許容しない (scanability が崩れる)

これは greedy max-coverage の発想で、上流 sampling や rep args の取り方を「最大被覆」に振る議論ともつながる。

### 提案されたアルゴリズム候補

| 案 | 概要 | コスト |
|---|---|---|
| tokoroten 案 | タイトル候補の embedding と各要素 embedding の cos 類似度総和 `∑ cos(emb(title), emb(item))` を最大化する title を選ぶ | embedding 計算のみで軽い |
| nishio 案 1 | LLM で title 候補を複数生成 → emb 距離でスコアづけ → 選択 | 候補生成分の LLM 呼び出しが増える |
| nishio 案 2 | 各 data point が title にカバーされているかを直接スコア化して最良候補を選ぶ | コスト度外視前提 |
| nishio 案 3 | 候補を複数 UI に出して人間に選ばせる | 計算コストは中程度、ユーザの好みを言語化する負担を肩代わりする UX として価値あり |

どれもメインパイプラインに即入れる話ではなく、experimental ステップとして比較する価値がある。

## 論点 3: 「エンタメ」のような口語の register

**人間判断: ユースケース次第。最悪、文字列置換で吸収できる。**

`contrast` の `AIによるエンタメと研究革新` のような口語が混ざる件は、product のトーン (政策意思決定の補助 vs 軽量レポート) によって許容度が変わる。優先度は論点 1, 2 より下で、必要なら post-processing で揃えられる。

## 上流の sampling 制約 (新発見)

論点 2 を議論する中で tokoroten が、ラベル付け時の sampling で「読み込まれない標本が出てラベルから情報が落ちる」可能性を指摘した。実コードを確認すると以下である。

- `packages/analysis-core/src/analysis_core/steps/hierarchical_initial_labelling.py:154-155`
- `packages/analysis-core/src/analysis_core/steps/hierarchical_merge_labelling.py:262-266`

両方とも `sampling_num = min(sampling_num, len(cluster_data))` で件数を切ったあと、`cluster_data.sample(n=sampling_num)` を呼んでいる。これは polars の `DataFrame.sample` で **完全ランダムサンプリング**。

件数上限は実行経路で違う:

- 管理画面/API 経由の通常レポート作成: `apps/api/src/services/report_launcher.py:42-49` が initial / merge とも `sampling_num = 30` を明示する
- analysis-core CLI / config default / builtin plugin default: initial / merge とも `sampling_num = 10`

- `compat/config_converter.py:120 / 129`: `setdefault("sampling_num", 10)` (initial / merge とも)
- `plugins/builtin/hierarchical_initial_labelling.py:51`: `step_config.get("sampling_num", 10)`
- `plugins/builtin/hierarchical_merge_labelling.py:51`: `step_config.get("sampling_num", 10)`

つまり、Web の通常経路では **クラスタに 30 件超の意見がある場合、ラベル付け対象はランダムに 30 件**、CLI/default 経路では **10 件超ならランダムに 10 件** しか選ばれない。tokoroten の「デフォルト 30」という発言は API 経由では正しく、analysis-core default だけを見ると 10 である。本質「ランダムサンプリングで情報が落ちる」点はどちらの経路でも同じ。[[source-code]]より

これが論点 1, 2 にとって意味するところ:

- 大規模クラスタほど、ラベルに反映される dimension が **「クラスタの実体」ではなく「ランダムに当たった 10/30 件」** に引っ張られる
- refinement で書き換えても、上流のランダム偏りは取り戻せない (refinement は rep args を見ないので [[label-refinement-input-scope-2026-05-29]])
- カバレッジ重視ラベルを実現するなら、refinement の入力を増やすより先に **`hierarchical_initial_labelling` の sampling 戦略** を `random → farthest point sampling / max coverage / k-medoids` に切り替える方が本質的

## UI 上の rep args 表示についても同じ問題

ラベル付け時の sampling とは別に、UI 上で「ラベル + rep args 3〜5 件」を表示する時に、どの args を選ぶか (random vs label に被覆される代表性の高いもの) も同じ最大被覆問題の系列である。

current main `0c294da` では、public-viewer の通常概要 (`ClusterOverview`) は label / 件数 / takeaway だけで、representative arguments は並べない。階層リスト表示 (`HierarchyListChart`) では deepest-level cluster だけ argument を展開できるが、ここでも representative selection はしていない。実装は `argumentList.filter((arg) => arg.cluster_ids.includes(cluster.id))` で対象 cluster の arguments を拾い、初期表示は `argumentsList.slice(0, 10)`。つまり **配列先頭 10 件**であり、最大被覆、ラベル適合度、クラスタ中心性、ランダム再抽選のいずれでもない。`hierarchical_result.json` の arguments 配列は aggregation が `hierarchical_clusters.csv` の行順に全件を詰めているので、表示順はおおむね upstream の argument order に従う。[[source-code]]より

代表例選定を入れる場合、`クラスタ中心に近いもの` や `ラベル embedding との類似度が高いもの` は納得感があるが、それだけだとクラスタ内の散らばりを過小に見せる。典型例だけを並べると、実際には複数の軸や周辺論点を含むクラスタでも「中心に綺麗に集まった単一論点」に見えやすく、公開 UI と judge 入力の両方で過信を誘う。

したがって rep args は 1 種類の「代表」ではなく、少なくとも次を分ける方がよい。

- **典型例**: centroid 近傍、または label embedding との類似度が高い argument。ラベルの意味を素早く理解するために使う
- **幅を見せる例**: 典型例から遠いが cluster 内に属する argument、または FPS / k-medoids / subtopic coverage で選んだ argument。クラスタが抱える散らばりや副論点を見せるために使う
- **境界例**: sibling cluster との境界に近い argument。ラベル間の違いが曖昧な場所を点検するために使う

UI 上は「代表例 3 件」だけより、`典型例 2 + 幅 2 + 境界 1` のように役割を分けて出す方が、納得感と過小表現のバランスを取りやすい。judge 入力でも同じで、典型例だけを渡すと label の良さを過大評価しやすい。

## 実験運用上の lesson

今回の流れ:

1. GPT judge が信頼できないと感じた
2. 判断対象を Markdown に固定形式で吐き出した ([[label-refinement-judge-bundle-2026-05-25]])
3. Claude Code に judge させた
4. Claude に「人間に確認すべきことはある？」と聞き、論点 3 件を引き出した
5. Slack で人間判断を集め、tokoroten から上流 sampling の仮説まで出た
6. 仮説をコードで確認し、本ページに政策として固定

このループは「Codex が experiment を実行 → Claude が judge して論点を切る → 人間が方針を決める」という分業として機能した。今後 sampling 戦略や title 選択アルゴリズムの実験を回す時にも同じ形が使える。

## Open Questions

- `hierarchical_initial_labelling` の sampling を max coverage / FPS に切り替える実装コストはどの程度か。`merge_labelling` も同様に切り替えるべきか
- ラベル候補を embedding 類似度総和で選ぶ tokoroten 案を実装する場合、候補は何個生成すれば実用的か (LLM 呼び出し回数とトレードオフ)
- UI / judge に渡す rep args を `典型例 / 幅を見せる例 / 境界例` に分ける場合、それぞれ何件ずつ出すのがよいか。まずは `典型例 2 + 幅 2 + 境界 1` のような少数構成で十分か
- 「上位 2〜3 軸まで」というカバレッジ方針を product として明文化する場所はどこか (refinement prompt? UI 仕様? guidelines?)
- 候補を UI で人間に選ばせる UX (案 3) はどのフェーズに位置付けるか (作成時の admin UX? 公開後のレビュー UX?)

## Updates

- 2026-05-30: nishio の指摘を受け、centroid 近傍や label embedding 類似度だけで rep args を選ぶと、クラスタ内の散らばりを過小に見せるリスクがあると追記。rep args は `典型例 / 幅を見せる例 / 境界例` を分けて設計する方針がよい
- 2026-05-30: current main `0c294da` を再確認し、ラベル付け時の `sampling_num` は API 通常経路では 30、analysis-core default では 10 であると補正。どちらも Polars の seed なし random sample で、最大被覆ではない。UI の「個別データ」表示は representative selection ではなく deepest-level cluster の配列先頭 10 件であることも追記
- 2026-05-29: 初版作成。Slack での人間判断 (論点 1: カバレッジ優先 / 論点 2: 上位 2-3 軸まで / 論点 3: 後回し OK) と、tokoroten が指摘した sampling 制約をコード確認 (`sampling_num` デフォルト 10、polars ランダム sample) して記録。refinement 改善より先に上流 sampling 戦略を見直す方が本質的、という方針につながった
- 2026-05-29: nishio から「ラベリング部分のコストは extraction と比べてごく少ないことが既知なので、max coverage / FPS のような複雑なアルゴリズムに飛ぶ前に **まず全件渡して試し、ダメなら減らす** というシンプルな実験で十分ではないか」という指摘。これは妥当で、初版で「sampling 戦略を `random → max coverage / FPS / k-medoids` に切り替える」と書いた方針は早計だった。順序を以下に整理し直す:
  1. **第一実験**: `sampling_num` を実質無効化 (十分大きい値か None) して全件をラベリング LLM に渡し、ラベル品質が改善するかを見る。LLM 呼び出し回数は変わらず、各呼び出しの token 量だけ増えるので、extraction と比べてのコスト増は小さい
  2. (1) で品質が改善しない、または context window が現実的に厳しいクラスタが出てきたら、初めて max coverage / FPS / k-medoids の比較に進む
  3. tokoroten 案 (タイトル候補 emb × 各要素 emb の cos 類似度総和最大化) は、(1) でも残る「LLM が長文 context から代表性のあるラベルを書けるか」とは別軸の改善なので並行して実験可能
  
  この順序にすることで、「上流 sampling が本当にボトルネックか」を最小コストで確認できる
- 2026-05-29: 過去議論の発掘。`raw/meeting_minutes.txt:5169-5170` (2025-06-18 定例) で tokoroten が「ラベリングのためには、ランダムサンプリングではなくて、Farthest Point Sampling を使った方がよさそう」と提案し、nishio が「アルゴリズム的には良い、計算量がどうかは未確認」と保留したまま、約 11 ヶ月実装されないままになっていた。今回 tokoroten が Slack で「Farestなんたらサンプリングで全体のサンプルを包括してタイトルをつけるってはいってるんだっけ」と書いたのは、この自分の過去提案を思い出していたもの。今日の nishio の「全件渡し」提案は、**11 ヶ月前に gating question として残っていた『FPS の計算量未確認』を、FPS を実装する前に sampling 自体の必要性を問うルートで回避する**アプローチになっている。実装コスト未確認のまま放置されてきたアイデアを、別角度から無効化する形で前進させた事例として記録
