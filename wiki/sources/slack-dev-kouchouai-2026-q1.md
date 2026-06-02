---
name: slack-dev-kouchouai-2026-q1
summary: "`oss_weekly_reporter` の `#2_開発_広聴ai` 抜粋（2026-01-14 〜 2026-03-04）— plugin 化、再利用、LLM grouping 系分類の設計意図"
type: source
url: https://github.com/nishio/oss_weekly_reporter/tree/data/data
last_read: 2026-05-17
coverage: "2026-01-14〜2026-03-04 のうち設計意図が濃い 6 週"
sources:
  - init.txt
  - nishio-source-freshness-criterion-2026-06-02.md
---

## What it is

`work/oss_weekly_reporter` の `data` ブランチにある Slack 公開ログ `#2_開発_広聴ai` を、設計意図の濃い週だけ `raw/oss_weekly_reporter/2026-q1-dev-kouchou-ai/` にコピーした source。対象は以下の 6 週：

- `2026-01-14_to_2026-01-21.json`
- `2026-01-21_to_2026-01-28.json`
- `2026-01-28_to_2026-02-04.json`
- `2026-02-04_to_2026-02-11.json`
- `2026-02-11_to_2026-02-18.json`
- `2026-02-25_to_2026-03-04.json`

2026-05 まで新しい週から広めに遡って grep したところ、**実装報告ではなく「なぜその機能が必要か」を濃く語っているのは主に 2026-Q1** だったため、この帯を一次参照として保持する。

## Freshness marker

この source の鮮度基準は、**2026-05-17 に `oss_weekly_reporter` の `#2_開発_広聴ai` を 2026-05 から遡読し、2026 Q1 の対象 6 週を `raw/oss_weekly_reporter/2026-q1-dev-kouchou-ai/` に固定した時点**。2026-03-04 より後の Slack を含む現在進行形の判断には、この page 単体ではなく後続 source か live state の再確認が必要。[[nishio-source-freshness-criterion-2026-06-02]]より

## Refresh protocol

1. `work/oss_weekly_reporter/` を `git fetch origin data:data && git switch data` で最新化
2. `find data -path '*/raw/slack/2_開発_広聴ai.json' | sort -r` で対象週を確認
3. 必要に応じて `rg` で論点を絞る
4. 設計意図の濃い週だけ `raw/oss_weekly_reporter/...` にコピーして、当ページと関連 Wiki を更新

`weekly-log-2026-05-06` は「特定週の薄い観測」だが、このページは **チャンネル横断ではなく `#2_開発_広聴ai` の時系列設計メモ** を扱う。

## Coverage by topic

- **分析 plugin と再利用機能の関係**: 分析手法を差し替えて比較するには、同じ入力・`extraction`・`embedding` を再利用したいという要求が先にある
- **LLM grouping 系 LLM 分類の導入経路**: まずは `extraction, embedding` の後ろで LLM クラスタリングに分岐し、既存のパイプライン／可視化との両立を優先する
- **分類ツリーをパラメータで与える発想**: 既存のカテゴリーツリーや自治体の予算カテゴリに合わせた分類を LLM 分類の亜種として扱える
- **可視化を分析から切り離す理由**: LLM grouping 分析は散布図を自然には出せないため、管理者が可視化方式を選べる必要がある
- **plugin 化の UX 目標**: エンジニアが plugin を差し込み、非エンジニアは管理画面から使える状態を理想とする

この source からの要点整理は [[slack-design-intents-2026-q1]]。

前史にあたる 2025 4Q は [[slack-dev-kouchouai-2025-q4]]。

## Open Questions

- `raw/` に保存したのは設計判断が濃い週のみ。実装の細かい経緯や UI 修正まで完全保存しているわけではない
- 公開 Slack ログ由来なので、DM や private channel の議論は含まれない

## Updates

- 2026-05-17: `oss_weekly_reporter` の `#2_開発_広聴ai` を 2026-05 から遡読し、設計意図の濃い 2026-Q1 6 週分を `raw/` に取り込み
- 2026-06-02: source の鮮度基準として `last_read` / `coverage` と Freshness marker を明示
