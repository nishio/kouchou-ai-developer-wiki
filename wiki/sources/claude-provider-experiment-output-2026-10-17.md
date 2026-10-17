---
title: "Claude provider 接続実験の結果 2026-10-17"
type: source
summary: "広聴AI に Claude を繋ぐ 2 形式を実装して回した exploratory 実験の結果。(ii) in-pipeline anthropic provider と (i) Opus オーケストレータ harness を作り、kaito 997 件をローカル埋め込み+クラスタリングで API キー無し完走（L1 silhouette≈0.06, 要同指標比較）。Anthropic 固有の確定事項（埋め込み非提供／temperature 不可／system top-level／response_format 無）と、残課題（live labelling 品質・embedding model 選択可能化・clean experiment）を記録"
sources:
  - raw/experiments/claude-local-embed-opus-2026-10-17/manifest.json
  - work/kouchou-ai-claude@claude-provider-experiment(98cf5677, base main 083593ba)
---

## 何の実験か

[[claude-provider-connection-proposal-2026-10-17]] で「embedding はローカル、オーケストレーション/ラベリングは Opus」の 2 形式を挙げた。それを**具体実装して、API キー無しで回る範囲を実行確認**した exploratory 実験。採用判断（どの embedding が良いか）ではなく、「両形式が成立するか」「key 無しでどこまで動くか」「Anthropic 固有の制約は何か」を確かめるのが目的。

- **形式 (i)**: Opus 等がオーケストレータとして駆動（ローカル埋め込み→クラスタリング→Claude がラベリング→アドホック再分析）
- **形式 (ii)**: 固定パイプラインに `provider="anthropic"` を追加し、`is_embedded_at_local=True` と組み合わせる

`experiment_class = exploratory`。採用判断用の clean experiment は別（末尾）。[[experiment-methodology]]

## セットアップ

| 項目 | 値 |
|---|---|
| corpus | kaito 997 件の抽出済み argument（日英韓混在、抽出スキップ＝1 コメント 1 argument） |
| embedding | `local:paraphrase-multilingual-mpnet-base-v2`（768 次元・CPU・キー不要） |
| clustering | analysis-core `hierarchical_clustering`（UMAP + KMeans）、`cluster_nums=[8,24]` |
| labelling | Claude（新 anthropic provider 経由）。この実験では key 未設定のため prompt のみ生成 |
| code | worktree branch `claude-provider-experiment`（commit 98cf5677、base `main@083593ba`、未 push） |

## 実装の結果

### 形式 (ii) in-pipeline anthropic provider（実装・検証済み）

`request_to_chat_ai` に `provider="anthropic"`（`request_to_anthropic_chatcompletion`）を追加。`model_catalog.json` に `claude-opus-5-5` / `claude-sonnet-5-5` / `claude-haiku-5-5` を chat モデルとして登録（料金は 2026-10 時点の概算・要公式確認）。

- 実 `anthropic.types` を使った mock test 3 件＋**既存 47 件 green、ruff clean**、差分は約 +200 行。
- `[#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285)`（利用可能な LLM を増やす）に素直に乗る粒度。

### 形式 (i) orchestrator harness（実装・キー無し部分実行）

`orchestrate_claude.py` が、ローカル埋め込み+クラスタリング結果の上で各クラスタを Claude にラベリングさせ（新 provider を再利用）、さらに最大 L1 クラスタをアドホック再クラスタ（drill-down）する。これが**固定 Web パイプラインに出せない「結果を見て絞り込んで再分析」の最小実演**。

- drill-down 実測: L1 の最大クラスタ `1_8`（245 件）→ 4 サブクラスタ `{74, 46, 64, 61}`。
- labelling は key 未設定のため、各クラスタへ送る prompt を生成して確認（key ありで labels + コスト見積りまで出る設計）。

## Anthropic 固有の確定事項（再利用可能な知見）

実装を通じて、他 provider と違う Claude の制約が確定した。これは今後 Claude を使う全コードに効く。

- **埋め込みを提供しない**。`request_to_embed(provider="anthropic")` は `NotImplementedError`。埋め込みは `is_embedded_at_local=True` か別 provider（OpenAI/Azure/Gemini/local）で行う。→ [[llm-providers]] / [[offline-local-clustering]]
- **`temperature` / `seed` / prefill が現行 Claude では非対応**（送ると 400）。したがって他 provider のような `temperature=0` による決定化ができない。[[pipeline]] の再現性前提が Claude labelling では弱まる。
- **`system` は top-level**。messages 配列から分離して渡す。
- **OpenAI 互換の `response_format` が無い**ので、JSON 要求時はスキーマを system に注入し、出力から JSON 本体を抽出する（コードフェンス付き出力も吸収）。

## API キー無しで測れた数値

共通基盤（embedding leg）を実データで完走。**ここは API キー不要**。

- 997 件、ローカル埋め込み 64.6s + クラスタリング 32.0s（CPU）。
- クラスタ構造（L1, k=8）のサイズ: `{245, 167, 167, 152, 110, 92, 54, 10}`。
- full-dim cosine silhouette: L1(k=8) ≈ **0.060**、L2(k=24) ≈ 0.049。

**この数値の読み方（重要な caveat）**: 768 次元の cosine silhouette は一般に低く出る（クラスタリングは UMAP 低次元で行うため、full-dim の分離度とは一致しない）。**絶対値で「クラスタが悪い」とは断じない**。意味があるのは**同一指標での local vs 他 embedding の比較**で、それは key が要る次の clean experiment。

## 再現手順

`raw/experiments/claude-local-embed-opus-2026-10-17/` に harness と artifact（`manifest.json` / `metrics.json` / `reps.json` / `prompts.json` / `drilldown.json` / `outputs/`）がある（`raw/` は gitignored なので local 一次置き場）。

1. venv で analysis-core を `[embeddings,clustering]` 付きインストール
2. `python run_embed_cluster.py`（キー無しで embedding+clustering+silhouette）
3. `python orchestrate_claude.py`（形式 (i)。`ANTHROPIC_API_KEY` ありで live labelling、無しで prompt 生成。`ORCH_MODEL` で opus/sonnet/haiku 切替）

## この実験が示していないこと

- **live labelling の品質**（Opus が付ける日本語ラベルの良し悪し）。key が要る。(i) の harness でそのまま測れる。
- **embedding の優劣**。silhouette は上記 caveat のとおり比較用の同一指標でないと意味が薄い。
- **決定性**。step 関数直呼びは乱数固定できず（[[offline-local-clustering]]）、Claude labelling は temperature 固定不可。
- 小型ローカルモデルの**意味忠実性**は別途注意（[[local-llm-extraction-faithfulness-2026-10-05]]）。この実験は抽出をスキップしているため該当しないが、抽出を含める場合は効く。

## 次の clean experiment

`factor_under_test = embedding provider` だけを変え（local vs OpenAI `text-embedding-3-large` vs Gemini）、clustering / labelling / judge を固定して cluster 品質を blind 比較する。embedding model が現状ハードコード（`paraphrase-multilingual-mpnet-base-v2` 固定）なので、**選択可能化が前提作業**。[[experiment-methodology]]

## 関連

- 考察・意思決定: [[claude-provider-connection-proposal-2026-10-17]]
- provider 一覧と埋め込みの壁: [[llm-providers]]
- キー不要のローカル経路: [[offline-local-clustering]] / [[cli]]
