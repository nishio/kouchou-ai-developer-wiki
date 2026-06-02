---
type: source
summary: "2026-06-02 に nishio が、実験をやってみることは大事だが、current main から一度に多くの要素を変えると解釈が難しいため、今後は 1 要素ずつ変えた実験にすべきだと指摘したメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの追加メモを source 化したもの。

要点は、実験をやってみること自体は大事で、既存 artifact を比較コーパスへ移したことにも価値がある。一方で、current `main` から一度にいろいろなものを変えると、結果の解釈が難しくなる。今後の採用判断に使う実験は、**1 要素ずつ変えた実験** にするべき、という指摘である。

## Extracted Points

- 実験は机上で止めず、実際にやってみることが重要。
- ただし、`main` から clustering、tree shape、labelling prompt、evidence policy、judge などを同時に変えると、どれが結果差の原因か分からない。
- 既存 artifact から作った比較コーパスは、観察軸を見つける探索 corpus としては有用だが、そのまま causal な採用根拠にしてはいけない。
- 今後の clean experiment では、baseline を current `main` に置き、`factor_under_test` を 1 つだけ明示する。
- 複数要素を同時に変えた run は、`exploratory` と明記し、仮説生成・judge calibration・failure mode 発見に使う。

## Related Pages

- [[cli-pipeline-experiment-roadmap-2026-06-02]]
- [[clustering-labeling-comparison-corpus-2026-06-02]]
- [[experiment-result-storage-policy-2026-06-02]]
- [[llm-grouping-400-tree-label-corpus-2026-06-02]]

## Open Questions

- `factor_under_test` / `fixed_inputs` / `changed_inputs` を `manifest.json` に必須項目として入れるか。
- 複数要素が変わった実験を、どの時点で exploratory から clean experiment に切り直すか。
- tree を変える実験では label output も従属的に変わるが、それを「1 要素変更」として扱うための固定条件をどう書くか。

## Updates

- 2026-06-02: 初版作成。
