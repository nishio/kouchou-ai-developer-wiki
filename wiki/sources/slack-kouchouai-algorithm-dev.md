---
type: source
summary: "`oss_weekly_reporter` の `#2_開発_広聴ai_アルゴリズム開発` 抜粋（2025-04 〜 2026-03）— UMAP→k-means への批判、対立軸発見、LLM分類、可視化代替案"
last_read: 2026-05-18
coverage: "2025-04-23〜2026-03-25 の `#2_開発_広聴ai_アルゴリズム開発`"
sources:
  - init.txt
  - nishio-source-freshness-criterion-2026-06-02.md
---

## What it is

`work/oss_weekly_reporter/data/*/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` を横断して読んだ source。  
対象期間は **2025-04-23 〜 2026-03-25** で、`#2_開発_広聴ai` よりもアルゴリズムの内訳や理論的な不満、代替案の試行が濃く出ている。

## Freshness marker

この source の鮮度基準は、**2026-05-18 に `work/oss_weekly_reporter/data/*/raw/slack/2_開発_広聴ai_アルゴリズム開発.json` を横断して 2025-04-23 〜 2026-03-25 を読んだ時点**。この page は `raw/` に固定した snapshot ではなく、`work/oss_weekly_reporter` 側の data を参照して作った要約である。[[nishio-source-freshness-criterion-2026-06-02]]より

このチャンネルは「広聴AIをどう運用するか」よりも、

- 現行の `embedding → UMAP 2D → k-means / 階層化` の何が弱いか
- その弱さをどう回避するか
- 可視化と分析をどう切り分けるか

を詰める場として機能している。

## Refresh protocol

1. `work/oss_weekly_reporter/` を最新化
2. `find work/oss_weekly_reporter/data -path '*/raw/slack/2_開発_広聴ai_アルゴリズム開発.json' | sort` で対象週を確認
3. 必要に応じて `markdown/slack/all_summary.md` も併読して文脈を補う
4. 新しい論点が出ていれば本ページと関連 analysis を更新

## High-signal periods

- **2025-04 〜 2025-05**: 重複意見検知、diff 類似度、ローカル埋め込み、クラスタラベルの納得感
- **2025-05 〜 2025-06**: UMAP の軸に意味があるか、なぜ 2D なのか、PCA / UMAP / HDBSCAN の比較
- **2025-07 〜 2025-08**: ベクトル検索、可視化ポリゴン、Concave Hull / ボロノイ、UMAP 並列化
- **2025-10 〜 2025-11**: UMAP 後クラスタリングへの強い批判、LLM 直接グルーピング / 対立軸発見 / taxonomy 当てはめ
- **2025-12**: EVOC や高速 HDBSCAN 代替への関心
- **2026-02 〜 2026-03**: 下位クラスタビュー、少数意見救済、時系列ヒートマップ、外部有識者による UMAP→k-means 批判の明文化

## Coverage by topic

- **重複・コピペ検知**: embedding だけでは複数意見結合型の攻撃に弱く、`n-gram` / `TF-IDF` / 類似 UI 補助が必要という初期議論がある
- **UMAP の意味づけ問題**: 軸に意味を読み込みたくなる利用者行動がありつつ、射影軸自体には意味がないという認識が繰り返し確認される
- **UMAP 後にクラスタリングする弱さ**: 2D に落としてからの `k-means` や階層化は精度劣化やアーティファクト混入を招くという批判が継続する
- **高次元クラスタリング / HDBSCAN 回帰**: 精度優先なら高次元のまま HDBSCAN 系へ戻したいが、速度と可視化の問題がある
- **LLM 直接分類 / LLM 直接グルーピング**: embedding 空間では賛否対立が埋もれやすいため、対立軸発見や分類ツリー生成を LLM でやる路線が検討される
- **既存カテゴリへの当てはめ**: 東京都など既存の政策カテゴリーツリーに意見をはめこむ実験と、その限界認識が語られる
- **可視化代替案**: ワードクラウド風 drill-down、下位クラスタビュー、凸包 / ボロノイ、時系列ヒートマップ、画像生成つきビューなど
- **外部有識者レビュー**: 2026-03 に朝日新聞社の新妻氏が参加し、`UMAP` の局所構造偏重と `UMAP後k-means` の危うさを整理している

## Related Pages

- 本チャンネルから読める設計判断の整理は [[slack-algorithm-themes]]
- 近接する実装・plugin 方針の議論は [[slack-dev-kouchouai-2025-q4]] と [[slack-dev-kouchouai-2026-q1]]
- 現行パイプラインの構造は [[pipeline]]

## Open Questions

- `work/oss_weekly_reporter` 側の全週を source 化しているが、`raw/` へローカル保存した固定 snapshot ではない
- 実験アイデアは豊富だが、どこまで `main` や open PR に落ちたかは別観測が必要
- `2_開発_広聴ai` と論点が往復している週もあり、設計意図の最終決定は別チャンネル側に出ることがある

## Updates

- 2026-05-18: `#2_開発_広聴ai_アルゴリズム開発` を 2025-04 〜 2026-03 で横断読解し、主要論点を source 化
- 2026-06-02: source の鮮度基準として `last_read` / `coverage` と Freshness marker を明示
