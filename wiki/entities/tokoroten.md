---
name: tokoroten
summary: "中山心太 — kouchou-ai メンテナ。LocalLLM、属性フィルタ、書籍主担当"
type: entity
sources:
  - meeting-minutes.md
---

## Who

**中山心太 (tokoroten)**。[[kouchou-ai]] メンテナ（2025-05-07 〜）。

## kouchou-ai での主な貢献

- **LocalLLM (Ollama / LM Studio) 統合** — PR #422 (2025-05-07)。「OpenAI API key が無くても使える」ことを目的化
- **属性フィルタ** — PR #531。年齢・地域などのメタデータでクラスタを絞る
- **技術解説スライド／動画** — `docs.docswell.com` の 1h40min プレゼン、YouTube `SpOI-JuJv5o`。新規コントリビュータが kouchou-ai のアルゴリズム全体像を掴むのに有用
- **sentiment-weighted UMAP 実験** — 賛否を埋め込みに重み付けして反対派／賛成派を分離する prototype（メインリポジトリ外）
- **farbrain** (`tokoroten/farbrain`) — UMAP+k-means+ラベリングを使ったゲーミフィケーション派生

## [[broad-listening-book]] 関連

- 書籍の主担当（本 Wiki スコープ外）
- 「民意」と「統計的世論」を分離する整理を書籍に持ち込んだ
- ナラティブアプローチ vs 要約アプローチの対比を整理（[[broadlistening]] 参照）

## Updates

- 2026-05-17: 初回作成
- 2026-05-25: `#2_開発_広聴ai_アルゴリズム開発` 2026-Q1 の短い spectral clustering メモを独立ページ化。tokoroten は TTTC を「`UMAP` の `n_neighbors` を小さめにして紐状分離を作り、それを `SpectralClustering` で切る scatter-first な系」と読んでおり、単なる `k-means` 代替というより可視化都合を含んだ理解だった。詳細は [[tokoroten-spectral-clustering-reading]]
- 2026-05-25: 2025-12 方向性議論から 2026-Q1 spectral / 新妻 thread / LLM grouping 実験までを接続し、tokoroten とのアルゴリズム議論は手法比較ではなく、散布図 product・深い分析・説明責務・運用ワークフローを分け直す議論だったと整理。詳細は [[tokoroten-algorithm-discussion-retrospective]]
