---
type: analysis
summary: "PR #935のshell一覧でReact #418を5/5再現。EmotionとTurbopackの不整合をWebpackで回避し、回帰E2E付きPR #938を作成"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/935
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/936
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/938
  - https://chakra-ui.com/docs/get-started/frameworks/next-app
  - https://react.dev/errors/418
---

## 結論と原因

2026-09-09 16:14 JST時点。[React公式エラー説明](https://react.dev/errors/418)より、#418は初期HTMLとブラウザ側の描画が一致せず、クライアントで再生成したことを意味する。[[pr-935-936-overview-2026-09-09]]の観測を追試したところ、shell一覧の初回表示で5回中5回再現。エラー後の一覧→詳細→一覧・欠落表示は成功した。

ローカルブラウザへ配信するReact bundleに診断ログを一時挿入して、Reactが一覧loadingのdivを期待する位置に、Emotionのcss-global styleがあることを確認。[Chakra UI公式ガイド](https://chakra-ui.com/docs/get-started/frameworks/next-app#hydration-errors-turbopack)のTurbopack / Emotion hydration不整合と症状が一致する。元ソースへの診断コード変更は行っていない。

同一PR HEAD `373c76b`、同じfixture、ChromiumでWebpack出力に変えると同じ5回の操作でpageerrorなし。修正方針はshellビルドだけに`--webpack`を指定すること。通常build / build:static / devやレポート描画ロジックには変更を加えない。

## ユーザー指定の順序と実施内容

1. 原因調査と修正見通しを確立。
2. #935を`472b607`、#936を`23c7821`でマージ。GitHubのMERGEDを再取得確認。
3. mainから`codex/shell-hydration-fix`を作り、[PR #938](https://github.com/digitaldemocracy2030/kouchou-ai/pull/938)を作成（`c90cae4`、CI待ち、未merge）。
4. #935作者が明記していたtitle / unlisted noindexは、修正PRのマージ後に後続Issueとして切り出す。

## 検証

- viewer Jest: 12 suites / 123 tests成功。
- shellの本番ビルド、既存package-shellによるfixture同梱とローカルHTTP配信で検証。静的JSONの到達・parseを事前確認。
- shell E2E既存4件＋回帰1件は5 passed（7.9秒）。ローカル専用設定でshellだけを実行し、ブラウザはキャッシュ済みChromiumを使用。
- 新規E2Eはpageerrorを監視する。元のTurbopack出力では#418で失敗し、Webpack出力では成功することを確認。
- viewerだけの変更でも回帰テストが発火するようE2E workflowのpathsを補った。
- APIキー・実APIは使用していない。CIの全体E2E・通常ビルドは別途確認する。

## Open Questions

- 上流でTurbopack / Emotionの問題が解消されたら、同じ回帰テストでWebpack回避策を外せるか確認する。
- タイトル・検索除外は本エラーとは別件。実配布の用途と接続段階を踏まえてIssueで管理する。

## Updates

- 2026-09-09 16:14: 調査と修正PR作成を記録。マージとIssue作成は続けて実行する。
