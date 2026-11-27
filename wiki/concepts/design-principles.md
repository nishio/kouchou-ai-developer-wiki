---
title: 機能設計の方針
type: concept
summary: "広聴AI の機能を作る・直す時に繰り返し使われてきた 4 つの設計方針：高度な機能は CLI から先に出す、plugin だけが使う依存を本体に入れない、Web 版と Windows 版を 1 つの実装で両立させようとしない、所与カテゴリの分類には必ず「その他」を付ける。それぞれの理由・判断の例・当てはめ方"
sources:
  - meeting-report-2026-10-18.md
  - open-decisions.md
  - municipal-workshop-issues-triage-2026-11-24.md
  - plugin-system.md
  - admin-api-key-threat-model-2026-11-11.md
  - llm-grouping-supervised-classification.md
---

# 機能設計の方針

広聴AI の Issue や PR で「どう作るか」を決める時に、メンテナ（nishio）の判断として繰り返し使われてきた方針を集めた。どれも個別の Issue で一度ずつ示されたもので、ここではそれを次の判断に使える形にまとめる。新しい機能を提案する前、実装の形を選ぶ前、レビューで設計に違和感を持った時に読む。

各方針の詳しい経緯は、リンク先の個別ページにある。

## 1. 高度な機能は CLI から先に出す

**方針**：一部の利用者しか使わない機能や実験的な機能は、まず analysis-core と CLI で使える形にする。Web の管理画面に載せるかは、別の判断として後に回す。

**理由**：Web UI と CLI を分けて analysis-core を共通の本体にしたのは、研究・開発向けの入口と非専門家向けの入口を分けるためだった（[[analysis-core-and-web-ui]]）。core で安く実現できる機能を、重い画面設計の都合で止めずに済む。実際に使われてから画面を作れば、画面設計の手間をかける価値があるかも分かる。

**判断の例**
- 別のレポートの UMAP の平面を使い回す（[#515](https://github.com/digitaldemocracy2030/kouchou-ai/issues/515)）：core では `fit_transform` を `transform` に変えるだけだが、管理画面では「使い回す元のレポートを選び、新しいデータを選ぶ」画面が要り、それが重くて止まっていた。CLI の設定項目として出し（PR [#988](https://github.com/digitaldemocracy2030/kouchou-ai/issues/988)）、画面側は [#989](https://github.com/digitaldemocracy2030/kouchou-ai/issues/989) に分けた。[[meeting-report-2026-10-18]]より
- tokoroten の賛否分離の 2 手法：本体には取り込まず docs で関連研究として紹介し、「入れるとしても CLI から」（[[open-decisions]] の A14）
- 利用者が定義するラベル（[#1225](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1225)）も CLI 先行で起こした。[[municipal-workshop-issues-triage-2026-11-24]]より

**当てはめ方**：機能を「仕上げる」依頼を受けたら、core・spec・CLI の docs・テストまでを 1 つの成果として出す。画面への配線は、先送りできる別の判断として示す（黙って省かず、勝手に作り込みもしない）。確かめる時は step 関数を直接呼ぶテストだけで済ませず、CLI の起動経路（設定の検証を含む）を通す。#515 の旧ブランチは、spec に設定項目が無いため起動時の検証で落ちるのに、step を直接呼ぶテストは全部通っていた。

## 2. plugin だけが使う依存を本体に入れない

**方針**：plugin の依存が足りなくて動かない時、lock や Docker イメージに依存を足す前に、その依存で実際に何を使っているかを見て、本体が既に持つ依存で置き換えられないかを考える。

**理由**：入力 plugin は実行時に環境変数で有効にするが、依存はイメージを作る時に決まる。全員のイメージに入れれば使わない依存を全員が持ち、入れ分ければ有効化とずれて同じ失敗が起きる。[[plugin-system]]より

**判断の例**：YouTube plugin が v4.2.0 のイメージで動かなかった件。最初は lock に extra を入れる案だったが、「plugin だけが使う依存を全体に入れるのは変」として、実際に使っていた REST 呼び出し 3 つを本体の依存にある `httpx` で直接呼ぶ形に作り直した（PR [#1149](https://github.com/digitaldemocracy2030/kouchou-ai/pull/1149)）。

**当てはめ方**：新しい入力 plugin では、まず `httpx` など本体の依存で足りるかを考える。重い SDK がどうしても要る時は、イメージへの入れ方（build arg と plugin の有効化をどう揃えるか）を先に決める。

## 3. Web 版と Windows 版を 1 つの実装で両立させようとしない

**方針**：配布の形が違う要求（Web で運用する管理画面と、手元の PC で動かす Windows 版）を、同じコードベースで同時に満たそうとしない。Windows 版は、CLI と静的 HTML のレポートを核にした別の配布物として考える。

**理由**：片方の制約がもう片方を歪める。たとえば Windows 版のために管理画面の作りを変えると、Web で運用する人に不要な変更を押し付ける。

**判断の例**：管理画面の API キーをサーバー側に隠す（[#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547)）と、Node をなくしてブラウザから直接 API を呼ぶ（[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)）の衝突を、「A／B／C のどれを選ぶか」の Issue（[#1197](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1197)）にしたところ、前提そのものが見直された。[[admin-api-key-threat-model-2026-11-11]]より

**あわせて使う考え方：露出は「見えて何が増えるか」で測る**。管理画面にログインできる人が API キーを知り得ることは、脅威とは言いにくい。キーが無くても、ログインした人は同じ操作ができるからである。秘密が見えることを一律に脅威とせず、「誰に見えて、見えたことで何ができるようになるか」で測る。

**当てはめ方**：2 つの Issue が逆向きの要求に見えたら、選択肢を並べる前に「そもそも同じ成果物で満たすべき要求か」「その露出で権限が増えるか」を先に問う。

## 4. 所与カテゴリの分類には必ず「その他」を付ける

**方針**：意見を、人間が与えたカテゴリ（指定カテゴリ）に振り分ける機能では、どのカテゴリにも当てはまらない意見のための「その他」を、システムが必ず付ける。利用者が指定しなくても付け、消せないようにする。

**理由**：当てはまらない意見を無理にどれかへ押し込むと、分類の質が落ち、カテゴリの抜けも見えなくなる。「その他」に意見が多く集まること自体が、カテゴリを見直す合図になる。[[llm-grouping-supervised-classification]]より

**判断の例**：LLM grouping の指定カテゴリ分類（[#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176) の方向性 2、[#996](https://github.com/digitaldemocracy2030/kouchou-ai/issues/996)）で、`llm_grouping.other_group_label`（既定「その他」）として実装した。LLM の応答が無効だった意見も、先頭のカテゴリではなく「その他」に寄せる。

**当てはめ方**：分類の機能を設計・レビューする時は、「その他」の受け皿があるかを必ず確かめる。将来は「その他」が多すぎる時の表示や警告もあるとよい。

## 関連ページ

- [[analysis-core-and-web-ui]]：Web UI と CLI を分けた理由（方針 1 の土台）
- [[usage-modes]]：CLI 版・サーバー版・ブラウザ版の違い（方針 3 の配布形態）
- [[plugin-system]]：plugin の仕組みと入力 plugin の依存（方針 2）
- [[llm-grouping-supervised-classification]]：指定カテゴリ分類の仕様（方針 4）
- [[open-decisions]]：まだ決まっていない論点の一覧

## Open Questions

- 方針 1 で CLI に先に出した機能（UMAP の使い回し、指定カテゴリ分類など）を、いつ・どんな条件で管理画面に載せるか。基準はまだ決まっていない
- 方針 3 の Windows 版を、具体的にどの形で配布するか（CLI と静的 HTML を同梱するのか、薄い専用の画面を付けるのか）
