---
name: ojpp-vs-kouchou-ai-broadlistening-model-2026-10-13
summary: "OJPP BroadListening と kouchou-ai のモデルをコード単位で突き合わせた評価。OJPP は埋め込み(TF-IDF truncate)と空間可視化(grid)が破綻、argument mining と生態系ダイナミクスは着想価値あり。kouchou-ai は忠実な地図化に一貫"
type: analysis
sources:
  - ojpp-repo-source-2026-10-13.md
---

# OJPP BroadListening vs kouchou-ai — モデルの突き合わせ評価

[[nishio]] の依頼:「OJPP の BroadListening モデルを [[kouchou-ai]] と突き合わせて評価して」。

**読んだコード（freshness）**: OJPP `ochyai/open-japan-politech-platform` @ `d1a9c2b`（2026-03-21、以降 dormant）の `apps/broadlistening-web/src/lib/{algorithms,llm}` と `api/topics/[id]/{analyze,ecosystem}` を **2026-10-13 に実読**。kouchou-ai 側は `work/kouchou-ai` @ `main 8f402d2e` の `packages/analysis-core/src/analysis_core/steps/` を一次参照。[[ojpp-repo-source-2026-10-13]]・[[broadlistening]]・[[ojpp-agent-first-design-read-2026-10-13]] と併読。

## 結論（先に）

- **OJPP は「意見＝デジタル生態系」というコンセプト・プロトタイプ**。設計思想（フェロモン / 適応度 / quorum sensing）は斬新だが、**クラスタリングの土台（埋め込み）と空間可視化が実装レベルで破綻**している。especially 日本語で機能しない。
- **kouchou-ai は「忠実な意見の地図化」に一貫**。実埋め込み + UMAP + 階層クラスタリング + LLM ラベリング。合意形成・収束判断は人間に委ねる。目的に対し設計が揃っている。
- 「どちらが上か」は目的次第だが、**「人間の意見分布を正確に把握する」目的では kouchou-ai が明確に上**。OJPP から kouchou-ai が採れるのは **argument mining / gap detection / 時間発展**という別軸の着想で、埋め込み・AI 注入・自動 CLOSE は採ってはいけない。

## パイプライン対応表

| 軸 | OJPP BroadListening | kouchou-ai |
|:---|:---|:---|
| メタファ / 目的 | 意見の**生態系**。`OPEN→DELIBERATION→CONVERGENCE→CLOSED` へ自動フェーズ遷移＝自己組織化的合意形成 | 意見の**地図**。俯瞰→drill-in の探索。合意・収束判断はしない |
| 入力単位 | ユーザ投稿 1 opinion（100–200字） | raw コメント(CSV)→ LLM で複数「意見単位」に抽出 |
| 抽出 | **Argument mining**: claims/premises/evidence/rebuttals + relations(ATTACK/SUPPORT/UNDERCUT)。confidence は固定 `0.7` | `extraction.py`: コメント→意見単位（**flat**、議論構造なし） |
| 埋め込み | **TF-IDF 128次元**。語彙を alphabetical sort して**先頭128語だけ**に truncate。tokenize は**空白分割で日本語形態素解析なし** (`lib/llm/embeddings.ts`) | 実埋め込みモデル（`request_to_embed`, OpenAI 等、provider/model は config。#450/#984 で embedding モデルを chat モデルと独立選択可）。batch 1000 (`steps/embedding.py`) |
| 次元削減 | **なし**。TF-IDF 128次元で直接 k-means | **UMAP**（`compute_umap_embeddings`、model を `umap_model.pkl` に永続化し #515 で再利用可） |
| クラスタリング | k-means++、auto-k は elbow（inertia の2階差分最大、`k ≤ min(10, n/2)`）、**flat** (`lib/algorithms/kmeans.ts`) | UMAP 後に KMeans（最細 `cluster_nums[-1]`）→ **Ward linkage で centroid を階層マージ**（`scipy...linkage(method="ward")` + `fcluster`）＝**多階層** (`steps/hierarchical_clustering.py`) |
| ラベリング | LLM、max20字、代表5件 (`lib/llm/label-generator.ts`) | LLM、initial + merge の各層ラベル + **overview** (`hierarchical_*_labelling.py`, `hierarchical_overview.py`) |
| 階層 | **なし**（flat clusters） | **あり**（複数レベル＝地図の「ゾーン」） |
| 空間可視化 | **grid レイアウト**。`x=(i%cols)/cols, y=row/...` を fitness 降順で並べるだけ。**保存した embedding は layout に未使用**。cluster 円は grid 上メンバーの平均座標 (`api/.../ecosystem/route.ts`) | UMAP 2D 座標がそのまま散布図 |
| ダイナミクス | **フェロモン**(stigmergy, `I(t)=I₀e^{-λt}`, 支持で reinforce) / **fitness** (`robustness·ln(1+support)·persistence`) / **quorum sensing** による phase 自動遷移 / Shannon 多様性 / 時系列 snapshot | **なし**（静的スナップショット） |
| AI 参加 | **あり**（`ai-participate` が合成意見を注入、[[ojpp-agent-first-design-read-2026-10-13]]） | **なし**（人間の声を聴くのが目的） |
| 想定規模 | デモ（`analyze` は1回6意見ずつ、seed 5topic/200意見） | 数千〜数万コメント（polars、batch embed） |
| 第一価値 | 生態系ストーリー・熟議ダイナミクス | 人間分布の**忠実な**地図化（ラベル品質＝探索成立の機能要件） |

## OJPP 側の実装評価（どこが効いていて、どこが破綻か）

**破綻 / デモ演出:**

1. **埋め込みが semantic でない。** `embed()` は `vocab.terms`（alphabetical sort 済み）を TF-IDF 化し、`raw[0..127]` に truncate する。128語を超える語彙は捨てられ、どの語が残るかは**アルファベット順という恣意**で決まる。semantic 近接はほぼ表現できない。
2. **日本語で特に壊れる。** `tokenize` は `/[^\p{L}\p{N}\s]/` を空白化して**空白で split** するだけ。日本語は分かち書きしないので、1意見が巨大な1–2トークンになり、意見間で共有語彙がほぼ生じない → cosine ≈ 0 → **クラスタリングが意味を成さない**。政治インフラの主対象言語で中核が機能しないのは致命的。
3. **「生態系の可視化」は semantic マップではない。** ecosystem route の 2D 座標は fitness 降順の **grid**。保存済み embedding は node に同梱されるが layout では無視。"意見を生態系として可視化" の見た目は演出で、位置に意味はない。
4. **`gap-detector.ts` は定義のみで analyze/ecosystem route から未使用**（dead/aspirational）。argument mining の confidence も固定 `0.7` で、強度の実測ではない。
5. **quorum sensing の閾値がヒューリスティック。** `determinePhase` は件数・`convergenceScore`(最大クラスタ比率)・`avgPheromone` の固定閾値で `CLOSED` まで機械遷移する。「多数決ではない自己組織化」を謳いつつ、実態は**最大クラスタ比率と early mover のフェロモンを増幅して収束を宣言**する設計で、少数意見を潰す方向に働きうる。

**着想として価値がある部分:**

1. **Argument mining**（Toulmin 風: claims/premises/evidence/rebuttals + ATTACK/SUPPORT/UNDERCUT の argument graph）。kouchou-ai の意見単位は flat なので、**熟議の構造**を見る方向性は持っていない。
2. **Gap detection**（MISSING_EVIDENCE / UNADDRESSED_CLAIM / WEAK_PREMISE）。「まだ語られていない論点」を地図に重ねる発想は探索価値が高い（現状未実装なのが惜しい）。
3. **時間発展 snapshot**（`BLEcosystemSnapshot` の時系列）。同じ問いを時間で追う軸は kouchou-ai にない。

## kouchou-ai 側

`steps/` の構成が目的に素直: `extraction → embedding(実モデル) → hierarchical_clustering(UMAP+KMeans+Ward) → initial/merge labelling → overview → aggregation → visualization`。別経路として `llm_grouping.py`（`analysis_mode=llm_grouping` の LLM 直接グルーピング、用語は [[broadlistening]] のルール参照）も持つ。「忠実さ」を機能要件に据え、ラベル品質を探索成立条件として扱う姿勢が OJPP と対照的（[[broadlistening]] の「遊園地の地図」）。

## kouchou-ai への示唆

**採る候補（別軸の上積み。忠実さを壊さない）:**

- **構造化抽出オプション**: 意見単位に加え claims/evidence/rebuttals を抽出する mode。熟議の質・論点の依存関係を見たい用途に。ただし confidence は実測（自己評価 or 複数サンプル一致度）にすべき。
- **Gap / 不在論点の可視化**: 「地図に無いゾーン」をLLMで示唆し、追加収集の設計に回す。broadlistening の収集フェーズ（[[idobata]]）と接続しうる。
- **時間発展ビュー**: 同一テーマの再分析を snapshot 系列として比較する枠（既存 experiment 蓄積ルールと相性が良い）。

**採ってはいけない:**

- **TF-IDF truncate 埋め込み** / 分かち書きなし tokenize（「API 不要」を売りにしてもクラスタ品質を壊す）。
- **AI 合成意見の意見プール注入**（人間信号と同一集計に混ぜる形。[[ojpp-agent-first-design-read-2026-10-13]] と同じ結論）。
- **quorum sensing による自動 CLOSE**。少数意見の可視化と相性が悪く、収束の宣言を機械に委ねるのは broadlistening の価値と逆行。

## Open Questions

- OJPP の argument mining + gap detection を kouchou-ai の pipeline に plugin として足す価値はあるか（`analysis_core/plugins/builtin` に実験 plugin として切れる）。[[nishio]] の CLI-first 方針（niche 機能は WebUI より先に CLI/core で出す）と整合
- 「熟議の質」や「論点の不在」を評価する指標は、kouchou-ai のラベル品質 A/B 評価（CLAUDE.md の実験設計ルール）とどう接続するか
- OJPP の time-series snapshot 的な「意見分布の時間変化」を kouchou-ai で見たい需要が実在するか
