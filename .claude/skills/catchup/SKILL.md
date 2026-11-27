---
name: catchup
description: 広聴AI の現在地を観測する定期メンテナンス。前回の current-status 以降の本体 main・open PR・Issue・CI・Dependabot・ブラウザ版・Slack・議事録の変化を読み、wiki の current-status と状態を書いているページに反映する。「キャッチアップして」「現状を確認して」「定期メンテ」「current-status を更新して」などで使う。開始は人が決める（自分から始めない）。
---

手順の正本は、この repo の `skills/catchup/SKILL.md`（Codex など他のエージェントとも共有している）。まずそのファイルを読み、その手順どおりに進める。このファイルは Claude Code から名前で呼ぶための入口で、手順はここに書き足さない。

Claude Code で実行する時の補足：

- ログの見出しや「観測範囲」の時刻は、推測で書かずマシンの時計（`TZ=Asia/Tokyo date`）から取る。`clock-timestamps` スキルがあればそれに従う
- 範囲が大きい時（前回から 2 週間以上空いている、open PR が多い）は、始める前に作業量の見込みを人に示す（`usage-budget` スキルがあれば使用量の枠も確かめる）
- PR やコードの読み取りを subagent に任せる時は、`git show origin/main:<path>` で読ませ、`git checkout` を禁じる
