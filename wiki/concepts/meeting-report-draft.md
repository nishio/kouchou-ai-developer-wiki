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

- [[meeting-report-2026-06-01]] — ラベル品質仕切り直し、構造把握スタンス、open issue 全件棚卸し、PR #887 deploy false positive / runtime build risk、PR #883 撤回後の quickstart 再設計、Windows / local LLM route など
- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## 議題候補 (2026-06-08 定例)

- Dependabot alerts (`https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot`) を週次または定例前の確認対象として固定するか。公開 wiki には alert 詳細を転記せず、対応 issue / PR / 優先度判断だけ残す運用でよいか。
- デプロイ詳細は公開 wiki に書かず、Google Drive「広聴AI-Azureデモ環境」を一次置き場にする方針でよいか。アクセス権は大木・西尾・小野(moai)。

## 月曜にそのまま読む用 (2026-06-08 向け)

- 進行中: `public-viewer` の startup `next build` 撤去に向けて、PR #888 (`codex/public-viewer-build-serve-split`) で実装を進めた。dynamic hosting は API なしで `next build`、static export は fixture API ありで build する形に分離し、container 起動は `next start` のみにした。
  ローカルでは Jest 94 件、API-less dynamic build、static export build、runtime smoke (`/`, `/faq/`, `/example/`) が通過。PR #888 の CI `client build` でも API-less dynamic build、static export build、Docker build が通過した。
- wiki 運用: Dependabot alerts を GitHub current state の定期観測対象として `CLAUDE.md` / [[wiki-driven-workflow]] / [[codeql-introduction-context]] に追記した。main / open PR / issue だけでは拾えない security live state として扱い、公開 wiki には脆弱性詳細を転記しない方針にした。あわせて、デプロイ詳細は公開 wiki に書かず Google Drive「広聴AI-Azureデモ環境」側で管理する方針に更新した。
- main 済み: Dependabot alerts に対し、PR #889 (`codex/dependabot-alerts-2026-06-01`) を admin merge した。`pnpm.overrides` と `pnpm-lock.yaml` だけを更新し、audit / tests / build は通過。merge 後の Dependabot open alerts は 19 件から 6 件へ減った。alert 詳細は公開 PR / wiki に転記していない。

## 次回定例向け詳細 (テーマ別)

### public-viewer build/serve 分離

- 進行中 PR: #888 (`codex/public-viewer-build-serve-split`)。`apps/public-viewer/entrypoint.sh` から runtime build を消し、`Dockerfile` の builder stage で `.next` を作る構成に変更した。
- 実装判断: `/` と `/faq` は `connection()` で request-time rendering に寄せた。一方 `[slug]` に `connection()` を入れると `/example` が `DYNAMIC_SERVER_USAGE` で落ちたため、non-export では `generateStaticParams() => []` と fallback metadata、runtime env 読みで対応した。
- CodeRabbit review 対応: `/` の `generateMetadata()` は `connection()` で request-time 化し、API-less build を維持しつつ reporter-specific metadata を復元した。`[slug]` metadata の request-time 化は `/example` 500 を起こすため見送った。
- 次に見ること: Docker build を CI / daemon 起動済み環境で通すことと、別 PR で Azure deploy readiness poll / representative report smoke を入れること。

### security alert 運用

- Dependabot alerts は main / open PR / issue だけでは拾えない GitHub live state なので、security / dependency の保守では `https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot` を定期確認対象に含める。
- 公開 wiki には alert の具体的な脆弱性詳細を転記せず、対応 issue / PR / 優先度判断だけを残す。確認頻度と担当は次回定例で決めたい。

### public wiki の公開境界

- デプロイ詳細は公開 wiki に書かない。実環境 URL、resource 名・サイズ、revision / run details、ログ、具体手順、secret / access 周辺は Google Drive「広聴AI-Azureデモ環境」側で扱う。
- 公開 wiki に残すのは、設計判断・公開可能な課題・対応 issue / PR・次に見る論点の粒度にする。
- main 済み PR: #889 (`codex/dependabot-alerts-2026-06-01`)。open PR #888 / #863 は `package.json` / `pnpm-lock.yaml` を触っていなかったため、差分上の干渉は小さかった。

## Open Questions

- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-06-01: 2026-06-01 定例後に [[meeting-report-2026-06-01]] へ rotate し、本ページを 2026-06-08 向けの空テンプレートへ戻した
- 2026-06-01: Dependabot 脆弱性詳細とデプロイ詳細を公開 wiki に書かない方針を次回定例向け議題に追加
- 2026-05-31: 「議題候補」セクションを status 報告と分ける運用を追加。2026-06-01 定例で、developer-quickstart 再設計、組織内デモ役 / SaaS ホスト型、議題候補常設化を相談対象にした
- 2026-05-30: 月曜読み上げ用要約を冒頭に追加し、本文をテーマ別に束ね直した
- 2026-05-21: 初回作成。直近の `analysis-core` / Web UI / deploy / AI 運用ルールの進捗を次回定例向けに要約
