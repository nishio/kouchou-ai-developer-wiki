---
type: source
summary: `PR #824` merge 後の current `main` では analysis 実行経路は full URL な LOCAL LLM を受け取れるが、admin の model list probe はまだ `host:port` + `http://` 前提という観測メモ
sources:
  - source-code.md
  - github-dev-docs.md
---

2026-05-19 に `digitaldemocracy2030/kouchou-ai` の `PR #824` と current `origin/main@55e93e1` を確認した観測メモ。GitHub 上の merge metadata、`analysis-core` / legacy pipeline / admin API の current 実装を見比べた。[[github-dev-docs]]より [[source-code]]より

## Observations

- GitHub 上の `PR #824` は `state: merged`、`mergedAt: 2026-05-18T14:00:00Z`、merge commit は `8ab85068236606e0f83803066b9e675d73cf7791`
- current `packages/analysis-core/src/analysis_core/services/llm.py` には `_resolve_local_llm_base_url(address)` があり、`host:port` 互換を保ちながら `https://gateway.example.com` のような full URL も受け付け、末尾に `/v1` を補う
- 同ファイルの `request_to_local_llm()` / `request_to_local_llm_embed()` は `LOCAL_LLM_API_KEY` を参照するため、認証付き OpenAI 互換 gateway も想定した実装になっている
- `packages/analysis-core/tests/test_local_llm_base_url.py` には `https://...` / `https://...:8443` / `/openai` path 付き URL まで含むテストが追加されている
- legacy 側の `apps/api/broadlistening/pipeline/services/llm.py` にも同じ helper と `LOCAL_LLM_API_KEY` 対応が入っている
- current `apps/api/src/services/report_launcher.py` は `local_llm_address` を config に渡して `python -m analysis_core` を起動するので、**実際の分析実行経路は current `main` で HTTPS/full-URL 対応済み** と読める
- ただし current `apps/api/src/services/llm_models.py` の `get_local_llm_models()` はなお `address` を `host[:port]` として解釈し、`http://{host}:{port}/v1` を組み立てる
- `apps/api/src/routers/admin_report.py` の `/admin/models` はこの `get_local_llm_models()` を使うため、**admin 画面での LocalLLM モデル一覧取得は full URL / HTTPS gateway にまだ追随していない**

## Open Questions

- `/admin/models` でも `_resolve_local_llm_base_url()` 相当の共通 helper を使うべきか
- schema comment や UI 文言の `127.0.0.1:1234` 例を、full URL も許容する説明へ広げるべきか

## Updates

- 2026-05-19: 初版作成
