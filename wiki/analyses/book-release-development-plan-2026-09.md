---
name: book-release-development-plan-2026-09
summary: "2026-09 ごろの書籍リリースを前提にした開発計画案 — v4 回帰をテストで保証しつつ、発展性の高い v5 へ移行する"
type: analysis
sources:
  - versioning-strategy.md
  - refactoring-status.md
  - open-decisions.md
  - slack-design-intents-2025-q4.md
  - meeting-minutes.md
  - pypi-auto-release-requirements.md
---

本ページは、この問いで与えられた **「書籍リリースは 2026-09 ごろ」** という前提のもとで、[[kouchou-ai]] の開発計画を整理したもの。  
その後の追加前提として、**書籍で広聴AIの使い方自体を紹介することはしない** が、**書籍公開のタイミングで新規流入は見込まれる**、かつ **その人たちがつまずきにくく、contribute しやすい地盤作りは必要** と整理された。  
したがって優先すべきなのは、**stable v4 系を固定保存すること** でも、**v5 を無防備に前倒しすること** でもない。  
目標は、**v4 の既存機能が壊れていないことをテストで保証しつつ、2026-09 までにより発展性の高い v5 へ移行すること** である。  
受け皿整備や contribution 導線整備も、この **「回帰保証付き移行」** を成立させるための土台として扱う。[[versioning-strategy]]より [[slack-design-intents-2025-q4]]より [[testing]]より

## Planning Principle

### 1. 9月までの主目標は「v4 回帰を防ぎながら v5 へ移行すること」

既存の方針では「書籍出版まで大規模リファクタを抑える」「出版時の `main` を stable v4.x として扱う」とされていた。[[versioning-strategy]]より  
ただし本ページでは、その前提をそのまま踏襲するのではなく、**書籍で使い方を紹介しないなら、むしろ 9 月までを v5 移行の最後の大きなチャンスと見なす** 立場を取る。  
したがって 2026-09 までの計画は、**v4 を温存する計画** でも **v5 を一気に差し替える計画** でもなく、**v4 相当の挙動をテストで固定しながら、v5 を main の中心へ押し上げる計画** として組む。

### 2. v5 系コードは default 化まで前進させるが、v4 回帰テストをガードレールにする

`packages/analysis-core/`、plugin infrastructure、workflow engine、frontend の chart plugin 基盤など、v5 的な部品は既に main に多く入っている。一方で `run_workflow()` は dormant で、plugin システムは production default になっていない。[[refactoring-status]]より  
この状態は「未来の理想像」ではなく、**途中まで入った v5 が宙ぶらりんで残っている状態** とも読める。  
したがって 9 月までの方針は、**v5 を補助線として温存する** のではなく、**main に入っている v5 系部品をつなぎ込み、default path として安定化させる** 方向に寄せるべきである。  
ただしその際、`v4 で出来ていたこと` が落ちていないかを unit / integration / E2E で継続確認できる状態を先に作らないと、移行は単なる置換事故になる。[[testing]]より

### 3. テスト整備は「v5 移行を成立させるための主タスク」

未着地論点の中では、「未定」より「方針決定済み・未着手」が多い。[[open-decisions]]より  
書籍前の期間は新規の大論争を増やすより、**v5 移行の障害になる既知の不整合・運用不足・テスト不足・ドキュメント不足を減らす** 方が効く。  
特にテスト整備は補助線ではなく、**v5 移行を正当化するための主タスク** である。

## 9月までの優先計画

### P0. v5 を何として出すかを先に固定する

最優先は、9 月時点で **何を v5 の本体として出すのか** を固定すること。  
ここが曖昧なままでは、受け皿整備も docs 整理も全部ぶれる。

- どこまでを `v5` と呼ぶかを固定する
- `main` 上で support する default 実行経路を明文化する
- deprecated な旧実行経路を、互換用に残すのか、非推奨として外すのか決める
- plugin / workflow / capability のどこまでを 9 月前に support するかを決める

現状は canonical 実装が `packages/analysis-core/` に移っている一方、旧 `apps/api/broadlistening/pipeline/` も shim として残っており、古い手順で動いてしまう。[[refactoring-status]]より  
したがって書籍前には **「どの実行経路を v5 の正規経路として前に出すか」** を 1 本に絞る必要がある。

### P1. v5 の default path を通す

`run_workflow()` が dormant、plugin system が production default ではない、という現状を温存すると、v5 はいつまでも「入っているが使われない」状態のまま残る。[[refactoring-status]]より  
したがって 9 月までの中核課題は、**v5 の execution path を main の正規経路に押し上げること** である。

- `run_workflow()` を default path 候補として検証する
- plugin dispatch 前提で既存ステップ互換性を確認する
- API / CLI / static output から v5 path を通せるようにする
- v4 shim に依存している経路を洗い出す

ここが進まない限り、他の v5 議論は doc-only のまま残る。

### P2. v4 回帰を検知するテスト帯を先に作る

`v5` へ移行したいなら、その前提として **「どこまでが v4 の守るべき機能か」** をテストに落とす必要がある。  
ここを曖昧にしたまま進めると、「移行したが何が壊れたか分からない」状態になる。

- v4 の主要ユースケースを列挙する
- API / CLI / static output / viewer のうち、回帰が困る経路を優先順位付きで固定する
- unit test だけでなく integration / E2E で「v4 で出来ていたこと」を残す
- v5 path と v4 相当結果の差分を比較できるテストを整える

既存の `analysis-core` unit / pipeline integration / frontend test / Playwright E2E を、**v5 移行時の回帰検知帯** として再設計するのが重要。[[testing]]より [[refactoring-status]]より

### P3. セットアップと実行の再現性を固める

新規流入で最も困るのは、興味を持った人が最初のセットアップや最初の実行で詰まること。[[slack-design-intents-2025-q4]]より  
ただしここでは、**v4 の再現性を検証できること** と **v5 default path の再現性** の両方を優先する。

具体的には：

- local dev setup の最短経路を 1 つ明示する
- CLI の既知バグ修正
- static HTML 出力まわりの経路整理
- `public-viewer` の build / requirements 判定の安定化
- E2E または最小統合テストで「v4 相当機能が保たれたまま v5 path で 1 回動かす」導線を毎回検証できるようにする

`--without-html` / `--skip-interaction` の argparse 問題、Python 直接静的 HTML 出力の open PR、viewer 側 capability 判定の計画などは、まさにこのレイヤに属する。[[refactoring-status]]より [[open-decisions]]より

### P4. v5 周辺の未完了部をまとめて前進させる

9 月までにやるべきなのは、v5 要素を小出しに温存することではなく、**main に既に存在する v5 系の未完了部をまとめて前進させること** である。

- plugin system の production 接続
- workflow engine の default 化判断
- capability / requirements 判定の整合
- frontend plugin 基盤と backend 側の説明責務整理
- Jigsaw 系など次の分析モードを受けるための土台整理

ただし、何でも同時に入れるのではなく、**9 月までに一貫した v5 ストーリーになる順番** で進める。

### P5. contribution 導線を整える

新規流入者にとっては、使い始めること以上に **どこから貢献すればよいか分からない** ことが大きな離脱点になる。[[contributing]]より  
書籍前に優先度が高いのは、PR レビュー基準の完全定義よりも、**初回コントリビュータが迷わない導線** を作ること。

- `CONTRIBUTING.md` / wiki 上で「最初の 1 issue の選び方」を明示する
- setup 済みなら再現しやすい小さめの課題群を見える化する
- open PR / issue / docs ギャップの見方をまとめる
- AI agent / 人間 contributor のどちらでも入りやすい最低限の作法を揃える

とくに現状は「Issue を立てる → 実装計画を投稿 → 反応待ち」という基本フローはあるが、**初回貢献者がどの粒度の仕事を選べばよいか** はまだ薄い。[[contributing]]より

### P6. リリース運用を v5 前提に組み直す

`analysis-core` は PyPI 公開済みだが、自動 publish は未整備で、`CHANGELOG.md` も無い。[[refactoring-status]]より [[open-decisions]]より  
v5 を主戦場にするなら、release 運用も **v5 を出す前提** で組み直す必要がある。

- `analysis-core-v*` tag 規約ベースで release 手順を固定
- package 専用 test/lint を release 前提で整える
- 最低限の `CHANGELOG.md` を作る
- 手動リリース手順の抜け漏れを潰す
- v4 回帰テストを release gate に含める

ここは新機能ではないが、v5 を出した後のメンテナンス負荷を大きく下げる。[[versioning-strategy]]より [[pypi-auto-release-requirements]]より

### P7. open PR を「v5 完成」と「v4 回帰防止」に効くかで選別して着地させる

main に未反映の open PR 群を、「9 月前に必要」「9 月後でよい」で仕分ける必要がある。[[open-decisions]]より  
基準は **v5 default path に効くか / v4 回帰を減らすか / v5 の安定化に効くか / release 後の運用事故を減らすか**。

9 月前に優先しやすい候補：

- static HTML 出力の簡素化
- Local LLM の接続安定化
- viewer build / capability 判定の整合
- doc-only ではなく、v5 path を前に進める実装

逆に、v5 と無関係な周辺改善は、緊急性が低ければ後ろ倒しでよい。

### P8. docs を「将来像」から「回帰保証付き v5 移行の構造」へ組み替える

2025 4Q の議論では、現行 UI / UX を保つ安定版と、plugin 化された次世代系を時間分離する方針が明確だった。[[slack-design-intents-2025-q4]]より  
しかし main には将来計画と現状実装が混在している。[[refactoring-status]]より

そのため書籍前は docs も次の形に寄せるべき：

- v5 の正規経路を最初に書く
- 「この repo は何が current で、何が legacy か」を先頭で明示する
- 初見の人向けに「読む順番」と「やる順番」を分ける
- 「v4 互換を何で保証しているか」を明示する
- 未完の部分は「experimental」と明示する
- plugin / workflow engine / YAML workflow は roadmap と current state を分けつつ、current の v5 path を前に出す

これはコード変更量の割に、新規流入者とコントリビュータ双方の混乱を大きく減らせる。

## 後回しでよいもの

以下は重要だが、v5 を main に押し上げる観点では優先度を一段落としてよい。

- YAML workflow の本実装
- 可視化 plugin の Python 側統一設計
- DB 導入や SaaS ホスト戦略のような、技術より運営体制に依存する論点

これらは不確実性が高いか、v5 の default path 確立と v4 回帰保証に直結しにくい。[[open-decisions]]より [[refactoring-status]]より

## 提案スケジュール

### 2026-05 後半 〜 2026-06

- v5 の正規経路を決める
- v4 の守るべき機能をテスト観点で固定する
- open PR / 既知不具合を「v5 完成に効くか」で triage する
- workflow / plugin / capability の接続方針を固める
- docs 上で current v5 path と legacy path を分離する

### 2026-07

- CLI / API / static output で v5 path を通す
- v4 回帰テストと v5 path テストを並走できるようにする
- contribution 導線と release 手順を v5 前提で更新する
- 主要 open PR を取り込みつつ不整合を潰す

### 2026-08

- v5 path で入口からセットアップまで通し検証
- v4 相当機能が残っていることを release 候補で確認する
- legacy 経路との不整合が致命傷にならないか確認する
- 不具合修正中心の freeze に入る
- v5 を stable として出す tag / branch の打ち方を確定する

### 2026-09（リリース前後）

- 出版時 `main` または対応 branch を stable v5 系として扱う
- 流入後の問い合わせで頻出しそうな FAQ / troubleshooting を補強する
- v5 の default 化後に残った未完了部を次期課題へ回す

## 実務上のチェックリスト

- v5 の正規経路が決まっているか
- v4 の守るべき機能がテストとして固定されているか
- v5 path を CI か手順書で再現確認できるか
- 初回コントリビュータ向けの小さな課題群が見える化されているか
- current v5 path と legacy path が docs 上で混ざっていないか
- release 手順が個人依存になっていないか
- open PR のうち、書籍前にマージすべきものと凍結すべきものが整理されているか

## Open Questions

- 出版時点の stable を `main` tag で切るのか、branch を分けるのか
- open PR #825 / #824 / #827 のうち、どこまでを 9 月前の対象に含めるか
- `run_workflow()` / plugin system / capability 判定のどこまでを 9 月前に default 化できるか
- v4 互換として最低限どこまでを保証対象にするか
- legacy path をいつまで残すか

## Updates

- 2026-05-19: open issue を新しい順に読み直した優先度案として [[issue-priority-through-2026-09]] を追加。`analysis-core` CLI の canonical path 固定と Web/static 公開の事故回避を、9 月前の issue triage の最優先と読む補助線を置いた。[[issue-priority-through-2026-09]]より
- 2026-05-18: 初回作成。ユーザから与えられた「2026-09 ごろ書籍リリース」前提で、既存 Wiki の観測を開発計画に再編
- 2026-05-18: 「書籍で使い方を紹介しない」前提を反映し、計画の軸を操作導線固定から流入者の受け皿整備・contribution 地盤整備へ修正
- 2026-05-18: 「v5 は間に合う範囲なら入れる」前提を反映し、default 化と限定投入を分けて整理
- 2026-05-18: 「v5 を主戦場として入れ切ってから安定化したい」前提を反映し、v5 完成と安定化を中心に全面修正
- 2026-05-18: 「v4 の既存機能が壊れていないことをテストで保証しつつ v5 へ移行する」前提を反映し、回帰検知帯の整備を主タスクとして追加
