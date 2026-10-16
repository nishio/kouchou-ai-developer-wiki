---
title: "ソースコードレビュー棚卸し 2026-10-16"
type: analysis
summary: "main eb38328d の freshest コードを多エージェント+敵対的検証でレビュー。確定 10 件のうち 8 件を PR 化（#1015 Gemini全断/#1016 指定カテゴリ再実行/#1017 複製時埋め込み+作成検証/#1018 Azure temperature/#1019 cluster_nums/#1020 slug検証/#1021 status atomic）。残り 2 件（D ローカル埋め込み fallback・H 散布図薄表示）は仕様/表示判断待ち"
sources:
  - source-code.md
  - llm-grouping-supervised-classification.md
---

## 観測（freshness marker）

- 対象 commit: `work/kouchou-ai/` main **eb38328d**（2026-10-16 時点）。直近 feature（[#450](https://github.com/digitaldemocracy2030/kouchou-ai/pull/984) 埋め込みモデル独立選択、[#996](https://github.com/digitaldemocracy2030/kouchou-ai/pull/996) 指定カテゴリ分類、[#306](https://github.com/digitaldemocracy2030/kouchou-ai/pull/986) 散布図）を中心に、変更churn の高い analysis-core / API / public-viewer / admin を重点レビュー。
- 手法: 8 領域に finder を分散 → 各指摘を「実コードtrace / 仕様意図 / 再現」の 3 レンズで敵対的検証（多数決）→ 確定分を手元で再確認。確定 **10 件**（HIGH 1 / MEDIUM 8 / LOW 1）。
- このページは設計判断・公開可能な課題・対応 PR の粒度まで。実環境 URL・secret・デプロイ詳細は載せない（[[contributing]] の公開境界）。

## 修正済み（PR 化）

### 1. Gemini 埋め込みが常に失敗する（HIGH, [#450](https://github.com/digitaldemocracy2030/kouchou-ai/pull/984) 由来）→ PR [#1015](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1015)

`services/llm.py` の `request_to_gemini_embed` は統合 `google-genai`(>=1.0) の `client.models.embed_content()` を呼ぶ。実レスポンス `EmbedContentResponse` は `.embedding`(単数) ではなく **`.embeddings`(複数, 各 `ContentEmbedding.values`)** を持つが、`extract_embedding_values` は単数 `.embedding` object と dict 系しか解釈せず、実 SDK object では常に `None` → `RuntimeError`。#450 で追加した Gemini 埋め込み選択は実質まったく機能しない状態だった。

- 根因の二次要因: 既存テストが `embed_content` を **dict** で mock しており実 SDK 形状と乖離、バグを検知できていなかった。
- 検証: lock 固定の `google-genai==1.62.0` の実型を introspect して `.embeddings` 複数形を確認。実 object 形状で mock するようテストを更新 + 回帰ユニットテスト追加。修正前コードで当該テストが `RuntimeError` で fail することを確認。
- 関連概念: [[llm-providers]]。

### 2. 指定カテゴリを変えても再実行されない（MEDIUM, [#996](https://github.com/digitaldemocracy2030/kouchou-ai/pull/996) 由来）→ PR [#1016](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1016)

`llm_grouping_specs.json` の `dependencies.params` に `predefined_groups` / `other_group_label` が未登録。`decide_what_to_run()` はこの list に挙がったキーしか前回実行と比較しないため、**同じ `output_dir` への増分再実行（-f なし）** でカテゴリ集合を変えても「nothing changed」でステップがスキップされ、古いカテゴリ・古い割当のまま残る。`discovery_prompt`/`assignment_prompt` を守る既存ガードテストの適用漏れだった。

- 修正: 2 キーを `dependencies.params` に追加 + 既存ガードテストに倣った spec 契約テストを追加。
- 関連概念: [[llm-grouping-supervised-classification]]。

## 確定 10 件の対応状況

いずれも 3/3 で確定済み。2026-10-16 に **6 件を追加 PR 化**（A・B・C・E・F・G、HIGH の #1015・#1016 と合わせ計 8 件）。残り **2 件（D・H）** は仕様/表示判断待ちの backlog。各 PR は CI green を確認。人間 attention 操作（reviewer 依頼・merge）は未実施（明示指示時のみ）。

| finding | 対応 |
|---|---|
| (HIGH) Gemini 埋め込み全断 | PR [#1015](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1015)（merge 済み判断は nishio） |
| 指定カテゴリ再実行漏れ | PR [#1016](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1016) |
| A. 複製時に埋め込みモデル欠落 | PR [#1017](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1017)（B と同梱） |
| B. admin 埋め込み検証の非接続 | PR [#1017](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1017) |
| C. Azure reasoning の temperature | PR [#1018](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1018) |
| E. from_dict の cluster_nums | PR [#1019](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1019) |
| F. create slug 未検証 | PR [#1020](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1020) |
| G. status.json の lock/atomic | PR [#1021](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1021) |
| D. ローカル埋め込み batch swap | backlog（要仕様判断） |
| H. 散布図の薄表示 no-op | backlog（要表示判断） |

以下は各 finding の詳細（A–H）。D・H に着手する場合は assignee 確認 → self-assign → `work/kouchou-ai/` の worktree で作業、の手順を踏む。

- **A. report duplicate の embedded-config fallback が埋め込みモデルを落とす**（MEDIUM, data-loss, [#450](https://github.com/digitaldemocracy2030/kouchou-ai/pull/984) 由来）。`report_duplicate.py` の `_build_analysis_core_config_from_embedded_config` は `ReportConfig(**cfg).model_dump()` で再生成するが、`ReportConfig` に `embedding` フィールドが無く extra は ignore されるため、config ファイル不在時の fallback 経路で元レポートの埋め込みモデルが欠落し、複製が既定モデルで別ベクトル空間を作る。`enable_source_link` 同様に `embedding.model` を再付与するのが素直。
- **B. admin create の埋め込み検証が効いていない**（MEDIUM, validation-gap, [#450](https://github.com/digitaldemocracy2030/kouchou-ai/pull/984) 由来）。`useAISettings` が算出する `embeddingModelError` が `page.tsx` の `validateFormValues` に渡されず、OpenRouter×非ローカル埋め込みのような必ず失敗する組合せがそのまま submit できる（抽出ステップの LLM コストを払った後に埋め込みステップで落ちる）。`modelError` と同様に検証ゲートへ接続すればよい。
- **C. Azure chat completion が reasoning model に temperature=0 を送る**（MEDIUM, correctness）。OpenAI 側は `_is_openai_reasoning_model` で temperature を省くガードがあるが、`request_to_azure_chatcompletion` には無い。o3/gpt-5 系 Azure デプロイで 400 になりステップが落ちる。Azure 側にも同等ガードが要る。
- **D. ローカル埋め込み fallback が batch 単位で別モデルに暗黙 swap**（correctness/robustness・要仕様判断）。`request_to_local_llm_embed` が全例外を捕まえて別モデル（768次元 mpnet）の `request_to_local_embed` を返す（1000件バッチ単位）。**当初の「混在次元で無言に壊れる（data-loss）」は不正確で、nishio 指摘で訂正**: `embedding.pkl` は `list[dict]` 保存なので書き込みは通るが、下流 `steps/hierarchical_clustering.py`（L228/230）の `np.asarray([...embeddings...])` が **pinned `numpy>=1.26` では混在次元を `ValueError: inhomogeneous shape` で即死**させる（実測: numpy 2.5.4）。したがって実挙動は 2 分岐 — **(1) 一部バッチだけ fallback → dict 保存は成功するが clustering で opaque に crash**（真因＝embedding 途中の endpoint fallback から遠く、原因が追いにくい失敗）、**(2) 全バッチ fallback → 次元が揃うので crash せず、設定と違う mpnet で silent に完走**（＝本当に silent なのはこちら。wrong model の data-quality 問題）。本質は「黙って別モデルに swap する」点なので、fix は silent swap をやめ **fail-fast（原因が分かる明確なメッセージ）か run 全体の明示判断**にするのが筋。severity は data-loss ではなく correctness/robustness。
- **E. `from_dict` + hierarchical で `cluster_nums` 未指定時に落ちる**（MEDIUM, correctness）。file 経路（`initialization`）は `cluster_nums=None` を埋めるが dict 経路（`normalize_config`）は意図的に未設定にする。default workflow の template `${config.hierarchical_clustering.cluster_nums}` が engine で解決不能になり `WorkflowExecutionError`。2 経路の既定を揃えるか、`reuse_umap_model` と同じく plugin 側で full config から読むのが筋。要再現確認。
- **F. create_report の slug 未検証**（MEDIUM, path-traversal / 要セキュリティ判断）。他の admin エンドポイントが `validate_slug` を通すのに対し、作成経路は `report.input` を検証せずファイルパス構築に使う。admin API キー保持が前提の authenticated path だが、他エンドポイントと一貫させ作成時も `validate_slug`（または `ReportInput.input` の field_validator）を入れるのが妥当。詳細な攻撃ペイロードは本ページに載せない。
- **G. report_status.json の読み書きが lock 無し・非 atomic**（MEDIUM, concurrency）。`load_status` 系が `_lock` 無しで global を再代入し、`save_status` は truncate→rewrite で非 atomic。バックグラウンド writer と GET /admin/reports が競合すると一瞬 0 件表示や取りこぼしが起こりうる。読み取りも lock 下に、書き込みは temp + `os.replace` で atomic 化。
- **H. 散布図のフィルタ済みラベルが薄くならない**（LOW, correctness, [#306](https://github.com/digitaldemocracy2030/kouchou-ai/pull/986) 由来）。`ScatterChart.tsx` で全点フィルタ済みクラスタのラベルを薄くする意図の hex 置換が、元の alpha が既に `cc` のため no-op。意図通り薄くするには置換先 alpha を下げるか base を `ff` にする。表示判断を含むので実機確認が要る。

## 次の作業

1. PR [#1015](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1015)・[#1016](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1016)・[#1017](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1017)〜[#1021](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1021) のレビュー・merge 判断（人間 attention 操作＝reviewer 依頼・merge は明示指示時のみ、現状未実施）。
2. backlog **D**（ローカル埋め込み fallback の silent swap）と **H**（散布図の薄表示）の採否・方針を nishio が判断。
3. 着手するものは着手前に assignee 確認 → self-assign。

## Open Questions

- D（ローカル埋め込み fallback）と H（薄表示）は「現状が意図的な挙動か」の仕様判断が残る。D は silent な別モデル代替が本当に望ましいか、H は filtered ラベルの視認性をどこまで下げるか。
- PR 分割は #450 系（A・B）を [#1017](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1017) に同梱、C/E/F/G を個別化して出した（レビュー面を小さく保つため）。merge 順の希望があれば nishio 判断。
