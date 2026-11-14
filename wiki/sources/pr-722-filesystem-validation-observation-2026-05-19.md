---
title: "PR #722 ファイルシステム実行 validation の観測 2026-05-19"
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

- current CLI には設定・入力・出力の検証経路が実装された。[#721](https://github.com/digitaldemocracy2030/kouchou-ai/issues/721) / [#722](https://github.com/digitaldemocracy2030/kouchou-ai/issues/722) の残要件のうち、既存の検証で満たせない部分を再起票するかは未決。
- current CLI には --validate-config / --validate-input、独立モジュール validate_output が実装された。残る検証要件は、この 3 経路で検出できない具体例を確認して切り分ける。

## Updates

- 2026-05-19: 初版作成

- 2026-11-07: Open Questions の現状を更新 — 「[#721](https://github.com/digitaldemocracy2030/kouchou-ai/issues/721)/[#722](https://github.com/digitaldemocracy2030/kouchou-ai/issues/722) の問題設定自体を、current analysis-core CLI 向けに読み替えて再起票する方がよいか」。設定・入力・出力の検証経路は実装済み。旧課題の残要件を再起票する必要があるかは未決。（根拠: kouchou-ai upstream/main@085366779（2026-10-29） packages/analysis-core/src/analysis_core/__main__.py:79；kouchou-ai upstream/main@085366779（2026-10-29） packages/analysis-core/src/analysis_core/validate_output.py:1）。
- 2026-11-07: Open Questions の現状を更新 — 「input/config/output validation のうち、current CLI にまだ欠けているものは何か」。config/inputの専用フラグ、outputの専用モジュールが実装された。全種類の妥当性を保証したという意味ではない。（根拠: kouchou-ai upstream/main@085366779（2026-10-29） packages/analysis-core/src/analysis_core/__main__.py:79；kouchou-ai upstream/main@085366779（2026-10-29） packages/analysis-core/src/analysis_core/validate_output.py:1）。
