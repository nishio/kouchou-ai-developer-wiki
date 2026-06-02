---
name: gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25
summary: "2026-05-25 の nishio ↔ 外部 GPT 対話。データ量が数十件規模の時、LLM に N:N 類似度を出させて spectral clustering する案を検討。LLM-as-pairwise-oracle + 対称化・校正・疎化した affinity graph + spectral/agglomerative の設計を推奨"
type: source
sources:
  - gpt-umap-clustering-bertopic-deep-research-2026-05-25.md
---

## What it is

2026-05-25 に `raw/gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25.txt` として保存した GPT 出力。  
nishio の問い「数十件規模で N:N の類似度を LLM で出した上で spectral clustering する案について検討して」に対する応答。  
Viswanathan et al.（LLM を clustering の前・中・後に組み込む手法比較）、scikit-learn `SpectralClustering(affinity='precomputed')`、A Survey on LLM-as-a-Judge、Optimized Algorithms for Text Clustering with LLM-Generated Constraints (AAAI 2025) などを引用している。

## Key Points

### 1. 案そのものは数十件規模で「かなり検討に値する」

有効な条件:

- N が 20〜80 程度（N=50 でも unordered pair 1,225 件で全ペア比較が現実的）
- クラスタリング基準を自然言語で説明できる（rubric として LLM に渡せる）
- embedding cosine では粗すぎる（topic / stance / 意図 / 価値判断 / 提案内容を区別したい）
- 監査可能性が欲しい（各 edge に LLM の短い理由を付けられる）
- 2D UMAP の見た目より、意味的同一性を重視する

特に broad listening / Slack 議論 / 短文コメント分類では、embedding は「同じ語彙・同じ話題」に反応しやすいが、**同じ論点か、同じ立場か、同じ要望か、同じ原因認識か** を混同しやすい。LLM pairwise scoring はそこを rubric で制御できるのが利点。

### 2. spectral clustering 自体は precomputed affinity と相性がよい

- scikit-learn `SpectralClustering(affinity='precomputed')` でユーザ定義 affinity matrix を渡せる。値は非負・大きいほど類似であればよい。
- 近年の survey でも、spectral clustering の最初で最重要のステップは、同一クラスタ内では強く・異なるクラスタ間では弱い pairwise similarity matrix を作ることだと整理されている。
- 本質は **LLM を clustering 器として使うのではなく、グラフの edge weight 生成器として使う** こと。

### 3. ただし「類似度を 0〜100 で出して」は危ない（4 つのリスク）

- A. **LLM の絶対スコアは校正されにくい**：同じ「70 点」でもペアごとに意味が変わる。モデル・プロンプトで分布が変わる。
- B. **順序バイアス**：(A, B) と (B, A) で異なる判定。
- C. **推移律違反**：A〜B 強、B〜C 強でも A〜C 弱を返しうる。
- D. **rubric ドリフト**：プロンプトの揺れで類似度の意味が変わる。

### 4. 推奨設計：連続スコアではなく 0–4 の離散ラベル + 関係タイプ

- `0=同じでない`, `1=ほぼ別`, `2=部分的に重なる`, `3=明らかに同じ論点`, `4=ほぼ同一` のような **離散ラベル**にする。
- 連続スコアより校正しやすく、人間検品もしやすい。
- 関係タイプを `same_topic / same_stance / same_request / cannot_judge / unrelated / cannot_link` のように出させ、rubric を 1 つに固定する（混ぜると壊れる）。
- 各ペアに `confidence` と short `reason` を必ず付ける（後の監査用）。

### 5. graph 構築：対称化・閾値疎化・自己ループ排除

- (A, B) と (B, A) を両方判定し、最小値を採用するなどで対称化。
- score 3 以上だけを edge にする保守化、score 1〜2 は edge に入れない。
- 必要に応じて k-NN sparsification（各ノードから top-k のみ残す）。
- これで spectral clustering 入力としての品質を担保する。

### 6. k の決め方と graph 分断への対応

- eigengap を見る。
- k を 2〜8 でスキャンし、各 k で LLM に cluster label を出させ、人間が「分かれすぎ／粗すぎ」を判定。
- N=30〜50 なら最初は `k=3〜7` から。
- threshold が強すぎて connected components に分かれた場合は、components が意味的に自然ならそれを粗クラスタにするか、threshold を緩めるか、孤立点・bridge node を「境界文書」として扱う。

### 7. cannot-link を強く守りたいなら spectral より別手法

- 普通の spectral clustering は **正の affinity を切る** 手法。`cannot-link` を強制的に「別クラスタ」にする力は弱い。
- cannot-link 重視なら must-link / cannot-link constrained clustering、correlation clustering、ILP / local search の方が合う。
- これは AAAI 2025 *Optimized Algorithms for Text Clustering with LLM-Generated Constraints* の方向。

### 8. 推奨プロトコル（最小構成）

1. rubric を 1 つに固定する
2. 全ペアを LLM 判定して `score / relation / confidence / reason` を JSON 取得
3. 10〜20%（または小 N なら全件）を swapped order で再判定
4. score 3 以上だけを edge に
5. spectral clustering と agglomerative を両方試す
6. LLM に各クラスタの label を生成させる（代表文書 + 境界文書を渡す）
7. 人間が edge とクラスタを確認（特に LLM `reason` が弱い edge、swapped で揺れた edge、bridge node）
8. 必要なら merge/split

### 9. 評価軸

- ARI/NMI は使えるなら使う。少量データでは **人間によるクラスタ意味の確認** の方が重要。
- pairwise disagreement (swapped 判定が変わる edge 数)、stability (prompt / model / edge dropout で保たれるか)、graph structure（components、bridges、weak cuts）、human spot-check を併用。

### 10. 結論

**少量データでは BERTopic 的 `embedding → UMAP → HDBSCAN` より、LLM pairwise graph → spectral/agglomerative の方が筋がよい場面がある**。  
ただし spectral にこだわる必要はなく、LLM pairwise graph を作った時点でかなり価値がある。spectral / 階層 / connected components + 手動 merge/split は目的に応じて選べる。

## Compared to existing wiki claims

- [[llm-grouping-experiment-output-2026-05-25]] の 400 件規模 `analysis_mode=llm_grouping` 実験とは別の **小規模（数十件）向け代替設計** を提示している。
- [[tokoroten-spectral-clustering-reading]] が「TTTC 的 spectral は scatter-first」と読んだのに対し、ここでの spectral は **明示的に高次元 affinity graph を切る** 手法として使われる。同じ「spectral」でも意図が違う。
- [[niizuma-thread-algorithm-critique]] の「分析 artifact と表示 artifact を分ける」「LLM 直分類でも説明責務が残る」読みと整合する：LLM pairwise graph は各 edge に `reason` を残せるため、説明 artifact として強い。

## Open Questions

- チームみらいの 300 件規模分析（[[nishio]] が "vive 広聴AI" として実践）で、この LLM pairwise + spectral を current `kouchou-ai` の代替経路として試した場合、どの評価軸でどれだけ違いが出るか。
- N が 100〜500 規模に増えた時、pair 数が爆発する（500 で約 125,000 件）。階層化・サンプリング・能動学習で pair 数を減らす設計は別途必要。
- `analysis-core` の plugin contract に「小規模 / LLM pairwise / spectral」モードを追加する場合、`analysis_mode=llm_pairwise_spectral` のようなラベルでよいか、それとも analysis_mode は scatter / grouping の 2 軸に絞り、内部 backend の switch にすべきか。

## Related Pages

- 並行ブレスト: [[gpt-umap-clustering-bertopic-deep-research-2026-05-25]] / [[gpt-mst-bridge-visualization-brainstorm-2026-05-25]]
- 類似手法の議論: [[tokoroten-spectral-clustering-reading]] / [[slack-tokoroten-spectral-clustering-notes-2026-q1]]
- 既存 LLM grouping 実験: [[llm-grouping-experiment-output-2026-05-25]] / [[llm-grouping-experiment]]
- 派生 analysis: [[clustering-deep-research-findings-2026-05-25]]

## Updates

- 2026-05-25: 初回作成
