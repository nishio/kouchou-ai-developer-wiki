---
type: analysis
summary: `hierarchical_status.json` は branch 上で workflow path でもほぼ legacy 互換になったが、`current_job` の残し方や `duration` など一部に意味論差分が残る
sources:
  - source-code.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
---

# `hierarchical_status.json` の意味論

`hierarchical_status.json` は CLI / API / rerun 判定の接点にある status file で、legacy `.run()` では `core/orchestration.py` が、workflow path では `orchestrator.run_workflow()` が書く。2026-05-21 時点の branch tip `04516af` では、workflow path もかなりこの file を維持するようになった。[[source-code]]より

本ページの目的は、**legacy `.run()` と workflow path で何が同等で、何がまだ差分か** を棚卸しすることにある。open PR `#840` の review では「workflow default 化の blocker は status semantics に残るか」が論点の 1 つだったため、その判定材料をここへ寄せる。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

## 結論

- API が日常的に読む `status`, `current_job`, token usage, `provider`, `model`, `error_stack_trace` は、branch 上ではほぼ workflow path でも維持される
- rerun 判定に使う `completed_jobs` / `previously_completed_jobs` も branch 上では carry-forward される
- ただし **`current_job` の終端時の扱い**, **`completed_jobs[].duration`**, **`estimated_cost`**, **progress 系 key** は legacy と完全同等ではない
- したがって「production path に乗せる最低限」はかなり満たしたが、「完全互換」と書くのはまだ強すぎる

## 項目別の比較

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
- workflow path: 同じ shape の entry を append するが、`duration` は現在 `0.0` 固定で、実測時間ではない。[[source-code]]より
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

- legacy `.run()`: token usage 更新時に保存されうる。[[source-code]]より
- workflow path: branch 上でも明示保存していない。[[source-code]]より
- API reader: `/status/step-json` は値があれば返すが、無ければ `None` になる。[[source-code]]より
- 評価: **差分あり**

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

## API / 運用から見て重要な差分

### 1. `current_job` を終端時に消さない

file 単体だけ読むと「completed なのに `current_job=embedding` が残っている」状態がありうる。もっとも API router は `status=completed` を優先して `"completed"` を返すため、現行の利用者には大きな破綻はない。[[source-code]]より

### 2. `completed_jobs[].duration` が workflow path では実測値でない

status file を進捗 UI や perf 分析の材料に再利用したくなると、この差分は無視できない。逆に rerun 判定や API の ready/error 表示にはほぼ効かない。[[source-code]]より

### 3. `estimated_cost` は workflow path で欠落しうる

現行 API は optional として読んでいるので致命傷ではないが、「legacy と同じ cost 見積りが status file に常に出る」と期待すると外れる。[[source-code]]より

### 4. `error` 文字列の形式は統一されていない

機械処理向けに parse するなら危険だが、現状の API は表示用途が中心で、workflow path の方が step 名を含むぶん診断しやすい。[[source-code]]より

## 含意

- `hierarchical_status.json` は branch 上で既に **workflow default 化を支える最低限の互換** をかなり満たしている
- 一方で、status file を「legacy と byte-for-byte 同じ意味」と見なすのはまだ早い
- 残課題は status file の存在そのものではなく、**progress / duration / cost のような周辺意味論をどこまで legacy に寄せるか** に縮んでいる
- したがって `Phase 3b` の完了宣言を出す前に見るべきなのは、「API と rerun が壊れないか」よりむしろ「差分を許容するか、さらに寄せるか」の設計判断である

## Open Questions

- workflow path でも `completed_jobs[].duration` を実測値にするべきか
- `estimated_cost` は status file の正式契約として維持するべきか
- `error` を `ExceptionType: ...` に寄せるべきか、step 文脈付き文面を canonical にするべきか
- `current_job_progress` / `current_jop_tasks` を workflow engine にも正式導入するべきか

## Updates

- 2026-05-21: 初回作成。branch tip `04516af` を基準に、legacy `.run()` と workflow path の `hierarchical_status.json` semantics を比較
