---
title: 再実行の判定と集計のミューテーションテスト 2026-11-24
type: analysis
summary: "mutmut を core/orchestration.py と steps/hierarchical_aggregation.py の 2,832 変異に広げ、テストが気づいた割合は 71.5%。本番経路の生存 605 件を仕分けると約 135 件が本番で振る舞いの変わる穴で、管理画面の再集約（--only）、管理画面の config の検証、期限切れロック、結果 JSON のクラスタ ID・value・元コメント、パブコメ CSV などに集まっていた"
sources:
  - source-code.md
  - mutation-testing-trial-2026-11-24.md
---

# 再実行の判定と集計のミューテーションテスト 2026-11-24

対象: kouchou-ai main `2a924af6`（2026-11-24、[#1220](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1220) merge 後）。本体のコードは変更していない。手法と mutmut の設定は [[mutation-testing-trial-2026-11-24]] と同じ（`process_isolation = "forkserver"`）。[[source-code]]より

## 何をしたか

1 回目で対象にした 4 モジュールに続けて、過去のレビューで回帰が多かった 2 ファイルに広げた。

- `core/orchestration.py`: 再実行の判定（`decide_what_to_run`）、`--reuse-from` の流用、トークン数の引き継ぎ、config・API キーの検証、status ファイルとロック
- `steps/hierarchical_aggregation.py`: 結果 JSON（`hierarchical_result.json`）、公開用の写し、パブコメ CSV の組み立て

## 結果

| | 件数 |
|---|---|
| 変異の総数 | 2,832 |
| kill（テストが気づいた） | 2,022 |
| timeout | 3 |
| 生存 | 807 |
| kill 率 | 71.5% |

8 並列で 29 分半。1 回目（76.0%）より低い。

CLI と管理画面は、どちらも `PipelineOrchestrator.from_config` → `run_default()` → `run_workflow()` を通る。管理画面の API は `python -m analysis_core` を起動する。`run_step`（生存 101 件）と `termination`（同 51 件）は、Python API の `PipelineOrchestrator.run()` だけが使う旧経路なので、仕分けの対象から外した。

残りの生存 605 件（print / logging の文面だけの変異を除く）は、3 領域に分けて仕分けた。各変異を本番に近い入力で動かし、元のコードと出力を比べている。

| 領域 | 生存 | 実害なし | 軽微 | 本番の穴 |
|---|---|---|---|---|
| 再実行の判定まわり | 176 | 102 | 51 | 23 |
| 初期化・検証・status | 211 | 91 | 65 | 55 |
| 集計（結果 JSON） | 218 | 129 | 32 | 57 |

## 見つかった穴（重要度順）

本番で振る舞いが変わるのに、テストが確かめていないもの。★は、変異を入れて再現するか、呼び出し元のコードと照合するかして、この分類とは別にもう一度確かめたもの。それ以外は、仕分けで出力の違いを確かめたもの（「推論」と書いたものを除く）。

### 管理画面の操作に直接響くもの

1. ★ **ラベル編集の後の再集約**（`decide_what_to_run` の `config.get("only") == stepname`）
   - 比較キーが一致しなくなっても、テストはすべて通る。
   - 壊れると、前回の結果が揃っていて設定も同じときに、`--only hierarchical_aggregation` を付けても集約が「変更なし」で飛ばされる。そのまま `initialization` が ValueError で失敗する。
   - 管理画面は、ラベルを編集した後の再集約でこの引数を付けて CLI を起動している（`report_launcher.py`）。つまり、この操作が必ず失敗するようになる。
   - 既存の `--only` のテストは、`force` と組み合わせた場合と、不正な値を拒否する場合しか見ていない。
2. ★ **管理画面が作る config の検証**（`validate_config` の `valid_fields`）
   - `local_llm_address`・`enable_source_link`・`enable_original_comments` のどれかが許可リストから消えても、テストは通る。
   - 管理画面が作る config にはこの 3 つが必ず入るので、「Unknown field」で全レポートが起動時に落ちる。
   - 同じ関数の、工程オプションの綴り間違い（`extraction.limt` など）を拒否する検査が丸ごと抜けても、テストは通る。
3. ★ **期限切れのロック**（`initialization` のロック判定）
   - `lock_until and 期限内` を `or` にしても、テストは通る。
   - 壊れると、OOM などで落ちて `status=running` と期限切れの `lock_until` が残ったレポートは、再実行が毎回「Job already running.」で止まる。
   - 既存テストは、期限内のロックしか見ていない。
   - 関連して、`update_status` が未来の `lock_until` を書かなくなる変異も生き残った。`update_progress` がロックを延長しなくなる変異も同様。

### 結果 JSON・公開ビューアに響くもの

4. ★ **意見のクラスタ ID**（`_build_arguments`）
   - 階層の列を見つけられなくなると、全意見の `cluster_ids` が `["0"]` だけになる。それでもテストは通る。
   - 公開ビューアは、散布図の色分け・一覧の件数・ツリーマップの絞り込みに `cluster_ids` を使う。
   - 意見の本文が全件 `"None"` になる変異も生き残った。
5. **クラスタの value・parent・density とルートのクラスタ**（`_build_cluster_value`、25 件）
   - value が null になる変異は、静的 HTML の書き出しで TypeError になることまで確かめた。
   - parent が壊れると、階層リストが組めない。density が null になると、密度フィルタが効かない。この 2 つと、公開ビューアの value の絞り込みが全部外れる影響は推論。
   - ルートのクラスタ（`id "0"`）の形を確かめるテストが 1 つも無い。
6. ★ **元コメント一覧**（`_build_comments_value`）
   - ループの `continue` を `break` にしても、テストは通る。
   - 壊れると、先頭に「意見が出なかったコメント」があるときに `comments` が空になる。非公開に指定したコメントがあるときは、それより後ろが全部消える。
7. **パブコメ CSV**（`add_original_comments`、11 件）
   - 入力に url・source・`attribute_` の列があると、集計ごと失敗する変異（列名の重複など）が生き残った。
   - category 列が空になる変異、列が落ちる変異も生き残った。
   - 読み手は管理画面の CSV ダウンロード。
8. **公開される説明文の件数**（`create_custom_intro`）
   - 「None 件の意見」になる変異が生き残った。

### 再実行・流用の判定

9. **`--reuse-from` で別の入力を指定したとき**（`_seed_reused_outputs`）
   - 流用した記録に `global_params` が引き継がれなくても、テストは通る。
   - 壊れると、別の CSV や別の question を指定しても、抽出からラベルまで流用元のものが使われる。走るのは集約だけになる。
10. **モデルの変更・`-f`**（`decide_what_to_run`）
    - 比較キーの `model` が壊れると、工程のモデルを変えても何も再実行されない。
    - `force` を読まなくなっても、テストは通る。`-f` を使うのは CLI だけ。
11. **既定の config での再実行**（`decide_what_to_run`）
    - 意見分類などの任意工程が無効のまま、完了済みのレポートを再実行すると AttributeError で落ちる変異が生き残った。
12. **古いレポートのトークン数の引き継ぎ**（`carried_over_token_usage`）
    - 工程ごとの input / output の内訳は v4.2.0（[#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031)）で入った。それより前のレポートを部分的に再実行するときの按分が壊れても、テストは通る。
    - 例: 前回の合計が input 300 / output 100 で、3 工程を引き継ぐ場合、input の正解は 225。変異によって 75 に減ったり、300 になって二重に数えたりする。

### CLI の利用者に響くもの

13. **gemini / openrouter の API キー検証**（`validate_api_keys`、8 件）
    - 壊れると、`GEMINI_API_KEY` だけを設定していても「not set」で起動できない。ユーザーキーだけを渡した場合も落ちる変異がある。
14. **LLM 直接グルーピングのプロンプト**（`initialization`）
    - config に書いた `discovery_prompt` / `assignment_prompt` が既定のプロンプトに上書きされても、テストは通る。管理画面はこのプロンプトを送らない。
15. その他
    - `--validate-input` / `--dry-run` が、CSV が無くても「passed」と出る。
    - `--output-dir` / `--input-dir` を省いたときの既定値が壊れる。
    - 公開ビューアの「分析手順」から `source_code` が消える。
    - 翻訳ファイルが欠けているのを検知しない。

ユーザー API キーを status に書き出さない処理（`redact_error_texts`・`strip_secret_keys`）には、生き残った変異が無かった。2026-10 の漏洩の修正（[[user-api-key-leak-2026-10]]）は、テストでしっかり守られている。

## 実害なしと判断した主な類型

- **呼び出し元が必ず値を渡すので、既定値の分岐に届かない**: specs・出力先・`skip_interaction` など
- **起こらない入力を前提にした分岐**: plan の要素には必ず `run` がある。意見は必ず対応表にある。polars が numpy の型を返さない
- **直後に同じキーで上書きされる値**: `initialization` が書く running status は、`run_workflow` が直後に上書きする
- **二重の守りの片側**: `read_merge_labels` の null 埋めと `_text_or_empty` は互いに補い合うので、片方を壊しても JSON は変わらない
- **流用しない工程が specs の末尾にある**: そのため `continue` と `break` で結果が同じになる
- **Windows でだけ問題になりうるもの**: open の `encoding` 省略。Linux では同じなので「軽微」に入れた。Windows 版の配布物では文字化けしうる

## 次に見るもの

- 1〜4 と 6 は、どれもテスト 1 本で塞げる。管理画面の操作に直接響く 1〜3 から先に PR にするのがよい
  - 1: 完了済みの status から `--only hierarchical_aggregation` の計画を作る
  - 2: 管理画面の `_build_config` と同じ形の config を通す
  - 3: 期限切れのロックと、`lock_until` の無い running status を置く
- 5 と 7 は、2 階層・url / attribute 列ありの入力で、結果 JSON とパブコメ CSV を丸ごと照合するテストを 1 本足せば、まとめて塞げる見込み

## Open Questions

- `run_step` と `termination` の旧経路（`PipelineOrchestrator.run()`）は、Python API として残すのか。残すなら生存 152 件も仕分けが要る。残さないなら削除候補
- 3 領域の仕分けは、関数を直接呼んで出力を比べる方式で行った。★を付けた 5 件以外は、PR にする時にテストを書いて改めて確かめる

## Updates

- 2026-11-24: 見つけた穴を塞ぐテストを 2 本の PR にした（どちらも未 merge、CI 全件 pass、本体のコードは変更なし）
  - [#1233](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1233)（起動と再実行の判定）: 1〜3 と 9〜15 を塞ぐ。仕分けで穴とした変異 58 件に流して 57 件が落ちた。残る 1 件（`initialization` の `getattr` の既定値）は直後の `try/except` で結果が同じになる等価な変異。analysis-core 全体 901 passed
  - [#1231](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1231)（結果 JSON とパブコメ CSV）: 4〜8 を、2 階層・属性列ありの入力で出力を丸ごと照合する 1 ファイルで塞ぐ。集計の生存変異 234 件のうち 73 件が落ち、穴とした変異はすべて含まれる。残りは出力が変わらないか軽微なもの。analysis-core 全体 883 passed
  - 非公開の属性値を持つコメントの扱い（本文だけ隠し、意見と属性は残す）は現行の挙動を固定した。[#1180](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1180) で扱いが変わる時はテストも合わせて直す
  - CodeRabbit は 2 本ともレビューを skip した

