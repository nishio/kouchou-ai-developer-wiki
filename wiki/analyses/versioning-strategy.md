---
name: versioning-strategy
summary: "v4 凍結 / v5 plugin 化のリリース戦略 — 書籍出版とのリスク調整"
type: analysis
sources:
  - meeting-minutes.md
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

## 動機

- 書籍出版（[[broad-listening-book]]）と連動するコード安定性が必要
- 大規模リファクタは安定性のリスクが大きい
- 「互換性を保ちたい vs 新機能を実験したい」のジレンマを、**バージョン軸の分割** で吸収

この判断は 2025-12-13 に突然出たものではない。[[kouchou-ai-direction-2025-12-06]] では、鈴木健ブログ [[kensuzuki-broad-listening-insight-types-2025-11-29]] を踏まえて「ブロードリスニングは用途ごとに欲しいインサイトが違う」「現行散布図方式はアジェンダ発見には有効だが万能ではない」「GUI ノードエディタより config の方が現実的」という問題設定が共有された。続く [[kouchou-ai-direction-2-2025-12-13]] では、現行広聴AIを stable に保ちながら次世代探索を別軸へ出す 4 番案が実務的な落とし所として固まっている。[[kouchou-ai-direction-2025-12-06]]より [[kouchou-ai-direction-2-2025-12-13]]より

## v4.0.0 リリース

2025-12-29、[[ohki-shingo]] がタグ。

## v5.0 の中身（想定）

[[plugin-system]] 参照：

- 入力／解析／可視化が 3 軸 plugin 化
- `pip install kouchou-ai` で CLI / Python import で使える形（[[kouchou-ai#4-meeting-minutes-2025-10-08]]）
- CLI quickstart / import quickstart / plugin guide ドキュメント整備
- 旧アルゴリズムは「デフォルト」、新規は「オプションプラグイン」（[[meeting-minutes]] 2026-02-09）

## リファクタの実行戦略 — 別リポジトリ案は採用されなかった

[[meeting-minutes]] 2025-10-08 で [[nishio]]：

> 今のコードがあちこち動かなくなると思うので、今のリポジトリで開発するより、**リポジトリ自体を複製して必要なコードだけ残して削って開発する** といい

= [[talk-to-the-city|TTTC]] からの kouchou-ai フォークと同じ「drastic 変更は別リポジトリ」パターン。

**実際の運用は別リポジトリではなく main 上の Phase 段階移行** だった。旧コードに `DeprecationWarning` を貼って共存させ、`apps/` → `packages/analysis-core/` への canonical 移行を Phase 単位で進めている。詳細は [[refactoring-status]]。

`main@3809a7a` を見る限り、`analysis-core` パッケージ、workflow engine、frontend 側の chart plugin 基盤、レポート再利用機能など、**「v5 で入るはずだったもの」のかなりの部分は既に in-tree**。したがって現在の論点は「v5 のコードが存在するか」よりも、**どこまでを stable / default / supported と見なすか** に寄っている。

## Open Questions

- v4 → v5 のタグ／ブランチ運用は具体化されていない
- リリース時期 2026-06 が現実に間に合うか未確認
- v4 系へのバックポート方針

書籍リリースを 2026-09 ごろと見込んだ場合の具体的な開発優先順位案は [[book-release-development-plan-2026-09]] に整理した。[[meeting-minutes]]より [[refactoring-status]]より

## Updates

- 2026-05-17: 初回作成
- 2026-05-17: `main@3809a7a` を参照し、「v5 は未着手の未来機能」ではなく main にかなり流入済みだと補足
- 2026-05-18: 2026-09 ごろの書籍リリース前提での実務計画ページ [[book-release-development-plan-2026-09]] への導線を追加
- 2026-05-25: 2025-12-06 / 2025-12-13 の方向性メモと、出発点になった鈴木健ブログを source として分離し、v4 / v5 分離判断の前史を補強
