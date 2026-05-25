---
type: source
summary: "developer-wiki の graph 表示調整と main 直接 push 運用を 2026-05-25 の実作業から整理した観測メモ"
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-25 に `kouchou-ai-developer-wiki` 自体の Quartz 表示調整と push 運用を確認した観測メモ。対象は `nishio/kouchou-ai-developer-wiki` の `main` で、`kouchou-ai` 本体 repo ではない。

## Observations

- commit `e136cd4` (`Hide index and log from graph`) で、`quartz.layout.ts` の `Component.Graph()` に `localGraph` / `globalGraph` 共通で `removeSlugs: ["index", "log"]` を渡すようにした。[[source-code]]より
- `quartz/components/Graph.tsx` の `D3Config` と default options に `removeSlugs` を追加し、`quartz/components/scripts/graph.inline.ts` で `fetchData` 由来の graph node を描画前に slug filter するようにした。[[source-code]]より
- 意図は、`wiki/index.md` と `wiki/log.md` が知識生成の導線として重要すぎるため、graph 上で全体を吸い込みすぎる問題を避けること。ページ自体は公開されたままで、Explorer / wikilink / URL からは到達できる。[[source-code]]より
- 検証では `pnpm build` が `wiki/` 152 files を処理し、`public/` へ 322 files を出力して成功した。`scripts/lint_wiki.py` も壊れた wikilink / index 未登録 / frontmatter 不備 0 で通過した。[[source-code]]より
- 一方、通常の `pnpm check` は Node 既定ヒープで OOM し、`NODE_OPTIONS=--max-old-space-size=8192 pnpm check` でも `work/` 配下の local clone まで TypeScript が拾って大量の既存エラーを出した。現状の commit gate としては `pnpm build` の方が実使用経路に近い。[[source-code]]より

## Push observation

- 先行する wiki 更新 commit `4cd4775` (`Update wiki operation notes`) では、`git push origin main` が GitHub 側の `Internal Server Error` で 2 回拒否された。退避用 branch / draft PR を作ったが、Wiki 更新が PR 経由になる運用は望ましくないと判断された。[[github-dev-docs]]より
- `main` は protected ではなく、local `HEAD` は `origin/main` からの fast-forward だったため、`gh api -X PATCH repos/nishio/kouchou-ai-developer-wiki/git/refs/heads/main -F sha=<HEAD> -F force=false` で `refs/heads/main` を直接進めた。`force=false` により fast-forward でない更新は拒否される。[[github-dev-docs]]より
- 同じ commit が `main` に入ったため退避 PR は GitHub 上で `MERGED` 扱いになり、退避 branch `codex/wiki-operation-notes-20260525` は削除した。[[github-dev-docs]]より
- その後の `e136cd4` は通常の `git push origin main` で成功した。したがって、今後の wiki 更新は PR を作らず、まず direct push を試す。GitHub 側の transient error で direct push だけが落ち、かつ `main` が unprotected / fast-forward 可能な場合だけ、API fast-forward を fallback にする。[[github-dev-docs]]より

## Open Questions

- `pnpm check` が `work/` 配下 clone を拾う状態を、`tsconfig.json` の `exclude` で直すべきか。
- `tsconfig.tsbuildinfo` が検証時に生成されるため、ignore 対象にするべきか。
- `wiki/log.md` は graph から除外したが、公開ページとして残すか、より内部向け導線に寄せるか。

## Updates

- 2026-05-25: 初版作成
