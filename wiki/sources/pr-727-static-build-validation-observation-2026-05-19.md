---
type: source
summary: `PR #727` は「公開レポート 0 件時の静的 build エラー改善」を狙うが、2026-05-19 時点の patch には validation が実行されない不具合と API URL 解決のずれがある
sources:
  - source-code.md
---

2026-05-19 に `digitaldemocracy2030/kouchou-ai` の draft PR 一覧を確認すると、draft の open PR は `#727` と `#722` の 2 件だけだった。差分規模が小さい `PR #727` を対象に、GitHub 上の patch と current `work/kouchou-ai/` の `public-viewer` 実装を照合してレビューした。[[source-code]]より

## Observations

- `PR #727` の変更対象は `client/package.json` と新規 `client/scripts/validate-reports.mjs` のみ
- `prebuild:static` は `npm run validate-reports && npm run copy-image && NEXT_PUBLIC_OUTPUT_MODE=export npm run rename-file` に変更されている
- 追加スクリプトは先頭で `process.env.NEXT_PUBLIC_OUTPUT_MODE !== "export"` なら即 return する
- しかし `prebuild:static` 内では `validate-reports` 実行時点に `NEXT_PUBLIC_OUTPUT_MODE=export` が付いていないため、意図した validation は常に skip される
- current `apps/public-viewer/app/utils/api.ts` は server-side で `API_BASEPATH` が無ければ `NEXT_PUBLIC_API_BASEPATH` に fallback する
- 一方 `validate-reports.mjs` は `API_BASEPATH || "http://localhost:8000"` を直接使い、`NEXT_PUBLIC_API_BASEPATH` fallback を持たない
- そのため current 系の環境変数運用に寄せて考えると、build 本体が到達できる API に validation だけが到達できず、誤って build を落とす余地がある
- GitHub 上で `PR #727` は 2026-05-19 時点でも `draft: true`

## Open Questions

- `client/` 時代の branch でも `NEXT_PUBLIC_API_BASEPATH` fallback が build 実装に存在していたか
- `#727` を revive するなら、script 追加で直すより `generateStaticParams()` 側 fail-fast に寄せた方が保守しやすいか

## Updates

- 2026-05-19: 初版作成
