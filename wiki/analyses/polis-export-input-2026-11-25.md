---
title: "広聴AIで読めるPolisエクスポート 2026-11-25"
type: analysis
summary: "Polisのcomments.csvは本体の管理画面・CLIとブラウザ版で読める。投票履歴や参加者グループを分析に組み込む専用連携はない"
sources:
  - source-code.md
---

Polisの `comments.csv` にはコメントIDの `comment-id` と本文の `comment-body` がある。本体の管理画面では「CSVファイル」からアップロードし、コメント列に `comment-body` を選ぶ。CLIの必須列もこの2列なので、同じファイルをそのまま指定できる。ブラウザ版も `comment-body` と `comment-id` を初期選択に使う。[[source-code]]より。[Polisのエクスポート仕様](https://compdemocracy.org/export/)・[CLIの入力仕様](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9a19cb8471fc353b54ae07a4710336299/docs/user-guide/cli-quickstart.md#2-入力csvの準備)・[ブラウザ版のCSV入力](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/7a9c9212f70d834290939f8bb51e078689282b77/src/components/WizardPage.tsx#L112-L143)

`votes.csv`、参加者ごとの投票行列、Polisのグループ分けを分析に取り込む専用連携は、本体の `main` にない。`comments.csv` の `agrees` と `disagrees` は管理画面で属性として選べるが、投票数で分析を重み付けする機能ではない。Polis側で除外されたコメントを対象外にする場合は、取り込み前に `moderated = -1` の行を除く。[[source-code]]より。[Polisのエクスポート仕様](https://compdemocracy.org/export/)・[通常のCSV入力から分析に渡す処理](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9a19cb8471fc353b54ae07a4710336299/apps/admin/app/create/page.tsx#L119-L147)

2026-11-25 に GitHub の本体 `main` (`afde1cb9`) とブラウザ版 `main` (`7a9c921`) を確認した。本体同梱の [`example-polis.csv`](https://github.com/digitaldemocracy2030/kouchou-ai/blob/afde1cb9a19cb8471fc353b54ae07a4710336299/apps/api/broadlistening/pipeline/inputs/example-polis.csv) で、両UIのCSV読み込み関数が全342件のIDと本文を読み取れること、および本体CLIの `--validate-input` が通ることを確認した。確認範囲は入力まで。関連する進行中の専用連携PRは GitHub 検索で見当たらなかった。[[source-code]]より。

Polis入力プラグインは過去の構想で候補に挙がっていた。通常のCSV入力は上記の手順で利用できる。[[plugin-system]]より。

## Updates

- 2026-11-25（ローカル試作 `codex/polis-import`、`c95489e7`）: 本体管理画面に Polis タブを追加した。`moderated = -1` と空欄本文を外し、件数を表示する。選んだ元コメント単位の票数はレポートのフィルタ属性として渡す。参加者IDと個別票は管理画面のブラウザ内で使う。[[source-code]]より。
- 参加者を1点として、投票行列の最終時点に学習した2軸に投影する。未投票は列平均、パスは明示的な `0` として扱う。`participants-votes.csv` でエクスポート時のグループを色分けし、`votes.csv` があれば日ごとに最新票を再現して個人の軌跡も表示する。点の移動には、別のコメントに投票したことと投票し直したことの両方が含まれる。[[source-code]]より。[Polis投票行列の仕様](https://compdemocracy.org/polis-opinion-matrix/)
- 公開データ Scoop Hivemind・UBI の71コメントのうち70件を取り込み、参加者234人、4グループ、19日分を実ブラウザで確認した。2つの投票CSVから求めた最新票のコメント別全体集計は、このデータでは一致した。Polisのエクスポートは `1` が賛成で、データベースや投票送信APIの符号とは異なる。個別データや大規模会話での性能確認はまだ行っていない。[公式の公開データ](https://github.com/compdemocracy/openData/tree/master/scoop-hivemind.ubi)・[Polisのエクスポート実装](https://github.com/compdemocracy/polis/blob/edge/math/src/polismath/darwin/export.clj#L2598-L2648)
- 2026-11-25: 関連 [Issue #1247](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1247) を作り、使い方と実画面を添えて、本体 [PR #1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248) を作成した。`codex/polis-import` の `1f2c1a8f` を `main` に提案中。[[source-code]]より。
- 2026-11-25: 初回の管理画面E2Eは通常CSVとPolisのファイル入力を同時に拾った。セレクタを通常CSVタブに限定した `f51e51c8` で再実行し、GitHub Actionsの5ワークフローが成功した。初回の公開ビューアの375pxテストは本体 `main` (`afde1cb9`) でも再現し、再実行では通過した。[PR #1248](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1248)
