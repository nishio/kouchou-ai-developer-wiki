---
type: source
summary: "鈴木健 2025-11-29 ブログ。ブロードリスニングは用途ごとに欲しいインサイトが違い、TTTC / 広聴AI は主にアジェンダ発見向きだという整理"
sources:
  - meeting-minutes.md
---

## What It Is

2025-11-29 公開の鈴木健ブログ記事「ブロードリスニングにおけるインサイトの分類とツールの使い分け」の要約。日本で「ブロードリスニング」がやや表層的に語られていることへの違和感から、**何のインサイトを得たいのかを先に分け、その用途ごとに道具を選ぶべき** だと論じている。2025-12 の「広聴AIの方向性について」会議はこの問題提起を直接参照している。[[meeting-minutes]]より

## Key Points

- ブロードリスニングを 1 個の手法として扱うのではなく、少なくとも次のような用途を分けるべきだとしている
  - アジェンダ / issue finding
  - 対立する論点間の uncommon ground 探索
  - 特定政策への意見収集
  - 特定政策への改善提案収集
  - アンケート選択肢の発想支援
- TTTC / 広聴AI 型の散布図・クラスタ俯瞰は、**大量の声から全体像や論点候補を見つける** には向いているが、それがすべての用途を満たすわけではない
- Polis は uncommon ground に向き、AI interview 的な手法は特定政策に対する意見や改善案の深掘りに向くなど、**欲しいアウトカムごとに最適な道具は違う** と整理している
- TTTC / 広聴AI についても、散布図表現は大量意見の俯瞰には強い一方で、**クラスタや距離の見え方に限界があり、深い意味理解の万能解ではない** という批判的視点がある

## Why It Matters

このブログは、後の広聴AIの設計議論で

- 現行散布図方式の適用範囲を限定的に捉える
- 一つの product / one-size-fits-all analysis に閉じない
- plugin 化や複数 analysis mode を考える

という方向へ進む起点の一つになっている。[[versioning-strategy]] や [[strategic-development-order-2026-05-23]] を読む際の前提 source として重要。[[meeting-minutes]]より

## Open Questions

- ブログで挙げられた各用途に対して、kouchou-ai が今後どこまで cover するのかは未確定
- 「アジェンダ発見に強い mode」と「対立軸・分類木に強い mode」を同一 product でどう扱うかは、現在も [[jigsaw-sensemaker-history]] と [[plugin-system]] の open question である

## Updates

- 2026-05-25: はてなブログ本文から初回作成
