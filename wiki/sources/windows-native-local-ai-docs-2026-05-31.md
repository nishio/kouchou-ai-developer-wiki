---
type: source
summary: "Microsoft 公式 docs から見た Windows native local AI の要点。Phi Silica は Copilot+ PC / NPU 向け Windows AI APIs、Foundry Local は Python SDK・OpenAI-compatible endpoint・embeddings・model lifecycle 管理を持つ local runtime で、広聴AIには Foundry Local が特に接続しやすい"
sources:
  - https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local
  - https://learn.microsoft.com/en-us/azure/foundry-local/how-to/how-to-integrate-with-inference-sdks
  - https://learn.microsoft.com/en-us/azure/foundry-local/how-to/how-to-generate-embeddings
  - https://learn.microsoft.com/en-us/azure/foundry-local/concepts/foundry-local-architecture
  - https://learn.microsoft.com/en-us/windows/ai/cards/phi-silica-platform-card
  - https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai
---

## 何のソースか

Microsoft 公式 docs の Windows native local AI 関連。[[slack-local-llm-native-runtime-2026-05-31]] の「Chrome や Windows が LLM を native support し始めている」論点について、広聴AIの Windows 単一実行ファイル / local 完結 route に関係する部分だけを整理する。

## Foundry Local

Foundry Local は、user device 上で完結する local AI application を shipping するための runtime / SDK で、C# / JavaScript / Rust / Python SDK、curated model catalog、自動 hardware acceleration を持つ。公式 docs は、user data は device から出ず、offline で動き、per-token cost や backend infrastructure は不要と説明している。OpenAI-compatible API もあり、既存 OpenAI SDK 利用アプリは local endpoint へ向け替える設計ができる。[[windows-native-local-ai-docs-2026-05-31]]より

Python では `foundry-local-sdk-winml` または `foundry-local-sdk` を使い、model download / load 後に OpenAI-compatible local REST endpoint を起動できる。初回実行時には model や execution provider の download が数分かかる場合がある。Foundry Local は text embeddings API も持ち、Windows package は Windows ML runtime と統合される。[[windows-native-local-ai-docs-2026-05-31]]より

architecture docs では、Foundry Local は application が platform-specific native library を in-process に load し、model lifecycle、hardware abstraction、local cache を扱う構造とされる。HTTP が必要な場合だけ optional OpenAI-compatible REST endpoint を起動できる。これは current kouchou-ai の `provider="local"` が OpenAI-compatible endpoint を叩く構造と相性がよい。[[windows-native-local-ai-docs-2026-05-31]]より [[source-code]]より

## Phi Silica / Windows AI APIs

Phi Silica は Windows Copilot+ PC の NPU 向けに optimized された local language model で、Windows AI APIs / Windows App SDK から text generation, summarization, rewrite などに使える。platform card は local 実行・privacy・speed を利点として説明する一方、対象は Copilot+ PC / NPU を備えた device で、unsupported PC では available でない可能性がある。[[windows-native-local-ai-docs-2026-05-31]]より

Microsoft.Windows.AI namespace docs では、該当 API は Windows App SDK experimental channel であり、breaking changes や removal の可能性があり、production support / Microsoft Store publish の制約があると明記されている。したがって、2026-05-31 時点で広聴AIの primary backend として直ちに採用するより、Windows native local AI の将来 route として観測する位置づけが妥当。[[windows-native-local-ai-docs-2026-05-31]]より

## 広聴AIへの含意

- Foundry Local は Python SDK、OpenAI-compatible endpoint、embeddings、model lifecycle 管理が揃っており、current `provider="local"` と接続しやすい
- 「モデルを exe に直接同梱する」より、「runtime は package に入れ、model は初回 download / local cache」に寄せる route を作れる可能性がある
- Phi Silica / Windows AI APIs は privacy / NPU acceleration の方向性は合うが、Copilot+ PC 依存と experimental API 制約により、まずは benchmark / future option として扱うのが安全

## Updates

- 2026-05-31: 初版作成。Windows native local AI route の feasibility 判断材料として公式 docs を整理
