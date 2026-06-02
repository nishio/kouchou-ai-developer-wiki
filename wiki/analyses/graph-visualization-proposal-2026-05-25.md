---
name: graph-visualization-proposal-2026-05-25
summary: "UMAP 2D に意味クラスタも可視化品質も背負わせる設計から抜け、`クラスタ内 MST + mutual kNN、クラスタ間 bridge edge、2 段階 cluster-separated layout` で graph drawing として可視化する案。既存 niizuma 批判への visualization 側の答えになりうる"
type: analysis
sources:
  - gpt-mst-bridge-visualization-brainstorm-2026-05-25.md
  - niizuma-thread-algorithm-critique.md
  - tokoroten-spectral-clustering-reading.md
  - llm-grouping-experiment-output-2026-05-25.md
  - weekly-log-2026-05-20.md
---

[[gpt-mst-bridge-visualization-brainstorm-2026-05-25]] は、nishio 発案の「クラスタ内 MST + クラスタまたぎ edge を明瞭分離を壊さない範囲で追加」という可視化案を、既存研究と突き合わせて改良した提案である。  
この案の価値は、UMAP 2D を巡る議論を、UMAP のパラメータ調整・clustering アルゴリズム選択ではなく、**graph drawing 系の設計問題に置き換える** ところにある。

この発案は、2026-05-25 の `#2_開発_広聴ai_アルゴリズム開発` でも「1 意見 = 1 点」の点群要件、UMAP 2D と意味クラスタリングの衝突、クラスタ内 MST とクラスタ間 bridge edge の組み合わせとして共有されていた。[[weekly-log-2026-05-20]]より

## 1. UMAP 2D の問題を 3 要求の衝突として読み直す

[[niizuma-thread-algorithm-critique]] が露出させた論点を、可視化側から読み直すと、UMAP 2D は 3 つの要求を同時に満たそうとしている：

- 点群として見たい（1 意見 = 1 点）
- 意味的にまとまってほしい（意味クラスタが正しい）
- 見て理解しやすい（クラスタが分離して見える）

これらは並行成立しない。意味的に正しいクラスタは 2D 上で飛地や重なりを作り、見やすい分離は意味的忠実性を壊す。[[gpt-mst-bridge-visualization-brainstorm-2026-05-25]]より

UMAP 2D での解は **位置で意味を読ませる**。MST + bridge edge での解は **エッジで意味関係を読ませる**。後者は 2D 座標の歪みをエッジという別チャネルで補えるため、衝突を分散できる。

## 2. niizuma 批判への visualization 側の答えになりうる

[[niizuma-thread-algorithm-critique]] は最終的に、広聴AI の返す artifact を 3 種類に分けるべきと整理した：

- 分析 artifact（どの意見がどの論点群に属するか）
- 表示 artifact（非専門家が全体像を掴み個別意見へ辿れる UI）
- 説明 artifact（報道・自治体・外部レビューで「なぜそう分けたか」を説明する材料）

MST + bridge edge 提案は、これらを **同じ図の中で別チャネルに分離** する：

| 役割 | チャネル |
| --- | --- |
| 分析 artifact | cluster assignment（色 + クラスタ外形 / hull） |
| 表示 artifact | 点配置 + クラスタ内 MST / kNN（位置と背骨） |
| 説明 artifact | クラスタ間 bridge edge + `relation type` + `reason` |

特に bridge edge の `relation type`（same claim / adjacent issue / cause-effect / contrast / boundary）と `reason` は **説明 artifact** として直接機能する。これは UMAP 2D 散布図には欠けていた成分である。

## 3. tokoroten の TTTC 読みと違う方向

[[tokoroten-spectral-clustering-reading]] では、TTTC 的 spectral clustering は **UMAP が作る 2D 幾何の後始末** として理解されていた。tokoroten の読みは、scatter UX を残したまま k-means より自然な切り方を探す方向である。

これに対し本提案は **2D 幾何そのものを graph drawing で作り直す** 方向で、UMAP に依存しない。

| アプローチ | 2D 幾何の起点 | 意味的クラスタリングの居場所 |
| --- | --- | --- |
| 広聴AI 現状 | UMAP 2D | UMAP 後 KMeans |
| TTTC | UMAP 2D（小さい `n_neighbors`） | UMAP 後 SpectralClustering |
| TMAP / 本提案 | graph layout（MST + kNN + cluster separation） | embedding / LLM affinity から graph 構築 |

つまり「`UMAP -> k-means` を spectral に変える」だけでなく、「UMAP を使わない」という選択肢が研究上は妥当に存在する。[[clustering-deep-research-findings-2026-05-25]]より

## 4. 2 段階 layout の妥当性

GPT が提案し、nishio の指摘（「bridge を表示だけにするとクラスタ配置が任意になる」）を受けて修正された 2 段階設計：

1. **クラスタ間 layout** — 各クラスタをメタノードとして配置。クラスタ間重みは `top-3 mean` 類の集約値。
2. **クラスタ内 layout** — `MST + mutual kNN` で点を配置。クラスタ中心の周囲に収める。
3. **bridge edge を描く** — 点 i, j 間の線描画 + クラスタ中心同士への弱い layout 制約の 2 役。

これは clustered graph drawing（Frishman ら）や stress majorization（Gansner ら）の weighted edge 設計と整合する手法であり、自前で 0 から発明するのではない。  
nishio の修正が当てた本質は、**「bridge は overlay-only にする」と layout が崩れる** ことで、これは graph drawing 系研究では既に明示的に扱われている設計点である。

## 5. 全体 MST は避けるべき

nishio の元発案では「LLM で N:N の類似関係を抽出し、関係の強い方から繋いで全域木にする」だったが、全体 MST だと **必ず全意見が 1 本の木につながる** ため、本来離れたクラスタ間にもどこかで接続が生まれ、それが「重要な橋」に見えてしまう。[[gpt-mst-bridge-visualization-brainstorm-2026-05-25]]より

代わりに「クラスタ内 MST + クラスタ間少数橋」に分けるのが安全。これは MapSets 的（同一クラスタの点を spanning tree で接続し、非重複領域を作る）発想に、意味的 bridge edge を加える構成として読める。

## 6. current `kouchou-ai` への移植可能性

current `kouchou-ai` は Plotly 散布図 + 階層ツリー UI を持つ。MST + bridge 系 layout を入れる方法は 3 つ考えられる：

- **A. 既存散布図を維持し、bridge edge だけを overlay 追加** — 最小変更で実装可能。ただし scatter 座標は UMAP 2D のままなので、本案の利点（layout を作り直す）の半分しか得られない。
- **B. View plugin として cluster-separated graph layout を別 view に追加** — `analysis_mode` ではなく viewer level の選択肢。「scatter view」「graph view」をユーザが切り替える。[[public-ui-requirements-for-broadlistening]] の view plugin 契約と整合する。
- **C. `analysis-core` の output schema に MST edges / bridge edges / cluster centers を追加** — フルパス。後方互換性を保ちつつ、新 viewer がこれを使う設計。

短期的には A、中期的には B、長期的には C が筋に見える。[[llm-grouping-implementation-plan]] が示した `analysis_capabilities` / viewer `requirements` の枠組みは、ここでも使える。

## 7. 評価軸：bridge usefulness を中心に置く

[[gpt-mst-bridge-visualization-brainstorm-2026-05-25]] は、この案の評価軸として bridge usefulness を中心に据えている：

| 評価 | 見るもの |
| --- | --- |
| semantic coherence | クラスタ内意見が同じ見出しで読めるか |
| visual separation | クラスタが見た目に分かれているか |
| bridge usefulness | クラスタ間エッジが発見的か |
| stability | LLM 再実行・順序変更で大きく変わらないか |
| editability | 人間が merge / split / edge 削除しやすいか |

bridge usefulness は従来 UMAP 評価には出てこない指標であり、本案の中心価値である。  
これは [[clustering-deep-research-findings-2026-05-25]] の「評価軸を 1 つに畳まない」原則とも整合する。

## 8. 設計判断としての扱い

本案を current `kouchou-ai` の implementation backlog に乗せるかどうかは別問題である。  
[[development-priority-roadmap-2026-05-23]] / [[strategic-development-order-2026-05-23]] は Windows 配布・既知バグ・運用基盤を優先しており、可視化設計の作り直しはそれより下位である。  
ただし、[[llm-grouping-experiment]] のような小規模実証実験で **scatter 互換の限界が露出した時の代替案** として、本提案を持っておく価値は高い。

優先順位の整理：

1. **議論ストック** — 本案を「使えるカード」として持っておく。コードに直接落とす前段。
2. **小規模実証** — `policy-pr-hub.vercel.app` 系の小規模 UI 実験で、MST + bridge を 1 度 prototype する価値はある。
3. **schema 拡張** — `analysis-core` の output に MST / bridge を載せる方向は、急ぐ理由がないので保留。

## Open Questions

- 100 件未満用と 10,000 件超用で MST + bridge 設計を同一にできるか。N が大きい場合、MST + kNN は描画と計算の両面で scalability が課題。階層化（cluster-of-clusters）が必要かもしれない。
- bridge edge の `relation type` 自動分類精度は、LLM のどのモデル世代で実用に乗るか。誤分類された bridge は誤誘導のリスクが高く、誤判定の影響が見た目を支配する設計上の弱点になる。
- 2 段階 layout の `λ_inter` greedy schedule は、データセットごとに最適値が違う。デフォルト値を経験的に決める研究が必要。
- 本案を view plugin として実装する場合、既存の Plotly 散布図と co-exist するか、置き換えるか。co-exist だと UI 上の重複が増え、置き換えだと既存ユーザの期待を裏切る。

## Updates

- 2026-05-25: nishio ↔ GPT の MST + bridge 提案を、niizuma 批判への visualization 側の答え／tokoroten 読みと違う方向／2 段階 layout の妥当性／current への移植経路、として整理
- 2026-06-02: `oss_weekly_reporter` の 2026-05-20_to_2026-05-27 週次 dump で、MST + bridge 案の Slack 上の seed 発言を確認し、[[weekly-log-2026-05-20]] を source に追加
