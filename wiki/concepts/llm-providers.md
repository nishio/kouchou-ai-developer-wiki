---
name: llm-providers
summary: "対応 LLM プロバイダ — OpenAI / Azure OpenAI / Gemini / OpenRouter / LocalLLM (Ollama/LM Studio 等)。Windows local 完結 route では Foundry Local / Chrome built-in AI / Windows AI APIs も候補だが、2026-05-31 時点では未実装"
type: concept
sources:
  - github-dev-docs.md
  - meeting-minutes.md
  - source-code.md
  - windows-native-local-ai-docs-2026-05-31.md
  - chrome-built-in-ai-docs-2026-05-31.md
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

## Local provider の次候補 (未実装)

Windows 単一実行ファイル / API 契約不要 route では、Foundry Local が current `provider="local"` に最も接続しやすい候補である。Foundry Local は Python SDK、OpenAI-compatible local endpoint、embedding API、model download/cache 管理を持つため、既存の OpenAI-compatible local LLM 経路に近い。ただし 2026-05-31 時点では広聴AI main には未実装で、model catalog の日本語品質、license / redistribution、first-run download UX、preview maturity の確認が必要。[[windows-native-local-ai-docs-2026-05-31]]より [[source-code]]より

Chrome Prompt API / Gemini Nano は browser 内 local model として有望だが、Python/FastAPI の batch pipeline から直接使う provider ではない。client-side 補助や browser-only 実験には向くが、分析 backend として使うには browser tab lifecycle と user activation を抱える。[[chrome-built-in-ai-docs-2026-05-31]]より

Phi Silica / Windows AI APIs は Copilot+ PC / NPU 向けの Windows native local model route だが、experimental channel や supported device 制約があるため、現時点では primary provider ではなく future option として観測する。[[windows-native-local-ai-docs-2026-05-31]]より

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
- Foundry Local を `provider="local"` の単なる endpoint として扱うか、first-class provider として model download/cache/progress UI まで持つか

## Updates

- 2026-05-31: Windows local 完結 route の候補として Foundry Local / Chrome Prompt API / Phi Silica を追記。Foundry Local は現行 OpenAI-compatible local endpoint に接続しやすいが未実装
- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を確認し、LOCAL LLM の HTTPS 対応は「議事メモ上の報告あり・main 反映は要再確認」という書き方に修正
