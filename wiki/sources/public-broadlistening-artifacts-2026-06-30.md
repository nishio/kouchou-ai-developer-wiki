---
type: source
summary: "8/2 イベント向けの公開事例候補として、2026-06-30 に確認した public viewer / official page / public article の棚卸し"
last_checked: 2026-06-30
coverage: "奈良 #全員市長 public viewer、渋谷区 official page / PDF、八代市 Democracy-X public article / viewer"
sources:
  - https://everyonemayor.github.io/kouchou-ai/2025-7-13/
  - https://www.city.shibuya.tokyo.jp/kusei/kocho/questionnaire/kuminishikichosa_ai.html
  - https://files.city.shibuya.tokyo.jp/assets/12995aba8b194961be709ba879857f70/38d509b421d049c4ad53536fc88ae4ca/kuminishikichosa_ai.pdf
  - https://democracy-x.org/news/yatsushiro-kouchouai-202508/
  - https://democracy-x.github.io/kouchou-ai-yatsushiro/47ae7bf4-e5de-4dbd-82ab-520160f373d6/
  - meeting-minutes.md
  - broad-listening-book-source.md
  - broad-listening-book-extractions.md
---

## What it is

8/2 イベントで「ブロードリスニングの技術 / ツール」を説明する時に、公開境界を守って見せられそうな外部 artifact の確認メモ。実環境 URL、resource 名、revision、ログ、secret / access 周辺の情報は扱わず、すでに公開されているページとレポートだけを対象にする。

この source は、公開可否の最終承認ではない。イベント直前には URL の再確認、スクリーンショット利用可否、政治・選挙文脈での話し方を人間側で確認する必要がある。

## Freshness marker

2026-06-30 に公開 URL を確認した時点の観測。上記 5 URL はいずれも HTTP 200 を返した。議事録 source は 2026-06-30 に Google Doc export を再取得済みで、先頭見出しは `2026/06/22`、txt は 7703 行だった。[[meeting-minutes]]より

## Public artifacts checked

### 奈良 #全員市長 public viewer

- URL: https://everyonemayor.github.io/kouchou-ai/2025-7-13/
- 2026-06-30 確認時点で、public viewer として `2025年7月13日のレポート - 全員市長` が公開されていた。
- 公開 HTML 上では reporter が `全員市長`、コメント数は `1022` と読める。
- 広聴AIの public-viewer で、全体図 / 濃いクラスタ / 階層図 / 個別意見へ戻る動きを見せる候補になる。

### 渋谷区 official page / PDF

- Overview: https://www.city.shibuya.tokyo.jp/kusei/kocho/questionnaire/kuminishikichosa_ai.html
- Detail PDF: https://files.city.shibuya.tokyo.jp/assets/12995aba8b194961be709ba879857f70/38d509b421d049c4ad53536fc88ae4ca/kuminishikichosa_ai.pdf
- 議事録では 2025-07-02 の共有として、渋谷区の official public case が overview / detail PDF つきで記録されている。[[meeting-minutes]]より
- 自治体公式ページとして、広聴AIが公共 sector で試されていることを説明する材料になる。

### 八代市 Democracy-X public article / viewer

- Article: https://democracy-x.org/news/yatsushiro-kouchouai-202508/
- Result viewer: https://democracy-x.github.io/kouchou-ai-yatsushiro/47ae7bf4-e5de-4dbd-82ab-520160f373d6/
- 2026-06-30 確認時点で、Democracy-X の公開記事として `熊本県八代市ブロードリスニング公開` が公開され、広聴AIを活用したことと result viewer へのリンクが確認できた。
- 議事録上では、八代市事例は政策・選挙文脈を含み、「みんなが一番望んでいる」のような断定ではなく「そのニーズが見つかった」と説明する方が安全、という注意が残っている。[[meeting-minutes]]より

## Related candidates from meeting minutes / book source

- 広島県: 議事録では、公開中間結果、2,549 件規模、以前の類似 public comment が 13 件 / 5 人だったことなどが記録されている。ただし 8/2 でそのまま見せるには最新公開 URL と許諾の確認が必要。[[meeting-minutes]]より
- 朝日新聞: 書籍 source では、ラベル抽象化、見出しプロンプト、SNS キーワード設計、外れ値除外要望など、技術説明に有用な運用知見が多い。ただし図表・紙面・引用は権利確認が必要。[[broad-listening-book-source]]より
- サイボウズ / 富士通など企業・NPO系: 書籍・議事録上の事例として有用だが、権利者・顔出し・公開範囲の確認が必要。[[meeting-minutes]]より

## Open Questions

- 8/2 で public viewer を実演するなら、奈良 / 八代 / synthetic sample のどれを第一候補にするか。
- 渋谷区 official PDF をスライドに載せる場合、リンク紹介だけで足りるか、スクリーンショット利用の確認が要るか。
- 八代市事例を扱う場合、選挙・政策文脈を誰がどの表現で説明するか。
- 広島県など他自治体の公開 URL を、イベント直前に再確認して候補へ昇格できるか。

## Updates

- 2026-06-30: 初回作成。8/2 イベント向けの公開事例候補として、奈良 #全員市長、渋谷区、八代市の公開 artifact を確認し、広島県 / 朝日新聞 / 企業系は確認待ち候補として分けた。
