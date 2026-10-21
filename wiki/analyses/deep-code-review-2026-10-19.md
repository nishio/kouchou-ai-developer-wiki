---
title: "本格コードレビュー 2026-10-19"
type: analysis
summary: "main 083593ba を 8 領域＋横断フロー追跡で洗い出し、指摘を全件反証・再現で検証したレビューのうち、修正 PR（#1032–#1041）を出した 36 件の記録"
sources:
  - source-code.md
  - code-health-review-2026-10-18.md
---

## 位置づけ

nishio「コードのチェックをもっと本格的にやろうか」を受けたレビュー。[[code-health-review-2026-10-18]] より範囲と検証を深くし、9 つの観点での洗い出し（API の router / service、analysis-core の orchestration / 解析ステップ、LLM プロバイダ、public-viewer、admin、インフラ・CI、横断のフロー追跡）→ 指摘ごとの反証・再現 → 重要度の高いものは別の検証者が再現をやり直す、の順で進めた。観測時点は kouchou-ai main `083593ba`。[[source-code]]より

横断のフロー追跡は「入力や設定値がファイルをまたいでどの出口に届くか」を追う担当で、ある変更が離れた場所の古い処理とつながって起きる不具合を探すために置いた。

修正は 10 グループに分け、グループごとに独立に実装 → 実装とは別の検証者がレビュー → 指摘を修正、の順で進め、最後に全ブランチの差分確認・テスト再実行・全ブランチをまとめて merge した状態でのテスト（analysis-core 383 / api 362 passed）を手元で行ってから PR にした。merge は未実施。

## 修正 PR と指摘

### [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1032) 集計結果のデータ欠落

- 【中】同じ文面に抽出された意見が複数の回答から出たとき、属性と URL が最後の回答の分しか残らず、属性フィルタで他の回答者が消える（`packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py:264`）
- 【中】relations.csv を型推論で読み直すため、先頭ゼロ等の comment-id が壊れ、属性・出典URL・comment_id が黙って失われる（`packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py:88`）
- 【中】古い opinion_classifications.csv が無条件に結果へマージされ、optional ステップが失敗しても exit 0 になる（`packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py:337`）
- 【低】custom intro の「分析対象件数」が、空コメント除外前の件数で過大に表示される（`packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py:142`）

### [#1033](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1033) 再実行判定と CLI オプション

- 【中】input・question・intro・is_pubcom・enable_source_link・hidden_properties・extraction.properties の変更を再実行判定が検知せず、--reuse-from では複製元の結果がそのまま出力される（`packages/analysis-core/src/analysis_core/specs/hierarchical_specs.json:4`）
- 【中】途中で失敗した実行を再実行すると、上流だけ更新済みで下流が古いまま全段 skip され、古い結果で completed になる（`packages/analysis-core/src/analysis_core/core/orchestration.py:394`）
- 【中】kill や Ctrl+C で中断した後の再実行では、最も古い previous まで遡って判定するため、中断した実行が上書きした成果物を見落とす（`packages/analysis-core/src/analysis_core/core/orchestration.py:346`）
- 【低】hierarchical_status.json の非アトミックな書き込みで、admin の進捗ポーリングが実行中のレポートを失敗扱いにして止まる（`packages/analysis-core/src/analysis_core/core/orchestration.py:450`）
- 【低】--only の値を検証しておらず、存在しないステップ名では何も実行せずに成功終了する。--force と併用すると --only が無視されて全段が再実行される（`packages/analysis-core/src/analysis_core/core/orchestration.py:382`）
- 【低】--dry-run / --validate-config / --validate-input でも --reuse-from の成果物コピーと seed 済み status の書き込みが走り、以後の --reuse-from 指定が黙って無視される（`packages/analysis-core/src/analysis_core/core/orchestration.py:690`）

### [#1034](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1034) レポートのライフサイクル

- 【高】タイトル・説明の編集（PATCH /admin/reports/{slug}/config）で config から enable_source_link と embedding.model が消え、再集計で出典リンクが黙って消える（`apps/api/src/repositories/config_repository.py:50`）
- 【中】既存レポートと同じIDで新規作成すると全ステップが skip され、旧レポートの結果が新レポートとして黙って残る（`apps/admin/app/create/utils/validation.ts:9`）
- 【中】POST /admin/reports が既存 slug（削除済み含む）を拒否せず、既存レポートを上書きし、旧成果物を黙って再利用する（`apps/api/src/routers/admin_report.py:79`）
- 【中】サーバー再起動で処理中のレポートが processing のまま固まり、再実行も複製もできない（`apps/api/src/services/report_launcher.py:290`）
- 【低】成果物のアップロードが失敗しても ready のまま status がアップロードされ、再起動後は結果ファイルの無い ready レポートになる（`apps/api/src/services/report_launcher.py:260`）
- 【低】reuse 付き複製では元レポートの completed な status ファイルがコピーされ、新しいカードの進捗ポーリングが即座に止まる（`apps/admin/app/_components/ReportCard/ProgressSteps/useReportProgressPolling.ts:72`）

### [#1035](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1035) llm_grouping レポートのラベル編集

- 【中】llm_grouping レポートのラベル CSV に density 列が無く、ラベル編集が使えない（API を直接呼ぶと全ラベルが消える）（`apps/api/src/repositories/cluster_repository.py:50`）
- 【中】llm_grouping レポートで cluster-labels が常に空になり、PATCH cluster-label が hierarchical_merge_labels.csv をヘッダーだけに切り詰める（`apps/api/src/repositories/cluster_repository.py:44`）

### [#1036](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1036) スプレッドシート取り込みの comment-id

- 【中】スプレッドシートの comment-id が数値だとレポート作成が 422 で失敗し、属性値の先頭 0 も黙って消える（`apps/api/src/routers/spreadsheet.py:96`）

### [#1037](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1037) LLM プロバイダ（analysis-core）

- 【中】Flex（最大900秒）と、バッチ待機タイムアウト（timeout_seconds=既定300秒）が食い違い、遅い成功応答を TimeoutError として分析全体を中断する（`packages/analysis-core/src/analysis_core/steps/extraction.py:193`）
- 【中】Gemini の出力トークンに thinking トークンが入らず、費用見積もりが過小になる（`packages/analysis-core/src/analysis_core/services/llm.py:406`）
- 【中】Gemini 埋め込みは1テキスト1リクエストを逐次で送り、429 を再試行しないので、件数が多いと埋め込みステップが失敗する（`packages/analysis-core/src/analysis_core/services/llm.py:810`）
- 【低】local LLM のアドレスが解析できないと、警告だけ出して localhost:11434 に黙って接続先を差し替える（`packages/analysis-core/src/analysis_core/services/llm.py:513`）
- 【低】overview の JSON パースに失敗した時の代替処理が、think タグを外しただけの JSON 文字列（または途中で切れた JSON）をそのまま overview として公開する（`packages/analysis-core/src/analysis_core/steps/hierarchical_overview.py:72`）

### [#1038](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1038) LLM プロバイダ（API）

- 【中】/admin/models の local アドレス解析がパイプラインと違い、HTTPS ゲートウェイやポート省略のアドレスでモデル一覧を取れない（`apps/api/src/services/llm_models.py:93`）
- 【低】admin の接続確認で、Gemini の認証エラーやレート制限が「不明なエラー」に分類される（`apps/api/src/routers/admin_report.py:576`）

### [#1039](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1039) 公開ビューアの OGP・表示

- 【中】「濃い意見」モードのまま抽出結果が 0 件になると、一つ上の階層の全クラスタを「濃い意見」として黙って表示する（`apps/public-viewer/components/charts/plugins/scatter.tsx:62`）
- 【中】OGP フォントのキャッシュに失敗した Promise が残り、Google Fonts が一度失敗するとプロセス再起動まで OGP 生成が全滅する（`apps/public-viewer/app/[slug]/_op-image.tsx:32`）
- 【中】Next 16 で opengraph-image の params が Promise になったのに同期で読んでおり、SSR の OGP 画像が全レポートで失敗する（`apps/public-viewer/app/[slug]/opengraph-image.tsx:6`）
- 【低】サーバーモードの public-viewer では /meta/reporter.png と /meta/icon.png が 404 になる（copy-image が static ビルドでしか動かない）（`apps/public-viewer/package.json:6`）
- 【低】build:static が失敗すると postbuild:static が走らず、opengraph-image.tsx がリネームされたまま作業ツリーに残る（`apps/public-viewer/scripts/rename-file.mjs:7`）
- 【低】OGP 用 fetchApiWithRetry が、リトライしないはずの 4xx を自分の catch で拾って 6 回・約 5 秒リトライする（`apps/public-viewer/app/[slug]/_op-image.tsx:52`）
- 【低】静的書き出しで metadataBase を設定しないため、og:image が http://localhost:3000/... に解決される（`apps/public-viewer/app/[slug]/page.tsx:117`）

### [#1040](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1040) static-site-builder の静的ビルド

- 【中】static-site-builder がイメージ作成時点の apps/api/public をコピーして使うため、静的 HTML 出力に既定のテスト用 reporter.png・icon・ogp が混ざる（`apps/static-site-builder/Dockerfile:49`）

### [#1041](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1041) 管理画面（再利用ページ・作成時エラー）

- 【中】再利用ページで分析方式を切り替えても override に含まれず、元の方式で黙って実行される（`apps/admin/app/reuse/[slug]/page.tsx:234`）
- 【低】createReport が API のエラー詳細を捨て、statusText だけを表示する（`apps/admin/app/create/api/createReport.ts:82`）

## 気づき

- **黙ったデータ欠落が多い**: comment-id の型推論、同じ文面の意見の帰属、古い中間ファイルのマージなど、エラーにならずに結果だけが少し違う種類の不具合が目立った。テストは「動くこと」だけでなく「属性・件数が入力と一致すること」まで確かめる必要がある
- **再実行の判定は状態が多い**: params に入っていない設定値、途中で失敗した実行、中断後の previous、`--only` / `--force` / `--reuse-from` の組み合わせで、古い結果のまま完了になる経路が複数あった（[#1033](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1033)）
- **同じファイルを複数の PR が触る**: `admin_report.py` は 4 本の PR が触る。[#1034](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1034) と [#1041](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1041) は `createReport.test.ts` が衝突するので、後から merge する側で解消する
- **挙動が変わる修正**: [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1032) は、別の回答から出た同じ文面の意見を回答ごとに 1 件として数えるようになるので、意見数・散布図の点の数が増えることがある

## Open Questions

- 10 本の PR のレビューと merge の判断（人間 attention を使う操作なので明示指示時のみ）
- [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1032) の意見数の数え方の変更をリリースノートでどう伝えるか

## Updates

- 2026-10-19: nishio「CI が通った PR は admin merge」の指示で [#1032](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1032)–[#1041](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1041) を squash merge。[#1033](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1033)・[#1036](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1036)・[#1041](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1041) は先行 PR との衝突を rebase で解消し、テスト再実行・CI 通過後に merge した。merge 後の main でも analysis-core / api のテストが通ることを確認
