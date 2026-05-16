---
name: meeting-minutes
summary: Google Doc 議事メモ — weekly kouchou-ai dev meeting minutes (2025-03 〜 2026-05, ~7300 lines, JP)
type: source
url: https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/edit
sources:
  - meeting_minutes.txt
---

## What it is

[[kouchou-ai]] の週次開発会議「議事メモ」。Google Doc 1 本に reverse-chronological で全週分が追記され続けている。最新取得時点の先頭見出しは **2026/05/18（次回分）**、最古は 2025/03/26 付近。各週のフォーマットは概ね統一されている：

```
YYYY/MM/DD（次回分）
会の趣旨 / お知らせ / 直近1週間の活動まとめ / 共有・相談等 / Issues確認 / 次回に向けて
```

「共有・相談等」が分量的にも内容的にも本体で、ハンドル別（nishio / tokoroten / nasuka / Ohki ...）の自由形式の活動報告と相談がまとまっている。

## Refresh protocol

議事メモを根拠にページを更新する前に、まず Google Doc export から `raw/meeting_minutes.txt` を取り直す：

```bash
curl -L -sS \
  'https://docs.google.com/document/d/1plggszRTxEEYUcZuCLiHkPrBsMtxr3RQpctKtZe5y4M/export?format=txt' \
  > raw/meeting_minutes.txt
```

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
- 同名の人物が複数の表記（漢字/ローマ字/略称）で登場する — エイリアスを entities 配下のページで吸収する必要がある

## Updates

- 2026-05-17: 初回 ingest（次回分 2026/05/11 まで）
- 2026-05-17: Google Doc export から再取得し、先頭見出しが `2026/05/18（次回分）` に更新されていることを確認
- 2026-05-17: source 更新前に `raw/meeting_minutes.txt` を再取得する refresh protocol を追記
