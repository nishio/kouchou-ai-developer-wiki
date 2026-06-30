---
type: analysis
summary: "2026-06-30 時点の広聴AI開発状況スナップショット。コード main、open PR / issue、議事録、Slack log の鮮度を合わせて読む"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
  - slack-logs-repository.md
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

Slack の広聴AI本体 channel は、直近14日では新しい実装論点が多くない。6/26 の Yokohama Hack! / 横浜型ブロードリスニング共有と、6/30 の Codex `/goal` 活用・速度制御方針が中心。アルゴリズム channel では embedding / Spherical K-means / Faiss K-means の話が出ているが、採用判断にはまだ GitHub issue / 実験設計への接続が必要。[[slack-logs-repository]]より

議事録 6/22 回は、8/2 イベントでブロードリスニングをどう出すか、Brand Compass、high priority issues、情報発信、運用ポリシーが主題。実装を急ぐより、現在の priority 軸と docs / wiki の入口を揃える作業が先に効く。[[meeting-minutes]]より

GitHub 現在地としては、PR #903 の docs inventory は小さく直せそうだが、user attention を使う review request / merge には踏み込まない。PR #891 は draft のままなので、今は状況把握対象。issue #898 は PR #899 merge 済みだが issue は open で、aarch64 実機確認または close 判断が残っている。

## Next

- PR #903 は、着手するなら assignee / owner を確認した上で CodeRabbit 指摘を小さく直す候補。
- issue #898 は、aarch64 Docker 実機確認ができるか、確認不能なら issue 上でどの状態まで close 可能かを整理する候補。
- docs / wiki 側は、`slack-logs` を Slack raw 一次 source として定着させ、議事録は `2026/06/29` 以降の見出しが入ったら再取得する。

## Open Questions

- `slack-logs` の `raw/` が 2026-05 以降を取り込んだ後、既存 `oss_weekly_reporter` 由来 source とどこまで置き換えるか。
- 8/2 イベント向けのブロードリスニング表示は、既存 viewer / docs のどの入口を最優先で整えるべきか。

## Updates

- 2026-06-30: 初回作成。`work/kouchou-ai` / GitHub open PR・issue / 議事録 export / `work/slack-logs` / `work/oss_weekly_reporter` の最新確認をまとめた。
