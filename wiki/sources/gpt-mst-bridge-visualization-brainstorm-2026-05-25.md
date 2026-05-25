---
name: gpt-mst-bridge-visualization-brainstorm-2026-05-25
summary: "2026-05-25 の nishio ↔ 外部 GPT 対話。意味クラスタリングと 2D 散布図の衝突を、`クラスタ内 MST + クラスタ間 bridge edge + 2 段階 cluster-separated layout` という graph-drawing 系の設計で解く案を整理"
type: source
sources:
  - gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25.md
  - clustering-research-survey-seeds-2026-05-25.md
---

## What it is

2026-05-25 に `raw/gpt-mst-bridge-visualization-brainstorm-2026-05-25.txt` として保存した GPT 出力。  
nishio の発案「クラスタ内に距離ベース MST を作り、クラスタまたぎのエッジを短い方から順に明瞭分離を壊さない範囲で追加する」を、graph drawing 系の既存研究（TMAP、MapSets、stress majorization、Frishman らの clustered graph drawing、Duch & Matykiewicz の semantic MST）と突き合わせて改良した設計提案。

## Key Points

### 1. 出発点：UMAP 2D に背負わせている 3 要求の衝突

| 要求 | 欲しいもの | 問題 |
| --- | --- | --- |
| 点群として見たい | 1 意見 = 1 点 | 集約図だけではだめ |
| 意味的にまとまってほしい | 意味クラスタが正しい | 2D 上では飛地や重なりが出る |
| 見て理解しやすい | クラスタが分離して見える | 意味的忠実性と衝突する |

UMAP 2D 一発で全部を背負わせる設計から抜けて、**位置で意味を読ませる** のではなく **エッジで意味関係を読ませる** 設計に切り替える。

### 2. 提案の核：クラスタリング空間と表示空間を分ける

> 表示空間では、各意見を点として置き、クラスタ内は MST で "背骨" を作り、クラスタ間は少数の強い意味的 bridge だけを表示する。  
> bridge は layout を崩す力ではなく、ユーザが読むべき示唆として扱う。

TMAP（kNN graph → MST → tree layout）や MapSets（同クラスタの点を spanning tree で接続し、非重複領域を作る）と発想が近い。Duch & Matykiewicz は semantic similarity の MST 表示が「関係の骨格」を見せる図として有用だが、すべての距離を正確に表す図ではないと注意している。

### 3. そのままだと危ない点（GPT 側の修正）

- **MST だけだと細すぎる** → `MST(C, D) ∪ mutual_kNN(C, S)` でクラスタ内連結性 + 局所密度を両立。
- **1 本の誤った LLM edge が見た目を支配** → soft edge + 理由付き + 人間確認可能にする。LLM を絶対視せず、`relation type` と `reason` を残す。
- **クラスタ間 edge を強い force にすると分離を壊す** → 点間 attraction として強く使うのは避ける。

### 4. nishio による修正：「bridge を表示だけにすると配置が決まらない」

GPT の最初の案では「クラスタ間 edge は overlay のみ」を推していたが、nishio は **クラスタ配置が任意になり意味的地図にならない** と指摘。GPT は修正を受け入れ、

- 点レベルの強い attraction としては参加させない
- **クラスタ間配置を決める弱い制約** として layout に参加させる
- 同時に、bridge edge は表示にも使い「なぜこのクラスタ同士が近いか」の説明にする

という形に再設計した。これは clustered graph drawing（Frishman ら）や stress majorization（Gansner ら）の weighted edge 設計と整合する。

### 5. 推奨：2 段階 layout

#### 第 1 段階：クラスタ間 layout

各クラスタを 1 メタノードとして扱う。クラスタ間重みは

```
w_AB = top-3 mean similarity(i, j)  where i in A, j in B
```

を使う（`max` だと 1 本の誤判定で歪むため `top-k mean` 推奨）。理想距離は `L_AB = base_distance / (epsilon + w_AB)` などで決める。

#### 第 2 段階：クラスタ内 layout

各クラスタ内で `MST + mutual kNN` を作り、クラスタ中心の周囲に配置。クラスタ半径は `radius_C ≈ r0 * sqrt(|C|)`。

#### 第 3 段階：bridge edge を描く

クラスタ間 bridge は **クラスタ中心同士への弱い制約 + 点 `i, j` 間の線描画** という 2 役を持たせる。

### 6. クラスタ間 bridge の本数制御と種類

各クラスタ対 (A, B) について `top 1〜3 本` だけを bridge 候補に。endpoint が偏る場合は間引く。bridge edge には relation type を付ける：

| bridge type | 意味 |
| --- | --- |
| same claim across clusters | クラスタ分割が粗い／細かい可能性 |
| adjacent issue | 隣接論点 |
| cause-effect | 片方が原因、片方が対策 |
| contrast | 似た話題だが立場が違う |
| boundary / ambiguous | 分類が揺れる点 |

この分類が出ると、クラスタ間 edge は単なる線ではなく **読むべき示唆** になる。

### 7. 「明瞭分離を壊さない程度」の制御は greedy が無難

二分探索より、まずは `λ_inter` を 0 から段階的に上げる greedy schedule:

```python
for lambda_inter in [0.00, 0.03, 0.06, 0.10, 0.15, 0.25, 0.40]:
    layout = solve_layout(lambda_inter=lambda_inter)
    if visual_separation_ok(layout):
        best_layout = layout
    else:
        break
```

判定指標は hull overlap / cluster gap / normalized gap / edge crossing count / visual components（同クラスタが画面上で飛地化していないか）/ bridge clutter など。

### 8. 全体 MST はやめた方がよい

nishio の元提案では「LLM で N:N 類似関係を抽出し、関係の強い方から繋いで全域木にする」だったが、GPT は **全体 MST だと本来離れたクラスタ間にもどこかで接続が生まれ、それが "重要な橋" に見えてしまう** と注意。代わりに「クラスタ内 MST + クラスタ間少数橋」に分けるのが安全。

### 9. UI 像

- 点：意見
- 色：クラスタ
- 薄い線：クラスタ内 MST / kNN
- 太い線または破線：クラスタ間 bridge
- クラスタ外形：薄い hull / bubble / map region
- ラベル：LLM 生成のクラスタ要約
- bridge hover：A・B の原文、`relation type`、LLM の `reason`
- bridge 一覧：「クラスタ間の重要な接点」を別パネルで読める

### 10. 評価軸

クラスタリング精度だけでは足りない。**bridge usefulness** がこの設計の中心価値で、従来 UMAP 評価には出てこない。

| 評価 | 見るもの |
| --- | --- |
| semantic coherence | クラスタ内意見が同じ見出しで読めるか |
| visual separation | クラスタが見た目に分かれているか |
| bridge usefulness | クラスタ間エッジが発見的か |
| stability | LLM 再実行・順序変更で大きく変わらないか |
| editability | 人間が merge / split / edge 削除しやすいか |

## Compared to existing wiki claims

- [[niizuma-thread-algorithm-critique]] が「分析 artifact / 表示 artifact / 説明 artifact を分けるべき」と整理した方向の **具体的な visualization 設計案** として読める。bridge edge は「説明 artifact」の機能も担う。
- [[tokoroten-spectral-clustering-reading]] の「TTTC 的 spectral は 2D 幾何の後始末」読みに対し、こちらは **2D 幾何そのものを graph drawing で作り直す** 方向。UMAP に依存しない。
- [[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]] の LLM pairwise graph は、この設計の入力（意味関係層）として自然に接続する。
- [[jigsaw-llm-grouping-experiment-output-2026-05-25]] が「LLM grouping は top-level label では強いが scatter 互換は悪い」と観測したことへの応答：scatter 自体を作り直す方向。

## Open Questions

- current `kouchou-ai` の Web UI（Plotly ベース散布図 + 階層ツリー）に、この graph drawing 系 layout を plugin として組み込めるか。`analysis-core` の output schema にクラスタ中心座標・MST edges・bridge edges を載せる場合、後方互換性をどう保つか。
- 100 件未満用と 10,000 件超用で、UI の同一設計を取れるか。N が大きい場合 MST + kNN は scalability の課題が出る。
- bridge edge の `relation type` 自動分類の精度は LLM のどのモデル世代で実用に乗るか。誤分類された bridge は誤誘導のリスクが高い。
- `λ_inter` の greedy schedule は人間のチューニングが要るが、デフォルト値を経験的に決められるか。

## Related Pages

- 並行ブレスト: [[gpt-umap-clustering-bertopic-deep-research-2026-05-25]] / [[gpt-llm-pairwise-spectral-small-n-brainstorm-2026-05-25]]
- 議論の出発点: [[niizuma-thread-algorithm-critique]] / [[slack-niizuma-umap-kmeans-thread-2026-03-18]]
- 関連既存実験: [[jigsaw-llm-grouping-experiment-output-2026-05-25]] / [[jigsaw-llm-grouping-experiment]]
- 派生 analysis: [[graph-visualization-proposal-2026-05-25]]

## Updates

- 2026-05-25: 初回作成
