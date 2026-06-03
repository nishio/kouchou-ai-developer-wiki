---
type: source
summary: "Codex が既存 LLM grouping 400 件 corpus から blind A/B label preference bundle を生成した作業ログ。`hierarchical_8_40` tree を固定し、`none` vs `setwise` の label variants を 24 questions にして `human_preference_questions.jsonl` と Markdown / HTML bundle を作った"
sources:
  - label-quality-human-preference-improvement-plan-2026-06-03.md
  - llm-grouping-400-tree-label-corpus-2026-06-02.md
---

## Context

2026-06-03、[[label-quality-human-preference-improvement-plan-2026-06-03]] の first implementation slice として、既存 LLM grouping 400 件 corpus から blind A/B label preference bundle を生成した。

実装は developer-wiki の `scripts/build_label_preference_bundle.py`。これは kouchou-ai 本体の product code ではなく、gitignored raw experiment corpus から human preference collection 用 artifact を作る wiki 運用スクリプトである。

## What Ran

対象 corpus:

```text
raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/
```

固定したもの:

- dataset: LLM grouping 400 件 corpus
- tree: `tree:hierarchical_8_40`
- comparison unit: top-level 8 clusters
- presentation contexts: `label_only`, `sibling_label_set`, `label_with_representatives`

比較した label variants:

- `labelling:hierarchical_8_40_refine_none`
- `labelling:hierarchical_8_40_refine_setwise`

生成された raw artifact:

```text
raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/human_preference_questions.jsonl
raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/human_preferences.jsonl
raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/human_preferences.schema.json
raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/bundles/label_preference_ab.md
raw/experiments/2026-06-02-llm-grouping-400-tree-label-corpus/bundles/label_preference_ab.html
```

`manifest.json` には `human_preference_questions: 24` と `human_preferences: 0` を追記した。

## Records

生成した questions は 24 件。

| dimension | count |
|---|---:|
| top-level clusters | 8 |
| presentation contexts | 3 |
| total questions | 24 |

各 question は pending 状態で、まだ人間の回答は入っていない。`human_preferences.jsonl` は回答保存用の空ファイルとして作成した。

## Blindness Check

表示用 bundle (`label_preference_ab.md` / `.html`) には `labelling_run_id`、`refine_none`、`setwise` などの candidate origin を出していない。origin は `human_preference_questions.jsonl` の hidden metadata 側だけに残している。

A/B の表示順は deterministic seed `20260603` で randomize した。24 questions の内訳は、`setwise -> none` が 14 件、`none -> setwise` が 10 件だった。

## Caveat

`label_with_representatives` の example arguments は、既存 `hierarchical_clusters.csv` の各 top-level cluster から先頭 3 件を取ったもので、設計済み representative artifact ではない。metadata には `example_arguments_source = first_rows_from_hierarchical_clusters_csv; not a calibrated representative artifact` と明記した。

したがって、この bundle は「代表例 selection の完成版」ではなく、human preference collection の first slice である。representative artifact 自体の改善は別の clean experiment として扱う。

## Validation

- `python3 scripts/build_label_preference_bundle.py` で 24 questions と bundle を生成
- `python3 -m py_compile scripts/build_label_preference_bundle.py` 通過
- `python3 -m ruff check scripts/build_label_preference_bundle.py` 通過
- Playwright / Chromium を一時環境 `/tmp/codex-playwright` に入れ、生成済み HTML を開いて `winner` / `confidence` / `reason_tags` / `free_text` / `evaluator_id` の入力が JSONL textarea に反映されることを確認
- bundle 表示に candidate origin が出ていないことを `rg` で確認
- `human_preference_questions.jsonl` の contexts は `label_only`, `sibling_label_set`, `label_with_representatives`
- `algorithm_origin_visible` は全件 `false`

## Open Questions

- HTML の回答入力フォームは追加済みだが、複数 evaluator の回答をどう識別・merge するか。
- `label_with_representatives` は先頭 3 件ではなく、代表例 artifact ができてから再生成すべきか。
- comparison target を `none` vs `setwise` だけでなく、`short` / `contrast` / `balanced` へ広げるか。

## Updates

- 2026-06-03: `label_preference_ab.html` に winner / confidence / reason tags / free text の入力フォームと、完成済み回答を JSONL として出す textarea を追加。`evaluator_id` は任意入力にした。由来情報は引き続き表示 HTML に出していない。
- 2026-06-03: Playwright で HTML を実操作し、1 件の completed answer だけが JSONL に出力され、winner だけ選んだ incomplete answer は出力されないことを確認した。
- 2026-06-03: 初版作成。
