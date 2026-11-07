---
title: "CodeQL導入の経緯と位置づけ"
type: analysis
summary: "`PR #817` 文脈では、CodeQL は accidental な混入をきっかけに常設の security scan として整理された"
sources:
  - codeql-docs.md
  - pr-813-817-codeql-coderabbit-observation-2026-05-18.md
  - meeting-minutes.md
---

## Short Answer

CodeQL は GitHub の静的解析エンジンで、コードを解析して脆弱性や security quality 上の問題を見つけるためのもの。`kouchou-ai` では `PR #817` の文脈を見る限り、**最初から強い計画性を持って導入したというより、`PR #813` で誤って入った設定を「せっかくなので適切に整えて残す」形で導入された** と読むのが正確。[[codeql-docs]]より [[pr-813-817-codeql-coderabbit-observation-2026-05-18]]より

## What CodeQL Is

- CodeQL は GitHub の code scanning を支える静的解析エンジンで、push / PR / schedule / manual run に載せて継続的に security scan を回せる。[[codeql-docs]]より
- `github/codeql-action` を workflow に置くと、対象言語のコードを解析してセキュリティ上の問題候補を GitHub 上の alert として扱える。[[codeql-docs]]より

## Why It Was Introduced Here

### 直接のきっかけ

`PR #813` の主題は空コメントのフィルタ修正で、CodeQL / CodeRabbit は scope 外の混入だった。PR 本文でも「主題とは無関係」「別PRに分離すべきか検討」と書かれている。[[pr-813-817-codeql-coderabbit-observation-2026-05-18]]より

### 実際の導入判断

`PR #817` では、その accidental な設定追加を撤回するのではなく、以下のように運用しやすい形へ調整している。[[pr-813-817-codeql-coderabbit-observation-2026-05-18]]より

- `main` push と `main` 向け PR で実行
- weekly schedule を追加
- 手動実行を許可
- concurrency で重複実行を抑制
- docs-only 変更では走らないよう `paths-ignore` を追加

この調整内容から逆算すると、導入理由は「コード変更に対して継続的な security scan を掛けたいが、無駄実行は減らしたい」という実務的なものだったと言える。[[pr-813-817-codeql-coderabbit-observation-2026-05-18]]より

## Interpretation

`PR #817` の文脈では、CodeQL 導入は「セキュリティスキャンを新規企画した」というより、**混入した CI 設定を棚卸しした結果、残す価値があると判断して最小限の常設 scan として整えた** もの。したがって、「なぜ導入したか」への短い答えは、**脆弱性検出の自動化のためだが、導入の発火点自体は accidental inclusion だった**。[[codeql-docs]]より [[pr-813-817-codeql-coderabbit-observation-2026-05-18]]より

2026-06-01 定例では、tokoroten から Actions に `node20` / CodeQL deprecated 系の警告が出ていること、Dependabot にも警告があることが共有され、nishio は「これは最優先でやるべき」と反応した。現時点では具体 issue / PR 番号まではこの wiki に固定していないが、CodeQL は一度入れて終わりではなく、action runtime や security alert の保守が必要な運用物として扱うべき状態になっている。[[meeting-minutes]]より

Dependabot alerts は GitHub Security 側の live state であり、main / open PR / issue の観測だけでは取りこぼす。したがって security / dependency 保守では `https://github.com/digitaldemocracy2030/kouchou-ai/security/dependabot` を定期的に確認する。ただし alert の具体的な脆弱性詳細は公開 wiki に転記せず、対応 issue / PR / 優先度判断だけを残すのがよい。

2026-06-02 00:29 JST 時点では、Dependabot alerts に対応する PR [#889](https://github.com/digitaldemocracy2030/kouchou-ai/issues/889) を admin merge した。変更は root `pnpm.overrides` と `pnpm-lock.yaml` の dependency-only PR で、audit / test / build の確認も通している。open PR [#888](https://github.com/digitaldemocracy2030/kouchou-ai/issues/888) / [#863](https://github.com/digitaldemocracy2030/kouchou-ai/issues/863) は `package.json` / `pnpm-lock.yaml` を触っていなかったため、差分上の干渉は小さかった。merge 後の Dependabot open alerts は 19 件から 6 件へ減った。alert の具体的な脆弱性詳細は公開 wiki / PR 本文には転記していない。

## Open Questions

- `#815` の議論で誰がどの論点を出したか
- #889 直後の残り 6 件は当時の snapshot。その後の依存保守は #949 と対応 PR 群へ引き継がれた。現在の未解消 alert と担当・優先度は別途 live 確認が必要（具体的な脆弱性詳細は公開 Wiki に記載しない）。
- Dependabot alerts の確認頻度と担当を、週次確認として固定するか

## Updates

- 2026-05-18: 初版作成
- 2026-06-01: 定例で Actions / CodeQL / Dependabot 警告が最優先扱いになったことを追記。CodeQL を CI に入れた経緯だけでなく、継続保守対象として見る必要が出ている
- 2026-06-01: Dependabot alerts ページを定期観測対象として明記し、公開 wiki には脆弱性詳細を転記しない方針を追記
- 2026-06-02: Dependabot alerts に対応する PR [#889](https://github.com/digitaldemocracy2030/kouchou-ai/issues/889) を admin merge し、open alerts が 19 件から 6 件へ減ったことを追記

- 2026-11-07: Open Questions から除去 — 「merge 後の main に schedule / concurrency / paths-ignore がどのタイミングで入ったか」。schedule / concurrency / paths-ignore は #817 merge後の追加ではなく、2026-03-10 の先行commitで導入されていた。git log -S で各キーを確認。（根拠: kouchou-ai ebfb4ac1f（2026-03-10、.github/workflows/codeql.yml。git log -S schedule: / concurrency: / paths-ignore:））。 ／ Claude の検証（2026-11-07、OQ-0081）: ebfb4ac1f（2026-03-10）は PR #817 自身の commit で、merge 前の main には無かった。3 キーが main に入ったのは #817 の merge（2026-05-18）の時点
- 2026-11-07: Open Questions の現状を更新 — 「PR #889 merge 後に残った Dependabot alerts 6 件の扱いをどう分けるか」。6件は #889直後の観測。その後 #949 と対応PRに保守が引き継がれており現在件数の根拠にはしない。（根拠: 0f2ebe6:wiki/analyses/current-status-2026-10-05.md:78（既存 Updates）；kouchou-ai a97b357c1 / 5357e1fa1（対応PR #1013 / #1157））。
