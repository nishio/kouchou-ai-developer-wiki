---
name: open-pr-observation-2026-05-18
summary: "2026-05-18 の open PR / review triage 実験で観測した head branch 更新挙動"
type: source
sources:
  - github-dev-docs.md
---

2026-05-18 に `digitaldemocracy2030/kouchou-ai` の open PR を観測し、未解決 review comment を整理したうえで review fix を push した時のメモ。

## 観測事項

- PR `#824`, `#825`, `#826` は、GitHub 上の PR metadata に出ている head branch が remote に実在し、その branch へ push すると PR head SHA も素直に更新された。[[github-dev-docs]]より
- PR `#794` は、PR metadata 上は head branch が `chore/plan-llm-grouping-capabilities` だったが、remote には同名 branch が存在しなかった。[[github-dev-docs]]より
- その状態で同名 branch を新規 push すると branch 自体は作られたが、既存 PR `#794` の head SHA は更新されなかった。通常の「既存 PR branch へ push すれば PR が更新される」前提が崩れた。[[github-dev-docs]]より
- 対処として旧 PR `#794` を close し、新しく PR `#827` を `chore/plan-llm-grouping-capabilities` から作り直した。[[github-dev-docs]]より

## 運用メモ

- open PR を「存在する作業」として数えるだけでなく、**head branch 名と remote branch 実体が一致しているか** まで確認した方がよい。[[github-dev-docs]]より
- stale な PR を review だけ追いかけても branch 側が壊れていれば update できない。PR metadata と remote branch の不整合が見えた時点で、close + recreate を検討した方が早い。[[github-dev-docs]]より

## Open Questions

- GitHub 上で「PR metadata は branch 名を保持しているが remote branch 実体は消えている」状態がどの操作で発生したかは不明。

## Updates

- 2026-05-18: 初回作成
