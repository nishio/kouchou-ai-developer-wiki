---
type: source
summary: "議事メモ Google Doc の HTML export から、`txt` では落ちる URL を抽出して分類した棚卸し"
sources:
  - meeting-minutes.md
---

## What it is

[[meeting-minutes]] の `raw/meeting_minutes.html` から URL を抽出し、`raw/meeting_minutes_urls.tsv` と `raw/meeting_minutes_urls_summary.md` に整理した派生 source。`txt` export では落ちるリンク先 URL や、ラベルだけ見えていた anchor の実体を再回収するための棚卸しである。[[meeting-minutes]]より

2026-05-25 時点の抽出結果は **531 unique URLs / 89 domains**。主な内訳は次の通り。

- `kouchou-ai repo`: 136
- `weekly history` (`dd2030.org/history/...`): 81
- `slack permalink`: 49
- `google docs/drive`: 28
- `broad-listening-book`: 52
- `external web`: 131

つまり、議事録のリンク群は **広聴AI本体への導線** と **周辺資料・書籍系の外部参照** が混在しており、`txt` だけでは後者の URL をかなり取りこぼす。[[meeting-minutes]]より

## Extraction method

`scripts/extract_meeting_minutes_urls.py` を追加し、以下を行う。

1. `raw/meeting_minutes.html` を document order で読み、直近の `YYYY/MM/DD` 見出しを持ちながら `<a href>` を抽出
2. Google Docs 特有の `https://www.google.com/url?q=...` を実 URL にデコード
3. anchor だけでなく、本文にベタ書きされた URL も追加回収
4. `kouchou-ai repo` / `weekly history` / `slack permalink` / `google docs/drive` / `broad-listening-book` などに分類

これで、たとえば **リンクラベルしか見えない Figma / Google Docs / Slack permalink** や、GitHub issue / PR の直 URL を後から grep 可能な形へ戻せる。[[meeting-minutes]]より

## Why it matters

- **current state の追跡**: `kouchou-ai` の issue / PR / docs 直リンクが 136 件あり、議事録内の「あの時どの PR を見ていたか」を URL 単位で辿りやすくなる
- **Slack 週次ログとの接続**: `dd2030.org/history/...` が 81 件、Slack permalink が 49 件あり、議事録から週次履歴や Slack 原文へ戻る導線が見える
- **スコープ管理**: `broad-listening-book` 52 件と `external web` 131 件が混ざるので、`raw/init.txt` のスコープ外話題を分離する時の補助線になる

## Caveats

- これは HTML export 由来の派生棚卸しであり、議事録本文の要約 source を置き換えるものではない。本文の意味理解は引き続き [[meeting-minutes]] を主に使う
- category は URL pattern ベースの粗い分類なので、`external web` には自治体事例・報道・雑多な参考資料が同居する
- Google Docs export の崩れ方次第で、稀に URL の重複や結合が起きうるため、厳密な引用前には原文確認が必要

## Open Questions

- `external web` 131 件を、自治体事例 / 報道 / 個人メモ / AI 生成物などにもう一段分解するべきか
- `broad-listening-book` 系を自動でスコープ外タグ付けし、広聴AI本体のリンクだけ別出力にするべきか

## Updates

- 2026-05-25: `raw/meeting_minutes.html` を取得し、`scripts/extract_meeting_minutes_urls.py` で URL 531 件を抽出。`raw/meeting_minutes_urls.tsv` と `raw/meeting_minutes_urls_summary.md` を生成
