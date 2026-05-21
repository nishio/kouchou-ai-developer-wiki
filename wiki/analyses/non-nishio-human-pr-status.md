---
type: analysis
summary: "2026-05-18 の stale cleanup 後、nishio 以外の人間 authored open PR は `shingo-ohki` の `#817` だけで、古い draft `#734` と `#597` は close 済み"
sources:
  - open-pr-snapshot-2026-05-18.md
  - open-pr-observation-2026-05-18.md
---

2026-05-18 の open PR cleanup 前 snapshot では、**nishio 以外の人間が author の open PR は `#734` と `#597` の 2 本だけ** だった。しかも両方とも 2025 年の draft で、`mergeable: false`、更新も止まっていた。その後、同日中に stale 理由を添えて 2 本とも close したため、cleanup 後の current state では **non-nishio human authored open PR は `shingo-ohki` の `#817` だけ** になった。[[open-pr-snapshot-2026-05-18]]より

## Findings

### `PR #734` は revive コストが高そうな stale draftだった

`PR #734` は `Devesh36` authored の Biome 導入 PR。2025-12-04 作成、最終更新は 2025-12-07 で止まっており、2026-05-18 cleanup 前時点でも draft のまま `mergeable: false` だった。body では `client/`, `client-admin/`, `client-build/` を前提にしており、現行の active PR 群（`#824` `#825` `#826` `#828`）と比べても時間差が大きかった。そのため stale と判断して close した。[[open-pr-snapshot-2026-05-18]]より

### `PR #597` はさらに古い UI 系 draftで、open のまま凍っていた

`PR #597` は `dentaro` authored の scatter chart スクロール誤操作回避 PR。2025-06-09 作成、2025-10-01 更新以降止まっており、これも draft かつ `mergeable: false` だった。レビュー依頼は残っていたが、現状は review queue に乗っているというより **historical residue** に近かったため close した。[[open-pr-snapshot-2026-05-18]]より

### cleanup 後に残る human open PR は `shingo-ohki` の `#817`

cleanup 後に残る non-nishio human authored open PR は `shingo-ohki` の `#817` だけ。これは 2026-03-10 作成の non-draft / `mergeable: true` で、内容は CodeQL / CodeRabbit 設定の調整。`#734` や `#597` と違って stale draft ではなく、current open work として扱える。[[open-pr-snapshot-2026-05-18]]より

### `tokoroten` の最近の PR は open ではないが、2026-02〜03 に複数 merged している

[[tokoroten]] authored の recent PR としては `#812`（散布図ホバー時のクラスタラベル非表示）、`#811`（属性フィルタロジック統合と stale closure 修正）、`#807`（Docker image 大幅縮小）があり、いずれも 2026-02〜03 に merged 済み。したがって「tokoroten の新しい PR が無かった」わけではなく、**open に残っていないだけ**。[[open-pr-snapshot-2026-05-18]]より

## Practical Read

- cleanup 後の「nishio 以外の人間の open PR」は `#817` だけ
- `#734` `#597` は stale draft として close し、open 一覧のノイズを減らした
- `tokoroten` の recent work は open ではなく merged 側に並んでいる

## Open Questions

- `#817` の CodeQL / CodeRabbit 設定調整をこのまま取り込むか、それとも current security / review policy に合わせて再整理するか
- `#597` が扱っていたスクロール誤操作 UX は、現行 `public-viewer` / chart 実装でもまだ課題として残るのか

## Updates

- 2026-05-18: 初版作成
- 2026-05-18: `#734` `#597` close 後の current state に合わせて更新し、`tokoroten` / `ohki` の recent PR 事情を追記
