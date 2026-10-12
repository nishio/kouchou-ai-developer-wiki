---
type: analysis
summary: "2026-10-12 の作業まとめ（draft・後で nishio が1ページに仕上げる）。広聴AI open Issue 全105件の棚卸しを並列ワークフローで実施→現行 main@c297bc97 基準で分類。nishio 判断で4件 close(#573/#519/#417/#871)＋残件を#973へ切り出し。要件再確認14件を対話で処理中: #308=blocked整理(wontfix除去/question付与, open維持)、#213=案3(矢印廃止・方向非含意の併記)決定で good first issue 再募集。"
sources:
  - issue-audit-2026-10-12-full.md
---

> **draft**: 2026-10-12 の作業ログ。後で nishio が1ページにまとめ直す前提の下書き。判定の正本は [[issue-backlog-audit-2026-10-12]]、各 Issue の更新案・close ログ・判断ログは private キュー `drafts/issue-audit/2026-10-12-full/`。

## 今日やったこと（概要）

1. 広聴AI の **open Issue 全105件を棚卸し**（並列ワークフロー）。現行 main `c297bc97` にコード照合して分類。
2. 解決済みのうち根拠が揃ったものを **nishio 判断で close**（自動 close は独立検証で0件→対話で個別判断）。計 **4件 close**、残件1件を **新 Issue #973** に切り出し。
3. 「要件再確認」14件を nishio と **1件ずつ判断**（進行中）。

## 1. 全105件の棚卸し結果

判定内訳（今回95件＋前回再利用10件）: **未解決53 / 一部解決34 / 要件再確認14 / 解決済3 / 不明1**。
詳細な一覧表・file:line 根拠は [[issue-backlog-audit-2026-10-12]]（＋根拠 source [[issue-audit-2026-10-12-full]]）。前回10件は [[issue-backlog-audit-2026-10-11]] を再利用。

## 2. close 実行（nishio 判断・2026-10-12）

| # | 題名 | 判断根拠 |
|---|---|---|
| #573 | PLaMo-Embedding-1B の動作実験 | 実験完了・現行モデル優位＝交換不要。実験目的達成として close |
| #519 | エネルギー庁パブコメ分析レポート公開 | データ生成完了・報告 Note 作成済み。成果物が揃ったとして close |
| #417 | コードレビューの効率化 | 明示的完了条件なし。CodeRabbit 導入＋ガイドライン達成をもって目的達成 |
| #871 | Azure deploy safety の Blob health check 切替 | 切替本体は完了。残件を #973 へ切り出して close |

- **#973（新規・OPEN）**: #871 の残件（`report_status.json`/artifact の read-back 確認＋「API scrape でなく Blob health check を基準にする理由」の docs 明記）。

## 3. 要件再確認14件の判断

### 判断済み

- **#308 HTMLフォームで簡易デプロイ**: close せず **open 維持**。「やらない(wontfix)」ではなく **需要の裏取り＋配布戦略(#885/#921)の決定待ちでブロック** として整理（`wontfix`除去→`question`付与、評価と再検討条件をコメント）。
  - 評価: ①対象ズレ（Azure 取得は Docker より高ハードルで組織規約層に効かない）②レイヤーズレ（本音は「レポートが欲しい」＝ホスティング側）③認証情報フォーム入力リスク＋Function 密結合の維持コスト。加えて #300 close・#885/#921 の「クラウドを建てさせない」方向と逆行。
- **#213 「5→50」表記**: **案3（矢印をやめ、第1/第2階層の意見グループ数を方向を含意しない形で併記）に決定**。5→50 vs 50→5 の順序論争を解消。`good first issue` 再付与で実装募集可能に。実装は小（`Analysis.tsx:119` / `_op-image.tsx:265` の `→` 連結を併記へ）。過去議論（Slack 発端→認知順でママ主張→意見分裂で保留）を今回解消。
- **#289 exe配布**: **open 維持・`wontfix` 除去**。nishio「exe は選択肢（署名なしでも実行可、組織ポリシーはまちまち）」を記録。2025 の「exe も install 不可では」懸念は、インストール不要のポータブル単一バイナリなら必ずしも当たらない、で整理。具体実装は **#885**（Node runtime 依存除去）に集約、#289 は一般版/親。

### 未着手（残り）

- 確認1つで片付く系: #898(Apple Silicon実機) / #227(新UI実表示) / #577(silhouette→cube-root置換合意) / #474(bonsai目的) / #517(スライド反映) / #529(デザイン更新案待ち)
- 方針・スコープ決定系: #104(利用把握のプライバシー方針) / #255(Azure政治利用FAQ) / #471(推奨スペックのスコープ) / #464(APIキー・PO待ち) / #921(ブラウザ版本流化・戦略会議)

## 4. PR レビュー・merge（issue 棚卸しとは別系統）

- **PR #969（CI: Docker Hub 429 対策）を admin merge**（squash, merge commit `4faaf256`）。Copilot bot 作成。client-build（public-viewer）のベースイメージ `node:22-alpine` 取得が Docker Hub の匿名 pull レート制限（HTTP 429）で落ちる件に、**ECR Public へのフォールバック**で対処（1回目 Docker Hub→失敗で待機付き ECR Public 再試行、`ARG REGISTRY=""` で後方互換）。CI 全 green を確認して反映。
- 評価: 有効な火消しだが**対症療法**。根本は認証 pull（匿名制限の回避）。ECR Public も匿名制限あり。対象も client-build のみで、`apps/admin` / `apps/static-site-builder` の Dockerfile と `azure-deploy.yml` / `api-docker-dependency-smoke.yml` が未対応（`work/kouchou-ai`@`c297bc97` で grep 確認）。
- **残件は Issue #974 に切り出し**: ①認証 pull の恒久化 ②他ビルドへの横展開 ③リトライ設計の見直し。
- 当日の他 open PR（全12件）は CI ほぼ green・レビュー承認待ちで BLOCKED。#891 のみ Draft。

## Open Questions / 次の一手

- 残り「未着手」10件の処理方針（実機確認で閉じる系を先に潰すか、方針決定系を会議に回すか）。
- #213 の併記デザインの具体（design と調整）。
- #519 の公開 URL が確定したら Issue に追記。
