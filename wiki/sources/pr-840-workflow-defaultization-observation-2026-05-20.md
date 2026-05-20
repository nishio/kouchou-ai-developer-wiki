---
type: source
summary: draft PR #840 は `run_workflow()` default 化に向けて、初期 artifact・status 永続化・rerun artifact 再利用までを段階的に進めている
sources:
  - source-code.md
  - github-dev-docs.md
---

# `PR #840` workflow defaultization 観測

2026-05-20 時点の open PR `#840` (`[codex] Start workflow defaultization groundwork`) を観測すると、Phase 3b は current `main` ではなお dormant だが、**open PR 上では blocker の一部が既に分割コミットで前進している**。[[github-dev-docs]]より [[source-code]]より

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

## まだ残っていること

- e2e test 群はまだ `.run()` 主経路のまま
- `apps/api` は `analysis-core` CLI を叩くため branch 上では実質 workflow path に寄るが、`--without-html` 固定など API 独自の運用前提はなお残る
- repo 内 docs には legacy mode 前提の説明がまだ散在する
- CodeRabbit は 2026-05-20 13:01 JST 時点で rate limit に到達しており、直近 commit 群への追加 review は一時保留状態

## 含意

- `refactoring-status` を main だけで読むと Phase 3b は dormant のままだが、**open PR まで含めて読むと「CLI default path を workflow へ寄せる active work」へ移っている**
- 一方で、まだ merged ではない以上、wiki 上の canonical current state は main と open PR を分けて書く方が誤読が少ない

## Updates

- 2026-05-20: 初回作成。draft PR #840 の 3 commit と review 状態を観測
- 2026-05-20: 追加 3 commit (`cc17509`, `24e02cc`, `ec694b7`) を反映し、CLI default path 切替と API launcher 共通化まで進んだと追記
