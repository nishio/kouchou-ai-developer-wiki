---
title: "コード・Wiki・Issue の健全性レビュー 2026-10-18"
type: analysis
summary: "main 083593ba のコード健全性調査（新規の改善点と 5 PR）、wiki の事実照合、open Issue 90 件のトリアージをまとめた 2026-10-18 の棚卸し"
sources:
  - source-code.md
  - source-review-findings-2026-10-16.md
  - issue-backlog-audit-2026-10-12.md
  - meeting-minutes.md
---

## 位置づけ

nishio「ソースコードと Wiki を読んで物事を把握して、改善すべきことがないか考えて」→「やると良いと思う順番で進めて」を受けた棚卸し。観測時点は kouchou-ai main `083593ba`（2026-10-17 の #1022 merge 後）、open Issue 90 件・open PR 2 件（#1024 / #1025）。[[source-review-findings-2026-10-16]] で確定・修正済みの 10 件（#1015–#1022 と #1023）は対象外。調査は 3 並列（コード健全性 / wiki と main の照合 / Issue トリアージ）で行い、コードの指摘は PR 化の前に手元で再確認した。[[source-code]]より

## コード: PR 化したもの（2026-10-18・全件未 merge）

| PR | 内容 | 確認 |
|---|---|---|
| [#1027](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1027) | プラグイン取込の `fileName` とスプレッドシート取得の `file_name` を `validate_slug` で検証（パストラバーサル。#1020 と同種）、`SLUG_PATTERN` を `fullmatch` に | api 348 passed |
| [#1028](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1028) | async エンドポイント内の同期 I/O（接続確認の LLM 呼び出し、スプレッドシート取得、revalidate）を `run_in_threadpool` に。`requests.get` に timeout | api 338 passed |
| [#1029](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1029) | `cluster_nums[-1]` を sort 前に取っていたため降順指定で最大階層が消える問題。正規化（昇順・重複除去・意見数で clamp・非破壊）してから使う | analysis-core 342 passed |
| [#1030](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1030) | `hierarchical_aggregation` が例外を握りつぶし、失敗しても run が成功・report が ready になる問題。re-raise に | analysis-core 335 passed |
| [#1031](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1031) | 編集後の aggregation-only 実行でトークン数・推定コストが 0 に戻る問題。スキップしたステップ分を前回 status から引き継ぐ | analysis-core 336 passed |

PR の作成は subagent に worktree で実装させ、diff の確認・テスト再実行・push / PR 作成は親セッションで行った（[[source-review-findings-2026-10-16]] と同じ運用）。

## コード: 未着手の backlog

- **編集後の集計が投げっぱなし**（M）: `execute_aggregation` は起動しただけで成功を返す。完了前に cache invalidate する、5 分以内の 2 回目の編集が lock で失敗して status を error にしうる、集計失敗で READY のレポートが error になり公開側から消える。#1030 で失敗が表に出るようになったので、aggregation-only の失敗を report status と分けて扱うかどうかの設計判断が要る
- **再現性**: UMAP / KMeans / ラベル用サンプリングに seed が無い。UMAP は `random_state` を固定すると並列化が効かなくなるので、#513 / #809 の方針判断とセット
- **llm_grouping の割り当て欠落**: 割り当ての無い意見が警告なしで先頭グループに入る（指定カテゴリを使わないモード）
- **extraction の comment-id 重複**: 同じ id の行があると前の行が黙って消える
- **Gemini chat の 5xx**: 一時的な 503 を再試行せずパイプライン全体が止まる（SDK 既定の再試行の有無は要確認）
- **CI**: admin の build / jest が `packages/report-schema` の変更で起動しない。analysis-core / server の CI が `specs/*.json` の変更で起動しない。static-site-builder には CI が無い
- **static-site-builder**: 同時ビルドが同じ出力ディレクトリを共有する
- **小さめのもの**: `REVALIDATE_SECRET` 未設定時の比較、`/test-error` の残置、`validate_path_within_report_dir` の文字列 startswith 判定、root の古いファイル（`PLAN_llm_grouping_capabilities.md` / `test-plan-admin-interface.md` / `tests/seed.spec.ts`）、report-schema の `ReportStatus` と Python 側のずれ
- API schema での `cluster`（正の整数・昇順）と `workers >= 1` の検証（#1029 の対象外）

## Wiki: 照合して直したもの

- 公開境界: 未修正の Dependabot alert のパッケージ名を除去（[[dependabot-alerts-2026-10-14]] / [[gotchas]] / [[meeting-report-draft]] / log）。デモ環境のキー構成の記述を抽象化（[[deployment]]）
- 事実の古さ: static-site-builder は Next.js ではなく Express 5（[[architecture-overview]] / [[kouchou-ai]]）、パイプラインは既定 9 ステップ（`opinion_classification` を含む）と `llm_grouping` モード 6 ステップ（[[pipeline]]）、Biome CI は導入済み・workflow は 22 本・analysis-core は rye ではなく素の pytest（[[testing]]）、起動時 build は 2026-06-01 に廃止済み（[[deployment]]）、docs rename 後のパス（[[cli]] / [[local-dev-setup]]）など
- [[meeting-report-draft]] を [[meeting-report-2026-10-18]] へ rotate（47KB → 進行中だけ）

## Wiki: 残っている構造課題

- concept ページの本文に「#NNN 未 merge」のような日付つきの現在形を書くと古くなる。concept 本文は構造・手順に限り、現在の状態は analysis か `## Updates` に置く運用にすると再発しにくい
- Windows 配布・セットアップ（約 30 ページ）に hub となる concept が無い。次点は公開事例・trust layer、ブラウザ版（#921）
- 後続版があるのに `status: superseded` の目印が無い snapshot が多い（daily-report / issue-audit / open-pr 系など）
- 本体 `docs/testing.md` も workflow 5 本・rye 前提のままで実態とずれている（upstream docs PR 候補）

## Issue: トリアージ結果（提案のみ。GitHub 上の操作は未実施）

- **close 候補**: [#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285)（プロバイダ追加は実装済み。実モデル検証は #912 / #913 / #991 へ）、[#994](https://github.com/digitaldemocracy2030/kouchou-ai/issues/994)（実 LLM での完走確認後）、[#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809) → #513 統合、[#679](https://github.com/digitaldemocracy2030/kouchou-ai/issues/679) → #997 統合、[#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898)（aarch64 実機確認後）
- **前回監査の訂正**: [#507](https://github.com/digitaldemocracy2030/kouchou-ai/issues/507) の削除条件（v3.0）は v3.0.0 以降のタグで既に満たしている（[[issue-backlog-audit-2026-10-12]] は package.json の 0.1.0 を見て未到達と判定していた）
- **次に着手しやすいもの**: [#954](https://github.com/digitaldemocracy2030/kouchou-ai/issues/954)（CLI の report.html で原文リンク・タイトル設定が効かない）、[#213](https://github.com/digitaldemocracy2030/kouchou-ai/issues/213)（good first issue）、[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79) / #11（作成前の費用・時間の目安）、[#974](https://github.com/digitaldemocracy2030/kouchou-ai/issues/974)（Docker Hub 429 の横展開）、[#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121)（縦長画面の散布図）
- **人間判断**: 60 日超・担当なしの 46 件のうち not planned 候補（#173 #346 #516 #517 #529 #576 #641 #342 #339）、2025 年から止まっている assignee（#280 #310 #324 #337 #454 #547 #643）の再確認

## Open Questions

- #1031 の「合計」を、現在の成果物を作ったステップのコストとするか、再実行を含む累積支出とするか

## Updates

- 2026-10-19: 範囲と検証を深くした本格レビューを実施し、修正 PR #1032–#1041 を作成。記録は [[deep-code-review-2026-10-19]]
