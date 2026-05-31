---
type: analysis
summary: "Windows 単一実行ファイル配布を再評価する前提として、Web UI の Node runtime を build-time の frontend assets に押し込み、runtime を Python/FastAPI + static assets に寄せる案は段階的には実現可能。MVP は外部 API route と API 契約不要の offline route を比較し、offline は自前 bundled-model だけでなく Chrome / Windows native local AI runtime も見るべき"
sources:
  - slack-windows-single-exe-2026-05-31.md
  - source-code.md
  - nextjs-static-export-docs-2026-05-31.md
  - windows-distribution-options.md
  - github-dev-docs.md
  - slack-local-llm-native-runtime-2026-05-31.md
  - chrome-built-in-ai-docs-2026-05-31.md
  - windows-native-local-ai-docs-2026-05-31.md
  - local-ai-runtime-user-share-estimate-2026-05-31.md
---

## 問い

[[windows-distribution-options]] では、完全な単体 exe は Python API と Next.js/Node runtime の両方を抱えるため保守コストが大きい、と整理していた。今回の問いは、[[slack-windows-single-exe-2026-05-31]] の発想どおり **Node runtime を build-time に閉じ込め、runtime を Python/FastAPI + static assets へ寄せれば、Windows 単一実行ファイル配布の実現可能性は上がるか** である。

## 結論

段階的には実現可能と見る。current main では、domain logic と analysis 実行は既に `apps/api` / `packages/analysis-core` 側にあり、Node runtime の主な責務は Next.js の server-side wrapper と static-site-builder の薄い build wrapper に寄っている。つまり「Python に移植すべき server logic」は巨大な業務ロジックではなく、かなりの部分が既存 FastAPI endpoint への proxy / fetch / cache invalidation / static build 起動である。[[source-code]]より

ただし、これは「完全単体 exe がすぐ作れる」という意味ではない。実装単位としては、まず **runtime Node なしで Web UI を動かす** ところを切り出し、その後で PyInstaller / Nuitka などの Windows packaging spike に進むのが妥当である。GitHub issue は `#885` として起票した。[[slack-windows-single-exe-2026-05-31]]より

## current main の Node runtime 責務

`apps/admin` は `next.config.ts` で `output: "standalone"` を使い、Node runtime 前提の Next app として動いている。Node server 側に残っている主なものは、トップページの server-side fetch、11 個の `"use server"` actions、3 個の route handlers (`/api/download`, `/api/admin/reports/[slug]/config`, `/api/healthcheck`)、CSP headers である。これらの多くは既存 FastAPI endpoint を呼ぶ薄い wrapper なので、client fetch + shared API client または FastAPI への移設で置き換え可能に見える。[[source-code]]より

`apps/public-viewer` は `NEXT_PUBLIC_OUTPUT_MODE=export` で static export できる経路を既に持つ。一方、通常 runtime では page の server-side fetch と `revalidateTag` route を使っており、Next.js の server/cache runtime に依存する部分がある。Node runtime を消すなら、live viewer を static assets + client fetch へ寄せるか、local desktop MVP では admin からの閲覧と static zip 出力の扱いを別途決める必要がある。[[source-code]]より [[nextjs-static-export-docs-2026-05-31]]より

`apps/static-site-builder` は Express で `/build` を受け、`pnpm run build:static` を実行して `apps/public-viewer/out` を zip するだけである。この API 自体は Python/FastAPI に移せる。ただし runtime に `pnpm run build:static` を残すなら Node runtime 同梱問題が戻るため、本当に単一 exe を狙うなら「事前ビルド済み public-viewer assets で足りるか」「Python で静的レポート zip を生成するか」を切る必要がある。[[source-code]]より

## 実装の切り方

第一段階は `apps/admin` の SPA/static assets 化。server actions を client fetch に移し、`app/page.tsx` の初期一覧 fetch も client 側に寄せる。`/api/admin/reports/[slug]/config` は既に FastAPI に `/admin/reports/{slug}/config` があるため、Next route handler を経由しない形にできる。`/api/download` だけは static export の設計判断が必要なので別 slice に分ける。[[source-code]]より

第二段階は FastAPI に static serving を持たせること。prebuilt admin assets と public-viewer assets を FastAPI が配信し、API と UI を 1 port に寄せる。これにより CORS と base path の問題を単純化できるが、CSP headers は Next `headers()` から Python 側へ移す必要がある。[[source-code]]より [[nextjs-static-export-docs-2026-05-31]]より

第三段階は Windows packaging spike。ここは当初「OpenAI/Gemini API、local storage、CPU、localhost、Docker なし」を最小 MVP と見ていたが、nishio 指摘により、単一実行ファイル配布の価値は **API 契約なしで local 完結できること**にもあると修正した。したがって `#885` の MVP は、(1) artifact を小さくし品質を優先する external API route と、(2) local 完結を優先する offline route の 2 本を比較する形に更新した。さらに offline route は、自前で lightweight chat / embedding model を同梱するだけでなく、Chrome / Windows の native local AI runtime を使う route も見る必要がある。[[github-dev-docs]]より [[slack-local-llm-native-runtime-2026-05-31]]より

## 同梱モデル route

current code には `provider="local"` の OpenAI 互換 local LLM 経路と、`is_embedded_at_local` の SentenceTransformer local embedding 経路が既にある。`request_to_local_llm()` は Ollama / LM Studio のような OpenAI 互換 endpoint を叩き、`request_to_local_embed()` は `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` を遅延ロードする。つまり「local inference を使うための抽象」は既にある。[[source-code]]より

ただし、これはそのままでは「同梱モデル」ではない。現状の local LLM は外部 runtime (Ollama / LM Studio など) を前提にし、local embedding は Hugging Face cache / 初回 download に寄る。Windows 単一実行ファイルで API 契約不要・ネットワーク不要を目指すなら、モデルファイルを配布物に含めるか初回起動時 download にするか、package 内の local path からロードするか、推論 runtime を Python 内に持つか OpenAI 互換 local server として同梱起動するか、を product scope として決める必要がある。[[source-code]]より [[github-dev-docs]]より

この route はユーザー価値が強い一方、モデルサイズ、ライセンス、Windows antivirus 誤検知、初回ロード時間、CPU 速度、品質差の説明が主要リスクになる。既存 issue では `#471` が local LLM benchmark / 推奨スペック / 標準モデル未決を扱い、`#450` が embedding model 選択、`#573` が PLaMo-Embedding-1B 実験を扱っている。`#573` の観測では PLaMo-Embedding-1B は CPU で現行 multilingual-mpnet より遅く、クラスタリング指標も低かったため、同梱モデル選定は「日本語特化っぽい」だけでは決められない。[[github-dev-docs]]より

## Native local AI runtime route

tokoroten は 2026-05-31 Slack で、20B class model が現実的になりつつあることと、Chrome / Windows が LLM を native support し始めていることを指摘した。これは「モデルを広聴AI artifact に直接同梱する」route とは少し違う。platform が model lifecycle / hardware acceleration / cache を担い、広聴AIは local runtime を provider として使う route である。[[slack-local-llm-native-runtime-2026-05-31]]より

Chrome Prompt API は Gemini Nano を Chrome 内で使う API で、初回 model download 後は外部送信なしで使える。ただし広聴AIの current pipeline は Python/FastAPI 側で batch analysis を走らせるため、Python process から直接 Chrome Prompt API を呼ぶ形にはならない。browser tab が LLM call を実行して API に結果を返す設計にすると、user activation、tab lifecycle、長時間 batch 実行、Chrome availability が risk になる。したがって、Chrome route は primary analysis backend よりも、client-side 補助・将来の browser-only viewer / admin 実験として見るのが現実的。[[chrome-built-in-ai-docs-2026-05-31]]より

Windows route は 2 種類ある。Phi Silica / Windows AI APIs は Copilot+ PC / NPU に寄った local model で、privacy と低 latency の方向性は合うが、2026-05-31 時点では experimental channel や unsupported device の制約があり、広い Windows user 向け primary route には早い。一方 Foundry Local は Python SDK、OpenAI-compatible local endpoint、embeddings、Windows ML integration、model download/cache 管理を持つため、current `provider="local"` と接続しやすい。まず spike するなら Foundry Local が最も自然な候補である。[[windows-native-local-ai-docs-2026-05-31]]より [[source-code]]より

user share の rough estimate では、Chrome Prompt API は一般 desktop なら 45〜55% 程度に届く可能性があるが、自治体・組織貸与 PC では 20〜40% 程度に落ちる。Foundry Local + small model は browser 依存がないため 25〜50% 程度の target user に届く可能性があり、first spike として最もよい。Phi Silica / Copilot+ PC は installed base がまだ小さく、target user では 1〜5% 程度の future option と見る。[[local-ai-runtime-user-share-estimate-2026-05-31]]より

## Issue 化

`digitaldemocracy2030/kouchou-ai#885` として、`#289` の直接再開ではなく「`#289` を現実的に再評価するための前提 issue」として起票した。2026-05-31 15:07 に nishio 指摘を受け、body を更新して MVP を external API route / offline bundled-model route の 2 本比較に変更した。2026-05-31 19:25 には Chrome / Windows native local AI runtime も offline route の候補として追記した。完了条件も、同梱モデル候補・モデル配布方式・CPU で現実的に待てるデータ量・API route との品質差 UX・native runtime option の比較を含む形へ修正した。[[github-dev-docs]]より

## Open Questions

- static zip 出力を Node build なしで維持するのか、local desktop MVP では一旦 scope 外にするのか
- admin API key を static client に載せる local desktop threat model をどう明文化するか
- public-viewer の OGP / revalidate / ISR 相当を static fallback に倒してよいか
- PyInstaller / Nuitka のどちらを packaging spike の first try にするか
- offline bundled-model route は Python process 内 inference に寄せるか、同梱 local server を起動する形にするか
- モデルを配布物に同梱するか、初回起動時 download にするか
- API route と offline route を同一 UI で切り替えるか、配布物を分けるか
- Chrome Prompt API を batch analysis backend として使う設計は成立するか、client-side 補助用途に限定すべきか
- Foundry Local の preview maturity、model catalog、Japanese quality、license / redistribution 条件をどう確認するか
- 広聴AI target user の実機 spec をどう測るか。Steam Hardware Survey は高 spec 側に偏るため、自治体・政党・市民団体の貸与 PC を直接見る必要がある

## Updates

- 2026-05-31: Chrome / Foundry Local / Phi Silica route の user share estimate を追加。Foundry Local + small model は first spike 候補、Chrome Prompt API は補助用途、Phi Silica / Copilot+ は future option と整理
- 2026-05-31: tokoroten 指摘「Chrome / Windows の native LLM support を使えないか」を受け、offline route に native local AI runtime route を追加。Chrome Prompt API は browser lifecycle 依存が強く、Foundry Local は Python/OpenAI-compatible/embedding まで揃うため最初の spike 候補と整理
- 2026-05-31: nishio 指摘「適当なモデルを同梱して API 契約不要で local 完結」を受け、MVP scope を external API route / offline bundled-model route の 2 本比較に修正。`#885` body も同じ方針へ更新
- 2026-05-31: 初版作成。Slack の単一実行バイナリ議論を受け、current main の Node runtime 責務を確認し、`#885` を起票した
