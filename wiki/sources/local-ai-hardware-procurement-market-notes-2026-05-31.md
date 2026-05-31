---
type: source
summary: "2026-05-31 時点の local AI hardware 調達 route 検討用 source。RTX 5060 Ti 16GB / RTX 5070 Ti 16GB / RTX PRO 4000 Blackwell 24GB / Mac mini M4 Pro / Foundry Local 公式情報を、広聴AI local box 構想の判断材料として整理"
sources:
  - https://nvidianews.nvidia.com/news/nvidia-blackwell-geforce-rtx-arrives-for-every-gamer-starting-299
  - https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5070-family/
  - https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-4000/
  - https://www.apple.com/mac-mini/specs/
  - https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local
  - https://learn.microsoft.com/en-us/azure/foundry-local/concepts/foundry-local-architecture
---

## 何のソースか

[[local-ai-runtime-user-share-estimate-2026-05-31]] では「既存の普通の業務 PC で local AI を動かせる user share」を見た。この source は、逆に **hardware 調達からやってもらう route** の現実性を判断するための材料である。

## NVIDIA GPU desktop / workstation

NVIDIA は RTX 5060 Ti 16GB を 2025-04 に発表し、16GB 版の starting price を 429 USD としていた。entry / midrange の 16GB VRAM GPU を使えるため、7B〜14B 級 quantized model や local embedding の first spike に使う「広聴AI local box」の最小候補になる。[[local-ai-hardware-procurement-market-notes-2026-05-31]]より

RTX 5070 Ti family は NVIDIA 公式 specs で 16GB GDDR7。より余裕のある 16GB class として、標準 box 候補になる。[[local-ai-hardware-procurement-market-notes-2026-05-31]]より

RTX PRO 4000 Blackwell は NVIDIA 公式 specs で 24GB GDDR7。professional workstation 向けなので consumer GPU より調達・サポート・業務利用説明がしやすく、20B class や大きめ embedding / rerun を見る上位 box 候補になる。ただし費用は consumer route より上がる。[[local-ai-hardware-procurement-market-notes-2026-05-31]]より

## Mac mini / small appliance

Apple Mac mini は M4 / M4 Pro、最大 64GB unified memory まで構成できる。Windows PC ではないが、組織が 1 台の「local analysis appliance」を調達し、利用者は各自の browser からアクセスする route なら OS は必ずしも Windows でなくてよい。[[local-ai-hardware-procurement-market-notes-2026-05-31]]より

この route は「Windows 単一実行ファイル」とは別物になるが、local 完結・API 契約不要・普通の業務 PC から browser で使える、という product value には合う。Mac mini / compact workstation / small tower のどれを採るかは、local model runtime、運用担当者の OS 慣れ、調達ルールで決まる。

## Foundry Local と hardware 調達

Foundry Local は model acquisition、hardware acceleration、model lifecycle、OpenAI-compatible API、optional local server を持つ。調達 route では、「ユーザーの既存 PC に合うか」を広く見るより、Foundry Local で動作確認済みの hardware SKU を数種類に絞り、preload / first-run setup / benchmark を固定できる。[[windows-native-local-ai-docs-2026-05-31]]より

## 含意

- 既存 PC route では user share が問題になるが、hardware 調達 route では share ではなく **SKU 認定と運用責任** が問題になる
- 担当者の PC を高性能化するより、1 台の local box を置き、複数人が browser で使う方が support boundary を切りやすい
- local box route は「単一 exe」ではなくなるが、「API 契約不要」「データを外に出さない」「普通の業務 PC でも使える」を満たせる可能性がある

## Updates

- 2026-05-31: 初版作成。hardware 調達前提の local AI route 判断材料を整理
