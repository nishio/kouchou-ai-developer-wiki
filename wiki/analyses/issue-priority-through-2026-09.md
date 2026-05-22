---
type: analysis
summary: "2026-05-19 時点の open issue を 9 月までの開発計画に引き直すと、最優先は `analysis-core` CLI の canonical path 固定と Web/静的公開の事故回避であり、純粋な新機能は後ろ倒しが妥当"
sources:
  - problem-list-from-open-issues-2026-05-19.md
  - open-issues-snapshot-2026-05-19.md
  - book-release-development-plan-2026-09.md
  - open-decisions.md
  - refactoring-status.md
---

2026-05-19 時点の open issues を新しい順に読むと、9 月までの優先度はかなり明確に絞れる。最優先は **`analysis-core` CLI の canonical path を使いやすくし、Web / static 公開の事故を減らすこと** であり、アルゴリズム新機能や広い意味での UX 改善はその後でよい。[[open-issues-snapshot-2026-05-19]]より [[book-release-development-plan-2026-09]]より

より土台にある「何が問題なのか」の棚卸しは [[problem-list-from-open-issues-2026-05-19]] に分離した。本ページはその problem list の上に「9 月までにどこから解くか」を重ねた読み物として扱う。[[problem-list-from-open-issues-2026-05-19]]より

## Priority

### P0. `analysis-core` CLI の入口を固定する

9 月前に最優先なのは `#721` を current `analysis-core` 前提に解体した `#836` `#837` を進めること。これは既存の開発計画で言う `P1. v5 の default path を通す` と `P3. セットアップと実行の再現性を固める` に直結する。[[book-release-development-plan-2026-09]]より

- `#836` は current CLI path の正しい使い方を固定する
- `#837` は config / input の preflight validation を入れて失敗を早くする
- `#721` は umbrella として残しつつ、旧 `server/broadlistening/...` 改修に戻さない

ここが曖昧なままだと、新規 contributor も agent も deprecated path に迷い込みやすい。[[refactoring-status]]より

### P1. Web / static 公開の「壊れ方」を減らす

9 月前の次点は `#833` `#818` `#820` `#707` `#716` の束で、非専門家向け利用モードの事故を減らすこと。これらは別 issue に見えても、実際には **Web UI / static export の失敗時に、回避不能または原因不明になる** 問題群である。[[open-issues-snapshot-2026-05-19]]より

2026-05-22 時点の current state を踏まえると、この束のうち `#846` は `PR #848` merge で前進し、`#707` は current main 非再現として close、`#716` も `PR #852` merge で close 済みである。したがって active な残論点は、主に `#818` `#820` と、provider UX 側では `#681` へ寄る。[[github-dev-docs]]より [[source-code]]より [[pr-852-error-log-visibility-observation-2026-05-22]]より

優先順は次の通り。

- `#833`: admin create/reuse flow の UUID fallback
- `#846`: CSP / remote asset policy の current-tree fix
- `#707`: provider 判定を誤る API 接続チェック
- `#818` `#820`: PNG download と CSP 設定ガイド

理由は、`#833` / `#846` / `#707` は product が「壊れて見える」直接原因で、`#716` `#818` `#820` はその原因把握と運用回避を支えるからである。`#716` 自体は `PR #852` により current `main` へ入ったため、以後は active 実装候補ではなく **着地済みの改善** として扱う。[[book-release-development-plan-2026-09]]より [[pr-852-error-log-visibility-observation-2026-05-22]]より

### P2. provider / validation 論点を束ね直す

`#707` `#681` `#473` は別々に開いているが、9 月までの計画では **provider ごとの接続チェック設計を 1 つの論点として束ねる** 方がよい。現在の問題は feature 不足というより、OpenAI / Azure / LocalLLM で check path が一貫していないことにある。[[open-issues-snapshot-2026-05-19]]より [[open-decisions]]より

この束ね直しが必要な理由は次の通り。

- `#707` だけ直しても user-provided key や LocalLLM check との整合が残る
- `#681` は user input API key check を求めている
- `#473` は Azure / OpenRouter / LocalLLM を環境確認ページに広げたい話

ただし 2026-05-21 の再確認では `#707` の元症状は current main で非再現として close されたため、active な実装順としては **`#681` など未解決の provider UX / validation issue を同じ設計へ寄せる** 読みに更新してよい。[[open-issues-snapshot-2026-05-19]]より [[github-dev-docs]]より

### P3. output validation は即実装より設計判定を先にする

`#838` は直近 issue の中では優先度を一段落としてよい。理由は、出力 artifact validation は重要でも、**runtime feature なのか test infrastructure なのかがまだ決まっていない** からである。[[open-issues-snapshot-2026-05-19]]より

9 月前に必要なのは、まず `#837` で preflight を固めること。`#838` は次のどれかに絞ってから着手した方が安全。

- end-user CLI の fail-fast
- maintainer 向け diagnostic command
- CI / integration test helper

曖昧なまま入れると、旧 `#721` のように scope が膨らみやすい。[[open-decisions]]より

### P4. 既知だが current 再現性が弱い問題は後ろへ送る

`#799` React dev overlay crash のように、報告自体は理解できても current `main` での再現性が弱いものは、9 月前の主戦場からは外してよい。wiki 側観測では clean install の current `main` では非再現だった。[[open-issues-snapshot-2026-05-19]]より

同様に、`#690` `ts-node-dev` 置換のような保守改善も重要だが、9 月前の default path 安定化に直接効くわけではない。[[open-issues-snapshot-2026-05-19]]より

### P5. 新機能は「9 月の受け皿作り」に効くもの以外は後ろ倒し

`#679` 任意カテゴリー分類、`#648` 一括編集、`#641` 完了通知、`#638` 濃い意見ビュー改善、`#809` UMAP 並列化などは、いずれも価値はあるが、9 月までの主目標である **回帰保証付き v5 移行** を進める主タスクではない。[[book-release-development-plan-2026-09]]より

例外として前倒し候補になり得るのは `#696` で、これは機能追加というより **誤読を減らす説明責務** に属する。書籍公開で新規流入が増える前提を踏まえると、docs / in-product warning / website copy のどれかで先に着手する価値がある。[[open-issues-snapshot-2026-05-19]]より [[book-release-development-plan-2026-09]]より

## Suggested Order

### 2026-05 後半

- `#836` を先に進め、canonical CLI path の usage doc を固定する
- `#837` の scope を config / input preflight に絞って実装計画を切る
- `#845` を先に進め、`#848` merge 後に残った LocalLLM UX の穴を埋める
- static export の残論点は `#683` の build bug ではなく、no-report 時の期待挙動や周辺 UX として切り分ける

### 2026-06 〜 2026-07

- `#837` 実装と最低限の integration test
- `#681` を含む provider check / user-provided key UX の設計整理
- `#818` `#820` を product fix と doc fix に分けて着地させる

### 2026-08

- `#838` を runtime feature にするか test helper にするか最終判断
- `#696` の注意書き・説明責務を docs / product に反映
- それでも余力があれば `#681` など周辺の provider UX を広げる

## Defer

9 月前は次を後ろ倒し候補として扱うのが妥当。

- `#809` UMAP 並列化
- `#679` 任意カテゴリー分類
- `#648` 一括編集
- `#641` 完了通知
- `#690` `ts-node-dev` 置換

これらは current path の安定性よりも、次段の拡張性や UX 向上に属する。[[book-release-development-plan-2026-09]]より

## Open Questions

- `#833` を 1 issue のまま扱うと review 単位が大きすぎないか
- `#696` を docs issue と product issue に分割した方が実装しやすいか

## Updates

- 2026-05-22: `PR #856` merge と `#740` close を反映。artifact/schema 論点のうち、legacy `report_status.json` の `slug` 欠落で一覧取得が落ちる直接バグは `main@fba8e81` で解消済みとなった。[[source-code]]より [[github-dev-docs]]より
- 2026-05-19: 初版作成
- 2026-05-21: current `main@5d591ef` では `#683` の元症状（`opengraph-image.png` の `generateStaticParams()` 欠落 build error）は再現せず、説明的 fail-fast に置き換わっていることを反映
- 2026-05-21: `#833` を UUID slice に絞り、CSP / remote asset policy を `#846`、LocalLLM auto-fetch UX を `#845` へ分割した current state を反映
- 2026-05-21: `PR #848` merge による `#846` 前進と、`#707` close を反映し、P1 / P2 の active 論点を `#845` `#716` `#818` `#820` `#681` 側へ寄せた
- 2026-05-22: `PR #852` merge と `#716` close を反映し、P1 の active 実装候補から外した
