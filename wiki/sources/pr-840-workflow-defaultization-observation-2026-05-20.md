---
type: source
summary: draft PR #840 は `run_workflow()` default 化に向けて、初期 artifact・status 永続化・rerun artifact 再利用に加え、CLI/API 入口と duplicate/reuse rerun plan の integration 確認まで段階的に進めている
sources:
  - source-code.md
  - github-dev-docs.md
---

# `PR #840` workflow defaultization 観測

2026-05-20 時点の open PR `#840` (`[codex] workflow default化の土台を整備`) を観測すると、Phase 3b は current `main` ではなお dormant だが、**open PR 上では blocker の一部が既に分割コミットで前進している**。[[github-dev-docs]]より [[source-code]]より

## 観測対象

- PR: `https://github.com/digitaldemocracy2030/kouchou-ai/pull/840`
- head branch: `codex/refactor-workflow-defaultization`
- base: `main`
- 観測時点の head commits:
  - `067e8a5` `Seed workflow inputs and align html config`
  - `71e603a` `Persist workflow status during execution`
  - `0c71649` `Reuse prior workflow outputs for reruns`
  - `cc17509` `Harden workflow flag sync and plugin callbacks`
  - `24e02cc` `Route CLI through workflow default path`
  - `ec694b7` `Consolidate analysis-core launcher commands`
  - `bfda3dd` `Validate scoped workflow e2e plans`
  - `7167cf4` `Preserve explicit workflow plans in from_dict`
  - `b6310cd` `Test workflow status handling in report launcher`
  - `fe5eda5` `Cover aggregation rerun status updates`
  - `2c8632b` `Exercise aggregation rerun service flow`
  - `b869324` `Exercise full report launcher service flow`
  - `142a63f` `Cover CLI workflow rerun planning`
  - `3737642` `Align workflow failure status semantics`
  - `1e3ec9e` `Cover config-based launcher service flow`
  - `6f940fc` `Test duplicate workflow artifact reuse`
  - `d43a07b` `Test duplicate-style workflow reruns`
  - `b163ba2` `Test duplicate rerun planning from config`
- `2565b07` `Add real workflow rerun e2e`
- `8e54904` `Cover workflow failure step status API`
  - `04a8e97` `Refresh refactoring docs for workflow default path`

## 何が進んだか

### 1. 初期 `comments` artifact 注入

`WorkflowEngine` が `config["input"]` から入力 CSV を初期 artifact として seed するようになり、workflow 先頭の `analysis.extraction` plugin が `inputs=["comments"]` を満たせる方向へ進んだ。[[source-code]]より

### 2. `without_html` / `without-html` の整合

legacy 初期化と workflow 条件判定の key drift を吸収する変更が入り、visualization step の gating が両 naming 変種に対して安定化した。[[source-code]]より

### 3. visualization plugin の `report.html` 契約化

builtin `analysis.hierarchical_visualization` plugin が、旧来の `index.html` ではなく current CLI の self-contained `report.html` 契約に揃えられた。[[source-code]]より

### 4. workflow path での status 永続化

`PipelineOrchestrator.run_workflow()` が `hierarchical_status.json` に `status`, `current_job`, `completed_jobs`, token usage を書くようになり、legacy `.run()` の責務の一部を吸収し始めた。[[source-code]]より

### 5. rerun plan と既存成果物の再利用

`from_dict()` でも既存 `hierarchical_status.json` を読んで `previous` / plan を作り、workflow engine 側でも既存 `args.csv`, `embeddings.pkl`, `hierarchical_result.json`, `report.html` などを初期 artifact として見えるようにしている。さらに plan に基づいて workflow step を skip する経路が入った。[[source-code]]より

### 6. flag 同期と callback 契約の補強

`without_html` / `without-html` の同期は helper に寄せられ、競合時は legacy key を正として deterministic に揃えるようになった。さらに optional step が例外で失敗した場合でも `on_step_complete` を必ず呼ぶようになり、workflow status 更新側が completion event を取りこぼしにくくなった。visualization plugin では `report_html_title` / `report_url_pattern` の forward も補強された。[[source-code]]より

### 7. CLI の default path 切替

`analysis_core.__main__` は branch 上で `orchestrator.run_default()` を呼ぶようになり、その実体は `run_workflow()` に向く。`PipelineResult.steps` も legacy step 名 (`hierarchical_visualization` など) で返すように寄せられており、CLI の表示契約を大きく壊さずに workflow path を主経路へ動かし始めている。[[source-code]]より

### 8. API launcher の command 共通化

`apps/api/src/services/report_launcher.py` では `python -m analysis_core ... --without-html` の command 組み立てが helper に寄せられ、通常実行・config 再実行・aggregation-only 実行の 3 経路で同じ CLI 契約を使うようになった。これは workflow defaultization 後も API 側の起動条件を 1 箇所で維持しやすくする補助変更である。[[source-code]]より

### 9. CLI / API の service-level 確認が増えた

その後の commit では、入口が本当に workflow default path の rerun / status 更新へつながるかを test で補強している。[[source-code]]より

- `bfda3dd`, `7167cf4` で e2e の plan scope helper と `from_dict()` の explicit plan 保持を揃え、部分実行指定が workflow path でも実際に効くようにした
- `142a63f` で CLI `main()` を直接通し、前回 status を読んで `skip_steps={"extraction"}` が workflow engine に渡ることと、`previously_completed_jobs` への carry-forward を確認した
- `b6310cd`, `fe5eda5`, `2c8632b`, `b869324` で API `report_launcher` の success path / aggregation rerun path / full report generation path を service-level で検証し、workflow の `hierarchical_status.json` から token usage を読み、`report_status.json` を壊さず `ready` と sync 更新へ進むことを確認した

### 10. failure semantics と duplicate/reuse rerun の確認が増えた

さらに後続 commit で、単に成功系が通るだけでなく、legacy path が担っていた rerun / error semantics にどこまで寄ったかを追加で確認している。[[source-code]]より

- `3737642` で workflow failure 時の `hierarchical_status.json` に、generic な `"Workflow execution failed"` ではなく failed step の具体的 error を残し、`current_job` と `error_stack_trace` も legacy に近い形で保持するようにした
- `1e3ec9e` で API `launch_report_generation_from_config()` の rerun success path を service-level で検証し、既存 report status を壊さず `ready` / token usage / sync 更新へ進むことを確認した
- `6f940fc` で duplicate/reuse 経路が source 側の workflow artifacts と `hierarchical_status.json` を新 slug に引き継ぎ、`launch_report_generation_from_config()` へ渡ることを確認した
- `d43a07b` で CLI 入口から duplicate/reuse 相当の rerun plan を通し、`overview` と `aggregation` だけが再実行される skip set を確認した
- `b163ba2` で `from_config()` が実ファイル群付きの duplicate/reuse 状態を読み、missing downstream artifact から rerun plan を組む integration test を追加した
- `2565b07` で real LLM call を使う e2e 群にも rerun scenario を追加し、前回 status と既存 artifact を置いた状態から late-stage rerun が通ることを検証し始めた
- `8e54904` で API `/admin/reports/{slug}/status/step-json` が workflow failure 時の `current_job`, token usage, provider/model をそのまま返せることを確認し、failure semantics が UI/API まで伝播することを押さえた

### 11. pre-push hook blocker は別 PR に切り出された

workflow defaultization branch の push を止めていた legacy `apps/api/broadlistening/pipeline/steps/` の Ruff import 並びは、本筋ではないため open PR `#841` (`[codex] legacy API step imports を Ruff に合わせる`) に切り出された。hook と同じ `cd apps/api && rye run ruff check . && rye run ruff format . --check` を通すための最小修正である。[[github-dev-docs]]より [[source-code]]より

### 12. merge 後に stale になる refactoring docs も先行更新された

`04a8e97` では `docs/refactoring/phase2_5_plan.md`, `docs/refactoring/phase3_plan.md`, `apps/api/broadlistening/README.md` の文面が current branch state に合わせて更新され、`branch 上では` のような暫定表現を消し、`run_default()` → `run_workflow()` を canonical path として読めるように寄せた。  
これにより docs drift は「workflow default 化前提の説明が散在」から「大半の主要 docs は更新済み」へ前進した。[[source-code]]より

## まだ残っていること

- success path, failure path, duplicate/reuse rerun plan に加え real LLM call を使う rerun e2e も入り始めたが、production 相当の実データ寄り証拠としてはまだ十分厚いとは言い切れない
- `apps/api` は `analysis-core` CLI を叩くため branch 上では実質 workflow path に寄るが、`--without-html` 固定など API 独自の運用前提はなお残る
- repo 内 docs の大半は current workflow canonical path に寄ったが、なお細部の stale 説明が残る可能性はある
- CodeRabbit は 2026-05-20 時点で rate limit / auto-pause に入った時間帯があり、最新 commit 群への bot review は間を空けて扱う必要がある

## 含意

- `refactoring-status` を main だけで読むと Phase 3b は dormant のままだが、**open PR まで含めて読むと「CLI default path を workflow へ寄せる active work」へ移っている**
- 一方で、まだ merged ではない以上、wiki 上の canonical current state は main と open PR を分けて書く方が誤読が少ない

## Updates

- 2026-05-20: 初回作成。draft PR #840 の 3 commit と review 状態を観測
- 2026-05-20: 追加 3 commit (`cc17509`, `24e02cc`, `ec694b7`) を反映し、CLI default path 切替と API launcher 共通化まで進んだと追記
- 2026-05-20: 追加 7 commit (`bfda3dd`, `7167cf4`, `b6310cd`, `fe5eda5`, `2c8632b`, `b869324`, `142a63f`) を反映し、CLI/API の service-level 証拠が増えたことと、hook blocker が PR `#841` に切り出されたことを追記
- 2026-05-20: 追加 5 commit (`3737642`, `1e3ec9e`, `6f940fc`, `d43a07b`, `b163ba2`) を反映し、failure semantics と duplicate/reuse rerun plan の確認がさらに進んだことを追記
- 2026-05-21: 追加 2 commit (`2565b07`, `8e54904`) を反映し、real workflow rerun e2e と workflow failure step status API の確認まで進んだと追記
- 2026-05-21: 追加 1 commit (`04a8e97`) を反映し、refactoring docs と deprecated README も merge 後前提の canonical path へ更新されたと追記
