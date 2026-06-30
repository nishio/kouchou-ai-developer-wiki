# Log

> 直近 7 日分のみ。全件 compact 履歴は [log.txt](log.txt)、それより古い entry の詳細は `git log -- wiki/log.md` で参照。
> 更新は `python3 scripts/refresh_logs.py` で log.txt と log.md を再生成する。

## [2026-06-30 13:10] filing-back | 議事録と Slack log の freshness を更新

- 議事録 Google Doc export を再取得し、[[meeting-minutes]] を `last_checked: 2026-06-30` / 先頭見出し `2026/06/22` / txt 7702 行 / URL unique 551 件へ更新
- `digitaldemocracy2030/slack-logs` を `work/slack-logs/` に clone / pull し、[[slack-logs-repository]] を追加。mirror は `synced_at=2026-06-30T04:12Z` / window `2026-06-16〜06-30`
- Slack raw の一次参照を `slack-logs` の `mirror/` / `raw/` に更新し、`oss_weekly_reporter` は週次 AI 要約 / GitHub activity 補助線として整理。あわせて [[current-status-2026-06-30]] に current snapshot を固定
