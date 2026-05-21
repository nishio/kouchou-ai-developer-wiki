---
type: source
summary: "`PR #722` は 2025-10-23 作成の draft open PR で、ファイルシステム実行の文書化と validation を追加するが、2026-05-19 時点では deprecated な旧 `server/...` 経路を増築している"
sources:
  - github-dev-docs.md
  - source-code.md
---

2026-05-19 に `gh pr view 722 -R digitaldemocracy2030/kouchou-ai` と `gh pr diff 722 -R digitaldemocracy2030/kouchou-ai` を確認し、current `work/kouchou-ai/` の canonical 実装と照合した。`PR #722` は **2025-10-23 作成、2025-11-08 更新、draft のまま open、mergeable: CONFLICTING** と観測できた。[[github-dev-docs]]より

## Observations

- 変更対象は `server/broadlistening/...` と `server/tests/...` に集中している
- 追加内容は `FILESYSTEM_USAGE.md`、Pydantic schema、input/config/output validator、`hierarchical_main.py` への `--validate-*` と `--dry-run`、54 個のテスト
- PR 本文と issue `#721` は、`server/broadlistening/pipeline/hierarchical_main.py` を「API サーバなしで直接実行する既存エントリ」とみなして改善対象にしている
- しかし current `main` では `apps/api/broadlistening/pipeline/hierarchical_main.py` 冒頭に deprecation notice があり、利用者には `python -m analysis_core` / `kouchou-analyze` を使うよう案内している
- current `main` の canonical CLI は `packages/analysis-core/src/analysis_core/__main__.py` にあり、既に `--dry-run`, `--output-dir`, `--input-dir` を持つ
- wiki 既存整理でも、`apps/api/broadlistening/pipeline/` は deprecated shim、canonical 実装は `packages/analysis-core/` としている（[[refactoring-status]] 参照）
- `PR #722` の patch は旧 `server/` パス前提なので、current tree にはそのまま適用できない。実際、2026-05-19 時点の local clone へ `gh pr checkout 722` を試すと既存差分とは別に branch 自体が古く、checkout 前提からズレていることが分かる
- `server/broadlistening/pipeline/validators/*.py` は `sys.path.insert(...)` で import path を書き換えており、CodeRabbit でも相対 import へ直すべきという指摘が付いている
- `FILESYSTEM_USAGE.md` は旧 `hierarchical_main.py` を主経路として案内しており、current 利用者を stale path へ誘導する

## Open Questions

- `#721/#722` の問題設定自体を、current `analysis-core` CLI 向けに読み替えて再起票する方がよいか
- input/config/output validation のうち、current CLI にまだ欠けているものは何か

## Updates

- 2026-05-19: 初版作成
