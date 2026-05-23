---
type: analysis
summary: "`run_workflow()` default 化を止めていた主 blocker は main で解消され、Phase 8 cleanup 後はいま何が follow-up だけ残っているかを切り分ける履歴ページ"
sources:
  - github-dev-docs.md
  - source-code.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
  - report-html-non-web-canonical-decision-2026-05-23.md
---

# `run_workflow()` default 化の blocker

current `main@e5ed743` では、PR `#840` 相当による workflow default 化だけでなく、後続の legacy cleanup まで main に入った。したがって本ページは、もはや「いま default 化を止めている blocker 一覧」ではなく、**何が blocker だったか / main でどこまで解消されたか / 何が follow-up にだけ残ったか** を整理する履歴ページとして読むのが近い。[[source-code]]より [[pr-840-workflow-defaultization-observation-2026-05-20]]より

## 結論

default 化を止めていた blocker は少なくとも 4 つあり、current `main` ではこの 4 点に対応する実装が入った。

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

- `hierarchical_status.json` の `duration` / `estimated_cost` / progress semantics にはなお legacy との差分があるが、[[phase3b-exit-criteria]] では production blocker でなく follow-up と位置づけた
- `apps/api` は current `main` でも `--without-html` を固定しており、CLI 既定の `report.html` 出力との役割分担はなお分かれている
- plugin wrapper の多くは still legacy-step wrapper であり、workflow-native 実装へどこまで寄せるかは別論点として残る
- 2026-05-24 の current state では Phase 8 cleanup まで merge 済みで、本ページに残る価値は blocker 履歴と follow-up の切り分けにある

## いま follow-up に残った理由

workflow path は main で production 入口へ入ったが、なお follow-up が要る理由は次の通り。[[source-code]]より

1. **rerun 判定の exact semantics はなお観測対象である**
   current main は実用互換に達したが、legacy path と byte-level に同じ判断をすること自体は完了条件に含めていない。

2. **status file の意味論差分は残る**
   `hierarchical_status.json` の主要項目は実用互換だが、duration や progress 表現まで完全同等ではない。項目別の棚卸しは [[hierarchical-status-semantics]] を参照。[[source-code]]より

3. **plugin はまだ workflow-native 実装というより legacy step の薄い wrapper が多い**
   したがって config や artifact の契約差分が、今後も別の step で露出する可能性がある。

4. **実データバリエーションの証拠はまだ増やせる**
   merge blocker ではないが、real data / provider 差分の e2e は今後も厚くできる。

5. **docs / 開発者メンタルモデルの残差は引き続き観測が要る**
   主要 docs は更新されたが、古い手順書や口頭前提が残る可能性はある。

## 標準経路化後の残課題（優先順）

1. **status semantics の follow-up**
   `hierarchical_status.json` の duration / progress / estimated_cost をどこまで寄せるかを決める。

2. **実データ寄り e2e の拡充**
   merge blocker ではないが、provider 差分や artifact 欠損パターン差分は今後も足せる。

3. **plugin wrapper / 拡張経路の整理**
   builtin plugin の多くはなお legacy step wrapper なので、workflow-native 実装へどこまで寄せるか、外部 `plugins/analysis/` や YAML workflow をどう本当に使うかは別途残る。

4. **`report.html` の位置づけ整理**
   current main でも CLI 向け観察用HTMLと Web canonical output は分かれたままであり、2026-05-23 の maintainer 判断でも `report.html` は Web canonical にしない。[[report-html-non-web-canonical-decision-2026-05-23]]より

5. **release hardening**
   current package / CI / PyPI publish は動くが、Trusted Publishing、`apps/api` 互換まで含む release gate、metadata の詰めは refactoring 完了後の別タスクとして残る。

## 含意

- Phase 3b の課題は「CLI の呼び先を `.run()` から `.run_workflow()` に置換する」だけではない
- 最低でも **初期入力注入**, **status 永続化**, **config key 正規化**, **visualization artifact 契約の更新** を揃えてからでないと default 化は危ない
- PR `#840` 相当の merge により、この 4 点は current `main` で概ね解消された
- workflow default 化の主戦場は終わり、Phase 8 cleanup も current `main` で完了した。次の論点は status semantics / plugin wrapper / release hardening へ移った
- 逆に言うと、plugin system 自体を削除すべき根拠が見つかったわけではない。止まっているのは主に **運用経路との接続** である

## Open Questions

- 初期 `comments` artifact は engine が暗黙注入するべきか、input plugin を workflow に明示的に入れるべきか
- `hierarchical_status.json` のような legacy status file を workflow path でも維持するのか、別形式へ移すのか
- `without_html` / `without-html` をどの層で正規化するのがよいか

## Updates

- 2026-05-20: 初回作成。current `main@b4d4bcf` を読み、`run_workflow()` default 化を止めている実装差分を整理
- 2026-05-20: open PR [[pr-840-workflow-defaultization-observation-2026-05-20]] を反映し、4 blocker のうち初期 artifact / status / key drift / visualization 契約には先行実装が出ていると追記
- 2026-05-23: maintainer 判断 [[report-html-non-web-canonical-decision-2026-05-23]] を反映し、`report.html` 一本化の問いを Open Questions から外した
- 2026-05-20: 同 PR の追加 commit を反映し、CLI default path も branch 上では workflow 側へ切り替わったため、残差分を e2e / API 運用 / docs 側へ整理し直した
- 2026-05-20: 「まだ安全に切り替えられない理由」と「残課題の優先順」を追記し、workflow path の現在位置を説明しやすくした
- 2026-05-20: 追加 commit により CLI `main()` と API `report_launcher` の service-level 確認まで進んだこと、pre-push hook blocker が PR `#841` に切り出されたことを反映
- 2026-05-20: さらに failure semantics、duplicate/reuse 経路、`from_config()` rerun plan integration の確認まで進んだことを反映し、「まだ足りないこと」を real LLM を含む e2e と docs 側へ寄せて更新
- 2026-05-21: real workflow rerun e2e と workflow failure step status API の確認を反映し、残課題を「e2e 未着手」ではなく「実データバリエーションと運用経路の厚み不足」と表現し直した
- 2026-05-21: 「実装上かなり切り替わっている」と「main で標準経路化が完了した」は別だ、という読み分けを含意に追記
- 2026-05-21: `hierarchical_status.json` の項目別 semantics 棚卸しを [[hierarchical-status-semantics]] に分離し、status file blocker の中身を参照可能にした
- 2026-05-21: `04a8e97` により refactoring docs と deprecated README の主要 drift も branch 上で更新済みになったため、docs blocker を「大半更新済み、残差確認フェーズ」へ寄せた
- 2026-05-21: `main@0e1552d` を再確認し、PR #840 相当 merge 後の current state に合わせて、本ページを「未解決 blocker 一覧」から「解消された blocker と follow-up の整理」へ更新
- 2026-05-24: `work/kouchou-ai/main@e5ed743` を確認し、Phase 8 cleanup も main に入った前提へ更新。残課題の優先順から legacy 削除を外し、status semantics / plugin wrapper / release hardening 側へ寄せ直した
