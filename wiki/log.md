# Log

## [2026-05-17 01:15] filing-back | 未着地の論点を 3 分類で整理 ([[open-decisions]])

- A. 未定 11 件、B. 方針決定済み・未着手 13 件、C. 着手済み・未完了 4 件
- 「PyPI アップデート機構」「plugin 機構」など複数粒度の作業状態を観測整理
- コントリビュータ募集時に B カテゴリから候補を引きやすい設計

## [2026-05-17 01:00] ingest | リポジトリ本体をコードリーディング — リファクタ／plugin／CLI／pip 化の実装状況を取り込み

- 一次参照を `raw/kouchou-ai-snapshot/` に保存、新規 source ページ [[source-code]] を追加
- 新規 concept ページ [[cli]] — `kouchou-analyze` / `python -m analysis_core` の挙動と argparse の落とし穴
- 新規 analysis ページ [[refactoring-status]] — Phase 0〜3a 着地 / 3b dormant / 8 部分的、aspirational なものとの乖離整理
- 更新: [[pipeline]] (canonical 配置を `packages/analysis-core/` に修正、`run()` vs `run_workflow()` を追記)
- 更新: [[plugin-system]] (同名 `PluginRegistry` が 2 系統あること、production 未配線、外部 `plugins/analysis/` 不在を明記)
- 更新: [[architecture-overview]] (subprocess 境界をデータフロー図に反映)
- 更新: [[gotchas]] (deprecated shim・PluginRegistry 衝突・argparse バグ・名前不一致を追加)
- 更新: [[versioning-strategy]] (「別リポジトリで refactor」案は採用されず main 上 Phase 移行になった)

## [2026-05-17 00:35] ingest | raw/init.txt と 3 つの一次ソース（GitHub repo、議事メモ Google Doc、oss_weekly_reporter 2026-05-06 週）を取り込み、初期ページ群を作成

- sources/: meeting-minutes, github-dev-docs, weekly-log-2026-05-06
- concepts/: kouchou-ai, broadlistening, architecture-overview, pipeline, plugin-system, local-dev-setup, testing, deployment, llm-providers, coding-agents, contributing
- entities/: dd2030, talk-to-the-city, idobata, polimoney, broad-listening-book, nishio, tokoroten, nasuka, ohki-shingo, kuboon, anno, other-contributors
- analyses/: gotchas, versioning-strategy, npm-vs-pnpm, glossary
- 議事メモから書籍執筆スレッドは init.txt の指示に従い除外（broad-listening-book.md でスコープ宣言）
- 議事メモ本体（meeting_minutes.txt）は raw/ にコピー保存
