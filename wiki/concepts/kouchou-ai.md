---
title: "広聴AI の概要"
name: kouchou-ai
summary: "広聴AI — DD2030 配下の OSS ブロードリスニング実装。CSV → 抽出 → 埋め込み → 階層クラスタリング → 可視化"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - public-web-kouchouai-tttc-lineage-2026-06-30.md
---

## 概要

**広聴AI (kouchou-ai)** は [[dd2030|デジタル民主主義2030]] が開発する [[broadlistening|ブロードリスニング]] の OSS 実装。[[talk-to-the-city|Talk to the City (TTTC)]] の Scatter 版を起点に、**日本語ユーザ・自治体／政党・非エンジニア運用** に最適化されている。

DD2030 公式ページは、TTTC を起源に置きつつ、2024 年の東京都知事選 / 日本テレビ衆院選報道 / `シン東京2050` などの国内前史を挙げ、その後に日本の自治体・政治家の実務向け改善として広聴AIが開発され、2025-03-16 に OSS 公開されたと説明している。公開事例整理では、これらの前史を `TTTC direct / pre-kouchou lineage` として扱い、広聴AI confirmed case と混ぜない。[[public-web-kouchouai-tttc-lineage-2026-06-30]]より

リポジトリ: `digitaldemocracy2030/kouchou-ai`。利用シナリオは「自治体や政党が収集した自由記述コメント（数百〜数万件）を、CSV でアップロードして意見の地図を作る」。

## 4 つの配布形態（[[meeting-minutes]] 2025-10-08）

[[nishio]] が整理した「同じコアを 4 つの形で提供する」分類：

- **A: 研究者向け Jupyter Notebook** — ステップ単位の制御
- **B: エンジニア向け CLI / `pip install kouchou-ai-analysis-core`** — AI コーディングエージェントから叩く想定（"vive 広聴AI"）
- **C: WebUI** — B をラップした現行プロダクト
- **D: ホスト型デモ** — エンジニアのいない組織向け（未提供）

2026 年に入って B のテコ入れが進行中。[[cli|kouchou-analyze CLI]] が PyPI 配信されており、[[pipeline]] の Python 直接静的 HTML 出力（PR [#825](https://github.com/digitaldemocracy2030/kouchou-ai/issues/825)、main 済み）は **CLI 向け観察用HTML出力** として入っている。

この 4 形態のうち、現在の実務で特に重要なのは **非専門家向け Web UI モード** と **研究者・データサイエンティスト向け CLI モード** の 2 本柱。詳細は [[usage-modes]]。

この A/B/C/D 整理が出てきた背景、すなわち **TTTC の clone 前提ツールを Web UI で包み、その後 `analysis-core` / PyPI へ再切り出した経緯** は [[tttc-to-analysis-core-history]] にまとめた。現在の設計判断として「なぜ Web UI は core の consumer なのか」は [[analysis-core-and-web-ui]]。[[meeting-minutes]]より

設計判断の core stance としては **「広聴AI は構造把握スタンスのツールであって、定量分析スタンスのツールではない」** ([[analysis-stance]]) を抑える。「全体傾向を把握する」は数を数えるだけで完結する装置ではなく、reader が構造を読み解くための装置として設計する。

## ランタイム構成

詳細は [[architecture-overview]]。要約：

| Service | Port | Stack |
|---|---|---|
| `api` | 8000 | Python 3.12 / FastAPI / Rye |
| `public-viewer` | 3000 | Next.js 16 / Chakra UI / Plotly.js |
| `admin` | 4000 | Next.js 16 |
| `static-site-builder` | 3200 | Express 5 / TS（public-viewer の静的書き出しを ZIP 化） |
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

## 命名の再編（2026-01）と旧名の名残

2026-01-19 の定例では、リポジトリの再編で「混乱を招くネーミング」（path が `server` なのに Docker 名が `api`、`client` という名前のサーバを建てる、など）をまとめて修正したと報告された。[[meeting-minutes]] 2026-01-19 より。改名は refactoring ブランチで行われ、PR [#746](https://github.com/digitaldemocracy2030/kouchou-ai/issues/746) で 2026-01-23 に main へ入った。対応は `docs/refactoring/naming_convention.md` にある。

| 旧ディレクトリ | 現ディレクトリ | Docker サービス名 |
|---|---|---|
| `server/` | `apps/api/` | `api`（変更なし） |
| `client/` | `apps/public-viewer/` | `client` → `public-viewer` |
| `client-admin/` | `apps/admin/` | `client-admin` → `admin` |
| `client-static-build/` | `apps/static-site-builder/` | `client-static-build` → `static-site-builder` |

今はディレクトリ名と Docker サービス名が一致している。API の Python コードも `src.*` として import され（例: `uvicorn src.main:app`）、`server` というモジュール名は使っていない。旧名が残っているのは主に次の箇所。

- `apps/api/pyproject.toml` の `name = "server"`、`apps/api/README.md` の見出し「kouchou-ai-server」と「`server` フォルダ」という記述
- `Makefile` のターゲット `client-setup` / `client-dev` / `client-dev-server` / `client-admin-dev-server` / `client-build-static`
- CI の `client-build.yml` / `client-jest.yml` / `client-admin-build.yml` / `client-admin-jest.yml` / `server-pytest.yml`

README・`skills/kouchou-ai-development/SKILL.md`・`docs/deployment/github-pages.md` などは今も `make client-*` を手順として案内しているので、新規コントリビュータが名前で戸惑うとすればここ。`client` が歴史的な呼び名であることは [[glossary]]、再編の完了状況は [[refactoring-status]] の Phase 1 を参照。

## Open Questions

- v5.0 plugin 化のリリース時期（[[meeting-minutes]] で 2026 年 6 月目標。2026-10-18 時点で最新タグは v4.1.0 のままで未着地）。詳細は [[versioning-strategy]]
- DB 導入は v4 以降の継続課題（毎回先送り）。今もファイルストレージ
- SaaS ホスティング（`kouchou-ai.dd2030.org`）の本格運用は体制不足で 2025-07 時点で先送り、現状未解決

## Updates

- 2026-10-21: 「命名上の混乱」節を「命名の再編（2026-01）と旧名の名残」に書き換え。出典の 2026-01-19 定例は改名済みの報告で、PR [#746](https://github.com/digitaldemocracy2030/kouchou-ai/issues/746) で main に入っていた。main `b71e0b79` と照合し、旧名が残る箇所を列挙
- 2026-10-18: static-site-builder を Express 5 に、CLI のパッケージ名を `kouchou-ai-analysis-core` に訂正。v5.0 未リリース（最新タグ v4.1.0）を明記
- 2026-06-30: [[public-web-kouchouai-tttc-lineage-2026-06-30]] を反映し、DD2030 公式ページ上の TTTC 起源 / 国内前史 / 2025-03-16 OSS 公開の公開説明を追加。公開事例では前史と広聴AI confirmed case を混ぜない。
- 2026-05-30: 設計判断の core stance として [[analysis-stance]] (広聴AI = 構造把握スタンス、定量分析スタンスではない) への導線を追加
- 2026-05-17: 初回作成
- 2026-05-23: 4 つの配布形態が生まれた歴史的経緯への導線として [[tttc-to-analysis-core-history]] を追加
- 2026-10-12: サービス要約表の Next.js 15→16 を current main に合わせて訂正（[[architecture-overview]] と同期）。[[wiki-self-audit-2026-10-12]]
