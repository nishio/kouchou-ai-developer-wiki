---
name: glossary
summary: "kouchou-ai 周辺の用語集 — 日本語特有・プロジェクト固有のショートハンド"
type: analysis
sources:
  - github-dev-docs.md
  - meeting-minutes.md
---

## プロジェクト・組織

| 用語 | 意味 |
|---|---|
| 広聴AI / kouchou-ai | 本プロジェクト。「広聴」= 広く聴く（[[kouchou-ai]]） |
| ブロードリスニング / broad listening | 大規模意見集約手法（[[broadlistening]]） |
| デジタル民主主義2030 / DD2030 | アンブレラ組織（[[dd2030]]） |
| Talk to the City / TTTC | 上流（[[talk-to-the-city]]） |
| いどばた / idobata | 1-on-1 深掘りインタビュー OSS（[[idobata]]） |
| polimoney / ポリマネー | 政治資金可視化（[[polimoney]]） |
| Cartographer | idobata 系の自動追問プロトタイプ |
| コアループ | DD2030 横断イニシアチブ。Process / Tech / Policy / Reference Product / Communication の 5 領域 |
| broad-listening-book / 広聴AI本 | [[tokoroten]] 主担当の書籍。2026-05-21 から開発向け source 扱い（[[broad-listening-book-source]] / [[broad-listening-book-extractions]]） |
| しゃべれるマニフェスト | team-mirai のチャット型マニフェスト UI |
| マル見え / marumie | team-mirai の歳出可視化プロジェクト |

## 概念・機能

| 用語 | 意味 |
|---|---|
| 濃いクラスタ / 濃い意見グループ | 意見密度の高いクラスタを抽出する UI 要素。1 万件以上のデータ向け |
| 一層目 / 二層目 | 階層クラスタリングのレイヤ。`∛n` 個程度を推奨 |
| 属性フィルタ | 年齢・地域などのメタデータでクラスタを絞る（PR #531） |
| 限定公開 / unlisted | YouTube 風の URL を知っている人だけ閲覧可能（Issue #341, PR #500） |
| 静的 HTML 出力 / static export | `next export` または Python 直書きで static site を吐く（[[deployment]]） |
| extraction / 抽出 | パイプラインの最初の LLM ステップ。コスト最大 |
| パブコメ / 公けコメ | パブリックコメント（行政手続）。`config.is_pubcom=true` で専用 CSV を出す |
| パブコメ攻撃 / パブコメ DDoS | AI による大量コメント投稿によるパブコメ妨害 |
| 民意 vs 統計的世論 | 書籍側の整理。前者は質的、後者は量的 |
| ナラティブアプローチ | チャット型インテーク手法（[[broadlistening]] 参照） |
| シルエットスコア / silhouette score | クラスタ数自動選択の評価指標 |
| ブロードリスニングの 4 つのデータ型 | [[nishio]] の分類 — 書籍と plugin 設計に影響 |
| CUI / CLI / "vive 広聴AI" | AI コーディングエージェントから叩く CLI 利用パターン |
| bikeshed dataset | 文化庁公開コメントなどの合成攻撃データセット |

## アーキテクチャ・実装

| 用語 | 意味 |
|---|---|
| api / server | バックエンド FastAPI サービス（path は `apps/api/`） |
| public-viewer / client | エンドユーザ向け Next.js（"client" は歴史的呼称） |
| admin | 管理 UI Next.js |
| static-site-builder | 静的書き出し用 Next.js（port 3200） |
| analysis-core | PyPI 公開している解析パッケージ `kouchou-ai-analysis-core` |
| dummy-server | dev / E2E 用モック API |
| input plugin / analysis plugin / visualization plugin | [[plugin-system]] の 3 軸 |
| Rye | Python ツールチェイン |
| pnpm | フロントエンドパッケージマネージャ（npm 非対応） |
| Biome | TS/JS lint+format（ESLint+Prettier 代替） |
| lefthook | Git hook マネージャ |
| LOCAL LLM | Ollama / LM Studio など自己ホスト LLM の一括カテゴリ名 |
| ELYZA-JP | 既定 Ollama モデル `Llama-3-ELYZA-JP-8B-GGUF` |
| Azure OpenAI | env は `AZURE_CHATCOMPLETION_*`（`AZURE_OPENAI_*` ではない、[[gotchas]]） |
| OpenRouter | 多モデル中継 API |

## AI ツール

| 用語 | 意味 |
|---|---|
| Devin | コーディング AI。`devin-ai-integration[bot]`、ACU credits は [[anno]] 経由 |
| Claude Code | Anthropic の coding CLI。[[nishio]] と polimoney が多用 |
| Codex / GPT-5.2 | OpenAI コーディング AI |
| GitHub Copilot Agent | issue にアサイン可能な並行選択肢 |
| CodeRabbit | AI PR レビュアー。kouchou-ai でも導入検討（Issue #417） |
| #devin部屋 | Slack 内 Devin 指示用チャンネル |

## 自治体・行政まわり

| 用語 | 意味 |
|---|---|
| 広聴課 / 広報広聴課 | 自治体の意見受付部署（kouchou-ai のターゲット顧客と名前が衝突） |
| LGWAN | 自治体専用ネットワーク。外部 API 不可で郡山市の対応断念に至った |
| パブコメ | パブリックコメント（既出） |
| 政務活動費 | 議員に支給される活動費。岩永淳志ダッシュボードのテーマ |

## 会議・運用

| 用語 | 意味 |
|---|---|
| 議事メモ | 週次会議の Google Doc（[[meeting-minutes]]） |
| Brand Compass | プロダクト戦略文書。毎週の「今後追求する事」の筆頭 |
| PROJECTS.md | board 運用と自動化 bot の定義 |

## Updates

- 2026-05-17: 初回作成
- 2026-05-21: 書籍を「Wiki スコープ外」から「開発向け source」表記へ更新
