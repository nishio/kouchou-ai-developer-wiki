---
name: gotchas
summary: 非自明な落とし穴・ハマりどころの一覧 — 経験的に繰り返し発生する footgun
type: analysis
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - source-code.md
---

コードを読むだけでは復元しづらく、議論や実地報告で繰り返し顔を出すハマりどころ。一次ソースは [[meeting-minutes]] と `docs/development/*`。

## 環境変数・設定

### `AZURE_OPENAI_*` ではなく `AZURE_CHATCOMPLETION_*`

`.env.example` のコメントが明示的に警告：「Use AZURE_CHATCOMPLETION_* (NOT AZURE_OPENAI_*)」。Azure OpenAI SDK の慣例命名と異なるため、コピペ系の onboarding ドキュメントで踏みがち。

### `.env` の一部は build 時に焼き込まれる

`docker compose up --build` し直さないと反映されない env var がある。`Makefile` が `.env` / `.env.azure` のハッシュを `.env-hashes/` に保存し、変更検知で `docker compose build --no-cache` を強制する救済策がある。

### LOCAL LLM は `main@3809a7a` でも `https://...` を素直には受け取れない

[[meeting-minutes]] 2026-05-18 見出し / PR #824 では修正報告があるが、`main@3809a7a` の `packages/analysis-core/src/analysis_core/services/llm.py` と `apps/api/src/services/llm_models.py` は依然として `local_llm_address` を **`host:port` 形式として解釈し、`http://{host}:{port}/v1` を組み立てる**。`https://example.com` のような URL をそのまま渡すと崩れる可能性が高い。  
**「LOCAL」という命名が実装に HTTP 前提を埋め込みやすい** という教訓自体は有効。詳細は [[llm-providers]]。

## パイプライン・データ

### `embeddings.pkl` は UMAP 後 2D

`embeddings.pkl` という名前だが中身は **2 次元化された後のベクトル**。元の埋め込みを使いたい場合は再埋め込みが必要。[[nishio]] が 2025-10-08 に踏んで気づいた。

### CSV 列名の case 不一致

`config.is_pubcom=true` 経路で出る `final_result_with_comments.csv` だけ **snake_case** (`arg_id`, `category_id`)。他は kebab-case (`arg-id`, `category-id`)。`docs/development/plugin-output-data-structures.md` が明示的な例外として書いている。

### `comment-id` 自動採番が経路依存

- Web CSV アップロード／スプレッドシート取り込み → 自動生成
- CLI ／プラグイン／直接 CSV → **プラグイン側で出す責任**

### `propertyMap` 不整合でクラッシュ

`hierarchical_result.json` の `propertyMap` に対応する列が `args.csv` に無いと `hierarchical_aggregation` ステップで落ちる。

### デフォルトクラスタ数 `[3, 6]` が小さすぎる

[[meeting-minutes]] 2026-05-18 見出し：`docs/user-guide/cli-quickstart.md` の例 `[3, 6]` を Claude Code が転用し、300 件規模でも粗いまとめになる。本質的修正は「optional 化 + データ件数から自動算出」。一度 silhouette-score ベースの自動選択（PR #567）が試されたが embedding エラーで revert (#579)。**未解決**。詳細は [[pipeline]]。

### `extraction.skip: true` がない

整形済みデータの再分析でも extraction が走り、コスト・時間の無駄。複数回希望されたが未実装（最新確認は議事メモ 2026-05-18 見出し）。

## OS・環境

### Windows インストール地獄

[[meeting-minutes]] 2025-04 〜 2025-10 で繰り返し報告：

- Docker Desktop の 4GB RAM デフォルトでパイプラインが OOM
- `entrypoint.sh` の **CRLF 改行**（Git の `core.autocrlf` 起因）で起動失敗
- 「使いたいだけで開発はしない」非エンジニアユーザは Git も未導入

対策が幾度も積まれている（PR #314、setup script、kitaro のバッチ、#524 ネイティブ環境）が継続課題。

### `docker compose up` だけだとデータが消える

[[meeting-minutes]] 2025-04：クラウドへ再デプロイすると過去レポートが消える事故が頻発。`/scripts/fetch_reports.py` でバックアップできるが discoverability が悪い。

## リファクタ・パッケージ周り

### 旧 `hierarchical_main.py` は黙って動く

`apps/api/broadlistening/pipeline/hierarchical_main.py` は `DeprecationWarning` を出すだけで実行は通る。古い手順書を見て `python hierarchical_main.py` した人は **黙ってステイル版のステップが走る**。バグレポートのトレースに `broadlistening/pipeline/steps/...` が含まれていたら旧パスを疑う。canonical は `packages/analysis-core/`（[[refactoring-status]]）。

### 同名 `PluginRegistry` が 2 つある

- `src.plugins.registry.PluginRegistry` (input plugin、class-level state)
- `analysis_core.plugin.registry.PluginRegistry` (analysis plugin、instance-based singleton)

同じクラス名でも全く別物。import 先を間違えると一見動くがどこにも登録されない（[[plugin-system]]）。

### CLI `--without-html` / `--skip-interaction` が無効化できない

両者は `action="store_true"` + `default=True` で定義されていて、**コマンドラインから False に戻せない**。HTML を出したい時はライブラリ API を直接叩く（[[cli]]）。

### PyPI パッケージ名 `kouchou-ai-analysis-core` と import 名 `analysis_core`

ハイフン／アンダースコアの食い違い。`pip install` と `import` で違う。

### `analysis-core` pyproject.toml の Documentation URL が壊れている

`Documentation = "...docs/CLI_QUICKSTART.md"` を指すが実体は `docs/user-guide/cli-quickstart.md`。

## ツールチェイン

### npm は非対応

`docs/development/why-pnpm.md`：[[plugin-system]] が strict isolation な `node_modules` を前提とするため。詳細は [[npm-vs-pnpm]]。

### Biome の CI 強制が弱い

`lefthook.yml` で Biome 系は `skip: true`、`docs/testing.md` の CI ワークフロー列挙にも Biome 系がない。フロントエンドの lint 強制力はバックエンド（ruff）より緩い可能性。

### import-order チェックでの Devin 無限ループ

[[meeting-minutes]] 2025-10-01：Devin がリント自動修正できないものを `ruff format` 連打してループ。PR #708 で **ruff の import-order チェック自体を無効化** + 既存違反を一括修正して打開。

### `EXDEV: cross-device link not permitted`

Issue #724：静的ファイル出力時のクロスデバイスリンクエラー。Devin が 30 分で緊急修正した（2025-10-29）。

## デプロイ・ホスティング

### 静的書き出し HTML の置き場問題

非エンジニアユーザが kouchou-ai の出力 HTML をどこに置くか — 2025-04 から 2026-05 まで毎回議論されながら未解決。候補：SaaS ホスト `kouchou-ai.dd2030.org`、埋め込み fetch 型、BASIC 認証付き Azure。

### GitHub Pages サブパスで画像 404

PR #709：ハードコードされた `/images/foo.png` 形式のパスがサブパス配信で 404 に。`NEXT_PUBLIC_STATIC_EXPORT_BASE_PATH` で配信パスを設定する運用。

### Plotly 散布図 click 不発

Issue #710：`displayModeBar: "hover"` が `ScatterChart.tsx` にあると、URL を持つ scatter が click 移動しなくなる。

### PyPI build は package ディレクトリの外で

`docs/development/pypi-release.md`：venv が `packages/analysis-core/` 内にあると `AbsoluteLinkError`。リリースは外側で実施。

## ドキュメント・運用

### `docs/` の例が AI に伝播する

`docs/user-guide/cli-quickstart.md` の `[3, 6]` が示す通り、**ドキュメント中の具体例は AI の de facto デフォルト** になる。例を書くときは「真似されたら困らないか」を意識する必要がある。

### Devin の自動 PR クローズ

[[meeting-minutes]] 2025-11-12：Devin は 1 週間放置 PR を自分で閉じる仕様。kouchou-ai では workaround で無効化。

### CLA 必須

[[contributing]] 参照。AI 生成 PR も人間がレビューして引き取れば CLA 範囲。

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を再確認し、LOCAL LLM の HTTPS 問題は「修正済み」と断定しない表現に修正
