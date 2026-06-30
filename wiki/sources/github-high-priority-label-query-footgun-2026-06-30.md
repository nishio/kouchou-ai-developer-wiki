---
type: source
summary: "GitHub issue の高優先度 label は `high priority` が正で、`priority: high` ではない。label 名を間違えると open high priority issue が 0 件に見える"
last_checked: 2026-06-30 19:30 JST
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues
  - github-dev-docs.md
---

## What it is

2026-06-30 19:30 JST に GitHub live state を再確認した際、`gh issue list --label "priority: high"` は 0 件を返した。一方で、#884 / #564 / #221 を個別に `gh issue view` すると、いずれも open で `high priority` label が付いていた。正しい label 名は **`high priority`** である。[[github-dev-docs]]より

この source は issue 状態の変化ではなく、観測コマンドの footgun を残すためのメモである。

## Correct Query

高優先度 open issue を見る時は、次を使う。

```bash
gh issue list -R digitaldemocracy2030/kouchou-ai --state open --label "high priority" --json number,title,assignees,labels,updatedAt --limit 20
```

2026-06-30 19:30 JST の結果は #884 / #564 / #221 の 3 件で、いずれも unassigned だった。[[github-dev-docs]]より

`priority: high` という label 名は存在しないため、次のような query は 0 件を返し、あたかも high priority issue が消えたように見える。

```bash
gh issue list -R digitaldemocracy2030/kouchou-ai --state open --label "priority: high"
```

## Implication

GitHub live state を wiki に反映する時は、label 名を自然言語で推測せず、既存 issue の `labels[].name` または GitHub の label list で exact name を確認する。特に `priority: high` / `high priority` のような言い換えは、current state の誤読に直結する。

## Open Questions

- `high priority` label の名称を repo 側で `priority: high` などの機械的に検索しやすい命名へ変えるか。ただし既存 wiki / issue comment との互換があるため、現時点では観測コマンド側で正確に扱う。

## Updates

- 2026-06-30: 初回作成。`priority: high` query が 0 件を返した後、#884 / #564 / #221 の個別確認と `--label "high priority"` query で open high priority issue 3 件を再確認した。
