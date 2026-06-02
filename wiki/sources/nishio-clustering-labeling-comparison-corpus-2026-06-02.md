---
type: source
summary: "2026-06-02 に nishio が、各種 clustering method が作る tree と、その tree を入力にした各種 summarization / labelling process のラベルを蓄積・比較できるようにすべき、judge 改善以前に現状が曖昧すぎると指摘したメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの追加メモを source 化したもの。

要点は、品質 judge を改善する前に、まず **各種クラスタリング方法でどのような tree ができたのか**、その tree を入力として **各種の要約 / ラベリングプロセスでどのような label ができたのか** を、しっかり蓄積して比較できるようにした方がよい、という指摘である。

現状は judge 改善を考えようとしても、比較対象・入力 tree・ラベリング手順・出力 label・人間の違和感が十分に固定されておらず、曖昧すぎる。

## Extracted Points

- `clustering method` と `labelling process` を同時に変えると、どちらが品質差の原因か分からない。
- まず tree そのものを保存し、「この clustering method / params ではこういう親子構造になった」を比較できる必要がある。
- 次に同じ tree を入力として、複数の summarization / labelling process を走らせ、label set の違いを比較する必要がある。
- judge 改善は、この比較コーパスがあって初めて具体化できる。現状のまま rubric を磨いても、何を正解に寄せるのかが曖昧なままになる。

## Related Pages

- [[cli-pipeline-experiment-roadmap-2026-06-02]]
- [[llm-grouping-experiment]]
- [[llm-grouping-experiment-output-2026-05-25]]
- [[label-quality-redesign-reset-2026-05-30]]
- [[label-quality-rubric-evaluation-2026-05-29]]

## Open Questions

- tree 比較の最小単位は `hierarchical_clusters.csv` / `hierarchical_merge_labels.csv` で足りるか、それとも normalized tree JSON が必要か。
- labelling process の provenance は prompt text、model、sample/evidence、tree input hash のどこまで残すべきか。
- 人間の違和感メモはどの粒度で保存するか。cluster 単位、label set 単位、tree 単位のどれを主にするか。

## Updates

- 2026-06-02: 初版作成。
