---
name: deployment
summary: "デプロイ — Azure 本番、静的サイト書き出し、PyPI リリース"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - pr-887-production-deploy-observation-2026-06-01.md
---

## Azure（本番運用）

[[dd2030]] の本番デプロイ先。`Makefile` に専用ターゲットが揃っている：

```
azure-cli         azure-login        azure-build        azure-push
azure-deploy      azure-info         azure-config-update
azure-cleanup     azure-status       azure-apply-policies
azure-save-env    azure-setup-all
```

サービスごとの log ターゲットもある。詳細手順は `docs/deployment/azure.md`。

- `.env.example` の注記：Azure 経路は `STORAGE_TYPE=azure_blob` 必須
- [[ohki-shingo]] が Azure 環境を主担当（[[meeting-minutes]] 2025-07-09 で account 作成、admin 追加募集中）
- main マージで自動デプロイする CI が 2025-07-30 に着地（Issue #642）
- 公開デモ環境 `https://admin.kouchou-ai.dd2030.org/` は VM 上で手動運用

2026-06-01 の `PR #887` 本番反映では、Azure Deployment workflow は success になったが、public-viewer の new revision はしばらく Ready にならず、stable URL は旧 ready revision を返していた。原因は二層で、(1) deploy confirmation が stable URL の 200 だけを見て new revision readiness を待っていない、(2) `public-viewer` は container 起動後に `entrypoint.sh` で `next build` を実行しており、1Gi memory 環境で TypeScript phase が exit 137 になり得る、というもの。暫定策は memory increase、恒久策は latest revision readiness と代表 report smoke を deploy check に入れること。[[pr-887-production-deploy-observation-2026-06-01]]より [[meeting-minutes]]より

`public-viewer` の起動時 `next build` は、2025-03 の初期 Docker 化で「build時にAPIサーバーを参照するため、APIサーバーの起動を待ってからbuildを行う」ために入った。その後、monorepo / pnpm workspace / Turbopack / shared package の問題を runner image 側の copy 追加や `turbopack.root` で延命してきた経緯がある。詳細は [[public-viewer-runtime-build-history-2026-06-01]]。

## 静的サイト書き出し (GitHub Pages 等)

```bash
make client-build-static
# out/ を任意のホスト先へ
```

サブパス配信時は `NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH` を設定（[[gotchas|GitHub Pages サブパスで画像 404 になった歴史]]：PR #709）。

非エンジニアが静的書き出した HTML をホストする手段は **長年の未解決課題**（[[meeting-minutes]] 2025-04 〜 2026-05 で繰り返し議論）。候補：

- SaaS ホスティング `kouchou-ai.dd2030.org`（体制不足で先送り）
- 埋め込み fetch 型 HTML
- BASIC 認証付き Azure ホスティング

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
- 自動デプロイの kill-switch / rollback プロセス
- Azure Deployment の success 条件を stable URL 200 ではなく、latest revision readiness と代表 report URL の実動作確認へ寄せる具体実装

## Updates

- 2026-05-17: 初回作成
- 2026-05-18: PyPI 自動 publish の不足要件を整理した [[pypi-auto-release-requirements]] への導線を追加
- 2026-05-18: `Azure Deployment` workflow で `No subscriptions found` による `azure/login@v2` failure を観測したが、同日 rerun では `Azure CLI ログイン` が成功した。少なくともこの事例は「恒久的な資格情報破損」と断定せず、一時的な Azure 側不調や secret / 権限状態の揺れも候補に残すべき
- 2026-05-19: `analysis-core-v*` tag push 起点の自動 publish と、`0.1.1` failure / `0.1.2` success の実観測を反映
- 2026-06-01: `PR #887` 本番反映で、Deploy Success が旧 ready revision の 200 による false positive になりうること、public-viewer startup `next build` が 1Gi memory で exit 137 になりうることを追記。暫定 memory increase と readiness / representative report smoke の必要性を整理
- 2026-06-01: `public-viewer` の runtime `next build` は初期 Docker 化からの API 起動待ち設計であり、以後の monorepo / Turbopack / runner stage copy 漏れ修正で温存されてきた経緯を [[public-viewer-runtime-build-history-2026-06-01]] に整理して導線を追加
