---
name: ojpp-repo-source-2026-10-13
summary: "ochyai/open-japan-politech-platform（OJPP）README 読解。PoliTech / 7アプリ / 「エージェントファースト設計」表 / BroadListening の ai-participate を記録"
type: source
sources:
  - https://github.com/ochyai/open-japan-politech-platform
  - https://raw.githubusercontent.com/ochyai/open-japan-politech-platform/main/README.md
---

# OJPP リポジトリ読解（2026-10-13 時点）

**Freshness marker**: `ochyai/open-japan-politech-platform` の README・ファイルツリー・`ai-participate` route を **2026-10-13 に読んだ**。対象は `main` HEAD `d1a9c2b`（commit date 2026-03-21、repo 最終 push 2026-03-22、作成 2026-02-12、★387）。**repo は 2026-03 以降 dormant**で、`v0.2` ロードマップ項目は未着手のまま。License は README 上 `AGPL-3.0-or-later`（GitHub API は `NOASSERTION`）。

> 本 wiki スコープ外の外部プロジェクト。[[kouchou-ai]] / [[dd2030]] に対する「参考」であり、無批判に採用しない前提で記録する。

## プロジェクト概要

- タグライン **「AIエージェント時代の政治インフラ」**／**「政党にも企業にもよらない、完全オープンな政治テクノロジー基盤」**
- 自称カテゴリは **PoliTech**（GovTech でも CivicTech でもない、「政治の意思決定プロセスそのものを全ての人に開く」）。主体を **「市民 + AIエージェント」**、時代を「AIエージェント時代」と置く
- 構成: Next.js 15 / React 19 / Prisma 6（29 models）monorepo。**Portal + 7 apps** = BroadListening β / MoneyGlass / PolicyDiff / ParliScope / SeatMap / CultureScope / SocialGuard。各アプリに REST API
- データは v0.1 時点で大半が公的機関の実データ（総務省・衆参・文化庁・厚労省・財務省等）、政党別スタンスのみデモデータ

## 7つの原則（冒頭）

> **1** エージェントファースト — AIの参加を前提に設計
> **2** 非党派性 / **3** 非企業性 / **4** 完全オープン（AGPL）/ **5** 誰でも参加（人間でもAIでも）/ **6** 議席不要 / **7** 持続性（フォーク可能で分散的）

導入文: 「**AIエージェントの時代が、この構造を変える。**」「AIエージェントがあなたの代わりに政治を読み解き、あなたに届ける」。

## 「エージェントファースト設計」セクション（README 本文の表、原文）

| 設計原則 | 詳細 |
|:---|:---|
| **API-First** | 全データをRESTful APIで提供。エージェントが直接アクセス |
| **機械可読データ** | JSON構造化データを標準。人間用UIとエージェント用APIの両方 |
| **エージェント認証** *(v0.2)* | AIエージェント用の認証・権限管理 |
| **MCP対応** *(v0.2)* | Model Context Protocol による外部AIとの連携 |
| **思考の共有** | Entire によるエージェントセッションの永続化。コミットと紐付けて「なぜこのコードが書かれたか」を共有 |
| **Attribution** | Entire による人間/AI貢献比率の自動算出・記録 |
| **監査ログ** *(v0.2)* | 全操作のトレーサビリティ。エージェントの行動も透明 |

- 「AIエージェントで開発する」節: clone して `claude`（Claude Code）を起動するだけ、を謳う。コーディング規約に **API-first** を明記
- Contributing: 「AIエージェントからのPull Requestも歓迎」。`agent/` ラベルで PR を送る運用

## 関連プロジェクト表（原文の該当行）

- **DD2030** — 「方向性は近い。本プラットフォームは**エージェントファースト設計を追加**」
- **チームみらい** — 「技術的参考。本プラットフォームは全政党対応の非党派版」
- 他に g0v/vTaiwan、Decidim/Consul、mySociety を参照先として列挙

## BroadListening β（kouchou-ai との接点として重要）

README 記述: 市民の意見を「デジタル生態系」としてモデリング。**Argument Mining（LLM）**で議論構造抽出、**デジタルフェロモン（Stigmergy）**で支持の軌跡、**適応度ランドスケープ + Shannon 多様性指数**でクオーラムセンシングによるフェーズ自動遷移。「多数決ではない自己組織化的合意形成」。`k-means++` / `TF-IDF 埋め込み` / `フェロモン減衰`。

API に **`POST /api/topics/:id/ai-participate`（AIエージェント参加）** がある。route 実装（`apps/broadlistening-web/.../ai-participate/route.ts`）を読むと:

- LLM に **政策討論エージェント**として「100〜200字の日本語の意見を、既存意見と重複しないよう独立した論点で」生成させる（system prompt: 「各意見は独立した論点を持ち、既存の意見と重複しないようにしてください。」）
- 入力はトピック題・説明と既存意見最大50件。`body.perspectives`（default 3、最大 5）件を `{ content, stance(FOR/AGAINST/NEUTRAL), perspective }` の JSON 配列で生成
- 生成した各件を **`BLOpinion`（`authorId: "ai-agent"`, `fitness: 0`）** として DB に書き込み、`BLPheromone`（intensity/quality 0.5, decayRate 0.01）を紐付ける
- 要するに **AI が合成意見を意見プールへ注入する**エンドポイント

## 追加読解（2026-10-13、同日）

BroadListening のモデル比較のため、README に加えて次の実コードを `@ d1a9c2b` で読んだ:

- `apps/broadlistening-web/src/lib/llm/`: `embeddings.ts`（TF-IDF 128次元 truncate・空白 tokenize）, `argument-extractor.ts`, `label-generator.ts`, `gap-detector.ts`（analyze/ecosystem route から未使用）
- `apps/broadlistening-web/src/lib/algorithms/`: `kmeans.ts`（k-means++ / elbow）, `fitness.ts`, `quorum.ts`, `pheromone.ts`
- `apps/broadlistening-web/src/app/api/topics/[id]/`: `analyze/route.ts`（抽出→埋め込み→クラスタ→fitness→quorum→snapshot）, `ecosystem/route.ts`（2D は fitness 降順 grid、embedding は layout 未使用）
- `packages/db/prisma/schema.prisma`（BL* モデル）

要点: 埋め込みが非 semantic（TF-IDF を alphabetical 先頭128語に truncate）で日本語 tokenize も分かち書きなし、空間可視化は grid レイアウトで embedding を使っていない。詳細評価は [[ojpp-vs-kouchou-ai-broadlistening-model-2026-10-13]]。

## このソースから判断すること

- OJPP の「エージェントファースト設計」の具体像・批判的読解は [[ojpp-agent-first-design-read-2026-10-13]] に filing back
- BroadListening モデルの kouchou-ai との突き合わせ評価は [[ojpp-vs-kouchou-ai-broadlistening-model-2026-10-13]]
- プロジェクト node は [[ojpp]]
