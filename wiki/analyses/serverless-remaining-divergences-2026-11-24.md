---
title: ブラウザ版に残る仕様差10項目と修正の優先順 2026-11-24
type: analysis
summary: 残る10項目を再現して評価。優先はJSON補正による本文改変と、公開JSONの再クラスタリングでの属性・スコア・件数喪失。番号や寛容な応答受理は維持し、原文保存・件数定義・実行方法の表示・指定値の扱いを別に直す
sources:
  - source-code.md
  - serverless-implementation-2026-11-24.md
  - serverless-integration-options-2026-11-24.md
---

## 結論

**10個の不一致をゼロにすることより、本文・属性・件数を壊さずに受け渡せることを優先する。** 調査で次の2群を再現した。

1. **応答を読みやすくする補正が、JSONの文字列内の意見本文まで変更する。** コードフェンス・`<think>`・末尾カンマを受け入れる利便性は残し、補正の実装を直す。
2. **公開JSONを別環境へ渡して再クラスタリングすると、属性・意見ごとのスコア・元のコメント数が失われる。** `propertyMap` の内容を本体へ機械的に揃える前に、読み手を直す。PR #2で元コメント本文を既定OFFにしたため、元コメント本文があることに依存した復元の問題が表に出やすくなった。前回はこの受け渡し後の再分析を検証していなかった。

その次に、入力原文の保存、件数の定義、実行方法の正しい表示、指定クラスタ数を黙って変える挙動を整理する。クラスタ番号や、抽出した意見の前後空白まで、本体の現状へ一律に揃える必要はない。

## 観測範囲

- 2026-11-24に両repoをfetch / fast-forward pull。本体mainは `a775d3d21ec369986028af4c9bc67feb9cbe1f59`、org serverless mainは `234123512681e686ece4f86ebaac6085f107a04e`。orgのopen PRは0、本体は #1227〜#1231 / #1233 / #1234 の7件を観測した。今回扱う仕様差を変更する進行中PRは確認できなかった。
- `tests/conformance` を再実行し、**44 passed / 10 expected fail（計54件）**。期待値の基準は本体 `3649fe417d2ee441e3475350e89ff6f4b35980e8` のままで、本体mainからの全期待値再生成はしていない。
- 本体の抽出パーサは現行ソースを直接ロードした。依存の多いモジュール内の `parse_label` / `_extract_json_text` / `normalize_cluster_nums` は、実際の関数定義をASTで抜き出し、変更せずに実行して確認した。これは本体パイプライン全体の実行ではない。
- serverlessの実際の工程関数に固定入力・偽のHTTP応答を流した。JSON復元→集計も工程関数の合成で確認した。実LLM・画面操作・品質評価は今回の対象外。再現コードと出力は `raw/serverless-remaining-divergences-2026-11-24/` に保存。
- ソースコードやテストは変更していない。以下は修正の判断材料と受け入れ条件であり、実装済みの報告ではない。

一次参照は [既知差の一覧](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/234123512681e686ece4f86ebaac6085f107a04e/conformance/known-divergences.json)と [[serverless-implementation-2026-11-24]] より。

## 10項目の判定

P1は本文・属性などの喪失、P2は誤表示・入力の扱い、維持は差として受け入れる判断。寛容な応答受理を維持する項目にも、共通パーサの修正は必要である。

| # / テストID | 差 | 判断 | 理由・修正対象 |
|---|---|---|---|
| 1 `units.ward_merge.labels` | Wardのクラスタ番号が違う | **維持** | 固定7ケースの分割は全件一致、番号まで一致するのは2件。番号はレポート内の識別子として整合していればよい。本体の番号を模倣する修正はしない。参照・親子・件数と、番号を無視した分割を検査する |
| 2 `units.normalize_cluster_nums` | 指定した1クラスタを2へ変更 | **P2：黙って変える点を修正** | `[1,4]` が `[2,4]` になる。本体は `[1,4]` を許す。1クラスタを正式にサポートするかは機能判断だが、未対応なら課金処理の前に明示的に拒否する。既定の推奨数を2以上にすることとは分ける |
| 3 `case.surrounding-whitespace.extraction.requests` | 入力本文の前後空白を削る | **P2：原文保存を修正** | 空白だけの回答を除外する処理と、非空の原文を書き換える処理を分ける。現状は保存する `CommentRow.body` 自体がtrim済みで、引用時にも原文を復元できない。原文を保存し、LLMへ送る正規化が必要なら方針を明示する |
| 4 `case.basic.result.comment_num` | 空白だけの回答を数えるか | **P2：件数の定義と表示を修正。再分析での喪失はP1** | 固定CSVは入力12行・有効コメント11件で、本体のcomment_numは12、serverlessは11。同じキーを違う分母に使っている。入力・処理対象・意見が出た回答を区別する。公開JSONの既知の件数を元コメント本文の件数から再計算してはいけない |
| 5 `case.basic.result.propertyMap` | serverlessは全属性を重複して入れる | **差自体は維持可。復元側をP1で修正** | 公開契約は属性表を許し、属性の本体は `arguments[].attributes` にある。本体と同じ `{}` にするだけでは再分析時の属性喪失を悪化させる。列の発見・型・値の保持をpropertyMapや元コメント本文の有無へ依存させない |
| 6 `case.basic.result.config.intro` | 「OpenAI API」と「OpenAI互換API」 | **P2：実行方法と来歴を修正** | 単なる表記差の場合もあるが、Gemini Nanoにも「OpenAI互換API」と書くのは実態と合わない。プロバイダ・モデル・ブラウザ内実行を区別する。再クラスタリングで元の抽出モデルを現在のラベル生成モデルへ置き換えず、イントロの自動説明を重複追記しない |
| 7 `parse.extraction.2` | 抽出した意見の前後空白を削る | **通常の自然言語の意見では維持** | 空白だけの意見を除き、同一回答内の同文を整理する挙動として妥当。本体の「空白だけの意見も文字列として残せる」挙動を模倣しない。入力原文の保存とは別にする。コード・詩など空白が意味を持つ入力には抽出仕様の判断が必要 |
| 8 `parse.extraction.3` | JSONコードフェンスを受け入れる | **受理は維持、本文を書き換える補正をP1で修正** | 外側のフェンスだけを除く。本体にもプロバイダのfallbackでフェンスを除く関数があり、「本体は必ず拒否する」とは断定できない。文字列内のバッククォートを削ってはいけない |
| 9 `parse.extraction.7` | JSONの末尾カンマを受け入れる | **受理は維持可、本文を書き換える補正をP1で修正** | 現行の正規表現は引用符内の `,]` も変更する。引用符・エスケープを認識して文字列外だけを補正するか、安全に読めない場合は失敗にする |
| 10 `parse.label.4` | ラベル応答の `<think>` を除いて読む | **外側の前置きへの対応は維持、本文削除をP1で修正** | 有効なJSON内のdescriptionにある `<think>…</think>` も消してしまう。最初にJSONをそのまま解釈し、必要なら外側の前置きだけを除く。必須フィールド検証と失敗扱いは維持する |

参照: [クラスタリング](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/234123512681e686ece4f86ebaac6085f107a04e/src/lib/pipeline/clusteringCore.ts)、[クラスタ数の適用](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/234123512681e686ece4f86ebaac6085f107a04e/src/lib/pipeline/steps/clustering.ts)、[CSV正規化](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/234123512681e686ece4f86ebaac6085f107a04e/src/lib/csv.ts)、[集計](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/234123512681e686ece4f86ebaac6085f107a04e/src/lib/pipeline/steps/aggregation.ts)、[JSONパーサ](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/234123512681e686ece4f86ebaac6085f107a04e/src/lib/llm/jsonParse.ts)より。

## P1：JSONの補正が本文を変更する

`parseJsonObjectLoose()` はJSONの解釈より先に文字列全体へ `stripNoise()` をかけ、JSONが壊れていると正規表現でカンマを削る。実際の抽出工程に流した結果は次のとおりだった。

| 元の応答内の意見 | 実際に保存される意見 | 条件 |
|---|---|---|
| `文字列 <think>ここは意見本文</think> です` | `文字列  です` | 正常なJSONでも変更される |
| バッククォート3個＋`json を使って例示する` | `を使って例示する` | 正常なJSONでも変更される |
| `文字列,]` | `文字列]` | 応答の配列末尾に余分なカンマがある場合 |

ラベルの `description: "<think>本文</think>を残す"` も `"を残す"` になった。本体の現行パーサでは、このような正常JSON内の文字列は変更されなかった。

**修正の受け入れ条件**:

- 最初に元のJSONを解釈し、成功した文字列値を書き換えない。
- 補正するのはJSONの外側のフェンス・前置き、または文字列外の末尾カンマだけ。曖昧な応答・途中切れ・スキーマ不正は失敗のままにする。
- 上の3例、ラベル本文中のタグ、エスケープされた引用符、正常0件、不正応答後の再試行を固定入力で検査する。
- 抽出・ラベル・概要・賛否スペクトラムが同じパーサを使うため、全呼び出し元で値の保持を確認する。

## P1：公開JSONの再分析で属性と件数が失われる

`projectFromResult()` は属性列を `Object.keys(propertyMap)` からだけ決め、意見の属性を回答単位へ集約し、元コメント本文の一覧から再構成した `CommentRow` に載せる。その後の `aggregation()` は、このCommentRowから意見の属性と件数を作り直す。[projectFromResult](https://github.com/digitaldemocracy2030/kouchou-ai-serverless/blob/234123512681e686ece4f86ebaac6085f107a04e/src/lib/reportProject.ts)と[本体の公開契約](https://github.com/digitaldemocracy2030/kouchou-ai/blob/a775d3d21ec369986028af4c9bc67feb9cbe1f59/docs/development/public-result.md)より。

5入力・2意見の公開JSONを合成し、復元→集計した結果:

| 入力の形 | 再分析後 |
|---|---|
| 本体の通常形：propertyMapは空、属性は各意見にあり、元コメント本文は2件ある | 年代2件が両方消える。comment_numは5→2 |
| serverlessの既定公開形：propertyMapにも年代があり、元コメント本文は空 | 年代2件が両方消える。comment_numは5→0 |
| 同じ回答から出た2意見に、数値スコア0.8と-0.5が付いている | 両方とも文字列の`"0.8"`になる。値だけでなく型も変わる |

元コメント本文を公開しないことと、公開済みの属性・件数を保持することは両立させる必要がある。元のプロジェクトが同じブラウザにある場合はそれを再利用するので、主な再現条件は**JSONだけを別ブラウザへ渡して再クラスタリングする場合**。通常の閲覧時には属性が見えていても、再分析後に消える。

**修正の受け入れ条件**:

- 意見ごとの `attributes` をarg_idに結び付けて保持する。回答単位へまとめず、数値を文字列へ変えない。
- 元コメント本文がなくても、`comment_num` が既知なら引き継ぐ。不明な値は0件と断定しない。意見の出なかった回答もあるため、意見のcomment_id数から入力件数を復元しない。
- propertyMapが空・一部だけ・全属性ありのいずれでも、属性と型が落ちない。
- 原文公開OFFを保持したまま、JSON読込→再クラスタリング→公開用JSON書き出しを検査する。
- 元の抽出モデル・入力件数と、今回のラベル生成モデル・変更したクラスタ数を別に残す。完成済みイントロへ同じ自動説明を繰り返し足さない。

## その次に直すもの

1. **入力原文と件数の区別（#3・#4）**: 空白だけの回答を処理しない判断は維持し、非空の原文はそのまま保存する。`comment_num`を入力コメント数として扱うなら、CSVの受理行数と有効コメント数を別々に保持し、画面・HTML・PowerPointでも分母を明示する。本体のイントロは空白を除いた処理対象数を使うため、comment_numとイントロが同じ数であることを前提にしない。
2. **実行方法の表示（#6）**: Gemini Nanoを使った合成入力でも現行のイントロは `OpenAI 互換 API (gemini-nano)` となった。ブラウザ内実行・ローカルAPI・外部APIを区別できる公開可能なメタデータを引き継ぐ。APIキーや接続先の詳細を公開設定へコピーしない。
3. **指定値の検証（#2）**: `1`を黙って`2`へ変える挙動をやめる。通常版で1クラスタを許すか、未対応として実行前に説明するかを決める。UMAPの最小データ数とクラスタ数の下限は別の制約として検査する。

## 適合性テストの見直し

- **番号の差**は分割・親子参照・件数の整合性で検証する。本体の番号そのものの完全一致は採用条件にしない。
- **原文の正確さ**、**公開JSONの情報保持**、**意図した入力の受理**をそれぞれ検査する。再分析で属性が消えても、生成工程だけの比較では検出できない。
- フェンス受理の比較は、**工程に渡される値の境界**を揃える。本体の工程パーサはフェンス付き文字列を拒否する一方、プロバイダfallbackの `_extract_json_text()` を先に通すと受け入れた。現行の偽LLMによる工程比較から、すべての実プロバイダでの受理・拒否を推定しない。
- 維持すると決めた差にはserverless側の期待する挙動を通常のテストとして置き、本体との不一致は理由付きで追跡する。expected failを減らした件数だけで改善を評価しない。

本体の関連実装: [抽出のパース](https://github.com/digitaldemocracy2030/kouchou-ai/blob/a775d3d21ec369986028af4c9bc67feb9cbe1f59/packages/analysis-core/src/analysis_core/services/parse_json_list.py)、[ラベルのパース](https://github.com/digitaldemocracy2030/kouchou-ai/blob/a775d3d21ec369986028af4c9bc67feb9cbe1f59/packages/analysis-core/src/analysis_core/steps/_labelling.py)、[プロバイダのJSON補助](https://github.com/digitaldemocracy2030/kouchou-ai/blob/a775d3d21ec369986028af4c9bc67feb9cbe1f59/packages/analysis-core/src/analysis_core/services/llm.py)、[集計・件数・説明文](https://github.com/digitaldemocracy2030/kouchou-ai/blob/a775d3d21ec369986028af4c9bc67feb9cbe1f59/packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py)より。

## Open Questions

- 1クラスタを通常分析の入力として正式に扱うか。推奨クラスタ数と対話画面の操作範囲も合わせて決める。
- 空白が意味を持つ素材を対象にする際、意見抽出の出力空白をどこまで保持するか。
- 入力・処理対象・意見が出た回答の件数を、公開契約へどの形で追加するか。既存comment_numの意味は事前に揃える。

## Updates

- 2026-11-24: 残る10項目を調査し、固定入力でパーサの本文改変とJSON再分析の情報喪失を再現。今回は修正・Issue作成・PR作成は行わず、優先順と受け入れ条件を整理した。
