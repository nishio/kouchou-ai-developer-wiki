---
title: analysis-core のミューテーションテスト試行 2026-11-24
type: analysis
summary: "mutmut 3.8.1 で analysis-core の 4 モジュール（770 変異）を試し、kill 76%。既定の fork 方式では 220 件が誤って timeout になるので forkserver 方式が要る。生存変異から、部品は試験済みでもつなぎ目が未検証という穴（429 の結果を同時実行数の制御へ渡す配線、SDK の再試行を止める HTTP クライアント、工程をまたぐトークン数の合計）が見つかった"
sources:
  - source-code.md
---

# analysis-core のミューテーションテスト試行 2026-11-24

対象: kouchou-ai main `600479b7`（2026-11-20 時点、[#1219](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1219) merge 後）。本体のコードは変更していない。[[source-code]]より

## 何をしたか

ミューテーションテストは、ソースコードを機械的に少しずつ壊し（`+=` を `=` に、`"ok"` を `"XXokXX"` に、`continue` を `break` に、など。壊した 1 か所ごとの版を「変異」と呼ぶ）、既存のテストがその変化に気づくかを数える手法。テストが落ちれば「kill」、全部通ってしまえば「生存」で、生存した変異はテストが確かめていない振る舞いを指す。行カバレッジでは「実行はされたが結果を誰も確かめていない」行が見えないので、それを補う。

- ツール: mutmut 3.8.1（Python）、analysis-core の通常のテスト（873 件、e2e を除く）
- 対象は、外部 API を呼ばずに単体で試しやすい 4 モジュールに絞った:
  - `services/rate_limit.py`（429 を受けた時の待ち・送り直し・同時実行数の自動調整）
  - `workflow/engine.py`（工程を順に実行する本体。CLI の `PipelineOrchestrator.run()` から `run_workflow()` 経由で使われる）
  - `workflow/resolver.py`（工程の依存関係の並べ替え、実行条件の判定）
  - `public_result.py`（公開用の結果ファイル）
- 全体を対象にしなかったのは時間のため。素のテスト一式に約 2 分 15 秒かかり、770 変異でも 7 分 20 秒（8 並列）かかった

## 結果

| | 件数 |
|---|---|
| 変異の総数 | 770 |
| kill（テストが気づいた） | 578 |
| timeout（変異で無限待ちになった。気づいたのと同じ扱い） | 7 |
| 生存 | 185 |
| kill 率 | 76.0% |

生存はモジュールで大きく偏る。

| 関数 | 生存 |
|---|---|
| `WorkflowEngine.run` | 70 |
| `WorkflowEngine._build_initial_artifacts` | 45 |
| `rate_limit.call_with_rate_limit` | 20 |
| `AdaptiveConcurrencyLimiter`（`release` / `__init__`） | 14 |
| resolver（`evaluate_condition` / `validate_dependencies` / `resolve_execution_order`） | 19 |
| `retry_after_seconds` / `chat_http_client` ほか rate_limit の残り | 13 |
| `_resolve_step_config` / `build_public_result` | 4 |

`public_result.py` はほぼ全滅（生存 1）で、契約を細かく固定したテスト（[#1179](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1179) で追加）が効いている。

## 見つかったテストの穴

共通する形は「**部品は単体で試験済みだが、部品同士のつなぎ目を誰も確かめていない**」。

### 優先度高: つなぎ目の配線が未検証

1. **429 の結果を同時実行数の制御へ渡す配線**（`call_with_rate_limit`）。`limiter.release("rate_limited")` / `release("ok")` の文字列を壊しても生き残る。制御側（`AdaptiveConcurrencyLimiter`）のテストは自分で `release("rate_limited")` を呼んでいるので通るが、`call_with_rate_limit` が正しい文字列で呼んでいることは確かめていない。壊れると、429 を受けても同時実行数が下がらず全員の一時停止も起きない（rate limit の自動調整が丸ごと効かなくなる）のに、テストは green のまま
2. **SDK の自動再試行を止める HTTP クライアント**（`chat_http_client`）。フックを外す・`None` を返す変異がすべて生存。`test_sdk_does_not_retry_429_itself` はテストの中で自前のクライアントを組み立てており、本番が使う `chat_http_client()` がフックを付けているかは見ていない。壊れると Azure の数ミリ秒の `retry-after-ms` で SDK が送り直しを重ねる、このモジュールが防ぐはずの元の不具合に戻る
3. **工程をまたぐトークン数の合計**（`WorkflowEngine.run`）。`total_token_usage += ...` を `=` にしても `-=` にしても生存。工程ごとのトークン数は見ているが、複数工程を通した合計を確かめるテストが無い。壊れると、レポートに出るトークン数・費用が最後の工程の分だけ、または負の値になる

### 優先度中

4. **再実行時に既存の出力を引き継ぐ表**（`_build_initial_artifacts`）。`relations` / `classifications` / `stances` / `novelty` / `embeddings` / `public_result` / `html` について、名前やファイル名を壊しても生存（45 件の大半）。この表は各プラグインが宣言する出力ファイル名と二重管理になっている。表とプラグインの宣言が一致することを確かめるテストを 1 本足せば、これらがまとめて kill でき、将来のずれも捕まえられる
5. **工程の完了通知の中身**（`on_step_complete` / `on_step_start`）。引数を `None` にしても生存。orchestrator はこの通知で status の `completed_jobs` を更新するので、通知の中身が壊れると管理画面の進捗表示に響く
6. **任意工程のプラグインが無い時**に `continue` を `break` にしても生存（以降の工程が黙って飛ばされる）
7. **待ち時間の計算**（`call_with_rate_limit`）。サーバが送ってきた `retry-after`（60 秒超）を上限 60 秒で切る処理を外しても生存。また、ジッターを固定するテストが `random()` を 0.5 に固定しており、ジッターの係数がちょうど 1 になるので、`backoff * 係数` を `backoff / 係数` に変えても区別できない（テストの固定値の選び方による盲点）
8. **依存関係が不正なワークフロー**（`validate_dependencies` を `None` にする、エラー文言を壊す）。resolver 単体のテストファイルが無く、不正な依存（自己依存・存在しない工程）を `engine.run` が拒否することを確かめていない

### 生存したが実害の無いもの（等価変異）

- HTTP ヘッダ名の大文字化（`retry-after` → `RETRY-AFTER` など）。httpx のヘッダは大小文字を区別しない
- `float("-inf")` → `float("-INF")`、ログ文言・`print` の文字列、上書きされる初期値（`in_degree` の 0 → 1）、全呼び出しが明示する既定引数
- `getattr(error, "code", None)` の既定値を外す変異。呼び出し元は常に `openai.RateLimitError` で、属性が必ずある
- engine の `config.get("user_api_key")`（エラーメッセージからユーザーのキーを伏せる対象）。本番では `ctx.user_api_key` が同じ値を `resolve_user_api_key(config)` から受け取るので、片側を壊しても伏せ字は効く。二重の守りの片側が未検証、という扱い
- `evaluate_condition` の `without_html` キー。orchestrator が `without_html` と `without-html` を常に同じ値に揃えるため、本番経路では区別できない

## やってみて分かった運用上の落とし穴

- **mutmut 3 は既定（`process_isolation = "fork"`）だとこのテスト一式で誤判定する**。初回は 770 件中 220 件が timeout になったが、そのうち 172 件は通常の pytest で流すと全テストが通る（＝本当は生存）変異だった。timeout をすべて「テストが気づいた」と数えるので、kill 率は見かけ上 98% に膨らむ。既に重いライブラリを読み込んだ mutmut 本体から fork すると、子プロセスが止まって時間切れになるのが原因とみられる（どのテストが止まるかまでは特定していない）。`process_isolation = "forkserver"` にすると、通常の pytest で生存と判定した 172 件はすべて生存と出るようになり、時間も 12 分半から 7 分 20 秒に縮んだ
- mutmut 3 は変異させるファイルだけを `mutants/` に複製するので、`also_copy` に `src/` と、テストが `tests/` の 1 つ上から読む `LICENSE` を足さないと収集の段階で落ちる
- 変異を通常の pytest で再現する時は、editable install のせいで元の `src/` が import されるので、`PYTHONPATH=mutants/src` が要る（これを忘れると、どの変異も「生存」に見える）
- 設定は次の形で動いた（実験ブランチの `pyproject.toml` に追記）:

```toml
[tool.mutmut]
paths_to_mutate = ["src/analysis_core/services/rate_limit.py", "..."]
tests_dir = ["tests/"]
also_copy = ["src/", "LICENSE", "README.md"]
pytest_add_cli_args = ["-p", "no:cacheprovider", "-q"]
process_isolation = "forkserver"
```

- 環境: `uv pip install -e ".[clustering,gemini]" pytest mutmut`。`gemini` extra が無いと `test_llm_failure_reporting.py` の収集で落ちる

## 次に見るもの

- 優先度高の 3 件（429 の配線、`chat_http_client`、トークン数の合計）は、それぞれテスト 1 本で kill できる。足すかどうか、Issue にするか PR にするかは判断待ち
- 対象を広げるなら、次は `steps/hierarchical_aggregation.py` と `core/orchestration.py`（再実行の判定）。後者は過去のレビューで回帰が多かった場所（[[code-review-r3-continuation-2026-10-23]]）
- CI に常設するには重い。PR で変更されたファイルだけを対象にする使い方なら現実的

## Open Questions

- fork 方式で止まる原因のテストはどれか（umap / numba のスレッドか、テスト内のスレッドプールか）。forkserver で回避できたので未特定
- 二重管理になっている出力ファイル名の表（`_build_initial_artifacts`）は、テストで一致を固定するのと、プラグインの宣言から組み立てるように直すのと、どちらが良いか

## Updates

- 2026-11-24: 優先度高の 3 件（429 の配線、`chat_http_client`、トークン数の合計）を塞ぐテスト 4 本を PR [#1220](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1220) にした（未 merge、本体のコードは変更なし）。生き残っていた変異 10 件を手で入れ、どれも新しいテストで落ちることを確認した。analysis-core 全体は 876 passed
- 2026-11-24: [#1220](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1220) の CI（Pytest・Ruff・CodeQL・CodeRabbit ほか）は全件 pass。merge 判断の時に見る点: 429 の配線を確かめる 1 本目は、制御側に渡す名前の並び（`rate_limited` / `ok` / `error`）を直接固定しており、実装寄りのテストになっている。特に `error` は制御側がどの分岐でも参照しないので、名前が変わっても振る舞いは変わらない（その部分だけ外す選択肢もある）。振る舞いで確かめる 2 本目（制限が下がってから送り直し、成功で外れる）は `rate_limited` と `ok` を別途 kill している
- 2026-11-24: nishio の指示で [#1220](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1220) を admin merge（squash、main `2a924af6`）。merge 前に CI 全件 pass・CodeRabbit の指摘なしを確認し、merge 後の main で Analysis Core CI・Server Tests・CodeQL ほか全件 success。名前の並びを固定する 1 本目のテストはそのまま入れた
- 2026-11-24: 対象を `core/orchestration.py` と `steps/hierarchical_aggregation.py` に広げた（2,832 変異、kill 率 71.5%）。管理画面の再集約・config の検証・期限切れロックなど本番の穴が多く見つかった。結果は [[mutation-testing-orchestration-aggregation-2026-11-24]]
