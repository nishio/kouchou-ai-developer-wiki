---
type: analysis
summary: "Issue #707 は 2026-05-21 に close され、backend の provider-aware verify 実装が current main で非再現だったことから、元報告は stale bug と判断された"
sources:
  - github-dev-docs.md
  - source-code.md
  - open-issues-snapshot-2026-05-19.md
---

`Issue #707` は 2026-05-21 に close された。close 前に current `main` を一次参照すると、当初の「Azure 環境でも常に OpenAI として接続チェックしてしまう」形の実装はそのままでは残っておらず、verify endpoint でも provider 取り違えは非再現だった。したがってこの issue は、**current tree では解消済みの stale bug report** と読むのが妥当である。[[github-dev-docs]]より [[source-code]]より

## Findings

### GitHub current state では #707 は close 済み

`gh issue view` では `#707 [BUG]APIが利用可能であってもAPI接続チェックが失敗する` は 2026-05-21 に close 済みで、close コメントには current `main@14e9772987b95af816d33e9fe09315715ac200b9` で `/admin/environment/verify?provider=azure` が内部で `provider="azure"` を渡していること、少なくとも当初の原因は非再現であることが書かれている。[[github-dev-docs]]より

### current main の backend verify endpoint は provider-aware に統合済み

`work/kouchou-ai/` の current `origin/main` を見ると、`apps/api/src/routers/admin_report.py` には `/admin/environment/verify?provider=...` があり、`request_to_chat_ai(..., provider=provider)` を呼んでいる。`provider == "azure"` のとき `packages/analysis-core/src/analysis_core/services/llm.py` は `request_to_azure_chatcompletion()` へ分岐し、実際の deployment 名は `AZURE_CHATCOMPLETION_DEPLOYMENT_NAME` から取る。つまり、issue コメントで指摘されていた「provider 未指定のため常に OpenAI」そのものは current code では解消済みと読める。[[source-code]]より

### ただし admin UI には Azure 特別扱いの痕跡が残る

`apps/admin/app/create/components/AISettingsSection.tsx` には `TODO: azure の場合は別の方法が必要そうなので別途対応する` が残っており、Azure では user API key 入力欄を出していない。また `EnvironmentCheckDialog/verifyApiKey.ts` には current `/admin/environment/verify` 実装とは別に、未使用に見える旧 `verify-chatgpt` 呼び出し関数も残っている。したがって current risk は backend の provider 固定 bug そのものより、**Azure path の UI/テスト整理不足** にある。[[source-code]]より

### テストは OpenAI / Gemini のみで、Azure verify regression を直接は塞げていない

`apps/api/tests/routers/test_admin_report.py` には `provider=openai` と `provider=gemini` の verify test はあるが、Azure 用の verify test は見当たらない。そのため、実装が provider-aware になっていても、`#707` 型 regression を CI で防げているとはまだ言い切れない。[[source-code]]より

### 優先度整理としては「provider / API 接続チェック統合問題」の一部という旧判断は still useful だが、個別 issue としてはクローズ済み

既存 wiki では `#707` `#681` `#473` を provider / API 接続チェック設計の束として扱っていた。この読み自体はまだ妥当だが、`#707` 単体は current main で非再現として close されたので、今後の active な論点は `#681` など **remaining provider UX / validation issues** へ寄る。[[open-issues-snapshot-2026-05-19]]より

## Open Questions

- Azure 環境で admin UI の「API接続チェック」ボタンを実際に押した end-to-end 再現は、2026-05-21 時点でまだ取れていない
- 旧 `verify-chatgpt` 呼び出し関数が本当に dead code なら削除すべきか、それとも別 UI からまだ参照されるのか
- Azure verify regression test を別 issue に切るべきか、それとも `#681` など既存の provider UX issue に吸収すべきか

## Updates

- 2026-05-21: 初版作成
- 2026-05-21: current `main` で provider 取り違えが非再現だったことを受け、GitHub 上で `#707` が close されたことを反映
