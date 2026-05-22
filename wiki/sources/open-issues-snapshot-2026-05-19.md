---
type: source
summary: "2026-05-19 時点の `digitaldemocracy2030/kouchou-ai` open issue を新しい順に読み、`analysis-core` CLI 整備と Web/静的公開まわりの事故修正に論点が集中していることを記録した snapshot"
sources:
  - github-dev-docs.md
  - source-code.md
---

2026-05-19 に GitHub 上の `digitaldemocracy2030/kouchou-ai` open issues を新しい順で再取得し、9 月までの優先度判断に使うための観測メモ。live state なので、当日時点の snapshot として扱う。コード側の一次参照は `work/kouchou-ai` で `origin/main@2b92ed1c14cc55ebc7a23570fa0548ec9635c9c2` を見た。`work/kouchou-ai` の checkout は `codex/issue-830-auto-cluster-nums` で、追跡先 branch が削除済みのため `git pull --ff-only` 自体は失敗したが、`origin/main` の fetch までは成功している。[[github-dev-docs]]より [[source-code]]より

## Findings

### 2026-05-19 時点で open PR は 0 本

`gh pr list -R digitaldemocracy2030/kouchou-ai --state open` は空配列を返した。したがって current state は、**PR review queue を捌く局面ではなく、issue を次の実装単位に切り直す局面** と読める。[[github-dev-docs]]より

### 直近 4 件は `analysis-core` CLI の canonical path 整備に集中

2026-05-18 〜 2026-05-19 に新しく見えた open issue は次の 4 件。

- `#836` Document filesystem-based usage for analysis-core CLI
- `#837` Add config and input preflight validation to analysis-core CLI
- `#838` Evaluate output artifact validation for analysis-core CLI
- `#833` Issue #685 follow-up: reimplement remote HTTP/CSP/UUID fixes on current apps/* tree

このうち `#836` `#837` `#838` は、旧 `server/broadlistening/...` 前提だった `#721` を current `packages/analysis-core/` 向けに分解した子 issue である。[[github-dev-docs]]より

### `#721` は旧 pipeline 改修ではなく current `analysis-core` umbrella に読み替え済み

`#721` には 2026-05-19 のコメントで、次の整理が追記されている。

- canonical な利用経路は `python -m analysis_core` / `kouchou-analyze`
- 旧 `server/broadlistening/...` の改善 issue としては扱わない
- 実作業は `#836` `#837` `#838` に分割して current CLI path を前提に追う

したがって `#721` 系は、**deprecated shim を延命する論点ではなく、v5 的な `analysis-core` CLI を contributor / agent が安全に使うための足場** と読むのが正確。[[github-dev-docs]]より [[source-code]]より

### `#833` は `#685` を current `apps/*` tree へ再実装し直すための follow-up

`#833` は、`Issue #685` 自体はまだ有効だが、対応を試みた `PR #735` は current tree では stale なので revive ではなく再実装すべき、という整理。論点としては次が混ざっている。

- public IP + HTTP 環境での `crypto.randomUUID()` 問題
- CSP による asset / image load 制約
- `apps/admin` の LocalLLM model auto-fetch UX

この issue は、**remote/self-hosted な Web 利用を 9 月前にどこまで support するか** を問う位置にある。[[github-dev-docs]]より

### Web UI / static export の未解決バグは 2026-03 以前のものも残っている

新しい順で読むと、`analysis-core` 系の直後に次の Web/静的公開まわりの issue が並ぶ。

- `#820` 静的エクスポート環境向けの CSP 設定ガイド
- `#818` Plotly PNG download が CSP の `img-src` 制約で死ぬ可能性
- `#716` レポート作成時のエラーログを Web UI から確認できない
- `#707` API が実際には使えるのに接続チェックが誤判定する
- `#683` 公開レポート 0 件時に static export が落ちる

これらはそれぞれ独立に見えるが、共通して **「非専門家向け Web UI / static 公開で、失敗時に何が起きたか分かりにくい」** 問題に属する。[[github-dev-docs]]より

### React dev overlay 問題 `#799` は current `main` の再現性が弱い

`#799` は root と `apps/public-viewer` で React version が二重化して dev overlay crash が起きるという報告だが、wiki 側の観測では current `main` clean install では非再現だった。したがって 2026-05-19 時点では、**即修正より「再発待ち or 再現条件の明確化」寄り** に読める。[[source-code]]より

### アルゴリズム・新機能系の open issue はあるが、9 月前の主戦場ではない

`#809` UMAP 並列化、`#679` 任意カテゴリー分類、`#648` レポート一括編集、`#641` 完了通知、`#638` 濃い意見ビュー改善などの enhancement も open だが、直近 issue 群と比べると **current default path の安定化** には直結しにくい。[[github-dev-docs]]より

## Open Questions

- `#838` の output validation を runtime feature にするのか、test helper に留めるのか
- `#833` のスコープを CSP / UUID / LocalLLM UX で分割すべきか

## Updates

- 2026-05-21: その後 GitHub 上では実際に分割が行われ、`#833` は admin create/reuse flow の UUID fallback へ縮小、CSP / remote asset policy は `#846`、LocalLLM auto-fetch UX は `#845` へ分離された
- 2026-05-21: さらに `PR #848` が merge されて `#846` は close、`#707` も current main 非再現として close された。したがって 2026-05-19 snapshot における P1 群のうち、active な残論点は `#845` `#716` `#818` `#820` `#681` 側へ移っている
- 2026-05-22: `PR #852` が merge され、`#716` も close された。したがってこの snapshot における P1 群の active 残論点は、主に `#818` `#820` `#681` 側へ寄っている。[[pr-852-error-log-visibility-observation-2026-05-22]]より
- `#707` `#681` `#473` を、provider / API 接続チェック統合の 1 本の問題として束ね直すべきか

## Updates

- 2026-05-19: 初版作成
