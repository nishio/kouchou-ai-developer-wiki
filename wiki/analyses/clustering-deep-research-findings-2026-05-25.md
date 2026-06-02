---
name: clustering-deep-research-findings-2026-05-25
summary: "[[clustering-research-survey-plan]] が立てた survey bucket への 2026-05-25 時点の deep-research 応答。`UMAP -> clustering` は否定されないが 2D 用と clustering 用は分離（15D〜25D 推奨）、BERTopic は完成品から backbone へ、数十件規模は LLM pairwise + spectral が筋という整理"
type: analysis
sources:
  - gpt-umap-clustering-bertopic-deep-research-2026-05-25.md
  - gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25.md
  - clustering-research-survey-seeds-2026-05-25.md
  - clustering-research-survey-plan.md
---

[[clustering-research-survey-plan]] は 2026-05-25 の時点で、Deep Research に出す前に survey を `UMAP -> clustering`、spectral、BERTopic、可視化と分析の分離、評価軸の 5 棚に分けていた。  
その後の nishio ↔ GPT 対話 2 本（`UMAP/clustering/BERTopic` の深掘り、`LLM pairwise + spectral` の小規模ケース）は、その棚への一次的な応答として読める。  
この page では、survey bucket ごとに **何が裏付けられ、何が更新されたか** を整理する。

## 1. `UMAP -> clustering` の妥当性は否定されない。ただし 2D と clustering 空間は分けるべき

[[clustering-research-survey-seeds-2026-05-25]] の bucket 1 への応答として、Deep Research 系の答えは

- UMAP 公式 docs は HDBSCAN などの前処理として UMAP を使うこと自体には肯定的
- 同時に "false tears" による過細分化のリスクを caution している
- したがって **「UMAP を使うな」ではなく「可視化用 2D UMAP を clustering 空間と同一視するな」** が正しい読み

である。[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]より

この結論は [[broad-listening-book-extractions]] の「UMAP の 2D 結果でクラスタリングしているのは標準作法と異なる妥協」（書籍 13.2.4 の自認）と一致する。  
つまり広聴AI / TTTC の現状は「標準作法から外れている」が、その妥協の正体は **「散布図とクラスタの見た目を一致させる」要請** にあって、技術論ではなく product 要請が起点である。

## 2. clustering 用 UMAP は 15D〜25D が empirical な基準線

Eklund et al. 2023 は BERT + UMAP + KMeans/HDBSCAN をニュースデータで比較し、出力次元は **15D 以上** を、初期値として 15D〜25D を推奨している。2D から 10D〜15D に上げると性能が改善、その後は伸びが鈍る。[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]より

これは [[niizuma-thread-algorithm-critique]] の「`UMAP` 後 `k-means` 批判」への具体的な答えになる。新妻 thread の問題提起は「2D へ落とすこと自体が局所保存射影と centroid 距離の不整合を作る」だったが、**15D〜25D へ落とすという中間解** が研究側から示されている。

ただし対象データは英語ニュース・BERT 系。日本語短文コメントへの一般化は ablation 必須。  
current `analysis-core` で `n_components` を可変にして 15D〜25D を試す実験は、研究上は素直な次の一歩である。

## 3. `n_neighbors` は単一の正解値ではなく、データ依存

- UMAP 公式 docs: clustering 用には可視化用より大きめの `n_neighbors`、`min_dist` は小さめ
- Eklund et al. 2023: 文書埋め込みでは `n_neighbors` の影響は小さく、小さい方がよい場合も多い

両者は矛盾ではなく **画像・連続多様体 vs テキスト意味的近傍** の違い。[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]より

これは [[tokoroten-spectral-clustering-reading]] の「TTTC は小さめ `n_neighbors` で紐状分離を作り spectral で切っている」読みとも整合する：TTTC のチューニング自体は document clustering の研究上、無理筋ではない。ただし [[tttc-spectral-clustering-code-observation-2026-05-25]] が示すように、TTTC の `n_neighbors <= 10` は **意図的な選択** であり、その意図を再現するなら同様のチューニング戦略が必要になる。

## 4. BERTopic は陳腐化していないが、位置がずれた

bucket 4 （BERTopic 系 pipeline はどこで clustering をしているか）への応答は

- BERTopic 標準（c-TF-IDF + 代表語列）は LLM 系（TopicGPT, LLooM）に coverage / 可読性で劣る研究が複数（NSF/LLooM, ACL 2025/NIST）
- LLM 直分類は重い・shortcut・coverage 不足が残る
- 現実的設計は **clustering で代表文書を選び LLM に label / summary を生成させる**（BERTopic 公式 docs もこの flow を前提化）

である。[[gpt-umap-clustering-bertopic-deep-research-2026-05-25]]より

これは current `kouchou-ai` の `analysis_mode=llm_grouping` 設計と整合する。  
[[llm-grouping-experiment-output-2026-05-25]] が「LLM grouping は top-level label では強いが scatter 互換は悪い」と観測したのは、まさに **clustering backbone + LLM labeler という現代の落としどころ** に対応するパターンとも読める。

設計判断としては、

- BERTopic 系を捨てる必要はない（clustering backbone として残せる）
- ただし c-TF-IDF の topic 表現をそのままユーザに見せる UI は古い
- LLM labeler + interactive merge/split + 代表文書 + 境界事例を返す contract が必要

となる。これは [[llm-grouping-implementation-plan]] の方向（`analysis_mode` + `analysis_capabilities` + viewer `requirements`）と矛盾しない。

## 5. 数十件規模では LLM pairwise + spectral / agglomerative が筋

[[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]] は、survey の元 bucket には直接対応しないが、**N=20〜80 規模で BERTopic 的 pipeline を使うこと自体が不適切** という新しい論点を出した。

要点：

- spectral clustering は precomputed affinity と相性がよい（scikit-learn `affinity='precomputed'`）
- LLM pairwise scoring は連続スコアより **0〜4 の離散ラベル + relation type + reason** で
- 対称化 + 閾値疎化（score 3 以上）+ k-NN sparsification
- 順序バイアス対策に 10〜20% を swapped order で再判定（小 N なら全件）
- cannot-link を強く守りたいなら spectral より constrained clustering（AAAI 2025）

これは [[nishio]] が "vive 広聴AI" として実践しているチームみらい 300 件規模分析や、`policy-pr-hub.vercel.app` の小規模 UI 実験と地続きの設計提案である。  
current `kouchou-ai` の Web UI は 10,000 件超を想定しており、数十〜数百件規模ではそのまま使うのに無理がある。**小規模専用の analysis_mode** という設計枝は、survey 計画には明示されていなかったが、追加すべき棚として残しておく価値がある。

## 6. 評価軸を 1 つに畳まないこと

両ブレストは同じ結論に到達している：

- ARI / NMI / silhouette のような geometry score
- coverage / label readability / specificity のような semantic score
- 代表文書の納得性、境界事例の説明可能性
- 公開説明責務（reason 付き edge、prompt / model / seed の audit log）
- UX（飛地の少なさ、drill-down、編集容易性）
- コスト、再実行安定性

これらは **同一 winner を返さない**。 [[niizuma-thread-algorithm-critique]] と [[llm-grouping-experiment-output-2026-05-25]] が既に示している通り、1 つの algorithm score に畳むと設計判断を誤る。

survey 計画の評価軸分離方針（bucket 5 / 6）は、Deep Research 後も維持すべきだ。

## 7. 次の Read Order の更新

[[clustering-research-survey-plan]] が提示した read order：

1. UMAP docs `Using UMAP for Clustering`
2. document clustering pipeline の empirical study
3. spectral clustering の explainability / interpretability 論文
4. BERTopic paper
5. visualization vs analysis の caution literature

これは Deep Research 結果でほぼ妥当性が確認できた。追加すべきは：

6. LLM-as-pairwise-judge / LLM-generated constraints の研究（Viswanathan et al., AAAI 2025 *Optimized Algorithms for Text Clustering with LLM-Generated Constraints*, A Survey on LLM-as-a-Judge）
7. 概念誘導系（LLooM, TopicGPT, PromptTopic）
8. From Traditional Topic Models to LLM Topic Models（ACL 2025 / NIST）

これらは「LLM 系が BERTopic に対してどこで勝ち、どこで負けるか」を見るのに直接的である。

## 8. 設計判断への落とし込み

実装に落とすなら、優先度はこうなる：

1. **`analysis_mode` を data scale で切り分ける** — 数十件用と 1 万件用は別 plugin。current Web UI は大規模前提だが、`policy-pr-hub` 系の小規模 UI を切り出すか、`analysis-core` の plugin として明示する。
2. **UMAP `n_components` を可変化する** — clustering 用は 15D〜25D、表示用は 2D、で同一 embedding から両方を出す。これは [[niizuma-thread-algorithm-critique]] の「分析 artifact / 表示 artifact / 説明 artifact 分離」と直接対応する。
3. **LLM labeler を BERTopic 系 backbone に重ねる契約を整える** — [[llm-grouping-implementation-plan]] の延長線で、`representative_docs` を analysis-core の output に追加する。
4. **小規模専用の LLM pairwise + spectral plugin を実証する** — チームみらい 300 件規模で試す価値が高い。実装より前に [[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]] の推奨プロトコルを 1 度動かしてみる。

ただし、これらは **すべて Deep Research の応答であって、current `kouchou-ai` の implementation backlog 上の優先順位とは別** である。  
[[development-priority-roadmap-2026-05-23]] / [[strategic-development-order-2026-05-23]] は Windows 配布・既知バグ・運用基盤を上位に置いており、clustering 系研究は研究テーマ層に位置している。研究と実装の優先順位を混ぜない。

## Open Questions

- 日本語 broad listening データで `2D UMAP + KMeans`, `15D UMAP + HDBSCAN`, `raw embedding + spectral`, `LLM grouping`, `LLM pairwise + spectral` を同一データで比較した結果は、どこの軸でどう違いが出るか。
- `n_components` 可変化を current `analysis-core` に入れる場合、CLI / Web UI / `report.html` のどこにそれを露出するか。隠す方が UX としてはよいが、研究用途では露出が要る。
- 「LLM pairwise + spectral を試す」「BERTopic backbone + LLM labeler を明示化する」のどちらを先に試すかは、N の規模と用途で分かれる。チームみらい 300 件規模なら前者、自治体 1 万件想定なら後者。
- 小規模専用の plugin を切り出す場合、`analysis-core` の plugin contract（`analysis_mode`, `analysis_capabilities`）にどう載せるか。

## Updates

- 2026-05-25: survey bucket への deep-research 応答として整理。`UMAP -> clustering` は 2D vs 15D〜25D の分離が筋、BERTopic は backbone + LLM labeler の組合せに移行、数十件規模は LLM pairwise + spectral が筋、評価軸は 1 つに畳まない、を整理した
