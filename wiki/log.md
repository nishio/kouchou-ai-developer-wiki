# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-06-30 14:15] filing-back | #876 developer docs PR slice を具体化

- [[github-issue-876-live-2026-06-30]] を追加し、issue #876 が open / nishio assigned のまま、PR #883 撤回後の 5 読者像・Mode 1 default 廃止方針が issue 本文に反映済みであることを GitHub live state として固定
- [[issue-876-docs-pr-slice-2026-06-30]] を追加し、次の本体 docs PR を `developer-quickstart` 単体ではなく mkdocs nav、README、docs/index、getting-started/quickstart の役割調整まで含める file-by-file first slice として整理
- [[docs-issue-map-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から #876 の次 action へ接続

## [2026-06-30 14:08] filing-back | Spherical K-means / Faiss K-means Slack 議論を整理

- [[slack-algorithm-kmeans-2026-06-29]] を追加し、`work/slack-logs/main@341cf8022d32` の `#2_開発_広聴ai_アルゴリズム開発` mirror から 2026-06-29 の embedding / Spherical K-means / Faiss K-means 言及を source 化
- [[spherical-kmeans-experiment-scope-2026-06-30]] を追加し、current main の「元 embedding → 2D UMAP → sklearn KMeans → ward merge」を baseline に、clustering space / objective / backend を分けて clean experiment 化する方針を整理
- [[source-code]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から、採用判断ではなく実験候補として接続

## [2026-06-30 14:01] filing-back | PR #903 review comment draft を追加

- [[pr-903-review-comment-draft-2026-06-30]] を追加し、PR #903 へ直接投稿せず、last verified / Server Actions count / static-site-builder dev script / CSV・JSON download actions の 4 点をコメント案として固定
- PR #903 は open / review required / blocked のまま、差分は `docs/development/web-ui-node-runtime-dependencies.md` 1 ファイル追加で変化なしと確認
- [[pr-903-node-runtime-doc-review-2026-06-30]] / [[docs-issue-map-2026-06-30]] / [[meeting-report-draft]] からコメント案へ接続

## [2026-06-30 13:57] filing-back | #876 developer docs の gap audit を追加

- [[issue-876-developer-docs-gap-audit-2026-06-30]] を追加し、PR #883 撤回後草案、6/3 docs spine 議論、Azure demo 動線化議論、current main docs を照合
- developer quickstart 草案は 5 読者像 / Mode 1 default 廃止などを概ね満たす一方、README / docs index / quickstart / mkdocs nav は setup-first のままと整理
- [[docs-issue-map-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] に #876 の次 PR scope 判断を接続

## [2026-06-30 13:51] filing-back | #877 Windows guide outline を具体化

- [[windows-setup-guide-outline-2026-06-30]] を追加し、#877 の Windows setup guide を本体 docs PR に落とす前の章立て、対象 / 対象外、troubleshoot 表を固定
- current main `d5c9ece` の `docs/getting-started/windows-setup.md` は `setup_win.ps1` 導線を含む一方、API key 前提と組織管理端末の非対象分岐が弱いことを整理
- [[docs-issue-map-2026-06-30]] / [[current-status-2026-06-30]] / [[meeting-report-draft]] から #877 の次アクションへ接続

## [2026-06-30 13:42] filing-back | docs 系 issue の横断地図を追加

- [[docs-issue-map-2026-06-30]] を追加し、#876 developer quickstart、#877 Windows setup guide、#885 Node runtime 排除、PR #903 inventory docs の関係を整理
- #876 は入口設計、#877 は現行 Windows supported path、#885/#903 は将来の単一 exe 前提と切り分け、同じ docs 群でも混ぜない方針を明示
- [[current-status-2026-06-30]] と [[meeting-report-draft]] から横断地図へリンク

## [2026-06-30 13:27] filing-back | PR #903 と issue #898 の docs-safe 現状整理

- [[pr-903-node-runtime-doc-review-2026-06-30]] を追加し、human authored PR #903 に直接 push せず、CodeRabbit 指摘と current main の server action inventory 漏れ候補を整理
- [[issue-898-close-readiness-2026-06-30]] を追加し、PR #899 merge 済みの issue #898 は aarch64 Docker 解消確認前に AI 単独 close しない方針を明示
- [[meeting-report-draft]] に docs-first / no-conflict lane として次に見る順序を追記

## [2026-06-30 13:10] filing-back | 議事録と Slack log の freshness を更新

- 議事録 Google Doc export を再取得し、[[meeting-minutes]] を `last_checked: 2026-06-30` / 先頭見出し `2026/06/22` / txt 7702 行 / URL unique 551 件へ更新
- `digitaldemocracy2030/slack-logs` を `work/slack-logs/` に clone / pull し、[[slack-logs-repository]] を追加。mirror は `synced_at=2026-06-30T04:12Z` / window `2026-06-16〜06-30`
- Slack raw の一次参照を `slack-logs` の `mirror/` / `raw/` に更新し、`oss_weekly_reporter` は週次 AI 要約 / GitHub activity 補助線として整理。あわせて [[current-status-2026-06-30]] に current snapshot を固定
