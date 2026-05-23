---
name: plugin-system
summary: "入力／解析／可視化を plugin 化する設計。v5.0 の中核"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - source-code.md
  - slack-dev-kouchouai-2026-q1.md
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
3. **可視化 (visualization) plugin** — `why-plugin-system.md` で第 3 軸として語られるが、**バックエンド側に Python plugin システムは無い**。一方でフロント側には `apps/public-viewer/components/charts/plugins/` があり、`registry.ts`, `types.ts`, `validation.ts` と built-in の `scatter` / `treemap` / `hierarchy-list` plugin が実装済み

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

[[slack-dev-kouchouai-2026-q1]] 2026-01-14 週でも、**分析プロセスを WebUI で切り替えるか、管理者が設定ファイルを書けば十分かはユースケースがまだ明確でないので保留** とされている。analysis plugin は「何でも GUI で切り替える」前提で固めていたわけではない。

## なぜ再利用機能が plugin 化とセットだったか

[[slack-dev-kouchouai-2026-q1]] 2026-01-21 週では、分析 plugin を変えて試行錯誤するなら「同じデータに対して違う分析をして結果を比較したい」ので、**入力データや `extraction`, `embedding` の再利用** がセットで欲しくなると述べられている。

つまりレポート再利用は単独の便利機能ではなく、**analysis plugin を比較可能にする基盤** として要請された。2026-02-04 週の「同一データ、同一抽出、同一埋め込み」で比較できる、という説明も同じ意図。

## drastic refactor は別リポジトリで

[[meeting-minutes]] 2025-10-08 で [[nishio]]：「今のコードがあちこち動かなくなるので、リポジトリを複製して必要なコードだけ残して開発するといい」。[[talk-to-the-city|TTTC]] からの kouchou-ai フォーク自体が同じパターン。

## production パスとの繋がり：現状 dormant

実装は存在するが **default 実行パスは plugin dispatch を通らない**：

- `PipelineOrchestrator.run()` — レガシーの `run_step()` ループを直接呼ぶ。[[cli|CLI]] と API サーバはこちら
- `PipelineOrchestrator.run_workflow()` — plugin dispatch 経由。**呼ばれていない**

= plugin システムは [[refactoring-status|Phase 3a 完了 / Phase 3b dormant]] の状態。今ステップを書き換える時、plugin wrapper も同時に直すか／wrapper は最終的に削除予定かは要確認。

「なぜ dormant のままか」を current `main` のコード差分で見ると、初期 input artifact、status 永続化、config key 正規化、visualization artifact 契約に未吸収のギャップがある。詳細は [[workflow-defaultization-blockers]]。

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

`[[slack-dev-kouchouai-2026-q1]]` で補足される設計意図：

- Jigsaw 系分析はまず `extraction, embedding` の後ろに差し込む互換枝として考えられていた
- その亜種として **既存のカテゴリーツリーをパラメータで与える分類** も想定されていた
- 自治体の事業計画・予算カテゴリに合わせた分類ニーズがその具体例
- Jigsaw 系分析は散布図を自然には出せないので、**可視化を管理者選択可能にすること** が必要条件
- したがって Jigsaw Sensemaker 的な第 2 モードを本気で受け入れるなら、「analysis plugin を増やす」だけでは足りず、**scatter を持たない mode が first-class citizen になれる visualization / capability 契約** まで含めて設計し直す必要がある

## 関連ドキュメント

- `docs/development/plugin-guide.md` — plugin 作成手順
- `docs/development/plugin-output-data-structures.md` — plugin が従うべき I/O スキーマ。`comment-id` 採番の責任は plugin 側にある点に注意
- `docs/development/why-plugin-system.md` — rationale
- `docs/development/why-pnpm.md` — pnpm 強制の理由

## Open Questions

- v5.0 のリリース時期。2026-06 目標だが進捗未確認（[[versioning-strategy]]）
- `pnpm-workspace.yaml` の `plugins/*` glob と実体ディレクトリ不在のギャップ
- taxonomy-guided な LLM 分類を analysis plugin の設定として持たせるのか、別 workflow として切るのか

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を再確認し、可視化 plugin は「気配」ではなくフロント側基盤が実装済みと修正
- 2026-05-17: `#2_開発_広聴ai` ログから、再利用機能と Jigsaw 系 analysis plugin の結びつきを追記
