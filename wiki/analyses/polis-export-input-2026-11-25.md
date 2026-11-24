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
