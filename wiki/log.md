# Log

## [2026-05-18 23:21] filing-back | Azure deploy login failure は rerun で再現しなかったことを記録

- [[deployment]] に、`Azure Deployment` workflow の `azure/login@v2` が `No subscriptions found` で落ちた後、同じ run の rerun では `Azure CLI ログイン` が成功した観測を追記
- 今回の deploy failure については、恒久的な `AZURE_CREDENTIALS` 破損と断定せず、一時的な Azure 側不調や secret / RBAC 状態の揺れも候補に残す整理へ修正

## [2026-05-18 23:41] filing-back | draft PR は merge せず ready 化してから扱う運用を追記

- [[contributing]] に、draft PR は merge 手順に入っていない状態とみなし、ready for review にしてから merge 判断へ進むメモを追記
- [[coding-agents]] に、AI エージェント起点の draft PR も同様に ready 化を人間判断のゲートにする運用を追記

## [2026-05-18 23:05] filing-back | merge 理由コメントと通常 merge 優先の方針を追記

- [[pr-824-admin-merge-observation-2026-05-18]] に、「admin merge が通る」観測をそのまま推奨せず、理由コメントと approve を先に残す運用方針を update として追記
- [[contributing]] に、merge 手順を「rationale comment → approve → 通常 merge → admin merge fallback」の順で扱うメモを追記
- [[gotchas]] に、admin merge だけで押し切ると判断根拠がタイムラインに残りにくいという運用上の注意を追記

## [2026-05-18 23:01] filing-back | `PR #824` merge で見えた admin merge と review requirement の差を記録

- 新規 source [[pr-824-admin-merge-observation-2026-05-18]] を追加し、checks success / `REVIEW_REQUIRED` / `gh pr merge --admin` 成功が併存した観測を記録
- [[gotchas]] に、通常 merge 可否と admin merge 可否を分けて見る必要があることを追記
- [[contributing]] に、owner 観点の PR triage では review requirement と admin merge を別軸で扱うメモを追記
- [[index]] を更新して source を登録

## [2026-05-18 20:12] filing-back | `PR #810` 背景の seed 固定経緯を source / analysis 化

- 新規 source [[seed-reproducibility-history]] を追加し、`work/kouchou-ai/` のコード履歴、2025-05 の Slack / issue 群、2025-07 の並列化議論、2026-02 の `PR #810` を束ねた
- 新規 analysis [[umap-seed-history]] を追加し、seed 固定を「完全再現性の設計」ではなく「見た目の揺れを抑えたい要求から生まれ、後に並列性とのトレードオフとして見直された折衷」と整理
- [[index]] を更新して source / analysis を登録

## [2026-05-18 19:31] ingest | `#2_開発_広聴ai_アルゴリズム開発` を source / analysis 化

- 新規 source [[slack-kouchouai-algorithm-dev]] を追加し、`work/oss_weekly_reporter/data/*/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` を 2025-04 〜 2026-03 で横断読解した論点を整理
- 新規 analysis [[slack-algorithm-themes]] を追加し、UMAP後クラスタリング批判、分析と可視化の分離、対立軸・taxonomy・LLM分類の流れを整理
- [[pipeline]] と [[gotchas]] に本チャンネルを一次ソースとして接続し、[[index]] を更新

## [2026-05-18 19:31] lint | アルゴリズム開発チャンネル取り込み後の健全性確認

- `python3 scripts/lint_wiki.py` 実行。壊れた wikilink / index 未登録 / フロントマター不備はいずれも 0

## [2026-05-18 16:55] ingest | `PR #827` の LLM grouping 計画を source repo Markdown ではなく wiki 文脈へ取り込み

- 新規 source [[pr-827-llm-grouping-capabilities-plan-2026-05-18]] を追加し、`PLAN_llm_grouping_capabilities.md` の要点を要約
- [[pipeline]] に、PR `#827` が「`embedding` 後の LLM 分類互換枝」と `analysis_capabilities` / `requirements` 設計をどう具体化したかを追記
- [[open-decisions]] B14 を更新し、Jigsaw 系 LLM 分類は「意図だけ」ではなく doc-only の plan PR までは進んだと整理

## [2026-05-18 16:32] filing-back | `#823` merge 時の review requirement と Codex 署名ルールを記録

- [[pr-823-review-observation-2026-05-18]] に、head 更新後は approval が剥がれて `REVIEW_REQUIRED` に戻ることがある観測を追記
- [[contributing]] に、checks success 後も review requirement を見直す運用メモと、AI エージェント comment に `by Codex` 署名を付ける提案を追記
- [[gotchas]] に、merge blocker が CI ではなく approval 再取得である場合があることと、AI comment の由来がタイムライン上で埋もれやすいことを追記

## [2026-05-18 14:05] filing-back | nishio 以外の人間 authored open PR の現状を snapshot 化

- 新規 source [[open-pr-snapshot-2026-05-18]] を追加し、2026-05-18 時点の open PR を nishio authored / bot authored / nishio 以外の人間 authored に分類
- 新規 analysis [[non-nishio-human-pr-status]] を追加し、`#734` と `#597` が古い draft かつ `mergeable: false` の stale 状態に見えることを整理
- [[index]] を更新して source / analysis を登録

## [2026-05-18 14:12] filing-back | stale PR cleanup と `tokoroten` / `ohki` recent PR の状況を反映

- `#734` と `#597` に stale 理由をコメントして close
- [[open-pr-snapshot-2026-05-18]] / [[non-nishio-human-pr-status]] を更新し、cleanup 後は non-nishio human open PR が `#817` (`shingo-ohki`) のみになったことを反映
- `tokoroten` の recent PR は `#812` `#811` `#807` が merged 済み、`ohki-shingo` は merged `#808` に加えて open `#817` があることを追記

## [2026-05-18 14:24] filing-back | `Issue #493` / `PR #597` の UX 議論を source 化

- 新規 source [[issue-493-pr-597-discussion]] を追加し、ScatterChart スクロール誤操作対策の issue / PR コメントを整理
- 新規 analysis [[chart-scroll-ux-decision]] を追加し、click-to-enable を避けて「短い遅延付きの自動ロック解除」が支持されたことと、shared preview 不足が stale 化要因だったことを整理
- [[gotchas]] に、体感依存 UI は preview 導線がないと議論が止まりやすいという運用上の教訓を追記

## [2026-05-18 14:31] filing-back | `Issue #493` / `PR #597` 議論が PC 前提だったことを明記

- [[issue-493-pr-597-discussion]] に、mouse / hover / wheel 中心の議論で、スマホ操作は主題に入っていないことを追記
- [[chart-scroll-ux-decision]] に、当時の結論をモバイルへそのまま一般化しない方がよいという注記を追加

## [2026-05-18 14:38] filing-back | スマホ向け代替案として「静的画像 → 全体ビュー」を追記

- [[chart-scroll-ux-decision]] に、モバイルでは散布図を最初は画像で見せ、必要時だけインタラクティブ全体ビューへ遷移する案を追記
- [[open-decisions]] の A7 に、スマホ散布図表示の未決論点として同案を追加

## [2026-05-18 13:42] filing-back | `PR #823` 切り分けで見えた `public-viewer` build gotcha を記録

- 新規 source [[pr-823-review-observation-2026-05-18]] を追加し、`main@3809a7a` / `pr-823` 比較、API なし build の timeout、mock API 下での `Reporter` `ERR_INVALID_URL` を整理
- 新規 analysis [[public-viewer-build-behavior]] を追加し、「security bump 回帰ではなく build-time API 条件の問題として読むべき」ことを明文化
- [[gotchas]] に `public-viewer` の API reachable 前提と `API_BASEPATH` 依存を追記

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

## [2026-05-18 13:18] filing-back | open PR review triage で得た branch/head 更新の gotcha を記録

- 新規 source ページ [[open-pr-observation-2026-05-18]] を追加。`#824` `#825` `#826` は既存 head branch push で更新でき、`#794` は close + recreate が必要だった観測を整理
- [[contributing]] に「review fix を push する前に PR metadata と remote branch 実体の両方を確認する」運用メモを追記
- [[gotchas]] に stale PR の head branch drift を追加

## [2026-05-18 19:48] filing-back | 書籍リリース前提の開発計画を整理

- 新規 analysis ページ [[book-release-development-plan-2026-09]] を追加
- 2026-09 ごろの書籍リリースを前提に、stable v4.x の維持、CLI/static output/viewer の再現性向上、release 運用整備を 9 月前の優先課題として整理
- plugin default 化や Jigsaw 系本格導入は出版後に回す案として位置づけた

## [2026-05-18 19:50] filing-back | 書籍で使い方を紹介しない前提を反映

- [[book-release-development-plan-2026-09]] を更新し、計画の軸を「書籍で説明する導線」から「新規流入者の受け皿整備」と「contribution しやすい地盤作り」へ修正
- [[contributing]] に、新規流入者が最初の 1 回で詰まらないための観点を追記

## [2026-05-18 19:54] filing-back | v5 は間に合う範囲なら入れる前提を反映

- [[book-release-development-plan-2026-09]] を更新し、v5 を全面後ろ倒しするのではなく「受け皿整備を優先しつつ、安全に入れられる要素は 9 月前に限定投入する」方針へ修正
- `default 化` と `限定投入` を分けて整理し、open PR triage の基準にも反映

## [2026-05-18 19:55] filing-back | v5 を主戦場にして安定化する前提へ再修正

- [[book-release-development-plan-2026-09]] を全面更新し、「stable v4 を守る」寄りの構図から、「v5 を main の正規経路として押し上げ、9 月までに安定化する」計画へ修正
- `run_workflow()` / plugin system / capability 判定の default 化を検討対象の中心に据え、受け皿整備はその補助線として再配置

## [2026-05-18 19:57] filing-back | v4 回帰をテストで保証しつつ v5 へ移行する方針を反映

- [[book-release-development-plan-2026-09]] を更新し、「v5 を進める」と「v4 の既存機能が壊れていないことをテストで保証する」を両立させる計画へ修正
- [[testing]] に、v5 移行期のテスト責務として v4 ユースケース固定と回帰検知帯の考え方を追記

## [2026-05-18 13:40] filing-back | AI エージェントの権限分離と devcontainer 方針を整理

- 新規 analysis ページ [[agent-sandboxing-strategy]] を追加。host full access を標準にせず、devcontainer を編集面、Docker Compose を実行面、高権限操作を CI / 人間に分離する方針を整理
- [[local-dev-setup]] に、AI エージェント向けには devcontainer と Compose の役割分離が望ましい旨を追記
- [[coding-agents]] に、AI の作業権限と deploy / credential 権限を分ける運用方針への参照を追記

## [2026-05-18 21:21] filing-back | `PR #817` 文脈の CodeQL 導入理由を整理

- 新規 source ページ [[codeql-docs]] を追加し、CodeQL 公式 docs から「静的解析による security scanning」という役割を要約
- 新規 source ページ [[pr-813-817-codeql-coderabbit-observation-2026-05-18]] を追加し、`PR #813` での accidental inclusion と `PR #817` での設定見直しを記録
- 新規 analysis ページ [[codeql-introduction-context]] を追加し、「導入目的は security scan 自動化だが、発火点は accidental inclusion」という整理を残した

## [2026-05-18 21:21] lint | CodeQL 導入文脈の filing-back 後の健全性確認

- `python3 scripts/lint_wiki.py` を実行
- URL を wikilink 扱いしていた 2 件を修正し、`index.md` 未登録や frontmatter 不備がないことを確認
- `codeql-introduction-context` は index 経由のみの参照で孤立扱いだが、意図した単発 analysis として許容

## [2026-05-17 01:48] ingest | DeepWiki を補助ソースとして登録し、コード更新時は local clone 最新化を先に行う運用を明文化

- `work/kouchou-ai/` で `git fetch origin` を実行し、local `main` tip `3809a7a` が origin と一致することを確認
- 新規 source ページ [[deepwiki-kouchou-ai]] を追加。DeepWiki は 2026-02-14 / `f894ce` 時点の補助ソースとして扱う
- [[source-code]] に refresh protocol を追記し、コード由来の更新前に local clone を pull するルールを追加
- `CLAUDE.md` の Ingest / 運用方針にも、local clone 優先・DeepWiki は補助線という原則を追記

## [2026-05-17 01:50] filing-back | work/ の運用合意を CLAUDE.md スキーマに反映

## [2026-05-17 08:47] filing-back | `analysis-core-v*` を release tag 規約として採用

- [[pypi-auto-release-requirements]] から `v*` / `analysis-core-v*` の比較を外し、`analysis-core-v*` 採用済み前提へ更新
- 次の publish workflow 実装が `push.tags: ['analysis-core-v*']` を trigger にすべきことを明記

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
