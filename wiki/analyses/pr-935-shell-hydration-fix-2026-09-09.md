---
type: analysis
summary: "PR #935のshell一覧のReact #418をWebpackで解消。#935・#936・修正#938をマージ、E2E78件成功、title/noindexは#939へ切り出し"
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

### 2026-09-09 16:24 JST — CIのモバイルテストを補正

初回CIはshellの回帰テストを含む76件成功、通常静的exportのモバイル2件失敗。artifactの画面・DOMから、初期表示が折りたたまれた階層リストであり、テストが子クラスタ名の初期表示を前提としていると分かった。画面側の当該ロジックは#935時点から変更されていない。

root / subdirのテストでリスト選択を確認し、全体を展開して子要素を表示する操作を加えた（`c8488a7`）。dummy-server事前検証4件と、通常static buildを使ったモバイル2件がローカル成功。dummy-server指定のNext版はローカルキャッシュになく、検証時だけworkspaceの16.2.6を使用した。変更対象のBiome検査も成功。CIを再実行中で、PRはまだ未merge。

### 2026-09-09 16:31 JST — 全手順完了

更新HEAD `c8488a7`のCIは全チェック成功、全体E2Eは78 passed（4.3分）。[PR #938](https://github.com/digitaldemocracy2030/kouchou-ai/pull/938)をマージし、GitHubのMERGEDとmerge commit `679ee9e13d6e671a82a0978fb1d92c67cc1e669b`を再取得確認。local mainもfetch / fast-forwardで一致した。

[Issue #939](https://github.com/digitaldemocracy2030/kouchou-ai/issues/939)「shell配布物にレポート別title・noindexを反映する（#935由来）」を作成し、本文とOPEN状態を再取得確認。#935作者が挙げた制約由来と明記し、実配布への接続時のHTML metadata、Node再ビルド不要の維持、ブラウザ遷移の整合を完了条件にした。

今回解消したのはshell一覧のhydrationエラー。全体E2Eログには通常dev経路のhydrationログが残るが、その経路のビルド方式は本修正では変更していない。全viewer経路で同種エラーがなくなったという意味ではない。
