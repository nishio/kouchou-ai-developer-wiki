---
type: source
summary: "OpenAI 'Sign in with ChatGPT' (SIWC) の plan 共有（token sharing）公式 docs の要点。OSS / local-hosted アプリが、サインインしたユーザの ChatGPT プランで Responses API 推論を実行できる OAuth 機能。API キー不要ルートの候補だが、対応 endpoint は Responses API に明示限定で embedding は docs 範囲外（2026-10-12 確認）。embedding が広聴AI pipeline の中核のため、SIWC 単独ではキー不要ルートとして不完全"
sources:
  - https://developers.openai.com/siwc/token-sharing-open-source
---

## 何のソースか

OpenAI Developers の **Sign in with ChatGPT (SIWC)** docs のうち、OSS / self-hosted アプリ向けの "token sharing"（プラン共有）概要ページ。SIWC は OpenAI の OAuth ベース機能で、identity scope に加えて「サインインしたユーザの **ChatGPT プラン枠で eligible な Responses API リクエストを実行する**」権限をアプリが要求できる。これはユーザの ChatGPT 会話やアカウント文脈を露出するものではなく、docs が "token sharing" と呼ぶのはこの **plan-usage capability** を指す。対象は OSS / ローカルホスト型アプリで、**有料・リモートホスト型アプリは別途 interest form が必要**。[[openai-siwc-token-sharing-docs-2026-10-12]]より

## 主要概念

- **Client**: サインイン時にユーザが認可する OAuth 登録。発行される `client_id` は認証ユーザと選択 workspace に紐づき、セキュリティ境界と plan-usage 設定を定義する。[[openai-siwc-token-sharing-docs-2026-10-12]]より
- **Agent host**: ツールのインスタンスが動く環境（laptop / self-hosted VM 等）。何を 1 host と数え、lifecycle をいつ開始・終了するかはアプリが決める。再起動や再サインインは新 host を作らない。
- **Relationship**: 1 client が同一 user / workspace の複数 host を束ね、plan 設定と limit を共有する。host ごとに固有の識別子が要る。
- **`ext_agent_host_id`**: client が **初回サインイン前に選んで永続化する** stable で opaque な識別子。個人情報を含めず、認証クレデンシャルでもない。format は JWK thumbprint URI (RFC 9278, 推奨) / `urn:uuid:` (RFC 9562) / `did:key` のいずれか。公開鍵由来 ID でも OpenAI は秘密鍵の所持を検証しない。

## フロー（初回起動〜初回推論）

1. **Prepare**: host ID を選択/再利用し、local loopback listener を起動、state / nonce / PKCE を生成。
2. **Authorize**: ブラウザで OpenAI の認可ページを開き、ユーザが認証・同意、code つきで redirect。
3. **Exchange & validate**: state 検証 → PKCE で token endpoint と code 交換 → ID token と granted scope を検証 → 基本アカウント情報と credential を保存。
4. **Infer**: bearer access token で Responses API に `store: false`・`stream: true` でリクエストし、`response.completed` までストリーム処理。

OAuth 2.0 authorization code flow + PKCE + state + nonce を前提とする。概要ページにコードサンプルは無く、リンク先に sign-in / registration、token refresh、models & streaming、Codex app-server 設定、self-hosted VM への credential 移送、error handling、preview 制約がある。[[openai-siwc-token-sharing-docs-2026-10-12]]より

## 広聴AIへの含意

[[llm-providers]] の根本課題――日本の自治体は **クレカ / \$ 決済 / 海外 API 利用ルール**で OpenAI 直契約が難しく、[[meeting-minutes]] でも「公開のためにはユーザ自身のキーを入れさせる」（Issue #660 の API キーフォーム）で回避してきた――に対し、SIWC は「**API キーを配らず、ユーザが自分の ChatGPT プランでサインインして推論を回す**」という別ルートを提示する。広聴AIは OSS なので SIWC の対象カテゴリには概念上合致する。ただし以下の制約から、現時点では **未実装・将来 option として観測**に留めるのが妥当。[[openai-siwc-token-sharing-docs-2026-10-12]]より

### 無批判採用を避ける論点

- **Responses API 限定（embedding は docs 範囲外）**: plan 共有は "eligible Responses API requests" が対象。リンク先 docs（models-and-inference / preview-limitations）を確認したところ、plan 共有の推論 endpoint は **`POST /v1/responses` に明示限定**（"Supported endpoint: Use the public Responses API endpoint… for this ChatGPT plan usage flow"）。文書化されているのは他に `GET /v1/models`（model picker 用）のみで、**Embeddings API は supported にも blocked にも挙げられず docs の対象外**。preview-limitations も supported endpoint を Responses API とし、未対応 input として audio/video・Files upload・transcription を挙げるが embedding には触れない。広聴AIの pipeline は embedding を analysis-core 経由で呼ぶ（[[llm-providers]] / [[pipeline]]）クラスタリングの中核コストなので、**SIWC 単独ではキー不要ルートとして不完全**で、embedding は別途 OpenAI キーか別プロバイダが必要になる。(2026-10-12 確認)
- **preview**: docs 自身が preview limitations ページを持つ。production 依存の判断には早い。
- **hosted デモとの不整合**: 有料・リモートホスト型は別 interest form。広聴AIの Azure デモ環境のような **hosted 提供には素直に使えず**、価値が出るのは「ユーザが自分の端末で local に広聴AIを動かす」配布形態に限られる。
- **統合コスト**: OAuth loopback flow、PKCE、host ID の永続管理、token refresh を実装する必要があり、単純な env var 1 本の API キー入力より重い。
- **ロックイン**: OpenAI 固有。[[llm-providers]] が多プロバイダ対応で自治体制約を回避してきた方針（OpenRouter / LocalLLM）とは逆に、OpenAI プランへの依存を強める。

## Responses API 側の制約（preview-limitations より）

plan 共有ルートでは Responses API でも一部 field / tool が使えない。広聴AIが OpenAI 呼び出しで前提にしがちなものが含まれる点に注意。[[openai-siwc-token-sharing-docs-2026-10-12]]より

- **未対応 field（HTTP）**: `max_output_tokens`, `temperature`, `top_p`, `user`, `metadata`, `previous_response_id`。→ 温度や最大出力トークンを明示指定する分析コードはそのままでは通らない。
- **未対応 tool**: image generation, file search, Code Interpreter, native computer use, hosted MCP/connectors, Responses `tool_search`、top-level `tools` の `programmatic_tool_calling`。
- **対応 tool**: function / custom tools（namespace か `additional_tools` 経由）。
- **未対応 input**: audio/video input, Files upload API, transcription API。
- model 固定リストは無く、catalog はサインインしたアカウント依存（例示は `gpt-6.1-sol`）。

## Open Questions

- ~~SIWC の plan 共有は embedding API を含むか~~ → **2026-10-12 確認: docs は Responses API 限定で embedding は対象外**。SIWC 単独ではキー不要にならず、embedding は別キー/別プロバイダが要る。
- OSS 配布版（ユーザ端末で動かす形態）を広聴AIが正式サポートする計画と噛み合うか。現状の一次配布は hosted デモ寄り。
- preview の rate / quota / 商用利用条件が自治体スケールの分析（数千〜数万コメント）に耐えるか（docs は rate/quota に言及なし）。

## Updates

- 2026-10-12: 初版作成。OpenAI SIWC token-sharing docs を「API キー不要ルート」の feasibility 判断材料として整理。Responses API 限定・embedding 対象未確認・preview・hosted 不適合を caveat として明記
- 2026-10-12: リンク先 docs（models-and-inference / preview-limitations）を確認し、embedding の扱いを「未確認」→「**Responses API に明示限定で embedding は docs 範囲外**」に確定。あわせて Responses API 側の未対応 field（`temperature` / `max_output_tokens` 等）・未対応 tool / 未対応 input を追記
- 2026-10-12: **nishio の経済的動機の仮説を追記**（Slack `#2_開発_広聴ai` 2026-10-12 09:14 nishio より）。「広聴AIに Sign in with ChatGPT をつけると **Codex（ChatGPT プラン）の weekly limit を使って分析ができる**。使い切らず余らせた枠を切り替え間際に使うなら実質無料」という説。SIWC の plan 共有＝サインインしたユーザの ChatGPT プラン枠で Responses API を回す仕組みを、**定額プランの未消化 weekly quota の転用**として捉える見方。コスト面で [[llm-providers]] の自治体決済課題を緩める候補になりうる一方、本ソースの技術 caveat はそのまま効く——特に **embedding は SIWC の対象外**なので weekly quota で賄えるのは Responses API 側（ラベリング等）だけで、クラスタリング中核の embedding は別途キー/別プロバイダが要り、「pipeline 全体が実質無料」にはならない。plan の weekly limit / rate / quota が自治体スケール（数千〜数万コメント）に耐えるかも未確認（docs は rate/quota に言及なし）。現時点では **feasibility アイデアとして観測**に留める。
