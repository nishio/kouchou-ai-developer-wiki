---
type: analysis
summary: `run_workflow()` を default にできていない理由は docs 不足より実装差分で、初期入力・状態管理・設定キー・可視化出力契約に未吸収のギャップがある
sources:
  - github-dev-docs.md
  - source-code.md
---

# `run_workflow()` default 化の blocker

[[refactoring-status]] では Phase 3b を「実装あるが dormant」と書いている。current `main@b4d4bcf` を読むと、これは単に CLI / API から呼ばれていないというだけではなく、**legacy `.run()` が持つ実運用上の責務を workflow path がまだ吸収していない** ため、と整理するのが正確。[[source-code]]より

## 結論

default 化を止めている blocker は少なくとも 4 つある。

1. **初期入力 artifact の受け渡しが未実装**
2. **status / rerun / plan の永続化が workflow path に無い**
3. **`without_html` と `without-html` の設定キー drift**
4. **可視化 plugin の出力契約が current CLI とずれている**

## 1. 初期入力 artifact の受け渡しが未実装

`analysis.extraction` plugin は `inputs=["comments"]` を要求する。ところが `WorkflowEngine.run()` は、各 step への入力 artifact を **前段 step の `outputs.artifacts` からしか組み立てない**。`HIERARCHICAL_DEFAULT_WORKFLOW` に「comments を生成する step」は無く、engine 側にも初期 artifact を注入する仕組みが無い。したがって current 実装のままでは、builtin workflow の先頭 step である extraction が入力検証に失敗する構造になっている。[[source-code]]より

これは docs の不足ではなく、**workflow definition / engine / builtin plugin metadata の接合部** の欠落である。

## 2. status / rerun / plan の永続化が workflow path に無い

legacy `.run()` は `core/orchestration.py` の `initialization()` / `decide_what_to_run()` / `run_step()` / `termination()` を通じて、次をまとめて面倒見ている。[[source-code]]より

- `hierarchical_status.json` への `status`, `current_job`, `completed_jobs`, token usage の永続化
- 前回実行との差分を見た rerun 判定
- `--force`, `--only`, `--without-html` を含む plan 生成
- crashed run の lock / resume 的な扱い

一方 `run_workflow()` は `WorkflowEngine` を呼んで `WorkflowResult` を `PipelineResult` に変換するだけで、上記の状態管理をほぼ引き継いでいない。`apps/api` が現在 `.run()` を使っているのは、plugin dispatch そのものよりも **report status を保てる経路** を必要としているから、と読むのが自然。[[source-code]]より

## 3. `without_html` と `without-html` の設定キー drift

workflow 側の `HIERARCHICAL_DEFAULT_WORKFLOW` は visualization step の条件を `${not config.without_html}` で判定する。これに対して legacy 初期化 (`from_config()` → `initialization()`) は CLI フラグ `--without-html` を `config["without-html"]` に格納する。  
つまり `from_config()` で作った orchestrator から `run_workflow()` を呼ぶと、workflow condition はフラグを見落とす。逆に `from_dict()` は `normalize_config()` で `without_html` を使うため、こちらだけ別挙動になる。[[source-code]]より

このズレは「workflow path を default にする前に config schema を一本化すべき」ことを示している。

## 4. 可視化 plugin の出力契約が current CLI とずれている

`steps/hierarchical_visualization.py` は current `main` で self-contained な `report.html` を書く。これは `PR #825` 後の canonical な CLI 挙動である。  
しかし builtin `analysis.hierarchical_visualization` plugin は、docstring でなお「npm build」と説明し、返す artifact path も `ctx.output_dir / "index.html"` になっている。実 step 実装が書くファイル名と一致していない。[[source-code]]より

したがって workflow path を default にすると、少なくとも visualization step の artifact 契約は現状の CLI 仕様と噛み合わない。

## 含意

- Phase 3b の課題は「CLI の呼び先を `.run()` から `.run_workflow()` に置換する」だけではない
- 最低でも **初期入力注入**, **status 永続化**, **config key 正規化**, **visualization artifact 契約の更新** を揃えてからでないと default 化は危ない
- 逆に言うと、plugin system 自体を削除すべき根拠が見つかったわけではない。止まっているのは主に **運用経路との接続** である

## Open Questions

- 初期 `comments` artifact は engine が暗黙注入するべきか、input plugin を workflow に明示的に入れるべきか
- `hierarchical_status.json` のような legacy status file を workflow path でも維持するのか、別形式へ移すのか
- `without_html` / `without-html` をどの層で正規化するのがよいか
- visualization artifact は `report.html` に一本化するのか、Web/UI 用に別 output contract を持つのか

## Updates

- 2026-05-20: 初回作成。current `main@b4d4bcf` を読み、`run_workflow()` default 化を止めている実装差分を整理
