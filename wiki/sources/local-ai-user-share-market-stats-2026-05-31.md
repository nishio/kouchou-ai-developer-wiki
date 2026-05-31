---
type: source
summary: "2026-05-31 時点で local AI runtime のユーザー到達率を推定するための外部統計メモ。Chrome desktop share、Steam Hardware Survey の RAM/CPU/VRAM、Gartner PC shipment、Canalys AI-capable PC forecast、Chrome Prompt API / Foundry Local / Phi Silica 公式要件を整理"
sources:
  - https://developer.chrome.com/docs/ai/prompt-api
  - https://store.steampowered.com/hwsurvey/4?platform=pc
  - https://gs.statcounter.com/browser-market-share/desktop/worldwide/
  - https://www.gartner.com/en/newsroom/press-releases/2026-1-20-gartner-says-worldwide-pc-shipments-increased-9-point-3-percent-in-fourth-quarter-of-2025-and-9-point-1-percent-for-the-full-year
  - https://govsmart.com/wp-content/uploads/2025/06/canalys_now_and_next_for_ai_pcs.pdf
  - https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local
  - https://learn.microsoft.com/en-us/windows/ai/cards/phi-silica-platform-card
---

## 何のソースか

[[node-runtime-free-windows-exe-2026-05-31]] の offline route について、「条件を満たすユーザーがどの程度いるか」を rough estimate するための統計メモ。

## Chrome Prompt API の条件

Chrome Prompt API / Gemini Nano は、Windows 10/11, macOS 13+, Linux, Chromebook Plus などの desktop 環境で、Chrome profile volume に 22GB 以上の空き容量、CPU path では 16GB RAM 以上かつ 4 CPU cores 以上、GPU path では 4GB 超の VRAM が必要。初回 model download には unmetered network が必要で、以後は network 不要・data は Google / third party に送信されない、と公式 docs は説明している。[[chrome-built-in-ai-docs-2026-05-31]]より

StatCounter の desktop browser share では、2026-04 時点の global desktop Chrome share は 71.56%。これは Chrome Prompt API route の上限を決める強い制約である。[[local-ai-user-share-market-stats-2026-05-31]]より

## Hardware proxy としての Steam Hardware Survey

Steam Hardware Survey 2026-04 は gaming / consumer PC に偏るが、公開されている cross-device hardware proxy として使える。Windows users の RAM は 16GB が 40.72%、32GB が 38.53% で、24GB / 28GB / 48GB / 64GB なども合わせると **16GB 以上は約 88%** と見積もれる。CPU cores は 4 cores 未満が少ないため、16GB RAM 以上かつ 4 cores 以上の intersection は **約 85〜88%** と見積もれる。VRAM は 6GB 以上だけで 75% 前後あるが、Chrome Prompt API は CPU path でも動くため、RAM/core 条件の方が支配的。[[local-ai-user-share-market-stats-2026-05-31]]より

ただし、Steam は自治体・企業の貸与 PC より明らかに高 spec 側へ偏る。したがって広聴AIの target user share を見積もる時は、Steam の 85〜88% をそのまま採用せず、かなり保守的に落とす必要がある。

## AI-capable / Copilot+ PC の installed base

Gartner は 2025 年の worldwide PC shipments を 270M+ units とし、Windows 11 upgrade cycle と AI PC promotion が成長要因だったと説明している。ただし同時に、local inference など多くの AI PC features は cloud AI と比べた productivity gain をまだ大きく示せておらず、多くの organization は immediate AI value より future-proofing 目的で upgrade している、と見ている。[[local-ai-user-share-market-stats-2026-05-31]]より

Canalys の AI-capable PC forecast は、2025 年に category 全体で 100M+ devices shipped、2027 年に total 174M、business 向けの 60% 以上が AI-capable になる見通しを示す。ただしこれは shipment forecast であり installed base share ではない。Windows 全体の installed base は 1B+ 〜 1.4B+ devices 規模なので、2026-05 時点の Copilot+ PC / NPU 前提 route は installed base で見るとまだ小さい。[[local-ai-user-share-market-stats-2026-05-31]]より

## Foundry Local / Phi Silica の条件

Foundry Local は user device 上で完結し、runtime は model acquisition / hardware acceleration / lifecycle / cache を扱う。CPU fallback もあり、OpenAI-compatible API と Python SDK を持つため、Chrome share や Copilot+ PC share には縛られない。一方、実際の useful share は選ぶ model size、初回 download 許可、空き容量、組織 policy に依存する。[[windows-native-local-ai-docs-2026-05-31]]より

Phi Silica は Windows Copilot+ PC の NPU 向け local model で、Windows AI APIs から使える。ただし NPU / Copilot+ PC 対象であり、2026-05 時点では broad Windows user 向けの primary route ではなく、将来 option と見るのが妥当。[[windows-native-local-ai-docs-2026-05-31]]より

## Updates

- 2026-05-31: 初版作成。Chrome / Foundry Local / Phi Silica route の user share estimate に必要な統計を整理
