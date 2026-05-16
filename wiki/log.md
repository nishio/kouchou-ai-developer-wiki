# Log

## [2026-05-17 07:51] lint | `embeddings.pkl` 記述補正後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0

## [2026-05-17 07:50] filing-back | `embeddings.pkl` が UMAP 後 2D という記述をコード照合で補正

- `work/kouchou-ai/` の `main@3809a7a` を確認し、`packages/analysis-core/src/analysis_core/steps/embedding.py` が元の埋め込みベクトルを `embeddings.pkl` に保存することを確認
- `packages/analysis-core/src/analysis_core/steps/hierarchical_clustering.py` が `embeddings.pkl` を読んだ後で UMAP 2D 化することを確認
- [[pipeline]] / [[gotchas]] / [[slack-design-intents-2025-q4]] / [[slack-dev-kouchouai-2025-q4]] / [[source-code]] を更新し、Slack 上の認識とコード実装を分離

## [2026-05-17 07:35] ingest | `#2_開発_広聴ai` の 2026-Q1 ログから設計意図を抽出して Wiki に反映

- `work/oss_weekly_reporter` の `data` ブランチを参照し、2026-05 から遡って `#2_開発_広聴ai` を横断 grep
- 設計意図が濃い 2026-01-14 〜 2026-03-04 の 6 週分を `raw/oss_weekly_reporter/2026-q1-dev-kouchou-ai/` にコピー保存
- 新規 source [[slack-dev-kouchouai-2026-q1]] を追加し、`Jigsaw` 系 LLM 分類、再利用機能、plugin UX、可視化分離の意図を整理
- 新規 analysis [[slack-design-intents-2026-q1]] を追加
- [[pipeline]] / [[plugin-system]] / [[open-decisions]] / [[index]] を更新

## [2026-05-17 07:36] lint | Slack 由来ページ追加後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備は 0
- 新規 analysis の孤立を避けるため [[slack-dev-kouchouai-2026-q1]] からリンク追加

## [2026-05-17 07:39] ingest | `#2_開発_広聴ai` の 2025 4Q ログも source 化して前史を整理

- 2025-10〜12 の `#2_開発_広聴ai` を横断し、現行方式の限界認識、SenseMaker志向、JSON/YAML カスタマイズ、v4/v5 二段構えが濃い 7 週分を `raw/oss_weekly_reporter/2025-q4-dev-kouchou-ai/` に保存
- 新規 source [[slack-dev-kouchouai-2025-q4]] を追加
- 新規 analysis [[slack-design-intents-2025-q4]] を追加
- [[index]] と [[slack-dev-kouchouai-2026-q1]] を更新して、2025 4Q → 2026 Q1 の流れを辿れるようにした

## [2026-05-17 02:05] ingest | Open PR 観測を Wiki の更新手順に追加

- `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` で 2026-05-17 時点の open PR を確認
- `CLAUDE.md` に、current state を扱う時は open PR も観測するルールを追記
- [[contributing]] に open PR の見方と当日時点の主要 PR (`#825`, `#824`, `#817`, `#823`, `#822`) を追記
- [[open-decisions]] に、C カテゴリが open PR 観測を含むことを明記

## [2026-05-17 02:01] ingest | 議事メモの最新 export を再取得し、参照日付を `2026/05/18（次回分）` に更新

- Google Doc export から `raw/meeting_minutes.txt` を再取得。差分は先頭見出し `2026/05/11（次回分）` → `2026/05/18（次回分）` と `2026/05/04` 見出しの整形
- [[meeting-minutes]] に refresh protocol を追記し、source 更新前に `raw/meeting_minutes.txt` を取り直す運用を明記
- `2026-05-11` を会議実日付のように読める記述を、`2026-05-18 見出し` 表記へ補正

## [2026-05-17 02:00] ingest | Claude Code 生成 Wiki の主張を `main@3809a7a` に照合し、古くなった断定を補正

- `work/kouchou-ai/` を `git fetch origin && git pull --ff-only` で最新確認。local `main` は引き続き `3809a7a`
- [[gotchas]] / [[llm-providers]]: LOCAL LLM の HTTPS 対応は main コード上まだ `http://{host}:{port}/v1` 前提と分かるため、「修正済み」断定を撤回
- [[open-decisions]]: CodeRabbit は `.coderabbit.yaml` により最小導入済み、レポート再利用機能は API / UI / docs まで main に存在するため「未完了」一覧から除外
- [[plugin-system]] / [[refactoring-status]] / [[versioning-strategy]]: frontend 側 chart plugin 基盤が実装済みであることを反映

## [2026-05-17 01:48] ingest | DeepWiki を補助ソースとして登録し、コード更新時は local clone 最新化を先に行う運用を明文化

- `work/kouchou-ai/` で `git fetch origin` を実行し、local `main` tip `3809a7a` が origin と一致することを確認
- 新規 source ページ [[deepwiki-kouchou-ai]] を追加。DeepWiki は 2026-02-14 / `f894ce` 時点の補助ソースとして扱う
- [[source-code]] に refresh protocol を追記し、コード由来の更新前に local clone を pull するルールを追加
- `CLAUDE.md` の Ingest / 運用方針にも、local clone 優先・DeepWiki は補助線という原則を追記

## [2026-05-17 01:50] filing-back | work/ の運用合意を CLAUDE.md スキーマに反映

## [2026-05-17 08:47] filing-back | UMAP warning の扱いを wiki に記録

- `analysis-core` の `hierarchical_clustering` が出す `umap-learn` の `UserWarning` は、再現性優先の副作用であり現時点では failure 扱いしないと整理
- [[gotchas]] に「既知で許容、将来 seed / 並列性オプション追加時に再整理」を追記
- [[testing]] に現時点の運用判断として追記

## [2026-05-17 07:53] lint | PyPI自動更新要件ページ追加後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0
- 新規 `[[pypi-auto-release-requirements]]` は index 登録済み。孤立扱いは本文からの inbound link 未追加によるもの

## [2026-05-17 07:53] filing-back | PyPI自動更新に必要な要件を整理 ([[pypi-auto-release-requirements]])

- 現状は `docs/development/pypi-release.md` に参考 workflow があるだけで、実 `.github/workflows/` に publish job は未実装
- 必須要件を「workflow / PyPI secrets / package 専用 test-lint / tag 規約」に整理
- `v*` と `analysis-core-v*` の tag 規約差分、`apps/api` CI だけでは package 配布の gate にならない点を明記

- ディレクトリ構造図に `work/` を追加し「実装確認用の local clone を置く場所、gitignored、`/tmp` は ephemeral なので永続参照はここへ」を明記
- 既に [[source-code]] と [[local-dev-setup]] には個別に追記済みだったが、スキーマファイル側にも書かないと将来のエージェントが場所を勝手に決めてしまう

## [2026-05-17 01:41] lint | setup 追記後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0

## [2026-05-17 01:40] setup | Wiki 配下で実装確認するための local clone 置き場を `work/kouchou-ai/` に統一

- `git clone --depth 1 https://github.com/digitaldemocracy2030/kouchou-ai.git work/kouchou-ai` を実行
- clone 先は `main` / tip `3809a7a`

- `.gitignore` に `work/` を追加して親 Wiki repo から除外
- [[source-code]] と [[local-dev-setup]] に、AI コーディングエージェント向けの推奨 clone 位置を追記

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
