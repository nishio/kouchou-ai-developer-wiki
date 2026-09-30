# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-09-30 23:59] filing-back | 別リポジトリでの drastic refactor は提案だったと明記

- wiki森の public wiki 12個を grasp `cross-project-spreads` で同名 handle ごとに束ね、Gemini（3.8 Flash medium / 3.1 Pro）に wiki をまたぐ食い違いを挙げさせ、Claude が原文と照らして判定した（2026-09-30、galleria の taskF）。Gemini の修正案はそのまま当てていない。
- [[plugin-system]] の節「drastic refactor は別リポジトリで」が現在の方針に読めた。見出しを「という提案（2025-10-08）」に変え、実際は main 上の段階移行になったこと（[[refactoring-status]]）を追記。
