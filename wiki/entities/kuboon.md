---
title: "Ohkubo KOHEI(Outline 運用・ドキュメント基盤)"
name: kuboon
summary: "Ohkubo KOHEI — Outline self-host とドキュメント基盤運用"
type: entity
sources:
  - weekly-log-2026-05-06.md
  - meeting-minutes.md
---

## Who

**kuboon (Ohkubo KOHEI, 大久保)**。[[dd2030]] のドキュメント基盤・website 周りを担当。2025-06-18 に website 書き込み権限を取得。

## 主な活動

- **Outline self-host** — `dd2030-docs.kbn.one` を自宅サーバで運用。2026-05 時点では、`docs.dd2030.org` への DNS 統合と S3 バックアップを計画していた（2026-10-21 時点で `docs.dd2030.org` は名前解決できない）
- **MCP / dd-bot 統合** — Outline MCP server や Slack `/outline` スラッシュコマンドを実装
- **Outline の `[[X]]` wikilink エスケープ問題** を発見し、2026-05 時点でソース修正を予定していた（[[weekly-log-2026-05-06]]）。その後の状況は未確認（2026-10 時点で `kuboon/outline` フォークの main にある独自コミット 9 件に、該当する変更は見当たらない）
- **DD2030 website の Deno Lume 化** — `dd2030.org/newcomer` ページの移行など

## kouchou-ai 直接の貢献

kouchou-ai 本体への code commit よりも、**周辺のドキュメント／ツール基盤** を整備する役。MCP 連携やドキュメント自動化のノウハウは本 Wiki のような実験にも波及する。

## Updates

- 2026-05-17: 初回作成
- 2026-10-21: Outline の運用計画と wikilink エスケープ修正の記述に 2026-05 時点と日付を付け、その後の状況を追記
