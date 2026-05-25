---
type: analysis
summary: "TTTC / 広聴AI の clustering 議論を外部研究で検証するには、`UMAP -> clustering`、spectral clustering、BERTopic、可視化と分析の分離、評価軸を別棚で読むべき"
sources:
  - clustering-research-survey-seeds-2026-05-25.md
  - niizuma-thread-algorithm-critique.md
  - tokoroten-spectral-clustering-reading.md
---

TTTC / 広聴AI の clustering 議論を Deep Research したい時、最初にやるべきなのは論文を無差別に集めることではない。  
先に **何を検証したいのか** を棚分けしないと、`UMAP` の caution、spectral clustering の一般論、topic modeling の実装事情、公開説明責務の話が全部混ざる。[[clustering-research-survey-seeds-2026-05-25]]より

## 1. 最優先は `UMAP -> clustering` の妥当性

いま一番強く検証したいのは、新妻 thread の中心論点である

- `UMAP` 後に `k-means` を掛けてよいのか
- 2D 可視化用 `UMAP` と clustering 用 `UMAP` を分けるべきか
- `n_neighbors` をどう読むべきか

である。[[niizuma-thread-algorithm-critique]]より

この棚では、理論論文よりもまず

- UMAP 公式 docs の caution
- document clustering pipeline の empirical comparison

を押さえる方が効率がよい。  
ここで 2D clustering 自体がかなり不利だと出るなら、広聴AI / TTTC の比較も「どちらがより自然か」より前に、「どちらも scatter-first な妥協なのでは」という読みが強くなる。

## 2. spectral clustering は独立棚で読むべき

tokoroten の読みで面白いのは、「TTTC は spectral を使っている」ことより、「その spectral は `UMAP` 側で作られた 2D 幾何を切っているのでは」という推測である。[[tokoroten-spectral-clustering-reading]]より

この論点を検証するには、

- spectral clustering の数学的性質
- nearest-neighbor affinity を使う時の意味
- non-spherical shape に強いという通説
- explainability の弱さ

を別棚で見る必要がある。  
ここは `UMAP` caution literature とは目的が違うので、混ぜずに読んだ方がよい。

## 3. BERTopic は implementation detail ではなく、解釈の攪乱要因

TTTC の code observation では `BERTopic`, `HDBSCAN`, `UMAP`, `SpectralClustering` が同居していた。  
このため survey では、BERTopic を単なる周辺ツール扱いせず、

- BERTopic が本来どこで cluster assignment を持つか
- topic labeling と final cluster-id が分離しうるか

を押さえるべきである。[[clustering-research-survey-seeds-2026-05-25]]より

これを読まないと、「TTTC は HDBSCAN 系なのか spectral 系なのか」という問い自体を雑に立ててしまう。

## 4. 可視化と分析の分離は、論文より design principle として読む

新妻 thread と tokoroten spectral 読みはどちらも、結局は

- clustering as semantic grouping
- scatter as public-facing shape

の衝突を示している。[[niizuma-thread-algorithm-critique]]より [[tokoroten-spectral-clustering-reading]]より

したがって survey では、純粋な ML 精度比較だけでなく、

- 可視化 embedding は explanation artifact と割り切るべきか
- analysis artifact と view artifact をどう分離するか

という design principle も読むべきである。  
この棚は broad listening product 設計に直結するので、文献 survey だけでなく後で wiki の概念ページにも戻しやすい。

## 5. 評価軸を混ぜない

この survey でいちばん避けたい失敗は、「精度が高い」「見やすい」「説明しやすい」を同じ勝敗で扱うことである。  
少なくとも次は分けるべきだ。

- geometry
- label semantics
- public explanation / accountability
- UI / UX

これは current `LLM grouping` 実験でも既に露出している構図であり、survey でも同じ整理を保つべきである。[[clustering-research-survey-seeds-2026-05-25]]より

## Practical Read Order

1. UMAP docs `Using UMAP for Clustering`
2. document clustering pipeline の empirical study
3. spectral clustering の explainability / interpretability 論文
4. BERTopic paper
5. visualization vs analysis の caution literature

この順なら、先に「現在の争点に効く強い一次主張」を押さえてから、周辺理論で肉付けできる。

## What to Do Next

survey の次段として妥当なのは 2 本ある。

1. TTTC 側の他 commit / issue / docs を掘り、spectral と `n_neighbors` の意図説明を探す  
2. current `analysis-core` 上で `UMAP -> SpectralClustering` を再現して、scatter / label / hierarchy の挙動を比較する

今回の時点では、まず 1 を優先し、2 は possibility としてメモしておくのが筋である。

## Open Questions

- broad listening 文脈特有の説明責務は、一般 document clustering 文献の外に専用文献があるか
- spectral clustering を civic tech / public communication 文脈で比較した既存議論があるか

## Updates

- 2026-05-25: Deep Research 前に、survey を `UMAP`, spectral, BERTopic, 可視化分離, 評価軸へ棚分けする計画を整理
- 2026-05-25: nishio ↔ GPT の 2 本のブレスト（[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]] / [[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]]）を deep-research 応答として吸収。bucket 1 (UMAP→clustering) は「2D 用と 15D〜25D の分離が筋」、bucket 3 (spectral) は「数十件規模では LLM pairwise + spectral / agglomerative」、bucket 4 (BERTopic) は「backbone + LLM labeler への位置ずれ」と整理。詳細は [[clustering-deep-research-findings-2026-05-25]] へ filing back。Read order に LLM-as-pairwise-judge / 概念誘導系 (LLooM, TopicGPT) / ACL 2025 NIST 論文を追加すべきと記録
