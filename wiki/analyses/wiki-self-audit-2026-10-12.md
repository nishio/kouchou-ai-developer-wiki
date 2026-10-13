---
type: analysis
summary: "developer-wiki 自身を 6 レンズ（内容健全性 / 構造ライフサイクル / コード乖離 / スキーマ / スクリプト / 公開境界）で監査し敵対的検証した結果と、2026-10-12 に適用した修正・残課題"
sources:
  - source-code.md
  - github-dev-docs.md
---

# Wiki 自己監査 2026-10-12

## このページの目的

developer-wiki そのものを「改善すべき点はないか」という問いで棚卸しした記録。機械 lint（`scripts/lint_wiki.py`）は 0 件で健全だったため、**lint が構造的に拾えない判断レベルの drift** を対象にした。適用した修正・副作用・残課題を一箇所に固定化し、次の保守セッションが同じ監査を繰り返さなくて済むようにする。

## 監査方法

6 レンズを並列 finder で走らせ、各指摘を**敵対的 verifier**（証拠を自分で再現し、既対応・過大評価・CLAUDE.md 違反なら棄却）で再検証した（計 12 subagent、全 CONFIRMED / PARTIAL を独立に裏取り）。

レンズ: ①内容健全性・自wiki矛盾 ②構造・スケール・dated snapshot のライフサイクル ③コード→wiki の乖離 ④CLAUDE.md / README / llm-wiki の policy 精度 ⑤スクリプト正しさ・自動化の梃子 ⑥公開境界・鮮度 self-audit。

## この pass で適用した修正

### 1. 入口・文書の整合
- `index.md`: 「305 ページ」literal を除去（drift するので index.txt 参照へ）。「直近の状態」を 2026-10-12（[[daily-report-2026-10-12]] / [[meeting-report-2026-10-10]]）へ更新。meeting-report の「最新」pointer を 2026-06-01→2026-10-10 に修正し、唯一未リンクだった concept（meeting-report-2026-10-10）を回収。
- `CLAUDE.md`: 「305 ページ（2026-10-07 時点）」「onboarding 5 ステップ」「Entities 全件」を drift しない表現へ訂正（Entities は index.md 設計上 curated 入口のみ）。scripts ツリーに CI gate の `check_pages_links.py` を明記し「主要スクリプトのみ」と注記。`sources` は source/concept 必須・他 type 任意と実態（lint の挙動）に合わせた。
- `README.md`: 「302 ページ」「5 ページ導線」の hardcode 数字を除去。

### 2. first-read ページの内容訂正（`## Updates` 方式で履歴を残す）
- [[architecture-overview]] / [[kouchou-ai]]: Next.js 15→16（main は `^16.3.8`）。自wiki内で gotchas 等は既に 16 で矛盾していた。データフロー図の `PipelineOrchestrator.run()` も `run_default()` に修正。
- [[cli]]: ライブラリ利用例 `run()`→`run_default()`、実行モード説明を「`run_default()`→`run_workflow()` が canonical、`run()` は `DeprecationWarning` つき deprecated」に統一（本文が同ページの L125 lint 注記・[[pipeline]] と矛盾していた）。解決済みの Open Question「PyPI 公開＋GHA 自動リリース」を除去。
- [[pipeline]] / [[plugin-system]]: `analysis_mode=llm_grouping` は engine レベルで出荷済み（#866 / `4f893ab5`、2026-05-25 main 入り。`register_all` が `llm_grouping` を含む 9 plugin を登録）だが、**admin / `apps/api` は `analysis_mode` 未受け渡しでユーザ到達は未**（#176 / 未 merge PR #987）、という「engine 出荷済み・プロダクト到達未」の状態を追記。plugin-system の builtin 数を「8」→「9」に訂正。[[pipeline]] の解決済み Open Question「レポート再利用（#19）」を除去（`report_duplicate.py` 実装済み）。
- [[refactoring-status]]: Phase 2.5 の PyPI 版を `0.1.2`→現行 `0.1.3`（AGPL-3.0、旧 MIT 版 yank 済み）に訂正。deployment.md 等の日付つき `0.1.2` 歴史観測は dated-correct なので据え置き。

### 3. スクリプト堅牢化 & lint 強化
- `refresh_logs.py`: (a) `log.md` のヘッダが strict HEADER 正規表現に外れる（型名 typo 等）と entry が両ログから無警告で消える問題に、書き換え前 hard-fail ガードを追加。(b) 窓内 entry を編集すると append-only の `log.txt` に旧版が孤児として残る問題に、cutoff を merge 前に計算し「窓外 entry は無条件保持・窓内は log.md と一致する物だけ残す」reconcile を追加。
- `lint_wiki.py`: WIKILINK 正規表現が `[[page#anchor]]` を取りこぼす問題を修正。「ドキュメント整合」セクションを追加 ―― ①`CLAUDE.md`/`index.md` の「N ページ」literal と実ページ数の不一致検出、②`index.md` の meeting-report pointer の stale 検出、③`sources:` の bare wiki ページ参照（space/slash/URL を除外）の未解決検出。
- `build_index_txt.py`: summary 内の tab/CR を空白へ畳む（TSV 破壊防止）。

### 4. 公開境界の sanitize（PR-887 系）
- [[codex-log-pr-887-deploy-investigation-2026-06-01]] / [[pr-887-pr-888-runtime-build-removal-episode-2026-06-01]] が revision ID・replica health JSON・コンテナログ・resource サイズを公開 wiki に残置しており、兄弟ページ（sanitize 済み）と矛盾していた（episode には「公開 wiki にはサニタイズ版だけを残せる」という事実に反する記述もあった）。設計の教訓（deploy 判定は安定 URL 200 ではなく新 revision readiness で見る／起動時 `next build` が OOM で SIGKILL）を残しつつ、具体値を一般語へ置換。verbatim は `raw/deploy-detail-preservation/`（gitignored）に local 退避。[[deploy-success-but-nothing-changed-story-2026-06-01]] の軽微なログ断片も softening。

## 作業の副作用として検出・修正

- `work/kouchou-ai` の HEAD が `main` ではなく feature ブランチ `codex/issue-52-scatter-linked-text` に detached していた。reflog から、本監査の code-coverage finder が #52 を調べる際に（「git を触るな」の指示に反して）`git checkout` し HEAD を動かしたのが原因と判明。CLAUDE.md「HEAD は常に main」原則違反なので `main` に復帰済み。

## 残課題（人間判断が要る）

- **dated snapshot のライフサイクル**: ~211 の dated page に supersession/archive policy も machine-readable status も無い。唯一の archive 規律＝meeting-report rotation は 4 ヶ月 silent に途絶していた（10-10 で一括退避済み）。additive な `status: superseded` + `superseded_by:` frontmatter 層（削除なし・git がアーカイブ、build_index_txt が prefix、lint が参照先チェック）を CLAUDE.md 節として入れるかは要判断。**`status` の意味は「より新しい wiki snapshot が存在」であって「live に対し検証済み current」ではない**と定義すること（情報鮮度の明示と整合）。
- **PR-887 の raw verbatim**: 現在 `raw/deploy-detail-preservation/`（local, gitignored）に退避済み。デプロイ詳細の一次置き場は Google Drive「広聴AI-Azureデモ環境」なので、そちらへ移す判断は権限保持者（大木・西尾・小野）。
- **work/kouchou-ai の残渣**: 別セッション（#982–#988 を進めた session）の agent worktree が約 13 個、`.env.example.bak` の untracked が 1 個。別セッションの作業なので未処理。棚卸しは要判断。
- **CLAUDE.md の冗長性**: public-boundary / work freshness / 二分原則などが 操作 と 運用方針 で 3–6 回ずつ再掲される。ただし prose は未 drift（drift したのは数字だけ）で、一部は locality-of-reference として意図的。gut せず verbatim ペア（deploy 境界の L40/L172 等）のみ保守的に統合、が安全。

## 健全と確認できた軸（やらなくてよい）

- **用語ルール**（Jigsaw / LLM grouping）違反ゼロ。49 hit すべて「混同を避けよ」という警告文脈で、一般カテゴリを Jigsaw と誤称した本文は 0。
- **security / 脆弱性 / secret 境界** clean。CVE/GHSA ID・affected version・exploit 手順・鍵の実値・Azure live URL はいずれも 0。Dependabot は issue/PR/優先度 pointer のみ（公開境界どおり）。
- **scripts は happy path で idempotent**（2 回実行で byte 一致）。data-loss はヘッダ編集/typo でのみ発火する latent risk で、上記 guard で塞いだ。

## Open Questions

- lifecycle policy（`status`/`superseded_by` 層）を CLAUDE.md に正式採用するか。採用するなら rotating series（meeting-report、issue-backlog-audit、daily-report）に「latest in series」導線を足すか。
- freshness marker を lint 強制するか。prose scrape は false positive が多いので、強制するなら source 系に明示 frontmatter field（例 `last_read: YYYY-MM-DD`）を足してそれを検査する形が現実的。8 本の旧 Slack source が `最終読解日` を欠くが、6 本は raw snapshot pin 済みで drift risk は低い。

## Updates

- 2026-10-12: 初版作成。6 レンズ監査 → 敵対的検証 → 修正適用の filing-back。[[wiki-driven-workflow]] の運用下で developer-wiki を自己点検した記録。
- 2026-10-12: 残課題①「dated-page lifecycle policy」を nishio 判断で**採用**。CLAUDE.md に「スナップショットのライフサイクル」節（opt-in の `status: superseded` + `superseded_by:`、意味は「より新しい snapshot が存在」で live 照合済みではない）、`build_index_txt.py` の superseded prefix、`lint_wiki.py` の `superseded_by` 実在チェックを追加。demo として [[issue-backlog-audit-2026-09-09]] / [[issue-backlog-audit-2026-10-11]] → [[issue-backlog-audit-2026-10-12]]、[[current-status-2026-06-30]] → [[current-status-2026-10-05]] を superseded マーク（zero migration、残りは今後 incremental）。残課題②PR-887 verbatim の Drive 移送、③`work/` worktree 棚卸しは保留（③は open PR 処理後）。
- 2026-10-12: 本監査の数時間後に #176 統合 PR #987 が kouchou-ai main に merge（`c33d264a`）。Batch 2 で「engine 出荷済み・プロダクト到達未」と書いた [[pipeline]] / [[plugin-system]] を「到達も main 入り」に追補訂正、index.md の「#982–#987 未 merge」も softening。**同一セッション内で concurrency により freshness が動いた実例**（別セッションが PR を land → 自分の記述が数時間で stale 化）。freshness marker は「ページ更新日」でなく「その時点の観測」である、という原則を地で行った。
- 2026-10-13: Batch 4（PR-887 sanitize）の粒度を nishio がレビューし**現状維持で確定**。確認すると、実際に除去したのは生テレメトリ（health JSON・console/system ログ逐語）と実環境の個体識別子（revision 実 ID・resource サイズ実値行）だけで、portable な教訓（`exit 137`=OOM SIGKILL、`latestRevisionName ≠ latestReadyRevisionName` の false-positive 機序、Unhealthy/Degraded・progress deadline 超過の状態語）と、**narrative の中でそれ自体が教訓になっている resource 数字**（[[deploy-success-but-nothing-changed-story-2026-06-01]] L70 の「1Gi→2Gi」= build のためだけに 24h 分メモリを固定費で払うトレードオフの肝）は意図的に残置済み。方針として明文化: sanitize の目的は secret 防衛ではなく**境界衛生＋兄弟ページ整合**で、生データ/個体識別子だけ落とし教育価値は削らない。verbatim は `raw/deploy-detail-preservation/`（gitignored）退避で**可逆**。残課題②の sanitize 面はこれで close（verbatim の Drive「広聴AI-Azureデモ環境」移送は引き続き権限保持者の手作業）。
