---
type: analysis
summary: kouchou-ai 本体ドキュメント（mkdocs サイト + README）の方針をめぐる議論の系譜。2026-05 の「docs は AI の default」発見から、利用モード別導線・demo-first spine 再設計・docs issue の地図化・README 多言語化とアンカー凍結回避まで、通底する設計原則と未決論点を一本化
sources:
  - auto-cluster-defaults.md
  - pr-883-restructuring-2026-05-31.md
  - pr-883-developer-quickstart-draft-2026-05-31.md
  - nishio-docs-entry-restructure-discussion-2026-06-03.md
  - kouchou-ai-docs-entry-restructure-2026-06-03.md
  - experimental-features-catalog-proposal-2026-06-03.md
  - azure-demo-public-visibility-proposal-2026-06-04.md
  - docs-issue-map-2026-06-30.md
  - issue-876-developer-docs-gap-audit-2026-06-30.md
  - slack-readme-language-docs-site-2026-10-13.md
  - readme-anchor-freeze-and-docs-entry-2026-10-13.md
---

## このページの範囲

ここで扱うのは [[kouchou-ai]] **本体のドキュメント**（mkdocs サイト `digitaldemocracy2030.github.io/kouchou-ai/` と repo の `README.md`）の方針議論であって、本 developer-wiki 自身の運用ではない。本体 docs の「あり方」は 2026-05〜10 に複数のきっかけで繰り返し議論されたが、各回が別ページに散っていたので、系譜と通底する原則を 1 枚にまとめる。

本 developer-wiki 自身の index / log / 公開境界などのメンテ方針は別系統（CLAUDE.md と [[wiki-driven-workflow]] / [[wiki-pages-publishing-stack]]）。

## 時系列の弧

### 1. 2026-05-18 「AI に読ませる docs は実装そのもの」

クラスタ数デフォルト `[3, 6]` 問題の本質は、アルゴリズム論ではなく **docs / 実装 / AI 利用経路のズレ** だった。docs の数値例が AI コーディングエージェントにそのまま default として転用され、しかも repo 内に「Web では cube-root rule、CLI では `[3, 6]`」という二重基準が長く共存していた。[[auto-cluster-defaults]]より

ここで出た教訓が以後のすべての docs 議論の土台になる：**kouchou-ai の docs は単なる説明資料ではなく、AI にとっての reusable prompt / template でもある**。具体例は「読者がコピペするか」だけでなく「AI が default と見なすか」で評価すべき。

### 2. 2026-05-29〜31 開発者導線を利用モード別に（PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883)）

開発者向け導線を利用モード別に整理する PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883)（closes [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)）を起点に、「開発者向け docs」というラベル自体が **動機の違うサブ役割を一括りにしていた** ことが露呈。最終的に読者像を 5 つ（一般ユーザ / 自治体担当本人 / 組織内デモ役 / WebUI 開発者 / 分析者・研究者）に分け、「迷ったら Mode 1（Docker Compose）」という default を廃止し、各読者像に直接 Mode を割り当てる方針へ。環境構築の決定フロー（最初の分岐は OS でなく利用主体）を Mode 選択の前に置く。[[pr-883-restructuring-2026-05-31]] / [[pr-883-developer-quickstart-draft-2026-05-31]]より

nishio は「もうちょっと何が語られるべきかを整理してから作るべきだな」と判断し、PR をいったん保留。直近 1 週間で固まった整理（platform 安定性ティア Linux > Mac > Windows、Docker Desktop license、構造把握スタンス、CLI のデータ量前提）を docs に取り込んでから書き直す方針に倒した。

### 3. 2026-06-03 docs 入口の spine 再設計（nishio 提起）

最も根本的な提起。本体 docs が `getting-started/`（= セットアップ手順）から始まる構造が、「興味を持った人 = 自分でツールを立てる開発者」というバイアスを産み、レポートの読み手・分析者・方法論研究者を振り落としていた。`getting-started/` という**ディレクトリ名自体が「ここから始めろ」という暗黙メッセージ**で、同じ罪を犯している。[[nishio-docs-entry-restructure-discussion-2026-06-03]]より

提案された新 spine（[[kouchou-ai-docs-entry-restructure-2026-06-03]]より）：

```
1. 入口: デモサイトでレポートを見る（viewer の使い方 + 公開事例リンク集）
2. 「自分のデータで作りたい」分岐
   ├ a. 誰かが建てたサーバを使う（managed）
   ├ b. 建ててくれる人を探す（仲介者）
   └ c. 自分で建てる ← ここで初めてセットアップ手順が登場
3. 「研究者・開発者はこちら」分岐（CLI + 実験的機能カタログ）
```

セットアップは spine の入口ではなく、特定ニーズの人が辿り着く先。既存 docs は「新構造に当てはめるために無理に残さず、改善・削除も含めて柔軟に」扱う（nishio 指示）。

同じ対話で **実験的機能カタログ** も提案された（LLM grouping / DivCon / Farbrain / マンダラート可視化 等を本体 docs 内にフラットに集め、個人 repo の stale 対策として「最終確認日」をエントリ必須にする）。これは developer-wiki 側の「情報鮮度の明示」ルールを本体 docs へ持ち込む発想。[[experimental-features-catalog-proposal-2026-06-03]]より

### 4. 2026-06-04〜05 Azure デモ動線化と tier の 3 択化

spine tier 2 を「(a) managed / (b) self-host」の 2 択から **3 択（managed / 仲介者 / self-host）** へ refinement。「自分で建てる気はないが社内・自治体内に建ててくれそうな人がいる」読者の経路を明示。デモ環境の価値を「データ投入の予行演習」ではなく **「使い方や準備すべきデータを理解するための参照環境」** に再フレーム。[[azure-demo-public-visibility-proposal-2026-06-04]]より

これにより spine tier 1（デモを見る）と tier 2-a（managed で作る）の docs 動線を埋める前提が立った。

### 5. 2026-06-30 docs issue の地図化

散った docs 系 issue / PR（[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) developer quickstart / [#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877) Windows setup / [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) Node runtime 排除 / PR [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) inventory / [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)・[#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) reading guide）の依存関係を 1 枚に。全部「docs」だが **同じページに詰めると読者像が混ざる** ため、「どの issue が誰向けの何を扱うか」を分離する地図。[[docs-issue-map-2026-06-30]]より

同時に [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) の gap audit を実施：草案（5 読者像 / Mode 1 default 廃止）は要件を満たすが、current main の `README.md` / `docs/index.md` / `docs/getting-started/quickstart.md` / `mkdocs.yml` はまだ setup-first のまま。**[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) を閉じるには単体ページ追加では弱く、nav と入口文言の調整を同時にやる first slice が要る**。6/3 spine の完成形（demo-first / getting-started rename）はより広い docs product design として別 issue に分ける。[[issue-876-developer-docs-gap-audit-2026-06-30]]より

### 6. 2026-10-13 README 多言語化事件とアンカー凍結回避

README を英語デフォルト化（PR [#966](https://github.com/digitaldemocracy2030/kouchou-ai/issues/966)）→日本語へ差し戻し（PR [#968](https://github.com/digitaldemocracy2030/kouchou-ai/issues/968)）した事件をきっかけに、nishio が 2 つの設計判断を提示。[[slack-readme-language-docs-site-2026-10-13]] / [[readme-anchor-freeze-and-docs-entry-2026-10-13]]より

1. **README を外部アンカーリンクで凍結してはいけない**：`README.md#section` への外部ディープリンクが切れることを理由に改訂を止めると、一度でも外部リンクされた README は金輪際改訂できなくなる。安定 URL を提供する責務は docs サイトの個別ページへ移し、README は改訂可能な入口として保つ（GitHub issue [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) が root-cause 対応）。
2. **非英語話者・非開発者の入口は GitHub でなくドキュメントサイト**：英語 UI の GitHub で全員を受け止めようとするのが無理筋。読者の層ごとに着地すべき面を変える。

後者は「docs 入口がセットアップ起点」「`getting-started/` 命名バイアス」という 6 月の spine 議論と**同じ地層**で、README 言語の議論はそこへ戻った。多言語 README 自体は「日本語デフォルト + `[English] | 日本語 | [한국어]` 言語リンク」で一旦着地（nishio 曰く「緊急避難的 OK」の暫定）。

## 通底する設計原則（横断テーマ）

議論は別々のきっかけから出たが、繰り返し現れる原則は共通している。

- **docs は AI の default / template**：具体例は「AI が default と見なすか」で評価する。docs・実装・AI 利用経路を同一方向に揃える。[[auto-cluster-defaults]]より
- **セットアップ起点をやめ、読者像で分岐する（demo-first）**：入口はレポート閲覧。setup は「自分で host したい人」が辿り着く先。[[kouchou-ai-docs-entry-restructure-2026-06-03]]より
- **「開発者」を一括りにしない**：5 読者像に分け、Mode 1 default を押し付けない。[[pr-883-restructuring-2026-05-31]]より
- **安定 URL 責務は docs サイト、README は流動的入口**：外部リンクは個別 doc ページへ張らせる。[[readme-anchor-freeze-and-docs-entry-2026-10-13]]より
- **読者像を混ぜない**：1 ページ / 1 issue に異なる読者の関心を詰めない。[[docs-issue-map-2026-06-30]]より
- **外部参照には freshness（最終確認日）**：developer-wiki の情報鮮度ルールを本体 docs にも拡張。[[experimental-features-catalog-proposal-2026-06-03]]より
- **公開境界は本体 docs でも適用**：Azure デモの実 URL・resource・secret・運用手順は本体 docs にも書かず、公開可能な案内・免責・入口文言の粒度に留める。[[issue-876-developer-docs-gap-audit-2026-06-30]]より

## 現在の状態（wiki 観測ベース）

**2026-09 wave 後の棚卸し（2026-10-13 live 確認で判明）**: 6/30 の [[docs-issue-map-2026-06-30]] が並べた docs レーンは、**2026-09-08〜09 の merge / close wave でほぼ消化された**（[#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877) Windows guide → PR [#929](https://github.com/digitaldemocracy2030/kouchou-ai/issues/929)、PR [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) Node inventory → merge、[#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884) 作成前確認 → PR [#922](https://github.com/digitaldemocracy2030/kouchou-ai/issues/922)、[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) 誤読防止 → PR [#924](https://github.com/digitaldemocracy2030/kouchou-ai/issues/924)・[#24](https://github.com/digitaldemocracy2030/kouchou-ai/issues/24)）。残る docs 方針の宙吊りは次の 3 点に絞られる：

1. **入口 spine の本丸 [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)**（nishio assigned。last comment は 2026-05-31 だが **body は 2026-09-08 に再スコープされ umbrella 化**）— demo-first spine / `getting-started/` rename という「書けば済む」より大きい docs product design
2. **README アンカー衛生 [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)**（2026-10-12 起票・ノータッチ）— 安定 URL を docs 側へ寄せる判断 1 の root-cause
3. **レポート責任所在 [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)**（2025-05-19 起票・ノータッチ）— reading-guide レーンの片割れ。「読み方」([#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)) は landing したが「責任所在」は未着手

3 点とも **実装レーン（[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) shell-build 等）より人間の方針判断待ち** が残っている部分であり、文言を書く作業ではなく入口設計・安定 URL 設計・責任分界の意思決定が律速。

- **[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)**（developer quickstart / docs entry 再構成）: **2026-10-13 live 確認で open / nishio assigned / label `documentation`**。コメントは 2026-05-31 の 1 件（PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883) 撤回 + 新方針）のみだが、**body が 2026-09-08（updatedAt）に再スコープ**され「現状と残作業」節で PR [#925](https://github.com/digitaldemocracy2030/kouchou-ai/issues/925) / [#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877)・[#929](https://github.com/digitaldemocracy2030/kouchou-ai/issues/929)・[#496](https://github.com/digitaldemocracy2030/kouchou-ai/issues/496)・[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) を束ねる umbrella になっている。したがって「2026-05-31 以降ノータッチ」ではなく「last comment は 5/31・body 再スコープは 9/08」が正確。developer-quickstart.md（PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883) は CLOSED）は本体 main 未着。
- **[#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877)**（Windows setup guide scope）: **2026-10-13 live 確認で CLOSED（2026-09-08、nishio assigned / label `documentation`）**。**PR [#929](https://github.com/digitaldemocracy2030/kouchou-ai/issues/929)「docs: Windows導入の対象環境と失敗時の確認順を明確化」（nishio, branch `codex/issue-877-windows-guide`, merged 2026-09-08）で close**。6 月に wiki で整理した [[windows-setup-guide-outline-2026-06-30]]（対象環境 / 対象外環境 / 失敗時の確認順）がほぼこの形で landing した。
- **PR [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903)**（Node runtime inventory docs, [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) 第1完了条件）: **2026-10-13 live 確認で MERGED（2026-09-08, yasumorishima）**。6/30 は open / review required / blocked だったが、その後 merge 済み。
- **[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)**（Windows 単一 exe 向け Node runtime 依存排除）: **2026-10-13 live 確認で open / unassigned / label enhancement・Client・Admin・API**。2026-09-09 に yasumorishima が shell-build 方式（`NEXT_PUBLIC_STATIC_SHELL=1` でレポート非依存 HTML を 1 ルート出力し slug へ複製）の実装計画を提示し、9 月の shell viewer PR 群（[[pr-935-936-overview-2026-09-09]] / [[issue-939-shell-metadata-2026-09-09]]）へ具体化。full な Node-runtime-free 配布はまだ未完。
- **[#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)**（README アンカー依存の脱却）: **2026-10-13 live 確認で open / unassigned / 起票（2026-10-12）以来コメント 0・ノータッチ**。判断 1 の root-cause 対応。
- **[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) / [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)**（レポート誤読防止 + 責任所在 = reading-guide / trust-layer docs レーン）: **2026-10-13 live 確認で [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) CLOSED（2026-09-08, nishio）/ [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) なお OPEN**。[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) は **PR [#924](https://github.com/digitaldemocracy2030/kouchou-ai/issues/924)「レポートに読み方ガイドを表示し、件数の誤解釈を防ぐ」（kouchou-ai, 2026-09-08 merge）** で close。あわせて cross-repo の **`tokoroten/kouchou-ai-serverless#24`（本体と揃えた読み方ガイドを単一HTMLに追加, 2026-09-09 merge）** が serverless 側で landing（`kouchou-ai#24` は無関係な別 issue なので混同しない）。一方 **[#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)「レポートに関する責任の所在を明記」（label `documentation`・`API`）は unassigned で 2025-05-19 起票以来ノータッチ**。[[report-reading-guide-minimum-wording-2026-06-30]] の「読み方」側は landing、「責任所在」側は未着手、と非対称に進んだ。
- **README**: current main は日本語デフォルト + 言語リンク（[#968](https://github.com/digitaldemocracy2030/kouchou-ai/issues/968) 差し戻し後）。

> freshness: [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) / [#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877) / [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) / [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) / [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) / [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) / [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) は 2026-10-13 に `gh issue view` / `gh pr view` で live 確認。6/30 からの変化は **[#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877) CLOSED（PR [#929](https://github.com/digitaldemocracy2030/kouchou-ai/issues/929)）/ PR [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) MERGED / [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) が shell-build で前進 / [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) CLOSED（PR [#924](https://github.com/digitaldemocracy2030/kouchou-ai/issues/924) + serverless#24）** の 4 点。残る OPEN は [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)（body 2026-09-08 再スコープ=umbrella）/ [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)（前進中・no-assignee）/ [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)（ノータッチ）/ [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)（ノータッチ）。

## Open Questions

- `getting-started/` rename は破壊的。redirect / alias / old URL 維持をどう扱うか。[[issue-876-developer-docs-gap-audit-2026-06-30]]
- [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) を単体ページ追加で close するか、docs spine first slice（nav + 入口文言同時変更）とするか。
- spine 2-a の managed service は実在するか。不在なら研究者の主入口は CLI + カタログ経由になり、カタログの重みが上がる。[[kouchou-ai-docs-entry-restructure-2026-06-03]] / [[experimental-features-catalog-proposal-2026-06-03]]
- 仲介者経路（建ててくれる人を探す）を docs 内の連絡先リストにするか、DD2030 Web / Slack / form へ逃がすか。誰がメンテし、紹介後の責任分界点をどうするか。
- README 外部アンカーリンクの実態（どこから何件）は未調査。移行先ページ・redirect 方針は未定（[#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)）。
- 非開発者を GitHub 経由させず docs サイトへ着地させる具体導線（配布物 / 事例サイト / 検索流入の向き先）は未設計。6 月 spine 再設計と合流が必要。

## 関連

- [[kouchou-ai-docs-overhaul-2026-10]]: 本原則を実装した 2026-10 改善スプリントの retrospective（総括の読み物）
- [[kouchou-ai-docs-improvement-roadmap-2026-10-13]]: 本ページの原則と現在地監査を踏まえ「何がどうなると良いか / どの順で」を 4 層 roadmap（write-and-done+rot-gate → additive reader-facing → signed content → policy-gated 本丸）に落とした direction
- [[docs-reader-coverage-audit-2026-10-13]]: 本ページの原則（5 読者像）に照らした current main の実カバレッジ監査。直近 feature wave 後に A/C(WebUI 利用者)が未追従・D/運用が nav 未登録で未到達、という偏りと 1-PR 粒度の修正候補
- [[docs-issue-map-2026-06-30]]: 2026-06-30 時点の docs issue 依存マップ（本ページの点断面）
- [[kouchou-ai-scope-line-from-marketing-to-plugin-2026-06-03]]: docs 読者像の背後にあるプロダクト・スコープ線
- [[broadlistening-tool-ecosystem-vision]]: Web UI = simple / CLI = 実験機能、という二段構造（docs 分岐の根拠）
- [[analysis-stance]]: 「広聴AI は構造把握スタンス」という、docs に 1 段落入れるべき core stance
- [[setup-script-env-drift-2026-10-07]] / [[docs-site-icon-shortcode-bug-2026-10-13]]: docs / setup の実装側の落とし穴

## Updates

- 2026-10-13: 初版作成。2026-05〜10 に散っていた本体 docs 方針議論（auto-cluster-defaults / PR [#883](https://github.com/digitaldemocracy2030/kouchou-ai/issues/883) / 6 月 spine 再設計 / Azure デモ動線化 / docs-issue-map / README 多言語化）を時系列の弧と横断原則で一本化した。
- 2026-10-13: [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) / [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) を `gh issue view` で live 確認。両者 open のまま wiki 記録と一致（[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) nishio assigned・新規議論なし、[#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) 起票以来ノータッチ）。freshness 注記を更新。
- 2026-10-13: [#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877) / [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) / PR [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) も live 確認し、6/30 からの差分を反映。**[#877](https://github.com/digitaldemocracy2030/kouchou-ai/issues/877) は PR [#929](https://github.com/digitaldemocracy2030/kouchou-ai/issues/929) で CLOSED（2026-09-08）**、**PR [#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903) は MERGED（2026-09-08）**、**[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) は shell-build 方式で前進**（いずれも wiki 記録では未反映だった）。
- 2026-10-13: reading-guide / trust-layer レーンの [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) / [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) を live 確認。**[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696)（誤読防止）は PR [#924](https://github.com/digitaldemocracy2030/kouchou-ai/issues/924)・[#24](https://github.com/digitaldemocracy2030/kouchou-ai/issues/24) で CLOSED（2026-09-08）/ [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)（責任所在）はなお OPEN・ノータッチ**。「読み方」は landing・「責任所在」は未着手の非対称を記録。なお [#884](https://github.com/digitaldemocracy2030/kouchou-ai/issues/884)（作成前確認パネル）は docs-policy というより試行錯誤負担（[#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221)）レーンの UX 機能で、PR [#922](https://github.com/digitaldemocracy2030/kouchou-ai/issues/922) の first slice で CLOSED 済み（下位 [#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11)/[#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)/[#292](https://github.com/digitaldemocracy2030/kouchou-ai/issues/292)/[#391](https://github.com/digitaldemocracy2030/kouchou-ai/issues/391) 等は残置）。詳細は [[issue-884-pre-create-review-contract-2026-06-30]] / [[trial-and-error-burden-reduction-2026-05-29]]。
- 2026-10-13: 独立 live 再検証（9 agent workflow）で 2 箇所を訂正。(1) **[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) は「2026-05-31 以降議論なし」でなく、body が 2026-09-08 に再スコープされた umbrella**（last comment と updatedAt を区別）。(2) **[#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696) を閉じた「[#24](https://github.com/digitaldemocracy2030/kouchou-ai/issues/24)」は cross-repo の `tokoroten/kouchou-ai-serverless#24`** であって `kouchou-ai#24` ではない。あわせて本ページの原則を道筋化した [[kouchou-ai-docs-improvement-roadmap-2026-10-13]] を新設。
- 2026-10-14: **入口 spine の本丸 [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) が CLOSED**。canonical「始め方の選び方」ページ（[#1010](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1010)）＋ demo-first 入口（[#1000](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1000)）＋ `getting-started/`→`self-hosting/` rename（[#1005](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1005)）で headline 完了条件を達成。残細目（README スリム化・モード別落とし穴集約等）は [#1012](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1012)、umbrella が参照していた [#496](https://github.com/digitaldemocracy2030/kouchou-ai/issues/496)/[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) は独立課題として de-bundle。実装の系譜は [[kouchou-ai-docs-improvement-roadmap-2026-10-13]]。
