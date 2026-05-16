---
name: plugin-system
summary: 入力／解析／可視化を plugin 化する設計。v5.0 の中核
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
---

## 重要：実体は「同名の別システム」が 2 つある

ドキュメント上は「3 軸の plugin」と語られるが、実コードには **同名 `PluginRegistry` を持つ無関係な実装が 2 つ** ある：

| 系統 | 場所 | 用途 | 登録方法 |
|---|---|---|---|
| **Input plugin** | `apps/api/src/plugins/` | FastAPI からの外部データ取り込み (YouTube etc.) | クラスレベル `PluginRegistry`（class methods/dict）、`@PluginRegistry.register` デコレータ |
| **Analysis plugin** | `packages/analysis-core/src/analysis_core/plugin/` | パイプラインステップの差し替え | インスタンスベース `PluginRegistry`（`get_registry()` で singleton）、`@step_plugin` デコレータ |

コードを書く時は、どちらの "PluginRegistry" を import しているか必ず確認すること（[[gotchas]]）。

## 3 つの plugin 軸（docs 上の整理）

1. **入力 (input) plugin** — `apps/api/src/plugins/`。サンプルとして YouTube plugin (`youtube.py`) が同梱。`ENABLE_{ID}_INPUT_PLUGIN=true` env で有効化。`pkgutil.iter_modules` で auto-import → `@PluginRegistry.register` で class-level 登録
2. **解析 (analysis) plugin** — `packages/analysis-core/src/analysis_core/plugins/builtin/` に **8 つの builtin** （extraction, embedding, hierarchical_*）。既存ステップ関数を `legacy_config` を再構築して呼び出す薄いラッパー
3. **可視化 (visualization) plugin** — `why-plugin-system.md` で第 3 軸として語られるが、**バックエンド側に Python plugin システムは無い**。`apps/public-viewer/` のフロント側で `ChartType extensible` 化が進んでいる気配あり（commit `05b6c11`）

## 採用理由

`docs/development/why-plugin-system.md` より：

> 互換性を保ちたい vs 新機能を実験したい、というジレンマの打開策。**技術的境界で関心を分離し、合意形成によらず並行進化を可能にする**。

[[meeting-minutes]] 2026-01-26 でも「従来のメインアルゴリズムはデフォルト、新しいものはオプションのプラグイン」が明示されている。

## なぜ npm ではなく pnpm 必須か

`docs/development/why-pnpm.md` より要約：

- plugin システムは strict-isolation な `node_modules` を前提に設計されている
- npm のホイストは phantom dependency を生み、配布された plugin が他環境で壊れる
- pnpm の non-hoisting `node_modules` がこの問題を回避

詳細は [[npm-vs-pnpm]]。

## 設計思想：customization は GUI ではなく config

[[meeting-minutes]] 2025-12-03 で言及。TTTC Turbo がグラフィカルなノードパイプラインエディタを試みたが「既存インスタンスを使いたい人にはハードル高すぎ」で tttc-light-js では固定パイプラインに退却。kouchou-ai の結論：**JSON/YAML config による customization が現実的**。

## drastic refactor は別リポジトリで

[[meeting-minutes]] 2025-10-08 で [[nishio]]：「今のコードがあちこち動かなくなるので、リポジトリを複製して必要なコードだけ残して開発するといい」。[[talk-to-the-city|TTTC]] からの kouchou-ai フォーク自体が同じパターン。

## production パスとの繋がり：現状 dormant

実装は存在するが **default 実行パスは plugin dispatch を通らない**：

- `PipelineOrchestrator.run()` — レガシーの `run_step()` ループを直接呼ぶ。[[cli|CLI]] と API サーバはこちら
- `PipelineOrchestrator.run_workflow()` — plugin dispatch 経由。**呼ばれていない**

= plugin システムは [[refactoring-status|Phase 3a 完了 / Phase 3b dormant]] の状態。今ステップを書き換える時、plugin wrapper も同時に直すか／wrapper は最終的に削除予定かは要確認。

## 外部 plugin loader と現実

`loader.discover_plugin_directories()` は以下を探す：

- 引数 `base_paths`
- `Path.cwd() / "plugins" / "analysis"`
- `ANALYSIS_PLUGINS_PATH` 環境変数

ただし **リポジトリに `plugins/analysis/` ディレクトリは存在せず、外部 analysis plugin の同梱もゼロ**。loader 検証用のテストはあるが production 利用例は無い（[[refactoring-status]]）。

## v5.0 plugin 例の構想

[[meeting-minutes]] 2026-01-26：

- **YouTube input plugin**（実装済み）— URL からコメント自動収集
- **階層リスト view plugin**（outliner 風）
- **Polis input plugin** — 容易と判定
- **Jigsaw analysis plugin** — 散布図データが出ない設計上の難点あり

## 関連ドキュメント

- `docs/development/plugin-guide.md` — plugin 作成手順
- `docs/development/plugin-output-data-structures.md` — plugin が従うべき I/O スキーマ。`comment-id` 採番の責任は plugin 側にある点に注意
- `docs/development/why-plugin-system.md` — rationale
- `docs/development/why-pnpm.md` — pnpm 強制の理由

## Open Questions

- v5.0 のリリース時期。2026-06 目標だが進捗未確認（[[versioning-strategy]]）
- `pnpm-workspace.yaml` の `plugins/*` glob と実体ディレクトリ不在のギャップ

## Updates

- 2026-05-17: 初回作成
