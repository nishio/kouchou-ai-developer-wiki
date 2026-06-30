---
type: analysis
summary: "PR #903 の Web UI Node runtime inventory docs を、current main と CodeRabbit 指摘から読むレビュー観点。人間 authored PR へ直接 push せず、docs 精度の確認材料として固定する"
sources:
  - source-code.md
  - github-dev-docs.md
  - current-status-2026-06-30.md
  - node-runtime-free-windows-exe-2026-05-31.md
  - wiki-driven-workflow.md
  - pr-903-review-comment-draft-2026-06-30.md
---

## Snapshot

PR #903 (`docs: Web UI の Node runtime 依存インベントリを追加 (#885)`) は、`docs/development/web-ui-node-runtime-dependencies.md` を 1 ファイル追加する docs PR。2026-06-30 確認時点では non-draft、review required、merge state blocked。checks は docs build と CodeRabbit が通っているが、CodeRabbit は actionable 1 件と nitpick 2 件を出している。[[current-status-2026-06-30]]より

この PR は human authored なので、AI エージェントが勝手に branch へ push するより、まず review / docs 精度の観点を Wiki に固定する方が衝突しにくい。[[wiki-driven-workflow]]より

## Confirmed Points

CodeRabbit の actionable は、`apps/static-site-builder/package.json` の `dev` script が `src/server.ts` を参照しているが、current main の実体は `src/index.ts` だけである、という指摘。`work/kouchou-ai/main@d5c9ece` でも `dev: ts-node-dev ... src/server.ts` と `src/index.ts` の不一致を確認できる。[[source-code]]より

CodeRabbit の nitpick は、(1) docs が `d5c9ece` の行番号付き実装観察に依存しているため、last verified date / commit を目立つ場所に置くこと、(2) Server Actions の difficulty map が `createReport` を含まず、count と詳細表の対応が崩れていること。どちらも docs-only の小修正で、PR の設計方針を変えない。

追加で current main を見ると、PR #903 の Server Actions 表には `ActionMenu` の CSV / JSON download 系が載っていない。少なくとも `apps/admin/app/_components/ReportCard/ActionMenu/csvDownloadCommon.ts` と `jsonDownload.ts` は `"use server"` で、client action menu から呼ばれ、API から取った CSV / JSON を `Buffer.from(...).toString("base64")` で返している。これは Node runtime inventory の対象に入れるか、対象外なら対象外理由を docs に書いた方がよい。[[source-code]]より

一方、`apps/admin/app/create/api/spreadsheet.ts` は `export async function` を持つが、ファイル先頭に `"use server"` はない。`useInputData` から使われる client-side API helper として読む方が自然で、Server Actions count に混ぜない方がよい。[[source-code]]より

## Reading

PR #903 は `#885` の「Node runtime を外す前の棚卸し」として有用だが、merge するなら「本当に inventory と言える粒度か」を少しだけ締めた方がよい。特に static-site-builder の dev script 指摘は軽微だが、CSV / JSON download server actions の漏れは `admin` の export 化方針に影響しうる。

ただし、この PR の価値は「完璧な移行計画」ではなく、Node runtime 依存をコード位置に落として見える化することにある。したがって次に入れるべき修正は、実装ではなく docs の検証日・count 整合・漏れた server action の追記に絞るのが妥当。

## Safe Next Steps

- PR #903 の作者 / assignee を尊重し、AI から勝手に branch push しない。
- 人間が対応するなら、[[pr-903-review-comment-draft-2026-06-30]] のコメント案を使い、CodeRabbit 3 点に加え、CSV / JSON download server actions を inventory に入れるか対象外理由を追記する。
- AI が対応する場合も、まず「docs-only で小さく直してよいか」を確認してから、PR branch ではなく必要なら別 PR / コメント案で進める。

## Open Questions

- `#885` の完了条件として、admin の `"use server"` action は全件 inventory する必要があるのか、それとも Node runtime 排除の blocker になるものだけでよいのか。
- CSV / JSON download は client fetch + Blob で置き換える方が自然か、Windows Excel BOM 対応や filename handling のために別 route / API helper を残すべきか。

## Updates

- 2026-06-30: 初回作成。PR #903 metadata、CodeRabbit 指摘、`work/kouchou-ai/main@d5c9ece` の static-site-builder / admin server actions を確認した。
- 2026-06-30: [[pr-903-review-comment-draft-2026-06-30]] を追加し、PR に直接投稿せず、last verified / count 整合 / static-site-builder dev script / CSV・JSON download actions の 4 点を短く伝えるコメント案として固定した。
