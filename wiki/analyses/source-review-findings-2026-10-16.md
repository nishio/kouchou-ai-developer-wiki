---
title: "ソースコードレビュー棚卸し 2026-10-16"
type: analysis
summary: "main eb38328d の freshest コードを多エージェント+敵対的検証でレビュー。確定 10 件。Gemini 埋め込み全断（#450 由来, HIGH）を PR #1015、指定カテゴリ再実行漏れ（#996 由来）を PR #1016 で修正。残り 8 件は nishio 判断待ちの backlog として整理"
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

## backlog（nishio 判断待ち、未着手）

いずれも 3/3 で確定済み。優先度と採否は設計判断を含むため棚卸しのみ。着手時は assignee 確認 → self-assign → `work/kouchou-ai/` の worktree で作業、の手順を踏む。

- **A. report duplicate の embedded-config fallback が埋め込みモデルを落とす**（MEDIUM, data-loss, [#450](https://github.com/digitaldemocracy2030/kouchou-ai/pull/984) 由来）。`report_duplicate.py` の `_build_analysis_core_config_from_embedded_config` は `ReportConfig(**cfg).model_dump()` で再生成するが、`ReportConfig` に `embedding` フィールドが無く extra は ignore されるため、config ファイル不在時の fallback 経路で元レポートの埋め込みモデルが欠落し、複製が既定モデルで別ベクトル空間を作る。`enable_source_link` 同様に `embedding.model` を再付与するのが素直。
- **B. admin create の埋め込み検証が効いていない**（MEDIUM, validation-gap, [#450](https://github.com/digitaldemocracy2030/kouchou-ai/pull/984) 由来）。`useAISettings` が算出する `embeddingModelError` が `page.tsx` の `validateFormValues` に渡されず、OpenRouter×非ローカル埋め込みのような必ず失敗する組合せがそのまま submit できる（抽出ステップの LLM コストを払った後に埋め込みステップで落ちる）。`modelError` と同様に検証ゲートへ接続すればよい。
- **C. Azure chat completion が reasoning model に temperature=0 を送る**（MEDIUM, correctness）。OpenAI 側は `_is_openai_reasoning_model` で temperature を省くガードがあるが、`request_to_azure_chatcompletion` には無い。o3/gpt-5 系 Azure デプロイで 400 になりステップが落ちる。Azure 側にも同等ガードが要る。
- **D. ローカル埋め込み fallback が batch 単位で別モデルに暗黙 swap**（MEDIUM, data-loss）。`request_to_local_llm_embed` が全例外を捕まえて別モデル（768次元 mpnet）の `request_to_local_embed` を返す。1000件バッチ単位で呼ばれるため一部バッチだけ次元が変わり、混在した埋め込み空間が無言で出力される。暗黙 swap せず fail させるか、run 全体の明示判断にすべき。要仕様判断。
- **E. `from_dict` + hierarchical で `cluster_nums` 未指定時に落ちる**（MEDIUM, correctness）。file 経路（`initialization`）は `cluster_nums=None` を埋めるが dict 経路（`normalize_config`）は意図的に未設定にする。default workflow の template `${config.hierarchical_clustering.cluster_nums}` が engine で解決不能になり `WorkflowExecutionError`。2 経路の既定を揃えるか、`reuse_umap_model` と同じく plugin 側で full config から読むのが筋。要再現確認。
- **F. create_report の slug 未検証**（MEDIUM, path-traversal / 要セキュリティ判断）。他の admin エンドポイントが `validate_slug` を通すのに対し、作成経路は `report.input` を検証せずファイルパス構築に使う。admin API キー保持が前提の authenticated path だが、他エンドポイントと一貫させ作成時も `validate_slug`（または `ReportInput.input` の field_validator）を入れるのが妥当。詳細な攻撃ペイロードは本ページに載せない。
- **G. report_status.json の読み書きが lock 無し・非 atomic**（MEDIUM, concurrency）。`load_status` 系が `_lock` 無しで global を再代入し、`save_status` は truncate→rewrite で非 atomic。バックグラウンド writer と GET /admin/reports が競合すると一瞬 0 件表示や取りこぼしが起こりうる。読み取りも lock 下に、書き込みは temp + `os.replace` で atomic 化。
- **H. 散布図のフィルタ済みラベルが薄くならない**（LOW, correctness, [#306](https://github.com/digitaldemocracy2030/kouchou-ai/pull/986) 由来）。`ScatterChart.tsx` で全点フィルタ済みクラスタのラベルを薄くする意図の hex 置換が、元の alpha が既に `cc` のため no-op。意図通り薄くするには置換先 alpha を下げるか base を `ff` にする。表示判断を含むので実機確認が要る。

## 次の作業

1. PR [#1015](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1015) / [#1016](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1016) の CI 確認とレビュー（人間 attention 操作＝reviewer 依頼・merge は明示指示時のみ）。
2. backlog A–H の採否・優先度を nishio が判断。A・B は #450 の後始末として #1015 と同系統、C–E は analysis-core の堅牢化、F はセキュリティ、G は運用、H は UI 微調整。
3. 着手するものは個別に issue/PR 化し、着手前に assignee 確認 → self-assign。

## Open Questions

- D（ローカル埋め込み fallback）と H（薄表示）は「現状が意図的な挙動か」の仕様判断が残る。D は silent な別モデル代替が本当に望ましいか、H は filtered ラベルの視認性をどこまで下げるか。
- backlog を 1 本の issue に束ねるか個別化するか。#450 系（A・B）は #1015 と合わせて「埋め込みモデル機能の後始末」として束ねる手もある。
