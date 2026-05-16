---
name: npm-vs-pnpm
summary: なぜ pnpm 必須で npm 非対応か — plugin システムが要求する node_modules 分離
type: analysis
sources:
  - github-dev-docs.md
---

## 結論

[[kouchou-ai]] は **pnpm 9.15.4 必須**、npm は **非対応** と明示。

## 理由（`docs/development/why-pnpm.md` の要約）

- [[plugin-system]] は **strict-isolation な `node_modules`** を前提に設計されている
- npm は依存をルートにホイストする — 結果として「直接 declare していないパッケージが import できてしまう」phantom dependency が発生
- plugin が **配布先で動作することを保証** したい場合、phantom dependency に依存した plugin はビルド時には通っても他環境で壊れる
- pnpm の non-hoisting `node_modules` はこの問題を構造的に排除する

## 運用上の意味

- 開発者は **corepack 経由で pnpm 9.15.4** を使う想定
- npm でローカル動作させたとしてもサポート外
- yarn についてはドキュメント上の明示はないが、同じ理由で非推奨と推察

## なぜ「ただの好み」ではないか

phantom dependency 問題はモノレポと plugin システムの組み合わせで顕在化する典型例。プラグイン配布を意図しないアプリでは npm でも問題にならないことが多いが、kouchou-ai は **plugin を技術的境界とする** 設計（[[plugin-system|採用理由]]）なので、依存解決の厳密性が中心的要件になる。

## Updates

- 2026-05-17: 初回作成
