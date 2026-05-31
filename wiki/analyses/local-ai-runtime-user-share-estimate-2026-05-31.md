---
type: analysis
summary: "Chrome Prompt API / Foundry Local / Phi Silica などの local AI runtime を広聴AI Windows offline route に使う場合の到達率推定。Chrome Prompt API は一般 desktop では 45〜55% 程度の可能性があるが、自治体・組織貸与 PC では 20〜40% に落ちる見込み。Foundry Local は first spike 候補、Phi Silica / Copilot+ は当面 1〜5% 級の future option"
sources:
  - local-ai-user-share-market-stats-2026-05-31.md
  - chrome-built-in-ai-docs-2026-05-31.md
  - windows-native-local-ai-docs-2026-05-31.md
  - node-runtime-free-windows-exe-2026-05-31.md
---

## 問い

[[node-runtime-free-windows-exe-2026-05-31]] の offline route で、Chrome Prompt API / Foundry Local / Phi Silica などの条件を満たす user share はどの程度か。

## 結論

2026-05-31 時点の rough estimate は次の通り。

| route | 一般 desktop / consumer 寄り | 広聴AI target の自治体・組織貸与 PC 寄り | 判断 |
|---|---:|---:|---|
| Chrome Prompt API / Gemini Nano | 45〜55% | 20〜40% | 便利だが primary backend にしない |
| Foundry Local + small model | 50〜70% | 25〜50% | first spike 候補 |
| Foundry Local + 7B 級 quality target | 15〜35% | 5〜20% | optional quality route |
| Phi Silica / Copilot+ PC / NPU | 2〜6% | 1〜5% | future option |
| 20B class local model を快適に動かす | 5〜15% | 1〜5% | 現時点の標準 route には早い |

この推定は public web / hardware statistics からの rough model であり、広聴AIの実ユーザー計測ではない。特に Steam Hardware Survey は consumer/gamer PC に偏るため、自治体・企業端末には高すぎる proxy である。[[local-ai-user-share-market-stats-2026-05-31]]より

## Chrome Prompt API

Chrome Prompt API の公式条件は desktop Chrome、22GB free storage、CPU path で 16GB RAM 以上かつ 4 CPU cores 以上、または GPU path で 4GB 超 VRAM、初回 download 用の unmetered network である。Chrome desktop share は global で 71.56% 程度。Steam Hardware Survey を proxy にすると、16GB RAM 以上かつ 4 cores 以上は 85〜88% 程度ある。単純積では `0.7156 * 0.85〜0.88 = 61〜63%` だが、ここから Chrome version / API availability / 22GB free storage / 組織 policy / user activation / long-running batch 失敗を引く必要がある。[[local-ai-user-share-market-stats-2026-05-31]]より

したがって、一般 desktop / consumer 寄りでは day-one usable が 45〜55% 程度、自治体・組織貸与 PC では Chrome install / policy / RAM 8GB 端末 / 空き容量で 20〜40% 程度まで落ちる、と見るのが妥当。Chrome Prompt API は「使える人には便利」だが、広聴AIの標準 offline backend にするには user share と batch lifecycle の両方が弱い。[[chrome-built-in-ai-docs-2026-05-31]]より

## Foundry Local

Foundry Local は Chrome share に縛られず、Python SDK / OpenAI-compatible endpoint / embeddings / model lifecycle 管理を持つ。小さい model (`qwen2.5-0.5b` のような smoke-test class) なら 16GB RAM / 4 cores / 空き容量 / 初回 download が通る端末で動く可能性が高く、一般 desktop では 50〜70%、自治体・組織貸与 PC では 25〜50% 程度を初期 target share と見る。[[windows-native-local-ai-docs-2026-05-31]]より

ただし、広聴AIの label / summarization quality を満たす 7B 級以上に上げると、latency と memory が支配的になる。一般 desktop でも useful share は 15〜35%、自治体・組織貸与 PC では 5〜20% 程度まで落ちる可能性が高い。つまり Foundry Local は first spike として自然だが、最初の success criteria は「small sample report が local で完走する」であり、API route と同等品質を即要求しない方がよい。[[local-ai-user-share-market-stats-2026-05-31]]より

## Phi Silica / Copilot+ PC

Phi Silica は Copilot+ PC / NPU 前提の Windows native route であり、platform direction としては魅力的。ただし Canalys の AI-capable PC forecast は shipment の伸びを示すもので、installed base share ではない。2026-05 時点の Windows installed base 全体から見ると Copilot+ PC / NPU 条件を満たす user は数%級に留まると推定するのが妥当。広聴AIの target user は組織貸与 PC が多く、導入サイクルも遅いため 1〜5% 程度と見る。[[local-ai-user-share-market-stats-2026-05-31]]より

## 20B class model

20B class model は「品質が現実的になってきた」という期待はあるが、Windows 単一実行ファイルの標準 route とは別に扱うべき。32GB RAM 以上、十分な memory bandwidth、dGPU / NPU / fast CPU、空き容量、長い初回 download を許容できる user は consumer/gamer でも一部に留まる。広聴AIの target user share は 1〜5% 程度と見て、標準 offline route ではなく power user / researcher 向け option に置くのが安全。[[local-ai-user-share-market-stats-2026-05-31]]より

## 実装判断

- `#885` の first spike は Foundry Local + small model + embeddings を優先する
- Chrome Prompt API は batch backend ではなく client-side 補助や browser-only experiment に限定して検証する
- Phi Silica / Windows AI APIs は future option として観測し、Copilot+ PC user share が十分増えるまで標準 route にしない
- offline route の UX は「高品質 API route」と「local privacy / no API contract route」を明確に分け、local route には quality / latency warning を出す

## Open Questions

- Foundry Local の model catalog で日本語 label / summarization に最低限使える候補は何か
- 広聴AI target user の実機 spec は、自治体・政党・市民団体のどの層を見ればよいか
- Chrome Prompt API の browser-only 実験は、analysis pipeline ではなく preflight / 入力要約 / sample preview に使う方がよいか

## Updates

- 2026-05-31: 初版作成。Chrome / Foundry Local / Phi Silica route の user share を rough estimate
