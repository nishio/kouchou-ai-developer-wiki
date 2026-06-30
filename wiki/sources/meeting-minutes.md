---
name: meeting-minutes
summary: "Google Doc 議事メモ — weekly kouchou-ai dev meeting minutes (2025-03 〜 2026-06, ~7700 lines, JP)"
type: source
url: https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/edit
last_checked: 2026-06-30
coverage: "2025-03-26頃〜2026-06-22 先頭見出し"
sources:
  - meeting_minutes.txt
  - nishio-source-freshness-criterion-2026-06-02.md
---

## What it is

[[kouchou-ai]] の週次開発会議「議事メモ」。Google Doc 1 本に reverse-chronological で全週分が追記され続けている。最新取得時点の先頭見出しは **2026/06/22**、最古は 2025/03/26 付近。各週のフォーマットは概ね統一されている：

```
YYYY/MM/DD（次回分）
会の趣旨 / お知らせ / 直近1週間の活動まとめ / 共有・相談等 / Issues確認 / 次回に向けて
```

「共有・相談等」が分量的にも内容的にも本体で、ハンドル別（nishio / tokoroten / nasuka / Ohki ...）の自由形式の活動報告と相談がまとまっている。

## Freshness marker

この source の鮮度基準は、**2026-06-30 19:04 JST に Google Doc export から `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を再取得した時点**。その時点の先頭見出しは `2026/06/22`、`2026/06/29` / `2026/06/30` 見出しは未検出、txt は 7703 行、HTML 由来の URL 棚卸しは unique 551 件だった。[[nishio-source-freshness-criterion-2026-06-02]]より

2026-06-22 より後の議事録内容を根拠にする場合は、まず `raw/meeting_minutes.txt` を再取得し、URL やリンク先が論点なら `raw/meeting_minutes.html` も更新する。HTML export は minified されることがあり、`wc -l` の行数は空/少数に見えてもファイルサイズと URL 抽出結果で確認する。

## Refresh protocol

議事メモを根拠にページを更新する前に、まず Google Doc export から `raw/meeting_minutes.txt` を取り直す：

```bash
curl -L -sS \
  'https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/export?format=txt' \
  > raw/meeting_minutes.txt
```

`txt` export は grep しやすい一方、**Google Doc 内リンクや貼り付け URL が本文から落ちることがある**。リンク先そのものが論点になる時は、同時に HTML も保存して参照する：

```bash
curl -L -sS \
  'https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/export?format=html' \
  > raw/meeting_minutes.html
```

通常の要約・grep・時系列確認は `txt` を主とし、**URL の復元やリンク先確認が必要な時だけ `html` を補助線にする**。

URL の棚卸しを一度まとめて取りたい時は、`scripts/extract_meeting_minutes_urls.py` を実行して `raw/meeting_minutes_urls.tsv` を生成する。派生 source の要約は [[meeting-minutes-url-extraction-2026-05-25]]。[[meeting-minutes-url-extraction-2026-05-25]]より

Google Doc の見出しは「次回分」を先に立てていることがある。したがって、**見出し日付をそのまま実会議日と見なさず、前後の文脈も確認する**。

## Scope

`raw/init.txt` の指示で **書籍執筆（[[broad-listening-book]] / [[tokoroten]] が主担当）の話は本 Wiki のスコープ外**。Wiki が扱うのは [[github-dev-docs]] が指すリポジトリ／開発者ドキュメントに紐づく範囲のみ。コードリポジトリに波及する範囲（バージョン凍結方針など）に限り取り込む。

## Coverage by topic

- **アーキテクチャ判断の根拠**: [[plugin-system]] への移行理由、[[versioning-strategy|v4 凍結 / v5 大規模リファクタ]]、[[talk-to-the-city|TTTC]] からフォークした理由、DB 導入を保留する理由など、コードを読むだけでは復元できない「なぜそうしたか」が一次ソースとして残っている
- **再発する痛点**: Windows インストール地獄、LOCAL LLM が HTTPS を喋れない、デフォルトクラスタ数が少なすぎる、`extraction` を skip したい、など複数回の会議で繰り返し挙がるもの。詳細は [[gotchas]]
- **コントリビュータの役割分担**: 個人ハンドルごとの主担当領域（[[nishio]]: 研究/リファクタ, [[tokoroten]]: LocalLLM/書籍, [[nasuka]]: 抽出/プロンプト, [[ohki-shingo]]: Azure/対外, ほか）
- **自治体・政党の利用実績**: 宇多津町、広島県、八代市、奈良、渋谷、郡山、朝日新聞、富士通、サイボウズ ... が時系列で言及される

## Open Questions

- ドキュメントが Google Doc 1 本に集約されているため、過去回の検索が grep ベース。古い議論を引きたいときは日付で grep する運用
- `txt` export だけではリンク URL が見えない週がある。URL 自体を根拠にしたい時の fallback は `raw/meeting_minutes.html`
- 同名の人物が複数の表記（漢字/ローマ字/略称）で登場する — エイリアスを entities 配下のページで吸収する必要がある

## Updates

- 2026-05-17: 初回 ingest（次回分 2026/05/11 まで）
- 2026-05-17: Google Doc export から再取得し、先頭見出しが `2026/05/18（次回分）` に更新されていることを確認
- 2026-05-17: source 更新前に `raw/meeting_minutes.txt` を再取得する refresh protocol を追記
- 2026-05-25: `txt` export ではリンク URL が落ちることがあるため、`raw/meeting_minutes.html` を補助取得する運用を追記
- 2026-05-25: HTML export から URL を抽出する `scripts/extract_meeting_minutes_urls.py` と派生 source [[meeting-minutes-url-extraction-2026-05-25]] を追加
- 2026-05-25: Google Doc export から `raw/meeting_minutes.txt` を再取得し、先頭見出しが `2026/05/25（次回分）` になっていることを確認
- 2026-06-01: Google Doc export から `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を再取得し、先頭見出しが `2026/06/01（次回分）`、txt が 7654 行になっていることを確認。主題は `#887` deploy success false positive / public-viewer runtime build risk、Actions / CodeQL / Dependabot 警告、developer-quickstart 読者像、SaaS / Azure 体験環境、Windows standalone / local LLM route。デプロイ詳細と alert 詳細は公開 wiki へ転記しない
- 2026-06-02: source の鮮度基準として `last_checked` / `coverage` と Freshness marker を明示
- 2026-06-30: Google Doc export から `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を再取得し、先頭見出しが `2026/06/22`、txt が 7702 行になっていることを確認。主題は 8/2 イベントでブロードリスニングをどう出すか、Brand Compass / high priority issue / 情報発信 / 運用ポリシーの優先軸。HTML URL 棚卸しは unique 551 件へ更新
- 2026-06-30 16:33 JST: `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を再取得し、先頭見出しは引き続き `2026/06/22`、`2026/06/29` 見出しは未検出、txt は 7702 行、URL unique 551 件と再確認。8/2 イベントと優先軸の該当箇所は [[meeting-2026-06-22-event-priority]] に切り出した
- 2026-06-30 18:30 JST: `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を再取得し、先頭見出しは引き続き `2026/06/22`、`2026/06/29` 見出しは未検出、txt は 7702 行、URL unique 550 件と再確認。内容面では 16:33 観測から新しい議事録見出しは増えていない
- 2026-06-30 19:04 JST: `raw/meeting_minutes.txt` / `raw/meeting_minutes.html` を再取得し、先頭見出しは引き続き `2026/06/22`、`2026/06/29` / `2026/06/30` 見出しは未検出、txt は 7703 行、URL unique 551 件と再確認。内容面では 18:30 観測から新しい議事録見出しは増えていない
