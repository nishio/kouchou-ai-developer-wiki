---
type: source
summary: "2026-05-18 時点の `digitaldemocracy2030/kouchou-ai` open PR 一覧を、作者種別と stale 度合いを見るために取得したスナップショット"
sources:
  - github-dev-docs.md
---

2026-05-18 に GitHub 上の `digitaldemocracy2030/kouchou-ai` open PR を再取得し、`nishio` authored / bot authored / nishio 以外の人間 authored を切り分けるための観測メモ。live state なので、長期保存用の断定ではなく当日時点の snapshot として扱う。[[github-dev-docs]]より

## Findings

### open PR 全体（close 前 snapshot）

2026-05-18 時点で open PR として観測できた主な番号は `#828`, `#827`, `#826`, `#825`, `#824`, `#823`, `#734`, `#727`, `#722`, `#597`。このうち `#828` `#827` `#826` `#825` `#824` は [[nishio]] authored、`#823` `#727` `#722` は bot authored、**nishio 以外の人間 authored は `#734` と `#597` の 2 本だけ** だった。[[github-dev-docs]]より

### `PR #734` は Devesh36 authored の古い draft

- title: `feat: integrate Biome for linting and formatting`
- author: `Devesh36`
- state: `open`
- draft: `true`
- mergeable: `false`
- created_at: `2025-12-04T05:31:40Z`
- updated_at: `2025-12-07T06:02:37Z`

`client/`, `client-admin/`, `client-build/` のような旧構成を前提にした Biome 導入案で、2026-05-18 時点の active PR 群よりかなり古い。[[github-dev-docs]]より

### `PR #597` は dentaro authored の最古級 draft

- title: `Feature/issue 493 レポート画面のスクロールイベント回避を追加`
- author: `dentaro`
- state: `open`
- draft: `true`
- mergeable: `false`
- created_at: `2025-06-09T12:11:47Z`
- updated_at: `2025-10-01T11:22:01Z`

レポート画面のスクロール時誤操作を避ける UI 改修案。requested reviewer として `UtkNggc` が残っているが、長期間更新されていない。[[github-dev-docs]]より

### Devin / Dependabot PR は open だが「人間 authored」ではない

`#823` は `dependabot[bot]` authored、`#727` `#722` は `devin-ai-integration[bot]` authored。後者は body に `Requested by: NISHIO` とあるが、PR author としては bot なので、「nishio 以外の人間による PR」には数えない方が正確。[[github-dev-docs]]より

### 2026-05-18 の cleanup 後は non-nishio human open PR は 0 本

同日中に `#734` と `#597` へ stale 理由をコメントして close したため、**2026-05-18 cleanup 後の open PR で non-nishio human authored と言えるものは `#817` (`shingo-ohki`) だけになり、古い draft 2 本は open 一覧から消えた**。[[github-dev-docs]]より

### `tokoroten` / `ohki` の最近の PR は「ゼロ」ではない

- [[ohki-shingo]] (`shingo-ohki`): `PR #817` が 2026-03-10 作成の open PR として残っている。内容は CodeQL / CodeRabbit 設定の調整
- 同 author の `PR #808` は 2026-02-25 merged。`minimatch` の ReDoS 対応
- [[tokoroten]] (`tokoroten`): `PR #812`, `#811`, `#807` が 2026-02〜03 に merged。散布図ホバー改善、属性フィルタ整理、Docker image 縮小が主題

したがって、「tokoroten や ohki の新しい PR が無い」わけではなく、**tokoroten は recent merged 側、ohki は recent merged に加えて open 1 本あり** と整理するのが正確。[[github-dev-docs]]より

## Open Questions

- `mergeable: false` が branch 消失・競合・保護設定のどれを主因にしていたかは、この snapshot だけでは分からない
- `#817` を current open work としてどう扱うか。security / review automation の定常運用に載せるのか、それとも内容を整理して作り直すのか

## Updates

- 2026-05-18: 初版作成
- 2026-05-18: `#734` `#597` を stale cleanup で close した後の状態と、`tokoroten` / `ohki` の recent PR を追記
