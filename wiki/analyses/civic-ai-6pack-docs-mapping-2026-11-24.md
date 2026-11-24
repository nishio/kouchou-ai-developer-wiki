---
title: "Civic AI（6-Pack of Care）と広聴AI docs の対応 2026-11-24"
type: analysis
summary: "Audrey Tang・Caroline Green の Civic AI（6-Pack of Care、civic.ai）の 6 観点で広聴AI の docs を点検した。元発言への遡りや少数意見への注意は厚く、公開後に止める・直す・異議を受ける手順と、同じ内容の大量投稿への注意が欠けていたので PR #1234 で埋めた。civic.ai 側に日本の broad listening 事例を届けるのは、docs が整ってからにする"
sources:
  - public-web-civic-ai-6pack-of-care-2026-11-24.md
  - role-model-papers-polis-birdwatch.md
  - kouchou-ai-docs-improvement-roadmap-2026-10-13.md
---

## 何を問うたか

広聴AI の docs と [Civic AI — 6-Pack of Care](https://civic.ai/) の間に関連を見出せるか。見出せるなら、それをどう活かすか。

civic.ai は、Audrey Tang と Caroline Green が Oxford の Institute for Ethics in AI で進めている研究プロジェクトの公開サイトで、Wiley から本（2027 年 2 月予定）が出る。「影響を受ける人々が確かめ、直し、止められる AI」を目標に、ケアの倫理（Fisher・Tronto）の 4 段階に 2 つを足した 6 つの観点（Pack）を示す。サイトは CC0。サイトの要約は [[public-web-civic-ai-6pack-of-care-2026-11-24]]。

読んだ範囲：civic.ai のトップと Pack 1〜6 の各ページ（2026-11-24 時点）。用語集・計測指標・FAQ は読んでいない。広聴AI 側は main `3649fe41` の docs。

## 結論

- **直接の言及は一方向にもない。** civic.ai には広聴AI・Talk to the City・チームみらい・安野の名前は出てこない。日本への言及は 2 か所だけで、Pack 2（規制当局が広告主の本人確認を検討したが実施されなかった）と Pack 3（台湾・カリフォルニアと並んで「市民インフラが整った土壌」なので、そこでの成果をそのまま他所に持ち込めない）。
- **観点は大きく重なる。** Pack 1 は道具として broad listening を名指しし、Polis と Community Notes を例に使う。これは広聴AI 論文の手本として置いている先行事例と同じである。[[role-model-papers-polis-birdwatch]]より
- **docs の点検枠として使うと、欠けている所が見える。** 下の対応表のとおり、遡れること・少数意見への注意・ローカルで完結できることは厚い。止める手段・直す手段・異議の受け方と、作られた世論（同じ内容の大量投稿）への注意が無かった。

## 対応表

| Pack | civic.ai の主張 | 広聴AI docs（点検前） | 判定 |
|---|---|---|---|
| 1 Attentiveness | 届いていない声に気づく。broad listening、Polis 型の bridging map、「Bridge first, decide second」 | 広聴AI そのもの。レポートの読み方の「濃い意見から少数派は抜け落ちる」警告 | 厚い。ただし bridging（投票から立場を超えた合意を探す）は広聴AI の機能ではない |
| 2 Responsibility | 導入ごとに範囲・義務・止め方・救済を公開で約束する（Engagement Contract） | 信頼性と責任のページの責任 3 レイヤー（OSS 開発者・運営者・発行者） | 誰の責任かはある。止め方と救済が無い |
| 3 Competence | 判断の痕跡、説明できること、他所の成功をそのまま持ち込まない | トレーサビリティ（`relations.csv`、原文不改変、出典リンク）、「モデルやプロンプトを変えた数字は比べない」 | 厚い |
| 4 Responsiveness | 影響を受けた人が異議を出し、実際に直させられる。作られた世論への警告（支援団体のプラットフォーム経由で届いた 2 万件超の反対コメントの例） | トップと README に「多数派攻撃に対する防御機能（予定）」のみ | 無い。異議・修復の道も、大量投稿の現状説明も無い |
| 5 Solidarity | 持ち出せる・乗り換えられる・連合できる | AGPL、セルフホスト、CSV／JSON の書き出し | 理念は合うが docs はこの観点で書いていない |
| 6 Symbiosis | 地域で動くオープンウェイトのモデル、「data as soil, not oil」 | 導入ガイドの「手元（組織内）だけで完結」「ローカル LLM」 | 厚い |

## やったこと：欠けている所を docs に足した

PR [#1234](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1234)（2026-11-24 作成、未 merge）。

- **公開した後に、止める・直す・異議を受ける**（Pack 2・4）：公開前に決める 3 点（何に使うか・どこに言えばよいか・言われたら何をするか）、公開設定の 3 区分、削除してもサーバーにファイルが残ること、外に出た静的 HTML は取り消せないこと、入力を直すときは作り直すこと、直した記録を調査概要に残すこと
- **同じ内容の大量投稿への注意**（Pack 4）：件数は投稿の数で人数ではない、同じ文面は散布図で重なり「濃い意見」に出やすい、公開前に重複を数えて調査概要に書く。機能としては [#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345)・[#1156](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1156) で検討中
- できること・できないことの表に「合意点探しは投票型ツールの役割」「件数を人数として扱えない」を追加（Pack 1・4）
- FAQ に「自分の投稿が違う意味で取り出されている・取り下げたい」
- トップと README の「多数派攻撃に対する防御機能（予定）」を「検討中（[#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345)）」に

書いた挙動はコードと照合した。管理画面の削除は status を `deleted` にするだけでファイルは消さない（`mark_report_deleted`）。非公開は公開 API で 404、限定公開は一覧に出ない。再利用の画面には入力を差し替える欄がない。調査概要（`intro`）は公開レポートに表示され、「レポート名編集」から後で書き換えられる。

## 次に見るもの

- **civic.ai に日本の事例を届ける（Pack 3 の問いへの材料）**は、docs が整ってからにする。外部との関わりが生じるので、まず広聴AI 側の docs を充実させる、が nishio の判断（2026-11-24）
- Pack 5（持ち出し・乗り換え）は、書き出し形式と結果 JSON の契約（層分離の取り組み）が固まってから、docs に観点として書けるか見る
- 大量投稿が実際に「濃い意見」の上位に出るかは、コード上の推論で実データ未確認。[#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345) の実験データで確かめられる

## Open Questions

- 異議を受けてから直すまでの期間（Pack 4 は 24 時間・7 日・30 日を提案している）を、docs で目安として示すか、発行者に任せるか
- 「濃い意見」が大量投稿を目立たせうることは、機能の名前や画面の説明にも反映すべきか

## Updates

- 2026-11-24 にドキュメントのビルドが通り、PR [#1234](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1234) を `main`（`0db5f614`）にマージした。大量投稿への機能面の対応は [#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345) で追跡する。
