---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。できるだけやさしい言葉で、直近の実装・調査・運用判断を短く積み上げる"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業を短時間で報告するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「全部の変更履歴」を書くことではなく、**会議で口頭共有したい判断と進み具合だけを残す** こと。詳しい根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連ページへ送る

## 月曜にそのまま読む用

1. `analysis-core` まわりでは、インストールを軽くする整理と、CLI の事前チェック追加を main に入れました。これで最初に触る人がつまずきにくくなっています。[[refactoring-status]]より
2. Web まわりでは、HTTP 環境で壊れていた問題を issue 分割しながら順番に直しました。UUID fallback、CSP、LocalLLM の model 自動取得を別々に main へ入れています。[[issue-priority-through-2026-09]]より
3. production deploy が落ちていた件は、CSP 用の共通ファイルを Docker build に入れ忘れていたのが原因でした。ここは修正済みです。[[source-code]]より
4. 失敗時の調査しやすさも少し改善しました。レポート生成に失敗したとき、admin 画面からエラーログの一部を見られるようにしています。[[pr-852-error-log-visibility-observation-2026-05-22]]より
5. 最近の小さめのバグ修正として、古い `report_status.json` で一覧取得が落ちる件と、散布図の source link をクリックしても開かない件を main へ入れました。[[problem-list-from-open-issues-2026-05-19]]より
6. 運用面では、AI エージェントが issue 着手前に assignee を確認し、自分を assign してから進めるルールを明文化しました。PR や issue の対外文面も、日本語をデフォルトにしています。[[coding-agents]]より

## 次回定例向け下書き

### 1. analysis-core の package/CLI 整理を main へ反映

- `PR #843` で、`analysis-core` の重い依存を extras に分けた。これで base install が軽くなり、使い始めやすくなった。[[analysis-core-extras-pr-scope]]より
- 続けて `PR #844` で、CLI の事前チェックと quickstart を整えた。`#836` と `#837` は close 済みで、最初の失敗を減らす方向に進んでいる。[[refactoring-status]]より

### 2. Web の public-IP HTTP 問題を issue 分割で片付けた

- もともと `#685` に混ざっていた問題を分けて、UUID fallback は `#833 -> PR #847`、CSP は `#846 -> PR #848/#849`、LocalLLM の model 自動取得は `#845 -> PR #850` として順番に main へ入れた。[[issue-priority-through-2026-09]]より
- これで、性質の違う問題を 1 issue にまとめたまま進める状態はかなり減った。今後も、小さめの review しやすい単位で進めやすくなっている。[[open-decisions]]より

### 3. production deploy 失敗を調査し、Docker build context 漏れを修正

- `Azure Deployment` が `Cannot find module '../shared/csp'` で落ちていた。原因は、共通ファイルを Docker build に入れ忘れていたことだった。[[deployment]]より
- `PR #851` で Dockerfile を直し、production deploy の元の落ち方は解消した。会議では「CSP の設計が悪かった」というより、「build に必要なファイルを入れ忘れていた」と説明すると分かりやすい。[[source-code]]より

### 4. AI エージェント運用ルールを明文化した

- reviewer request や admin merge のような、人の判断が必要な操作は、AI が勝手にやらず明示指示がある時だけ行うルールを wiki と `CLAUDE.md` に追記した。[[coding-agents]]より [[contributing]]より
- さらに、issue 実装前に assignee を確認し、着手するなら自分を assign してから進めるルールも追加した。並行開発でぶつからないための整理である。[[coding-agents]]より

### 5. レポート失敗時のエラーログを admin UI で見えるようにした

- `#716 -> PR #852` で、レポート生成に失敗した時に admin 画面からエラーログの一部を見られるようにした。[[pr-852-error-log-visibility-observation-2026-05-22]]より
- これで「失敗したが理由が分からない」という状態が減る。運用しながら原因を追いやすくなったのがポイント。[[coding-agents]]より [[source-code]]より

### 6. legacy status データ由来の一覧取得バグを current tree で潰した

- `#740 -> PR #856` で、古い `report_status.json` に `slug` が無い場合でも、一覧取得で落ちないようにした。[[source-code]]より
- これで admin/public のレポート一覧が、古いデータのせいで `ValidationError` になる直接バグは解消した。細かい契約の論点は残るが、いま再現していた不具合は閉じている。[[open-decisions]]より [[problem-list-from-open-issues-2026-05-19]]より

### 7. 散布図の source link がクリックできない不具合を直した

- `#710 -> PR #857` で、散布図の点をクリックしてもリンク先が開かない問題を修正した。原因は、Plotly の hover modebar が点クリックを邪魔していたことだった。[[source-code]]より
- modebar 自体は残しつつ、クリックを邪魔しないように DOM 側を調整した。見た目はあまり変えずに、期待どおり新しいタブで開ける方向へ直している。[[source-code]]より

## Open Questions

- このページを「常に次回会議向け 1 枚」に保つか、会議ごとに snapshot を切るかはまだ未決
- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-05-21: 初回作成。直近の `analysis-core` / Web UI / deploy / AI 運用ルールの進捗を次回定例向けに要約
- 2026-05-22: 月曜の定例会向けに、もっとやさしい言い方へ調整し、`#740 -> PR #856` と `#710 -> PR #857` まで反映

- 2026-05-22: 進行中: Windows 初回セットアップを塞ぐ `#731 -> draft PR #858` に着手し、`setup_win.bat` の文字コード依存メッセージを ASCII 化、API キー検証の重複を整理、Docker 未起動時の `cmd.exe` 実行確認まで実施。ブランチは `codex/fix-windows-setup-mojibake`。[[source-code]]より [[github-dev-docs]]より
