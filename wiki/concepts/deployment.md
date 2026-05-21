---
name: deployment
summary: "デプロイ — Azure 本番、静的サイト書き出し、PyPI リリース"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
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
ただしこれは CLI 向け sidecar 成果物であり、現行の Web 配信主経路はなお `hierarchical_result.json` を API 経由で `public-viewer` が描画する構成。詳細は [[pipeline]] の「軽量化と CLI 静的出力」節。

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

## Updates

- 2026-05-17: 初回作成
- 2026-05-18: PyPI 自動 publish の不足要件を整理した [[pypi-auto-release-requirements]] への導線を追加
- 2026-05-18: `Azure Deployment` workflow で `No subscriptions found` による `azure/login@v2` failure を観測したが、同日 rerun では `Azure CLI ログイン` が成功した。少なくともこの事例は「恒久的な資格情報破損」と断定せず、一時的な Azure 側不調や secret / 権限状態の揺れも候補に残すべき
- 2026-05-19: `analysis-core-v*` tag push 起点の自動 publish と、`0.1.1` failure / `0.1.2` success の実観測を反映
