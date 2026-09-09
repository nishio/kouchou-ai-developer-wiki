---
type: analysis
summary: "PR #934 の最新HEADをレビュー。既存指摘は修正済みだが、OpenAI SDKの再試行とTenacityが重なり最大4回の説明に対して12回のHTTP送信を再現"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/934
  - https://developers.openai.com/api/docs/guides/flex-processing
---

## 観測と結論

2026-09-09 14:51 JST、[PR #934](https://github.com/digitaldemocracy2030/kouchou-ai/pull/934) の HEAD `2771367a959f061675fd12bf18f79dce1ee5d32d` を確認。open / non-draft / review required。実行されたCIチェックは成功、docs deployはskip。mainはfetch / fast-forward確認後 `775e0f5ce9339ab7a2caf66156fdc09480719e65`。#917を置き換える意図のPRだが未mergeである。

PR差分より、temperature省略、Flex判定、900秒timeout、resource_unavailableだけを対象とするdefault tierへの切替を確認。既存レビューの通常429との区別、Flexへ戻らない再試行、空timeoutの扱いは最新HEADで修正済み。PR本文はautoへの切替と書かれたままだが、実装はdefaultに更新されている。

## 追加指摘（P2）

`_send_openai_chat_request` のTenacityはSDKが例外を返してから動く。`OpenAI()`のSDK内再試行を無効化していないため、resource_unavailableを即座に呼出側へ返す意図と、ドキュメントの最大4リクエストという説明がHTTP送信数と一致しない。

ローカルのOpenAI SDK 2.37.0（max_retries=2）とhttpx.MockTransportを使用し、Flexには429 resource_unavailable、defaultには429 rate_limit_exceededを返すと、HTTP送信は `flex × 3 → default × 9` の計12回になった。sleepだけを抑止し、実API・実キーは使用していない。既存のMagicMockベースのテストではSDK内再試行を通らない。

修正候補はOpenAI経路の再試行の責任範囲を整理すること。SDK側をmax_retries=0にするなら、従来SDKが扱うtimeout / connection / 5xxの扱いも明示する。HTTP transportまで通したテストでFlex切替と送信回数を検証する。

[OpenAI公式Flexガイド](https://developers.openai.com/api/docs/guides/flex-processing)より、15分timeoutとリソース不足時の標準処理への再送方針自体は整合している。

ローカルでPR側のanalysis-coreをPYTHONPATHに指定し、`tests/services/test_llm.py` は76 passed（41.08秒）。設定に必要なキーはダミー値を使用。通常テストの成功とSDK transport検証で見つかった問題を区別する。

## Open Questions

- SDK内部の再試行を維持するのか、アプリ側へ集約するのか。
- 実APIでの動作確認はPR作者の報告を参照。今回のレビューでは再実施していない。

## Updates

- 2026-09-09: 最新差分、CI、既存レビューを観測し、SDK経由の追加検証を実施。GitHubへのレビュー投稿・コード修正・mergeは行っていない。
