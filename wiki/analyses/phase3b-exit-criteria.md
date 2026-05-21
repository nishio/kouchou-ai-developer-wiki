---
type: analysis
summary: Phase 3b を「完了」と書くには workflow path が production 入口として実用互換であることを示せば足り、status file の byte-level 完全互換までは必須ではない
sources:
  - source-code.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
  - meeting-minutes.md
---

# Phase 3b 完了条件

[[refactoring-status]] では Phase 3b を「workflow engine はあるが dormant」と読んできたが、open PR `#840` の branch では CLI / API の canonical path がかなり workflow 側へ寄っている。次に必要なのは「まだ何が足りないか」を無限に増やすことではなく、**何を満たせば Phase 3b 完了と書いてよいか** を固定すること。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

本ページは、その完了条件を「必須条件」「許容差分」「merge 後 follow-up」に分けて定義する。

## 結論

Phase 3b の完了条件は、**workflow path が production 入口として実用互換であること** であって、legacy `.run()` と `hierarchical_status.json` が byte-for-byte 同じになることではない。[[source-code]]より

したがって、`PR #840` 相当の変更を main に入れたうえで次の必須条件を満たせば、「Phase 3b 完了、Phase 8 / follow-up へ移行」と書いてよい。

## 必須条件

### 1. CLI の canonical path が workflow である

- `python -m analysis_core`
- `kouchou-analyze`

の標準実行が `run_default()` / `run_workflow()` 系に乗ること。branch 上では既にそうなっている。[[source-code]]より

### 2. API の canonical path も workflow に乗る

`apps/api` の `report_launcher` / rerun / duplicate-reuse 経路が `python -m analysis_core` 経由で workflow path を使い、full generation・aggregation rerun・config rerun・duplicate reuse が service-level test で確認されていること。branch 上ではここもかなり満たしている。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

### 3. rerun に必要な status / artifact 再利用が実用互換である

少なくとも次が成立すること。

- `previous`, `completed_jobs`, `previously_completed_jobs` を読める
- 既存 artifact を使って downstream だけ rerun できる
- failure 後も `current_job`, `error`, token usage が API / rerun に必要な形で残る

これは **legacy と全く同じ shape** でなくてもよい。API と rerun 判定が壊れなければよい。[[hierarchical-status-semantics]]より

### 4. docs が canonical path を誤案内しない

README、deprecated README、refactoring docs が「まだ legacy `.run()` / `hierarchical_main.py` が標準」と読める状態を脱していること。branch 上では大半が更新済み。[[source-code]]より

### 5. 残差分が「未完 blocker」ではなく「許容差分」へ分類済みである

`hierarchical_status.json` の `duration`, `estimated_cost`, progress key のように、差分が残っていても production blocker ではないと説明できること。差分棚卸しは [[hierarchical-status-semantics]] にある。

## 許容差分

次は **Phase 3b 完了を止める理由にはしない** 方がよい。

### `completed_jobs[].duration` が workflow path で実測値でない

perf 分析には効くが、canonical path 切替の blocker ではない。[[hierarchical-status-semantics]]より

### `estimated_cost` が status file に常に出ない

現行 API は optional として扱っており、ready/error 判定や rerun には直結しない。[[hierarchical-status-semantics]]より

### `error` 文字列の形式が legacy と一致しない

parse 契約ではなく表示用途が中心で、workflow path の step 名付き文面はむしろ診断しやすい。[[hierarchical-status-semantics]]より

### 実データバリエーションの e2e が無限に厚くない

追加 e2e は価値があるが、ここは follow-up で増やせる。merge blocker にすると止めどころがなくなる。

## merge 後 follow-up でよいもの

### 1. status semantics の追加整備

- `duration` の実測化
- progress callback の正式導入
- `estimated_cost` の再導入有無

### 2. 実データ寄り e2e の拡充

provider 差分、artifact 欠損パターン差分、入力の揺れなどを厚くする。

### 3. Phase 8 の旧コード削除

Phase 3b 完了は「workflow を標準にした」段階であって、「legacy を全削除した」段階ではない。削除は次のフェーズ。[[refactoring-status]]より

## 完了宣言の文面案

`Phase 3b は完了。workflow engine は CLI / API の canonical path として実用互換に達し、status / rerun / duplicate-reuse を含む主要運用経路が workflow 側へ移った。legacy との差分は残るが、主に duration / cost / progress semantics の周辺差分であり、follow-up と Phase 8 で扱う。`

## 含意

- 「legacy 完全互換」を完了条件にすると、Phase 3b は無限に閉じなくなる
- 逆に「production 入口として使えるか」を基準にすると、完了判定はかなり明確になる
- `PR #840` の merge 判断と、wiki 上の Phase 3b ステータス更新は、この基準で揃えるのが一番混乱が少ない

## Open Questions

- 完了宣言を出すタイミングを `PR #840` merge 時点に置くか、その直後の small follow-up を 1 本入れてからにするか
- `hierarchical_status.json` の許容差分を、将来の正式 contract として文書化するか

## Updates

- 2026-05-21: 初回作成。Phase 3b の完了条件を、必須条件・許容差分・merge 後 follow-up に分けて整理
