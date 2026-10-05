---
type: source
summary: "2026-10-05 の会話で、直前の作業が国内 broad listening 事例と TTTC→広聴AI lineage の wiki filing-back だったと復元したメモ"
last_checked: 2026-10-05 11:00 JST
coverage: "current conversation recall plus existing wiki pages; no new external source observation"
sources:
  - public-web-kouchouai-tttc-lineage-2026-06-30.md
  - japan-broadlistening-use-case-map-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - current-status-2026-10-05.md
  - meeting-report-draft.md
---

## What it is

2026-10-05 にユーザーから「これ何してたんだっけ」「file back」と言われたため、直前セッションの再開文脈を短く固定する。

直前の完了作業は、2026-06-30 の国内 broad listening / 広聴AI / Talk to the City 事例調査の続きで、最終 commit は `ef430b3 docs: file back kouchou ai tttc lineage` だった。新規実装ではなく、LLM Wiki / docs 更新中心の作業である。[[public-web-kouchouai-tttc-lineage-2026-06-30]]より

## Recalled Context

その時点で進んだ理解は、公開事例を「広聴AI confirmed case」として一括りにせず、少なくとも次へ分ける必要がある、というものだった。

| bucket | handling |
|---|---|
| 広聴AI confirmed | DD2030 / 自治体 / public viewer / public artifact で広聴AIまたは kouchou-ai を確認できるもの |
| TTTC direct / pre-kouchou lineage | 東京都知事選 2024、M-1、NTV 衆院選報道など。広聴AI導入実績とは分ける |
| broad listening adjacent | 大阪府、いどばた系 platform、政党 AI、AI 支援住民対話など。広聴AI単体ではなく広義の実践として扱う |
| enterprise / VOC / civic discussion | サイボウズ、アルティウスリンクなど。自治体向け first demo とは分ける |
| critique / scope guardrail | 事例数や可視化そのものではなく、どの insight type を得たいのか、政策反映までの end-to-end を見る |

この分類は、[[japan-broadlistening-use-case-map-2026-06-30]] と [[public-web-kouchouai-tttc-lineage-2026-06-30]] に固定済み。

## Next Natural Action

当時の自然な次の一手は、#564 の公開事例ページに移すための **最小 schema / 掲載候補リスト / 読み方ガイド** を固めることだった。これは単なるリンク集ではなく、`source_strength`、`tool_lineage`、`public risk`、`レポートの読み方`、`何を保証しないか` を同じ first slice に入れる話である。[[public-case-page-skeleton-2026-06-30]]より

ただし、2026-10-05 時点では current state が更新されている。現在地は [[current-status-2026-10-05]] を先に読み、6/30 の open PR / issue 観測や 8/2 向けの表現をそのまま現在へ持ち越さない。10/5 時点の high priority は #564 / #221、本体は6PRレビュー待ち、Serverless改善5PRはmain済みである。[[current-status-2026-10-05]]より

## Open Questions

- #564 の公開事例ページは DD2030 website の `kouchou-ai/case` に first slice として入れるか、別の tagged / cross-product case-news list を待つか。
- TTTC direct / pre-kouchou lineage を公開ページに載せる場合、広聴AI confirmed case と同じ一覧に置くか、history / adjacent section に分けるか。
- 10/5 時点の #564 / #221 / #921 の優先順位に、この 6/30 事例整理をどう接続するか。

## Updates

- 2026-10-05 11:00 JST: 初回作成。会話上の「何をしていたか」の復元を、既存 wiki source と 10/5 current state に接続して保存した。
