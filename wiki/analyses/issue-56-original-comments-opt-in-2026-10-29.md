---
title: "Issue #56 元コメントの表示：レポート単位 opt-in で第一段階を実装（PR #1155、2026-10-29）"
type: analysis
summary: "2026-10-28 に shingo-ohki が実利用で再要望した元コメント表示について、公開可否を『レポート作成者が作成時に明示 ON』で扱う第一段階（config enable_original_comments）を PR #1155 として実装。per-comment の再頒布可否フラグは別段階に送った判断と、現行 main の実態・残論点の整理"
sources:
  - issue-audit-2026-10-11-batch1.md
  - source-code.md
---

## 問い

[#56](https://github.com/digitaldemocracy2030/kouchou-ai/issues/56) 元コメントの表示機能に、2026-10-28 shingo-ohki がコメントを付けた。main 最新でサンプルデータからレポートを作り、散布図で気になった点から元コメントを見ようとしたが、ソースリンク機能を有効にしても入力 CSV に `url` 列が無いと抽出意見の表示止まりだった。「公開可能なデータに限り、点から元コメント本文を見られると、AI の抽出・要約が適切かの確認にも使える」という実利用からの再要望である。これにどう応えるか。

## 現行 main の実態（1028da9c、2026-10-27）

[[issue-audit-2026-10-11-batch1]] の判定から変わっていなかった。

- 公開 JSON `hierarchical_result.json` の `comments` は空のまま。原文を詰める呼び出しはコメントアウトされ、`_build_comments_value` は dead code だった
- ソースリンク機能は `url` 列の値を hover に出して click で外部に開くだけで、原文本文は扱わない
- 原文を出す経路は pubcom 用の admin CSV（`is_pubcom`）だけで、viewer には届かない
- `comment_id` は report-schema では number、本体の CSV 処理では string で揃っていない

## 判断：公開可否の契約を 2 案に分け、1 を第一段階にする

論点は実装量ではなく「公開可否が不明な元コメントを公開出力に含めない」（Issue 本文 2026-09-09 追記）をどう担保するか。

1. **レポート単位の opt-in**。作成時に「元コメントを公開する」を明示 ON にした時だけ `comments` を詰め、viewer で表示する。既存のソースリンク機能と同じ「作成者が公開可能性に責任を持つ」契約で、新しい入力 schema は要らない
2. **per-comment の再頒布可否フラグ**を入力 CSV に持たせる。pubcom のように混在データで必要になるが、入力 schema と serverless 側の多対多契約の整理が先

nishio は 2026-10-29 に 1 を選択。2 は別段階として残す。

## 実装（PR [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155)、branch `feat/56-original-comments`、未 merge）

- **analysis-core**: config `enable_original_comments`（既定 false）。true のときだけ `comments` に意見へ紐づく元コメント本文を `{comment-id: {comment}}` で入れる。`comment-id` は入力 CSV の文字列のまま key にし、意見が抽出されなかったコメントと `hidden_properties` で非公開にした属性値を持つコメントは含めない。再実行判定の `global_params` にも追加
- **api**: `ReportInput` / `ReportDuplicateOverrides` にフラグを追加し、作成と複製の config に渡す
- **admin**: 作成画面のソースリンク機能の下に「元コメントの本文を公開レポートに含める」チェック。引用・再頒布が許されるデータだけで ON にする旨を説明に書き、ブラウザには保存せず毎回 OFF から始める（入力データごとの判断なので前回の ON を引きずらない）。再利用画面は複製元の設定を引き継ぐ
- **public-viewer**: フラグが true のレポートだけ、散布図ホバーに本文（先頭 200 文字、HTML エスケープ）を添え、階層リストの意見の下に本文を出す。ja / en / ko
- 検証: analysis-core 798 件、api 関連 72 件、viewer 314 件、admin 117 件のテストと ruff / biome / tsc が通過。実 LLM での生成と画面の目視は未実施

## 補足：「多対多参照」とは何か（nishio の問いへの回答、2026-10-29）

Issue 本文の 2026-09-09 追記にある「意見と元コメントの多対多参照を保持」の意味。出典は [[serverless-product-direction-2026-09-08]] と nishio の 2026-10-21 コメント。

- **本体は 1 対多**。1 件の元コメントから複数の意見が抽出されるが、1 件の意見が指す元コメントは常に 1 つ。[#1032](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1032) 以降は抽出の重複判定が「回答と文面の組」になり、別の回答から出た同じ文面の意見は回答ごとに別の意見になる。`relations.csv` の各行は「意見 1 つ → コメント 1 つ」、公開 JSON の `comment_id` も単一の値。PR [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155) はこの前提のままで、`comments[argument.comment_id]` を引くだけで原文に戻れる
- **多対多が出てくるのは serverless 版**。tokoroten/kouchou-ai-serverless は同じ文面の意見を回答をまたいで 1 つに束ね、最初の回答に帰属させる。意見側が複数の元コメントを指す構造で、その経路で文字列 ID・先頭ゼロ・JavaScript の数値精度を超える ID が数値化されて別のコメントに誤対応する不具合があり、serverless PR #22（2026-09-09 merge）で「表記が変わらない安全な整数だけ数値で出す」形に直された
- Issue 本文の項目は「将来、本体と serverless の両方で原文に戻れる契約を揃えるなら、意見 1 つが複数コメントを指せる形を壊さず、ID の型でも誤対応しないこと」を求めている
- PR [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155) との関係: ID の型の方は満たしている（`comment-id` を入力 CSV の文字列のまま key にし、先頭ゼロをテストで確認）。意見 1 つが複数コメントを指す形は本体のパイプラインが作らないので扱っていない。nishio は「設計としては serverless 版のように束ねた方がよい」と判断し、設計変更を [#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) に切り出した

## 設計上の小さな判断

- フラグをブラウザに保存しない点だけ、ソースリンク機能（localStorage に保存）と揃えなかった。公開範囲を広げる設定は毎回 OFF から始める方が安全と判断した
- `hidden_properties` の除外は属性値ベースのままで、per-comment の可否は表現できない。これが案 2 を別段階に残す理由
- hover は先頭だけに切り、全文は階層リスト側で読む。[[post-review-product-direction-2026-10-28]] の「階層リストを詳細モードとして正式化し、最下層で原文へ辿る」導線にそのまま使える

## Open Questions

- データ構造の設計変更（同一内容のコメント・同一意見の束ね、多対多、serverless との契約統一、`comment_id` の型揃え）は [#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) に切り出した。#56 は PR [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155) の merge で close してよいかは人間判断
- shingo-ohki への返信は未投稿。PR の自動リンクだけが Issue に付いている

## Updates

- 2026-10-29: 初版。nishio の案 1 選択を受けて PR [#1155](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1155) を作成
- 2026-10-29: nishio が #56 のコメントで「設計としては serverless 版のように束ねた方がよいが、まず現状の構造で元コメント表示を実現し、設計変更は別 Issue」と判断。切り出し Issue [#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) を作成（束ね方の基準、`comment_ids` への拡張、型揃え、serverless との契約統一、[#250](https://github.com/digitaldemocracy2030/kouchou-ai/issues/250) の表示）
- 2026-10-29: CI の how-to-use リマインダーを受け、利用ガイド `docs/user-guide/how-to-use.md` の散布図の操作に「元コメントの確認」を追記して PR に push（7f1e13b9）。レビュー・コメントはまだ無し
