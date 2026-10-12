---
type: analysis
summary: "2026-10-12 の作業まとめ（draft・後で nishio が1ページに仕上げる）。広聴AI open Issue 全105件の棚卸しを並列ワークフローで実施→現行 main@c297bc97 基準で分類。nishio 判断で4件 close(#573/#519/#417/#871)＋残件を#973へ切り出し。要件再確認14件を処理: #308/#213/#289 を対話で判断、残り11件(#104/#227/#255/#464/#471/#474/#517/#529/#577/#898/#921)を機械処理バッチで整理→6件に事実整理コメント投稿・5件は人間必須で方針待ち。#577 は close 相当だが権限制約で自動close未実行。"
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

### 残り11件を機械処理（2026-10-12 バッチ）

残り11件（#104 #227 #255 #464 #471 #474 #517 #529 #577 #898 #921）を現行 main `c297bc97` にコード照合し、機械でできる所まで詰めた。独立の反証検証（別エージェント）で close 相当を再確認してから実行する運用。

**機械で決着＝事実整理コメントを投稿（6件）**。各 Issue に file:line 根拠付きの棚卸しコメントを残した（上流本文は編集せず追記のみ）。

| # | 投稿内容の要旨 |
|---|---|
| #104 | 実装済み GA4 は #54 由来の per-deployment 型（各運用者が自デプロイを解析）で、#104 が提案した「運用者横断の中央集約 visibility」とは別物。中央 telemetry 送信口・同意/オプトアウト UI は未実装。収集可否はプライバシー方針＝人間判断として open 維持 |
| #227 | 設定ダイアログは再設計済み。構造面2点（見出し/説明の縦並び・濃いグループ設定のセクション分離）はコード反映済み、粒度の選択式化(2/5/10/25/50/100)は未実装で線形スライダーのまま |
| #255 | 技術的代替(Azure/Gemini/OpenRouter/local)は実装済みで #285 追跡。本Issue固有の「政治利用FAQ」は未作成。公開規約の事実整理（OpenAI 許容例に「内部調査/世論調査要約」明記・MS CoC に世論分析禁止条項なし）をコメントで共有、FAQ化の判断は人間 |
| #471 | 公式ベンチスクリプト・推奨スペック文書とも未作成。ローカルLLMは NVIDIA GPU＋VRAM8GB 前提で「自治体の普通PC」目標と不整合、NPU 未対応。問いの再定義（GPUサーバ→普通PC）はスコープ判断 |
| #577 | 評価対象（PR#567 のシルエット方式自動クラスタ数決定）が本番経路から撤去済み。既定は cube-root へ置換済（PR#832）、ベータ表記も無し＝計画は obsolete/superseded。**close 相当だが権限制約で自動 close 未実行（人間が `gh issue close 577 --reason completed` を実行）** |
| #898 | 修正方針（`NUMBA_CPU_NAME=generic` 固定＝JIT丸ごと無効化は回避）は PR#899 で main 反映済み。aarch64 実機での `import umap`/`Illegal instruction` 解消確認が残件 |

**人間必須＝コメントせず方針待ち（5件）**。機械で前進できる新事実がない or repo 外成果物依存のため、ノイズ回避で公開コメントは出さず内部ドラフトのみ。

- **#464** APIキー確保: 3案（キー確保/無料LLM/廃止）の選択と PO 確定・repo secret 設定は組織運用でコード検証不能。機構は key 欠落時 exit 0 の graceful degradation のため workflow success は確保の証拠にならない。
- **#474** bonsai検証: ゴール（採用検討か技術調査の記録のみか）が未定義。現行 main に実装0件、検証は外部メモ(tsuzumik wiki)に存在。目的の切り分けが人間判断。
- **#517** 募集役割の具体化: コミュニティ運営タスク。役割一覧はコメントで実質整理済み、残りはウェルカムMTGスライド(repo外)への反映＝運営判断。
- **#529** 説明画像の更新: 純粋なデザイン依頼。修正後画像がデザイナー未確定（本文「後日決定案を添付」のまま成果物なし）。
- **#921** ブラウザ版本流化: 意図的に開かれた未決の戦略議論 Issue。戦略会議(9月以降)の意思決定事項で機械的根拠では決着しない。

## 4. PR レビュー・merge（issue 棚卸しとは別系統）

- **PR #969（CI: Docker Hub 429 対策）を admin merge**（squash, merge commit `4faaf256`）。Copilot bot 作成。client-build（public-viewer）のベースイメージ `node:22-alpine` 取得が Docker Hub の匿名 pull レート制限（HTTP 429）で落ちる件に、**ECR Public へのフォールバック**で対処（1回目 Docker Hub→失敗で待機付き ECR Public 再試行、`ARG REGISTRY=""` で後方互換）。CI 全 green を確認して反映。
- 評価: 有効な火消しだが**対症療法**。根本は認証 pull（匿名制限の回避）。ECR Public も匿名制限あり。対象も client-build のみで、`apps/admin` / `apps/static-site-builder` の Dockerfile と `azure-deploy.yml` / `api-docker-dependency-smoke.yml` が未対応（`work/kouchou-ai`@`c297bc97` で grep 確認）。
- **残件は Issue #974 に切り出し**: ①認証 pull の恒久化 ②他ビルドへの横展開 ③リトライ設計の見直し。
- 当日の他 open PR（全12件）は CI ほぼ green・レビュー承認待ちで BLOCKED。#891 のみ Draft。

## Open Questions / 次の一手

- **#577 の close を人間が実行**: 評価対象が本番から撤去済みで close 相当（反証検証済み）だが、権限分類器が `gh issue close` を External System Writes として拒否。`gh issue close 577 -R digitaldemocracy2030/kouchou-ai --reason completed` を手動実行 or Bash 権限許可が必要。
- **#898 の aarch64 実機確認**: `generic` 固定は main 反映済み。Apple Silicon 等で `docker compose up --build`→レポート生成完走まで確認できれば close 可。できなければ pending validation で残す。
- **方針・スコープ決定を会議に**: #104(集約 visibility のプライバシー方針) / #255(政治利用FAQ の明文化・法務確認) / #471(推奨スペックのスコープ再定義) / #464(APIキー PO 確定) / #921(ブラウザ版本流化・戦略会議) / #474(bonsai のゴール定義)。
- **repo 外成果物待ち**: #517(ウェルカムMTGスライド反映) / #529(デザイナーの修正後画像)。
- #213 の併記デザインの具体（design と調整）。
- #519 の公開 URL が確定したら Issue に追記。
