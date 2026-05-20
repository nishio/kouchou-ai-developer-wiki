---
type: analysis
summary: `run_workflow()` を default にできていない理由は docs 不足より実装差分で、初期入力・状態管理・設定キー・可視化出力契約に未吸収のギャップがある
sources:
  - github-dev-docs.md
  - source-code.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
---

# `run_workflow()` default 化の blocker

[[refactoring-status]] では Phase 3b を「実装あるが dormant」と書いている。current `main@b4d4bcf` を読むと、これは単に CLI / API から呼ばれていないというだけではなく、**legacy `.run()` が持つ実運用上の責務を workflow path がまだ吸収していない** ため、と整理するのが正確。[[source-code]]より

2026-05-20 の open PR `#840` では、この blocker のうち大半に既に着手が入っている。したがって本ページは「main にまだ無いが branch 上ではどう前進したか」と「それでも残る差分」を併記して読む。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

## 結論

default 化を止めていた blocker は少なくとも 4 つあり、2026-05-20 の branch 上ではこの 4 点にすべて先行実装が入った。

1. **初期入力 artifact の受け渡しが未実装**
2. **status / rerun / plan の永続化が workflow path に無い**
3. **`without_html` と `without-html` の設定キー drift**
4. **可視化 plugin の出力契約が current CLI とずれている**

## 1. 初期入力 artifact の受け渡しが未実装

`analysis.extraction` plugin は `inputs=["comments"]` を要求する。ところが `WorkflowEngine.run()` は、各 step への入力 artifact を **前段 step の `outputs.artifacts` からしか組み立てない**。`HIERARCHICAL_DEFAULT_WORKFLOW` に「comments を生成する step」は無く、engine 側にも初期 artifact を注入する仕組みが無い。したがって current 実装のままでは、builtin workflow の先頭 step である extraction が入力検証に失敗する構造になっていた。[[source-code]]より

この点は open PR `#840` の `067e8a5` で **初期 `comments` artifact を `config["input"]` から seed する方向へ補修済み**。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

これは docs の不足ではなく、**workflow definition / engine / builtin plugin metadata の接合部** の欠落である。

## 2. status / rerun / plan の永続化が workflow path に無い

legacy `.run()` は `core/orchestration.py` の `initialization()` / `decide_what_to_run()` / `run_step()` / `termination()` を通じて、次をまとめて面倒見ている。[[source-code]]より

- `hierarchical_status.json` への `status`, `current_job`, `completed_jobs`, token usage の永続化
- 前回実行との差分を見た rerun 判定
- `--force`, `--only`, `--without-html` を含む plan 生成
- crashed run の lock / resume 的な扱い

一方 `run_workflow()` は `WorkflowEngine` を呼んで `WorkflowResult` を `PipelineResult` に変換するだけで、上記の状態管理をほぼ引き継いでいなかった。`apps/api` が現在 `.run()` を使っているのは、plugin dispatch そのものよりも **report status を保てる経路** を必要としているから、と読むのが自然。[[source-code]]より

この点も open PR `#840` の `71e603a`, `0c71649`, `24e02cc` で、`hierarchical_status.json`, `completed_jobs`, `previous`, `previously_completed_jobs`, rerun plan 読み込みに加え、CLI default path の workflow 側切替まで進んでいる。  
残る論点は、legacy `.run()` と完全同等の挙動か、e2e / Web API 運用が依存する status semantics をすべて満たすか、である。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

## 3. `without_html` と `without-html` の設定キー drift

workflow 側の `HIERARCHICAL_DEFAULT_WORKFLOW` は visualization step の条件を `${not config.without_html}` で判定する。これに対して legacy 初期化 (`from_config()` → `initialization()`) は CLI フラグ `--without-html` を `config["without-html"]` に格納する。  
つまり `from_config()` で作った orchestrator から `run_workflow()` を呼ぶと、workflow condition はフラグを見落とす。逆に `from_dict()` は `normalize_config()` で `without_html` を使うため、こちらだけ別挙動になる。[[source-code]]より

この点は open PR `#840` の `067e8a5` と `cc17509` で、legacy 初期化と workflow condition の双方で両 key を吸い、競合時の deterministic sync まで入った。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

このズレは「workflow path を default にする前に config schema を一本化すべき」ことを示している。

## 4. 可視化 plugin の出力契約が current CLI とずれている

`steps/hierarchical_visualization.py` は current `main` で self-contained な `report.html` を書く。これは `PR #825` 後の canonical な CLI 挙動である。  
しかし builtin `analysis.hierarchical_visualization` plugin は、docstring でなお「npm build」と説明し、返す artifact path も `ctx.output_dir / "index.html"` になっていた。実 step 実装が書くファイル名と一致していなかった。[[source-code]]より

この点は open PR `#840` の `067e8a5` と `cc17509` で `report.html` 契約と option forwarding が補修され、branch 上では major blocker ではなくなった。[[pr-840-workflow-defaultization-observation-2026-05-20]]より

## いま残る差分

- e2e test 群はまだ legacy `.run()` 前提で、workflow path を本当に production-ready と言えるだけの end-to-end 証拠が薄い
- `apps/api` は `analysis-core` CLI を叩くため branch 上では実質 workflow path に寄るが、`--without-html` 固定など API 独自の運用条件をまだ維持している
- docs / README / deprecated README の一部に legacy path を canonical に見せる説明が残る
- branch は open PR の段階であり、main の canonical state にはまだ反映されていない

## 含意

- Phase 3b の課題は「CLI の呼び先を `.run()` から `.run_workflow()` に置換する」だけではない
- 最低でも **初期入力注入**, **status 永続化**, **config key 正規化**, **visualization artifact 契約の更新** を揃えてからでないと default 化は危ない
- 2026-05-20 の open PR `#840` により、この 4 点は「未着手」ではなく **先行実装が出て review 中** の段階へ進んだ
- 逆に言うと、plugin system 自体を削除すべき根拠が見つかったわけではない。止まっているのは主に **運用経路との接続** である

## Open Questions

- 初期 `comments` artifact は engine が暗黙注入するべきか、input plugin を workflow に明示的に入れるべきか
- `hierarchical_status.json` のような legacy status file を workflow path でも維持するのか、別形式へ移すのか
- `without_html` / `without-html` をどの層で正規化するのがよいか
- visualization artifact は `report.html` に一本化するのか、Web/UI 用に別 output contract を持つのか

## Updates

- 2026-05-20: 初回作成。current `main@b4d4bcf` を読み、`run_workflow()` default 化を止めている実装差分を整理
- 2026-05-20: open PR [[pr-840-workflow-defaultization-observation-2026-05-20]] を反映し、4 blocker のうち初期 artifact / status / key drift / visualization 契約には先行実装が出ていると追記
- 2026-05-20: 同 PR の追加 commit を反映し、CLI default path も branch 上では workflow 側へ切り替わったため、残差分を e2e / API 運用 / docs 側へ整理し直した
