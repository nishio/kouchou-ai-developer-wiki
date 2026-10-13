---
title: "未解決53件の再検証(偽陰性洗い出し) 2026-10-12"
type: source
summary: "広聴AI の棚卸しで『未解決』とした53件を 2026-10-12 に9シャード並列で再検証（偽陰性洗い出し）した一次記録。固定 checkout c297bc97 基準。結果は still-unresolved 44 / human-required 7 / now-resolved 2。偽陰性は #953/#956 の2件のみ（現行 remote main a3c198e9 で解決済み）。判定まとめは [[daily-report-2026-10-12]]。"
last_checked: 2026-10-12 JST
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues
  - issue-audit-2026-10-12-full.md
  - issue-backlog-audit-2026-10-12.md
---

## What it is

digitaldemocracy2030/kouchou-ai の open Issue 棚卸し（[[issue-backlog-audit-2026-10-12]]）で **still-unresolved とした53件**を、別エージェント9シャードで現行 main に file:line 再照合し、**偽陰性（実は解決済み）を洗い直した再検証**の一次記録。公開 Issue への close/comment はこの記録ステップでは行わず、内部記録のみ（close はメインが別途実行）。

結論: 偽陰性は **2件（[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) [#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956)）**。残り51件は前回の「未解決 / 人間必須」判定が妥当と再確認した。

## Freshness marker

- 観測日: **2026-10-12**。
- 基準コード（固定 checkout）: `work/kouchou-ai` の main `c297bc97bb2bbce42964a90d7501c2d3592aeaf0`。commit 固定リンクは `https://github.com/digitaldemocracy2030/kouchou-ai/blob/c297bc97bb2bbce42964a90d7501c2d3592aeaf0/<path>#L<line>`。
- **現行 remote main**: `a3c198e9`（本日 2026-10-12 08:54–08:55Z に PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955) / [#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957) がマージされた後の HEAD）。now-resolved 2件は、固定 checkout がこのマージより古かっただけの偽陰性で、`a3c198e9` では解決済みを確認。
- 生データ（Issue 1件 = 1 JSON、シャード毎判定 = `results.json`）は `raw/issue-audit/2026-10-12-sweep/shard-0 … shard-8/` に固定（`raw/` は gitignored な local/private 一次置き場）。
- 再検証した53件の Issue 番号: 11, 44, 56, 60, 79, 121, 170, 172, 173, 186, 190, 236, 250, 266, 293, 323, 324, 337, 339, 342, 345, 346, 366, 445, 454, 470, 493, 503, 507, 513, 548, 556, 564, 576, 638, 641, 643, 648, 679, 869, 879, 880, 882, 912, 913, 953, 954, 956, 960, 962, 964, 971, 972。

## 内訳（53件）

| newVerdict | 件数 |
|---|---|
| still-unresolved | 44 |
| human-required | 7 |
| now-resolved（偽陰性＝close 確定） | 2 |
| partial | 0 |
| duplicate | 0 |

全件 `confidence: high`。partial/duplicate への格下げは0件（still-unresolved は中核要件が未充足のため据え置き）。

## now-resolved（偽陰性・close 確定）

- **[#953](https://github.com/digitaldemocracy2030/kouchou-ai/issues/953) CLI の HTML 出力で可視化が `report_dir` 未定義で失敗**: PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955)（merge `a4028c7e`、2026-10-12T08:54Z、`a3c198e9` の祖先）が `workflows/hierarchical_default.py:98-106` の可視化 step から `config={'report_dir': ...}` を削除、`plugins/builtin/hierarchical_visualization.py:53-56` は `ctx.output_dir / "report.html"` を使用、回帰テスト `tests/test_pipeline_paths_integration.py:474-525`（`test_only_visualization_writes_report_without_report_dir`）追加。固定 checkout `c297bc97` は本 merge 前の版。
- **[#956](https://github.com/digitaldemocracy2030/kouchou-ai/issues/956) セットアップ生成 .env に必須環境変数が欠落**: PR [#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957)（merge = 現 HEAD `a3c198e9`、2026-10-12T08:55Z）が `setup_linux.sh:17-19` / `setup_mac.sh:28-30` / `setup_win.ps1:187-189` の3スクリプト全てに `CLIENT_STATIC_BUILD_BASEPATH` / `REVALIDATE_SECRET` / `REVALIDATE_URL` を追加（値は `.env.example:43/58/62` と一致）、CI 検出用 `scripts/check_setup_env.py` ＋ `.github/workflows/setup-scripts-env.yml` / `windows-setup-script.yml` 追加。`.env.example` 丸コピー方式は不採用。消費側の不具合解消: `apps/admin/app/api/download/route.ts:4`（未設定だと `/build` で HTTP 500 だった）、`apps/public-viewer/app/api/revalidate/route.ts:9`（未設定だと 401 Invalid secret だった）。

## human-required 7件（実 API 課金・外部成果物・組織判断が必須）

- **[#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) ファクトチェックロジックの実験**: main に factcheck コード皆無（grep 0）。外部 repo `masatosasano2/factcheck-experiment` で実施、コード配置は idobata repo 統合まで保留。データセット作成・正解データ・組織判断が必須。
- **[#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346) 大量投稿対処の実験**: 外部 repo `nasuka/kouchou-ai-clustering-experiment` で部分実験済みだが『人間のまとめとかなり異なるクラスタ』で結論未確定。合意成果物が実験＋nishio/nasuka/takahiroanno の妥当性確認＝人間主導。
- **[#556](https://github.com/digitaldemocracy2030/kouchou-ai/issues/556) アクセシビリティ向上**: デジタル庁ガイドラインの TODO に順次対応する継続プログラム。個別合意要件なし、デザイナー判断必須。
- **[#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564) 活用事例を集めて公開**: 渉外担当が外部組織/自治体から事例収集・公開する渉外広報タスク。コードで解決不能。
- **[#882](https://github.com/digitaldemocracy2030/kouchou-ai/issues/882) KJ法プロンプト比較実験**: `experiments/` に baseline/KJ/neutral 比較の成果物なし（grep 0）。実機（課金 API）での実行・評価・採否方針が必須。
- **[#912](https://github.com/digitaldemocracy2030/kouchou-ai/issues/912) GPT-5.6 Terra/Luna 実 API 検証**: `model_catalog.json` で両モデル `verified=False`。Issue 本文が『実 API 検証は人間実施』と明記。
- **[#913](https://github.com/digitaldemocracy2030/kouchou-ai/issues/913) Gemini 3.8 Flash / 3.5 Flash-Lite 実 API 検証**: 同 `verified=False`。912 と同型。

## still-unresolved 44件（newVerdict と file:line 根拠の要約）

- **[#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11)** レポート出力時間の目安: `CreateReportConfirmation.tsx:143` が `時間：目安なし` 固定表示。時間目安未実装。
- **[#44](https://github.com/digitaldemocracy2030/kouchou-ai/issues/44)** クラスタ固有タイトル生成: `hierarchical_initial_labelling.py:151-154` がクラスタ内 argument のみを LLM 入力。近傍クラスタ差分の処理なし。
- **[#56](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56)** 元コメント表示機能: `hierarchical_aggregation.py:78` で公開 JSON は `"comments": {}` 固定、`_build_comments_value`(:97-98) はコメントアウト。表示側 `HierarchyListChart.tsx:36` は要約のみ。
- **[#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60)** 階層図で最下層を濃いクラスタに絞る: `ClientContainer.tsx:109` で density フィルタは散布図『濃い意見』モード専用、階層図は `effectiveMaxDensity=1`。
- **[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)** CSV アップロード時のコスト表示: `CreateReportConfirmation.tsx:142` が `費用：目安なし` 固定。費用概算(要素2)未実装。
- **[#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121)** 縦長画面で散布図表示が崩れる: `ScatterChart.tsx` に scaleanchor/scaleratio 等のアスペクト比固定なし（grep 0）、`Chart.tsx:88` は h=500px 固定・幅可変。是正コードなし。
- **[#170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/170)** ファクトチェック機能: grep factcheck/fact_check = 0 files。実験 [#324](https://github.com/digitaldemocracy2030/kouchou-ai/issues/324) も未実装。
- **[#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172)** クラスタ説明文のグラウンディング: grep grounding = 0。`enable_source_link` は別機能（argument→source URL）。
- **[#173](https://github.com/digitaldemocracy2030/kouchou-ai/issues/173)** グラウンディングの実験: [#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172) の実験 issue。スクリプト不在、[#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172) に依存。
- **[#186](https://github.com/digitaldemocracy2030/kouchou-ai/issues/186)** CSV を JSON 変換せず送信: `admin_report.py` ReportInput は依然 `comments: list[Comment]`(JSON)、UploadFile CSV エンドポイント無し。
- **[#190](https://github.com/digitaldemocracy2030/kouchou-ai/issues/190)** 1回の extraction で複数 comment: `extraction.py:159-191` は ThreadPoolExecutor で1コメント1リクエストの並列化のみ。PR [#246](https://github.com/digitaldemocracy2030/kouchou-ai/issues/246) closed unmerged。
- **[#236](https://github.com/digitaldemocracy2030/kouchou-ai/issues/236)** パブコメモードに回答案追加: `is_pubcom` は CSV 出力モードフラグのみ。回答案/RAG 未実装。
- **[#250](https://github.com/digitaldemocracy2030/kouchou-ai/issues/250)** 階層図最下層で原文表示: `HierarchyListChart.tsx:67` は `arg.argument`(抽出済み)のみ。`result.comments`(type.ts:114) を参照する表示コンポーネント無し。
- **[#266](https://github.com/digitaldemocracy2030/kouchou-ai/issues/266)** 散布図でクラスタラベル重なり: `ScatterChart.tsx` centroid 配置・固定 font 14/width 228。衝突回避/位置調整/可変 font/truncation 無し。
- **[#293](https://github.com/digitaldemocracy2030/kouchou-ai/issues/293)** レポート画面でプロンプト直接編集: `Analysis.tsx:133-326` は read-only。編集+再生成は admin reuse の回避策のみ。
- **[#323](https://github.com/digitaldemocracy2030/kouchou-ai/issues/323)** レポート多言語対応: 翻訳 step/出力言語選択がパイプライン・admin UI に無し。`Result.translations` 未投入。
- **[#337](https://github.com/digitaldemocracy2030/kouchou-ai/issues/337)** 全体図と階層図のクラスタ色統一: `ScatterChart.tsx:45-91` softColors[] と `TreemapChart.tsx:111-114`（Plotly default）が別割当。共有 cluster→color map 無し。
- **[#339](https://github.com/digitaldemocracy2030/kouchou-ai/issues/339)** 同義語マップ: extraction 他に同義語/読み替え処理なし（grep 0）。
- **[#342](https://github.com/digitaldemocracy2030/kouchou-ai/issues/342)** 文脈をふまえた生データ整形: 返信元/引用元/前後投稿の文脈付与前処理 step 無し。
- **[#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345)** 大量同一投稿への対処（情報整理）: 重複集約/similar-merge 前処理無し。実験子 [#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346) と役割分担（345=設計 triage）。
- **[#366](https://github.com/digitaldemocracy2030/kouchou-ai/issues/366)** 複数の公開リスト: 中核（複数リスト登録）は未実装。隣接の限定公開は `ReportVisibility` enum(report-schema/src/index.ts:38)＋PR [#500](https://github.com/digitaldemocracy2030/kouchou-ai/issues/500)(MERGED) で別途解決済み（混同しない。上流更新時に注記すべき）。
- **[#445](https://github.com/digitaldemocracy2030/kouchou-ai/issues/445)** .github/copilot-instructions.md 設置: main 非存在（find -iname '*copilot*' = 0）。ルート CLAUDE.md は代替にならず。
- **[#454](https://github.com/digitaldemocracy2030/kouchou-ai/issues/454)** Cold List 自動 wontfix: `status_update.py:22-49` は assign/unassign/ready/archive のみ。時間経過 wontfix 判定無し。前提 [#512](https://github.com/digitaldemocracy2030/kouchou-ai/issues/512) は MERGED だが本件固有機能は別。
- **[#470](https://github.com/digitaldemocracy2030/kouchou-ai/issues/470)** extract フェーズで個人情報除去: `extraction.py` に PII/マスキング無し。privacyLink はリンク表示のみ。
- **[#493](https://github.com/digitaldemocracy2030/kouchou-ai/issues/493)** スクロールで図が拡大縮小: `ScatterChart.tsx:532` が `scrollZoom: true` のまま。dentaro 案 PR [#597](https://github.com/digitaldemocracy2030/kouchou-ai/issues/597) は stale/close 済み。
- **[#503](https://github.com/digitaldemocracy2030/kouchou-ai/issues/503)** 個人情報生成と除去率測定: 生成・埋め込み・測定いずれも main 未実装。[#470](https://github.com/digitaldemocracy2030/kouchou-ai/issues/470) の評価基盤。
- **[#507](https://github.com/digitaldemocracy2030/kouchou-ai/issues/507)** report_status.json 互換コード削除: `convert_old_format_status`(report_status.py:24) が現存・実行時呼出。版は 0.1.x で削除条件 ver3.0 未到達（意図的残存・着手不可）。
- **[#513](https://github.com/digitaldemocracy2030/kouchou-ai/issues/513)** 再現性を選べる分析設定: `hierarchical_clustering.py:104` UMAP / :194 KMeans に `random_state` 無し。固定 seed は polars sample / PCA のみ。コメント『全場所で seed 記録』は不一致。
- **[#548](https://github.com/digitaldemocracy2030/kouchou-ai/issues/548)** 中間ファイルを CSV でなく DB 管理: `cluster_repository.py` は import csv・CSV パス参照、sqlite/sqlalchemy ヒット0。DB 移行未実装。
- **[#576](https://github.com/digitaldemocracy2030/kouchou-ai/issues/576)** 朝日 TTTC プロンプト取り込み: `extractionPrompt.ts` 他は独自既定文面のまま。asahi/TTTC 参照0。ソース別 RT 処理の条件分岐無し。
- **[#638](https://github.com/digitaldemocracy2030/kouchou-ai/issues/638)** 濃い意見ビュー改善案: `ScatterChart.tsx:472-498` ラベルは重心配置・showarrow:false のまま。点群外薄灰表示/縮小改良(nishio 案)未実装。
- **[#641](https://github.com/digitaldemocracy2030/kouchou-ai/issues/641)** レポート完成通知: osascript/watch_processing/完成通知 実装0。ReportCard は status 表示のみで能動通知無し。
- **[#643](https://github.com/digitaldemocracy2030/kouchou-ai/issues/643)** Docker build のシークレット渡し改善: `azure-deploy.yml:109-128` が依然 `--build-arg` で API キー類を渡す。BuildKit --secret 未移行。assignee=rolzy 着手痕跡なし。
- **[#648](https://github.com/digitaldemocracy2030/kouchou-ai/issues/648)** 管理画面レポート一括編集: `ReportCardList.tsx` は個別 ReportCard のみ。checkbox 複数選択/bulk 操作無し。
- **[#679](https://github.com/digitaldemocracy2030/kouchou-ai/issues/679)** 任意カテゴリーで分類: PR [#678](https://github.com/digitaldemocracy2030/kouchou-ai/issues/678)(merged) で category 分類削除。再実装なし（grep 0）。
- **[#869](https://github.com/digitaldemocracy2030/kouchou-ai/issues/869)** label refinement PR 化残作業整理: 前提 PR [#866](https://github.com/digitaldemocracy2030/kouchou-ai/issues/866)/[#867](https://github.com/digitaldemocracy2030/kouchou-ai/issues/867)/[#868](https://github.com/digitaldemocracy2030/kouchou-ai/issues/868) は merged だが label refinement 本体未 merge（コード・ファイル無し）。トラッキング issue。
- **[#879](https://github.com/digitaldemocracy2030/kouchou-ai/issues/879)** クラスタ×時刻ヒートマップ: heatmap コンポーネント無し（grep 0）。新規可視化提案、未着手。
- **[#880](https://github.com/digitaldemocracy2030/kouchou-ai/issues/880)** [8,64] のマンダラート可視化: grep mandal/マンダラート = 0。探索的可視化提案、未着手。
- **[#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954)** CLI の report_url_pattern / report_html_title: `a3c198e9` の `orchestration.py` validate_config の valid_fields に両フィールド無し、specs の options は ['replacements'] のみ。PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955) は 953 のみ修正、954 未対応。設定仕様(案A/案B)決定が残る。
- **[#960](https://github.com/digitaldemocracy2030/kouchou-ai/issues/960)** 全画面維持でクラスタ粒度切替: 粒度選択は全画面外 `DisplaySettingDialog.tsx:46` のみ。全画面ツールバー内トグル無し。PR [#961](https://github.com/digitaldemocracy2030/kouchou-ai/issues/961)(OPEN, 未 merge)。
- **[#962](https://github.com/digitaldemocracy2030/kouchou-ai/issues/962)** Biome lint 0＋CI で biome ci 強制: workflows 20ファイルに biome 含む0件。PR [#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)(OPEN, 未 merge)。
- **[#964](https://github.com/digitaldemocracy2030/kouchou-ai/issues/964)** 抽出プロンプト例の『〜すべき』言い直し: `prompts/__init__.py:35-36` と `extractionPrompt.ts:29-30` が『市民を教育すべき』等のまま。PR [#965](https://github.com/digitaldemocracy2030/kouchou-ai/issues/965)(OPEN)、docs [#967](https://github.com/digitaldemocracy2030/kouchou-ai/issues/967)(OPEN)。
- **[#971](https://github.com/digitaldemocracy2030/kouchou-ai/issues/971)** 侮辱/ヘイト・政策提案の任意分類ステップ: `opinion_classification.py`/`opinion_labels.py` 不在、参照0。PR [#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975)(OPEN, 未 merge)。
- **[#972](https://github.com/digitaldemocracy2030/kouchou-ai/issues/972)** 公開ビューアの表示言語切替(ja/en/ko): i18n/messages.ts/LanguageContext/kouchou-translate 不在。`translations` は型定義のみで常に空 {}。PR [#976](https://github.com/digitaldemocracy2030/kouchou-ai/issues/976)(OPEN, 未 merge)。

## 未確認範囲 / 注意

- **固定 checkout と remote の差**: 基準は `c297bc97` 固定 checkout。本日マージ済みの PR [#955](https://github.com/digitaldemocracy2030/kouchou-ai/issues/955)/[#957](https://github.com/digitaldemocracy2030/kouchou-ai/issues/957) を含む現行 remote main は `a3c198e9`。now-resolved 2件はこの差に起因する偽陰性で、remote 側のみで解決。他51件は両版で判定変わらず。
- **実機・実 API 未検証**: human-required 7件は実 API 課金・外部 repo 成果物・組織判断が前提で、コード静的照合では充足判定不能。偽陰性ではない。
- **in-flight PR は未 merge**: [#960](https://github.com/digitaldemocracy2030/kouchou-ai/issues/960)/[#962](https://github.com/digitaldemocracy2030/kouchou-ai/issues/962)/[#964](https://github.com/digitaldemocracy2030/kouchou-ai/issues/964)/[#971](https://github.com/digitaldemocracy2030/kouchou-ai/issues/971)/[#972](https://github.com/digitaldemocracy2030/kouchou-ai/issues/972) は OPEN PR（[#961](https://github.com/digitaldemocracy2030/kouchou-ai/issues/961)/[#963](https://github.com/digitaldemocracy2030/kouchou-ai/issues/963)/[#965](https://github.com/digitaldemocracy2030/kouchou-ai/issues/965)/[#975](https://github.com/digitaldemocracy2030/kouchou-ai/issues/975)/[#976](https://github.com/digitaldemocracy2030/kouchou-ai/issues/976)）が存在するが現行 main に未反映のため still-unresolved。merge されれば close 可。
- **隣接要件の既解決は格下げ対象外**: [#366](https://github.com/digitaldemocracy2030/kouchou-ai/issues/366) の限定公開/unlisted のように隣接機能が解決済みでも、中核要件が未充足なら still-unresolved のまま（partial へ格下げせず）。上流更新案で注記する。
- 公開 Issue への close/comment/本文編集/assign/merge はこのステップでは一切していない。close はメインが別途実行。
