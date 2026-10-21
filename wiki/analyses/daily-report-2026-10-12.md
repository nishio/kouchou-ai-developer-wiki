---
title: "開発日報 2026-10-12"
type: analysis
summary: "2026-10-12 の作業まとめ。広聴AI open Issue 全105件の棚卸しを並列ワークフローで実施→現行 main@c297bc97 基準で分類。nishio 判断で4件 close(#573/#519/#417/#871)＋残件を#973へ切り出し。要件再確認14件を処理: #308/#213/#289 を対話で判断、残り11件(#104/#227/#255/#464/#471/#474/#517/#529/#577/#898/#921)を機械処理バッチで整理→6件に事実整理コメント投稿・5件は人間必須で方針待ち。#577 は close 相当と判定（同日 close）。さらに未解決53件を再検証し偽陰性2件(#953/#956=現行main a3c198e9で解決済み)を検出、残51件は前回判定妥当・close確定は#953/#956のみ。"
sources:
  - issue-audit-2026-10-12-full.md
  - issue-audit-2026-10-12-sweep.md
---

> 2026-10-12 の作業ログ。判定の正本は [[issue-backlog-audit-2026-10-12]]。

## 今日やったこと（概要）

1. 広聴AI の **open Issue 全105件を棚卸し**（並列ワークフロー）。現行 main `c297bc97` にコード照合して分類。
2. 解決済みのうち根拠が揃ったものを **nishio 判断で close**（自動 close は独立検証で0件→対話で個別判断）。計 **4件 close**、残件1件を **新 Issue [#973](https://github.com/digitaldemocracy2030/kouchou-ai/issues/973)** に切り出し。
3. 「要件再確認」14件を nishio と **1件ずつ判断**（進行中）。

## 1. 全105件の棚卸し結果

判定内訳（今回95件＋前回再利用10件）: **未解決53 / 一部解決34 / 要件再確認14 / 解決済3 / 不明1**。
詳細な一覧表・file:line 根拠は [[issue-backlog-audit-2026-10-12]]（＋根拠 source [[issue-audit-2026-10-12-full]]）。前回10件は [[issue-backlog-audit-2026-10-11]] を再利用。

## 2. close 実行（nishio 判断・2026-10-12）

| # | 題名 | 判断根拠 |
|---|---|---|
| [#573](https://github.com/digitaldemocracy2030/kouchou-ai/issues/573) | PLaMo-Embedding-1B の動作実験 | 実験完了・現行モデル優位＝交換不要。実験目的達成として close |
| [#519](https://github.com/digitaldemocracy2030/kouchou-ai/issues/519) | エネルギー庁パブコメ分析レポート公開 | データ生成完了・報告 Note 作成済み。成果物が揃ったとして close |
| [#417](https://github.com/digitaldemocracy2030/kouchou-ai/issues/417) | コードレビューの効率化 | 明示的完了条件なし。CodeRabbit 導入＋ガイドライン達成をもって目的達成 |
| [#871](https://github.com/digitaldemocracy2030/kouchou-ai/issues/871) | Azure deploy safety の Blob health check 切替 | 切替本体は完了。残件を [#973](https://github.com/digitaldemocracy2030/kouchou-ai/issues/973) へ切り出して close |

- **[#973](https://github.com/digitaldemocracy2030/kouchou-ai/issues/973)（新規・OPEN）**: [#871](https://github.com/digitaldemocracy2030/kouchou-ai/issues/871) の残件（`report_status.json`/artifact の read-back 確認＋「API scrape でなく Blob health check を基準にする理由」の docs 明記）。

## 3. 要件再確認14件の判断

### 判断済み

- **[#308](https://github.com/digitaldemocracy2030/kouchou-ai/issues/308) HTMLフォームで簡易デプロイ**: close せず **open 維持**。「やらない(wontfix)」ではなく **需要の裏取り＋配布戦略([#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)/[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921))の決定待ちでブロック** として整理（`wontfix`除去→`question`付与、評価と再検討条件をコメント）。
  - 評価: ①対象ズレ（Azure 取得は Docker より高ハードルで組織規約層に効かない）②レイヤーズレ（本音は「レポートが欲しい」＝ホスティング側）③認証情報フォーム入力リスク＋Function 密結合の維持コスト。加えて [#300](https://github.com/digitaldemocracy2030/kouchou-ai/issues/300) close・[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)/[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) の「クラウドを建てさせない」方向と逆行。
- **[#213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213) 「5→50」表記**: **案3（矢印をやめ、第1/第2階層の意見グループ数を方向を含意しない形で併記）に決定**。5→50 vs 50→5 の順序論争を解消。`good first issue` 再付与で実装募集可能に。実装は小（`Analysis.tsx:119` / `_op-image.tsx:265` の `→` 連結を併記へ）。過去議論（Slack 発端→認知順でママ主張→意見分裂で保留）を今回解消。
- **[#289](https://github.com/digitaldemocracy2030/kouchou-ai/issues/289) exe配布**: **open 維持・`wontfix` 除去**。nishio「exe は選択肢（署名なしでも実行可、組織ポリシーはまちまち）」を記録。2025 の「exe も install 不可では」懸念は、インストール不要のポータブル単一バイナリなら必ずしも当たらない、で整理。具体実装は **[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)**（Node runtime 依存除去）に集約、[#289](https://github.com/digitaldemocracy2030/kouchou-ai/issues/289) は一般版/親。

### 残り11件を機械処理（2026-10-12 バッチ）

残り11件（[#104](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104) [#227](https://github.com/digitaldemocracy2030/kouchou-ai/issues/227) [#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255) [#464](https://github.com/digitaldemocracy2030/kouchou-ai/issues/464) [#471](https://github.com/digitaldemocracy2030/kouchou-ai/issues/471) [#474](https://github.com/digitaldemocracy2030/kouchou-ai/issues/474) [#517](https://github.com/digitaldemocracy2030/kouchou-ai/issues/517) [#529](https://github.com/digitaldemocracy2030/kouchou-ai/issues/529) [#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577) [#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898) [#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921)）を現行 main `c297bc97` にコード照合し、機械でできる所まで詰めた。close 相当のものは、独立に反証を試みて再確認してから実行する運用。

**機械で決着＝事実整理コメントを投稿（6件）**。各 Issue に file:line 根拠付きの棚卸しコメントを残した（上流本文は編集せず追記のみ）。

| # | 投稿内容の要旨 |
|---|---|
| [#104](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104) | 実装済み GA4 は [#54](https://github.com/digitaldemocracy2030/kouchou-ai/issues/54) 由来の per-deployment 型（各運用者が自デプロイを解析）で、[#104](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104) が提案した「運用者横断の中央集約 visibility」とは別物。中央 telemetry 送信口・同意/オプトアウト UI は未実装。収集可否はプライバシー方針＝人間判断として open 維持 |
| [#227](https://github.com/digitaldemocracy2030/kouchou-ai/issues/227) | 設定ダイアログは再設計済み。構造面2点（見出し/説明の縦並び・濃いグループ設定のセクション分離）はコード反映済み、粒度の選択式化(2/5/10/25/50/100)は未実装で線形スライダーのまま |
| [#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255) | 技術的代替(Azure/Gemini/OpenRouter/local)は実装済みで [#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285) 追跡。本Issue固有の「政治利用FAQ」は未作成。公開規約の事実整理（OpenAI 許容例に「内部調査/世論調査要約」明記・MS CoC に世論分析禁止条項なし）をコメントで共有、FAQ化の判断は人間 |
| [#471](https://github.com/digitaldemocracy2030/kouchou-ai/issues/471) | 公式ベンチスクリプト・推奨スペック文書とも未作成。ローカルLLMは NVIDIA GPU＋VRAM8GB 前提で「自治体の普通PC」目標と不整合、NPU 未対応。問いの再定義（GPUサーバ→普通PC）はスコープ判断 |
| [#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577) | 評価対象（PR#567 のシルエット方式自動クラスタ数決定）が本番経路から撤去済み。既定は cube-root へ置換済（PR#832）、ベータ表記も無し＝計画は obsolete/superseded。**close 相当（2026-10-12 17:42 JST に close 済み）** |
| [#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898) | 修正方針（`NUMBA_CPU_NAME=generic` 固定＝JIT丸ごと無効化は回避）は PR#899 で main 反映済み。aarch64 実機での `import umap`/`Illegal instruction` 解消確認が残件 |

**人間必須＝コメントせず方針待ち（5件）**。機械で前進できる新事実がない or repo 外成果物依存のため、ノイズ回避で公開コメントは出さず内部ドラフトのみ。

- **[#464](https://github.com/digitaldemocracy2030/kouchou-ai/issues/464)** APIキー確保: 3案（キー確保/無料LLM/廃止）の選択と PO 確定・repo secret 設定は組織運用でコード検証不能。機構は key 欠落時 exit 0 の graceful degradation のため workflow success は確保の証拠にならない。
- **[#474](https://github.com/digitaldemocracy2030/kouchou-ai/issues/474)** bonsai検証: ゴール（採用検討か技術調査の記録のみか）が未定義。現行 main に実装0件、検証は外部メモ(tsuzumik wiki)に存在。目的の切り分けが人間判断。
- **[#517](https://github.com/digitaldemocracy2030/kouchou-ai/issues/517)** 募集役割の具体化: コミュニティ運営タスク。役割一覧はコメントで実質整理済み、残りはウェルカムMTGスライド(repo外)への反映＝運営判断。
- **[#529](https://github.com/digitaldemocracy2030/kouchou-ai/issues/529)** 説明画像の更新: 純粋なデザイン依頼。修正後画像がデザイナー未確定（本文「後日決定案を添付」のまま成果物なし）。
- **[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921)** ブラウザ版本流化: 意図的に開かれた未決の戦略議論 Issue。戦略会議(9月以降)の意思決定事項で機械的根拠では決着しない。

## 4. PR レビュー・merge（issue 棚卸しとは別系統）

- **PR [#969](https://github.com/digitaldemocracy2030/kouchou-ai/issues/969)（CI: Docker Hub 429 対策）を admin merge**（squash, merge commit `4faaf256`）。Copilot bot 作成。client-build（public-viewer）のベースイメージ `node:22-alpine` 取得が Docker Hub の匿名 pull レート制限（HTTP 429）で落ちる件に、**ECR Public へのフォールバック**で対処（1回目 Docker Hub→失敗で待機付き ECR Public 再試行、`ARG REGISTRY=""` で後方互換）。CI 全 green を確認して反映。
- 評価: 有効な火消しだが**対症療法**。根本は認証 pull（匿名制限の回避）。ECR Public も匿名制限あり。対象も client-build のみで、`apps/admin` / `apps/static-site-builder` の Dockerfile と `azure-deploy.yml` / `api-docker-dependency-smoke.yml` が未対応（`work/kouchou-ai`@`c297bc97` で grep 確認）。
- **残件は Issue [#974](https://github.com/digitaldemocracy2030/kouchou-ai/issues/974) に切り出し**: ①認証 pull の恒久化 ②他ビルドへの横展開 ③リトライ設計の見直し。

### 当日の open PR 一斉処理（計 10 件 merge）

当初 open 12 件を順にレビューし、以下 **10 件を admin squash merge**（CI green 確認後）。残りは Draft の [#891](https://github.com/digitaldemocracy2030/kouchou-ai/issues/891) のみ。

- **小粒・低リスク（diff + main 照合レビュー）**: [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955)（CLI `report_dir` 未定義エラー・回帰テスト付き）/ [#965](https://github.com/digitaldemocracy2030/kouchou-ai/issues/965)（抽出プロンプト例「すべき」→「必要がある」）/ [#967](https://github.com/digitaldemocracy2030/kouchou-ai/issues/967)（抽出プロンプト実測調整例を docs 追加）/ [#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957)（setup `.env` 3キー欠落 + `check_setup_env.py` CI ガード）。
- **外部 PR**: [#968](https://github.com/digitaldemocracy2030/kouchou-ai/issues/968)（shingo-ohki、[#966](https://github.com/digitaldemocracy2030/kouchou-ai/issues/966) 英語化で切れた README 直リンクを日本語デフォルト復帰で当座復旧）。root cause（README 見出し直リンク依存）は **Issue [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)** へ。
- **規模大（4 本を並行して独立にレビュー・全件 correctness 問題なし）**: [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)（Biome lint 0化 + CI gate、`Reflect.deleteProperty` 等価）/ [#961](https://github.com/digitaldemocracy2030/kouchou-ai/issues/961)（全画面クラスタ粒度切替、`resolveChartModes()` 等価）/ [#946](https://github.com/digitaldemocracy2030/kouchou-ai/issues/946)（濃いクラスタ初期値保存、1ヶ月前 PR だが main 乖離なし実測）/ [#970](https://github.com/digitaldemocracy2030/kouchou-ai/issues/970)（AGPL 訂正 + report.html ライセンス同梱）。
- **[#970](https://github.com/digitaldemocracy2030/kouchou-ai/issues/970) は README 競合あり**: [#968](https://github.com/digitaldemocracy2030/kouchou-ai/issues/968) の再編と衝突 → 競合を解消（README.ja.md 削除・日本語行を README.md・英語行を README.en.md）して merge。F1（ライセンス資源欠如時の hard-fail）は **Issue [#978](https://github.com/digitaldemocracy2030/kouchou-ai/issues/978)**（link-only degrade）へ。
- 詳細な時系列は wiki の作業履歴（`wiki/log.txt` の 2026-10-12 の filing-back 群）、定例向けのまとめは [[meeting-report-2026-10-10]]。

## Open Questions / 次の一手

- **[#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577) の close**: 評価対象が本番から撤去済みで close 相当（反証検証済み）。2026-10-12 17:42 JST に close 済みで、解消。
- **[#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898) の aarch64 実機確認**: `generic` 固定は main 反映済み。Apple Silicon 等で `docker compose up --build`→レポート生成完走まで確認できれば close 可。できなければ pending validation で残す。
- **方針・スコープ決定を会議に**: [#104](https://github.com/digitaldemocracy2030/kouchou-ai/issues/104)(集約 visibility のプライバシー方針) / [#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255)(政治利用FAQ の明文化・法務確認) / [#471](https://github.com/digitaldemocracy2030/kouchou-ai/issues/471)(推奨スペックのスコープ再定義) / [#464](https://github.com/digitaldemocracy2030/kouchou-ai/issues/464)(APIキー PO 確定) / [#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921)(ブラウザ版本流化・戦略会議) / [#474](https://github.com/digitaldemocracy2030/kouchou-ai/issues/474)(bonsai のゴール定義)。
- **repo 外成果物待ち**: [#517](https://github.com/digitaldemocracy2030/kouchou-ai/issues/517)(ウェルカムMTGスライド反映) / [#529](https://github.com/digitaldemocracy2030/kouchou-ai/issues/529)(デザイナーの修正後画像)。
- [#213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213) の併記デザインの具体（design と調整）。
- [#519](https://github.com/digitaldemocracy2030/kouchou-ai/issues/519) の公開 URL が確定したら Issue に追記。

## 5. 未解決53件の潰し込み（再検証）

棚卸しで「未解決」とした53件を、9 つに分けて独立に現行 main と file:line で再照合し、偽陰性（実は解決済み）を洗い直した。基準は固定 checkout `c297bc97`（観測日 2026-10-12）だが、now-resolved 2件は固定版が本日マージの修正より古かっただけで、**現行 remote main `a3c198e9`** では解決済みと確認。根拠 source は [[issue-audit-2026-10-12-sweep]]。

**内訳（53件）**: still-unresolved **44** / human-required **7** / now-resolved **2** / partial **0** / duplicate **0**。

→ 偽陰性は 2件（[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) [#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956)）のみ。残り51件は前回判定（未解決 or 人間必須）が妥当と再確認、偽陰性なし。

### close 確定（偽陰性＝現行 main で解決済み）

| # | 題名 | 根拠（現行 main `a3c198e9`） |
|---|---|---|
| [#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) | CLI の HTML 出力で可視化が `report_dir` 未定義で失敗 | PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955)（merge `a4028c7e`）が `hierarchical_default.py:98-106` から `${config.report_dir}` 参照を削除、`hierarchical_visualization.py:53-56` は `ctx.output_dir` 使用、回帰テスト `test_pipeline_paths_integration.py:474-525` 追加。固定 checkout `c297bc97` はこの merge 前の版。 |
| [#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956) | セットアップ生成 .env に必須環境変数が欠落し静的版DL/キャッシュ更新が失敗 | PR [#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957)（merge = 現 HEAD `a3c198e9`）が `setup_linux.sh` / `setup_mac.sh` / `setup_win.ps1` 3スクリプト全てに `CLIENT_STATIC_BUILD_BASEPATH` / `REVALIDATE_SECRET` / `REVALIDATE_URL` を追加＋CI検出(`scripts/check_setup_env.py` ほか)。.env.example 丸コピー方式は不採用。 |

※ 2 件とも 2026-10-12 17:55 JST に close 済み。

### partial / duplicate 再分類で注目すべきもの

今回の再分類で partial・duplicate カテゴリへ移したものは**0件**（still-unresolved は中核要件が未充足のため格下げせず）。ただし上流更新時に「隣接要件が既に解決済み」と注記すべきものがある:

- **[#366](https://github.com/digitaldemocracy2030/kouchou-ai/issues/366) 複数の公開リスト**: 中核（リストを複数作成しレポート登録）は未実装で未解決のまま。ただし隣接の**限定公開/unlisted は `ReportVisibility` enum＋PR [#500](https://github.com/digitaldemocracy2030/kouchou-ai/issues/500)(MERGED) で実装済み**。別利用経路なので混同しないが、上流更新案に「限定公開は別要件として解決済み」と注記すべき。
- **[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) / [#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956)**: still-unresolved と見えていたのは固定 checkout が本日マージより古かっただけの偽陰性。now-resolved に是正。
- **[#507](https://github.com/digitaldemocracy2030/kouchou-ai/issues/507) 互換コード削除**: 互換コードは**意図的に残存中**。削除は `ver2.0→ver3.0` という未到来マイルストーン待ちで、現時点では着手不可（未解決だが前進不能）。
- **[#869](https://github.com/digitaldemocracy2030/kouchou-ai/issues/869) label refinement 残作業整理**: トラッキング issue。前提 PR [#866](https://github.com/digitaldemocracy2030/kouchou-ai/issues/866)/[#867](https://github.com/digitaldemocracy2030/kouchou-ai/issues/867)/[#868](https://github.com/digitaldemocracy2030/kouchou-ai/issues/868) は merged だが label refinement 本体は未 merge。merge 済み前提 PR との混同に注意。
- **[#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954) CLI の report_url_pattern / report_html_title**: [#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) の PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955) は 954 を**未カバー**（`orchestration.py` の `valid_fields`・specs 未変更）。設定仕様(案A/案B)の決定が残り未解決。

### 修正が in-flight（OPEN 未 merge PR あり）

実装着手済みで merge 待ちのため「未解決」だが、close は PR merge 次第: **[#960](https://github.com/digitaldemocracy2030/kouchou-ai/issues/960)**(PR [#961](https://github.com/digitaldemocracy2030/kouchou-ai/issues/961)) / **[#962](https://github.com/digitaldemocracy2030/kouchou-ai/issues/962)**(PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)) / **[#964](https://github.com/digitaldemocracy2030/kouchou-ai/issues/964)**(PR [#965](https://github.com/digitaldemocracy2030/kouchou-ai/issues/965), docs [#967](https://github.com/digitaldemocracy2030/kouchou-ai/issues/967)) / **[#971](https://github.com/digitaldemocracy2030/kouchou-ai/issues/971)**(PR [#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975)) / **[#972](https://github.com/digitaldemocracy2030/kouchou-ai/issues/972)**(PR [#976](https://github.com/digitaldemocracy2030/kouchou-ai/issues/976))。

### human-required 7件（実 API 課金・外部成果物・組織判断が必須）

[#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324)(ファクトチェック実験) / [#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346)(大量投稿対処の実験) / [#556](https://github.com/digitaldemocracy2030/kouchou-ai/issues/556)(アクセシビリティ継続デザイン) / [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564)(活用事例の渉外収集) / [#882](https://github.com/digitaldemocracy2030/kouchou-ai/issues/882)(KJ法プロンプト比較実験) / [#912](https://github.com/digitaldemocracy2030/kouchou-ai/issues/912)(GPT-5.6 実 API 検証) / [#913](https://github.com/digitaldemocracy2030/kouchou-ai/issues/913)(Gemini 3.8/3.5 実 API 検証)。いずれも現行 main のコード状態では充足されない種類（偽陰性ではない）。

## Updates

- 2026-10-21: 確定版とした。[#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577) は 2026-10-12 17:42 JST に、[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) / [#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956) は同日 17:55 JST に close 済みで、Open Questions の [#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577) の項はこのページの最終編集より前に解消していた（本文もそれに合わせた）。時系列の参照先を、7 日分だけを残す log.md から log.txt に変えた
