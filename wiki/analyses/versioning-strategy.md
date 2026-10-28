---
title: "v4凍結・v5 plugin化のリリース戦略"
name: versioning-strategy
summary: "2025-12-13 に決めた v4 凍結 / v5 plugin 化のリリース戦略（書籍出版とのリスク調整）と、その後の実際。リファクタは main 上で段階的に進み、v4.1.0 を 2026-10-13 に main から発行、v5 は 2026-10-21 時点で未リリース"
type: analysis
sources:
  - meeting-minutes.md
  - github-dev-docs.md
  - source-code.md
  - kouchou-ai-direction-2025-12-06.md
  - kouchou-ai-direction-2-2025-12-13.md
  - kensuzuki-broad-listening-insight-types-2025-11-29.md
---

## 決定事項（[[meeting-minutes]] 2025-12-13）

「広聴 AI の方向性について 第 2 回」で確認：

- **書籍出版までの間、大規模リファクタは入れない**
- **書籍出版時の `main` を stable v4.x としてタグ付け**
- **v5.0（[[plugin-system]] 本格化）は 2026 年 6 月目標**

これは 2025-12-13 時点の決定。実際には v4.0.0 は書籍出版を待たずに 2025-12 末に打たれ、大リファクタも 2026-01 から main 上で進んだ（下の「その後の実際」）。

## 動機

- 書籍出版（[[broad-listening-book]]）と連動するコード安定性が必要
- 大規模リファクタは安定性のリスクが大きい
- 「互換性を保ちたい vs 新機能を実験したい」のジレンマを、**バージョン軸の分割** で吸収

この判断は 2025-12-13 に突然出たものではない。[[kouchou-ai-direction-2025-12-06]] では、鈴木健ブログ [[kensuzuki-broad-listening-insight-types-2025-11-29]] を踏まえて「ブロードリスニングは用途ごとに欲しいインサイトが違う」「現行散布図方式はアジェンダ発見には有効だが万能ではない」「GUI ノードエディタより config の方が現実的」という問題設定が共有された。続く [[kouchou-ai-direction-2-2025-12-13]] では、現行広聴AIを stable に保ちながら次世代探索を別軸へ出す 4 番案が実務的な落とし所として固まっている。[[kouchou-ai-direction-2025-12-06]]より [[kouchou-ai-direction-2-2025-12-13]]より

## v4.0.0 リリース

2025-12-27（UTC。JST では 12-28 の 0 時台）に [[ohki-shingo]] が annotated tag を作成し、GitHub release を公開した。議事メモでは 2025-12-29 の回の共有事項として記録されているが（[[meeting-minutes]]）、日付は GitHub の tag / release に合わせている。[[github-dev-docs]]より

## v4.1.0 リリース（2026-10-13）

2026-10-13 に [[nishio]] が main の `6ad727ee`（PR [#1001](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1001) の merge commit）にタグを打ち、release を公開した。v4.0.0 以降の約 160 PR をまとめたマイナーリリースで、v4 用の保守ブランチではなく main から直接切っている。内容は [[kouchou-ai-v4-1-0-release-2026-10]]、版の切り方を決めた経緯は [[kouchou-ai-docs-improvement-roadmap-2026-10-13]] の Updates（バージョン方針の項）を参照。本体は `vMAJOR.MINOR.PATCH` の release tag で版を切り、`analysis-core` は `analysis-core-vX.Y.Z` の別系統で版を切る。[[github-dev-docs]]より

## その後の実際（2026-10-21 時点）

- v4.0.0 は「書籍出版時の main」ではなく、2025-12 末の main に打たれた
- 2026-01-19 の時点では、大リファクタ（`packages/analysis-core` の切り出し、PyPI 登録など）は refactoring ブランチ上で進んでおり、PR [#746](https://github.com/digitaldemocracy2030/kouchou-ai/issues/746) で 2026-01-23 に main に入った。Web UI を壊さないまま CLI 版を並行させる段階移行で、2026-05-20 に Web UI も analysis-core を使う形に切り替え、2026-05-23 の旧コード掃除を経て 2026-05-24 に完了した。[[meeting-minutes]]より [[refactoring-status]]より
- v4.1.0 はこのリファクタを含めて main から発行された。v4 用の保守ブランチは無い
- v5.0 は未リリースで、最新タグは v4.1.0。[[github-dev-docs]]より

## v5.0 の中身（想定）

[[plugin-system]] 参照：

- 入力／解析／可視化が 3 軸 plugin 化
- `pip install` で CLI / Python import で使える形（PyPI の配布名は `kouchou-ai-analysis-core`。[[kouchou-ai]] の「4 つの配布形態」節）
- CLI quickstart / import quickstart / plugin guide ドキュメント整備
- 旧アルゴリズムは「デフォルト」、新規は「オプションプラグイン」（[[meeting-minutes]] 2026-02-09）

## リファクタの実行戦略 — 別リポジトリ案は採用されなかった

[[meeting-minutes]] 2025-10-08 で [[nishio]]：

> 今のコードがあちこち動かなくなると思うので、今のリポジトリで開発するより、**リポジトリ自体を複製して必要なコードだけ残して削って開発する** といい

= [[talk-to-the-city|TTTC]] からの kouchou-ai フォークと同じ「drastic 変更は別リポジトリ」パターン。

**実際の運用は別リポジトリではなく main 上の Phase 段階移行** だった。旧コードに `DeprecationWarning` を貼って共存させながら `apps/` → `packages/analysis-core/` への canonical 移行を Phase 単位で進め、2026-05-23 に旧コードを掃除して 2026-05-24 に完了した。詳細は [[refactoring-status]]。

`main@3809a7a` を見る限り、`analysis-core` パッケージ、workflow engine、frontend 側の chart plugin 基盤、レポート再利用機能など、**「v5 で入るはずだったもの」のかなりの部分は既に in-tree**。したがって現在の論点は「v5 のコードが存在するか」よりも、**どこまでを stable / default / supported と見なすか** に寄っている。

## Open Questions

- v5 をいつ・どの条件で切るかは未定。2026-06 の目標は達成されず、2026-10-21 時点の最新タグは v4.1.0
- v4.x はこれまで main から直接タグを打っており、保守ブランチは無い。v5 で main を分岐させる場合に、v4 系へのバックポートをどう扱うか
- マイナー / メジャーの切り方の基準は明文化されていない（[[kouchou-ai-v4-1-0-release-2026-10]] の Open Questions と同じ論点）

書籍リリースを 2026-09 ごろと見込んだ場合の具体的な開発優先順位案は [[book-release-development-plan-2026-09]] に整理した。[[meeting-minutes]]より [[refactoring-status]]より

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を参照し、「v5 は未着手の未来機能」ではなく main にかなり流入済みだと補足
- 2026-05-18: 2026-09 ごろの書籍リリース前提での実務計画ページ [[book-release-development-plan-2026-09]] への導線を追加
- 2026-05-25: 2025-12-06 / 2025-12-13 の方向性メモと、出発点になった鈴木健ブログを source として分離し、v4 / v5 分離判断の前史を補強
- 2026-10-21: GitHub の tag / release と照合し、v4.0.0 の日付を 2025-12-27 に訂正。v4.1.0 の節と「その後の実際」を足し、リファクタ完了と Open Questions を現状に合わせ、[[kouchou-ai]] への見出しリンクと PyPI の配布名を直した
- 2026-10-29: v4.2.0（2026-10-26、セキュリティ修正を含む）の後、v4.2.1 は出さないと nishio が決めた（2026-10-28）。[#1149](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1149)〜[#1152](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1152) などの修正は次のリリースに入る。この repo では `v*` のタグはすべて GitHub Release と対になっていて（v2.0.1 のようなパッチ版も同じ）、本体の版番号はタグにしか無い（`package.json` などは 0.1.0 のまま）。タグをきっかけに動く workflow は `analysis-core-v*`（PyPI 公開）だけなので、本体のタグだけを打っても自動では何も起きないが、説明のない版ができるので、タグを打つならリリースも出す
