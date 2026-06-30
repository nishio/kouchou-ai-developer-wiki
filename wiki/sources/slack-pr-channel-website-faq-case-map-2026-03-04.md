---
type: source
summary: "Slack #2_広報_pr の 2026-03/04 raw snapshot。website FAQ、導入事例マップ、事例掲載 intake、ユーザー会の議論を #564 public case page へ接続する"
last_checked: 2026-06-30
coverage: "work/slack-logs main@341cf80; raw/slack/C08K4CUB12T/2025-01〜2026-04; substantive rows were in 2026-03/04; mirror 2026-06-16〜2026-06-30 は substantive message なし; website PR #192 は 2026-06-19 merged"
sources:
  - slack-logs-repository.md
  - https://github.com/digitaldemocracy2030/website/pull/192
---

## What it is

Slack `#2_広報_pr` (`C08K4CUB12T`) の `slack-logs` raw snapshot 確認メモ。#564 の public case page は kouchou-ai 本体 issue だけでなく、DD2030 website の情報設計・広報導線とも接続するため、この channel の 2026-03/04 議論を source 化した。

この source は、Slack 発言の全文保存ではない。公開事例ページの設計に再利用できる論点だけを抽出する。

## Freshness marker

2026-06-30 に `work/slack-logs` を `main@341cf80` まで確認した時点の観測。`raw/slack/C08K4CUB12T/2025-01〜2026-04` のうち substantive row があったのは 2026-03 と 2026-04 で、2026-03 は 16 rows、2026-04 は 9 rows。直近14日の `mirror/slack/C08K4CUB12T.jsonl.gz` は metadata のみで substantive message はなかった。[[slack-logs-repository]]より

関連する website PR #192 は 2026-06-19 に merge 済み。PR title は政治的中立性 FAQ の追加で、merge 時 comment では Slack にあったカテゴリ分け案は別 issue で考える、とされていた。

## Observations

### FAQ は読者別に分ける必要がある

2026-03/04 の `#2_広報_pr` では、website FAQ の追加 PR をめぐって、メンバー向け QA と外向け QA が混ざっていること、これから参加を検討している人と既に参加している人では必要な FAQ が違うことが議論された。[[slack-logs-repository]]より

最終的に website PR #192 は 2026-06-19 に merge されたが、カテゴリ分け案は別 issue で考える扱いになった。したがって、#564 の public case page に FAQ を置く場合も、単一の FAQ 一覧ではなく、少なくとも `導入検討者向け` / `既に関わっている人向け` / `レポート閲覧者向け` を分ける方が自然である。

### 事例マップは「見せる」だけでなく「集めたい」を伝える導線

2026-04 の `#2_広報_pr` では、DD2030 から見えないところで活用が進むケースにどう気づくか、HP に導入事例マップを載せる案、掲載 OK の確認、公開情報をもとに掲載すること、積極的に掲載してほしいという声を受けられるようにすることが議論された。[[slack-logs-repository]]より

これは #564 の public case page を、既存実績の陳列だけでなく **case intake surface** として設計すべきことを示す。外部ページには、確認済み事例一覧とは別に、`掲載候補を教えてください` / `実施主体・公開 URL・掲載可否を確認します` のような intake 導線を置く余地がある。

### ユーザー会は事例リストの次段

同じ 2026-04 議論では、他自治体がどう使っているかを知りたいので、ユーザー会のようなものがあるとよい、という発想も出ていた。[[slack-logs-repository]]より

これは #564 の初回 page scope には入れすぎない方がよいが、事例ページの次段としては重要である。公開事例ページは、単に広報するページではなく、実践者同士が「どう集めたか」「どう公開したか」「何に困ったか」を比較する入口になり得る。

## Implication

#564 の public case page は、次の 3 つを分けると整理しやすい。

| layer | role |
|---|---|
| confirmed public cases | primary URL と source strength を確認した事例だけを載せる |
| case intake | Slack / Drive / 人づての候補を、公開 URL・掲載可否・実施主体確認へ流す |
| FAQ / reading guide | 導入検討者、既存参加者、レポート閲覧者で質問を分ける |

この分離がないと、Slack lead をそのまま実績として載せるリスクと、FAQ が誰向けか分からないリスクが同時に出る。[[slack-case-introduction-channel-2026-03-04]]より

## Open Questions

- website PR #192 の merge 後、FAQ のカテゴリ分けをどの repo / issue で追うか。
- #564 の public case page に `掲載候補を教えてください` 導線を置く場合、誰が intake を確認し、primary URL / 許諾 / source strength を判定するか。
- 事例マップは public page の一部にするか、まずは developer wiki / internal list で候補管理してから外に出すか。
- ユーザー会は #564 の scope 外に置くか、事例ページの future section として軽く触れるか。

## Updates

- 2026-06-30: 初回作成。`#2_広報_pr` の 2026-03/04 raw と website PR #192 live state を確認し、FAQ の読者分離、導入事例マップ、case intake、ユーザー会を #564 public case page の情報設計へ接続した。
