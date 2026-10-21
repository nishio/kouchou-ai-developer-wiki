---
title: "nishio 以外の人間 PR の状況"
type: analysis
summary: "nishio 以外の人間が author の PR の状況。2026-05-18 の open PR 整理で古い draft 3 本（#597 / #734 / #735）を close し、#817 は同日 merge。その後 2026-10-21 までに 5 人の PR 10 本が merge され、同日時点で nishio 以外の人間の open PR は 0 本"
sources:
  - open-pr-snapshot-2026-05-18.md
  - open-pr-observation-2026-05-18.md
  - github-dev-docs.md
---

nishio 以外の人間が author の PR が、どう処理されてきたかの整理。2026-05-18 の open PR 整理（cleanup）の前、**nishio 以外の人間の open PR は `#597` / `#734` / `#735` / `#817` の 4 本** だった。古い draft 3 本は 2026-05-18〜19 に close し、`#817` は 2026-05-18 の夜に merge したので、2026-05-19 未明（JST）には 0 本になった。その後も 5 人が PR を出し、**2026-10-21 時点で 10 本が merge 済み、open は 0 本** である。最新の状態は `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` で確かめる。[[open-pr-snapshot-2026-05-18]]より [[github-dev-docs]]より

## 2026-05-18 の cleanup

### cleanup 前の open PR は 4 本だった

[[open-pr-snapshot-2026-05-18]] は open PR の「主な番号」だけを挙げていて `#735` と `#817` が抜けており、nishio 以外の人間の open PR を「`#734` と `#597` の 2 本だけ」と書いている。GitHub の作成・close 日時で数え直すと、cleanup 前に open だったのは `#597`（dentaro）・`#734`（Devesh36）・`#735`（Devesh36）・`#817`（shingo-ohki）の 4 本だった。[[github-dev-docs]]より

### `PR #734` は revive コストが高そうな stale draft だった

`PR #734` は `Devesh36` authored の Biome 導入 PR。2025-12-04 作成、最終更新は 2025-12-07 で止まっており、2026-05-18 cleanup 前時点でも draft のまま `mergeable: false` だった。body では `client/`, `client-admin/`, `client-build/` を前提にしており、当時の active PR 群（`#824` `#825` `#826` `#828`）と比べても時間差が大きかった。そのため stale と判断して 2026-05-18 に close した。[[open-pr-snapshot-2026-05-18]]より

### `PR #597` はさらに古い UI 系 draft で、open のまま凍っていた

`PR #597` は `dentaro` authored の scatter chart スクロール誤操作回避 PR。2025-06-09 作成、2025-10-01 更新以降止まっており、これも draft かつ `mergeable: false` だった。レビュー依頼は残っていたが、review queue に乗っているというより **historical residue** に近かったため、2026-05-18 に close した。[[open-pr-snapshot-2026-05-18]]より

### `PR #735` は current tree での作り直しに回した

`PR #735` は `Devesh36` authored の CSP header 追加 draft（2025-12 作成）。変更先が旧 `client/` / `client-admin/` tree で、conflict と CI failure も抱えていた。扱っていた問題自体は有効なので、merge ではなく現行 `apps/*` での作り直し（Issue [#833](https://github.com/digitaldemocracy2030/kouchou-ai/issues/833)）に回し、2026-05-19 00:55（JST）に close した。判断の詳細は [[pr-735-merge-assessment]]。[[github-dev-docs]]より

### `PR #817` は同日夜に merge した

`shingo-ohki` の `#817` は 2026-03-10 作成の non-draft / `mergeable: true` の PR で、内容は CodeQL / CodeRabbit 設定の調整。stale draft ではなく current open work として扱い、2026-05-18 22:57（JST）に merge した。設定は main の `.github/workflows/codeql.yml` と `.coderabbit.yaml` に残っている（[[security-maintenance]]）。[[github-dev-docs]]より

### `tokoroten` の PR は 2026-05-18 時点で open ではなかったが、2026-02〜03 に複数 merged している

[[tokoroten]] authored の recent PR としては `#812`（散布図ホバー時のクラスタラベル非表示）、`#811`（属性フィルタロジック統合と stale closure 修正）、`#807`（Docker image 大幅縮小）があり、いずれも 2026-02〜03 に merged 済み。したがって「tokoroten の新しい PR が無かった」わけではなく、**open に残っていなかっただけ**。[[open-pr-snapshot-2026-05-18]]より

## その後の PR（2026-10-21 時点）

2026-05-18 以降に nishio 以外の人間が出した PR は次のとおり。[[github-dev-docs]]より

| author | PR | 結果 |
|---|---|---|
| 101ta28 | [#887](https://github.com/digitaldemocracy2030/kouchou-ai/issues/887)（Plotly scattergl の CSP 修正）、[#897](https://github.com/digitaldemocracy2030/kouchou-ai/issues/897)（混在型の入力 CSV 属性を文字列として扱う） | どちらも merge |
| yasumorishima | [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) / [#935](https://github.com/digitaldemocracy2030/kouchou-ai/issues/935) / [#936](https://github.com/digitaldemocracy2030/kouchou-ai/issues/936)（[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) 関連。Web UI の Node runtime 依存の棚卸し、データ非依存の静的出力、OGP の docs 訂正） | すべて merge |
| tokoroten | [#934](https://github.com/digitaldemocracy2030/kouchou-ai/issues/934)（OpenAI Flex Processing の修正） | merge |
| tokoroten | [#891](https://github.com/digitaldemocracy2030/kouchou-ai/issues/891)（Windows スタンドアロン版の試作 draft） | 2026-10-13 に作者が merge せず close |
| katsushi2441 | [#952](https://github.com/digitaldemocracy2030/kouchou-ai/issues/952)（Ollama のホスト側ポートを変更可能に）、[#959](https://github.com/digitaldemocracy2030/kouchou-ai/issues/959)（韓国語版 README） | どちらも merge |
| shingo-ohki | [#968](https://github.com/digitaldemocracy2030/kouchou-ai/issues/968)（日本語 README を既定に戻す）、[#1014](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1014)（公開処理と定期 E2E テストを本家リポジトリに限定） | どちらも merge |

5 人の 10 本が merge され、2026-10-21 時点で nishio 以外の人間の open PR は 0 本（open は nishio の [#1024](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1024) / [#1025](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1025) だけ）。

## Practical Read

- 2026-05-18 の cleanup で、nishio 以外の人間の open PR は 0 本になった（古い draft 3 本は close、`#817` は merge）
- その後も nishio 以外からの PR は続いており、2026-10-21 時点で 5 人の 10 本が merge 済み
- `tokoroten` の 2026-02〜03 の work も、open ではなく merged 側に並んでいる

## Open Questions

- `#817` の CodeQL / CodeRabbit 設定調整をこのまま取り込むか、それとも current security / review policy に合わせて再整理するか → そのまま 2026-05-18 に merge した。設定は main に残っている（[[security-maintenance]]）
- `#597` が扱っていたスクロール誤操作 UX は、現行 `public-viewer` / chart 実装でもまだ課題として残るのか → 残っている。2026-10-21 時点で Issue [#493](https://github.com/digitaldemocracy2030/kouchou-ai/issues/493) は open で、`apps/public-viewer/components/charts/ScatterChart.tsx` は `scrollZoom: true` のまま。UX 判断の材料は [[chart-scroll-ux-decision]]

## Updates

- 2026-05-18: 初版作成
- 2026-05-18: `#734` `#597` close 後の current state に合わせて更新し、`tokoroten` / `ohki` の recent PR 事情を追記
- 2026-10-21: GitHub と照合し、cleanup 前の open PR に抜けていた [#735](https://github.com/digitaldemocracy2030/kouchou-ai/issues/735) を補って 4 本に訂正。[#817](https://github.com/digitaldemocracy2030/kouchou-ai/issues/817) の merge、その後の nishio 以外の PR（5 人・10 本が merge、[#891](https://github.com/digitaldemocracy2030/kouchou-ai/issues/891) は close）と open 0 本を追記し、Open Questions に結論を書き足した
