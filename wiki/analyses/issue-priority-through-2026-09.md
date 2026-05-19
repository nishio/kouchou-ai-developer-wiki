---
type: analysis
summary: 2026-05-19 時点の open issue を 9 月までの開発計画に引き直すと、最優先は `analysis-core` CLI の canonical path 固定と Web/静的公開の事故回避であり、純粋な新機能は後ろ倒しが妥当
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

9 月前の次点は `#833` `#683` `#818` `#820` `#707` `#716` の束で、非専門家向け利用モードの事故を減らすこと。これらは別 issue に見えても、実際には **Web UI / static export の失敗時に、回避不能または原因不明になる** 問題群である。[[open-issues-snapshot-2026-05-19]]より

優先順は次の通り。

- `#833`: remote HTTP / CSP / UUID の current-tree fix
- `#683`: 公開レポート 0 件時の static export failure
- `#707`: provider 判定を誤る API 接続チェック
- `#716`: レポート生成失敗時のエラーログ可視化
- `#818` `#820`: PNG download と CSP 設定ガイド

理由は、`#833` `#683` `#707` は product が「壊れて見える」直接原因で、`#716` `#818` `#820` はその原因把握と運用回避を支えるからである。[[book-release-development-plan-2026-09]]より

### P2. provider / validation 論点を束ね直す

`#707` `#681` `#473` は別々に開いているが、9 月までの計画では **provider ごとの接続チェック設計を 1 つの論点として束ねる** 方がよい。現在の問題は feature 不足というより、OpenAI / Azure / LocalLLM で check path が一貫していないことにある。[[open-issues-snapshot-2026-05-19]]より [[open-decisions]]より

この束ね直しが必要な理由は次の通り。

- `#707` だけ直しても user-provided key や LocalLLM check との整合が残る
- `#681` は user input API key check を求めている
- `#473` は Azure / OpenRouter / LocalLLM を環境確認ページに広げたい話

したがって実装順は `#707` の誤判定修正を先に行い、その上で `#681` `#473` を同じ設計に寄せるのが妥当。[[open-issues-snapshot-2026-05-19]]より

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
- `#833` を CSP / UUID / LocalLLM UX に分けるか判断する
- `#683` の static export fail-fast / no-report behavior を詰める

### 2026-06 〜 2026-07

- `#837` 実装と最低限の integration test
- `#707` 修正と provider check の設計整理
- `#716` の最小版を入れて「失敗しても調べられる」状態にする
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

- `#716` の high priority を P1 に置くか、`#707` と同列の P0.5 に上げるか
- `#833` を 1 issue のまま扱うと review 単位が大きすぎないか
- `#696` を docs issue と product issue に分割した方が実装しやすいか

## Updates

- 2026-05-19: 初版作成
