---
name: deployment
summary: "デプロイ — 公開 wiki では方針・課題・PR/issue の粒度に留め、Azure デモ環境の詳細は Google Drive 側で管理する"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - pr-887-production-deploy-observation-2026-06-01.md
---

## Azure（デモ環境・本番運用）

Azure デモ環境の運用詳細は公開 wiki に書かない。実環境 URL、resource 名・サイズ、revision / run の詳細、ログ、具体手順、secret / access 周辺の情報は、Google Drive の **「広聴AI-Azureデモ環境」** を一次置き場にする。アクセス権は大木・西尾・小野(moai)。`CLAUDE.md` より

公開 wiki に残すのは次の粒度に限定する。

- どの issue / PR がデプロイ運用に影響したか
- どの設計判断が公開コードや docs に反映されたか
- どの未解決課題を次に見るべきか
- 非公開詳細を参照すべき場合の置き場

2026-06-01 の `PR #887` 本番反映では、デプロイ成功判定と実際の反映状態にズレが出うること、また `public-viewer` の起動時 build が運用リスクになることが共有された。公開 wiki では詳細ログや実環境値は扱わず、恒久策として build / serve の責務分離と deploy readiness smoke を検討する、という課題粒度だけ残す。[[pr-887-production-deploy-observation-2026-06-01]]より [[meeting-minutes]]より

`public-viewer` の起動時 `next build` は、初期 Docker 化で「API 起動後に build したい」という設計から入った。その後の monorepo / pnpm workspace / shared package 化で runtime build の依存が増えたため、container 起動時 build をやめる方向が現在の改善軸になっている。詳細な実環境観測ではなく、設計上の経緯は [[public-viewer-runtime-build-history-2026-06-01]] に整理する。

## 静的サイト書き出し (GitHub Pages 等)

```bash
make client-build-static
# out/ を任意のホスト先へ
```

サブパス配信時は `NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH` を設定（[[gotchas|GitHub Pages サブパスで画像 404 になった歴史]]：PR #709）。

非エンジニアが静的書き出した HTML をホストする手段は **長年の未解決課題**（[[meeting-minutes]] 2025-04 〜 2026-05 で繰り返し議論）。候補：

- SaaS ホスティング `kouchou-ai.dd2030.org`（体制不足で先送り）
- 埋め込み fetch 型 HTML
- 認証付きクラウドホスティング

## CLI からの静的 HTML 出力（2026-05 〜）

PR #825 で Python が直接自己完結型 `report.html` を吐けるようになり、**AI コーディングエージェントから「サーバ無しで広聴 AI で分析」が可能に** なった。  
ただしこれは CLI 向けの観察用HTMLであり、現行の Web 配信主経路はなお `hierarchical_result.json` を API 経由で `public-viewer` が描画する構成。詳細は [[pipeline]] の「軽量化と CLI 静的出力」節と [[analysis-core-and-web-ui]]。

つまり deployment を考えるときは、[[usage-modes]] のうち **Web UI モードの配信** と **CLI モードの成果物持ち運び** を分けて考える方が事故が少ない。

## PyPI リリース (`kouchou-ai-analysis-core`)

2026-05-19 時点では、`analysis-core` の PyPI publish は **`analysis-core-v*` tag push で GitHub Actions が発火する自動運用** に移行した。発火条件の要約は [[pypi-release-trigger]]、実地確認の経緯は [[pypi-release-observation-2026-05-19]]。

`docs/development/pypi-release.md` の playbook：

1. `packages/analysis-core/pyproject.toml` の version をバンプ
2. `analysis-core-vX.Y.Z` で git tag
3. **package ディレクトリの外で build**（venv が package 内にあると `AbsoluteLinkError`）
4. tag push により `Publish analysis-core to PyPI` workflow が実行される

2026-05-18 の実観測では `analysis-core-v0.1.1` が version hardcoded test で失敗し、`analysis-core-v0.1.2` で publish success になった。つまり **tag push だけでは不十分で、workflow 内の `ruff` / `pytest` / `build` が通って初めて release される**。[[pypi-release-observation-2026-05-19]]より

## 環境変数の build 時焼き込み問題

`.env` を変えたら `docker compose down && docker compose up --build`。`Makefile` がハッシュ検出で `--no-cache` を強制（[[local-dev-setup]] 参照）。

## Open Questions

- 非エンジニアでもアクセスしやすい SaaS ホスト戦略
- 自動デプロイの kill-switch / rollback プロセスを公開可能な抽象度でどう表現するか
- Azure Deployment の success 条件をどの公開粒度で issue / PR 化するか

## Updates

- 2026-05-17: 初回作成
- 2026-05-18: PyPI 自動 publish の不足要件を整理した [[pypi-auto-release-requirements]] への導線を追加
- 2026-05-18: Azure Deployment workflow の一時失敗を観測したが、公開 wiki では資格情報・権限・実環境状態の詳細に踏み込まず、「一時的な外部環境不調や権限状態の揺れも候補に残す」粒度に留める
- 2026-05-19: `analysis-core-v*` tag push 起点の自動 publish と、`0.1.1` failure / `0.1.2` success の実観測を反映
- 2026-06-01: `PR #887` 本番反映で、デプロイ成功判定と実反映状態がズレうること、public-viewer startup build が運用リスクになることを公開可能な粒度で追記
- 2026-06-01: `public-viewer` の runtime `next build` は初期 Docker 化からの API 起動待ち設計であり、以後の monorepo / Turbopack / runner stage copy 漏れ修正で温存されてきた経緯を [[public-viewer-runtime-build-history-2026-06-01]] に整理して導線を追加
- 2026-06-01: Azure デモ環境などデプロイ詳細は公開 wiki に書かず、Google Drive「広聴AI-Azureデモ環境」を一次置き場にする方針へ更新
