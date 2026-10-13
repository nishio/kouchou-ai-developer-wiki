---
name: ojpp-agent-first-design-read-2026-10-13
summary: "『エージェントファースト設計』の批判的読解。agent-as-consumer / participant / co-developer の3義に分解し、kouchou-ai broadlistening との緊張（ai-participate）と転用可能な部分を整理"
type: analysis
sources:
  - ojpp-repo-source-2026-10-13.md
---

# 「エージェントファースト設計」とは何を意味するか（OJPP を題材に）

[[nishio]] の問い:「[[ojpp|open-japan-politech-platform]] を参照して、"エージェントファースト設計" という言葉の意味が気になる」。[[ojpp-repo-source-2026-10-13]]を一次に、語の中身を分解して批判的に読む。

## 1. OJPP が言う「エージェントファースト」の明示的定義

原則 [#1](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1) に「**エージェントファースト — AIの参加を前提に設計**」。「エージェントファースト設計」節は 7 項目（API-First / 機械可読データ / エージェント認証(v0.2) / MCP対応(v0.2) / 思考の共有[Entire] / Attribution[Entire] / 監査ログ(v0.2)）。導入文は「AIエージェントがあなたの代わりに政治を読み解き、あなたに届ける」。[[ojpp-repo-source-2026-10-13]]より。

一言でいえば **「人間だけでなく AI エージェントを第一級のアクターとして最初から想定して設計する」**。UI を人間向けに作ってから API を後付けするのではなく、機械可読・API・エージェント参加を default にする、という主張。

## 2. 分解すると「エージェントファースト」は3つの別物が同居している

この語は実際には射程の異なる3つの意味を束ねている。混ぜると議論がぼやけるので分ける。

- **(A) agent-as-consumer（エージェントが読み手・利用者）** — 全データを RESTful JSON / API で出し、エージェントが UI を介さず直接消費できる。MCP 対応もここ。README の「24時間 全法案を読み差分を届ける」はこの像。→ 要は **agent-ready / API-first**。
- **(B) agent-as-participant（エージェントが参加者・当事者）** — AI が意見形成やコントリビューションに「参加」する。BroadListening の `POST /ai-participate`（AI が合成意見を注入）、`agent/` ラベルの AI からの PR 歓迎がこれ。
- **(C) agent-as-co-developer（エージェントが共同開発者）** — Entire でエージェントの思考セッションを commit に紐づけ永続化し、人間/AI の貢献比率を Attribution として記録。これは **プロダクトの利用者**ではなく **開発プロセス**が agent-first、という別軸。

## 3. 批判的読解:どこが標準で、どこが未実装で、どこが新しいか

- **(A) は大半が「良い API 設計」であって新規性は薄い**。機械可読 JSON・ページネーション・API-first は普通のベストプラクティス。「エージェントのために」と銘打つことで方向づけはするが、技術的には agent 固有ではない。
- **agent 固有を名乗る項目はほぼ `v0.2` = 未実装**。エージェント認証・MCP・監査ログはいずれも未チェックで、repo は 2026-03 以降 dormant。つまり「エージェントファースト設計」の agent 専用部分は **主張先行で、現状はまだ aspirational**。
- **実装済みで実際に特徴的なのは (B) の `ai-participate` と (C) の Entire 由来の attribution**。この2つが OJPP を「ただの API-first なデータサイト」と差別化している実体。

要するに「エージェントファースト設計」は、**実装の 8 割は agent-ready な API 設計（標準的）+ 残りに『AI が参加・共同開発する』という思想的賭け(B)(C)**、という構成。語の新味は (B)(C) にあり、そこがまさに kouchou-ai/DD2030 との論点になる。

## 4. kouchou-ai の broadlistening との緊張 —(B) ai-participate

ここが [[nishio]] にとって一番重要な点だと思われる。

- [[kouchou-ai]] の [[broadlistening]] は **「広く聴く」= 多数の人間の自由記述を忠実に集約・可視化**する。AI は**読み手**（抽出・クラスタリング・ラベリング）であり、価値は「人間の意見分布をどれだけ歪めず地図にできるか」にある。
- OJPP の `ai-participate` は逆で、**AI が FOR/AGAINST/NEUTRAL の合成意見を生成し意見プールへ注入**する（`authorId: "ai-agent"`, フェロモン付き）。[[ojpp-repo-source-2026-10-13]]より。
- 両者は「listening」の前提に対して**極性が逆**。broadlistening の信号（人間の分布）に AI 生成意見が混ざれば、地図が「実在する人間の声」を表しているという信頼が壊れうる。
- ただし AI 参加が常に悪いわけではない。シミュレーション・論点の網羅（抜けた観点の提示）・red-teaming・cold start の seeding には使える。**条件は、人間信号と AI 信号を厳密に分離・明示し、集計・可視化で混同させないこと**。OJPP は `authorId:"ai-agent"` で区別はするが、同じ生態系・同じフェロモン集計に乗せており、分離は弱い。
- 示唆: kouchou-ai が将来 AI 参加的な機能を考えるなら、「聴く」対象(人間)と「補助発話する」AI を**別レイヤー**として設計すべき。broadlistening の名で両者を1つの分布に混ぜるのは避ける。[[jigsaw-sensemaker]] 的な LLM 直接グルーピングとはまた別の、「AI が当事者として発話する」次元の話である点に注意。

## 5. kouchou-ai/DD2030 に転用できる部分 —(A)(C)

- **(A) agent-ready は無害で有用**。kouchou-ai のレポート（階層・ラベル・代表コメント）を機械可読 JSON / 安定 API / MCP server として出せば、外部エージェントが「意見の地図」を直接消費できる。これは broadlistening の思想と矛盾しない純粋な上積み。OJPP の主張のうち DD2030 がそのまま採れるのはここ。
- **(C) 開発プロセスの attribution** は [[coding-agents]]（Claude Code / Codex 運用）と地続き。人間/AI 貢献の記録は DD2030 のガバナンス議論にも効く論点。
- OJPP が「DD2030 の方向性にエージェントファースト設計を追加」と名乗る以上、DD2030 側としては **「どの (A)/(B)/(C) を自分たちは採り、どれは採らないか」を言語化**しておくと、外部からの『追加した』主張に対して立場が明確になる。

## Open Questions

- DD2030/kouchou-ai は (B) agent-as-participant を望むのか。望むなら人間信号との分離設計が要件（§4）
- kouchou-ai のレポートを MCP / API で agent-consumable にする需要と優先度（(A) は低リスクで着手しやすい）
- OJPP の BroadListening モデル（フェロモン/適応度/Shannon）は kouchou-ai の階層クラスタリングに対し、評価可能な別アプローチか、それとも demo 的演出か → コード実読で検証した: [[ojpp-vs-kouchou-ai-broadlistening-model-2026-10-13]]（埋め込み・空間可視化は破綻＝demo 的、argument mining / gap detection / 時間発展は別軸の着想として価値）
