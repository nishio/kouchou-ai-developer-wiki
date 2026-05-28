---
type: analysis
summary: "`LLM grouping` された 422 argument の 2D 可視化を `UMAP` / supervised UMAP / LDA / centroid-MDS で試した結果、embedding 由来散布図を主図にするより、cluster-first な semantic island map の方が要件に合うと分かった"
sources:
  - source-code.md
  - slack-niizuma-umap-kmeans-thread-2026-03-18.md
  - slack-kouchouai-algorithm-dev.md
---

## What Changed

`work/kouchou-ai-mst-visualization-prototype/` で、`jigsaw_sample_comments_400_config` の 422 argument / 8 clusters を対象に可視化の試作を複数系統で比較した。対象は current `analysis-core` の `hierarchical_result.json` と `embeddings.pkl` で、最終表示は prototype 側 `report-mst-prototype.html` に逐次反映した。[[source-code]]より

試した系統は大きく 5 つだった。

1. 元の 2D `UMAP` 上に MST / bridge を重ねる graph overlay
2. `LLM grouping` label を教師信号にした supervised UMAP
3. core point だけ教師信号を残す semi-supervised UMAP
4. `LinearDiscriminantAnalysis` による 2D 判別空間
5. cluster-first な semantic island map

## Main Finding

今回の要件では、**embedding 由来 2D 散布図を主図にするのは筋が悪い**。より正確には、`LLM grouping` の所属を優先したい要求と、embedding 空間の近傍構造を 2D に保ちたい要求が衝突していた。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

実験で起きたことは一貫していた。

- supervised UMAP を強く掛けると cluster は分かれるが、全体が不自然に離れ、cluster 内がスカスカになりやすい
- weight を下げると今度は境界点が他 cluster に参加して見え、所属の可読性が落ちる
- semi-supervised UMAP は「離れすぎ」と「混ざりすぎ」の妥協にはなったが、最終図として読むにはまだ不安定
- LDA は強い判別軸を 2 本だけ抜くので、一部 cluster は綺麗に分かれる一方、残りが同じ側で団子になりやすい
- centroid-MDS + local PCA も、cluster-first の方向としては前進だが、最終的に「点が必ず所属クラスタの領域にいる」という保証を持たない限り、混ざりの違和感が残る

この結果は、`UMAP` を分析 artifact と表示 artifact の両方に使うと責務が衝突する、という既存の問題意識と揃う。[[slack-kouchouai-algorithm-dev]]より [[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

## Why Semantic Island Map Worked Better

一番ましだったのは、**cluster 間配置と cluster 内配置を分離し、点を必ず所属クラスタの「島」に閉じ込める** semantic island map だった。[[source-code]]より

prototype では次のように作った。

- cluster 間は高次元 embedding 上の cluster centroid 距離を `classical MDS` で 2D に置く
- cluster ごとに island の中心を持ち、必要なら軽く overlap 解消する
- cluster 内は高次元 residual を `local PCA` で 2D にして、その形を小さく正規化して島の中へ置く
- 1 点 = 1 意見は維持するが、点は所属 cluster の外へ出さない

この方式では、点同士のユークリッド距離を「そのまま意味距離」とは読めない。代わりに、

- どんな cluster があるか
- 各 cluster の量はどれくらいか
- cluster 内でどの点が中心寄りか / 周縁寄りか

を優先して読める。今回の試行では、これが最も user intent に近かった。

## Practical Implication

今後の可視化設計は、主図と診断図を分けて考えるのがよい。

- **主図**: semantic island map のような cluster-first view
- **診断図**: raw UMAP / supervised UMAP / LDA など、embedding と label のズレを観察する補助図

特に `LLM grouping` のような「所属は意味分類、geometry は embedding」な mode では、散布図を canonical output とみなすより、**所属・量・代表性・境界性を読ませる主図** を別に持つ方が product 的にも説明責務的にも安全である。[[slack-kouchouai-algorithm-dev]]より

## Open Questions

- semantic island map で cluster 間の 2D 配置を何で決めるのが一番説明しやすいか。embedding centroid 距離は基準線にはなるが、人間に意味が伝わるとは限らない
- cluster 内配置を `local PCA` のままにするか、密度均一化した packing や代表性順の radial layout に寄せるか
- public viewer の plugin system に入れるなら、`analysis_capabilities` / chart `requirements` とどう結びつけるか

## Updates

- 2026-05-26: `work/kouchou-ai-mst-visualization-prototype/` で MST overlay, supervised UMAP, semi-supervised UMAP, LDA, centroid-MDS を順に比較し、最終的に semantic island map を採用する判断を記録
