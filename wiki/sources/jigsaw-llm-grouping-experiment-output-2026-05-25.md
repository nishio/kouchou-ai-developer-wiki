---
type: source
summary: "2026-05-25 に `analysis_mode=llm_grouping` を 400 件の日本語コメントで実行した観測。422 argument を 8 群へ分類でき、`report.html` も生成できたが、embedding 由来 2D 散布図との相性は悪かった"
sources:
  - source-code.md
  - llm-grouping-implementation-observation-2026-05-25.md
---

2026-05-25 に `work/kouchou-ai/packages/analysis-core` 上で、`apps/admin/public/sample_comments.csv` を `comment-id, comment-body` 形式へ整形し、`analysis_mode=llm_grouping` の最初の実験を行った観測メモである。これは [[jigsaw-llm-grouping-experiment]] の実行結果ページにあたる。コード実装は current working tree の `analysis-core` を使い、出力は `outputs/jigsaw_sample_comments_400_config/` に生成した。[[source-code]]より [[llm-grouping-implementation-observation-2026-05-25]]より

## Observations

- 入力は日本語コメント 400 件、抽出結果は 422 argument だった
- top-level grouping は 8 群で、件数は `101 / 93 / 84 / 42 / 31 / 29 / 28 / 14` に分かれた
- 群ラベルは `AIの社会的役割 / AIの技術的利点 / AIのビジネス影響 / AIの自動化と雇用 / AIの倫理と規制 / AIの未来展望 / AIと医療 / AIの教育と学習` だった
- `hierarchical_result.json` と `report.html` は生成でき、互換 artifact を作る短期目標自体は達成した
- ただし 2D 散布図の分離は弱く、`hierarchical_clusters.csv` 上の group label を正解として `x,y` の silhouette score を計算すると **-0.039** だった
- centroid ベースの単純な 2D 再分類精度も **0.488** で、group の意味まとまりを 2D 上で自然に再現できていない

## 実行メモ

- 1 回目は extraction + embedding まで完了した後、workflow 定義が `discovery_prompt` を spec に持っていなかったため `llm_grouping` 直前で失敗した
- spec に `discovery_prompt` / `assignment_prompt` / `model` を追加した後、2 回目は `llm_grouping -> overview -> aggregation` まで成功したが、workflow 側が `${config.report_dir}` を強制解決していたため最後の visualization で失敗した
- `analysis.hierarchical_visualization` plugin 自体は `report_dir` default を持っていたので、workflow 側の不要な `${config.report_dir}` 参照を外し、3 回目の再実行で `report.html` まで生成できた

## Time And Cost Notes

- 1 回目の extraction + embedding + 失敗終了までは `real 181.11s`、workflow が記録した chat token usage は `219,781` だった
- 2 回目の `llm_grouping -> overview -> aggregation` は `real 149.28s`、workflow が記録した chat token usage は `35,654` だった
- 3 回目の visualization-only rerun は `real 6.41s`、追加 token usage は 0 だった
- したがって今回の実験全体で確認できた chat token usage は **255,435 tokens** である
- embedding 入力は `args.csv` 422 件を `cl100k_base` で数えると **12,660 tokens** だった
- OpenAI の公式 pricing page を 2026-05-25 に参照した概算では、`gpt-4o-mini` の chat 部分はおおむね **$0.045 前後**、`text-embedding-3-small` の embedding 部分は **$0.0003 未満** で、総額は **約 $0.05** と見てよい

## Implications

- 「embedding は残すが grouping だけ LLM に置き換える」という短期互換案は、artifact 生成までは十分成立する
- 一方で、group meaning と scatter geometry はかなりずれる。今回の数値は「見えるが、あまり良くはない」という事前予想を裏づけている
- 次は scatter 改善より、`hierarchyList` / `treemap` / group-first detail view のような **grouping を主役にした表示** を先に試す方が筋が良い

## Same Args Comparison With Traditional Clustering

同じ 422 argument と同じ `embeddings.pkl` を使い、`cluster_nums: [8]` の従来 hierarchical clustering も別出力へ回して比較した。`extraction` と `embedding` は skip し、clustering 以降だけ実行したので、比較としては「同一 args に対する grouping の違い」にかなり近い。[[source-code]]より

- 従来法の実行時間は `real 48.89s`、workflow が記録した token usage は `7,088` だった
- 従来法の top-level 群サイズは `77 / 63 / 59 / 52 / 50 / 43 / 40 / 38` で、LLM grouping の `101 / 93 / 84 / 42 / 31 / 29 / 28 / 14` より均等だった
- 2D 指標も大きく違い、従来法は silhouette score **0.400**、centroid ベース再分類精度 **1.000**、平均 intra-radius **0.836**、平均最近接 centroid 間距離 **1.875** だった
- LLM grouping は同じ指標で silhouette score **-0.039**、centroid ベース再分類精度 **0.488**、平均 intra-radius **1.700**、平均最近接 centroid 間距離 **1.107** だった
- したがって scatter の見やすさだけを見るなら従来法が明確に有利で、LLM grouping は「散布図に向いたクラスタ」ではなく「意味的まとまりを優先した分類」だと捉えるべきである

## Label Quality Judge

`~/broadlistening-research` に残っていた 2025-02 のクラスタラベル評価研究を参考に、OpenAI API を使った label judge も実行した。元の研究では `一貫性 / 具体性 / 網羅性 / キーワード適切性` の 100 点満点評価だったが、今回の `analysis-core` 出力には `keywords` が無いので、4 項目目は `他ラベルとの区別性` に置き換えた。judge の入力には各 top-level cluster の `label`, `description`, サイズ, 意見例 5 件, 同一分析内の他ラベル一覧を与えた。[[source-code]]より

- judge 結果の保存先は `work/kouchou-ai/packages/analysis-core/outputs/label_quality_judge_2026-05-25.json`
- 平均総合点は `LLM grouping: 85.0`, `hierarchical: 80.4` だった
- 項目別平均は `LLM grouping` が `一貫性 28.1 / 30`, `具体性 21.1 / 25`, `網羅性 22.1 / 25`, `区別性 13.6 / 20`
- `hierarchical` は `一貫性 26.4 / 30`, `具体性 19.6 / 25`, `網羅性 21.0 / 25`, `区別性 13.4 / 20`
- 全体比較の judge は winner を **`llm_grouping`** とし、理由は「具体的で読みやすく、重複が少なく、各クラスタが明確で代表性が高い」だった

この結果は、「scatter 指標では従来法が強いが、ラベル品質では LLM grouping が上」という分離を示している。したがって、今回の比較で本当に見るべきなのは散布図品質だけではなく、**cluster geometry と label semantics を別軸で評価すること** だと分かる。[[jigsaw-llm-grouping-experiment]]より

## Cost Effectiveness Interpretation

費用対効果の観点では、今回の比較はかなり割り切って読める。same-args の downstream 比較だけを見ると、`LLM grouping -> overview -> aggregation` は `35,654 tokens` / `149s`、従来 hierarchical clustering は `7,088 tokens` / `49s` だった。つまり `LLM grouping` は **時間で約3倍、token で約5倍** 重い。[[source-code]]より

- scatter の見やすさだけを目標にするなら、この追加コストを払う意味は薄い。geometry は従来法が明確に勝っている
- 一方で label quality judge では `LLM grouping 85.0`、`hierarchical 80.4` で、読みやすさ・具体性・代表性では `LLM grouping` が上だった
- したがって `LLM grouping` は「散布図を改善する技術」ではなく、**ラベルと意味解釈を改善するために追加コストを払う技術** とみなすのが妥当である
- このため、費用対効果は `scatter-first view` では悪く、`group-first view` では改善余地がある、という整理になる

## K=20 Comparison

次の発展実験として、同じ 422 argument / 同じ `embeddings.pkl` を使い、`K=20` でも `LLM grouping` と従来 hierarchical clustering を比較した。設定ファイルは `jigsaw_sample_comments_400_k20_llm.json` と `jigsaw_sample_comments_400_k20_hierarchical.json` で、どちらも `--reuse-from sample_comments_400_upstream_seed` により upstream を再利用した。[[source-code]]より

### Geometry

- `LLM grouping K=20` は `52,088 tokens / 152.06s` で完了し、scatter 指標は `silhouette -0.041`, `centroid accuracy 0.472`, `avg intra-radius 1.090`, `avg nearest-centroid distance 0.764`
- `hierarchical K=20` は `17,387 tokens / 58.89s` で完了し、scatter 指標は `silhouette 0.469`, `centroid accuracy 1.000`, `avg intra-radius 0.426`, `avg nearest-centroid distance 1.145`
- したがって `K=20` でも geometry は従来法が明確に有利で、この点は `K=8` の時と変わらない

### Label Quality

- `K=20` の judge 結果は `work/kouchou-ai/packages/analysis-core/outputs/label_quality_judge_k20_2026-05-25.json` に保存した
- cluster 単位の平均点では `llm_grouping_k20: 83.3`, `hierarchical_k20: 85.0` で、`K=8` と逆転して `hierarchical K=20` の方が高かった
- ただし、ラベル集合全体をまとめて見せた direct judge は winner を **`llm_grouping_k20`** と返しており、平均点ベースの結論と一致しなかった
- この不一致は、judge の粒度によって結論がぶれること、特に `K` を増やして cluster size が小さくなると「個別 cluster の点数」と「集合としての読みやすさ」がずれ得ることを示している

### Interpretation

- `LLM grouping` は `K=8 -> K=20` で total token が `35,654 -> 52,088` に増えたが、label quality の平均点は `85.0 -> 83.3` と少し下がった
- `hierarchical` は `K=8 -> K=20` で token が `7,088 -> 17,387` に増えた一方、label quality の平均点は `80.4 -> 85.0` とかなり上がった
- 少なくともこの 400 件データでは、`K=20` まで細分化すると **LLM grouping の相対優位は自明ではなくなる**。`K=8` では label semantics が強みだったが、`K=20` では従来法もかなり具体的なラベルを返し始める
- したがって、今後の比較では「LLM grouping vs hierarchical」だけでなく、`K` を増やした時に各手法のラベル品質がどう変化するかも主変数として追うべきである

## Open Questions

- 日本語 400 件という比較的素直なデータでも 2D 分離が弱いので、英語の実データや対立の強いデータではさらに崩れるか
- top-level group discovery の sample size `80` は十分か、それとも group 定義自体がやや generic になりすぎているか
- `analysis_capabilities` と viewer plugin `requirements` を入れた時、scatter を default から外す UX にどこまで踏み込むべきか

## Updates

- 2026-05-25: 初回作成。400 件日本語データでの `analysis_mode=llm_grouping` 実行結果、token/time/cost 概算、散布図互換の限界観測を記録
- 2026-05-25: 同一 422 argument / 同一 embedding を使った従来 hierarchical clustering 比較を追記。散布図指標では従来法が大きく勝ち、LLM grouping は scatter より group-first view 向きだと確認
- 2026-05-25: `broadlistening-research` の 2025-02 ラベル評価研究を参考に OpenAI judge を実行。scatter 指標では従来法が強い一方、label quality では `LLM grouping` が平均 `85.0` 対 `80.4` で上回った
- 2026-05-25: 費用対効果の解釈を追記。same-args downstream 比較では `LLM grouping` が従来法より `約3倍` 遅く `約5倍` token を使うので、scatter 目的だと割高だが、label semantics 目的なら検討余地がある
- 2026-05-25: `K=20` 実験を追記。geometry は引き続き従来法が強かったが、label quality は `K=8` と違い `hierarchical K=20` の平均点が `85.0` と最も高く、judge の粒度によって結論がぶれることも観測した
