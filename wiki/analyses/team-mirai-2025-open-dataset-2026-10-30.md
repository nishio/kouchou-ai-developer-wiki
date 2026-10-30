---
title: チームみらい 2025 しゃべれるマニフェストのオープンデータ整備 2026-10-30
type: analysis
summary: 広聴AIの出力を外部の研究者が追試できる形で公開した事例。結果 JSON の config が再現の記録になる、arg-id と入力 CSV の行の対応、クラスタリングが UMAP 2D 上で行われる点、そして「embeddings.pkl は 2D」という誤認がデータセットまで伝播して不要な再計算を生んだこと
sources:
  - source-code.md
  - slack-dev-kouchouai-2025-q4.md
---

# チームみらい 2025 しゃべれるマニフェストのオープンデータ整備 2026-10-30

[[nishio]] が 2025-10 に Hugging Face で公開していた、チームみらい「しゃべれるマニフェスト」（2025 年参院選）由来のデータセット
[nishiohirokazu/team-mirai-2025-embeddings](https://huggingface.co/datasets/nishiohirokazu/team-mirai-2025-embeddings)
を、2026-10-30 に海外の研究者が追試・派生実験できる形に整えた（DOI `10.57967/hf/11332`、版 `05e2273`）。
広聴AI はその中の一段で、広聴AI の出力を外部公開するときに効く知見がいくつか出たので残す。

## データの流れ

1. 市民 ↔ AI インタビュアー（いどばた政策、`digitaldemocracy2030/idobata` の `policy-edit/`）→ team-mirai/policy への PR 9,688 件（97.9% が bot 作成）
2. PR から問題意識を抽出（gpt-4o）→ 18,967 件
3. **広聴AI**（2025-07-30 実行、gpt-4o-mini / text-embedding-3-small、`cluster_nums: [20, 400]`）→ 論点 21,348 件、2D 座標、クラスタ 421 件
4. 論点の 1536 次元 embedding を別に再計算（2025-10、下の「誤認の伝播」を参照）

HF には各段の出力を別 config（`arguments` / `problems` / `prs` / `clusters` / `embeddings`）として載せ、英訳列も足した。

## 広聴AI について分かったこと

### 結果 JSON の `config` がそのまま再現の記録になる

`hierarchical_result.json` の `config` には、各ステップのプロンプト全文・モデル・パラメータに加えて**各ステップの `source_code` が丸ごと入っている**。
実行時の kouchou-ai の commit が分からなくても、どのコードで回ったかをこれで示せる。HF ではこれを `pipeline/kouchou-ai-config.json` として公開した。

ただし `config` は**最後の実行**のもの。今回は `-o hierarchical_aggregation` で集約だけ再実行していたので、トップレベルの `start_time` やトークン数は集約の再実行分で（トークン 0）、
抽出〜ラベリングの実行時刻・トークン数は `config.previous` を辿る必要があった。

### arg-id と入力 CSV の行の対応

`Acsv-N_k` は「入力 CSV の N 行目（1 始まり）から抽出した k 番目の論点」。今回 21,348 件すべてで、N 行目の入力と対応する PR が一致することを確かめた。
入力 18,967 件のうち 165 件は論点が 1 件も出なかった。
外部公開するときは、この対応を表として出しておかないと、論点から元の入力へ戻れない（HF では `comment_id` = `csv-N` 列にした）。

### クラスタリングは UMAP 2D の上で行われる

[[pipeline]] にあるとおり、k-means（400）と Ward による併合（→ 20）は **UMAP で 2D にした座標**の上で走る（`n_neighbors=15`、`random_state=42`）。
高次元 embedding でクラスタリングし直して比べたい研究者には決定的な前提なので、データセットのカードに明記した。

## 誤認の伝播：「embeddings.pkl は 2D」

[[pipeline]] は 2026-05-17 に「`embeddings.pkl` は UMAP 後 2D」という Slack 上の誤認を撤回している。
同じ誤認が、このデータセットにも入っていた。

- 2025-10 の Drive の README に「広聴AI が中間データとして保存した embedding は 2 次元に削減した後のもの」と書かれ、それを理由に `policy-pr-hub` の `high-dim/create_embeddings.py` で 1536 次元を**作り直していた**
- 2026-10-30 の HF カードにも「Kouchou-AI keeps only the 2-D coordinates」と書いてしまった
- 実物を確かめると、広聴AI の `embeddings.pkl` は 21,348 × 1536（`arg-id` と `embedding` の 2 列）。作り直したベクトルとのコサイン類似度は中央値 0.999999、最小 0.987 で、実質同じもの（差は embedding API の非決定性と見られる）

つまり再計算は不要だった。`embeddings.pkl` という名前と、出力物に次元の説明が無いことが、誤認を繰り返し生んでいる。

## Open Questions

- HF カードの「Kouchou-AI keeps only the 2-D coordinates」と step 3b の説明は誤り。訂正は [[nishio]] の確認待ち（外部公開物のため）
- 広聴AI 側で、`embeddings.pkl` の中身（元の次元のベクトルであること）を出力物の説明や README に書くべきか。誤認は Slack（2025 Q4）とこのデータセット（2025-10）で少なくとも 2 回起きている

## Updates

- 2026-10-30: 初回作成
