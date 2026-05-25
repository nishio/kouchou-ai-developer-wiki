---
type: source
summary: "2026-Q1 の tokoroten による spectral clustering メモ。TTTC は小さめ `n_neighbors` で紐状分離を作り、SpectralClustering で切っているのではないか、という読み"
sources:
  - slack-kouchouai-algorithm-dev.md
  - slack-dev-kouchouai-2026-q1.md
  - tttc-spectral-clustering-code-observation-2026-05-25.md
---

## What it is

`work/oss_weekly_reporter/data/2026-02-11_to_2026-02-18/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` と  
`work/oss_weekly_reporter/data/2026-03-04_to_2026-03-11/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` にある、tokoroten の短いが示唆の大きい spectral clustering メモをまとめた source。[[slack-kouchouai-algorithm-dev]]より

近接文脈として、`#2_開発_広聴ai` 2026-02-04 週の nishio による「クラスタリング手法を切り替え可能にする」整理も併読すると意味が通る。そこでは TTTC 的 spectral clustering は、

- 散布図は残る
- ただし階層掘り下げがなくなる
- 飛地ができるケースがある

という別モード候補として位置づけられていた。[[slack-dev-kouchouai-2026-q1]]より

## Key Messages

### 1. 2026-02-11: `n_neighbors` を小さくすると分離しやすくなり、そこを spectral で切るのが TTTC っぽい

tokoroten は、本の図表を整えるために `UMAP` パラメータを試していた流れで、

- `UMAP` の `n_neighbors` を小さくするとクラスタが分離しやすい
- TTTC はその分離を `spectral clustering` で切断する方針に見える

と述べている。[[slack-kouchouai-algorithm-dev]]より

### 2. 2026-03-09: 実装参照つきで、TTTC は `n_neighbors=10`、広聴AIは `15`

tokoroten は TTTC と広聴AIのコード位置を貼り、

- TTTC の `n_neighbors` は `10`
- 広聴AI の `n_neighbors` は `15`

と比較したうえで、TTTC は紐状クラスタを作りやすく、それを `SpectralClustering` で切断しているという理解は「あながち間違いではなさそう」と補足している。[[slack-kouchouai-algorithm-dev]]より

このうち、**TTTC が `UMAP` 後に `SpectralClustering` を掛け、`n_neighbors` 上限が 10 であること**、および **広聴AI側の default `n_neighbors` が 15 であること** は後日コード一次参照でも確認できる。[[tttc-spectral-clustering-code-observation-2026-05-25]]より

## Why this matters

このメモの価値は、TTTC の spectral clustering を単に

- `k-means` の代替
- 高次元でのより賢いクラスタリング

として理解していない点にある。  
むしろ tokoroten は、**2D 散布図上で分離しやすい幾何を `UMAP` 側で作り、その形を spectral で切る** ものとして読んでいる。[[slack-kouchouai-algorithm-dev]]より

つまり spectral clustering は、純粋な clustering quality の改善策というより、**散布図で見た時の形を前提にした cut 手法** として理解されていたことになる。

## Verification Status

この source が記録しているのは、**tokoroten が 2026-Q1 にそう読んでいた** という事実であり、TTTC 側の設計意図そのものがこれで確定するわけではない。  
したがって本ページの価値はまず「当時の開発側解釈の記録」にある。TTTC の真の意図や実装実態を確定したいなら、別途 primary source での検証が必要。[[slack-kouchouai-algorithm-dev]]より

重要度も二段に分けて考えた方がよい。

- **高い重要度**: 広聴AI側が TTTC をどう理解し、その理解の上で次の設計案を考えていたか
- **中程度の重要度**: その理解が TTTC 本家の意図や挙動とどこまで一致していたか

2026-05-25 時点の primary source 検証により、**実装形 (`UMAP -> SpectralClustering`, `n_neighbors <= 10`) までは確認済み**、一方で **「紐状構造を作って切るのが方針」という意図読みは未確定**、という線引きができる。[[tttc-spectral-clustering-code-observation-2026-05-25]]より

## Related Pages

- このメモの含意を整理した page は [[tokoroten-spectral-clustering-reading]]
- 近接する broader 文脈は [[slack-design-intents-2026-q1]]
- TTTC / scatter / Turbo の系譜は [[talk-to-the-city]]

## Open Questions

- tokoroten の「TTTC の方針っぽい」という読みが、TTTC 側の設計意図とどこまで一致しているかは、この Slack source 単体からは断定できない
- `n_neighbors=10` と `15` の差が実運用でどの程度大きいかは、別途実験観測が必要
- spectral clustering を current `kouchou-ai` へ戻す場合、scatter-first な利点と hierarchy loss をどう扱うかは未整理

## Updates

- 2026-05-25: tokoroten の spectral clustering メモを独立 source 化
