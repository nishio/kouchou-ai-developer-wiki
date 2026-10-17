---
title: "「Claude Code を接続する案」の考察 2026-10-17"
type: analysis
summary: "直近の Slack #2_開発_広聴ai で出た『Claude を広聴AIに接続する』話は、(A) Claude Code をオーケストレータとして分析を回す案、(B) サブスク枠で LLM コストを賄う案、(C) pipeline に Anthropic provider を足す案の 3 層が混ざっている。核心は embedding——Anthropic は自前の embedding model を持たず docs は Voyage AI を薦めるため、SIWC と同じ壁に当たる。tokoroten の『Claudeはエンベディングもある』は docs の誤読。Max API credits は Messages API（ラベリング）には効くが interactive Claude Code・Voyage embedding には効かない。現コードに anthropic 分岐は 0 件"
sources:
  - llm-providers.md
  - offline-local-clustering.md
  - coding-agents.md
  - openai-siwc-token-sharing-docs-2026-10-12.md
  - https://platform.claude.com/docs/en/build-with-claude/embeddings
  - https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans
---

## 何の考察か

直近の Slack `#2_開発_広聴ai` で [[nishio]] と [[tokoroten]] が「Claude を広聴AIに繋ぐ」話を断続的にしている。本ページは、その一連の発言を **3 層に切り分け**、現行コードと公式 docs に照らして feasibility と設計上の切り分けを整理する。結論を先に書くと、**「Claude 対応」で解けるのは pipeline の LLM ステップ（extraction / labelling）だけで、クラスタリングの中核である embedding は Claude では解けない**（[[openai-siwc-token-sharing-docs-2026-10-12]] の SIWC と同じ壁）。

## ソースと鮮度

- **Slack**: `digitaldemocracy2030/slack-logs` の `mirror/`（`synced_at=2026-10-17T10:28 UTC`、window 75日）を 2026-10-17 に読解。対象 channel は `#2_開発_広聴ai`。関連 root 発言は 10-05 / 10-07 / 10-12 / 10-13 / 10-16。
- **コード**: `work/kouchou-ai/` main **083593ba**（2026-10-16）。`packages/analysis-core/src/analysis_core/services/llm.py` の `request_to_chat_ai` / `request_to_embed` を一次参照。
- **公式 docs**: Anthropic Embeddings docs と Max/Team API credits support 記事を 2026-10-17 に取得。

## Slack の発言は 3 層に分かれている

同じ「Claude を繋ぐ」でも、層が違う 3 つの話が混ざっている。混同すると「Claude 対応すれば OpenAI 不要」と早合点しやすい。

- **(A) Claude Code をオーケストレータとして使う**（[[nishio]]）
  - 10-05: Codex のおかげでデータ分析が楽。Web の pipeline は「データを入れて結果が出る」形に単純化せざるを得ないが、AI Agent がアドホックに pipeline を組めれば「結果を見て一部を絞り込んで再分析／再利用」がやり放題。
  - 10-07: ただし良い精度で回すには Codex か Claude Code の課金が要る。ローカル LLM が無償で agentic にこなせるのは半年〜1年先の肌感。
  - 10-13: **OpenAI API を置いていない環境で Claude Code に「広聴AIで分析して」と言ったら、ローカルモデルで embedding して Claude 自身がクラスタ命名をして完了させた**。OpenAI API を使わない経路が「爆誕」した。
- **(B) サブスク枠で LLM コストを賄う**
  - 10-12（[[nishio]]）: 広聴AI に Sign in with ChatGPT を付けると Codex の weekly limit で分析できる説。→ 同スレで「**embedding が対象外なのでダメという結論**」。これは既に [[openai-siwc-token-sharing-docs-2026-10-12]] に filing 済み。
  - 10-16（[[tokoroten]]）: **Claude の Max プランに API の無料トークンが付くので、これを広聴AI に突っ込みたい → Claude 対応したい**。続けて Max/Team の monthly API credits docs と embeddings docs を共有し「Claude はエンベディングもあるな」。
- **(C) pipeline に first-class な Anthropic provider を足す**（[[tokoroten]] 10-16「Claude 対応したいな」）
  - これは (A) の「エージェントが外から回す」とは別の、`provider="anthropic"` を [[llm-providers]] に追加する**コード変更**の話。

(A) は**使い方（usage mode）**、(C) は**コード変更**で、課金経路も別物。ここを分けないと議論が噛み合わない。

## 現状のコード — Claude 分岐は存在しない

main `083593ba` で `grep -rilE 'anthropic|claude'` を `packages/analysis-core/src` と `apps/api/src` に掛けると **0 件**。provider 抽象の現状は以下。

| ステップ | 対応 provider | Claude |
|---|---|---|
| chat（extraction / labelling）`request_to_chat_ai` | openai / azure / local / openrouter / gemini | **無し** |
| embedding `request_to_embed` | local（sentence-transformers, `is_embedded_at_local`） / azure / openai / gemini / local(Ollama) | **無し** |

- embedding は chat とは**独立に provider 分岐**している。`openrouter` の embedding は `NotImplementedError`。`is_embedded_at_local=True` なら sentence-transformers で**キー不要・ローカル完結**（例 `paraphrase-multilingual-mpnet-base-v2`、768次元、CPU 可）。[[offline-local-clustering]] がこの経路。
- chat 側に `anthropic` を足すのは、既存の `gemini` 分岐（628–637 行）と同型で**素直**。`apps/api/src/services/llm_pricing.py` などの価格表追加も要る。

## 技術的な核心: embedding の壁は Claude でも消えない

(B)(C) の肝は embedding。ここで tokoroten の「Claude はエンベディングもあるな」は **docs の誤読**である。

- Anthropic Embeddings docs の本文は明言している: **"Anthropic does not offer its own embedding model."**（Anthropic は自前の embedding モデルを提供しない）。ページの残りは **Voyage AI (by MongoDB)** という**サードパーティ**の使い方で、`VOYAGE_API_KEY` と MongoDB Atlas の課金が要る。つまりあの docs は「Claude の embedding API」ではなく「embedding をやるなら他社を使え」というガイド。
- したがって [[openai-siwc-token-sharing-docs-2026-10-12]] の SIWC が当たったのと**同じ壁**に当たる: LLM 側（labelling / extraction）は Claude で賄えても、**embedding は Claude では賄えない**。選択肢は (1) ローカル embedding（sentence-transformers、無償）、(2) Voyage / OpenAI / Gemini など別 provider のキー、のどちらか。

### Max API credits の経済性（実際に効く範囲）

tokoroten の「Max の無料トークンを突っ込む」案を support 記事で裏取りすると:

- 金額: **Max 5x = $100/月、Max 20x = $200/月**（Team は seat 課金、pool 上限 $500/月）。
- 効く先: **Messages API / Batches / Console / Managed Agents / Agent SDK**。→ `provider="anthropic"` を足して広聴AI が Messages API を直接叩けば、extraction / labelling のコストをこの credit で賄える。
- **効かない先**: **interactive Claude Code**、Bedrock / Vertex / Foundry 経由。→ (A) の「Claude Code に回してもらう」usage は Claude Code のサブスク枠を食う話で、この API credit とは**別勘定**。
- rollover 無し、毎月失効。Voyage は記事に記載なし（= MongoDB 側の別課金で、この credit では賄えないと見るべき）。

つまり **(C)「Claude 対応 + Max credit」は LLM ステップの実質無料化としては筋が通る**が、embedding 分は credit 外。embedding をローカルにすれば「LLM は Max credit・embedding は無償ローカル」で OpenAI キー無しの経路が成立する（これが 10-13 で Claude Code が偶発的に実演した構成に一致する）。

## 2 つの「Claude」経路を分けて評価

| | (A) Claude Code = オーケストレータ | (C) in-pipeline `provider="anthropic"` |
|---|---|---|
| 実体 | usage mode（外から CLI/agent が analysis-core を駆動） | コード変更（provider 分岐追加） |
| コード変更 | **不要**（10-13 で実証済み） | 要（chat 分岐 + 価格表） |
| 課金 | Claude Code サブスク枠 | Anthropic API credit（Max $100/$200）/ 従量 |
| embedding | ローカル（Claude Code が選んだ） | 別途ローカル or 他社キー |
| 誰が使える | frontier agent を持つ開発者・研究者（[[cli]] / [[usage-modes]] の研究者層） | WebUI/API 利用者全般（自治体含む） |
| 位置づけ | [[offline-local-clustering]] + ラベリングを Claude が担う一般化 | [[llm-providers]] への provider 追加、[#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285) の範疇 |

- **(A) は既に動く**。10-13 の「爆誕」は新機能ではなく、[[offline-local-clustering]]（ローカル embedding + 階層クラスタリング）に、ラベリングを Claude Code 自身が肩代わりする形を足しただけ。つまり**キー不要ルートは設計上すでに存在していて、Claude Code がそれを end-to-end で実演した**という理解が正確。[[coding-agents]] の「nishio が分析実務で Claude Code を多用」の一例。
- **(C) は [#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285)「利用可能な LLM を増やす」の自然な一項目**。自治体向けの動機は [#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255)「OpenAI が使えないケースのケア」にある通り、コストだけでなく「ChatGPT の政治利用 NG が売り込みの障害になりうる」= **provider 中立性**。#255 の現案は Azure / Gemini / OpenRouter / LiteLLM で、**Claude はまだ挙がっていない**ので、同じ列に足す提案になる。

## 設計上の切り分けと最小実装

「Claude 対応」を 1 個の塊として実装せず、**LLM provider と embedding provider を分けて**扱うのが現コードとも整合する。

1. **chat provider に `anthropic` を追加**（`request_to_chat_ai` に `gemini` と同型の分岐、`ANTHROPIC_API_KEY`、価格表）。extraction / labelling が Claude で回り、Max API credit で賄える。
2. **embedding は Claude に持たせない**。既定を `is_embedded_at_local=True`（ローカル無償）にするか、OpenAI/Gemini/Voyage のいずれかを選ばせる。「Claude で全部」はできないことを UI/docs に明示。
3. **キー不要プリセット** = `provider=anthropic`（labelling）+ `is_embedded_at_local`（embedding）。これが 10-13 で Claude Code が自動選択した構成の、WebUI/API からの再現にあたる。

## 引き継ぐ caveats

- **ローカル embedding / 小型モデルの意味忠実性**: 小型ローカルモデルで他言語の短文から意見抽出すると、主張の主体が逆転するなど意味が書き換わる観察がある（[[local-llm-extraction-faithfulness-2026-10-05]]）。「キー不要で回った」ことと「出力が正しい」ことは別。
- **決定性**: step 関数直呼び経路は `random_state` を取らず乱数固定できない（[[offline-local-clustering]]）。採用判断の比較実験では [[experiment-methodology]] に従い factor を 1 つだけ変える。
- **指定カテゴリ分類との関係**: provider を変えても、[[llm-grouping-supervised-classification]] の「その他」受け皿必須などラベリング側の原則は不変。
- **政治利用ポリシー**: #255 の動機が「ChatGPT 政治利用 NG」である以上、Claude を足す際も Anthropic 側の利用規約（政治用途の可否）を provider 選定時に確認する必要がある（本ページでは未確認、要 follow-up）。

## Open Questions

- (C) を [#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285) / [#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255) のどちらで追跡するか。embedding を別軸で扱う以上、「LLM を増やす（#285）」と「OpenAI 不可ケアの provider 列（#255）」の両方に跨る。
- embedding の既定を「ローカル無償」にするか「別社キー」にするか。精度（[[local-llm-extraction-faithfulness-2026-10-05]]）× コスト × 一貫性のトレードオフ。
- Max API credit の weekly/monthly 枠と rate が、自治体スケール（数千〜数万コメント）の labelling に耐えるか（docs に rate 記載なし。SIWC と同じ未確認点）。
- Anthropic の政治用途ポリシーが広聴AI の売り込み先（政党・自治体）と整合するか。

## Updates

- 2026-10-17: [[nishio]] が「**embedding はローカルモデル、オーケストレーションを Opus 等がやる形式**」を有力と表明（本 repo チャット）。これは本ページ (A)＋ローカル embedding。設計上の含意を整理:
  - **コストと価値の配分が合う**: embedding は大量・機械的（ローカル無償で可）、判断（抽出の是非・クラスタ解釈・命名・drill down）は少量・高価値（Opus）。OpenAI キー依存の痛点（[#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255)）はまさに embedding 側で、単なるコスト回避でなくフロンティア推論の投下先として正しい。
  - **「オーケストレーション」は 2 解釈で productization が分岐**: (i) エージェントがアドホックに駆動（研究者/CLI 層・非決定的・課金は **Claude Code サブスク枠で Max API credit 対象外**）/ (ii) in-pipeline の Opus provider＋ローカル embedding（WebUI/API 層・決定的・配布可・**Messages API なので Max credit 対象**）。**tokoroten の無料枠狙いに合うのは (ii)**。基盤（ローカル embedding）は共有で、上に乗る層が違うだけ。nishio の言い回しは (i) 寄りだが、目的（無料枠 vs アドホック力）で選ぶ。
  - **律速は embedding 品質（ラベリングではない）**: 出力構造は vector に乗るため、Opus を上に置いても壊れた構造は命名で救えない。現 main の `request_to_local_embed` は `paraphrase-multilingual-mpnet-base-v2`(768d) に**ハードコード（選択不可）**。[#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450) は既定 embedding に不満、[#516](https://github.com/digitaldemocracy2030/kouchou-ai/issues/516) が embedding×次元圧縮の調査。→ この形式を良くする実体は (a) ローカル embedding model の選択可能化（e5-large / bge-m3 等）、(b) ローカル vs OpenAI embedding の同一 corpus クラスタ比較を 1 本（[[experiment-methodology]]）。
  - **Opus はクラスタ単位に留めるのがコスト安全**: per-comment 抽出を Opus に投げると N に比例して credit を食う。per-comment は機械的/ローカルに寄せ、Opus は cluster-level の命名・overview・判断に充てる（小型 LLM の抽出不忠実（[[local-llm-extraction-faithfulness-2026-10-05]]）回避にもなる）。
  - 上記により Open Question「embedding 既定（ローカル無償 vs 他社キー）」は **nishio lean = ローカル寄り（ただし品質検証を前提）**。

- 2026-10-17（実装・検討）: 両形式を具体実装し、key 無しで回る範囲を実行確認した。**結果・数値・再現手順・Anthropic 固有の確定事項は [[claude-provider-experiment-output-2026-10-17]] に集約**（コードは worktree branch `claude-provider-experiment` 98cf5677 未 push、artifact は `raw/experiments/claude-local-embed-opus-2026-10-17/`）。要点:
  - (ii) in-pipeline `provider="anthropic"` と (i) orchestrator harness を実装。実 `anthropic.types` mock test 3 件＋既存 47 件 green・ruff clean。kaito 997 件をローカル埋め込みで key 無し完走（L1 silhouette≈0.06、要同指標比較）。
  - **検討の結論**: 両形式とも成立、基盤（ローカル埋め込み）は共有。(ii)=配布可・Max credit 対象の WebUI/自治体向け、(i)=アドホック再分析が効く研究者向け。**律速はやはり embedding 品質**で provider 追加（容易）では解けない。前提作業は **embedding model の選択可能化（現状ハードコード）** と `factor_under_test = embedding provider` だけ変える clean experiment（[[experiment-methodology]]）。live labelling 品質は key 入手後に (i) の harness で測れる。
