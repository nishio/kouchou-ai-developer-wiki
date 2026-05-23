---
name: kouchou-ai
summary: "広聴AI — DD2030 配下の OSS ブロードリスニング実装。CSV → 抽出 → 埋め込み → 階層クラスタリング → 可視化"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
---

## 概要

**広聴AI (kouchou-ai)** は [[dd2030|デジタル民主主義2030]] が開発する [[broadlistening|ブロードリスニング]] の OSS 実装。[[talk-to-the-city|Talk to the City (TTTC)]] の Scatter 版を起点に、**日本語ユーザ・自治体／政党・非エンジニア運用** に最適化されている。

リポジトリ: `digitaldemocracy2030/kouchou-ai`。利用シナリオは「自治体や政党が収集した自由記述コメント（数百〜数万件）を、CSV でアップロードして意見の地図を作る」。

## 4 つの配布形態（[[meeting-minutes]] 2025-10-08）

[[nishio]] が整理した「同じコアを 4 つの形で提供する」分類：

- **A: 研究者向け Jupyter Notebook** — ステップ単位の制御
- **B: エンジニア向け CLI / `pip install kouchou-ai`** — AI コーディングエージェントから叩く想定（"vive 広聴AI"）
- **C: WebUI** — B をラップした現行プロダクト
- **D: ホスト型デモ** — エンジニアのいない組織向け（未提供）

2026 年に入って B のテコ入れが進行中。[[cli|kouchou-analyze CLI]] が PyPI 配信されており、[[pipeline]] の Python 直接静的 HTML 出力（PR #825、main 済み）は **CLI 側 sidecar 出力** として入っている。

この 4 形態のうち、現在の実務で特に重要なのは **非専門家向け Web UI モード** と **研究者・データサイエンティスト向け CLI モード** の 2 本柱。詳細は [[usage-modes]]。

この A/B/C/D 整理が出てきた背景、すなわち **TTTC の clone 前提ツールを Web UI で包み、その後 `analysis-core` / PyPI へ再切り出した経緯** は [[tttc-to-analysis-core-history]] にまとめた。[[meeting-minutes]]より

## ランタイム構成

詳細は [[architecture-overview]]。要約：

| Service | Port | Stack |
|---|---|---|
| `api` | 8000 | Python 3.12 / FastAPI / Rye |
| `public-viewer` | 3000 | Next.js 15 / Chakra UI / Plotly.js |
| `admin` | 4000 | Next.js 15 |
| `static-site-builder` | 3200 | Next.js (静的書き出し) |
| `ollama` (opt-in) | 11434 | Local LLM |

## コア機能

- CSV アップロード（非エンジニア向け）
- [[pipeline|階層クラスタリング]]（一層目／二層目）
- **濃いクラスタ**（濃い意見グループ）抽出 — 主に 1 万件以上の大規模データセット向け（小規模だと誤解されやすい）
- 散布図・ツリーマップ・dense-scatter による可視化
- 静的サイト書き出し（[[deployment]]）
- 多 LLM プロバイダ対応（[[llm-providers]]）
- [[plugin-system|入力／解析／可視化の plugin 化]]（進行中、v5 で本格化）

## 用語・略語

頻出するプロジェクト固有の用語は [[glossary]] にまとめてある。

## 命名上の混乱

[[meeting-minutes]] 2026-01-19 で `docs/refactoring/naming_convention.md` の整理が議論された。歴史的経緯で：

- ディレクトリ名 `apps/api/` ↔ Docker サービス名 `api` ↔ コード内 `server` という三重名
- `client` という名前の Next.js プロセスが「サーバ」として動く
- これらが新規コントリビュータの初動コストを上げる

## Open Questions

- v5.0 plugin 化のリリース時期（[[meeting-minutes]] で 2026 年 6 月目標、未着地）。詳細は [[versioning-strategy]]
- DB 導入は v4 以降の継続課題（毎回先送り）。今もファイルストレージ
- SaaS ホスティング（`kouchou-ai.dd2030.org`）の本格運用は体制不足で 2025-07 時点で先送り、現状未解決

## Updates

- 2026-05-17: 初回作成
- 2026-05-23: 4 つの配布形態が生まれた歴史的経緯への導線として [[tttc-to-analysis-core-history]] を追加
