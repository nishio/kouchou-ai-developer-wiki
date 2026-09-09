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

### ユーザー判断：再試行をマージ条件から外す

- Flexは時間より費用を優先する用途なので、待ち時間の増加はドキュメントの注釈で十分というユーザー判断。上記P2は修正必須という扱いを撤回し、実装変更をマージ条件としない。
- 料金説明では、リソース不足で失敗したリクエストは課金されないことと、標準処理への切替後は通常料金になることを区別する。通常料金への自動切替の是非は、複数変更を含む#934のマージ後に別途議論する。
- ユーザーのマージ指示で確認済みHEADを指定して通常マージを試みたが、GitHubのブランチ保護（REVIEW_REQUIRED）で拒否された。管理者マージは未実施で、PRは未merge。

### 2026-09-09 15:41 JST — マージ完了

ユーザーの明示承認を受け、確認済みHEADを指定して管理者マージを実行。[PR #934](https://github.com/digitaldemocracy2030/kouchou-ai/pull/934)の状態を再取得し、MERGED、merge commit `c2390a10094ccaa9baf9072f489eb1424059f852` を確認した。上記のレビュー待ちは解消。通常料金への自動切替の是非と料金を含む説明は、別途議論する未決事項として残す。
