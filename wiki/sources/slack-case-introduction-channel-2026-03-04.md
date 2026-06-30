---
type: source
summary: "Slack #1_事例紹介_全体 の 2026-03/04 raw snapshot。公開事例候補の lead intake として有用だが、外部公開の根拠には primary URL 確認が必要"
last_checked: 2026-06-30
coverage: "work/slack-logs main@341cf80; raw/slack/C08LJ9T5MLY/2025-01〜2026-04; substantive rows were only in 2026-03/04; mirror 2026-06-16〜2026-06-30"
sources:
  - slack-logs-repository.md
  - https://maizuru2040.jp/wordpress/
  - https://maizuru2040.jp/kouchou-ai-reports/
  - https://maizuru2040.jp/kouchou-ai-reports/faq/
  - https://www.city.maizuru.kyoto.jp/shisei/0000014341.html
  - https://www.city.maizuru.kyoto.jp/shisei/cmsfiles/contents/0000014/14362/202510314.pdf
---

## What it is

Slack `#1_事例紹介_全体` (`C08LJ9T5MLY`) の `slack-logs` raw snapshot 確認メモ。Issue #564 の「活用事例を集めて公開する」に直結する channel だが、公開 wiki / 外部サイトに載せる根拠としては **Slack lead ではなく primary public URL を確認する** 必要がある。

この source は、Slack 発言の全文保存ではない。公開事例管理のために、lead の分類、鮮度、公開根拠への昇格条件だけを残す。

## Freshness marker

2026-06-30 に `work/slack-logs` を `main@341cf80` まで確認した時点の観測。`raw/slack/C08LJ9T5MLY/2025-01〜2026-04` のうち、substantive row があったのは 2026-03 と 2026-04 だけだった。2025-01〜2026-02 は各月 1 metadata row のみ、2026-03 は 3 text rows、2026-04 は 6 text rows。直近14日の `mirror/slack/C08LJ9T5MLY.jsonl.gz` も substantive message はなかった。[[slack-logs-repository]]より

## Observations

### Channel role

`#1_事例紹介_全体` は、公開可能な実績リストそのものではなく、事例 candidate を投げ込む lead intake として読むのが安全である。2026-03/04 の raw には、広聴AI / いどばたの地域 lead、広聴AIの confirmed case、隣接する AI assistant、政治家の broad listening 言及、他 channel への内部リンクが混ざっていた。[[slack-logs-repository]]より

したがって、#564 の公開事例ページへ移す時は、Slack channel から直接「実績」として転記せず、各 lead を次の分類へ落とす必要がある。

| classification | meaning |
|---|---|
| confirmed 広聴AI case | public page / viewer / official page で広聴AIまたは広聴AI成果物を確認できる |
| broad listening mention | ブロードリスニングの実施予定・意向・一般言及で、広聴AI利用とは限らない |
| adjacent civic AI | AI avatar / chatbot / いどばた的対話など、広聴AIとは別ツールだが近い実践 |
| internal pointer | Slack / Drive / 別 channel への参照。公開前に primary URL と許諾確認が必要 |

### Raw lead inventory

| month | lead | classification | public handling |
|---|---|---|---|
| 2026-03 | 北見での広聴AI・いどばたビジョンを使った「市民の声の可視化」体験会。北海道新聞 URL が共有されていた。 | broad listening / DD2030 tool lead | 新聞記事や主催者資料を primary source として確認するまで、外部公開の confirmed case にはしない。 |
| 2026-03 | 北見市議会議員選挙の当選 follow-up。 | political follow-up | ツール活用事例ではなく活動文脈の follow-up。public case list には入れない。 |
| 2026-04 | 舞鶴2040。特設サイト、広聴AI回答結果、市公式 project page が確認できる。 | confirmed 広聴AI case | public case / viewer demo 候補。市公式 project page と特設サイト / viewer / FAQ を分けて引用する。 |
| 2026-04 | 相模原市の生成AI avatar 実証。 | adjacent civic AI | 広聴AI / broad listening 事例ではない。周辺 civic AI lead として別管理。 |
| 2026-04 | 宮崎県知事選関連の broad listening 言及。 | broad listening mention | 実施予定・意向の言及として扱い、広聴AI利用とは断定しない。 |
| 2026-04 | 和歌山県のいどばた事例への Slack 内部リンク。 | internal pointer / idobata lead | public URL と公開可否を確認するまで public case list には入れない。 |

### 舞鶴2040 lead

2026-04 raw では、舞鶴市の `#みんなでつくる舞鶴2040` が広聴AI事例として共有されていた。Slack lead には特設サイトと舞鶴市公式資料への URL が含まれていた。[[slack-logs-repository]]より

公開確認では、次が確認できた。

- `https://maizuru2040.jp/wordpress/` は HTTP 200 で、本文に `広聴AIによる回答結果` への導線がある。
- `https://maizuru2040.jp/kouchou-ai-reports/` は public viewer として HTTP 200 を返し、`#みんなでつくる舞鶴2040` のレポート一覧を表示する。
- `https://maizuru2040.jp/kouchou-ai-reports/faq/` は、広聴AIが DD2030 の OSS 成果物であると説明している。
- 舞鶴市公式ページ `https://www.city.maizuru.kyoto.jp/shisei/0000014341.html` は、2040 年の舞鶴を考える project、特設サイト、意見募集、意見を新総合計画の参考にし特設サイトで公表する旨を確認できる。

舞鶴2040は、Slack lead から primary public source へ昇格できる case である。ただし、市公式ページ上では `広聴AI` という語を確認できなかったため、外部説明では「市公式 project page + 特設サイト / public viewer / FAQ で確認できる」と分けて書くのが安全である。

## Implication

#564 の事例管理では、`lead intake` と `public case list` を分ける必要がある。

- Slack channel: 事例候補を拾う場所。
- developer wiki source: lead の分類、primary URL 確認状況、公開リスクを記録する場所。
- 外部 public page: primary URL が確認でき、権利・文脈・責任所在の注意が書けるものだけを載せる場所。

この分離がないと、Slack で見つけた「近い話」まで広聴AIの導入実績として外に出してしまう。特に、AI assistant / いどばた / broad listening の意向表明 / 広聴AI viewer は読者にとって同じに見えやすいので、`tool lineage` と `source strength` を必須 field にするべきである。

## Open Questions

- `#1_事例紹介_全体` の 2026-05 以降に substantive row がないのは、channel 利用が少ないためか、backfill / export の制約か。
- 北見の体験会を public case へ昇格する場合、北海道新聞記事以外に、主催者資料や公開 viewer があるか。
- 宮崎の broad listening 言及は、実施済み case になったのか、意向表明で止まったのか。
- 事例 candidate は GitHub issue、Slack channel、Drive、website repo のどこを canonical intake にするか。
- 舞鶴2040を #564 の first public detailed case に昇格する場合、誰が実施主体・掲載許諾・スクリーンショット利用を確認するか。

## Updates

- 2026-06-30: 2025-01〜2026-04 raw を月別に確認し、substantive row は 2026-03/04 のみだったと追記。北見 / 舞鶴 / 相模原 / 宮崎 / 和歌山を lead inventory に分類した。
- 2026-06-30: 初回作成。`#1_事例紹介_全体` の 2026-04 raw を確認し、Slack lead intake と public case list を分ける必要を整理した。
