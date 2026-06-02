---
type: source
summary: "TTTC / 広聴AI の clustering 議論を外部研究で検証するための survey seed 集。UMAP 後 clustering、spectral clustering、BERTopic、可視化と分析の分離、評価軸"
sources:
  - slack-niizuma-umap-kmeans-thread-2026-03-18.md
  - slack-tokoroten-spectral-clustering-notes-2026-q1.md
  - tttc-spectral-clustering-code-observation-2026-05-25.md
---

## What it is

2026-05-25 に、広聴AI / TTTC の clustering 議論を Deep Research する前段として作った survey seed 集。  
目的は「いきなり TTTC の意図を断定する」のではなく、**どの論点に対して既存研究や既存実務議論を当てるべきか** を先に棚分けすることにある。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より [[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

## Survey Buckets

### 1. `UMAP -> clustering` の妥当性と限界

見るべき問いは、

- 2D 可視化用 `UMAP` にそのまま clustering を掛けてよいか
- clustering 用なら何次元程度まで落とすのがよいか
- `n_neighbors` が cluster shape や separation にどう効くか

である。  
この棚は、新妻 thread の `UMAP` 後 `k-means` 批判と直結する。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

候補:

- UMAP docs `Using UMAP for Clustering`
- Eklund et al. 2023 *An Empirical Configuration Study of a Common Document Clustering Pipeline*

### 2. 次元圧縮と clustering を混同すると何が危ないか

ここでは `UMAP` だけでなく、可視化 embedding と analysis clustering を同一視する危険一般を押さえる。  
問いは、

- scatter 上でよく分かれて見えることと clustering quality は同じか
- 2D visualization artifact を cluster structure と誤認しないために何を区別すべきか

である。  
新妻 thread と tokoroten spectral 読みの両方に関係する。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より [[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

候補:

- UMAP docs
- t-SNE / low-dimensional visualization caution literature

### 3. spectral clustering は何を最適化する手法として理解すべきか

問いは、

- high-dimensional semantic similarity を切る手法なのか
- nearest-neighbor graph 上の shape / connectivity を切る手法なのか
- `k-means` と比べて何が強く、何が説明しにくいのか

である。  
この棚は tokoroten の「TTTC は紐状構造を spectral で切っているのでは」という読みを検証するための中心になる。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より [[tttc-spectral-clustering-code-observation-2026-05-25]]より

候補:

- spectral clustering の explainability / interpretability 論文

### 4. BERTopic 系 pipeline はどこで clustering をしているのか

TTTC の historical code では `BERTopic`, `HDBSCAN`, `UMAP`, `SpectralClustering` が併存していた。  
したがって survey では、

- BERTopic 標準系は何を intended path にしているか
- topic representation と final cluster assignment がどう分かれているか

を見る必要がある。[[tttc-spectral-clustering-code-observation-2026-05-25]]より

候補:

- BERTopic paper / docs

### 5. 可視化と分析を分けるべきだ、という研究・実務議論

問いは、

- semantic truth に近い cluster と、scatter 上で納得感のある shape は両立するか
- 両立しないなら、view artifact と analysis artifact をどう分けるべきか

である。  
これは `TTTC vs 広聴AI vs LLM grouping` の product 設計にも直結する。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より [[tttc-spectral-clustering-code-observation-2026-05-25]]より

### 6. 何をもって「良い clustering」とするか

最後に survey では評価軸自体を分ける必要がある。

- geometry: silhouette, ARI, NMI など
- label semantics: readability, specificity, representativeness
- UX: 飛地の少なさ、drill-down しやすさ、説明責務

新妻 thread と current `LLM grouping` 実験が示しているように、これらは同じ winner を返さない可能性がある。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

## Practical Search Prompts

- `document clustering UMAP KMeans HDBSCAN empirical study`
- `UMAP clustering caution 2D visualization clustering`
- `spectral clustering text embeddings explainability`
- `BERTopic UMAP HDBSCAN clustering pipeline`
- `dimensionality reduction before clustering pitfalls text embeddings`

## Related Pages

- survey 計画の analysis は [[clustering-research-survey-plan]]
- 背景論点は [[niizuma-thread-algorithm-critique]] と [[tokoroten-spectral-clustering-reading]]

## Open Questions

- broad listening / civic tech の文脈に特有の explainability 論点を、一般 document clustering 文献だけでどこまでカバーできるか
- spectral clustering の実務 UX 論点は、機械学習論文より visualization / HCI 側も読むべきか

## Updates

- 2026-05-25: Deep Research 前段として survey bucket と検索軸を整理
- 2026-05-25: nishio ↔ GPT のブレスト 2 本（[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]] / [[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]]）が、これらの bucket への deep-research 応答にあたる。`UMAP -> clustering` の妥当性、15D〜25D 推奨、`n_neighbors` のデータ依存、BERTopic の現代的位置づけ、小規模 N での LLM pairwise + spectral 設計が答えた。整理は [[clustering-deep-research-findings-2026-05-25]]
