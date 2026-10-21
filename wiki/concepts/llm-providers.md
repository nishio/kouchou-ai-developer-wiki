---
title: "対応 LLM プロバイダ"
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
| Gemini | `GEMINI_API_KEY` | AkioPonkotu さんの PR 由来、継続改善（例: 思考トークンを出力トークンとして計上。PR [#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037)） |
| OpenRouter | `OPENROUTER_API_KEY` | 他社モデルへのルーティング |
| LocalLLM (Ollama) | `--profile ollama` | 既定モデル `hf.co/elyza/Llama-3-ELYZA-JP-8B-GGUF` |
| LM Studio 等 | "LOCAL LLM" 扱い | PR [#422](https://github.com/digitaldemocracy2030/kouchou-ai/issues/422) で [[tokoroten]] が一般化 |

## Local provider の次候補 (未実装)

Windows 単一実行ファイル / API 契約不要 route では、Foundry Local が current `provider="local"` に最も接続しやすい候補である。Foundry Local は Python SDK、OpenAI-compatible local endpoint、embedding API、model download/cache 管理を持つため、既存の OpenAI-compatible local LLM 経路に近い。ただし 2026-05-31 時点では広聴AI main には未実装で、model catalog の日本語品質、license / redistribution、first-run download UX、preview maturity の確認が必要。[[windows-native-local-ai-docs-2026-05-31]]より [[source-code]]より

Chrome Prompt API / Gemini Nano は browser 内 local model として有望だが、Python/FastAPI の batch pipeline から直接使う provider ではない。client-side 補助や browser-only 実験には向くが、分析 backend として使うには browser tab lifecycle と user activation を抱える。[[chrome-built-in-ai-docs-2026-05-31]]より

Phi Silica / Windows AI APIs は Copilot+ PC / NPU 向けの Windows native local model route だが、experimental channel や supported device 制約があるため、現時点では primary provider ではなく future option として観測する。[[windows-native-local-ai-docs-2026-05-31]]より

## なぜ複数プロバイダ対応か

[[meeting-minutes]] 2025-04 〜 2025-08 で繰り返し議論されている：

- 日本の自治体は **クレジットカード／$ 決済／海外 API 利用ルール** で OpenAI 直契約が困難
- 郡山市など LGWAN 環境では外部 API そのものが使えない（→ 結局非対応）
- OpenRouter / LocalLLM はその回避策
- API キー入力フォーム（PR [#660](https://github.com/digitaldemocracy2030/kouchou-ai/issues/660)）も同文脈

## LOCAL LLM の HTTPS 対応

[[meeting-minutes]] 2026-05-18 見出し / PR [#824](https://github.com/digitaldemocracy2030/kouchou-ai/issues/824)：

> OpenAI や Azure AI Service ではないモデルを叩くとき「LOCAL LLM」という扱いになっているが、これが HTTP を暗黙に仮定してたので **HTTPS の別サービスを叩くことができない**。

当初（`main@3809a7a`）は、分析パイプライン（analysis-core の `services/llm.py`）と管理画面のモデル一覧取得（api の `services/llm_models.py`）が、どちらも `http://{host}:{port}/v1` を固定で組み立てていた。その後、次の順に直った。[[source-code]]より [[pr-824-local-llm-https-observation-2026-05-19]]より

- PR [#824](https://github.com/digitaldemocracy2030/kouchou-ai/issues/824)（2026-05-18 merge）: パイプラインが `https://...` のような完全な URL と、接続先に送る API キー `LOCAL_LLM_API_KEY` に対応した
- PR [#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037)（2026-10-19 merge）: `host[:port]` の解析を厳密にした。解析できないアドレスを `localhost:11434` に黙って差し替えず、エラー（`ValueError`）にする
- PR [#1038](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1038)（2026-10-19 merge）: 管理画面の「モデル取得」（`/admin/models`）も、パイプラインと同じ `resolve_local_llm_base_url`（旧名 `_resolve_local_llm_base_url` は別名として残る）と `LOCAL_LLM_API_KEY` を使うようになった。解析できないアドレスは 400 エラーで返る

main での接続先の決め方は、`host[:port]` なら `http://host:port/v1`（port を省くと 11434）、`scheme://...` ならそのまま使い、末尾に `/v1` が無ければ補う。したがって main では、分析とモデル一覧の両方で HTTPS の OpenAI 互換ゲートウェイを扱える。ただし作成画面の入力欄の例と説明は、今も `ollama:11434` のような `host:port` 形式だけを案内している。

"LOCAL" という命名が実装にバイアスを与えていた古典的なケースであり、今後も類似の hidden assumption を疑う材料。

## 埋め込みモデル

- 既定は `text-embedding-3-small`（hierarchical / llm_grouping の両 spec の既定値）
- small より精度の高い埋め込みを選びたいという要望（Issue [#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450)）を受けて、PR [#984](https://github.com/digitaldemocracy2030/kouchou-ai/issues/984)（2026-10-13 merge）で、作成画面からチャットモデルとは別に埋め込みモデルを選べるようになった。選んだ値は config の `embedding.model` に入る。複製・再利用では元レポートの埋め込みモデルを引き継ぐ（PR [#1017](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1017)。複製・再利用の画面には選択欄が無い）
- プロバイダごとの選択肢:
  - OpenAI: `text-embedding-3-small` / `text-embedding-3-large`。それ以外の名前は analysis-core が拒否する
  - Gemini: `gemini-embedding-001`。OpenAI のモデル名や未指定のときも、自動でこれに置き換わる。100 件ずつまとめて送り、429（rate limit）は指数バックオフで再試行する（PR [#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037)）
  - OpenRouter: 選べる埋め込みモデルが無い（analysis-core も `NotImplementedError`）。作成画面では、サーバ内埋め込みを ON にしないと送信できない
  - LocalLLM: 作成画面ではサーバ内埋め込みが強制的に ON になる
  - Azure: 選択欄は無効。サーバ設定の `AZURE_EMBEDDING_DEPLOYMENT_NAME` で決まる
- サーバ内埋め込み（ローカル）のモデルは `paraphrase-multilingual-mpnet-base-v2` に固定（[[offline-local-clustering]]）
- `WITH_GPU=true` でビルドすると、API イメージに入る torch が CPU 版から PyPI 既定版（CUDA 対応）に変わる。ただし `compose.yaml` で GPU を予約しているのは ollama サービスだけで、api サービスには GPU の割り当てが無い

[[source-code]]より

## API キーフォーム入力

PR [#660](https://github.com/digitaldemocracy2030/kouchou-ai/issues/660)（Issue [#633](https://github.com/digitaldemocracy2030/kouchou-ai/issues/633) への対応、2025-08-13 merge）で、OpenAI / OpenRouter のキーを管理者画面の新規作成フォームから渡せるようになった。デモ環境の「公開のためにはユーザ自身のキーを入れさせる」要件（2025-06-23 board）に対応。その後 PR [#698](https://github.com/digitaldemocracy2030/kouchou-ai/issues/698)（2025-09-24 merge）で Gemini が選択肢に加わり、現行の作成画面では OpenAI / OpenRouter / Gemini でキーを入力できる。LocalLLM と Azure にはキー欄が無い。欄を空にすると、サーバに設定されたキーを使う。[[source-code]]より

## API キー不要ルートの候補（未実装・観測中）

OpenAI の **Sign in with ChatGPT (SIWC)** は、OSS / local-hosted アプリがサインインしたユーザの ChatGPT プラン枠で推論を回せる OAuth 機能で、「API キーを配らず、ユーザ自身のプランでサインインさせる」という PR [#660](https://github.com/digitaldemocracy2030/kouchou-ai/issues/660) とは別の回避ルートになりうる。広聴AIは OSS なので概念上は対象カテゴリに合致する。ただし **(1) plan 共有は Responses API に明示限定で embedding は docs 範囲外（2026-10-12 確認）＝embedding はクラスタリングの中核なので SIWC 単独ではキー不要にならず別キー/別プロバイダが要る、(2) preview、(3) 有料・リモートホスト型は別申請で Azure デモのような hosted には素直に使えない、(4) OAuth loopback flow の統合コスト、(5) OpenAI ロックイン、(6) Responses API でも `temperature` / `max_output_tokens` 等の field が未対応**という制約があり、多プロバイダで自治体制約を回避してきた本方針とは逆向き。現時点は future option として観測に留める。[[openai-siwc-token-sharing-docs-2026-10-12]]より

**Claude / Anthropic** を同じ文脈で足す案も 2026-10 の Slack で出ている（Max プランの月次 API credit を labelling に充てる）。ただし chat 側は `gemini` 同型で追加できる一方、**Anthropic は自前の embedding モデルを持たず**（公式 docs は Voyage AI を薦める）、SIWC と同じく embedding の壁に当たる。current main (`083593ba`) に `anthropic` 分岐は chat / embed とも 0 件。詳細と経済性・切り分けは [[claude-provider-connection-proposal-2026-10-17]]。

## Open Questions

- Embedding モデルのデフォルト変更（精度 vs コスト vs 一貫性）
- 「LOCAL LLM」というカテゴリ名そのものを「self-hosted endpoint」等にリネームすべきか
- Foundry Local を `provider="local"` の単なる endpoint として扱うか、first-class provider として model download/cache/progress UI まで持つか

## Updates

- 2026-10-21: main `b71e0b79` と照合して訂正。LOCAL LLM は PR [#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037) / [#1038](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1038) で管理画面のモデル一覧取得もパイプラインと同じ接続先解決・認証になり、2026-10-18 の項の「http 固定が残るのはモデル一覧取得だけ」は解消した。埋め込みモデル節を、作成画面で選べる現状（PR [#984](https://github.com/digitaldemocracy2030/kouchou-ai/issues/984) / [#1017](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1017) / [#1037](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1037)）に更新し、`WITH_GPU` は torch の種類を切り替えるだけと明記。[#660](https://github.com/digitaldemocracy2030/kouchou-ai/issues/660) は Issue ではなく PR で、merge は 2025-08-13（2025-07-30 の議事メモの時点ではまだマージ待ち）と訂正し、現行の作成画面では Gemini もキー入力の対象と追記
- 2026-10-18: main `083593ba` で analysis-core の `_resolve_local_llm_base_url` は `scheme://host[:port]` 形式（HTTPS ゲートウェイ）を受け付ける。http 固定が残るのは `apps/api/src/services/llm_models.py` のモデル一覧取得だけ。OpenRouter は embedding 非対応（`NotImplementedError`）
- 2026-10-17: Slack `#2_開発_広聴ai` の「Claude を接続する案」を考察し [[claude-provider-connection-proposal-2026-10-17]] を作成。「API キー不要ルートの候補」節に Claude/Anthropic の note を追記（chat は追加可・embedding は Anthropic 非提供で Voyage 依存、main に anthropic 分岐 0 件）
- 2026-10-12: OpenAI SIWC (Sign in with ChatGPT) token-sharing docs を ingest し「API キー不要ルートの候補」節を追記。リンク先 docs 確認で **plan 共有は Responses API 限定・embedding は docs 範囲外**と確定（embedding 中核のため SIWC 単独ではキー不要にならない）。preview・hosted 不適合も caveat に未実装観測 → [[openai-siwc-token-sharing-docs-2026-10-12]]
- 2026-10-07: 小型ローカルモデル（Qwen3 4B）で他言語の短文から意見抽出すると、処理は終わっても主張の主体の逆転などの意味の書き換えが起きた観察を [[local-llm-extraction-faithfulness-2026-10-05]] に記録
- 2026-05-31: Windows local 完結 route の候補として Foundry Local / Chrome Prompt API / Phi Silica を追記。Foundry Local は現行 OpenAI-compatible local endpoint に接続しやすいが未実装
- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を確認し、LOCAL LLM の HTTPS 対応は「議事メモ上の報告あり・main 反映は要再確認」という書き方に修正
