---
title: 広聴AIで次に検証したい性質 2026-11-25
type: analysis
summary: 階層レポートの件数・表示、生成から復旧までの状態遷移、LLM直接グルーピングの割当の3件を比較。現行の構造検査を通る合成レポートで、全件一致するフィルターにより件数が0から1に変わることを再現した
sources:
  - source-code.md
  - lean-verification-trial-2026-11-24.md
  - issue-1156-opinion-comment-contract-2026-11-25.md
---

## 調査範囲

2026-11-25 に広聴AI本体の `main` [`03d07295`](https://github.com/digitaldemocracy2030/kouchou-ai/commit/03d0729524ff5b8b3d3fc797a5dab98308032521) を読み、GitHub の直近コミットと照合した。依存解決・再実行判定・クラスタの親子関係の Lean 検証は [#1239](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1239)、多対多の出典の検証は [#1246](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1246) で本体に入っている。表示プラグインの登録と選択は進行中の [#1250](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1250) が扱う。[[source-code]]より [[lean-verification-trial-2026-11-24]]より

## 1. 階層レポートの件数と表示

最初に着手するならここ。Python の `validate_output` はクラスタ ID や意見の親子経路を検査するが、保存された `value` と所属意見数の一致は検査しない。TypeScript の `treemapContext` と `buildTreemapFigure` はフィルターなしでは保存値を使い、フィルターありでは `cluster_ids` から数え直す。階層リストにもフィルター時の集計がある。[[source-code]]より [構造検査](https://github.com/digitaldemocracy2030/kouchou-ai/blob/03d0729524ff5b8b3d3fc797a5dab98308032521/packages/analysis-core/src/analysis_core/validate_output.py#L16)・[階層図の説明欄](https://github.com/digitaldemocracy2030/kouchou-ai/blob/03d0729524ff5b8b3d3fc797a5dab98308032521/apps/public-viewer/components/report/treemapContext.ts#L5)・[階層図の値](https://github.com/digitaldemocracy2030/kouchou-ai/blob/03d0729524ff5b8b3d3fc797a5dab98308032521/apps/public-viewer/components/charts/TreemapChart.tsx#L74)

- **再現**。root の保存値を 1、子クラスタ `1_0` を 0 とし、経路 `['0', '1_0']` の意見 `a` を 1 件置いた。本物の `validate_output` はエラー 0 件。`treemapContext` は `1_0` をフィルターなしで 0 件、全件一致 `['a']` で 1 件と返した。リポジトリに含まれる結果 JSON 3 件では、全クラスタの保存値と所属意見数が一致した。階層図・説明欄・階層リストに関する既存 Jest 18 件も通過した。再現範囲は合成入力での検査器と表示計算の食い違い。
- **最初の検証**。同じ小さな JSON を Python と TypeScript に渡し、全件一致は未絞り込みと件数が同じ、0 件一致なら全部 0、同じ意見集合を使う画面間で件数が一致する、を確認する。各クラスタの保存値を 1 だけずらした入力で、検査が欠陥を検出することも確かめる。
- **Lean の対象**。妥当な親子経路と意見集合を前提に、あるクラスタの件数は直下の子クラスタの件数の合計と、そのクラスタに直接所属する意見数の和になる。絞り込み後もこの等式が成り立ち、表示に渡す葉を一部省略した場合は描画対象の子の合計が親を超えない。既存の木モデルは経路と親子関係を扱うので、件数の仕様と検査器がそれを保証する条件を追加できる。実データに届く保証は実装との適合性テストで確認する。[[lean-verification-trial-2026-11-24]]より

## 2. レポートの生成・保存・再起動をまたぐ状態遷移

`report_launcher` は成果物の同期後に `ready` を設定し、起動時は `processing` が残ったレポートを復旧する。既存テストはアップロード失敗や、削除と処理完了が重なったときの状態を検査している。次は複数のイベントが連続した場合を対象にする。たとえば保存途中で停止して再起動する、復旧中に同期が失敗してもう一度再起動する、再集計と削除の完了順が入れ替わる。[[source-code]]より [完了と復旧の実装](https://github.com/digitaldemocracy2030/kouchou-ai/blob/03d0729524ff5b8b3d3fc797a5dab98308032521/apps/api/src/services/report_launcher.py#L265)・[ライフサイクル修正 #1034](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1034)・[削除の回帰修正 #1067](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1067)

まず偽ストレージと一時ディレクトリで、実際の Python に操作列と故障を注入する。復旧後に `ready` なら対応する完成済み成果物が読める、完了通知で `deleted` が戻らない、同じ保存状態から復旧を繰り返しても結果が変わらない、を候補の条件にする。順序の組合せが増えたら TLA+/TLC の小さな有限モデルで網羅し、見つけた操作列を Python の回帰テストに戻す。今回、新たな障害の再現は行っていない。 [Hypothesis の状態機械テスト](https://hypothesis.readthedocs.io/en/latest/stateful.html)・[TLA+ の検証ツール](https://lamport.azurewebsites.net/tla/tools.html)

## 3. LLM 直接グルーピングの割当

`_assign_groups` は応答を辞書にまとめ、各入力 ID を順に引いて、欠落や未知のグループを既定枠に割り当てる。進行中の [#1255](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1255) は全件一括の場合に欠落・重複などをエラーにする方針。通常バッチと一括のそれぞれで、合意した規則を実コードに対して確かめる候補になる。[[source-code]]より [割当の実装](https://github.com/digitaldemocracy2030/kouchou-ai/blob/03d0729524ff5b8b3d3fc797a5dab98308032521/packages/analysis-core/src/analysis_core/steps/llm_grouping.py#L267)

LLM の応答を置き換えて、欠落・重複・余分な ID・未知のグループと、バッチの完了順を生成する。成功した出力では入力の各意見が一度だけ既知のグループに属する。欠落等を補った意見がどの枠に入るか、厳格な一括モードならどの応答を拒否するかも検査する。最初はプロパティベーステストで十分。分類やラベルの意味の妥当性は、固定した入力を元の意見と照合して評価する。

## Open Questions

- 旧版や外部で生成したレポートで `value` と所属意見数が食い違う場合、読み込み時に数え直すか、警告して保存値を示すか。まず検査コマンドで検出できれば、互換性を変えずに実例を調べられる。
- 復旧の仕様を単一サーバーの再起動からどこまで広げるか。現行コードはサーバー再起動後も解析プロセスが動き続けるケースに制約を明記している。
