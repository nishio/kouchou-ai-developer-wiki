---
type: source
summary: "2026-06-30 の Slack `#2_開発_広聴ai` で共有された Codex `/goal` 運用メモ。長い goal は人間が追える速度に制御し、まず状況把握・LLM Wiki・docs 更新を中心に走らせる"
last_read: 2026-06-30 16:59 JST
coverage: "work/slack-logs main@341cf80, mirror window 2026-06-16T04:12:50Z〜2026-06-30T04:12:50Z, channel C08F7JZPD63 (#2_開発_広聴ai), 2026-06-30 12:56/13:03 JST の2件"
sources:
  - slack-logs-repository.md
---

## What it is

2026-06-30 の Slack `#2_開発_広聴ai` で、Codex `/goal` を広聴AIに使う案と、その速度制御方針が共有された。`digitaldemocracy2030/slack-logs` の `mirror/slack/C08F7JZPD63.jsonl.gz` を `work/slack-logs main@341cf80` で読んだ観測である。[[slack-logs-repository]]より

この source は raw 発言の全文保存ではなく、AI エージェント運用として再利用できる判断だけを残す。

## Observation

2026-06-30 12:56 JST に、Codex の `/goal` が有用なので広聴AIにも走らせる案が共有された。続く 13:03 JST には、全力で走らせると人間が追いつけなくなるため、まずは状況把握、LLM Wiki、docs 更新を中心にする方針が共有された。[[slack-logs-repository]]より

この判断は、単に「コード変更を控える」という意味ではない。広い goal を持つエージェントは、過去議論・issue・Slack・議事録を読み、現状を分かる単位へ分解し、wiki / docs / meeting draft に還流してから、次の本体 PR 候補を人間が選べるようにする、という運用である。

## Implication

Codex `/goal` のような persistent goal は、単発タスクよりも速く大量の action を生みやすい。広聴AIのように issue / Slack / meeting minutes / docs / code が散らばる project では、最初の価値は「実装を量産すること」よりも、source freshness を揃え、未決論点を整理し、次に人間が判断する場所を作ることにある。

したがって、長い goal の初期運用は次が安全である。

- repo / source を pull して freshness marker を更新する。
- Slack / 議事録 / issue / current main を同じ snapshot として読む。
- 実装ではなく wiki source / analysis / concept / meeting draft を先に更新する。
- GitHub 上で人間 attention を使う reviewer request / 催促 / escalation は避ける。
- 本体 code PR に進む場合は、`thinking-targets` や `meeting-report-draft` に候補を出し、人間が次の slice を選べる状態にする。

## Open Questions

- Codex `/goal` を長時間走らせる時、どの頻度で人間向け status を出すか。
- wiki / docs 更新中心から本体 PR へ移る trigger は、定例合意、issue assignee、明示指示のどれに置くか。
- goal が広すぎる時、`thinking-targets` に候補を足すだけでよいか、goal ごとの runbook を作るべきか。

## Updates

- 2026-06-30: 初回作成。Slack `#2_開発_広聴ai` の Codex `/goal` 共有を、長い goal の速度制御と wiki/docs-first 運用として固定した。
