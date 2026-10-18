# Wiki Index

kouchou-ai(広聴AI)開発者向けの設計判断・コード構造・運用ノウハウ・既知の落とし穴を整理。コントリビュータが素早く文脈を掴むためのナレッジベース。

> **このページは人間向けの curated navigation です**。AI / LLM 向けの全件カタログは [index.txt](index.txt) を、時系列の作業履歴は [log.md](log.md) を参照。

直近の状態: [健全性レビュー 2026-10-18](analyses/code-health-review-2026-10-18.md) / [定例レポート退避分 2026-10-18](concepts/meeting-report-2026-10-18.md) — ソースコードレビュー確定 10 件のうち 9 件を main 反映（[#1015](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1015)–[#1022](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1022)）。続く第 2 弾で公開レポート JSON の非公開キー除外など 6 PR（[#1026](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1026)–[#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031)）をレビュー待ち。Claude provider 接続実験は branch で検証中。次は PR のレビュー・merge 判断と、散布図ラベル a/b（[#1023](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1023)）の決定。

## 最初に読むべき (推奨順)

[[kouchou-ai]] → [[usage-modes]] → [[analysis-core-and-web-ui]] → [[architecture-overview]] → [[local-dev-setup]] → [[gotchas]]

雰囲気を掴むためのストーリー: [[deploy-success-but-nothing-changed-story-2026-06-01]] — 「デプロイ成功なのに画面が変わらない」という小さな違和感から、Wiki つき Coding Agent が古い設計の沼を一日で遡って直した一日のエピソード。前提知識ゼロで読める

## 開発者が共通して知るべきこと

- [security-maintenance](concepts/security-maintenance.md) — CodeQL/Dependabot 保守の durable hub と公開境界ポリシー

- [broadlistening](concepts/broadlistening.md) — ブロードリスニング手法の定義と用語
- [zipf-broadlistening](entities/zipf-broadlistening.md) — 「なぜサンプリングでなく全件か」を1枚で体験させる nishio のデモサイト（ランダムK件は割合pの意見を exp(-Kp) で丸ごと見落とす）
- [kouchou-ai](concepts/kouchou-ai.md) — プロジェクト全体像と 4 つの配布形態
- [analysis-stance](concepts/analysis-stance.md) — 広聴AI は構造把握スタンスのツールであって、定量分析スタンスのツールではない、という core stance
- [broadlistening-tool-ecosystem-vision](analyses/broadlistening-tool-ecosystem-vision.md) — simple Web UI + CLI 実験の二段構造エコシステムビジョン（analysis-stance の「別ツールで補完」への答え）
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

- [serverless-product-direction-2026-09-08](analyses/serverless-product-direction-2026-09-08.md) — dd2030の目的から見たブラウザ版・既存版の役割、互換範囲、次の開発順序（本流化は未決）

- [thinking-targets](concepts/thinking-targets.md) — 今、人間の思考と判断が要る論点のハブ (ラベル品質仕切り直し / 次の view 方向 / pipeline 境界 / 公開運用摩擦)
- [refactoring-status](analyses/refactoring-status.md) — Phase 別の実装状況、current main との同期
- [open-decisions](analyses/open-decisions.md) — 未定 / 方針決定済 / 着手済の三分類 (全体棚卸し)
- [issue-backlog-audit-2026-10-12](analyses/issue-backlog-audit-2026-10-12.md) — **現行の全件 issue 棚卸し**（最新。2026-05〜06 の triage はこれに置換済み）
- [kouchou-ai-docs-policy-history](analyses/kouchou-ai-docs-policy-history.md) / [kouchou-ai-docs-overhaul-2026-10](analyses/kouchou-ai-docs-overhaul-2026-10.md) — 本体 docs 方針の系譜と 2026-10 改善スプリントの総括
- [faithful-aggregation-vs-deliberation-dynamics](concepts/faithful-aggregation-vs-deliberation-dynamics.md) — 忠実な集約 vs 熟議ダイナミクス（分析スタンスの核）
- [dependabot-alerts-2026-10-14](analyses/dependabot-alerts-2026-10-14.md) — security / dependency 保守の観測（脆弱性の具体詳細は公開 wiki に書かない方針）
- [code-health-review-2026-10-18](analyses/code-health-review-2026-10-18.md) — コード・wiki・Issue の健全性レビュー（新規改善点と 6 PR、未着手 backlog、Issue 整理提案）
- [source-review-findings-2026-10-16](analyses/source-review-findings-2026-10-16.md) — ソースコードレビュー確定 10 件の棚卸し

過去の優先度整理（歴史的文脈。現行判断は上の棚卸しを優先）:

- [strategic-development-order-2026-05-23](analyses/strategic-development-order-2026-05-23.md) — 3 層 platform として見た時の長期順序
- [issue-priority-through-2026-09](analyses/issue-priority-through-2026-09.md) — 2026-09 書籍リリースを前提にした優先度整理
- [bug-issue-triage-2026-05-25](analyses/bug-issue-triage-2026-05-25.md) — `bug` ラベル open issue の current main 基準での再点検
- [fetch-reports-deprecation-and-storage-health-2026-05-26](analyses/fetch-reports-deprecation-and-storage-health-2026-05-26.md) — `fetch_reports.py` を migration 手段に降格し、storage health check を deploy safety に据える整理

## CLI / analysis-core 開発者向け

- [label-quality](concepts/label-quality.md) — クラスタラベルの契約と品質評価 5 レイヤの durable hub
- [experiment-methodology](concepts/experiment-methodology.md) — 実験設計の方法論（exploratory/clean・1 要素・blind A/B・judge 較正・3 層保存）
- [offline-local-clustering](concepts/offline-local-clustering.md) — 外部 LLM キー無しでローカル埋め込み＋クラスタリングだけを回す経路と落とし穴
- [extraction-faithfulness](concepts/extraction-faithfulness.md) — 意見抽出(step1)の忠実性（完走≠意味保持・モデル別書換・受け入れ条件）

- [ライセンスと結果公開](analyses/agpl-output-and-plugin-boundaries-2026-10-12.md) — データ・HTML・拡張の境界、CLIの案内自動付与と短いリンク表示の方針
- [cli](concepts/cli.md) — `kouchou-analyze` / `python -m analysis_core` CLI
- [plugin-system](concepts/plugin-system.md) — 入力／解析／可視化の plugin 化（v5 の中核。analysis 側は workflow engine が CLI の既定経路、外部 plugin の同梱はまだ無い）
- [llm-grouping-implementation-plan](analyses/llm-grouping-implementation-plan.md) — `analysis_mode=llm_grouping` 第2分析モードの実装方針
- [llm-grouping-supervised-classification](concepts/llm-grouping-supervised-classification.md) — LLM grouping の自動／指定カテゴリ分類（supervised）の2モードと「その他」必須の設計
- [jigsaw-sensemaker](entities/jigsaw-sensemaker.md) — Jigsaw Sensemaker は LLM grouping の一例であり、LLM grouping 全体を Jigsaw と呼ぶと混乱する、という用語整理
- [clustering-deep-research-findings-2026-05-25](analyses/clustering-deep-research-findings-2026-05-25.md) — UMAP / clustering / BERTopic の deep-research 整理
- [public-ui-requirements-for-broadlistening](analyses/public-ui-requirements-for-broadlistening.md) — 公開UI 7 要件、view plugin の上位契約

## WebUI 開発者向け

- [deployment](concepts/deployment.md) — Azure 本番、静的サイト書き出し、PyPI リリース
- [public-viewer-build-behavior](analyses/public-viewer-build-behavior.md) — public-viewer build failure と API 入力条件の切り分け
- [npm-vs-pnpm](analyses/npm-vs-pnpm.md) — なぜ pnpm 必須か

## プロジェクト自体について

- [開発日報 — 2026年9月8日〜9日未明](analyses/daily-report-2026-09-09.md) — 本体とServerlessの実装・merge・Issue整理を、利用者に起きる変化と残課題から振り返る
- [wiki-driven-workflow](concepts/wiki-driven-workflow.md) — Wiki repo で整理しつつ `work/kouchou-ai/` を読み、本体 repo に PR を出す二層運用。議事録 / Slack の鮮度基準もここを見る
- [deploy-success-but-nothing-changed-story-2026-06-01](analyses/deploy-success-but-nothing-changed-story-2026-06-01.md) — wiki-driven-workflow が実際にどう動くかの一日エピソード (前提知識ゼロ向け narrative)
- [meeting-minutes](sources/meeting-minutes.md) — 議事メモ Google Doc (2025-03 〜)、ingest 時の refresh protocol
- [slack-logs-repository](sources/slack-logs-repository.md) — dd2030 Slack public channel log の新しい一次置き場。最新14日は mirror、古い月は raw canonical を読む
- [slack-dev-kouchouai-2026-q1](sources/slack-dev-kouchouai-2026-q1.md) など — `#2_開発_広聴ai` の Slack ログ source（他 quarter / channel は index.txt で `slack-` 検索）
- [meeting-report-draft](concepts/meeting-report-draft.md) — 次の定例で Codex が報告する内容の下書き（最新: [meeting-report-2026-10-18](concepts/meeting-report-2026-10-18.md)、その前: [meeting-report-2026-10-10](concepts/meeting-report-2026-10-10.md)、[meeting-report-2026-06-01](concepts/meeting-report-2026-06-01.md)）

## 全件カタログ / 人物・組織

Sources / Analyses / Entities の全件は [index.txt](index.txt) を参照。人物・組織（dd2030 / talk-to-the-city / nishio / tokoroten / nasuka / ohki-shingo / kuboon / anno など）も同ファイルから stem 検索で辿れる。
