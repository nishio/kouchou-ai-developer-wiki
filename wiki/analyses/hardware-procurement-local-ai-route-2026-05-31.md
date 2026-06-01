---
type: analysis
summary: "広聴AIの API 契約不要 local 完結を、既存業務 PC ではなく hardware 調達込みで実現する route の整理。担当者 PC を高性能化するより、認定済み local box / appliance を 1 台置いて browser から使わせる方が現実的。単一 exe とは別物だが、自治体・組織向け pilot には筋が良い"
sources:
  - local-ai-runtime-user-share-estimate-2026-05-31.md
  - local-ai-hardware-procurement-market-notes-2026-05-31.md
  - node-runtime-free-windows-exe-2026-05-31.md
  - windows-native-local-ai-docs-2026-05-31.md
  - meeting-minutes.md
---

## 問い

普通の業務 PC で local LLM を動かすのが茨の道なら、hardware 調達からやってもらう route はどうか。

## 結論

かなり現実的になる。ただし、目標は「担当者の Windows PC で単一 exe」ではなく、**認定済み local box / appliance を 1 台置き、担当者は普通の PC から browser で使う** route に切り替えるのがよい。

この route は、単一 exe 配布の問題を「全ユーザーの既存 PC で動くか」から「こちらが認定した数 SKU で確実に動くか」に変える。ユーザーの hardware share 問題は消える一方、調達、資産管理、設置、更新、故障対応、セキュリティ review、モデル更新責任が新しい論点になる。[[local-ai-runtime-user-share-estimate-2026-05-31]]より

## 推奨 route

最も筋が良いのは **広聴AI Local Box** route。

- 組織が推奨 hardware を 1 台調達する
- その box に FastAPI + static assets + local model runtime + model cache を載せる
- 利用者は普段の業務 PC から `http://local-kouchou-ai/` のように browser でアクセスする
- データは LAN / box 内に留め、OpenAI / Gemini API 契約なしで小〜中規模分析を完走させる
- 高品質が必要な時だけ API route に切り替える、または別 profile にする

この構成なら、担当者の PC は 8GB RAM の事務用 Windows でもよい。重い local inference は box 側で吸収し、support target も「認定 box」だけになる。[[local-ai-hardware-procurement-market-notes-2026-05-31]]より

2026-06-01 定例でも、来年くらいに local LLM で動く時代が来ると、Talk to the City 的なアルゴリズムの **large context を要求しない** 性質が強みに化ける、という見方が共有された。ローカルマシン / local LLM で完結すれば、データを外部に出さずに分析できる。tokoroten は `RTX Spark（RTX5070相当＋20コアARM＋128GBメモリ）` のような認定 hardware で動くと言えると楽、と例示しており、これは本ページの local box route と整合する。[[meeting-minutes]]より

## Hardware tier

| tier | 目安 | 役割 |
|---|---|---|
| Demo box | 16GB VRAM GPU, 64GB RAM, 1〜2TB SSD | 小さな sample / 100〜500 件規模の local 完走確認 |
| Standard local box | 16〜24GB VRAM GPU, 64〜128GB RAM, 2TB SSD | 7B〜14B 級 quantized model と local embeddings の実用検証 |
| High-memory box | 24GB+ VRAM GPU or 64GB+ unified memory | 20B class、複数 workflow、重い rerun の研究・pilot |

2026-05 時点の具体候補としては、RTX 5060 Ti 16GB が entry 16GB VRAM、RTX 5070 Ti が余裕のある 16GB VRAM、RTX PRO 4000 Blackwell が professional 24GB VRAM の候補になる。Mac mini M4 Pro / 64GB unified memory も、Windows にこだわらず appliance として置くなら候補になる。[[local-ai-hardware-procurement-market-notes-2026-05-31]]より

## 単一 exe route との関係

この route は「Windows user が exe を 1 個 download して自分の PC で動かす」話ではない。むしろ、単一 exe route の難点を避けるために、運用境界を box に移す案である。

| 観点 | 単一 exe / 既存 PC | local box / hardware 調達 |
|---|---|---|
| 導入 | download だけなら軽い | 調達・設置が要る |
| 動作保証 | PC 差分が大きい | 認定 SKU に絞れる |
| local privacy | 端末内 | 組織 LAN / box 内 |
| API 契約不要 | model 同梱 / download が必要 | preload / cache しやすい |
| サポート | 個別 PC と AV / policy が地獄 | box image と SKU を見る |
| 普通の業務 PC | spec 不足で厳しい | browser client だけなら可 |

したがって、非専門家向け普及の本線は「既存 PC で local LLM」ではなく、**SaaS route / API route / local box route** の 3 本に分けた方がよい。[[node-runtime-free-windows-exe-2026-05-31]]より

## 実装順

1. Foundry Local + small model + embeddings で、sample report が local box 上で完走するかを見る
2. 同じ box に FastAPI static serving を載せ、普通の client PC から browser で作成・進捗・閲覧できるかを見る
3. 100 / 500 / 1000 件の wall-clock、メモリ、品質を測る
4. 認定 hardware tier と dataset size guidance を docs にする
5. API route との品質差を UI で明示する

ここでの success criteria は「OpenAI/Gemini と同品質」ではなく、「API 契約不要で小〜中規模 pilot を完走し、出力品質の限界が説明できる」である。

## Open Questions

- local box を誰が調達・保守するのか。DD2030 が推奨 SKU を出すだけか、貸し出し / appliance 提供まで踏み込むか
- local box の OS は Windows にするか、Linux / macOS appliance も許すか
- 自治体ネットワークで LAN 内 web service を立てることの security review はどの程度重いか
- model download を初回起動時に許すか、事前 preload 済み image として配るか
- `RTX Spark` のような具体 SKU / appliance を候補として扱う場合、実在スペック・供給時期・価格・日本国内調達性を別途一次情報で確認する必要がある

## Updates

- 2026-05-31: 初版作成。既存業務 PC ではなく hardware 調達込みで API 契約不要 local 完結を実現する route を整理
- 2026-06-01: 定例議事録を反映し、local LLM 時代には TTTC 的な large context 不要アルゴリズムが強みになること、認定 hardware で「これで動く」と言える route が有効であることを追記
