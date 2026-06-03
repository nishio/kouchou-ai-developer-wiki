---
type: source
summary: "2026-06-03 に nishio が、blind A/B preference と presentation context 分解まで整理したラベル品質評価の改善計画を Wiki に書くべきか確認したメモ"
sources:
  - user-message-2026-06-03
---

## What it is

2026-06-03 の nishio からの確認を source 化したもの。

直前までの議論で、ラベル品質評価は単独 label 批評ではなく blind A/B preference とし、algorithm / process 由来を人間に隠し、full UI 評価は困難なので `label_only` / `sibling_label_set` / `label_with_representatives` に分解する方針になった。これを受けて、改善計画として Wiki にまとめるか、という確認である。

## Extracted Points

- 既存のロードマップ追記だけでは、次に何を実装・実験するかが散らばる。
- 改善計画は、抽象方針ではなく、次の PR / script / artifact / evaluation flow に落とす必要がある。
- 計画には、blind A/B、presentation context、human preference、judge calibration、実験結果の保存先を接続する必要がある。

## Related Pages

- [[human-pairwise-label-preference-experiment-2026-06-02]]
- [[cli-pipeline-experiment-roadmap-2026-06-02]]
- [[clustering-labeling-comparison-corpus-2026-06-02]]
- [[experiment-result-storage-policy-2026-06-02]]

## Open Questions

- 改善計画を GitHub issue 化する時、既存 `#881` に集約するか、新しい implementation issue を切るか。
- 最初の implementation slice は bundle generator だけにするか、human preference export まで含めるか。

## Updates

- 2026-06-03: 初版作成。
