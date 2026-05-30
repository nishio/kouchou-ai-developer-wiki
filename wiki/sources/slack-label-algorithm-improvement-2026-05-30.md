---
type: source
summary: "2026-05-29〜30 の Slack アルゴリズム改善ログ。ラベル欠落 vs 冗長、random sampling / 全件入力、rep args 選定、評価ユースケース分岐が議論された"
sources:
  - slack-label-algorithm-improvement-2026-05-29_30.txt
---

## What it is

2026-05-29 17:09 から 2026-05-30 09:08 までの `#2_開発_広聴ai_アルゴリズム開発` Slack 抜粋。Claude Code judge が出した label refinement への質問を nishio が転載し、tokoroten / ohki-shingo が反応した流れである。raw は `raw/slack-label-algorithm-improvement-2026-05-29_30.txt` に保存した。

議論の起点は `label refinement` だが、途中で「ラベル生成時に何件を LLM に見せるか」「UI に表示する arguments は代表例なのか」「judge が見る evidence は何か」「そもそもどのユースケースの出力を改善したいのか」へ広がった。

## Main Points

- **短いが欠落 vs 長いが冗長**: tokoroten は、ユーザ目線では label 外の話題がクラスタ内に混ざって見える方が気持ち悪いと反応した。nishio は「A と B」は許容できるが「A と B と C と D」は読みにくいので、上位 2〜3 キーワードに絞る greedy coverage 的な考え方を提示した。
- **タイトル候補のスコアリング**: tokoroten はタイトル候補 embedding と各要素 embedding の cosine 類似度総和を最大化する案を出した。nishio は LLM で複数候補を出して embedding で選ぶ案、あるいは各データをカバーしているかを直接スコアする案、候補を人間に選ばせる UX 案を挙げた。
- **sampling が落とし穴**: tokoroten は `sampling_num` によって cluster 内の未読標本が生じ、title から論点が落ちる可能性を指摘した。後続のコード確認では、管理画面/API 経由は initial / merge とも `sampling_num=30`、CLI / analysis-core default は `10`、実処理は seed なし Polars random sample で、最大被覆・FPS・k-medoids・ラベル適合度選択は入っていないと整理された。
- **まず全件入力を試す**: nishio / tokoroten とも、ラベリングのコストは extraction / cleansing に比べて小さいため、FPS の計算量を詰める前に「全部 LLM に載せて試し、ダメなら減らす」実験が自然だと見た。tokoroten は cleansing が現状コストの 99% 以上という見方も出している。
- **FPS は万能ではない**: 2025-06-18 定例で tokoroten が labeling 用 FPS を提案していたことが再発見された。ただし nishio は、FPS は cluster 境界付近のデータを拾いやすく、ラベル品質改善に直結するかは疑問だと指摘した。
- **UI の rep args は代表例ではない**: コード確認では、`hierarchical_result.json` に rep args artifact はなく、public-viewer の通常概要カードも label / 件数 / takeaway のみ。階層リスト表示は deepest-level cluster の arguments を `slice(0, 10)` するだけなので、代表性・典型性・幅・境界例の設計はまだ入っていない。
- **仕切り直し判断**: nishio は、今回の label refinement 実装だけを磨くより、sampling、UI/rep args、judge 実装を含めて考え直すべきと整理した。
- **ユースケース分岐**: ohki-shingo は、改善したい出力が「全体傾向の把握」なのか「少数だが重要そうな論点の発見」なのかで、適切な処理や評価が変わる可能性を指摘した。

## Design Implications

- label は「目次か要約か」だけではなく、対象ユースケースを先に固定しないと評価できない。全体傾向を把握したいなら高頻度トピックの安定カバーが重要になり、少数重要論点を見つけたいなら label そのものに詰め込むより edge / minority evidence を別 artifact として残す必要がある。
- `sampling_num` の値だけでなく、sample の選び方がラベル品質を規定している。random 10/30 件で生成した label は、大規模 cluster では cluster 全体ではなく「当たった標本」を説明している可能性がある。
- rep args は UI の見た目だけではなく、judge / human review の evidence でもある。配列先頭 10 件ではなく、典型例・幅を見せる例・境界例を分ける設計が必要。
- FPS / embedding 類似度 / max coverage / 全件入力は同じ土俵の代替案ではない。まず全件入力で sampling 自体がボトルネックかを見てから、context / cost / evidence 設計に応じて選ぶ方がよい。

## Related Pages

- [[label-coverage-policy-2026-05-29]]
- [[label-quality-redesign-reset-2026-05-30]]
- [[label-refinement-input-scope-2026-05-29]]
- [[label-quality-rubric-evaluation-2026-05-29]]
- [[source-code]]

## Open Questions

- ユースケースを `全体傾向把握` / `少数重要論点発見` / `公開 UI の説明責務` のように分けるなら、各 mode の標準 artifact は何か。
- 全件入力を試す時、cluster size ごとの token / latency / cost をどの粒度で記録するか。
- UI と judge が共有する rep args artifact をどの step で生成するか。

## Updates

- 2026-05-30: ユーザー提供の Slack ログを source 化。
