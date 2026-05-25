---
type: analysis
summary: "Jigsaw 的な LLM 分類の最初の実験は、`analysis_mode=llm_grouping` を 400 行の日本語コメントで回し、scatter 互換の見え方がどこまで耐えるかを観察するのがよい"
sources:
  - jigsaw-llm-grouping-implementation-plan.md
  - llm-grouping-implementation-observation-2026-05-25.md
  - jigsaw-llm-grouping-experiment-output-2026-05-25.md
  - source-code.md
---

Jigsaw 的な LLM 分類の最初の実験については、**専用の記録ページを持った方がよい**。理由は、この実験が単なる bugfix ではなく、`analysis_mode=llm_grouping` の product 価値、scatter 互換の限界、次の view 設計、という複数の論点を同時に含むからである。[[jigsaw-llm-grouping-implementation-plan]]より

2026-05-25 時点の最初の実験データとしては、`work/kouchou-ai/apps/admin/public/sample_comments.csv` を使うのがよい。このファイルは **400 行の日本語コメント** を持ち、現在の `analysis-core` 実装に対して「少なすぎず、多すぎず、最初の LLM grouping 実験として扱いやすい」サイズである。[[source-code]]より

## 目的

この実験の目的は 3 つある。

1. `analysis_mode=llm_grouping` が raw argument を直接 LLM 分類しつつ、viewer 互換の artifact を本当に生成できるか確かめる
2. embedding 由来 `x/y` に LLM grouping の結果を重ねた散布図が、どの程度「見えるがいまいち」になるかを観察する
3. その観察をもとに、`hierarchyList` / `treemap` / 専用 view のどれを次に優先すべきか判断する

## 今回使うデータ

対象ファイル:

- `work/kouchou-ai/apps/admin/public/sample_comments.csv`

観測できた性質:

- 行数は **400**
- カラムは **`comment` 1 列だけ**
- コメントは日本語
- 中身は AI に関する賛成・期待・懸念・規制・雇用・教育・プライバシーなど、ある程度テーマが散っている

## なぜこのデータがよいか

### 1. 日本語で観察できる

今回の実装と prompt は日本語前提の観察がしやすい。`example-polis.csv` は量としては良いが英語データなので、最初の「結果を人間がざっと見て違和感を掴む」実験には、日本語 400 行の方が向いている。

### 2. 400 行は初回実験としてちょうどよい

- `small_comments.csv` の 5 行では LLM grouping の性質が見えにくい
- `dummy-comments-japan.csv` の 20 行でも scatter の違和感は観察しづらい
- 400 行あれば top-level grouping の崩れ方、cluster size の偏り、scatter 上の混ざり方がある程度見える

### 3. Admin 公開サンプルなので later に UI 経路へ戻しやすい

このファイルは `apps/admin/public/` にあるので、analysis-core 単体での実験後に Admin/API 経路へ戻す時も文脈が切れにくい。

## 注意点

このデータには今のところ `comment-id, comment-body` 形式ではなく、`comment` 列しかない。したがって、現在の CLI canonical path にそのまま流すには **入力前処理** が要る。

最小の前処理は次で十分である。

- `comment-id`: 連番を付ける
- `comment-body`: `comment` を rename する

source や属性列は無くても、今回の first experiment には支障がない。

## 観察したいポイント

実験後に最低限見るべきなのは次の 4 点である。

1. **LLM grouping 自体のまとまり**  
   label / description が人間から見て自然か
2. **scatter 上の違和感**  
   同じ group が 2D 上で無理に散って見えないか
3. **cluster size の偏り**  
   1 グループに吸い込みすぎていないか
4. **次の view 候補**  
   scatter より `hierarchyList` や `treemap` の方が自然に見えそうか

## 次の実務

このページの次の更新で残すべきなのは、少なくとも次である。

1. 400 行データを `analysis-core` 入力形式へ変換したか
2. `analysis_mode=llm_grouping` で実際に完走したか
3. scatter 互換の見え方がどうだったか
4. 次に優先する view が何か

## Open Questions

- `sample_comments.csv` はテーマが AI 周辺に偏っているので、Jigsaw 的な「対立軸発見」の観察には十分か
- 400 行を 1 回で group discovery させるより、先に sampling して top-level groups を決める今の実装で十分か
- 実験 2 本目は `example-polis.csv` のような英語・実データ寄りサンプルに広げるべきか

## Updates

- 2026-05-25: 初版作成。`sample_comments.csv` 400 行日本語データを、Jigsaw 的 LLM grouping の最初の観察対象として採用する判断を記録
- 2026-05-25: 実験を実施。`sample_comments.csv` 400 件を `comment-id, comment-body` 形式へ整形し、`analysis_mode=llm_grouping` で 422 argument を 8 群へ分類できた。群ラベル自体は自然だが、embedding 由来 `x/y` 上の separation は弱く、silhouette score は `-0.039`、centroid ベース再分類精度も `0.488` だった。したがって、短期互換案としては成立するが、次に優先すべきは scatter 改善より group-first な別 view の検討である。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: 同じ 422 argument / 同じ embedding を使って `cluster_nums: [8]` の従来 hierarchical clustering と比較した。従来法は silhouette score `0.400`、centroid ベース再分類精度 `1.000` で、scatter の見やすさでは明確に優位だった。つまりこの比較は、「LLM grouping が悪い」のではなく、「LLM grouping を散布図に載せるのが不自然」という解釈を支持する。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: `~/broadlistening-research` の 2025-02 judge を参考に、OpenAI API で top-level ラベル品質も比較した。`一貫性 / 具体性 / 網羅性 / 区別性` の平均点は `LLM grouping 85.0`、`hierarchical 80.4` で、judge の全体判定も `llm_grouping` 勝ちだった。よって今回の結論は「geometry は従来法、label semantics は LLM grouping」と二軸で持つべきである。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: 費用対効果まで含めると、same-args downstream 比較で `LLM grouping` は `35,654 tokens / 149s`、従来法は `7,088 tokens / 49s` だった。つまり `LLM grouping` は scatter を良くするには割高で、label semantics を良くするための追加コストと解釈すべきである。次に view を変えずに mode だけ増やしても費用対効果は出にくい。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: `K=20` でも実験した。geometry は `K=8` と同じく従来 hierarchical が優位だったが、label quality は `LLM grouping K20 83.3`、`hierarchical K20 85.0` と平均点ベースでは逆転した。一方で集合全体を見た direct judge は `llm_grouping_k20` 勝ちを返しており、judge の粒度によって結論が揺れることも分かった。今後は `method` だけでなく `K` と `judge granularity` も主要変数として扱うべきである。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
