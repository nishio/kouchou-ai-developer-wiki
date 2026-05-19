---
type: analysis
summary: `PR #722` は validation 強化の意図自体は理解できるが、2026-05-19 時点では deprecated shim を増築する stale patch なので、そのまま merge すべきではない
sources:
  - pr-722-filesystem-validation-observation-2026-05-19.md
  - source-code.md
---

2026-05-19 時点の判断は、`PR #722` に対して **merge ではなく close + current 実装への再設計** が妥当。validation とファイルシステム実行の UX を良くしたいという狙いは分かるが、着地点が current `main` の canonical 経路から外れている。[[pr-722-filesystem-validation-observation-2026-05-19]]より

## Findings

### 1. 変更先が current の canonical 実装ではなく、deprecated shim になっている

`PR #722` は `server/broadlistening/pipeline/hierarchical_main.py` を主対象にしているが、current `main` で利用者に案内されているのは `packages/analysis-core/src/analysis_core/__main__.py` の `python -m analysis_core` / `kouchou-analyze` である。旧 `apps/api/broadlistening/pipeline/hierarchical_main.py` は deprecation notice 付きの shim として整理済みなので、そこへ新機能と大量ドキュメントを積むと、保守対象を誤認させる。これは設計レベルで `P1`。[[source-code]]より

### 2. ドキュメントが current 利用者を stale path へ誘導する

新規 `FILESYSTEM_USAGE.md` は「API サーバを起動せずに `hierarchical_main.py` を直接実行する」ことを推奨している。しかし current の canonical CLI はすでに `analysis-core` 側へ移っており、wiki でも旧経路は「動くが deprecated」と整理している。いまこの doc を merge すると、「正しい使い方の明確化」ではなく「古い使い方の再公式化」になる。[[pr-722-filesystem-validation-observation-2026-05-19]]より

### 3. 実装の一部は current 系ですでに別形で存在し、PR の価値がそのままでは移植されない

`PR #722` が追加する `--dry-run` は、current `analysis-core` CLI には既に実装済み。逆に current CLI が持つ `--output-dir` / `--input-dir` などは PR 側 doc に反映されていない。つまり「validation 追加」という核を除くと、提案内容の一部は陳腐化しており、差分全体をそのまま revive する価値は低い。必要なのは patch の救済ではなく、current CLI を前提にした要求の再分解。[[source-code]]より

## Recommendation

- 現時点の判定は `do not merge`
- `#721/#722` は旧パス前提の作業として閉じ、必要なら current `analysis-core` 向けに新 issue を切り直す
- 継承すべきものは「validation needs」であって patch そのものではない
- 再設計するなら優先順位は `config` / `input` の事前 validation、current CLI doc 整備、必要なら output validation の順が自然

## Open Questions

- current `analysis-core` CLI に `--validate-config` / `--validate-input` を独立フラグとして入れるべきか、それとも `--dry-run` と `PipelineOrchestrator.from_config()` の初期化失敗で十分か
- validation の責務を CLI 本体に置くか、別 subcommand / 別 helper に切るか

## Updates

- 2026-05-19: 初版作成
