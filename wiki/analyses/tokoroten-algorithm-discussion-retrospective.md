---
type: analysis
summary: "tokoroten とのアルゴリズム議論は、クラスタリング手法の優劣ではなく、散布図プロダクト・深い分析・説明責務・運用ワークフローを分け直す議論だった"
sources:
  - kouchou-ai-direction-2025-12-06.md
  - kouchou-ai-direction-2-2025-12-13.md
  - slack-kouchouai-algorithm-dev.md
  - slack-tokoroten-spectral-clustering-notes-2026-q1.md
  - slack-niizuma-umap-kmeans-thread-2026-03-18.md
  - tttc-spectral-clustering-code-observation-2026-05-25.md
  - jigsaw-llm-grouping-experiment-output-2026-05-25.md
---

tokoroten とのアルゴリズム議論を振り返ると、表面上は `UMAP`、`k-means`、`HDBSCAN`、`SpectralClustering`、Jigsaw / Sensemaker の比較に見える。  
しかし本質は、**広聴AIが何を成果物として約束しているのかを分解し直す議論** だったと読む方がよい。

## 1. tokoroten の初期批判は「精度が低い」ではなく「用途を間違えると危ない」だった

2025-12-06 の方向性メモで tokoroten は、現行アルゴリズムでは少数意見が消えやすく、定性分析としても十分ではない、とかなり強く言っている。  
同時に、散布図やアートは説得力を生む一方で、精度を悪化させる面があるとも見ている。[[kouchou-ai-direction-2025-12-06]]より

ここで重要なのは、tokoroten が単に「現行 clustering が悪い」と言っていたわけではないことだ。  
彼の批判は、**行政・政治家・実務家が深い insight や少数意見救済を期待するなら、散布図を切ってラベルを付ける方式をそのまま使うのは危うい** という用途批判に近い。[[kouchou-ai-direction-2025-12-06]]より

この批判は、広聴AIの価値を否定しているというより、価値の範囲を絞っている。  
現行方式は「全体をざっくり眺める」「市民参加のきっかけを作る」には強いが、「深い定性分析」「対立構造の発見」「少数意見の救済」まで同じ成果物で担わせると無理が出る、という整理である。[[kouchou-ai-direction-2025-12-06]]より

## 2. 「別のアルゴリズムを入れる」だけでは、tokoroten の問題意識に答えられない

2025-12-13 の議論では、tokoroten は「アルゴリズムの限界、散布図から離れる必要がある」としつつ、それを突き詰めるなら別のアルゴリズムや別 platform が必要になる、と整理している。  
ただし本人はそれを今すぐ自分がやりたいわけではなく、現実ラインとしては stable v4 と別軸の次世代探索に寄せている。[[kouchou-ai-direction-2-2025-12-13]]より

これはかなり大事な分岐である。  
もし問題を「`k-means` を `HDBSCAN` に替える」程度に狭めると、tokoroten の批判を取り逃がす。実際の論点は、**散布図を中心にした product contract のまま、どこまで分析品質を約束してよいか** だった。[[kouchou-ai-direction-2-2025-12-13]]より

そのため、広聴AIを全部入り platform にするより、分析部分を pip package として切り出し、既存 BI ツールや現場ワークフローの一部として使えるようにする案が出ている。  
これは「アルゴリズムを強くする」より前に、広聴AIを **単体製品ではなく、声を集めて意思決定へつなぐ運用パッケージの一部** として再配置する発想である。[[kouchou-ai-direction-2-2025-12-13]]より

## 3. spectral clustering の話は、正解アルゴリズム発見ではなく TTTC 的 scatter UX の読みだった

tokoroten の 2026-Q1 spectral clustering メモは、TTTC が `UMAP` 後に `SpectralClustering` している点を見ている。  
ただし彼の読みは、「高次元で正しく clustering している」ではなく、`UMAP` の `n_neighbors` を小さくして分離しやすい形を作り、それを spectral で切っているのではないか、というものだった。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

後で historical code を見ると、TTTC が `UMAP -> SpectralClustering` をしており、`n_neighbors` 上限が 10 であることは確認できた。  
一方で、「紐状構造を意図的に作って切るのが方針」という部分は依然 inference である。[[tttc-spectral-clustering-code-observation-2026-05-25]]より

この線引きから分かるのは、TTTC 的 spectral clustering も「散布図の外に出る正解」ではなかった可能性が高い、ということだ。  
むしろ tokoroten は、TTTC もまた scatter-first な UX をどう成立させていたか、という観点で読んでいた。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

## 4. 新妻 thread と LLM grouping 実験を経ると、議論の分解線がはっきりする

2026-03 の新妻 thread では、`UMAP` 後 `k-means` の幾何的な危うさ、先に clustering してから 2D 表示する案、supervised `UMAP`、LLM 直分類、説明責務が一気に出ている。  
この thread は、アルゴリズム論争が **幾何の自然さ・散布図での受容性・外部説明責務** の衝突だと示している。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

さらに 2026-05-25 の LLM grouping 実験では、LLM grouping は label semantics では強い一方、embedding 由来の 2D scatter とは相性が悪いことが観測された。  
逆に従来 hierarchical clustering は scatter geometry では強いが、ラベル集合の読みやすさでは別評価が必要だった。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より

これを踏まえると、tokoroten との議論の着地点は「よりよい単一アルゴリズム」ではない。  
少なくとも次の 3 artifact を分けるべき、という方向に見える。

- **分析 artifact**: どの意見をどの論点群として扱うか。ここでは 2D 散布図の近さだけを根拠にしない
- **表示 artifact**: 非専門家が全体像を掴み、個別意見へ辿るための UI。ここでは散布図の分かりやすさは価値だが、分析根拠と混同しない
- **説明 artifact**: 報道・自治体・外部レビューに対して、なぜそう分けたかを説明する材料。代表意見、境界例、分類基準、prompt、seed、パラメータを残す

この分解は、新妻 thread の説明責務と、tokoroten の「用途を間違えると危ない」という初期批判を同時に受け止める形になる。[[kouchou-ai-direction-2025-12-06]]より [[slack-niizuma-umap-kmeans-thread-2026-03-18]]より

## 5. 今振り返っての考察

自分の理解としては、tokoroten との議論で一番価値があったのは、**広聴AIの魅力と限界を同時に言語化したこと** だと思う。  
散布図は強い。見た目がよく、参加感を作り、全体像を一画面で掴ませる。ただし、その強さを「深い分析ができている」という約束に読み替えると危ない。[[kouchou-ai-direction-2025-12-06]]より

tokoroten はそこを早い段階から突いていた。  
「少数意見が潰れる」「カテゴリを切ってから分類する方が筋がよい」「現行方式にモチベーションが切れている」という発言はきつく見えるが、今読むと、散布図 product への失望というより **散布図 product に背負わせすぎていた期待の剥がし** だった。[[kouchou-ai-direction-2025-12-06]]より

一方で、現行広聴AIを捨てる話でもなかった。  
2025-12-13 の収束は、stable v4 として現行価値を守りつつ、次世代の分析・運用ワークフローは別軸で試す、というものだった。[[kouchou-ai-direction-2-2025-12-13]]より

したがって今後の実装判断では、次の態度がよい。

- `classic_scatter` は agenda discovery / 参加感 / 全体俯瞰の mode として守る
- `llm_grouping` や Jigsaw 系は、散布図互換ではなく group-first / explanation-first の mode として育てる
- `SpectralClustering` や `HDBSCAN` は「正解」ではなく、どの artifact を改善するかを明示して試す
- deep insight や少数意見救済を売るなら、入力収集プロセス、分類基準、説明 artifact まで含めて設計する

つまり tokoroten との議論は、「アルゴリズム改善」から「成果物の契約設計」へ視点を移すための重要な摩擦だった。

## Open Questions

- stable v4 の公開説明では、散布図の価値と限界をどこまで明示するべきか
- `analysis-core` の schema で、分析 artifact / 表示 artifact / 説明 artifact をどう分けて表現するか
- Jigsaw / Sensemaker 系 mode は、散布図を持たない前提でどの viewer を first-class にするべきか
- 少数意見救済を主張する場合、どの評価データセットと観測指標を標準にするべきか

## Updates

- 2026-05-25: tokoroten とのアルゴリズム議論を、散布図 product と分析・説明責務の分離として振り返った
