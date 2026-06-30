---
type: analysis
summary: "2026-06-30 時点の広聴AI開発状況スナップショット。コード main、open PR / issue、議事録、Slack log の鮮度を合わせて読む"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
  - slack-logs-repository.md
  - windows-setup-guide-outline-2026-06-30.md
  - issue-876-developer-docs-gap-audit-2026-06-30.md
  - pr-903-review-comment-draft-2026-06-30.md
  - slack-algorithm-kmeans-2026-06-29.md
  - spherical-kmeans-experiment-scope-2026-06-30.md
  - github-issue-876-live-2026-06-30.md
  - issue-876-docs-pr-slice-2026-06-30.md
---

## Snapshot

2026-06-30 時点では、広聴AI本体の `main` は `d5c9ece` (PR #899 merge) で止まっており、`work/kouchou-ai/` は `git pull --ff-only` 済み。open PR は 2 本で、nishio authored の open PR は 0 本だった。[[source-code]]より

- PR #903: `docs: Web UI の Node runtime 依存インベントリを追加 (#885)`。非 draft、review required、merge state blocked。CodeRabbit は static-site-builder の dev entrypoint、last verified note、Server Actions count mapping の指摘を出している。
- PR #891: `feat(packaging): Windows スタンドアロン（embeddable Python + 静的 viewer）`。tokoroten authored、draft、review required。
- open issue は 123 件。nishio assigned は #898, #876, #519, #370, #255, #11 の 6 件。

## Source Freshness

議事録は 2026-06-30 に Google Doc export を再取得し、先頭見出しは `2026/06/22`。`2026/06/29` 見出しはまだ export 内に見当たらない。txt は 7702 行、HTML URL 棚卸しは unique 551 件。[[meeting-minutes]]より

Slack log は `digitaldemocracy2030/slack-logs` を `work/slack-logs/` に clone / pull し、`main@341cf80` / `synced_at=2026-06-30T04:12:50Z` / window `2026-06-16〜06-30` まで確認した。[[slack-logs-repository]]より

`oss_weekly_reporter` は `data@e2c9b20` まで fast-forward 済みで、weekly dump は `2026-06-17_to_2026-06-24` まである。今後の Slack raw 一次確認は `slack-logs`、週次 AI 要約や GitHub activity とのセット確認は `oss_weekly_reporter` という使い分けが妥当。

## Reading

Slack の広聴AI本体 channel は、直近14日では新しい実装論点が多くない。6/26 の Yokohama Hack! / 横浜型ブロードリスニング共有と、6/30 の Codex `/goal` 活用・速度制御方針が中心。アルゴリズム channel では 6/29 に embedding / Spherical K-means / Faiss K-means の話が出ており、[[slack-algorithm-kmeans-2026-06-29]] と [[spherical-kmeans-experiment-scope-2026-06-30]] に固定した。採用判断ではなく、clustering space / objective / backend を分けた clean experiment 候補として扱うのが妥当。[[slack-logs-repository]]より

議事録 6/22 回は、8/2 イベントでブロードリスニングをどう出すか、Brand Compass、high priority issues、情報発信、運用ポリシーが主題。実装を急ぐより、現在の priority 軸と docs / wiki の入口を揃える作業が先に効く。[[meeting-minutes]]より

GitHub 現在地としては、PR #903 の docs inventory は小さく直せそうだが、user attention を使う review request / merge には踏み込まない。PR #891 は draft のままなので、今は状況把握対象。issue #898 は PR #899 merge 済みだが issue は open で、aarch64 実機確認または close 判断が残っている。

## Next

- docs 系 issue / PR の横断地図は [[docs-issue-map-2026-06-30]] に固定した。#876 / #877 / #885 / #903 は同じ docs 群でも読者像・Windows supported path・Node runtime 技術前提を分けて扱う。
- #876 は [[issue-876-developer-docs-gap-audit-2026-06-30]] で current main と草案の差分を確認し、[[issue-876-docs-pr-slice-2026-06-30]] に次の本体 docs PR の file-by-file first slice を固定した。`docs/development/developer-quickstart.md` 単体追加ではなく、README / docs index / quickstart / mkdocs nav の役割を同時に下げる方針。[[source-code]]より
- #877 の Windows setup guide は、[[windows-setup-guide-outline-2026-06-30]] に docs PR 化前の具体アウトラインを固定した。current main の `docs/getting-started/windows-setup.md` は `setup_win.ps1` 導線まで反映済みだが、API key 前提と対象外環境の切り分けがまだ弱い。[[source-code]]より
- PR #903 は、[[pr-903-node-runtime-doc-review-2026-06-30]] に docs 精度のレビュー観点を固定し、[[pr-903-review-comment-draft-2026-06-30]] に投稿前コメント案を置いた。AI からはまだ GitHub へ投稿していない。
- issue #898 は、[[issue-898-close-readiness-2026-06-30]] に close 判定条件を固定した。aarch64 Docker 実機確認ができるか、確認不能なら issue 上で pending validation とする。
- 6/29 Slack の Spherical K-means / Faiss K-means は、[[spherical-kmeans-experiment-scope-2026-06-30]] に実験 scope として切り出した。最初の clean experiment は、current main baseline から 2D UMAP と clustering 用 15D〜25D UMAP を比較するところが最も因果を読みやすい。
- docs / wiki 側は、`slack-logs` を Slack raw 一次 source として定着させ、議事録は `2026/06/29` 以降の見出しが入ったら再取得する。

## Open Questions

- `slack-logs` の `raw/` が 2026-05 以降を取り込んだ後、既存 `oss_weekly_reporter` 由来 source とどこまで置き換えるか。
- 8/2 イベント向けのブロードリスニング表示は、既存 viewer / docs のどの入口を最優先で整えるべきか。

## Updates

- 2026-06-30: 6/29 Slack の Spherical K-means / Faiss K-means 言及を [[slack-algorithm-kmeans-2026-06-29]] / [[spherical-kmeans-experiment-scope-2026-06-30]] に切り出し、採用判断ではなく clean experiment 候補として接続。
- 2026-06-30: issue #876 live state を [[github-issue-876-live-2026-06-30]] に固定し、[[issue-876-docs-pr-slice-2026-06-30]] で developer docs PR の file-by-file first slice を整理。
- 2026-06-30: PR #903 docs inventory のレビュー観点と issue #898 close readiness へのリンクを追加。
- 2026-06-30: docs 系 issue / PR の横断地図として [[docs-issue-map-2026-06-30]] を追加。
- 2026-06-30: #877 の Windows setup guide を本体 docs PR に落とすための具体アウトラインとして [[windows-setup-guide-outline-2026-06-30]] を追加。
- 2026-06-30: #876 developer quickstart / docs entry の gap audit として [[issue-876-developer-docs-gap-audit-2026-06-30]] を追加。
- 2026-06-30: PR #903 の投稿前レビューコメント案として [[pr-903-review-comment-draft-2026-06-30]] を追加。
- 2026-06-30: 初回作成。`work/kouchou-ai` / GitHub open PR・issue / 議事録 export / `work/slack-logs` / `work/oss_weekly_reporter` の最新確認をまとめた。
