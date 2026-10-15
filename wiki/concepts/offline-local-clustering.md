---
title: "APIキー無しのローカル・クラスタリング経路"
name: offline-local-clustering
summary: "analysis-core の LLM ステップ(extraction/labelling)を飛ばし、埋め込み＋階層クラスタリングだけをローカル(APIキー不要)で回す経路と、CLI 正規 JSON が作れない落とし穴"
type: concept
sources:
  - source-code.md
---

## これは何か

[[pipeline]] は `extraction → embedding → 階層クラスタリング → ラベリング → 可視化` の順で、**extraction と labelling は LLM** を要する。外部 LLM の API キーが無い環境で「意味的なクラスタ構造だけ」欲しい時は、**LLM ステップを飛ばして embedding ＋ 階層クラスタリングだけ**を回せる。[[source-code]]（`packages/analysis-core`）の step 関数を Python から直接呼ぶ。

## 手順（step 関数の直呼び）

- インストール: `pip install 'kouchou-ai-analysis-core[embeddings,clustering]'`（`torch` + `sentence-transformers` + `umap-learn` / `scikit-learn` / `scipy`）
- `analysis_core.steps.embedding.embedding` と `analysis_core.steps.hierarchical_clustering.hierarchical_clustering` を import し、dict config を渡して実行する。`is_embedded_at_local=True` で**ローカル埋め込み**（`sentence-transformers`、例 `paraphrase-multilingual-mpnet-base-v2` = 768次元・多言語・CPU 可）。
- **extraction の省略**: 入力 `comment` が既に論点（argument）に要約されているなら、1 comment = 1 argument として扱い LLM 抽出を飛ばせる。
- `cluster_nums=[L1,L2,L3]`（例 `[8,24,72]`）で多層クラスタリング。各コメントに階層クラスタ ID が付き、代表は centroid 近傍で取れる。

## 落とし穴

- **CLI の canonical `hierarchical_result.json` は API キー無しでは作れない。** 既定 workflow は `… → clustering → labelling → overview → aggregation` の順で、canonical JSON を組む `aggregation` が LLM 生成物（`hierarchical_merge_labels.csv` / `hierarchical_overview.txt` / `relations.csv`）に依存する。構造だけ欲しいなら step 関数直呼びで **label 無しの構造**を得て、ラベルは後工程（人手 or 別 LLM）で付ける。
- step 関数は `random_state` を取らず **乱数固定ができない**。UMAP / KMeans の再実行でクラスタ番号・境界が多少変わる（意味構造は安定する想定）。
- [[llm-providers]] の LocalLLM（Ollama / LM Studio 等）を使えば extraction / labelling も含めてローカル完結できる余地があるが、本経路は「LLM ステップ**自体**を飛ばす」点が別アプローチ。

## 使いどころ

既に論点要約済みのコメント群を素早くクラスタリングして俯瞰したい、API キーやコストを使わず構造だけ見たい、ラベリングを人間や別手段でやりたい、といった場面。研究用途の軽量な一次確認として [[experiment-methodology]] の scratch 層と相性がよい。

## 検証（鮮度）

- analysis-core **0.1.3**（main 近傍、2026-10-13 時点で確認）で、約 964 件の多言語（日英韓）コメントに適用し L1=8 クラスタを得た。公開アウトプット例: https://nishio.github.io/kaito-mondai-report/
- 関連: [[pipeline]] / [[cli]] / [[llm-providers]] / [[experiment-methodology]]

## Open Questions

- extraction を正式に skip する設定（1 コメント = 1 argument を CLI 経路で指定する手段）があるか。現状は step 関数直呼びで回避している。
- 決定性（乱数固定）を step 関数側へ通す手段があるか。
