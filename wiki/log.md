# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

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
