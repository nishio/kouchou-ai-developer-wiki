# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-10-05 10:02] filing-back | 10月5日のコード・GitHub・Slack・議事録へキャッチアップ

- [[catchup-2026-10-05]] / [[current-status-2026-10-05]] にsource鮮度と現在地を固定。本体mainは据え置き、#941〜#946はCI成功・必須レビュー待ち、#947は新規未担当。
- Serverless #22〜#26のmain反映を確認し、製品方針ページの未merge記録へ補足。依存更新4PRのbuild失敗は未調査として残した。
- 議事録txt/htmlとSlack snapshotを更新し、定例下書きの先頭側に今回の読み上げメモを追記。grasp書き込み未導入のため既存Markdown方式で保存した。
- 索引再生成で過去の未検証留保が消える不整合を検出し、KJ法関連2ページのfrontmatterへ反映して再生成した。

## [2026-09-30 23:59] filing-back | 別リポジトリでの drastic refactor は提案だったと明記

- wiki森の public wiki 12個を grasp `cross-project-spreads` で同名 handle ごとに束ね、Gemini（3.8 Flash medium / 3.1 Pro）に wiki をまたぐ食い違いを挙げさせ、Claude が原文と照らして判定した（2026-09-30、galleria の taskF）。Gemini の修正案はそのまま当てていない。
- [[plugin-system]] の節「drastic refactor は別リポジトリで」が現在の方針に読めた。見出しを「という提案（2025-10-08）」に変え、実際は main 上の段階移行になったこと（[[refactoring-status]]）を追記。
