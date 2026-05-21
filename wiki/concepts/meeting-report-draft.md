---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。直近の実装・調査・運用判断を短く積み上げる"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業報告を短時間で共有するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「完全な changelog」を作ることではなく、**会議で口頭共有すべき判断と進捗だけを残す** こと。詳細な根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連ページへ送る

## 次回定例向け下書き

### 1. analysis-core の package/CLI 整理を main へ反映

- `Task 2.5.6` 相当の optional dependency 分離を `PR #843` で main へ反映。`torch` / `sklearn` 系を extras に逃がし、base install で重い依存を必須にしない形へ寄せた。[[analysis-core-extras-pr-scope]]より
- 続けて `PR #844` で `analysis-core` CLI の preflight validation と filesystem-based quickstart を入れ、`#836` と `#837` を close した。`main` では CLI 利用者の初回つまずきを減らす方向が一段進んだ。[[refactoring-status]]より

### 2. Web の public-IP HTTP 問題を issue 分割で片付けた

- もともと `#685` に混ざっていた論点を分割し、UUID fallback は `#833 -> PR #847`、CSP / remote asset policy は `#846 -> PR #848/#849`、LocalLLM auto-fetch UX は `#845 -> PR #850` として個別に main へ入れた。[[issue-priority-through-2026-09]]より
- これで「違う性質の問題を 1 issue に詰めたまま進める」状態を解消した。今後は umbrella issue より、review 可能な slice へ分ける方針を取りやすい。[[open-decisions]]より

### 3. production deploy 失敗を調査し、Docker build context 漏れを修正

- `#848` 以降の `Azure Deployment` が `Cannot find module '../shared/csp'` で落ちていた。原因は `apps/admin` / `apps/public-viewer` の `next.config.ts` が `apps/shared/csp` を参照する一方、Docker build で `apps/shared` を copy していなかったこと。[[deployment]]より
- `PR #851` で両 Dockerfile に `apps/shared` の copy を追加して修正し、production deploy の元の failure pattern を解消した。会議では「CSP 共通化自体」ではなく「Docker build context の見落とし」が障害原因だったと共有すると分かりやすい。[[source-code]]より

### 4. AI エージェント運用ルールを明文化した

- reviewer request / approval 催促 / admin merge のような「人間 attention を使う操作」は、AI が独断で行わず、明示指示がある時だけ実行するルールを wiki と `CLAUDE.md` に追記した。[[coding-agents]]より [[contributing]]より
- さらに、Issue 実装前に assignee の有無を確認し、着手するなら self-assign してから進めるルールも追加した。並行開発の衝突防止が目的。[[coding-agents]]より

## Open Questions

- このページを「常に次回会議向け 1 枚」に保つか、会議ごとに snapshot を切るかはまだ未決
- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-05-21: 初回作成。直近の `analysis-core` / Web UI / deploy / AI 運用ルールの進捗を次回定例向けに要約
