---
type: analysis
summary: open issue 145 件から抽出すると、未解決なのは大量の個別要望ではなく、実行入口・失敗診断・公開運用・可視化・アルゴリズム・運用基盤など十数個の根本問題である
sources:
  - open-issue-backlog-2026-05-19.md
  - issue-priority-through-2026-09.md
  - open-decisions.md
  - refactoring-status.md
  - usage-modes.md
---

open issue 145 件を本文まで読むと、backlog は大量の feature request の集合というより、**少数の根本問題が別の言い方で何度も現れている状態** と読める。本ページでは「解決すべき問題」を先に立て、個別 issue はあくまでその問題に対する観測点や解決案へのリンクとしてぶら下げる。[[open-issue-backlog-2026-05-19]]より

この時に重要なのは、**ユーザが感じている「困りごと」は本物でも、issue 内で提案されている「解決策」は current `main` では外れていることが多い**、という読み方である。したがって issue triage では、まず「何に困っているか」を抽出し、その後で解決策を current path に引き直して再設計する。[[open-issue-backlog-2026-05-19]]より

## Priority Through 2026-09

9 月前に解く順へ並べると、次の順が妥当。基準は **current path の安定化、失敗時の自己診断性、公開運用の事故回避、新規流入の受け皿** である。[[issue-priority-through-2026-09]]より

1. 利用モードごとの正規入口が固定されておらず、古い経路や重すぎる入口に迷い込みやすい
理由: 研究者向けの CLI と非専門家向けの Web UI で正規入口が違うのに、その線引きが曖昧なままだと docs、validation、配布形態、サポート範囲が全部ぶれる。

2. 実行前に防げる失敗を preflight できず、壊れてから気づく
理由: 入力や設定の誤りを早く落とせないと、CLI でも Web でも調査コストが高い。

3. Web UI / static export / self-hosted 公開が壊れやすい
理由: 9 月前の利用導線として、成果物を共有・公開する経路が brittle なままなのは危険。

4. provider / API / 認証設定が一貫せず、使える環境でも「使えない」と見える
理由: 実際には動く環境で誤判定する状態は、非専門家ユーザにとって「壊れている」と同義になる。

5. 失敗したときに原因が見えず、自己解決もコミュニティ支援も難しい
理由: 不具合ゼロにはできないので、次に重要なのは失敗時に調べられること。

6. レポート artifact と schema の一貫性が弱い
理由: 保存・再読・同期・公開の契約が弱いと、公開運用や再利用のバグが繰り返される。

7. Windows / ローカル環境のセットアップ摩擦が高い
理由: 新規 contributor / user の初回離脱点として重いが、まず canonical path 固定の後に効かせたい。

8. テスト・CI・リリース・デプロイ基盤が弱く、保守負荷が高い
理由: 本来は常に重要だが、9 月前は user-facing failure を止める作業と並走で強化する位置づけ。

9. 分析結果の意味づけと責任ある読み方が伝わりにくい
理由: 書籍公開で流入が増える前に重要だが、まず product が安定してから載せる方が筋がよい。

10. 可視化が「読めない」「触りにくい」「誤操作しやすい」
理由: UX 上の痛みは強いが、入口・公開・誤判定の問題よりは一段後ろ。

11. contributor onboarding と non-code contribution 導線が弱い
理由: 地盤として重要だが、受け皿となる current path が固まってから整える方が効率がよい。

12. レポート作成後の編集・再利用・運用フローが弱い
理由: 運用機能として価値は高いが、まずは生成と公開の主経路を安定化したい。

13. セキュリティ・公開範囲・乱用対策がまだ完成していない
理由: 長期的には重いが、9 月前の短期では方針論も多く、即効の実装課題へ落ちにくい。

14. 非 OpenAI 系や low-cost 運用への需要があるが、製品としての受け皿が揃っていない
理由: 需要はあるが、provider の入口不整合を直す前に広げると複雑性だけ増えやすい。

15. アルゴリズム品質・速度・再現性のトレードオフ整理が終わっていない
理由: 重要だが探索空間が広く、9 月前の主目標である current path の安定化からは距離がある。

## Problem List

### 1. 利用モードごとの正規入口が固定されておらず、古い経路や重すぎる入口に迷い込みやすい

解決すべき問題は、「誰が、どの入口を使うべきか」が伝わりにくいこと。`analysis-core` への移行後も、研究者・データサイエンティスト向けの CLI と、非専門家向けの Web UI を別の正規入口として扱う整理が十分に前面化していない。[[refactoring-status]]より [[usage-modes]]より

ここでの実務的な前提は次の通り。

- 研究者・データサイエンティストには `Mac/Linux + CLI` をほぼ前提にしてよい
- その `Windows` 利用者には、まず `WSL2` か `Docker` を使ってください、で割り切る余地がある
- 一方、非エンジニアの試行錯誤ユースケースでは CLI 作業を最小化し、理想的には `Zip + setup.bat + Web UI` に近い入口を目指すべき

つまり 1 位の問題は CLI を全員の正規入口にすることではなく、利用モードごとに違う正規入口を固定し、それぞれに合った friction budget を明示することである。

関連 issue:
- 解決案の議論: [#721](https://github.com/digitaldemocracy2030/kouchou-ai/issues/721), [#836](https://github.com/digitaldemocracy2030/kouchou-ai/issues/836), [#496](https://github.com/digitaldemocracy2030/kouchou-ai/issues/496), [#287](https://github.com/digitaldemocracy2030/kouchou-ai/issues/287), [#254](https://github.com/digitaldemocracy2030/kouchou-ai/issues/254)

### 2. 実行前に防げる失敗を preflight できず、壊れてから気づく

本物の問題は、config・input・環境差分の誤りが高コストな実行後や build 後まで表面化しないこと。validation をどこに置くかは解決策の話であって、先にある問題は fail-fast 不足である。[[issue-priority-through-2026-09]]より

関連 issue:
- 解決案の議論: [#837](https://github.com/digitaldemocracy2030/kouchou-ai/issues/837), [#838](https://github.com/digitaldemocracy2030/kouchou-ai/issues/838), [#97](https://github.com/digitaldemocracy2030/kouchou-ai/issues/97), [#253](https://github.com/digitaldemocracy2030/kouchou-ai/issues/253), [#391](https://github.com/digitaldemocracy2030/kouchou-ai/issues/391)

### 3. provider / API / 認証設定が一貫せず、使える環境でも「使えない」と見える

OpenAI / Azure / LocalLLM / OpenRouter の分岐が利用モードや画面ごとに揃っておらず、実際には動く環境でも接続チェックや model list 取得で失敗しやすい。これは provider 拡張不足というより、**provider abstraction の不整合** が問題。[[open-decisions]]より

関連 issue:
- 解決案の議論: [#707](https://github.com/digitaldemocracy2030/kouchou-ai/issues/707), [#681](https://github.com/digitaldemocracy2030/kouchou-ai/issues/681), [#473](https://github.com/digitaldemocracy2030/kouchou-ai/issues/473), [#477](https://github.com/digitaldemocracy2030/kouchou-ai/issues/477), [#592](https://github.com/digitaldemocracy2030/kouchou-ai/issues/592), [#385](https://github.com/digitaldemocracy2030/kouchou-ai/issues/385), [#537](https://github.com/digitaldemocracy2030/kouchou-ai/issues/537), [#255](https://github.com/digitaldemocracy2030/kouchou-ai/issues/255)

### 4. Web UI / static export / self-hosted 公開が壊れやすい

レポートを共有・公開する経路が brittle で、環境差分や公開状態の違いによって build failure や runtime failure が起きやすい。これは個別バグというより **publish path がまだ堅くない** ことが問題。[[issue-priority-through-2026-09]]より

関連 issue:
- 解決案の議論: [#833](https://github.com/digitaldemocracy2030/kouchou-ai/issues/833), [#685](https://github.com/digitaldemocracy2030/kouchou-ai/issues/685), [#683](https://github.com/digitaldemocracy2030/kouchou-ai/issues/683), [#820](https://github.com/digitaldemocracy2030/kouchou-ai/issues/820), [#818](https://github.com/digitaldemocracy2030/kouchou-ai/issues/818), [#518](https://github.com/digitaldemocracy2030/kouchou-ai/issues/518), [#333](https://github.com/digitaldemocracy2030/kouchou-ai/issues/333), [#271](https://github.com/digitaldemocracy2030/kouchou-ai/issues/271)

### 5. 失敗したときに原因が見えず、自己解決もコミュニティ支援も難しい

ユーザは「失敗した」という事実だけを見ており、ログ・状態・原因候補に辿りつけない。結果としてプロダクトの信頼性というより、**失敗時の観測可能性** が不足している。[[issue-priority-through-2026-09]]より

関連 issue:
- 解決案の議論: [#716](https://github.com/digitaldemocracy2030/kouchou-ai/issues/716), [#315](https://github.com/digitaldemocracy2030/kouchou-ai/issues/315), [#211](https://github.com/digitaldemocracy2030/kouchou-ai/issues/211), [#11](https://github.com/digitaldemocracy2030/kouchou-ai/issues/11), [#79](https://github.com/digitaldemocracy2030/kouchou-ai/issues/79)

### 6. Windows / ローカル環境のセットアップ摩擦が高い

OS 差分や文字コード差分で初回導入が詰まりやすく、Docker 非依存の導線もまだ十分に安定していない。これは単発の Windows バグというより、**セットアップ体験が環境依存で壊れやすい** ことが問題。[[open-issue-backlog-2026-05-19]]より

関連 issue:
- 解決案の議論: [#731](https://github.com/digitaldemocracy2030/kouchou-ai/issues/731), [#666](https://github.com/digitaldemocracy2030/kouchou-ai/issues/666), [#530](https://github.com/digitaldemocracy2030/kouchou-ai/issues/530), [#287](https://github.com/digitaldemocracy2030/kouchou-ai/issues/287), [#254](https://github.com/digitaldemocracy2030/kouchou-ai/issues/254), [#289](https://github.com/digitaldemocracy2030/kouchou-ai/issues/289)

### 7. レポート artifact と schema の一貫性が弱い

list 表示、backup、status、token/cost 集計、slug など、report artifact の取り扱いが経路によって揺れやすい。これは UI 表示だけの問題ではなく、**report をどう保存し、再読し、同期し、公開するかの契約が弱い** ことが問題。[[open-decisions]]より

関連 issue:
- 解決案の議論: [#740](https://github.com/digitaldemocracy2030/kouchou-ai/issues/740), [#629](https://github.com/digitaldemocracy2030/kouchou-ai/issues/629), [#584](https://github.com/digitaldemocracy2030/kouchou-ai/issues/584), [#507](https://github.com/digitaldemocracy2030/kouchou-ai/issues/507), [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542), [#19](https://github.com/digitaldemocracy2030/kouchou-ai/issues/19)

### 8. 可視化が「読めない」「触りにくい」「誤操作しやすい」

scatter chart、hierarchy view、mobile view、fullscreen view、ラベル重なり、wheel 誤操作など、可視化レイヤには recurring pain が多い。本質は個々の UI tweak 不足というより、**可視化を exploration tool と communication artifact の両方に使っている緊張** にある。[[open-decisions]]より

関連 issue:
- 解決案の議論: [#710](https://github.com/digitaldemocracy2030/kouchou-ai/issues/710), [#493](https://github.com/digitaldemocracy2030/kouchou-ai/issues/493), [#306](https://github.com/digitaldemocracy2030/kouchou-ai/issues/306), [#290](https://github.com/digitaldemocracy2030/kouchou-ai/issues/290), [#294](https://github.com/digitaldemocracy2030/kouchou-ai/issues/294), [#266](https://github.com/digitaldemocracy2030/kouchou-ai/issues/266), [#283](https://github.com/digitaldemocracy2030/kouchou-ai/issues/283), [#121](https://github.com/digitaldemocracy2030/kouchou-ai/issues/121), [#337](https://github.com/digitaldemocracy2030/kouchou-ai/issues/337), [#227](https://github.com/digitaldemocracy2030/kouchou-ai/issues/227), [#60](https://github.com/digitaldemocracy2030/kouchou-ai/issues/60), [#52](https://github.com/digitaldemocracy2030/kouchou-ai/issues/52)

### 9. レポート作成後の編集・再利用・運用フローが弱い

一括編集、再利用、コピー、手動修正、属性フィルタ、入力補助など、作った後に育てる workflow が弱い。本質は「生成して終わり」寄りで、**運用しながら整える UI/UX が不足している** こと。[[open-issue-backlog-2026-05-19]]より

関連 issue:
- 解決案の議論: [#648](https://github.com/digitaldemocracy2030/kouchou-ai/issues/648), [#515](https://github.com/digitaldemocracy2030/kouchou-ai/issues/515), [#310](https://github.com/digitaldemocracy2030/kouchou-ai/issues/310), [#293](https://github.com/digitaldemocracy2030/kouchou-ai/issues/293), [#281](https://github.com/digitaldemocracy2030/kouchou-ai/issues/281), [#19](https://github.com/digitaldemocracy2030/kouchou-ai/issues/19), [#305](https://github.com/digitaldemocracy2030/kouchou-ai/issues/305), [#639](https://github.com/digitaldemocracy2030/kouchou-ai/issues/639)

### 10. 分析結果の意味づけと責任ある読み方が伝わりにくい

利用者が可視化の説得力をそのまま「正しさ」と受け取りやすく、分析の限界・偏り・責任範囲が十分に共有されていない。これは docs の有無より、**プロダクトが何を保証し、何を保証しないかの伝達不足** が問題。[[issue-priority-through-2026-09]]より

関連 issue:
- 解決案の議論: [#696](https://github.com/digitaldemocracy2030/kouchou-ai/issues/696), [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542), [#564](https://github.com/digitaldemocracy2030/kouchou-ai/issues/564), [#519](https://github.com/digitaldemocracy2030/kouchou-ai/issues/519)

### 11. アルゴリズム品質・速度・再現性のトレードオフ整理が終わっていない

クラスタ数、UMAP、embedding、grounding、個人情報除去、ファクトチェック、LLM 分類など、多くの issue は「機能追加」に見えて、実際には **どの品質軸をどこまで最適化するかが定まっていない** 問題に属する。[[open-decisions]]より

関連 issue:
- 解決案の議論: [#809](https://github.com/digitaldemocracy2030/kouchou-ai/issues/809), [#577](https://github.com/digitaldemocracy2030/kouchou-ai/issues/577), [#576](https://github.com/digitaldemocracy2030/kouchou-ai/issues/576), [#573](https://github.com/digitaldemocracy2030/kouchou-ai/issues/573), [#516](https://github.com/digitaldemocracy2030/kouchou-ai/issues/516), [#514](https://github.com/digitaldemocracy2030/kouchou-ai/issues/514), [#513](https://github.com/digitaldemocracy2030/kouchou-ai/issues/513), [#503](https://github.com/digitaldemocracy2030/kouchou-ai/issues/503), [#474](https://github.com/digitaldemocracy2030/kouchou-ai/issues/474), [#470](https://github.com/digitaldemocracy2030/kouchou-ai/issues/470), [#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176), [#173](https://github.com/digitaldemocracy2030/kouchou-ai/issues/173), [#172](https://github.com/digitaldemocracy2030/kouchou-ai/issues/172), [#170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/170), [#143](https://github.com/digitaldemocracy2030/kouchou-ai/issues/143), [#44](https://github.com/digitaldemocracy2030/kouchou-ai/issues/44)

### 12. 非 OpenAI 系や low-cost 運用への需要があるが、製品としての受け皿が揃っていない

ローカル LLM、embedding 選択、利用可能モデル拡張、Batch API、OpenRouter などの issue は多い。根本問題は provider 数不足より、**コスト制約や閉域環境に耐える運用モードをどこまで product として支えるか** が未整理なこと。[[open-issue-backlog-2026-05-19]]より

関連 issue:
- 解決案の議論: [#613](https://github.com/digitaldemocracy2030/kouchou-ai/issues/613), [#537](https://github.com/digitaldemocracy2030/kouchou-ai/issues/537), [#471](https://github.com/digitaldemocracy2030/kouchou-ai/issues/471), [#464](https://github.com/digitaldemocracy2030/kouchou-ai/issues/464), [#452](https://github.com/digitaldemocracy2030/kouchou-ai/issues/452), [#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450), [#385](https://github.com/digitaldemocracy2030/kouchou-ai/issues/385), [#374](https://github.com/digitaldemocracy2030/kouchou-ai/issues/374), [#295](https://github.com/digitaldemocracy2030/kouchou-ai/issues/295), [#285](https://github.com/digitaldemocracy2030/kouchou-ai/issues/285)

### 13. テスト・CI・リリース・デプロイ基盤が弱く、保守負荷が高い

deploy failure、CI 設定、レビュー自動化、E2E 不足、server テストしづらさなどの issue は、どれも「新機能」ではなく **変更を安全に出し続ける基盤** の不足を示している。[[open-decisions]]より

関連 issue:
- 解決案の議論: [#741](https://github.com/digitaldemocracy2030/kouchou-ai/issues/741), [#669](https://github.com/digitaldemocracy2030/kouchou-ai/issues/669), [#700](https://github.com/digitaldemocracy2030/kouchou-ai/issues/700), [#690](https://github.com/digitaldemocracy2030/kouchou-ai/issues/690), [#643](https://github.com/digitaldemocracy2030/kouchou-ai/issues/643), [#586](https://github.com/digitaldemocracy2030/kouchou-ai/issues/586), [#558](https://github.com/digitaldemocracy2030/kouchou-ai/issues/558), [#546](https://github.com/digitaldemocracy2030/kouchou-ai/issues/546), [#445](https://github.com/digitaldemocracy2030/kouchou-ai/issues/445), [#417](https://github.com/digitaldemocracy2030/kouchou-ai/issues/417), [#396](https://github.com/digitaldemocracy2030/kouchou-ai/issues/396), [#395](https://github.com/digitaldemocracy2030/kouchou-ai/issues/395), [#380](https://github.com/digitaldemocracy2030/kouchou-ai/issues/380), [#379](https://github.com/digitaldemocracy2030/kouchou-ai/issues/379)

### 14. contributor onboarding と non-code contribution 導線が弱い

役割の切り出し、ソースコード以外の貢献、コミュニティでの試行錯誤支援、AI agent 協働など、プロジェクトにどう関わればよいかの導線がまだ細い。これは採用広報の問題ではなく、**人が入ってきても仕事の切り出し方が見えにくい** ことが問題。[[open-issue-backlog-2026-05-19]]より

関連 issue:
- 解決案の議論: [#517](https://github.com/digitaldemocracy2030/kouchou-ai/issues/517), [#456](https://github.com/digitaldemocracy2030/kouchou-ai/issues/456), [#130](https://github.com/digitaldemocracy2030/kouchou-ai/issues/130), [#398](https://github.com/digitaldemocracy2030/kouchou-ai/issues/398), [#221](https://github.com/digitaldemocracy2030/kouchou-ai/issues/221)

### 15. セキュリティ・公開範囲・乱用対策がまだ完成していない

password 認証、private/unlisted、パブコメ大量投稿対策、個人情報対応など、公開と安全性に関わる問題が散発している。根本には **公開のしやすさと保護の強さの設計がまだ揺れている** ことがある。[[open-decisions]]より

関連 issue:
- 解決案の議論: [#370](https://github.com/digitaldemocracy2030/kouchou-ai/issues/370), [#346](https://github.com/digitaldemocracy2030/kouchou-ai/issues/346), [#345](https://github.com/digitaldemocracy2030/kouchou-ai/issues/345), [#364](https://github.com/digitaldemocracy2030/kouchou-ai/issues/364), [#177](https://github.com/digitaldemocracy2030/kouchou-ai/issues/177), [#503](https://github.com/digitaldemocracy2030/kouchou-ai/issues/503)

## Practical Read

- issue は「困りごとの観測点」と「提案された解決策」に分けて読む
- 前者は比較的そのまま信用し、後者は current `main` に合わせて疑い直す
- issue をそのまま roadmap 項目とみなすより、まずどの問題群に属するかを判定する
- 1 つの問題に複数 issue がぶら下がっている時は、最も current `main` に近い issue だけを active にし、他は参考リンクに落とす
- 逆に 1 issue が複数の問題をまたぐ時は、解決策単位でなく問題単位で分割し直した方がよい

## Open Questions

- この problem list を、`Web UI` / `CLI` / `共通コア` の利用モード別 index にも並べ替えるべきか
- 古い open issue のうち、問題は残るが提案解だけ stale なものをどう close / rewrite していくか

## Updates

- 2026-05-19: 初版作成
- 2026-05-19: 9 月前に解く順として 15 問題を並べ替え、優先理由を追記
- 2026-05-19: 会話中の整理を反映し、「ユーザの困りごと」と「issue 内の提案解」を分けて読む heuristic を明文化
