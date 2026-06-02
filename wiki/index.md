# Wiki Index

kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース。

> **このページは人間向けの curated navigation です**。AI / LLM 向けの全件カタログ（219 ページ）は [index.txt](index.txt) を、時系列の作業履歴は [log.md](log.md) を参照。

## 最初に読むべき (推奨順)

[[kouchou-ai]] → [[usage-modes]] → [[analysis-core-and-web-ui]] → [[architecture-overview]] → [[local-dev-setup]] → [[gotchas]]

## 開発者が共通して知るべきこと

- [broadlistening](concepts/broadlistening.md) — ブロードリスニング手法の定義と用語
- [kouchou-ai](concepts/kouchou-ai.md) — プロジェクト全体像と 4 つの配布形態
- [analysis-stance](concepts/analysis-stance.md) — 広聴AI は構造把握スタンスのツールであって、定量分析スタンスのツールではない、という core stance
- [usage-modes](concepts/usage-modes.md) — 非専門家向け Web UI と、研究者・データサイエンティスト向け CLI / analysis-core の使い分け
- [analysis-core-and-web-ui](concepts/analysis-core-and-web-ui.md) — なぜ Web UI は analysis-core を使う consumer で、Web は JSON、CLI は観察用HTMLを持つのか
- [architecture-overview](concepts/architecture-overview.md) — 5 サービスのランタイム構成
- [pipeline](concepts/pipeline.md) — 解析パイプライン（extraction → embedding → 階層クラスタリング → 可視化）
- [versioning-strategy](analyses/versioning-strategy.md) — v4 凍結 / v5 plugin 化のリリース戦略
- [llm-providers](concepts/llm-providers.md) — OpenAI / Azure / Gemini / OpenRouter / LocalLLM
- [local-dev-setup](concepts/local-dev-setup.md) — Docker 一発からネイティブ Rye/pnpm まで
- [testing](concepts/testing.md) — pytest / Jest / Playwright と lint
- [contributing](concepts/contributing.md) — Issue → 実装計画 → PR の流れ、CLA、レビュー
- [coding-agents](concepts/coding-agents.md) — Devin / Claude Code / Codex の協働運用
- [gotchas](analyses/gotchas.md) — 非自明な落とし穴の一覧

**いま何を考えるか / 何が起きているか:**

- [thinking-targets](concepts/thinking-targets.md) — 今、人間の思考と判断が要る論点のハブ (ラベル品質仕切り直し / 次の view 方向 / pipeline 境界 / 公開運用摩擦)
- [refactoring-status](analyses/refactoring-status.md) — Phase 別の実装状況、current main との同期
- [open-decisions](analyses/open-decisions.md) — 未定 / 方針決定済 / 着手済の三分類 (全体棚卸し)
- [strategic-development-order-2026-05-23](analyses/strategic-development-order-2026-05-23.md) — 3 層 platform として見た時の長期順序
- [issue-priority-through-2026-09](analyses/issue-priority-through-2026-09.md) — 2026-09 書籍リリースを前提にした優先度整理
- [bug-issue-triage-2026-05-25](analyses/bug-issue-triage-2026-05-25.md) — `bug` ラベル open issue の current main 基準での再点検
- [fetch-reports-deprecation-and-storage-health-2026-05-26](analyses/fetch-reports-deprecation-and-storage-health-2026-05-26.md) — `fetch_reports.py` を migration 手段に降格し、storage health check を deploy safety に据える整理

## CLI / analysis-core 開発者向け

- [cli](concepts/cli.md) — `kouchou-analyze` / `python -m analysis_core` CLI
- [plugin-system](concepts/plugin-system.md) — 入力／解析／可視化の plugin 化（v5 の中核、production 未配線）
- [llm-grouping-implementation-plan](analyses/llm-grouping-implementation-plan.md) — `analysis_mode=llm_grouping` 第2分析モードの実装方針
- [jigsaw-sensemaker](entities/jigsaw-sensemaker.md) — Jigsaw Sensemaker は LLM grouping の一例であり、LLM grouping 全体を Jigsaw と呼ぶと混乱する、という用語整理
- [clustering-deep-research-findings-2026-05-25](analyses/clustering-deep-research-findings-2026-05-25.md) — UMAP / clustering / BERTopic の deep-research 整理
- [public-ui-requirements-for-broadlistening](analyses/public-ui-requirements-for-broadlistening.md) — 公開UI 7 要件、view plugin の上位契約

## WebUI 開発者向け

- [deployment](concepts/deployment.md) — Azure 本番、静的サイト書き出し、PyPI リリース
- [public-viewer-build-behavior](analyses/public-viewer-build-behavior.md) — public-viewer build failure と API 入力条件の切り分け
- [npm-vs-pnpm](analyses/npm-vs-pnpm.md) — なぜ pnpm 必須か

## プロジェクト自体について

- [wiki-driven-workflow](concepts/wiki-driven-workflow.md) — Wiki repo で整理しつつ `work/kouchou-ai/` を読み、本体 repo に PR を出す二層運用。議事録 / Slack の鮮度基準もここを見る
- [meeting-minutes](sources/meeting-minutes.md) — 議事メモ Google Doc (2025-03 〜)、ingest 時の refresh protocol
- [slack-dev-kouchouai-2026-q1](sources/slack-dev-kouchouai-2026-q1.md) など — `#2_開発_広聴ai` の Slack ログ source（他 quarter / channel は index.txt で `slack-` 検索）
- [meeting-report-draft](concepts/meeting-report-draft.md) — 次の定例で Codex が報告する内容の下書き（最新: [meeting-report-2026-06-01](concepts/meeting-report-2026-06-01.md)、前回: [meeting-report-2026-05-25](concepts/meeting-report-2026-05-25.md)）

## 全件カタログ / 人物・組織

Sources / Analyses / Entities の全件は [index.txt](index.txt) を参照。人物・組織（dd2030 / talk-to-the-city / nishio / tokoroten / nasuka / ohki-shingo / kuboon / anno など）も同ファイルから stem 検索で辿れる。
