---
name: llm-providers
summary: 対応 LLM プロバイダ — OpenAI / Azure OpenAI / Gemini / OpenRouter / LocalLLM (Ollama)
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - source-code.md
---

## 対応プロバイダ

| プロバイダ | 主な env var | 備考 |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | デフォルト想定 |
| Azure OpenAI | `AZURE_CHATCOMPLETION_*`, `AZURE_EMBEDDING_*` | **`AZURE_OPENAI_*` ではない** ([[gotchas]]) |
| Gemini | `GEMINI_API_KEY` | AkioPonkotu さんの PR 由来、継続改善 |
| OpenRouter | `OPENROUTER_API_KEY` | 他社モデルへのルーティング |
| LocalLLM (Ollama) | `--profile ollama` | 既定モデル `hf.co/elyza/Llama-3-ELYZA-JP-8B-GGUF` |
| LM Studio 等 | "LOCAL LLM" 扱い | PR #422 で [[tokoroten]] が一般化 |

## なぜ複数プロバイダ対応か

[[meeting-minutes]] 2025-04 〜 2025-08 で繰り返し議論されている：

- 日本の自治体は **クレジットカード／$ 決済／海外 API 利用ルール** で OpenAI 直契約が困難
- 郡山市など LGWAN 環境では外部 API そのものが使えない（→ 結局非対応）
- OpenRouter / LocalLLM はその回避策
- API キー入力フォーム（Issue #660）も同文脈

## LOCAL LLM の HTTPS 問題（2026-05）

[[meeting-minutes]] 2026-05-18 見出し / PR #824：

> OpenAI や Azure AI Service ではないモデルを叩くとき「LOCAL LLM」という扱いになっているが、これが HTTP を暗黙に仮定してたので **HTTPS の別サービスを叩くことができない**。

= `main@3809a7a` のコードでは、`packages/analysis-core/src/analysis_core/services/llm.py` と `apps/api/src/services/llm_models.py` が今も `http://{host}:{port}/v1` を組み立てている。したがって、**議事メモ上で修正報告はあるが、main で HTTPS URL を自然に扱えるとはまだ断定しない方が安全**。  
= "LOCAL" という命名が実装にバイアスを与えていた古典的なケースであり、今後も類似の hidden assumption を疑う材料。

## 埋め込みモデル

- 既定の `small` は精度に不満あり（Issue #450）
- `large` への切り替えや SentenceTransformer ベースの代替が希望されている
- `WITH_GPU=true` 時は GPU 推論

## API キーフォーム入力

Issue #660（2025-07-30 マージ）— OpenAI / OpenRouter のキーを管理者画面のフォームから渡せる。デモ環境の「公開のためにはユーザ自身のキーを入れさせる」要件（2025-06-23 board）に対応。

## Open Questions

- Embedding モデルのデフォルト変更（精度 vs コスト vs 一貫性）
- 「LOCAL LLM」というカテゴリ名そのものを「self-hosted endpoint」等にリネームすべきか

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を確認し、LOCAL LLM の HTTPS 対応は「議事メモ上の報告あり・main 反映は要再確認」という書き方に修正
