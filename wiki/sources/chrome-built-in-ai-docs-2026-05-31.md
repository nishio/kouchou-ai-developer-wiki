---
type: source
summary: "Chrome Prompt API / built-in AI 公式 docs の要点。Gemini Nano を Chrome 内で使い、初回 model download 後は外部送信なしで動く一方、Chrome desktop・storage・RAM/CPU/GPU 条件と browser/API lifecycle への依存がある"
sources:
  - https://developer.chrome.com/docs/ai/prompt-api
---

## 何のソースか

Chrome for Developers の Prompt API docs。Chrome built-in AI は Gemini Nano を Chrome 内で使う API で、`LanguageModel.availability()` や `LanguageModel.create()` から session を作る。model は API 利用時に初回 download され、その後の利用では外部 network が不要で、model 利用時に Google や third party へ data は送信されない、と公式 docs は説明している。[[chrome-built-in-ai-docs-2026-05-31]]より

## 要件

Prompt API / Summarizer / Writer / Rewriter / Proofreader は、Windows 10/11, macOS 13+, Linux, Chromebook Plus などの desktop 条件で動く。Chrome Android / iOS や non-Chromebook Plus ChromeOS は対象外。storage は Chrome profile の volume に少なくとも 22GB free space が必要。CPU だけで動かす場合は 16GB RAM 以上・4 core 以上、GPU の場合は 4GB 超の VRAM が必要、とされる。[[chrome-built-in-ai-docs-2026-05-31]]より

## 広聴AIへの含意

Chrome built-in AI は「browser に既にある local model」を使える可能性があり、API 契約不要・初回 download 後 local 実行という価値には合う。一方で広聴AIの current pipeline は Python/FastAPI 側で batch analysis を走らせるため、Python process から直接 Prompt API を呼べない。使うなら、browser tab が LLM 呼び出しを実行して FastAPI に結果を戻す設計になり、user activation / tab lifecycle / browser support / batch 実行の安定性が主要リスクになる。[[chrome-built-in-ai-docs-2026-05-31]]より

## Updates

- 2026-05-31: 初版作成。Chrome native local LLM route の feasibility 判断材料として公式 docs を整理
