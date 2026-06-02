---
type: source
summary: "2026-06-02 に nishio が、Wiki の情報鮮度は議事録をいつ時点まで読んだか、Slack をいつ時点まで読んだかを基準として明示すべきだと指摘したメモ"
sources:
  - user-message-2026-06-02
---

## What it is

2026-06-02 の nishio からの短い運用改善メモを source 化したもの。

要点は、Wiki の情報がどれだけ新しいかを、ページ更新日だけでなく **議事録をいつ時点まで読んだか / Slack をいつ時点まで読んだか** で判断できるようにすべき、という指摘である。

## Extracted Points

- 議事録 Google Doc と Slack / `oss_weekly_reporter` は追記され続ける source なので、Wiki ページの更新日時だけでは鮮度が分からない。
- `meeting-minutes` 系 source では、Google Doc export を最後に取り直した日、先頭見出し、対象範囲を明示する必要がある。
- Slack 系 source では、最後に読んだ日、対象 channel、対象週または対象期間、raw snapshot の有無を明示する必要がある。
- 最新確認なしで答える場合は、Wiki の既存記述を「その source marker 時点の観測」として扱い、最新状態の断定には使わない。

## Related Pages

- [[wiki-driven-workflow]]
- [[meeting-minutes]]
- [[slack-dev-kouchouai-2025-q4]]
- [[slack-dev-kouchouai-2026-q1]]
- [[slack-kouchouai-algorithm-dev]]
- [[weekly-log-2026-05-06]]

## Open Questions

- Slack source が増えた時、全ページに `last_read` / `coverage` frontmatter を必須化するか。
- `oss_weekly_reporter` の latest data branch 到達日と、そこから Wiki が実際に読んだ対象週を別々に管理するべきか。
- 議事録や Slack を再取得したが Wiki 本文の判断が変わらなかった場合、log に残す粒度をどうするか。

## Updates

- 2026-06-02: 初版作成。
