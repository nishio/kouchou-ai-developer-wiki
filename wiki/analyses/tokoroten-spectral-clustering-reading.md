---
type: analysis
summary: "tokoroten の spectral clustering メモは、TTTC を『高次元で正しく切る手法』ではなく『UMAP が作る 2D 形状を前提に切る散布図寄りの手法』として理解していた点が重要"
sources:
  - slack-tokoroten-spectral-clustering-notes-2026-q1.md
  - tttc-spectral-clustering-code-observation-2026-05-25.md
  - slack-design-intents-2026-q1.md
  - talk-to-the-city.md
---

tokoroten の 2026-Q1 spectral clustering メモは短いが、広聴AIが TTTC をどう見ていたかをかなりよく表している。  
このメモが面白いのは、spectral clustering を単独のアルゴリズム選好として語っていない点である。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

ただし、ここで整理しているのは **TTTC の確定的事実** ではなく、**広聴AI側が当時どう解釈していたか** の分析である。  
したがってこの page は「設計意図の前提になった読み筋」の記録としては重要だが、「TTTC の真相」ページとして読むべきではない。

2026-05-25 に historical code を一次参照した結果、少なくとも

- TTTC が `UMAP` 後に `SpectralClustering` を掛けていること
- `n_neighbors` 上限が 10 であること
- 最終 `cluster-id` が spectral のラベルであること

までは確認できた。  
一方で **「小さめ `n_neighbors` で紐状構造を作り、それを切るのが方針」** は、依然として Slack 解釈の域を出ない。[[tttc-spectral-clustering-code-observation-2026-05-25]]より

## 1. tokoroten の読みでは、spectral clustering は `UMAP` の後始末に近い

普通に読むと、`k-means` の代わりに `spectral clustering` を使う話に見える。  
しかし tokoroten の表現はそうではなく、

- `UMAP` の `n_neighbors` を小さくすると分離しやすい
- TTTC はその分離を spectral で切っている

という順序になっている。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

つまりここでの spectral clustering は、抽象的な graph clustering というより、**2D 上に現れた紐状・島状の形を切るための道具** として理解されている。  
この読みだと、spectral clustering の主戦場は高次元 semantic space ではなく、scatter の見え方にかなり近い。

## 2. そのため TTTC 的 spectral clustering は、`UMAP` 後 `k-means` 批判への素直な答えではない

新妻 thread などで強く批判されていたのは、`UMAP` 後に距離ベースでクラスタリングすると 2D アーティファクトを拾うのではないか、という点だった。  
tokoroten のメモを踏まえると、TTTC 的 spectral clustering はこの批判から完全に自由な代替ではない。[[niizuma-thread-algorithm-critique]]より [[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

むしろこちらは、

- `k-means` よりは紐状構造を切りやすいかもしれない
- しかし依然として `UMAP` が作る 2D 幾何を強く前提にしている

という別種の scatter-first 手法として読む方が自然である。

## 3. nishio の 2026-02-04 整理と合わせると、spectral clustering は『第3の道』ではなく『散布図を残す枝』だった

2026-02-04 の `#2_開発_広聴ai` では、nishio が将来の大きな開発候補として

1. Jigsaw 的なもの
2. 既存構成の延長
3. オリジナル TTTC 的な spectral clustering

を並べている。そこで spectral clustering 枝は、

- 散布図はある
- ただし階層掘り下げはなくなる
- 飛地ができることがある

と整理されていた。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より [[slack-design-intents-2026-q1]]より

ここに tokoroten の補足を重ねると、spectral clustering は「より正しいクラスタリング」候補というより、**TTTC 的 scatter UX を残したまま current `kouchou-ai` と違う cut を試す枝** だったと分かる。

## 4. このメモは、TTTC を高次元派だと誤解しないためにも重要

後年の Slack や書籍草稿でも、「TTTC は元 embedding 次元でクラスタリングしていた」という理解に対して、tokoroten は「それは違う、`UMAP` してから `SpectralClustering` している」と修正を入れている。  
2026-Q1 のメモは、その修正の前段にあたる観察として読める。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

この修正自体は code observation と整合する。したがって **「TTTC は高次元 embedding に直接 spectral を掛けていた」理解は少なくともこの commit では誤り** と言ってよい。[[tttc-spectral-clustering-code-observation-2026-05-25]]より

このため、新規コントリビュータ向けには、

- 広聴AI = `UMAP` 後 `k-means` / 階層化
- TTTC = 高次元クラスタリング

という単純対比で覚えるのは危ない。  
tokoroten の読みでは、TTTC もまた **散布図都合の幾何をかなり活用する系譜** にある。

## 5. 必要な解説ページがあるなら、『TTTC は何を最適化していたか』である

このメモから分かるのは、アルゴリズム名だけを並べても本質は見えにくいということだ。  
本当に区別すべきなのは、

- semantic distance を守りたいのか
- scatter 上の分離や切れ味を守りたいのか
- hierarchy や drill-down を守りたいのか

である。[[slack-tokoroten-spectral-clustering-notes-2026-q1]]より

したがって spectral clustering の専用メモは有用だが、より大きい解説テーマは **「TTTC / 広聴AI / Jigsaw 系はそれぞれ何を最適化しているのか」** になる。  
この page はその入口として置く価値がある。

## Practical Priority

この論点の重要度は一様ではない。

- 広聴AIの設計史を追う文脈では重要
- current `analysis-core` に spectral clustering を戻す実装判断では、primary source と実験での再検証が必要
- 一般的な onboarding では「TTTC は high-dimensional clustering 派だった」と単純化しないための補助知識、くらいの重要度

つまり、今すぐ全件で厳密検証が必要というより、**この読みを前提に大きな設計判断や比較主張を書く時だけ、検証強度を上げる** のが妥当である。

## Open Questions

- current `analysis-core` 上で TTTC 的 `UMAP -> SpectralClustering` を plugin として再現した時、scatter / label / hierarchy のどの軸がどれだけ改善・悪化するか
- `n_neighbors` 調整で作る「紐状クラスタ」は、見やすさに寄与するだけか、それとも semantic distortion を増やす副作用が大きいか
- TTTC 的 scatter UX と、current broad listening の hierarchy / report UX を折衷できるか

## Updates

- 2026-05-25: tokoroten の spectral clustering メモを、scatter-first な TTTC 読みとして整理
- 2026-05-25: deep-research による cross-check で、TTTC の小さめ `n_neighbors` 採用は document clustering 研究上は無理筋ではないと確認。Eklund et al. 2023 でも文書埋め込みでは小さめ `n_neighbors` が有利な場合があると報告されている。整理は [[clustering-deep-research-findings-2026-05-25]]
- 2026-05-25: [[graph-visualization-proposal-2026-05-25]] は「TTTC 的 spectral は 2D 幾何の後始末」読みと別方向で、**2D 幾何そのものを graph drawing で作り直す** 設計案。UMAP に依存しない点が新しい
