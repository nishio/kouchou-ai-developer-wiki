# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-10-05 23:04] filing-back | #943をマージし#395の残件を維持

- 最新HEADの実レビュー・CI成功を確認して#943をmainへ反映。[[catchup-2026-10-05]]に証拠を記録した。
- #395にSpreadsheet等の残件を維持し、[[current-status-2026-10-05]]・[[meeting-report-draft]]へ反映済み範囲と残る2PRを追記した。

## [2026-10-05 22:18] filing-back | #941の再レビュー成功とmain反映を確認

- #941の最新HEADの指摘なし・CI成功を確認してadmin mergeし、#130 CLOSEDを確認。[[catchup-2026-10-05]]へ証拠を記録した。
- [[current-status-2026-10-05]]・[[meeting-report-draft]]へ反映済み範囲と残る3PRを追記した。

## [2026-10-05 22:06] filing-back | #942をマージし#518の残要件を維持

- 最新HEADの実レビュー・CI成功を確認して#942をmainへ反映。[[catchup-2026-10-05]]に根拠を記録した。
- #518は常設URL等が残るためopenを維持。残る4PRのレビュー状況を[[current-status-2026-10-05]]・[[meeting-report-draft]]へ追記した。

## [2026-10-05 21:45] filing-back | #950・#944をマージし他PRのレビュー未実行と競合に対応

- 明示許可に基づくadmin mergeと#949の残件追跡を[[catchup-2026-10-05]]へ記録。#948のマージ済み状態も確認した。
- #941・#942の競合を解消し、5PRを最新mainと統合。CodeRabbitの成功表示と実レビューを区別し、[[current-status-2026-10-05]]・[[meeting-report-draft]]へ進行中の残条件を反映した。

## [2026-10-05 21:30] filing-back | #950のCodeRabbit再レビュー成功と必須承認待ちを記録

- 関数説明の警告を修正し、最新commitの再レビュー・CI成功を確認。[[catchup-2026-10-05]]に追記した。
- 通常マージはGitHubの必須承認未充足で拒否。継続確認を設定し、[[current-status-2026-10-05]]と[[meeting-report-draft]]へ未mergeの残条件を記録した。

## [2026-10-05 20:50] filing-back | 依存保守を#949で担当し更新PR #950を提出

- [[catchup-2026-10-05]]へ依存更新と互換性検証、未mergeの#950を記録。具体的な脆弱性詳細は非公開のrawに固定した。
- [[current-status-2026-10-05]]と[[meeting-report-draft]]へ、修正版のある範囲を先行し、残件を#949で追跡する判断を追記。main反映後の再評価とレビューが残る。

## [2026-10-05 20:21] filing-back | #947の非公開報告を有効化しSECURITY.md追加PR #948を提出

- #947を担当し、GitHubの非公開報告機能を有効化。公開報告ボタンと通知購読を確認した。[[catchup-2026-10-05]]より。
- SECURITY.mdと貢献ガイドの導線を#948へ提出。strict build成功、文書は未merge。[[current-status-2026-10-05]]と[[meeting-report-draft]]へ設定反映済み・レビュー待ちの区別を記録した。

## [2026-10-05 20:14] filing-back | #947の非公開報告機能と文書整備の範囲を確認

- [[catchup-2026-10-05]]へmain・Issue・open PR・非公開報告設定の再観測を追記。SECURITY.mdなし、非公開報告機能は無効だった。
- [[current-status-2026-10-05]]と[[meeting-report-draft]]へ、文書追加と受付窓口・通知確認を一組にする対応案を記録。調査のみでassign・PR作成・設定変更は行っていない。

## [2026-10-05 11:08] filing-back | lint孤立ページ13件の導線を復旧

- `python3 scripts/lint_wiki.py` で incoming wikilink のないページ13件を検出し、過去の issue / PR 判断、Windows実機メモ、ラベル評価依頼、行政RAG調査を既存ハブへ接続した。
- 再実行で孤立ページ、壊れたwikilink、index未登録、frontmatter不備はいずれも0件になった。ページ追加やsummary変更はしていないため `index.txt` は再生成していない。

## [2026-10-05 11:00] filing-back | 直前セッションの広聴AI事例整理文脈を保存

- 「これ何してたんだっけ」への復元として、直前作業が国内 broad listening 事例と TTTC→広聴AI lineage の wiki filing-back だったことを [[codex-session-recall-broadlistening-lineage-2026-10-05]] に記録した。
- 次の自然な一手は #564 公開事例ページの schema / 掲載候補 / 読み方ガイド整理だが、6月30日の観測は古いので [[current-status-2026-10-05]] を先に読む注意を [[meeting-report-draft]] へ接続した。

## [2026-10-05 10:58] filing-back | 3件のIssue実装から検証境界と設定保護の知見を整理

- [[next-three-issues-progress-2026-09-09]]へ再利用できる3点と観測時点を追記し、[[testing]]へ反映。
- [[meeting-report-draft]]を更新。実装結果の再検証はしていない。
- grasp書込基盤（wiki.grasp/events.jsonl）が未導入のため、既存のMarkdown運用で更新。

## [2026-10-05 10:44] filing-back | 韓国からの取材に向けたデータ分析の公開範囲を記録

- [[interview-analysis-request-2026-10-05]] に、韓国からの取材対応のためデータ分析を試す依頼の概要を記録した。
- 定例下書きへ同じ概要を追記。公開記録はユーザーが許可した範囲に限定し、詳細を非公開で管理する。

## [2026-10-05 10:05] filing-back | 同一GitHub Pages origin上の別サイトへのリンク誤検出を修正

- 今回と直前の公開CIで、別プロジェクトへの絶対リンクがbase path逸脱とされる原因を確認。`check_pages_links.py`を修正した。
- 絶対hyperlinkを外部参照とし、相対逸脱・内部リンク切れ・asset逸脱は維持。回帰テスト5件をCIへ追加し、[[current-status-2026-10-05]]と定例メモへ記録。

## [2026-10-05 10:02] filing-back | 10月5日のコード・GitHub・Slack・議事録へキャッチアップ

- [[catchup-2026-10-05]] / [[current-status-2026-10-05]] にsource鮮度と現在地を固定。本体mainは据え置き、#941〜#946はCI成功・必須レビュー待ち、#947は新規未担当。
- Serverless #22〜#26のmain反映を確認し、製品方針ページの未merge記録へ補足。依存更新4PRのbuild失敗は未調査として残した。
- 議事録txt/htmlとSlack snapshotを更新し、定例下書きの先頭側に今回の読み上げメモを追記。grasp書き込み未導入のため既存Markdown方式で保存した。
- 索引再生成で過去の未検証留保が消える不整合を検出し、KJ法関連2ページのfrontmatterへ反映して再生成した。

## [2026-09-30 23:59] filing-back | 別リポジトリでの drastic refactor は提案だったと明記

- wiki森の public wiki 12個を grasp `cross-project-spreads` で同名 handle ごとに束ね、Gemini（3.8 Flash medium / 3.1 Pro）に wiki をまたぐ食い違いを挙げさせ、Claude が原文と照らして判定した（2026-09-30、galleria の taskF）。Gemini の修正案はそのまま当てていない。
- [[plugin-system]] の節「drastic refactor は別リポジトリで」が現在の方針に読めた。見出しを「という提案（2025-10-08）」に変え、実際は main 上の段階移行になったこと（[[refactoring-status]]）を追記。
