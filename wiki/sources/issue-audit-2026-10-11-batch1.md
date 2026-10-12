---
type: source
summary: "古い順 open Issue 先頭10件 (#11/#44/#52/#55/#56/#60/#79/#104/#121/#143) の 2026-10-11 live state と work/kouchou-ai main@c297bc97 への照合。作成前確認パネルの費用/時間は『目安なし』固定、#52 階層図連動は PR #927 merge 済み、#55 は viewer 読込済みだが admin 編集 UI 欠落、など要件別に確認"
last_checked: 2026-10-11 00:30 JST
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/11
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/44
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/52
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/55
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/56
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/60
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/79
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/104
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/121
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/143
  - source-code.md
  - issue-884-pre-create-review-contract-2026-06-30.md
  - issue-backlog-audit-2026-09-09.md
---

## What it is

digitaldemocracy2030/kouchou-ai の open Issue を `createdAt` 昇順に並べた先頭 10 件について、2026-10-11 00:30 JST に公開 GitHub の live state を再取得し、`work/kouchou-ai` の current main `c297bc97bb2bbce42964a90d7501c2d3592aeaf0` のコードに要件別照合したメモ。[[issue-backlog-audit-2026-10-11]] の根拠 source。判定一覧と次の一手はそちらに置く。

この 10 件の多くは [[issue-backlog-audit-2026-09-09]] が 2026-09-08〜09 に本文へ「2026-09-09 現状と残作業」を追記済み。本 source は、その後 merge された PR を反映しつつ current main を一次根拠に再確認したもの。過去の note を証拠として再利用せず、コードで確かめ直した。

## Freshness marker

- 公開 GitHub: 2026-10-11 00:30 JST に `gh issue list --state open --search 'sort:created-asc'`、`gh pr list --state open`、各 Issue の `gh issue view` を取得。open Issue 103 件、open PR 10 件。snapshot は `raw/issue-audit/2026-10-11-batch1/`（gitignored）と、公開 GitHub 由来のため private キュー `kouchou-issue-audit-queue/drafts/issue-audit/2026-10-11-batch1/github-snapshot/` にも保存。
- `work/kouchou-ai`: `main@c297bc97`、00:30 JST に `git fetch origin && git pull --ff-only`（Already up to date）。request.txt の参照 SHA と一致。
- 検証: 公開 Issue 本文・全コメント・現行コードの読解と、分類に効く主張の spot-grep（下記）。実 LLM / 実 API 課金・本番環境変更・アプリ起動による視覚再現は**していない**。
- 古い順 10 件の次候補（未着手）: #170, #172, #173, #176, #186。

## 先頭 10 件の作成日・担当・ラベル

| # | created | assignee | labels | title |
|---|---|---|---|---|
| 11 | 2025-03-04 | nishio | design/Admin/API | レポート出力にかかる時間の目安を記載する |
| 44 | 2025-03-15 | - | enhancement/API | クラスタ固有の特徴をより捉えたタイトルを生成する |
| 52 | 2025-03-16 | - | enhancement/Client | チャート表示に連動した文章表示 |
| 55 | 2025-03-16 | nishio | enhancement/Client/Admin/API | 濃いクラスタのしきい値のデフォルト値をレポートごとに設定 |
| 56 | 2025-03-16 | - (※) | enhancement/design/Client/API | 元コメントの表示機能 |
| 60 | 2025-03-16 | - | enhancement/design/Client/API | 階層図で最下層の表示を濃いクラスタだけに絞る |
| 79 | 2025-03-18 | - | enhancement/design/Admin | CSVアップロード時にそれを処理した場合のコストを表示 |
| 104 | 2025-03-20 | - | enhancement/Client | ツールの利用状況を知る仕組み |
| 121 | 2025-03-21 | - | Client | [BUG]縦長画面での散布図の表示がおかしい |
| 143 | 2025-03-25 | - | enhancement/API/Algorithm | クラスタ品質の自動評価 |

※ #56 は現在 assignee 欄は空だが、ei-blue が 2025-03-25 に `/assign`（#105 と共に対応）とコメントしている。GitHub の assignee 欄には現在反映されていない。進行中作業は観測されない。

## 関連 open PR（2026-10-11 時点）

| PR | state | 関連 | 要点 |
|---|---|---|---|
| [#946](https://github.com/digitaldemocracy2030/kouchou-ai/pull/946) | **open** | #55 | 「レポート別に濃いクラスタの初期値を保存する」。main 未反映。main の admin dialog には閾値入力が無いことを確認。タイトルだけで要件充足を断定しない。 |
| [#961](https://github.com/digitaldemocracy2030/kouchou-ai/pull/961) | open | (#60 ではない) | 「全画面表示のまま散布図のクラスタ粒度を切り替え」。#60（階層図最下層を濃いクラスタに絞る）とは別機能。 |
| [#927](https://github.com/digitaldemocracy2030/kouchou-ai/pull/927) | **merged** 2026-09-08 | #52/#528 | 「階層図の現在位置と説明一覧を連動させる」。commit `c5bb3004`。current main に反映済み。 |
| [#922](https://github.com/digitaldemocracy2030/kouchou-ai/pull/922) | merged | #11/#79/#884 | 作成前確認パネル。費用/時間欄は現在 placeholder。 |
| [#926](https://github.com/digitaldemocracy2030/kouchou-ai/pull/926) | merged | #79 | provider/model のチャット接続確認。 |

## 要件別の現行実装確認

コードリンクは commit `c297bc97` 固定。

### #11 レポート出力時間の目安 — 未解決
- 作成前確認パネル [`apps/admin/app/create/components/CreateReportConfirmation.tsx`](https://github.com/digitaldemocracy2030/kouchou-ai/blob/c297bc97bb2bbce42964a90d7501c2d3592aeaf0/apps/admin/app/create/components/CreateReportConfirmation.tsx#L143) L143 は `時間：目安なし` の固定文字列。`目安` の一致は apps/packages でこの費用/時間 2 箇所のみ。`CreateReportConfirmation.test.tsx:51` が `費用：目安なし` の表示を lock している。
- per-step の実行時間は記録されるが**実行中/後**のみ: `packages/analysis-core/src/analysis_core/core/orchestration.py` の `run_step` が `completed_jobs` に `duration` を書き status.json に保存。入力サイズ/モデルから事前に「分」を出すモデルは存在しない。`core/utils.py:106 estimate_tokens`（文字数ベース）はトークン推定であり時間ではなく、パネルに接続されていない。

### #44 クラスタ固有タイトル — 未解決
- ラベル生成は `packages/analysis-core/src/analysis_core/steps/hierarchical_initial_labelling.py`（`process_initial_labelling`、`df.filter(target_column == cluster_id)` で**単一クラスタのみ**抽出 → その argument だけを LLM 入力）と `hierarchical_merge_labelling.py`（対象クラスタの子ラベル＋対象クラスタ内 sample のみ）。
- プロンプト `prompts/__init__.py` の `INITIAL_LABELLING_PROMPT` / `MERGE_LABELLING_PROMPT` は具体性・抽象語回避（「多様な意見」を避ける）を促すが、**近傍/他クラスタの情報は入力に含まれない**。タイトル重複検出も無い（grep: neighbor/近傍/contrast/差分/dedup は無関係ヒットのみ）。distinctiveness は #143 の評価スクリプトに評価軸としてのみ存在し、生成には還流していない。

### #52 チャート連動文章 — 一部解決
- **階層図(treemap)は実装・テスト済**（PR #927, merged）。共有 state `treemapLevel`（`apps/public-viewer/components/report/ClientContainer.tsx:75`）→ `TreemapChart.tsx:169-173` の `onTreemapClick`→`onTreeZoom`（plotly 内部 zoom を React に反映＝issue の難所）→ `TreemapDetails.tsx`（現在位置の takeaway、「一つ上に戻る/全体に戻る」、属性フィルタ後件数と分母ラベル、0 件時メッセージ）。`treemapContext.test.ts` / `TreemapDetails.test.tsx` あり。
- **散布図は静的リスト**で選択非連動。`ScatterChart.tsx:536-559` の点クリックは source URL を開くだけ（`selectedCluster` state は存在しない）。`ClusterOverview.tsx:34-38` は takeaway と raw `cluster.value`（属性フィルタ後件数ではない）を表示。density 切替時にリストが再導出される list-level reactivity はあるが、per-selection の連動ではない。
- 補足: `ClusterBreadcrumb.tsx` は定義のみで未使用（dead/legacy）。

### #55 濃いクラスタ閾値のレポート別デフォルト — 一部解決
- **viewer 読込(b)=済**: `ClientContainer.tsx:55,70-71` が `visualizationConfig?.params.scatterDensity.maxDensity ?? 0.2` / `minValue ?? 5` を初期値に読む。
- schema / API は閾値 params を**保存可能**: `packages/report-schema/src/index.ts:405-460`（`ScatterDensityParams` / defaults 0.2・5）、`apps/api/src/schemas/visualization_config.py:12-55`、PATCH `apps/api/src/routers/admin_report.py:428-463` が config 全体を passthrough 保存。
- **admin 編集 UI(a)=欠落**: `apps/admin/app/_components/ReportCard/VisualizationConfigDialog/VisualizationConfigDialog.tsx` のフォームは「表示するチャート」チェックボックス（L186-200）と「デフォルト表示」Select（L205-243）のみ。閾値入力欄は無く、`config.params.scatterDensity` を読み書きしない。`DEFAULT_CONFIG`（L38-42）に params が無い。→ 出力者が閾値を保存できない。PR #946 は未 merge で main に無い。

### #56 元コメント表示 — 未解決
- 公開 `hierarchical_result.json` 組立は `packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py:75-115`。[`L78`](https://github.com/digitaldemocracy2030/kouchou-ai/blob/c297bc97bb2bbce42964a90d7501c2d3592aeaf0/packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py#L78) で `"comments": {}` と空、populate する呼び出し（L97-99）は**コメントアウト**。`_build_comments_value`（L373-389、`hidden_properties_map` で redaction）は dead code。出力は `comment_num`（件数）のみ。
- arguments は `comment_id` リンクを持つが原文本体は無し。
- pubcom のみ admin 向け CSV で原文を出す経路あり: `config["is_pubcom"]` 時 `add_original_comments`（L178-237）→ `final_result_with_comments.csv`。admin API ダウンロード `admin_report.py:149-157` でのみ取得でき、public-viewer には出さない。
- viewer に原文表示 UI は無い（ScatterChart hover は `arg.argument` を出すのみ、原文/元コメント toggle 無し）。
- **per-comment の再頒布可否フラグは入力/出力 schema に無い**（grep: 転載/引用/二次利用/consent/license は機能的ヒット無し）。あるのは属性値ベース redaction `hidden_properties_map` と粗い `is_pubcom` bool のみ。要件(1) の「引用元規約に注意」を満たす専用フィールドは未整備。

### #60 階層図最下層を濃いクラスタに絞る — 未解決
- 濃いクラスタ filter `getDenseClusters()`（`ClientContainer.tsx:258-272`、`density_rank_percentile <= maxDensity && value >= minValue`）は**散布図 density mode のみ**に適用（`ClientContainer.tsx:109-110` の `effectiveMaxDensity = selectedChart === "scatterDensity" ? maxDensity : 1`）。treemap は `result.clusters` 全件を受け取り、密度 pruning されない。
- treemap 最下層を濃いクラスタに絞る toggle は無い（R1/R2/R3 すべて未達）。`DisplaySettingDialog` の密度コントロールは散布図専用。
- PR #961 は fullscreen での散布図粒度切替であり #60 を満たさない。

### #79 CSVコスト表示 — 未解決
- 作成前確認パネル `CreateReportConfirmation.tsx:142` は `費用：目安なし` 固定。L130/L145 に「API 利用料がかかる」旨の文章警告はあるが数値/帯は無し。
- 価格 infra は存在するが**実トークン確定後の事後計算のみ**: `apps/api/src/services/model_catalog.json`（モデル別 input/output 単価）、`model_catalog.py:82 price_for_model`、`llm_pricing.py:8 calculate_cost`。表示は実行後のレポートカード `ReportCard/TokenUsage/TokenUsage.tsx:31`。
- frontend は単価を既に取得済み: `apps/admin/app/create/hooks/useModelCatalog.ts:13-33`。モデル選択も可能（`AISettingsSection.tsx` provider L93 / model L166）。**事前**にトークン量×単価→帯を出す関数と表示が欠落。Serverless の `src/lib/estimate.ts` はこの repo には無い。埋め込みモデルは独立 dropdown が無く（サーバ内処理 on/off toggle のみ）、埋め込み費用は別扱いが必要。

### #104 利用状況把握 — 要件再確認が必要
- GA4 は**各デプロイ単位**で導入済: `apps/public-viewer/app/layout.tsx:7-9,21`（`NEXT_PUBLIC_GA_MEASUREMENT_ID` かつ production 時）、`apps/admin/app/layout.tsx:16-18,30`、CSP `apps/shared/csp.ts`、`.env.example:52-55`、README.md:103-111。
- 各自ホスト者が**自分の GA ID** を入れる → データは運用者自身の GA プロパティに流れる。プロジェクトが横断的に集約 visibility を得る仕組みではない。レポート生成の ping イベントは無く generic pageview のみ。サーバ側に外部への phone-home / 集約は無い（`report_launcher.py:276,298` はローカル subprocess のみ）。opt-out UI / cookie consent も無い。
- Issue の Slack 議論（オプトアウト・自治体の温度感・プロトタイプで進める）から**方針が未合意**。実装着手は時期尚早。

### #121 縦長画面の散布図 — 未解決
- 散布図 `apps/public-viewer/components/charts/ScatterChart.tsx:506-525` の xaxis/yaxis には `scaleanchor` / `scaleratio` / `matches` / `constrain` が無い（repo 全体 grep でも散布図には無し＝spot 確認済み）。→ 1:1 を強制せず、plotly が x/y を独立に引き伸ばす。
- container は非全画面で `h=500px`（`Chart.tsx:87-90`）、全画面で `h=100dvh`（`Chart.tsx:57-77`）＋ `responsive:true`。縦長 viewport では縦横比が歪む。
- 唯一の縦長対応は `ClientContainer.tsx:60-69`、`≤600px` でデフォルト表示を hierarchyList（リスト）に切替＝**回避**であり散布図のアスペクト比自体は直していない。PR #329 のスマホ時ラベル非表示は current main に無い（`≤600px` リスト既定へ進化）。
- 視覚再現は未実施。確認には portrait viewport（例 390×844）で散布図を選択・全画面にして x/y の等距離が等 pixel になるか測定が要る。

### #143 クラスタ品質自動評価 — 一部解決
- 独立した評価スクリプトが `experiments/evaluation_report/`（約 951 LOC、committed）に存在。プロダクト runtime 非依存（`analysis_core.services.llm` を sys.path 経由で呼ぶのみ、orchestrator に未接続）。
  - `src/run_evaluation.py` CLI、`src/evaluate_silhouette_score.py`（silhouette、centroid/nearest 距離、1-5 scale）、`src/evaluation_consistency_llm.py`（LLM-judge 4 基準 Clarity/Coherence/Distinctiveness/Consistency を 1-5 rubric、`--mode print` で手動用）、CSV/HTML 出力。
- **欠落**: 同梱の評価データセット/harness（README は docker cp と OpenAI key 前提、#143 が挙げる文化庁パブコメの fixture も無し）、コミット済みの検証結果、プロダクト統合（grep: silhouette/coherence/品質評価 は experiments/ 外にゼロ）。統合は issue でも後段扱い。
- 補足: `experiments/embvec_reduce_public_comment/` に重複クラスタ検出の探索的 notebook 群があり #44/#143 の背景だが、統合 harness ではない。

## Open Questions

- #104 の収集項目・opt-out 既定・説明文という**方針決定**は人間判断。どの観測（プロトタイプ/自治体ヒアリング）で決めるか。
- #56 の per-comment 再頒布可否フラグを入力 schema に持たせるか、公開用と再分析用の情報契約をどこで分けるか。[[issue-backlog-audit-2026-09-09]] の #56 論点を継承。
- #11 / #79 の「粗い帯」を [[issue-884-pre-create-review-contract-2026-06-30]] の first PR scope に入れるか、後続 slice にするか。
- #121 の 1:1 lock は縦長で余白/可読性の tradeoff があり、container 側の調整と併せる必要がある。視覚再現での重症度確認が未。
