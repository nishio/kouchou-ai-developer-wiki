---
type: analysis
summary: "PR #903 に直接投稿せず Wiki 側に固定したレビューコメント案。CodeRabbit 3 点に加え、CSV / JSON download server actions の inventory 漏れを短く伝え、human-authored docs PR への安全な next action にする"
sources:
  - pr-903-node-runtime-doc-review-2026-06-30.md
  - docs-issue-map-2026-06-30.md
  - node-runtime-free-windows-exe-2026-05-31.md
  - source-code.md
  - github-dev-docs.md
---

## 結論

PR #903 は human-authored の docs-only PR なので、AI が branch へ直接 push するより、レビューコメント案を Wiki 側に固定して、人間が投稿 / 修正判断できる状態にするのがよい。[[pr-903-node-runtime-doc-review-2026-06-30]]より

2026-06-30 14:01 JST に PR #903 を再確認した時点で、状態は open / non-draft / review required / merge state blocked、差分は `docs/development/web-ui-node-runtime-dependencies.md` 1 ファイル追加のままだった。CodeRabbit の指摘も、static-site-builder dev entrypoint、last verified note、Server Actions difficulty map の 3 点で前回から変化なし。[[github-dev-docs]]より

current main `d5c9ece` では、`apps/admin` の `"use server"` は 11 ファイルで、export 関数数としては PR #903 docs に載っている 15 action に加え、`csvDownloadCommon` と `jsonDownload` の 2 action がある。これらは `ActionMenu` から CSV / JSON download に使われ、`Buffer.from(...).toString("base64")` を返すため、Node runtime inventory に入れるか、対象外理由を書くのが自然である。[[source-code]]より

## Comment Draft

以下は、PR #903 に人間が投稿する場合の短いコメント案。

```markdown
docs-only の棚卸しとしてかなり有用だと思います。merge 前に、精度を上げるなら次の 4 点だけ見ればよさそうです。

1. CodeRabbit 指摘どおり、冒頭に `last verified: 2026-06-27 / d5c9ece` のような注記を置く
   この docs は current main の実装行に強く依存しているので、確認 commit と日付が見えると後から更新しやすいです。

2. Server Actions の count / difficulty map を揃える
   本文は 15 actions と書いていますが、difficulty map は `Server Action 14本（proxy）` + `duplicateReport` になっていて、`createReport` の扱いが読み取りにくいです。`createReport` を map に入れるか、除外理由を明記するとよさそうです。

3. `apps/static-site-builder/package.json` の `dev` script の扱いを決める
   docs 本文にも注がありますが、current main では `dev` script が `src/server.ts` を指す一方、実体は `src/index.ts` です。docs PR 内で直すか、少なくとも follow-up として明示しておくとよさそうです。

4. CSV / JSON download 系の server actions を inventory に入れるか、対象外理由を書く
   current main では `apps/admin/app/_components/ReportCard/ActionMenu/csvDownloadCommon.ts` と `jsonDownload.ts` が `"use server"` で、ActionMenu から呼ばれています。どちらも API から取った CSV / JSON を `Buffer.from(...).toString("base64")` で返しているので、Node runtime inventory としては漏れ候補に見えます。対象外なら、その理由を書いておくと後続の admin export 化で迷いにくいです。

上の 4 点以外は、この PR の目的である「#885 の第1完了条件として Node runtime 依存を見える化する」には十分前進していると思います。
```

## Why This Shape

このコメント案は、PR #903 を「完璧な移行設計」に引き上げるのではなく、inventory docs としての信頼性だけを締める。具体的には、次の 4 類型に絞っている。

- freshness: last verified commit / date
- internal consistency: Server Actions count と difficulty map
- obvious stale fact: static-site-builder dev script
- inventory completeness: CSV / JSON download server actions

`#885` の本丸は、admin の proxy 置換より static-site-builder の runtime build をどう外すかである。PR #903 はその前段の inventory なので、コメントも移行方針の拡張ではなく、後続 prototype の判断に効く docs 精度へ絞るのがよい。[[node-runtime-free-windows-exe-2026-05-31]]より

## Posting Boundary

AI はこのコメントをまだ GitHub に投稿しない。理由は、PR #903 は human authored であり、CLAUDE.md の運用方針では reviewer request、対人 escalation、human attention を使う操作は人間の明示指示がある時だけ実行するため。[[docs-issue-map-2026-06-30]]より

## Open Questions

- CSV / JSON download の `Buffer` 使用は Node runtime inventory の blocker として扱うか、client-side Blob download に自然に置き換わる軽微項目として扱うか。
- PR #903 にコメントだけ出すか、作者が望むなら docs-only follow-up PR に分けるか。
- static-site-builder `dev` script は docs PR #903 内で直すべきか、別 issue / PR の掃除として分けるべきか。

## Updates

- 2026-06-30: 初回作成。PR #903 live state、CodeRabbit 指摘、current main `d5c9ece` の `"use server"` ファイルと CSV / JSON download actions を再確認し、投稿前のレビューコメント案として固定した。
