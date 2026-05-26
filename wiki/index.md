# Wiki Index

kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース。

新規コントリビュータは [[kouchou-ai]] → [[usage-modes]] → [[analysis-core-and-web-ui]] → [[architecture-overview]] → [[local-dev-setup]] → [[gotchas]] の順に読むと早い。

> **このページは人間向けの curated navigation です**。AI / LLM 向けの全件カタログ（156 ページ）は [index.txt](index.txt) を、時系列の作業履歴は [log.md](log.md) を参照。

## Concepts

- [kouchou-ai](concepts/kouchou-ai.md) — プロジェクト全体像と 4 つの配布形態
- [usage-modes](concepts/usage-modes.md) — 非専門家向け Web UI と、研究者・データサイエンティスト向け CLI / analysis-core の使い分け
- [analysis-core-and-web-ui](concepts/analysis-core-and-web-ui.md) — なぜ Web UI は `analysis-core` を使う consumer で、Web は JSON、CLI は観察用HTMLを持つのか
- [broadlistening](concepts/broadlistening.md) — ブロードリスニング手法の定義と用語
- [architecture-overview](concepts/architecture-overview.md) — 5 サービスのランタイム構成
- [pipeline](concepts/pipeline.md) — 解析パイプライン（extraction → embedding → 階層クラスタリング → 可視化）
- [plugin-system](concepts/plugin-system.md) — 入力／解析／可視化の plugin 化（v5 の中核、production 未配線）
- [wiki-driven-workflow](concepts/wiki-driven-workflow.md) — Wiki repo で整理しつつ `work/kouchou-ai/` を読み、本体 repo に PR を出す二層運用
- [cli](concepts/cli.md) — `kouchou-analyze` / `python -m analysis_core` CLI
- [local-dev-setup](concepts/local-dev-setup.md) — Docker 一発からネイティブ Rye/pnpm まで
- [testing](concepts/testing.md) — pytest / Jest / Playwright と lint
- [deployment](concepts/deployment.md) — Azure 本番、静的サイト、PyPI リリース
- [llm-providers](concepts/llm-providers.md) — OpenAI / Azure / Gemini / OpenRouter / LocalLLM
- [coding-agents](concepts/coding-agents.md) — Devin / Claude Code / Codex の協働運用
- [contributing](concepts/contributing.md) — Issue → 実装計画 → PR の流れ、CLA、レビュー
- [meeting-report-draft](concepts/meeting-report-draft.md) — 次の定例会議で Codex が報告する内容の下書き（最新スナップショット: [meeting-report-2026-05-25](concepts/meeting-report-2026-05-25.md)）

## Entities

- [dd2030](entities/dd2030.md) — 親組織 デジタル民主主義2030
- [talk-to-the-city](entities/talk-to-the-city.md) — 上流 TTTC（archived）
- [idobata](entities/idobata.md) — 兄弟プロジェクト（1-on-1 深掘り）
- [polimoney](entities/polimoney.md) — 兄弟プロジェクト（政治資金）
- [broad-listening-book](entities/broad-listening-book.md) — 書籍（スコープ外参照）
- [nishio](entities/nishio.md) — 西尾泰和
- [tokoroten](entities/tokoroten.md) — 中山心太
- [nasuka](entities/nasuka.md) — 角野
- [ohki-shingo](entities/ohki-shingo.md) — 大木真吾
- [kuboon](entities/kuboon.md) — 大久保
- [anno](entities/anno.md) — 安野たかひろ
- [other-contributors](entities/other-contributors.md) — kitaro / tanenobu / shirouchi / sasano ほか

## Sources / Analyses

[[meeting-minutes]] / [[source-code]] / [[github-dev-docs]] が常用一次参照。テーマ別の深掘りは [[gotchas]] / [[refactoring-status]] / [[open-decisions]] / [[strategic-development-order-2026-05-23]] から辿るのが入口になる。

全 sources（61 件） / analyses（66 件）の機械可読カタログは [index.txt](index.txt) に集約。新規ページを追加した時は `python3 scripts/build_index_txt.py` で regenerate する。
