---
name: weekly-log-2026-05-06
summary: "nishio/oss_weekly_reporter の週次ダンプ (2026-05-06 〜 2026-05-13) — Slack/GitHub の生ログ"
type: source
url: https://github.com/nishio/oss_weekly_reporter/tree/data/data/2026-05-06_to_2026-05-13/raw
sources:
  - init.txt
---

## What it is

[[nishio]] が運用する `oss_weekly_reporter` のデータブランチ。[[dd2030]] Slack の公開チャンネルと GitHub 上の Issue/PR を週単位で取り込んだ JSON 群。`data` ブランチに `data/YYYY-MM-DD_to_YYYY-MM-DD/raw/{github,slack}/*.json` の形で蓄積される。

参照 URL は週ごとに変わる。本ページが扱うのは **2026-05-06 〜 2026-05-13 の週**。

## What this particular week contains

[[kouchou-ai]] 本体の活動はこの週は **非常に薄い**：

- GitHub `digitaldemocracy2030/kouchou-ai`: **Dependabot の PR 2 本のみ** (#822, #823 — `next` を 16.2.x → 16.2.6 にバンプ、Next.js のセキュリティアドバイザリ一括対応)。人間が書いた PR / Issue / Discussion はゼロ
- Slack `#2_開発_広聴ai`: メッセージ 1 通（[[nishio]] が Karpathy 風 LLM Wiki を kouchou-ai に適用したい旨）

代わりに **周辺チャンネル** に新規コントリビュータが知っておくべきコンテキストが多い：

- **Slack ログ公開と CC-BY**（`0_全体お知らせ`, `7_雑談`）: 公開チャンネルログを `oss_weekly_reporter` で取り続けていた事実がリマインドされ、CC-BY での明示公開＋全体会で 1 週間の異議期間提案
- **Outline self-host + MCP 連携**（`1_outline_ドキュメント管理`, `7_雑談`）: [[kuboon]] が `dd2030-docs.kbn.one` を運用。`[[X]]` wikilink syntax は Outline 側のパーサがエスケープしてしまうため kuboon がパッチ予定
- **Discord 移行論争**（`7_雑談`）: [[ohki-shingo]] が「1500 人規模の Slack 参加者を失うリスク」を提起、[[nishio]] は並行運用を主張
- **法人化と新名称投票**（`0_全体お知らせ`）: 5/12–5/15 投票期間。`デジタル民主主義2030` はフラッグシップ名称として残る方針
- **[[polimoney]] 開発**: PR #248 で 岩永淳志ページ公開、Azure 障害（probe port 変更）対応
- **DD2030 website PR #212**: [[nishio]] が「広聴 AI 本」を独立プロジェクトとしてサイトに追加、[[ohki-shingo]] がマージ

## Why this matters for kouchou-ai devs

- このリポジトリで Slack に閉じた議論が起きた場合、`oss_weekly_reporter` から発掘できる
- 公開ログ＋ AI 検索の組み合わせが [[dd2030]] 全体の文書運用方針になりつつある（「覚えるのをやめて、AI が答えられる仕組みに賭ける」by nishio）

## Open Questions

- 本ダンプは公開チャンネルのみ。DM／プライベートチャンネルの議論は含まれない
- 一部チャンネル（`2_新しいプロジェクトの種`, `2_開発_cartographer`, `7_広聴ai読書会` ほか）は `ai_reports` 未統合 — backfill は有料のため翌週からフル取り込みに切り替え予定とのこと

## Updates

- 2026-05-17: 初回 ingest（init.txt 指定の週分）
