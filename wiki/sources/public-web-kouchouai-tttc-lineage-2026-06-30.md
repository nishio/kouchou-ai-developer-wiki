---
type: source
summary: "2026-06-30 の追加公開Web検索で確認した、Talk to the City から広聴AIへの系譜と、国内事例分類に使う公開根拠"
last_checked: 2026-06-30 19:39 JST
coverage: "public web search; DD2030 official page, public note articles, and already-filed critique source"
sources:
  - https://dd2030.org/kouchou-ai/
  - https://note.com/nishiohirokazu/n/nb37adf96fe50
  - https://note.com/annotakahiro24/n/nc571b40714b1
  - https://kensuzuki.hatenablog.com/2025/11/29/052230
  - public-web-broadlistening-japan-use-cases-2026-06-30.md
  - note-annotakahiro-broadlistening-resources-2025-02-05.md
  - kensuzuki-broad-listening-insight-types-2025-11-29.md
---

## What it is

2026-06-30 19:39 JST の追加公開Web検索で確認した、広聴AI / Talk to the City (TTTC) の系譜説明と、国内 broad listening 活用事例を分類する時の公開根拠メモ。

この source は新規事例の追加リストではない。[[public-web-broadlistening-japan-use-cases-2026-06-30]] と [[japan-broadlistening-use-case-map-2026-06-30]] に既に入っている事例群を、外部向けに説明する時の `tool_lineage` / `source_strength` / `scope` の根拠として使う。

## Findings

DD2030 公式の広聴AIページは、広聴AIを「Talk to the City の実用化」として説明し、起源を 2023 年の TTTC に置く。日本での前史として、2024 年の東京都知事選での TTTC 活用、日本テレビの衆院選報道での AI 意見分析、`シン東京2050` での使用を挙げ、その後、日本の自治体や政治家の実務に合わせた機能改善として広聴AIが開発され、2025-03-16 に OSS 公開されたと説明している。[[public-web-kouchouai-tttc-lineage-2026-06-30]]より

西尾 note「Talk to the City と広聴AIの歴史」は、DD2030 公式ページより開発者向けに細かい lineage を補う。TTTC の Scatter 実装を起点に、チームあんの側で非エンジニア向けの CSV upload / 管理画面 / 閲覧画面 / dense cluster / 階層 drill-down などを追加したため、単なる設定差分ではなく広聴AIとして分岐していった、という説明に使える。[[public-web-kouchouai-tttc-lineage-2026-06-30]]より

安野チーム公式 note「ブロードリスニングで〇〇してみたい！そのために必要なこと」は、2025-02 時点の TTTC 実践 guide として読める。TTTC 自体は OSS でも、データ収集費、分析環境の構築、運用費、LLM API cost が必要で、M-1 2024 分析のような単発事例でも API / X data acquisition の固定費が大きい。[[note-annotakahiro-broadlistening-resources-2025-02-05]]より

鈴木健ブログは、国内で「ブロードリスニング」が広がる一方で、実施そのものが広報目的化したり、end-to-end の政策反映まで届かないリスクを指摘している。また TTTC / 広聴AI型の散布図・クラスタ俯瞰は、主に大量意見から全体像や agenda candidate を見つける用途に向き、すべての insight type に向くわけではない。[[kensuzuki-broad-listening-insight-types-2025-11-29]]より

## Implication

国内事例ページでは、次の 4 つを同じ表で混ぜない。

| category | public explanation |
|---|---|
| TTTC direct / pre-kouchou lineage | 東京都知事選 2024、M-1、NTV 衆院選報道など。広聴AIそのものの導入実績とは分ける |
| kouchou-ai confirmed | DD2030 / 自治体 / public viewer / public artifact で広聴AIまたは kouchou-ai を確認できるもの |
| broad listening adjacent | 大阪府、いどばた系 platform、政党 AI、AI 支援住民対話など。広聴AI単体ではなく広義の実践として扱う |
| critique / scope guardrail | 事例数や可視化そのものではなく、どの insight type を得たいのか、政策反映までの end-to-end を見て評価する |

8/2 event material や #564 public case page では、DD2030 公式ページを「広聴AIの公開 lineage source」、西尾 note を「開発者向け lineage source」、鈴木健ブログを「万能視を避ける scope guardrail」として分けるのが安全である。

## Open Questions

- DD2030 website の case page に TTTC direct / pre-kouchou lineage を載せるなら、広聴AI confirmed case と同じ一覧に置くか、history / adjacent section に分けるか。
- 外部向けに西尾 note を lineage source として直接リンクするか、DD2030 公式ページを canonical にして note は開発者向け参考に留めるか。
- 鈴木健ブログの scope guardrail を、公開事例ページ本文に短く入れるか、docs / 技術資料側の「何を保証しないか」に送るか。

## Updates

- 2026-06-30 19:39 JST: 初回作成。追加公開Web検索で、DD2030 公式広聴AIページ、西尾 note、安野チーム公式 note、鈴木健ブログを、国内事例分類の lineage / scope guardrail として整理した。
