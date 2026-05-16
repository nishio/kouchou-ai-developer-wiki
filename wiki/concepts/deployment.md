---
name: deployment
summary: デプロイ — Azure 本番、静的サイト書き出し、PyPI リリース
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

PR #825 で Python が直接静的 HTML を吐くようになり、**AI コーディングエージェントから「サーバ無しで広聴 AI で分析」が可能に**。従来の `npm run build` 経路はオプションとして残す方針。詳細は [[pipeline]] の「軽量化と CLI 静的出力」節。

## PyPI リリース (`kouchou-ai-analysis-core`)

`docs/development/pypi-release.md` の playbook：

1. `packages/analysis-core/pyproject.toml` の version をバンプ
2. `vX.Y.Z` で git tag
3. **package ディレクトリの外で build**（venv が package 内にあると `AbsoluteLinkError`）
4. `twine upload`

GitHub Action のテンプレートも文書内にあるが配線されているかは別途確認が必要。

## 環境変数の build 時焼き込み問題

`.env` を変えたら `docker compose down && docker compose up --build`。`Makefile` がハッシュ検出で `--no-cache` を強制（[[local-dev-setup]] 参照）。

## Open Questions

- 非エンジニアでもアクセスしやすい SaaS ホスト戦略
- 自動デプロイの kill-switch / rollback プロセス

## Updates

- 2026-05-17: 初回作成
