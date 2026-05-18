# Wiki Index

kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース。

新規コントリビュータは [[kouchou-ai]] → [[architecture-overview]] → [[local-dev-setup]] → [[gotchas]] の順に読むと早い。

## Concepts

- [kouchou-ai](concepts/kouchou-ai.md) — プロジェクト全体像と 4 つの配布形態
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
- [slack-dev-kouchouai-2025-q4](sources/slack-dev-kouchouai-2025-q4.md) — `#2_開発_広聴ai` の 2025 4Q 設計ログ抜粋
- [slack-dev-kouchouai-2026-q1](sources/slack-dev-kouchouai-2026-q1.md) — `#2_開発_広聴ai` の設計意図が濃い 2026-Q1 ログ抜粋
- [slack-kouchouai-algorithm-dev](sources/slack-kouchouai-algorithm-dev.md) — `#2_開発_広聴ai_アルゴリズム開発` の 2025-04 〜 2026-03 論点整理
- [open-pr-observation-2026-05-18](sources/open-pr-observation-2026-05-18.md) — open PR review triage 実験で観測した head branch 更新挙動
- [open-pr-snapshot-2026-05-18](sources/open-pr-snapshot-2026-05-18.md) — 2026-05-18 時点の open PR 一覧を作者種別付きで切った snapshot
- [issue-493-pr-597-discussion](sources/issue-493-pr-597-discussion.md) — ScatterChart スクロール誤操作対策の issue / PR 議論メモ
- [pr-823-review-observation-2026-05-18](sources/pr-823-review-observation-2026-05-18.md) — `PR #823` 切り分けで観測した `public-viewer` build 挙動
- [pr-824-admin-merge-observation-2026-05-18](sources/pr-824-admin-merge-observation-2026-05-18.md) — `PR #824` merge 時に checks success / `REVIEW_REQUIRED` / admin merge が併存した観測
- [pr-827-llm-grouping-capabilities-plan-2026-05-18](sources/pr-827-llm-grouping-capabilities-plan-2026-05-18.md) — `PR #827` の LLM grouping / capability 自動判定計画の要約
- [seed-reproducibility-history](sources/seed-reproducibility-history.md) — UMAP / k-means の seed 固定と `PR #810` までの経緯
- [codeql-docs](sources/codeql-docs.md) — CodeQL 公式 docs の要約
- [pr-813-817-codeql-coderabbit-observation-2026-05-18](sources/pr-813-817-codeql-coderabbit-observation-2026-05-18.md) — `PR #813/#817` における CodeQL / CodeRabbit 設定混入と調整の観測メモ
- [issue-830-pr-832-auto-cluster-defaults-2026-05-18](sources/issue-830-pr-832-auto-cluster-defaults-2026-05-18.md) — CLI / analysis-core のクラスタ数デフォルト見直し issue / PR 観測メモ
- [pypi-release-observation-2026-05-19](sources/pypi-release-observation-2026-05-19.md) — `analysis-core-v0.1.1` / `v0.1.2` の PyPI publish 実観測
- [pr-735-issue-685-observation-2026-05-19](sources/pr-735-issue-685-observation-2026-05-19.md) — `PR #735` は issue 妥当でも patch は stale という観測メモ
- [pr-801-react-override-observation-2026-05-19](sources/pr-801-react-override-observation-2026-05-19.md) — `PR #801` は React version 統一の意図は妥当でも current `main` では `pnpm.overrides` 置換が回帰になるという観測メモ
- [pr-802-overview-config-observation-2026-05-19](sources/pr-802-overview-config-observation-2026-05-19.md) — `PR #802` は `Overview` だけの null-safe 化で `config` 欠損対応としては不十分という観測メモ
- [pr-814-static-export-error-observation-2026-05-19](sources/pr-814-static-export-error-observation-2026-05-19.md) — `PR #814` の draft 状態と static export error 差分の観測メモ
- [report-slug-config-repro-2026-05-19](sources/report-slug-config-repro-2026-05-19.md) — `/reports/{slug}` は通常生成物では `config` 付きだが、壊れた成果物は `config` 欠損のまま返すという再現メモ

## Analyses

- [gotchas](analyses/gotchas.md) — 非自明な落とし穴の一覧
- [public-viewer-build-behavior](analyses/public-viewer-build-behavior.md) — `public-viewer` build failure と API 入力条件の切り分け
- [refactoring-status](analyses/refactoring-status.md) — Phase 別の実装状況（docs と main の乖離）
- [open-decisions](analyses/open-decisions.md) — 未定／方針決定済・未着手／着手済・未完了 の三分類
- [versioning-strategy](analyses/versioning-strategy.md) — v4 凍結 / v5 plugin 化
- [npm-vs-pnpm](analyses/npm-vs-pnpm.md) — なぜ pnpm 必須か
- [glossary](analyses/glossary.md) — 用語集
- [pypi-auto-release-requirements](analyses/pypi-auto-release-requirements.md) — PyPI 自動更新に必要な構成要素
- [pypi-release-trigger](analyses/pypi-release-trigger.md) — PyPI リリースが発生する条件
- [slack-design-intents-2025-q4](analyses/slack-design-intents-2025-q4.md) — 2025 4Q の設計意図整理
- [slack-design-intents-2026-q1](analyses/slack-design-intents-2026-q1.md) — Slack から読める実装意図の整理
- [slack-algorithm-themes](analyses/slack-algorithm-themes.md) — アルゴリズム開発チャンネルから読める設計判断
- [agent-sandboxing-strategy](analyses/agent-sandboxing-strategy.md) — AI コーディングエージェント向けの権限分離と devcontainer 方針
- [chart-scroll-ux-decision](analyses/chart-scroll-ux-decision.md) — ScatterChart スクロール誤操作対策で好まれた UX と preview 不足の影響
- [non-nishio-human-pr-status](analyses/non-nishio-human-pr-status.md) — nishio 以外の人間 authored open PR が stale に見える理由の整理
- [book-release-development-plan-2026-09](analyses/book-release-development-plan-2026-09.md) — 2026-09 ごろの書籍リリースを前提にした開発計画案
- [umap-seed-history](analyses/umap-seed-history.md) — seed 固定が再現性要求から生まれ、後に並列性とのトレードオフとして見直された経緯
- [codeql-introduction-context](analyses/codeql-introduction-context.md) — `PR #817` 文脈で CodeQL がどう入ったか
- [auto-cluster-defaults](analyses/auto-cluster-defaults.md) — `[3, 6]` 固定値問題を docs / 実装 / AI 利用経路の不一致として整理
- [pr-735-merge-assessment](analyses/pr-735-merge-assessment.md) — `PR #735` は merge でなく current tree への再実装として扱うべきという判断
- [pr-801-merge-assessment](analyses/pr-801-merge-assessment.md) — `PR #801` は React fix の方向性は理解できても stale `package.json` patch なのでそのまま merge すべきでないという判断
- [pr-802-merge-assessment](analyses/pr-802-merge-assessment.md) — `PR #802` は `Overview` 1 箇所だけでは不十分なので merge しない方がよいという判断
- [pr-814-merge-assessment](analyses/pr-814-merge-assessment.md) — `PR #814` は方向性はよいが draft / review 未充足で、`BUILD_SLUGS` 誤診断も詰めてから merge したいという判断
- [report-slug-config-behavior](analyses/report-slug-config-behavior.md) — `reports/:slug` の `config` 欠損は通常生成ではなく router 無検証が原因という整理
