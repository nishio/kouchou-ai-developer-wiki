---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。会議ごとに過去回を snapshot として archive へ rotate し、本ページは次回向けの差分のみ積み上げる"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業を短時間で報告するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「全部の変更履歴」を書くことではなく、**会議で口頭共有したい判断と進み具合だけを残す** こと。詳しい根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- まず冒頭の「月曜にそのまま読む用」を 8 項目以内に保つ。詳細は下のテーマ別セクションへ送る
- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連 analysis / source ページへ送る
- 同じテーマで新しい情報が来たら、新しい bullet を足すのではなく既存セクションを書き換える
- **「議題候補」セクション** は team の判断・議論・合意が必要な論点を集める場所。status 報告 (「月曜にそのまま読む用」) とは別物として扱う
- 会議が終わったら本ページを `wiki/concepts/meeting-report-YYYY-MM-DD.md` へ rotate し、本ページは次回向けに空に戻す

## 過去回

- [[meeting-report-2026-06-01]] — ラベル品質仕切り直し、構造把握スタンス、open issue 全件棚卸し、PR #887 deploy false positive / OOM、PR #883 撤回後の quickstart 再設計、Windows / local LLM route など
- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## 議題候補 (2026-06-08 定例)

(追加予定)

## 月曜にそのまま読む用 (2026-06-08 向け)

(追加予定)

## 次回定例向け詳細 (テーマ別)

(追加予定)

## Open Questions

- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-06-01: 2026-06-01 定例後に [[meeting-report-2026-06-01]] へ rotate し、本ページを 2026-06-08 向けの空テンプレートへ戻した
- 2026-05-31: 「議題候補」セクションを status 報告と分ける運用を追加。2026-06-01 定例で、developer-quickstart 再設計、組織内デモ役 / SaaS ホスト型、議題候補常設化を相談対象にした
- 2026-05-30: 月曜読み上げ用要約を冒頭に追加し、本文をテーマ別に束ね直した
- 2026-05-21: 初回作成。直近の `analysis-core` / Web UI / deploy / AI 運用ルールの進捗を次回定例向けに要約
