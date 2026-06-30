---
type: source
summary: "2026-06-23〜06-30 の Slack で出た Devin / AI agent 運用メモ。使ってよい範囲・費用上限・繰り返し Web 更新候補は、Slack 記憶ではなく明文化された運用契約に落とす必要がある"
last_read: 2026-06-30 19:23 JST
coverage: "work/slack-logs main@7c17dd3, mirror synced_at=2026-06-30T09:54:03Z, window=2026-06-16T09:54:03Z〜2026-06-30T09:54:03Z; C08FL58M3D3 (#7_雑談), C08PRQVQWSE (#8_devinと人間たちの部屋), C08FF5MM59C (#2_開発_いどばた), C08F7JZPD63 (#2_開発_広聴ai)"
sources:
  - slack-logs-repository.md
  - slack-codex-goal-speed-control-2026-06-30.md
---

## What it is

2026-06-23〜06-30 の Slack mirror には、Codex `/goal` の速度制御とは別に、Devin / AI agent をどう使うかという運用論点が出ている。`work/slack-logs main@7c17dd3` の `mirror/` を 2026-06-30 19:23 JST に読んだ観測である。[[slack-logs-repository]]より

この source は、Slack 発言の全文保存ではなく、AI agent 運用として再利用できる判断だけを残す。発言者名そのものは判断に不要なので、channel / 日付 / 論点に落とす。

## Observation

`#7_雑談` では 2026-06-23〜06-25 に、Devin を今後も使ってよいのか、使ってよいなら用途と費用上限を明文化したい、という話が出ている。Slack 上では、過去に上限や負担元が口頭・Slack 記憶として共有されていたが、正式な docs として探せる状態ではない、という問題設定になっている。[[slack-logs-repository]]より

同じ流れで、Devin は GitHub repository と連携して使うため、どの project / repository の開発に使うのかを一度まとめるとよい、という整理も出ている。また、残っている credit をただ消費するより、「こういう使い方は有益だった」という事例を蓄積する方がよい、という方向で議論されている。[[slack-logs-repository]]より

具体的な候補として、毎週の議事録を見て Web サイトを更新するような繰り返しタスクを AI agent に任せると、Web サイトを活発に保てるかもしれない、という案が出ている。これは [[wiki-driven-workflow]] と相性がよい一方、source freshness、公衆向けに書いてよい境界、最終 review owner を先に決めないと、外部公開面で人間と衝突しやすい。[[slack-logs-repository]]より

`#8_devinと人間たちの部屋` では 2026-06-30 に、Devin が repository の構成整理 PR を作り、CI / build / dev server 起動確認まで報告した一方で、merge や billing / token 残量確認は bot 単独では扱えず、人間に返している。この観測は、AI agent が PR 作成・検証までは進められても、merge / billing / owner attention は人間側の操作として残る、という既存ルールを補強する。[[slack-logs-repository]]より

## Implication

Devin / Codex / Claude Code の共通ルールとして、「何をやらせるか」だけでなく、**どの人間の判断を消費する操作か**を分ける必要がある。

- AI agent に向く: issue / PR / Slack / 議事録を読み、source freshness を揃え、docs / wiki / draft を更新する。bounded な repository 内 refactor や、検証コマンドの実行結果整理も向く。
- 人間契約が必要: 費用上限、利用対象 repository、招待 / 権限、billing / token 残量、merge、review request、外部公開文面の最終判断。
- 繰り返し Web 更新を agent 化するなら、議事録 export → public boundary scrub → website diff → human review という contract を先に作る。単に「毎週更新して」と投げると、公開してよい内容・古い source・掲載許諾の境界で事故りやすい。

このため、Codex `/goal` の wiki/docs-first 運用と Devin の繰り返しタスク候補は同じ方向を向いている。まず wiki に source / judgement / public boundary を固定し、その後に website や docs の小さな PR へ切るのが、人間が追える速度を保ちやすい。[[slack-codex-goal-speed-control-2026-06-30]]より

## Open Questions

- Devin の利用対象 repository / 用途 / 費用上限をどこに明文化するか。Slack 記憶ではなく、DD2030 側の運用 docs として持つ必要がある。
- 毎週の議事録から Web サイトを更新する task は、DD2030 website、kouchou-ai docs、developer-wiki のどれを正本にするか。
- agent が作った public website diff の review owner は誰か。掲載許諾や外部向け表現は、AI が単独で確定しない方がよい。

## Updates

- 2026-06-30: 初回作成。`work/slack-logs main@7c17dd3` の 2026-06-23〜06-30 mirror から、Devin / AI agent 運用、費用・用途の明文化、議事録からの繰り返し Web 更新候補を整理。
