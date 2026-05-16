# Wiki Index

kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース。

新規コントリビュータは [[kouchou-ai]] → [[architecture-overview]] → [[local-dev-setup]] → [[gotchas]] の順に読むと早い。

## Concepts

- [kouchou-ai](concepts/kouchou-ai.md) — プロジェクト全体像と 4 つの配布形態
- [broadlistening](concepts/broadlistening.md) — ブロードリスニング手法の定義と用語
- [architecture-overview](concepts/architecture-overview.md) — 5 サービスのランタイム構成
- [pipeline](concepts/pipeline.md) — 解析パイプライン（extraction → embedding → 階層クラスタリング → 可視化）
- [plugin-system](concepts/plugin-system.md) — 入力／解析／可視化の plugin 化（v5 の中核、production 未配線）
- [cli](concepts/cli.md) — `kouchou-analyze` / `python -m analysis_core` CLI
- [local-dev-setup](concepts/local-dev-setup.md) — Docker 一発からネイティブ Rye/pnpm まで
- [testing](concepts/testing.md) — pytest / Jest / Playwright と lint
- [deployment](concepts/deployment.md) — Azure 本番、静的サイト、PyPI リリース
- [llm-providers](concepts/llm-providers.md) — OpenAI / Azure / Gemini / OpenRouter / LocalLLM
- [coding-agents](concepts/coding-agents.md) — Devin / Claude Code / Codex の協働運用
- [contributing](concepts/contributing.md) — Issue → 実装計画 → PR の流れ、CLA、レビュー

## Entities

- [dd2030](entities/dd2030.md) — 親組織 デジタル民主主義2030
- [talk-to-the-city](entities/talk-to-the-city.md) — 上流 TTTC（archived）
- [idobata](entities/idobata.md) — 兄弟プロジェクト（1-on-1 深掘り）
- [polimoney](entities/polimoney.md) — 兄弟プロジェクト（政治資金）
- [broad-listening-book](entities/broad-listening-book.md) — 書籍（スコープ外参照）
- [nishio](entities/nishio.md) — 西尾泰和
- [tokoroten](entities/tokoroten.md) — 中山心太
- [nasuka](entities/nasuka.md) — 角野
- [ohki-shingo](entities/ohki-shingo.md) — 大木慎吾
- [kuboon](entities/kuboon.md) — 大久保
- [anno](entities/anno.md) — 安野たかひろ
- [other-contributors](entities/other-contributors.md) — kitaro / tanenobu / shirouchi / sasano ほか

## Sources

- [meeting-minutes](sources/meeting-minutes.md) — 議事メモ Google Doc (2025-03 〜 2026-05)
- [github-dev-docs](sources/github-dev-docs.md) — kouchou-ai リポジトリと `docs/development/`
- [source-code](sources/source-code.md) — コード本体（docs ギャップを埋める一次参照）
- [deepwiki-kouchou-ai](sources/deepwiki-kouchou-ai.md) — DeepWiki 生成のコードベース要約（補助ソース）
- [weekly-log-2026-05-06](sources/weekly-log-2026-05-06.md) — `oss_weekly_reporter` 週次ダンプ

## Analyses

- [gotchas](analyses/gotchas.md) — 非自明な落とし穴の一覧
- [refactoring-status](analyses/refactoring-status.md) — Phase 別の実装状況（docs と main の乖離）
- [open-decisions](analyses/open-decisions.md) — 未定／方針決定済・未着手／着手済・未完了 の三分類
- [versioning-strategy](analyses/versioning-strategy.md) — v4 凍結 / v5 plugin 化
- [npm-vs-pnpm](analyses/npm-vs-pnpm.md) — なぜ pnpm 必須か
- [glossary](analyses/glossary.md) — 用語集
