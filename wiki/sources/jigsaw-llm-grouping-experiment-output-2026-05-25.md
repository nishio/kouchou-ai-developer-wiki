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

## Hierarchical [8, 40] Comparison

これまでは単層の `K=8` を見ていたが、多層 hierarchical clustering の効果を見るため、同じ 422 argument / embedding を使って `cluster_nums: [8, 40]` も実行した。これは「40 クラスタで一度分けてから 8 クラスタへ集約する」形になる。設定ファイルは `jigsaw_sample_comments_400_hierarchical_8_40.json`、出力は `outputs/jigsaw_sample_comments_400_hierarchical_8_40/` である。[[source-code]]より

### Geometry

- `[8, 40]` の実行時間は `160.74s`、workflow token usage は `43,169` だった
- `level 1 = 8` の geometry 指標は `silhouette 0.406`, `centroid accuracy 0.955`, `avg intra-radius 0.791`, `avg nearest-centroid distance 1.923`
- 単層 `K=8` は `silhouette 0.400`, `centroid accuracy 1.000`, `avg intra-radius 0.836`, `avg nearest-centroid distance 1.875`
- したがって geometry は大差なく、`[8, 40]` の方が少し締まる一方、centroid 完全分離はわずかに崩れる

### Label Differences

- 単層 `K=8` の top-level ラベルは `金融分野のリスク評価`, `環境問題解決`, `遠隔医療`, `生活の質向上` のように、比較的トピックが狭い
- `[8, 40]` の `level 1` ラベルは `公共サービスと都市インフラ`, `顧客体験と業務効率化`, `医療・教育・生活の質向上` のように、複数の近接 cluster を束ねた **より抽象度の高い集約ラベル** になった
- `level 2 = 40` の cluster size は `4` から `20` の範囲で、上位 10 個のサイズは `20, 19, 17, 15, 15, 15, 15, 14, 13, 13` だった

### Label Quality

- OpenAI judge で単層 `K=8` と `[8, 40]` の `level 1` を直接比べると、平均総合点は `single K=8: 79.4`, `[8, 40] level 1: 82.1` だった
- 項目別には `[8, 40]` が `一貫性 26.9`, `具体性 20.8`, `網羅性 21.9` で上回り、`区別性` だけ `13.9 -> 12.6` に少し下がった
- つまり、40 cluster を先に作ってから 8 へ集約すると、top-level label は **やや抽象的になる代わりに、まとまりと代表性が上がる** 傾向がある

### Interpretation

- user が想定していた通り、`40` の layer は細粒度 cluster 群として機能し、差が出るのは `8` の layer だった
- その差は「geometry が大きく変わる」ではなく、「top-level label の意味構成が変わる」という形で出ている
- 単層 `K=8` は topic-specific で sharp、`[8, 40] -> 8` は broader で representative、というトレードオフがある
- このため、公開UIの top-level summary を何に最適化するか次第で、単層 `K=8` と `[8, 40]` のどちらを default にするかは変わり得る

## LLM K=8 Vs Hierarchical [8, 40] Level1

`[8, 40]` の上位 8 layer が、`LLM grouping K=8` の代替としてどこまで使えるかを見るため、OpenAI judge で top-level label を直接比較した。比較対象は `outputs/jigsaw_sample_comments_400_config/` の `LLM grouping K=8` と、`outputs/jigsaw_sample_comments_400_hierarchical_8_40/` の `level 1` である。judge 結果は `work/kouchou-ai/packages/analysis-core/outputs/label_quality_judge_k8_llm_vs_hierarchical_8_40_2026-05-25.json` に保存した。[[source-code]]より

### Judge Result

- cluster 単位の平均点では `llm_grouping_k8: 85.6`, `hierarchical_8_40_level1: 88.0` で、`[8, 40] level1` の方が高かった
- 項目別平均は `LLM grouping K=8` が `一貫性 28.0 / 30`, `具体性 22.2 / 25`, `網羅性 22.0 / 25`, `区別性 13.9 / 20`
- `[8, 40] level1` は `一貫性 28.0 / 30`, `具体性 23.2 / 25`, `網羅性 22.8 / 25`, `区別性 14.0 / 20` で、ほぼ全項目でわずかに上回った
- 一方で、ラベル集合全体をまとめて見せた direct judge は winner を **`llm_grouping_k8`** と返し、理由は「読みやすく、重複が少なく、粒度が揃っている」だった

### Interpretation

- ここでも `K=20` の時と同じく、「個別 cluster の平均点」と「集合としての読みやすさ」で結論が割れた
- `[8, 40] level1` は cluster ごとの代表性や網羅性では強いが、ラベルが長く説明的になりやすく、並べて見た時の scanability では `LLM grouping K=8` に負ける
- したがって、top-level summary の評価では **代表性と readability を別軸で持つ必要がある**。`[8, 40]` は semantic aggregation としてかなり有力だが、そのまま UI の見出しに使うには冗長化しやすい
- 次に見るべきなのは、「`[8, 40]` の集約構造を保ったまま、top-level label だけを短く言い換える」後処理である。これが効けば、hierarchical aggregation と LLM labeling を組み合わせる折衷案が見えてくる

## Emerging Product Implications

今回の一連の比較をまとめると、`LLM grouping` と従来 hierarchical clustering は「どちらが上か」ではなく、**向いている観察粒度が違う** と読む方が自然である。[[jigsaw-llm-grouping-experiment]]より

- `K=8` のような粗い top-level grouping では、`LLM grouping` は読みやすくまとまりの良いラベルを返しやすかった
- しかし `K=20` まで細かくすると、`LLM grouping` は token を増やしているのに平均 label quality が `85.0 -> 83.3` と下がり、逆に従来 hierarchical は `80.4 -> 85.0` と上がった
- したがって、「細かい cluster を大量に見ながら分析する」用途では、少なくともこのデータでは **従来 hierarchical の方がむしろ向いている可能性** がある
- 逆に `LLM grouping` は、細粒度探索より「ざっくり全体像をつかむ top-level summary」向きの可能性が高い

この読みが正しければ、product / docs 上の guide も変わる。`LLM grouping` を「高精度な詳細分析 mode」として売るより、**粗い俯瞰用の mode** と位置付けた方が自然であり、従来 hierarchical の方を「数十 cluster に細かく割って分析する人向け」と案内する方が筋が通る。[[source-code]]より

また、多層 `[8, 40]` 実験で `一貫性` と `網羅性` が上がりつつ `区別性` が少し落ちたことは、改善課題をかなりシャープにした。つまり今後の性能向上で本当に解くべきなのは、単に「もっと代表的なラベルを作ること」ではなく、**top-level ラベル同士の区別をどう明瞭にするか** かもしれない。これは現場で以前から聞こえていた「隣のクラスタとの違いが分かりにくい」感想とも整合する。[[broad-listening-book-source]]より

そのため、次の改善候補は `aggregation` step の prompt / algorithm である。具体的には、代表性や網羅性を維持したまま、

- top-level 見出しを短く保つ
- sibling cluster との差分を明示させる
- ラベル集合全体として粒度を揃える
- 近接クラスタと重複しそうな語を避ける

といった制約を、aggregation 時に明示的に入れる方向が有力である。これは clustering 自体を置き換える話というより、**集約後ラベリングの最適化問題** として扱った方が前に進みやすい。[[source-code]]より

## Label Refinement Mode Comparison

上の仮説を受けて、`analysis-core` に `hierarchical_label_refinement` step を追加し、`merge_labelling` の後で top-level label set だけを再編集できるようにした。今回の比較では、同じ `[8, 40]` cluster 構造を固定したまま、`mode = none / setwise_refine / setwise_refine_short` の 3 条件を実行した。出力はそれぞれ `outputs/jigsaw_sample_comments_400_hierarchical_8_40_refine_none/`, `..._setwise/`, `..._short/` である。[[source-code]]より

### Cost And Shape

- `none` は downstream `1,864 tokens / 7.5s` だった
- `setwise_refine` は `8,767 tokens / 23.8s`、`setwise_refine_short` は `8,754 tokens / 18.8s` だった
- top-level label の平均文字数は `none: 24.2`, `setwise_refine: 17.6`, `setwise_refine_short: 12.8` まで短くなった
- `setwise_refine` は `AIによる業務効率化と競争力強化`, `AIによる公共サービスと都市インフラの革新` のように、元の長い見出しを意味を保ちながら圧縮した
- `setwise_refine_short` はさらに `AIによる業務効率化`, `AIによる顧客体験向上`, `AIによる国際交流促進` のような短い heading へ寄せた

### Judge Result

- OpenAI judge の cluster 平均点では `none: 87.0`, `setwise_refine: 84.1`, `setwise_refine_short: 85.4` だった
- 項目別には `none` が `一貫性 28.0`, `具体性 22.4`, `網羅性 23.1`, `区別性 14.0` で最も高く、個別 cluster の代表性では依然として baseline が強かった
- 一方で、ラベル集合全体をまとめて見せた direct judge は winner を **`setwise_refine`** とし、ranking は `setwise_refine > none > short` だった
- judge 理由は「読みやすさと代表性のバランスが高く、重複が少なく、粒度も揃っている」で、`none` は冗長、`short` は簡潔だが情報不足寄りと見なされた

### Interpretation

- ここでも再び、「cluster ごとの平均点」と「一覧としての scanability」がズレた
- `none` は各 cluster 単体では最も代表的だが、並べると長く説明的で、一覧 UI では重い
- `setwise_refine` は平均点を少し犠牲にする代わりに、**一覧としての読みやすさを改善する** 方向へ効いた
- `setwise_refine_short` は短くしすぎると情報量が落ちることも見えた。つまり今回の実験で良さそうなのは「短ければ短いほど良い」ではなく、**適度に圧縮した setwise refinement** である
- したがって、aggregation 改善の次の論点は「top-level label をどこまで短くするか」であり、`setwise_refine` 系の prompt に sibling 差分と長さ制約をどう両立させるかが中心課題になる

## Label Refinement Prompt Variants

上の結果を受けて、`setwise_refine` 系の prompt を 2 本追加で試した。比較対象は `setwise`（既存）, `contrast`（sibling 差分を前半に出す）, `balanced`（短さより領域保持を優先する）である。出力は `..._refine_setwise/`, `..._refine_contrast/`, `..._refine_balanced/` にある。[[source-code]]より

### Cost And Label Length

- downstream token usage は `setwise 8,767`, `contrast 8,484`, `balanced 8,363` で、いずれも baseline `none` より重いが、`setwise` よりは少し軽くなった
- top-level label の平均文字数は `setwise 17.6`, `contrast 13.0`, `balanced 12.0` だった
- `contrast` は `AIによる公共安全と福祉向上`, `AIによる顧客体験向上`, `AIによる国際交流促進` のように、差分語を前に出しつつ短縮した
- `balanced` はさらに短いが、`AIによるエンタメ革新`, `AIによる業務効率化`, `AIによる公共安全向上` のように、やや一般化が進んだ

### Judge Result

- cluster 平均点では `contrast 85.0`, `setwise 84.4`, `balanced 83.8` で、`contrast` が最上位だった
- `contrast` は `一貫性 28.0`, `具体性 22.1`, `網羅性 22.1`, `区別性 12.8` で、個別 cluster の品質では最も安定していた
- 一方で、ラベル集合全体をまとめて見せた direct judge は winner を **`balanced`** とし、ranking は `balanced > setwise > contrast` だった
- つまりここでも、「個別 cluster の点数」と「一覧としての受けの良さ」で結論が割れた

### Interpretation

- `contrast` は今回の中では **個別品質の best tradeoff** に見える。短くしつつ、`setwise` より平均点を少し伸ばした
- ただし direct judge は `balanced` を好んでおり、一覧としてはより単純で揃った見出しが好まれるらしい
- これは再び、top-level label set 最適化では「読みやすさ」と「情報密度」が引っ張り合うことを示している
- 現時点の実務判断としては、algorithm 改善の本線は `contrast` 系、UI copy / heading 候補としては `balanced` 系、という二系統を分けて持つのが妥当である
- また、judge 自体も cluster 平均点と direct set comparison で繰り返し winner が割れているので、**この二軸を今後も併記する前提** で進めた方がよい

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
- 2026-05-25: `LLM grouping K=8` と `hierarchical [8,40] level1` も直接比較した。cluster 平均点では `[8,40] level1` が `88.0` 対 `85.6` で上回った一方、ラベル集合全体の direct judge は `llm_grouping_k8` 勝ちで、代表性と読みやすさを分けて評価すべきだと分かった
- 2026-05-25: 実験含意を整理。`LLM grouping` は粗い俯瞰向き、従来 hierarchical は細粒度分析向きの可能性があり、改善すべきボトルネックは clustering 自体より `aggregation` における top-level ラベル同士の区別性かもしれない、という product / algorithm 上の示唆を追記
- 2026-05-25: `hierarchical_label_refinement` の 3 mode 比較を追記。cluster 平均点では baseline `none` が `87.0` で最上位だったが、ラベル集合全体の direct judge は `setwise_refine` を 1 位とし、top-level label set の最適化では「個別品質」と「一覧 readability」を分けて見る必要があることが再確認できた
- 2026-05-25: `setwise_refine` の prompt variation 比較を追記。cluster 平均点では `contrast` が `85.0` で最上位、direct judge は `balanced` を 1 位とし、読みやすさと情報密度のトレードオフがさらに明確になった
- 2026-05-25: ここまでの judge が OpenAI/GPT ベースで、生成側も同系統 LLM であることを明示した。cluster 平均点と direct judge で winner が繰り返し割れているため、judge を信じて refinement mode を増やし続ける前に、[[label-judge-mechanism-2026-05-25]] で評価器の仕組みと限界を説明し、[[label-refinement-judge-bundle-2026-05-25]] を出して Claude / 人間 judge で較正する段階へ移る。[[source-code]]より
