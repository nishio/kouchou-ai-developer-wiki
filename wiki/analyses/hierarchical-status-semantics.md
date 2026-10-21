---
title: "hierarchical_status.json の意味論差分"
type: analysis
summary: "`hierarchical_status.json` は PR #840（2026-05-21 merge）以降、CLI でも API でも workflow path だけが書く。`completed_jobs[].duration` は常に 0.0、`estimated_cost` は成功時には書かれず（費用は API が token 数から計算）、`current_job` は終了後も残る。legacy `.run()` との項目別比較は merge 直前の記録"
sources:
  - source-code.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
---

# `hierarchical_status.json` の意味論

`hierarchical_status.json` は CLI / API / rerun 判定の接点にある status file である。PR [#840](https://github.com/digitaldemocracy2030/kouchou-ai/issues/840)（2026-05-21 merge）以降は、CLI（`kouchou-analyze` / `python -m analysis_core`）も API も `run_default()` → `run_workflow()` だけを通るので、この file を書くのは workflow path である。API はレポート生成・config からの生成・集計だけの再実行の 3 経路とも、`python -m analysis_core` を subprocess で起動する。legacy の `PipelineOrchestrator.run()` は `DeprecationWarning` を出す形で残っているが、通常の経路からは呼ばれない。[[source-code]]より

本ページはもともと、この PR の review で論点だった「workflow default 化の blocker は status semantics に残るか」を判定するため、merge 直前の branch tip `04516af` で legacy `.run()`（`core/orchestration.py` が書く）と workflow path の差分を棚卸ししたものである。下の「項目別の比較」はその時点の記録として残し、今の main での性質は次の「結論」にまとめる。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

## 結論（2026-10-21 の main `b71e0b79` で確認）

- API が日常的に読む `status`, `current_job`, token usage, `provider`, `model`, `error` は workflow path が書く。予期しない例外で止まった時は `error_stack_trace` も書く
- rerun 判定に使う `completed_jobs` / `previously_completed_jobs` も carry-forward される
- `completed_jobs[].duration` は常に `0.0` で、実測値ではない
- `estimated_cost` は、成功時には status file に書かれない。error で終わった時は `estimated_cost: null` と `token_usage_complete: false` が書かれる。費用は API が token 数から計算して自分のレポート状態に持つので、admin の `/status/step-json` が status file から返す `estimated_cost` は `None` になる
- `current_job` は終了後も最後の step 名が残る。API は `status` を優先して読むので、実害は小さい
- analysis-core が書く `error` の文面は 3 通りある。workflow の step が失敗した時は `"Step '<step>' failed: ..."`（入力検証で止まった時は `"Step '<step>' validation failed: ..."`）、予期しない例外の時は `str(e)`、中断された時は `"Interrupted: <例外の型名>"`。analysis-core のプロセスが異常終了した時や、起動・storage への同期に失敗した時は、API が `status: error` と `error_log_path` / `error_log_excerpt`（ログの末尾）を書き足す
- analysis-core の `update_status()` は、一時ファイルに書いてから置き換える atomic な書き方をする（PR [#1033](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1033)、2026-10-19 merge）。admin の `/status/step-json` は JSON を読めなかった時も失敗扱いにせず、`loading` / `running` として次のポーリングに任せる
- 別の出力から中間成果物を再利用して作った時（config の `reuse_from`、CLI の `--reuse-from`）は、再利用元を示す `reused_from` が入る
- progress 系 key（`current_job_progress` / `current_jop_tasks`）は、workflow engine の正式な callback としては扱われていない（Open Questions）

## 項目別の比較（2026-05-21 時点、merge 直前の記録）

以下は branch tip `04516af` を基準にした当時の記録で、「workflow path」は当時 branch 上にあった実装を指す。今の main での性質は上の「結論」を見る。

### `status`

- legacy `.run()`: `running` → `completed` / `error` を `termination()` で確定する。[[source-code]]より
- workflow path: 同じく `running` で開始し、`WorkflowResult.success` に応じて `completed` / `error` を書く。予期しない exception でも `error` を書く。[[source-code]]より
- 評価: **ほぼ同等**

### `plan`

- legacy `.run()`: `initialization()` が `decide_what_to_run()` の結果を status file にも保存する。[[source-code]]より
- workflow path: `from_dict()` / `from_config()` から得た plan を開始時に保存する。explicit plan を渡した場合はそれを尊重するよう branch 上で修正済み。[[source-code]]より
- 評価: **同等**

### `start_time` / `end_time`

- legacy `.run()`: 開始・終了で保存する。[[source-code]]より
- workflow path: 同様に開始・終了で保存する。[[source-code]]より
- 評価: **同等**

### `current_job`

- legacy `.run()`: `run_step()` 開始時に step 名を入れる。終了時に明示的に消す処理は無く、最終 status が `completed` / `error` に変わる。[[source-code]]より
- workflow path: `mark_step_started()` で step 名を入れ、終了後も消さない。failure 時は失敗した step 名を残す。[[source-code]]より
- API reader: `/status/step-json` は `status=completed` なら `current_job` の値に関わらず `completed` を返し、`status=error` なら `current_job` を current step として返す。[[source-code]]より
- 評価: **実運用上はほぼ同等だが、file 単体の意味としては差分あり**

### `current_job_started`

- legacy `.run()`: step 開始時に保存する。[[source-code]]より
- workflow path: 同様に保存する。[[source-code]]より
- 評価: **同等**

### `current_job_progress` / `current_jop_tasks`

- legacy `.run()`: 長い step の進捗 callback から更新されうる。[[source-code]]より
- workflow path: step 完了時に空へ戻すが、engine 自体は進捗更新をまだ積極利用していない。[[source-code]]より
- 評価: **差分あり**

### `completed_jobs`

- legacy `.run()`: 各 step 完了時に `step`, `completed`, `duration`, `params`, `token_usage` を append する。`duration` は実測秒数。[[source-code]]より
- workflow path: 同じ shape の entry を append するが、`duration` は `0.0` 固定で、実測時間ではない。[[source-code]]より
- 評価: **shape は同等、意味は差分あり**

### `previously_completed_jobs`

- legacy `.run()`: rerun 時に prior status から carry-forward する。[[source-code]]より
- workflow path: branch 上で同様に carry-forward する。[[source-code]]より
- 評価: **同等**

### `total_token_usage` / `token_usage_input` / `token_usage_output`

- legacy `.run()`: step 実行のたびに加算し、status file に保存する。[[source-code]]より
- workflow path: step 完了時に加算し、最終結果と status file の両方へ保存する。exception path でも branch tip `04516af` で 0 に戻さず保持するよう直った。[[source-code]]より
- API reader: `report_launcher` と `/status/step-json` の両方がここを読む。[[source-code]]より
- 評価: **branch 上では実用上同等**

### `provider` / `model`

- legacy `.run()`: 初期化時に status file へ保存する。[[source-code]]より
- workflow path: 同様に保存する。[[source-code]]より
- API reader: `/status/step-json` は status file から返すが、`report_launcher` の完了処理は config 側も参照する。[[source-code]]より
- 評価: **同等**

### `estimated_cost`

- legacy `.run()`: `run_step()` が各 step の後に key を書くが、`run()` は `run_step()` に `pricing_calculator` を渡さないので、値は placeholder（当時は `0.0`）で計算値ではなかった。[[source-code]]より
- workflow path: branch 上でも明示保存していない。[[source-code]]より
- API reader: `/status/step-json` は値があれば返すが、無ければ `None` になる。[[source-code]]より
- 評価: **key の有無は違うが、どちらの経路でも status file に計算した費用は入っていなかった**

### `error`

- legacy `.run()`: `termination()` は原則 `"{ExceptionType}: {message}"` 形式で保存する。[[source-code]]より
- workflow path: workflow result failure では `"Step '<name>' failed: ..."` のような step 文脈付き文面になる。予期しない exception では `str(e)` をそのまま保存する。[[source-code]]より
- 評価: **差分あり。ただし API / rerun に必要な情報量は branch 上の方がむしろ多い**

### `error_stack_trace`

- legacy `.run()`: error 時に保存する。[[source-code]]より
- workflow path: 予期しない exception 時に保存し、failure semantics を legacy に寄せる修正が branch 上で入った。[[source-code]]より
- 評価: **ほぼ同等**

### `lock_until`

- legacy `.run()`: `update_status()` が毎回更新し、stale running detection に使う。[[source-code]]より
- workflow path: 同じ `update_status()` を通るので更新される。[[source-code]]より
- 評価: **同等**

## API / 運用から見て重要な性質

以下は 2026-05-21 時点で legacy との差分として挙げたもので、今の main では workflow path の性質としてそのまま残っている。

### 1. `current_job` を終端時に消さない

file 単体だけ読むと「completed なのに `current_job=embedding` が残っている」状態がありうる。もっとも API router は `status=completed` を優先して `"completed"` を返すため、利用者には大きな破綻はない。[[source-code]]より

### 2. `completed_jobs[].duration` が実測値でない

status file を進捗 UI や perf 分析の材料に再利用したくなると、この性質は無視できない。逆に rerun 判定や API の ready/error 表示にはほぼ効かない。[[source-code]]より

### 3. `estimated_cost` は status file に入らない

成功時は key が無く、error 時は `null` になる。費用は API が token 数から計算するので、status file の `estimated_cost` を費用の出どころとして読むと外れる。[[source-code]]より

### 4. `error` 文字列の形式は統一されていない

機械処理向けに parse するなら危険だが、現状の API は表示用途が中心で、step 名を含む文面の方が診断しやすい。[[source-code]]より

## 含意

- PR [#840](https://github.com/digitaldemocracy2030/kouchou-ai/issues/840) の merge で workflow path が canonical になり、Phase 3b は完了扱いになった（[[refactoring-status]] / [[phase3b-exit-criteria]]）。上の性質は merge の blocker ではなく、許容した差分として残っている
- status file を「legacy と byte-for-byte 同じ意味」と見なさない
- 残課題は status file の存在そのものではなく、**progress / duration / cost のような周辺意味論を、どこまで正式な契約にするか** である

## Open Questions

- workflow path でも `completed_jobs[].duration` を実測値にするべきか
- `estimated_cost` を status file の正式契約に戻すべきか、API 側の計算に一本化して key をやめるべきか
- `error` を `ExceptionType: ...` に寄せるべきか、step 文脈付き文面を canonical にするべきか
- `current_job` を終了時に消すべきか
- `current_job_progress` / `current_jop_tasks` を workflow engine の正式な callback にするべきか

## Updates

- 2026-05-21: 初回作成。branch tip `04516af` を基準に、legacy `.run()` と workflow path の `hierarchical_status.json` semantics を比較
- 2026-10-21: main `b71e0b79` と照合し、PR [#840](https://github.com/digitaldemocracy2030/kouchou-ai/issues/840)（2026-05-21 merge）後の現状（workflow path だけが書く、`duration` は 0.0 固定、`estimated_cost` は成功時に無い、PR [#1033](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1033) で atomic な書き込み）を冒頭と「結論」に書き直し、項目別の比較を merge 直前の記録として位置づけ直した。legacy `.run()` の `estimated_cost` が計算値ではなかったことも訂正
