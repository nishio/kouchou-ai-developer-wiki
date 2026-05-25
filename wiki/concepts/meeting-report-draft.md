---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。できるだけやさしい言葉で、直近の実装・調査・運用判断を短く積み上げる"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
  - analysis-core-web-ui-separation-decision-2026-05-23.md
  - report-html-non-web-canonical-decision-2026-05-23.md
  - slack-public-ui-requirements-2026-05-23.md
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
7. 長期論点として、LLM grouping 系の第2分析モードは自然な散布図を出しにくい一方、散布図はまだユーザ価値が強い、という緊張関係を整理しました。短期は散布図互換の暫定案でつなぎ、長期は散布図必須の前提を外す、という二段構えで考えるのがよさそうです。[[strategic-development-order-2026-05-23]]より [[jigsaw-sensemaker-history|LLM grouping 系の背景整理]]より
8. テスト面では、`analysis-core` 単体の e2e だけでなく、API が `analysis_core` を subprocess で起動する継ぎ目を手元で本当に踏める smoke test も追加しました。少なくとも merge 前に、その境界を 1 回は人間が踏める状態になっています。[[testing]]より

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

### 8. 長期論点として、LLM grouping 系第2モードと散布図前提の衝突を整理した

- issue の優先順だけではなく、`kouchou-ai` を「共通実験基盤 / 製品導線 / 探索枝」の 3 層 platform として見直した。そのうえで、次に考えるべき中心問題は bugfix の順番より、「散布図を前提にしない analysis mode でも product が成立する capability contract を作れるか」だと整理した。[[strategic-development-order-2026-05-23]]より
- LLM grouping 系の第2モードは自然な散布図を出しにくい。一方で散布図はユーザ価値が強いので、短期は embedding 併用で散布図互換に載せ、長期は散布図必須ビューをやめる、という二段構えを作業仮説として明文化した。[[jigsaw-sensemaker-history|LLM grouping 系の背景整理]]より [[strategic-development-order-2026-05-23]]より

### 9. API -> subprocess -> analysis-core の継ぎ目に手元 smoke test を足し、通常フローの path バグも直した

- これまで `analysis-core` 単体の e2e と、API `report_launcher` の mock ベース service test はあったが、FastAPI 側が本当に `python -m analysis_core` を起動して通常フローを最後まで通るかを踏む最小テストが無かった。そこで `apps/api/tests/manual/report_launcher_subprocess_smoke.py` を拡張し、`execute_aggregation()` だけでなく `launch_report_generation()` から full flow を本物の subprocess で起動し、`hierarchical_result.json`・`hierarchical_status.json`・`report_status.json` 更新まで手元で確認できるようにした。[[testing]]より [[source-code]]より
- この手元実行で、workflow plugin が `--input-dir` / `--output-dir` を legacy step に渡しておらず、通常フローが相対 `inputs/` / `outputs/` を見に行くバグも見つかった。`analysis_core.plugins.builtin.*` 側で path を受け渡すよう修正し、manual smoke と既存 `report_launcher` test まで通し直している。[[testing]]より [[source-code]]より
- その後、plugin ごとに重複していた legacy config 組み立てを `_legacy_config.py` に寄せ、`analysis.extraction` が解決済みの input/output path を legacy step に渡す regression test も追加した。バグを直しただけでなく、同じ種類の path plumbing がまた散らばらないようにしている。[[testing]]より [[source-code]]より

### 10. `report.html` は Web canonical にしない判断と、WebUI / core 分離の設計説明を wiki に固定した

- 新規 [[analysis-core-and-web-ui]] を作り、「CLI だけでは一般利用者に重いので WebUI で包んだが、今度は研究用途に重くなったので core を切り出し、WebUI はそれを使う consumer に戻した」という設計判断を、歴史ページとは別にまとめた。[[analysis-core-web-ui-separation-decision-2026-05-23]]より
- `report.html` は CLI / coding agent 向けの自己完結 **観察用HTML** で、Web の canonical path はこれまでどおり `hierarchical_result.json` + `public-viewer` とする。open question ではなく明示判断として整理し直した。[[usage-modes]]より [[report-html-non-web-canonical-decision-2026-05-23]]より
- これで `API が --without-html 固定なのは未整合なのか` という混線を減らせる。今後の Web 側の議論は HTML 昇格の是非ではなく、JSON / viewer 契約前提で進めればよい。[[cli]]より [[refactoring-status]]より

### 11. legacy pipeline cleanup を main へ入れ、refactoring を done 扱いにできる状態にした

- `PR #865` で、`apps/api/broadlistening/pipeline/` に残っていた旧 Python 実装と source tree 上の refactoring phase docs を除去した。current tree では `analysis-core` / workflow 側だけが canonical になっている。[[source-code]]より [[refactoring-status]]より
- 途中で `Server Tests` が `analysis_core` 未 install で落ちたので CI workflow も直し、checks success まで確認して admin merge した。これで、これまで refactoring 未完の根拠だった Phase 8 が main から消えた。[[source-code]]より [[github-dev-docs]]より

### 12. nasuka さんの過去発言から、実利用 loop の不足を整理した

- [[nasuka]] さんの過去発言を読み直すと、Azure 永続化、限定公開、手動編集、再利用、抽出品質、CI、運用ルールなど、実ユーザーが触った時に信頼を失う箇所をかなり早く見ていたことが分かった。[[nasuka-statements-retrospective-2026-05-25]]より
- 今の `analysis-core` / LLM grouping 系実験にもつながる示唆として、失敗入力・失敗出力を残し、同一条件で比較し、人間が直した結果を prompt / model / label refinement に戻す loop が必要だと整理した。[[nasuka-statements-retrospective-2026-05-25]]より

## Open Questions

- このページを「常に次回会議向け 1 枚」に保つか、会議ごとに snapshot を切るかはまだ未決
- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-05-21: 初回作成。直近の `analysis-core` / Web UI / deploy / AI 運用ルールの進捗を次回定例向けに要約
- 2026-05-22: 月曜の定例会向けに、もっとやさしい言い方へ調整し、`#740 -> PR #856` と `#710 -> PR #857` まで反映
- 2026-05-22: 進行中: Windows 初回セットアップを塞ぐ `#731 -> draft PR #858` に着手し、`setup_win.bat` の文字コード依存メッセージを ASCII 化、API キー検証の重複を整理、Docker 未起動時の `cmd.exe` 実行確認まで実施。ブランチは `codex/fix-windows-setup-mojibake`。[[source-code]]より [[github-dev-docs]]より
- 2026-05-22: 進行中: Windows 実機で `setup_win.bat` + Docker Desktop を検証するための手順を `#860` 向けに docs へ追加。`mkdocs build --strict` は通過し、ブランチ `codex/windows-real-machine-setup-docs` を push 済み。PR 作成は GitHub コネクタ操作が拒否されたため未作成。[[source-code]]より [[github-dev-docs]]より
- 2026-05-22: 進行中: `#860 -> draft PR #862` として、docs だけでなく `setup_win.bat` の非対話モード、`windows-latest` の軽量回帰 CI、実機 self-hosted runner 用の E2E workflow まで追加。任意 PR から実機 runner が動く危険を避けるため、PR 起動時は author が `nishio` の場合だけ実行する条件にした。[[source-code]]より [[github-dev-docs]]より
- 2026-05-22: 進行中: `#860 -> draft PR #862` の実機 E2E が `public-viewer` の `../shared/csp` 欠落を検出したため、`apps/public-viewer` と `apps/static-site-builder` の Dockerfile に `apps/shared` を含める修正を追加。さらに PowerShell の `Invoke-WebRequest` が Windows 実機でタイムアウトしたため、到達確認を `curl.exe --head --fail` に変更し、最新 PR checks は実機 E2E まで成功。[[source-code]]より [[github-dev-docs]]より
- 2026-05-22: 進行中: 公開 repo の self-hosted runner が個人マシンであることを踏まえ、`#862` の Real Windows E2E は PR / 定期実行からは起動しないように変更。`workflow_dispatch` かつ許可された実行者だけに限定し、checkout の credential persistence も無効化した。[[source-code]]より [[github-dev-docs]]より
- 2026-05-22: `#731` の Windows setup 文字化け対応は、`PR #858` の ASCII 化案を close し、`PR #863` で `setup_win.bat` を ASCII ランチャー、`setup_win.ps1` を日本語案内本体に分離する方針へ切り替え
- 2026-05-25: `PR #863` は open のままだが、確認に必要な Windows 検証環境が整備中のため、現時点では review / merge を保留。優先度自体は高いが、次の実作業は環境整備完了後の再確認になる
- 2026-05-23: issue の優先順整理だけではなく、LLM grouping 系の第2分析モードと scatter-first な product 契約の衝突を長期論点として整理した。短期は散布図互換の暫定案、長期は散布図必須前提の解体、という二段構えを [[strategic-development-order-2026-05-23]] と [[jigsaw-sensemaker-history|LLM grouping 系の背景整理]] に追記
- 2026-05-23: API `report_launcher` が `analysis_core` を subprocess で起動する継ぎ目を、mock ではなく実 subprocess で踏む手元 smoke test `apps/api/tests/manual/report_launcher_subprocess_smoke.py` を追加し、`ADMIN_API_KEY=dummy PUBLIC_API_KEY=dummy OPENAI_API_KEY=dummy rye run pytest tests/manual/report_launcher_subprocess_smoke.py -q -s` で通ることを確認
- 2026-05-23: `launch_report_generation()` から通常フロー全体を踏む manual smoke を追加。最初の実行で workflow plugin が `--input-dir` / `--output-dir` を legacy step に渡していないバグを検出し、`analysis_core.plugins.builtin.*` を修正したうえで、`tests/manual/report_launcher_subprocess_smoke.py -q -s` と `tests/services/test_report_launcher.py -q` の通過まで確認
- 2026-05-23: path 修正後の plugin 側に残っていた legacy config 組み立ての重複を `_legacy_config.py` に集約し、`packages/analysis-core/tests/test_builtin_plugins.py` に extraction plugin の path 受け渡し regression test を追加。`packages/analysis-core` の関連 unit test と API manual smoke は再通過
- 2026-05-23: TTTC の clone / CUI 前提から、実務のための Web UI 包装、さらに研究開発向けの `analysis-core` / PyPI 再切り出しへ至る入口設計の歴史を [[tttc-to-analysis-core-history]] に整理。Web UI と CLI が競合ではなく役割分担だと説明しやすくした
- 2026-05-23: maintainer 判断 [[report-html-non-web-canonical-decision-2026-05-23]] と [[analysis-core-web-ui-separation-decision-2026-05-23]] を反映し、`report.html` は Web canonical にせず、WebUI / core 分離の設計判断も会議向け下書きに追記
- 2026-05-23: GitHub Pages の project site を `https://nishio.github.io/kouchou-ai-developer-wiki` の末尾スラッシュなしで開いた時、root の相対リンクが repo サブパスを落として `/concepts/...` へ飛ぶ問題を修正。Quartz `Head` に root 専用 `<base href="https://nishio.github.io/kouchou-ai-developer-wiki/">` を追加し、トップページからの内部リンクと静的 asset が常に正しいサブパス基準で解決されるようにした。[[source-code]]より
- 2026-05-23: `#2_開発_広聴ai` の Slack で [[ohki-shingo]] が「散布図はそれ自体が本質なのではなく、量・整理・全体像・個別意見への辿り・透明性の 5 要素を一画面で出していたから受け入れられている」「公開UIに求められる要件は 7 項目で言語化できる」「embedding の距離精度は公開UIの本質ではなく、cluster grouping が保てれば十分」と整理。これは [[jigsaw-sensemaker-history|LLM grouping 系の背景整理]] が残していた『散布図の役割を別 view でどう代替するか』への回答で、短期の散布図互換案の技術バーが思ったより低いことも示している。詳細は [[public-ui-requirements-for-broadlistening]] と [[slack-public-ui-requirements-2026-05-23]]
- 2026-05-24: `PR #865` merge を反映し、legacy pipeline cleanup と CI 修正まで含めて current `main` では refactoring を done 扱いにできる、と会議向け下書きへ追記
- 2026-05-25: 議事録 Google Doc は `txt` export だけだと URL が落ちるため、`raw/meeting_minutes.html` と `scripts/extract_meeting_minutes_urls.py` で 531 件の URL 棚卸しを取れるようにした。`kouchou-ai` 本体リンク、Slack permalink、書籍系リンクを分けて見られるようになったので、今後の「議事録に出てきた参照先を辿る」調査がやりやすくなった。[[meeting-minutes-url-extraction-2026-05-25]]より
- 2026-05-25: `analysis-core` に `analysis_mode=llm_grouping` の最小実装を追加。`embedding` は散布図互換の `x/y` 生成だけに使い、cluster assignment 自体は raw argument を直接 LLM でグルーピングする構成にした。workflow / spec も mode 切替対応にし、`packages/analysis-core` の targeted test 20 件は `rye run pytest tests/test_compat.py tests/test_integration.py tests/test_llm_grouping.py -q` で通過。次は admin 経路への受け渡しと、散布図がいまいちな時の代替 view 検討になる。[[jigsaw-llm-grouping-implementation-plan|LLM grouping 実装計画]]より
- 2026-05-25: `sample_comments.csv` 400 件の日本語データで `analysis_mode=llm_grouping` を実際に回した。422 argument を 8 群へ分け、`report.html` まで生成できたので短期互換案は成立した一方、embedding 由来 2D 散布図との相性は悪く、silhouette score は `-0.039` だった。次は scatter 改善より `hierarchyList` / `treemap` など group-first な view を優先して試すのがよさそう。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: 同じ 422 argument / 同じ embedding を使って従来 hierarchical clustering とも比べた。従来法は silhouette score `0.400`、centroid ベース再分類精度 `1.000` で、散布図としてはかなり自然だった。なので今回の結論は「LLM grouping をやめる」ではなく、「LLM grouping を scatter 主体で見せない方がよい」である。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: ただし比較の本丸は scatter 指標だけではなかった。`~/broadlistening-research` の 2025-02 ラベル評価研究を踏まえて OpenAI judge で top-level ラベル品質も比べると、`LLM grouping` が平均 `85.0`、従来 hierarchical が `80.4` で、読みやすさ・具体性・代表性では LLM grouping が上だった。つまり `geometry` と `label semantics` を別軸で評価すべきだと確認できた。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: 費用まで含めると、same-args downstream 比較で `LLM grouping` は `35,654 tokens / 149秒`、従来法は `7,088 tokens / 49秒` だった。scatter のためにこの差を払うのは割に合わず、`LLM grouping` はラベルのわかりやすさを上げるためにだけ使う、という見方が自然である。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: さらに `K=20` でも同じ 422 argument で比較した。geometry はやはり従来法が強かったが、label quality は `K=8` と違って平均点ベースでは `hierarchical K20` が `85.0` で最上位になった。つまり「LLM grouping の方が常にラベルが良い」ではなく、`K` を増やすと従来法もかなり具体的なラベルを返し始める。judge の粒度によって winner も揺れたので、次は `K` を固定せず sweep で見た方がよい。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: 従来 hierarchical の多層 `[8, 40]` も回した。40 cluster を先に作ってから 8 cluster へ集約すると、top-level label は単層 `K=8` より少し抽象的になるが、一貫性と網羅性は上がった。なので「8 cluster をどう作るか」は単なる `K` 指定ではなく、上位 summary の性格を変える設計変数だと分かった。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: そのうえで `LLM grouping K=8` と `hierarchical [8,40] level1` も直接 judge した。cluster 平均点では `[8,40] level1` の方が高かったが、ラベル集合全体の読みやすさでは `LLM grouping K=8` 勝ちだった。つまり `[8,40]` は代表性の強い上位集約として有望だが、そのまま UI 見出しに出すと少し説明的すぎる。次は hierarchical 集約に短いラベルを後付けする折衷案を試すのがよさそう。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: 実験の読みも少し整理できた。`LLM grouping` は `K=8` の粗い俯瞰では強かったが、`K=20` の細粒度では従来 hierarchical の方が個別ラベル品質で勝ち、しかも LLM grouping はコスト増に対して逆に少し品質が下がった。なので LLM grouping は「細かく分析する mode」より「ざっくり全体像を見る mode」と捉える方が自然かもしれない。改善の本丸も clustering 本体ではなく、top-level ラベル同士の区別を明瞭にする aggregation prompt / algorithm 側に寄ってきた。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: その次の実験基盤も入れた。`analysis-core` に `hierarchical_label_refinement` step を追加し、`merge_labelling` の後で top-level label set をまとめて再編集できるようにした。`mode = none / setwise_refine / setwise_refine_short` を config で切り替えられるので、以後は clustering を固定したまま「上位見出しの付け方」だけを比較できる。aggregation 改善の試行錯誤を product 実験として回しやすくなった。[[source-code]]より
- 2026-05-25: さっそくその 3 mode を同じ `[8,40]` 構造で比べた。cluster 平均点では baseline `none` が一番高かったが、ラベル集合全体の読みやすさをまとめて judge すると `setwise_refine` が 1 位だった。つまり「各クラスタ単体で良い説明」と「一覧で見てちょうど良い見出し」は別問題で、aggregation 改善は後者の最適化として扱うのがよさそう。`setwise_refine_short` は短すぎて少し情報不足になった。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: その次に `setwise_refine` の prompt も 2 本増やして比べた。cluster 平均点では `contrast` が最も良く、短くしながら情報密度を保つ方向ではこれが今の本命に見える。一方で、ラベル集合全体の読みやすさをまとめて judge すると `balanced` が 1 位だった。つまり、algorithm 的に良い見出しと、UI 上で読みやすい見出しを分けて考える必要がある。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: ただし、ここまでの judge 自体が OpenAI/GPT ベースで、生成側も同系統 LLM を使っている。そこで次は refinement mode を増やす前に、judge の仕組みと限界を [[label-judge-mechanism-2026-05-25]] に明文化し、[[label-refinement-judge-bundle-2026-05-25]] を使って Claude Code と人間の判断を差し込める形へ整理した。今は「どのラベルが勝ちか」より「どの judge をどこまで信じるか」を確認する段階である。[[jigsaw-llm-grouping-experiment-output-2026-05-25]]より
- 2026-05-25: 進行中: `analysis_mode=llm_grouping` の最小実装を label refinement から切り分け、draft PR `#866` として作成した。ブランチは `codex/llm-grouping-pr`、commit は `4f893ab`。変更範囲は LLM grouping の workflow / spec / plugin / step / default prompt / tests に限定し、label refinement は別 PR に回す。`packages/analysis-core` は通常テスト `186 passed` まで確認済み。[[source-code]]より [[github-dev-docs]]より
- 2026-05-25: 進行中: `--reuse-from` を LLM grouping / label refinement より先に draft PR `#867` として切り出した。ブランチは `codex/reuse-from-outputs`、commit は `977d7eb`。既存出力ディレクトリから中間成果物と status を seed し、同一 upstream artifact を使った比較実験を作りやすくするための土台で、変更範囲は CLI / orchestration / tests のみに限定した。`packages/analysis-core` は `OPENAI_API_KEY=dummy` 付き通常テスト `181 passed`、GitHub checks も全通過まで確認済み。[[source-code]]より [[github-dev-docs]]より
- 2026-05-25: 進行中: 実行時 `USER_API_KEY` の受け渡しも独立した draft PR `#868` として切り出した。ブランチは `codex/user-api-key-plumbing`、commit は `a21bf27`。API / Web から subprocess に渡した user key を `analysis-core` の fail-fast validation、workflow context、built-in plugin 経由の legacy step まで通し、かつ status JSON には保存しないようにした。`packages/analysis-core` は `OPENAI_API_KEY=dummy` 付き通常テスト `181 passed`、GitHub checks も全通過まで確認済み。[[source-code]]より [[github-dev-docs]]より
- 2026-05-25: `#2_開発_広聴ai_アルゴリズム開発` の新妻 thread を独立ページ化した。要点は「`UMAP` 後 `k-means` が危うい」だけではなく、「分析として自然な構成」「散布図として受け入れられる見え方」「報道利用での説明責務」が別問題として衝突していることだった。新規コントリビュータ向けには [[niizuma-thread-algorithm-critique]] を入口にすると、その後の LLM grouping 議論へ繋ぎやすい。[[slack-niizuma-umap-kmeans-thread-2026-03-18]]より
- 2026-05-25: 新妻 thread の考察を少し進めた。これは `HDBSCAN` や `spherical k-means` への単純置換問題ではなく、分析 artifact / 表示 artifact / 説明 artifact を分ける設計問題として読む方がよい。後続の LLM grouping 実験でも、意味的に良い分類と scatter 上の自然さは別指標だと出ているので、次は `analysis_mode` と viewer requirements の契約を明示するのが重要そう。[[niizuma-thread-algorithm-critique]]より
- 2026-05-25: tokoroten の 2026-Q1 spectral clustering メモも独立ページ化した。こちらは「TTTC が spectral を使っていた」以上に、「`UMAP` の `n_neighbors` を小さめにして紐状分離を作り、それを `SpectralClustering` で切る scatter-first な系」として TTTC を理解していた点が面白い。新妻 thread が幾何と説明責務の衝突なら、こちらは TTTC 的 scatter UX を何で成立させていたかの設計読みである。[[tokoroten-spectral-clustering-reading]]より
- 2026-05-25: ただし tokoroten の spectral 読みは、そのまま TTTC の設計意図として確定してよいわけではないので historical code で検証した。確認できたのは「TTTC は `UMAP` 後に `SpectralClustering` を掛け、`n_neighbors` 上限は 10、最終 `cluster-id` も spectral ラベル」という実装形までで、「紐状構造を意図的に作って切るのが方針」という部分は依然 inference のまま、と線引きを入れた。[[tttc-spectral-clustering-code-observation-2026-05-25]]より
- 2026-05-25: そのうえで、TTTC 意図を掘る前に外部研究の survey 棚も切った。読む対象は、`UMAP -> clustering` の empirical / caution、spectral clustering の explainability、BERTopic pipeline、可視化と分析の分離、評価軸の 5〜6 棚に分けるのがよさそうで、まずは UMAP docs と document clustering pipeline 比較から入る方針。[[clustering-research-survey-plan]]より
- 2026-05-25: 先に TTTC repo 内の説明も探したが、fork 側も upstream 側も `README` は浅く、対応する `clustering.py` はどちらも実質 `first commit` / `first open-source commit` 由来で、issue / commit title にも spectral や `n_neighbors` の rationale は見当たらなかった。なので repo 単体からは「なぜそうしたか」は読めず、今のところ確定できるのは `UMAP -> SpectralClustering` という実装形までである。[[tttc-spectral-clustering-code-observation-2026-05-25]]より
- 2026-05-25: さらに見ると、`shugiinsenyo2024-tttc` で変わっている本丸は spectral / `UMAP` 側ではなく、日本語向け tokenization だった。upstream の `CountVectorizer(stop_words=...)` を、fork では `janome` ベースの `CountVectorizer(tokenizer=tokenize_japanese)` に差し替えている。一方 current `analysis-core` には BERTopic / CountVectorizer 自体がもう無く、今の main line ではこの tokenizer 差分は生きていない。[[tttc-spectral-clustering-code-observation-2026-05-25]]より
- 2026-05-25: ここで重要なのは、その tokenizer が spectral clustering 本体のためではなく、BERTopic の語彙表現のためだったこと。英語なら stopwords ベースで済むが、日本語では空白分かちがないので `janome` が必要だった、と理解するのが自然である。つまり fork の日本語対応は clustering kernel より topic representation 側に乗っている。[[tttc-spectral-clustering-code-observation-2026-05-25]]より
- 2026-05-25: tokoroten とのアルゴリズム議論全体も振り返った。これは「どの clustering が正しいか」ではなく、散布図 product が担える価値、深い分析、説明責務、現場の運用ワークフローを分け直す議論だったと見るのがよさそう。なので `classic_scatter` は agenda discovery / 参加感の mode として守り、LLM grouping 系は group-first / explanation-first の別 mode として育てる、という整理になる。[[tokoroten-algorithm-discussion-retrospective]]より
- 2026-05-25: ohki さんとの公開UI議論も振り返った。要点は「散布図を残すか捨てるか」ではなく、散布図が担っていた量感・全体探索・個別意見への到達・恣意性の低さを、別 UI でどう満たすかという説明責務の話だった。次の view 実験は geometry 指標だけでなく、公開UI 7 要件で見るのがよさそう。[[ohki-discussion-reflection-2026-05-25]]より
- 2026-05-25: nasuka さんの過去発言を振り返り、実利用で壊れる入口、抽出・ラベル品質の失敗例収集、再利用・手動編集・自動評価をつなぐ改善 loop、政党 fork から upstream へ戻す境界を次の論点として整理。[[nasuka-statements-retrospective-2026-05-25]]より
- 2026-05-25: open issue を current `main@e5ed743` で棚卸しし、すでに解決済みだった `#19` `#271` `#281` `#290` `#315` `#333` `#380` `#385` `#396` `#398` `#400` `#456` `#613` `#721` `#799` `#815` を close。レポート再利用、属性フィルタ、静的ホスティング docs、エラーログ、E2E 基盤、LocalLLM、環境確認、フォーム入力 API key などは backlog から落とせる状態になった。[[github-dev-docs]]より [[source-code]]より
