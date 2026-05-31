---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。会議ごとに過去回を snapshot として archive へ rotate し、本ページは次回向けの差分のみ積み上げる"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業を短時間で報告するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「全部の変更履歴」を書くことではなく、**会議で口頭共有したい判断と進み具合だけを残す** こと。詳しい根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- まず冒頭の「月曜にそのまま読む用」を 8 項目以内に保つ。詳細は下のテーマ別セクションへ送る
- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連 analysis / source ページへ送る
- 同じテーマで新しい情報が来たら、新しい bullet を足すのではなく既存セクションを書き換える
- 会議が終わったら本ページを `wiki/concepts/meeting-report-YYYY-MM-DD.md` へ rotate し、本ページは次回向けに空に戻す

## 過去回

- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## 月曜にそのまま読む用 (2026-06-01 向け)

1. ラベル品質改善は **仕切り直し方向** に寄せました。今の refinement 実装は polish-only で rep args を見ておらず、上流 sampling もランダム、UI の代表例表示も配列先頭、rubric judge も過去のズレを十分に検出できていない、と複数の層に同時に課題が見つかりました。次は prompt を磨くのではなく、ユースケース契約 → sampling 全件入力 → rep args artifact → judge 較正、の順で小さく検証します。[[label-quality-redesign-reset-2026-05-30]]より
2. 上のユースケース契約について nishio との対話で **「全体傾向把握ユースケース」 1 本に確定** し、tokoroten が Slack で **「デカい見落とし / デカい違和感を見つける」** と operational に言い換えました。合わせて **広聴AI の core stance** を **「構造把握スタンスのツールであって、定量分析スタンスのツールではない」** と明文化しています ([[analysis-stance]])。Web UI に契約選択は露出せず、少数重要論点系は CLI 分析者の prompt 責務、minority residual artifact なし。KJ #3/#4/#5 と公開UI 7 要件の #5/#7 は別ツール側に倒れ、本体は 5 件 + 構造把握の評価軸 2 件 (解説素材性 / 突合素材性) を担う整理です。
3. 構造把握装置の構造的限界として **「インサイト見つけられず止まる」現象** が ohki-shingo から提示され、reader 側に prior mental model がない / 一致している場合は突合素材があっても差異が生まれない、と説明されました。「すでにある総合計画に意見がどうマッピングされるか」のような明示的な prior model を持つ運用が構造把握装置が最も活きる場面、という整理です。UX 指針としては、ユーザは自分のしたいことを区別できない解像度で持つので **デフォルトモード提供 → 反応見て別 view を案内** する事後誘導型に倒し、選択強制は避ける。「ざっくり / 詳細」モード切替 + サンプル分析カタログを補助として用意する方向。[[slack-stance-discussion-2026-05-30]]より
4. 「別ツール」エコシステムの空き地に対する nishio の答えとして **CLI に多様な実験機能を積み、それが共有・比較・継承されるコミュニティを育てる** という二段構造のビジョンを [[broadlistening-tool-ecosystem-vision]] として整理しました。tokoroten の DivCon や Long Context 再分類のような少数意見救出系は CLI 拡張として位置づけ。Web UI に複雑機能を載せて DivCon 方向の発展が抑制された反省を踏まえます。
5. 進行中 PR は 2 本: 開発者向け docs 4 モード整理の `PR #883`(`#876`) と `fetch_reports.py` 降格 branch (`#870`)。`PR #883` は **merge を急がず再構成する判断** に切り替えました。理由は直近 1 週間で固まった整理 (利用主体先行分岐 / platform 安定性ティア / Docker Desktop license の決定フロー上の重み / データ量前提 / 構造把握スタンス) が docs に反映されておらず、現状だと「Docker Desktop を組織で使えない人」や「自治体担当の評価役」が詰まる構造のため。再構成方針は [[pr-883-restructuring-2026-05-31]] に整理済み。`#741` Azure deploy flaky は `PR #873` で workflow `concurrency` を追加し merge 済みで close、deploy safety の残課題は `#871` Blob health check に絞れています。[[remaining-issue-priority-2026-05-29]]より
6. open issue 121 件を再棚卸しし、project-wide 優先は `#221` 試行錯誤負担削減と `#564` 活用事例公開に戻しました。`#221` は単一 feature ではなく「作成前確認 / preflight / 入力検証 / 実行中見通し / 再利用」の 5 面のテーマとして整理し、具体起点として `#884`(作成前確認パネル) を切り出しました。[[trial-and-error-burden-reduction-2026-05-29]]より
7. Windows setup `#877` は、Docker Desktop が使える Windows 10/11 を標準入口にし、組織ポリシー / ライセンスで Docker Desktop や WSL2 が使えない端末は beginner guide のサポート境界外として明示する方針にしました。[[issue-877-windows-setup-guide-scope]]より
8. パイプライン step 追加判断は **「step 数」ではなく「新しい成果物責務を first-class にすべきか」** で決める方針にしました。`#874` の semantic island layout 生成は実験経路に戻し、標準パイプラインは 8 step のまま維持します。[[pipeline-step-default-policy-decision-2026-05-28]]より
9. スマホでの散布図 UX は、responsive 微調整より別ビュー方針を検討する `#872` を新規起票しました。`#121` `#283` も `bug` ラベルを外して `#872` の参考課題に寄せています。MST / supervised UMAP の試作からは、cluster 間と cluster 内を分けて点を所属島から出さない `semantic island map` を基準線にする判断も出ました。これは構造把握スタンス / 全体傾向把握ユースケース確定後も構造把握用主図候補として広聴AI 本体に残る位置づけです。[[semantic-island-map-prototype-2026-05-26]]より
10. developer-wiki の GitHub Pages は subpath link が壊れていた問題を Quartz `baseUrl` 方針で直し、生成物リンク検査を CI に追加しました。Quartz + GitHub Pages project-site の設計メモは public Gist `https://gist.github.com/nishio/35d604f23a39aca369ac74db8b65b655` として外出ししています。[[wiki-pages-publishing-stack]]より

(新しい可視化アイデア `#879` ヒートマップ / `#880` マンダラートは検討材料として残す。優先 lane の整理を先に進める想定)

## 次回定例向け詳細 (テーマ別)

### 1. ラベル品質改善: 仕切り直し

- Slack `#2_開発_広聴ai` 2026-05-29〜30 の議論を受けたユースケース契約は、nishio との対話で **「全体傾向把握ユースケース」一本** に確定 (詳細 [[label-quality-redesign-reset-2026-05-30]])。Web UI には契約選択を露出せず、CLI = 分析者が「重要」を prompt に書く責務、minority residual artifact なし、`analysis_mode` は契約と直交。次の実験以降は全体傾向把握最適化で sampling / rep args / judge を固める。[[slack-label-algorithm-improvement-2026-05-30]]より
- 現行 `hierarchical_label_refinement` の責務範囲を確認した結果、refinement は rep args を入力に取らず current_label + children labels だけで polish しており、`整った嘘` リスクがある polish-only 仕様だと分かった。default-off で main 同梱は OK だが、default-on 昇格を語る前段の整理が必要。[[label-refinement-input-scope-2026-05-29]]より
- 上流のラベル付け時 sampling は、API 通常経路で最大 30 件、analysis-core CLI/default で 10 件、いずれも Polars の seed なし random sample。最大被覆 / FPS / k-medoids / 適合度選択は入っていない。UI の階層リストも representative selection ではなく配列先頭 10 件である。改善の本丸は refinement より上流にある可能性が高い。[[label-coverage-policy-2026-05-29]]より
- 実装した rubric judge を退避済み過去出力 4 候補に当てると `none / setwise / balanced` が score_rate 1.0、`contrast` が 0.9766、fatal flag 0 件で、人間 / Claude judge が拾ったズレを v0 rubric は検出できていない。判定そのものを較正する必要がある。総コストは 174,839 tokens / 概算 \$0.0394。[[label-quality-rubric-evaluation-2026-05-29]]より
- 次の slice は (1) `sampling_num` を外して全件入力にしてラベル品質が上がるか、(2) `典型例 / 幅 / 境界` に分けた rep args artifact を生成、(3) UI / judge の入力をその artifact に揃える、(4) rubric criteria を厳格化する、を別々に切る。仕切り直しの全体像は [[label-quality-redesign-reset-2026-05-30]] に。
- 議論が散らないよう、上位トラッキング issue `#881` と KJ法的 prompt 比較実験 issue `#882` を起票し、既存 `#869` から辿れるように接続した。

### 2. 進行中 PR の着地と Azure deploy safety

- `PR #883` (`codex/issue-876-developer-quickstart`): `docs/development/developer-quickstart.md` を新規 canonical 入口にし、Docker Compose / dummy-server + frontend dev / native / CLI の 4 モードを「最初の 1 ページ」で判断できる構成にした。README は 240 → 92 行に trim、`mkdocs build --strict` pass。CodeRabbit 2 件は commit `3bd57a6` で address 済み。**ただし 2026-05-31 に nishio が「もうちょっと何が語られるべきかを整理してから作るべき」と判断し、merge を急がず再構成する方向に切り替え**。直近の整理 (利用主体先行 / platform 安定性ティア / Docker Desktop license / データ量前提 / 構造把握スタンス) が反映できていないため。具体的な再構成方針は [[pr-883-restructuring-2026-05-31]] に。次の一手は PR を draft に戻すか、追加 commit で再構成して push か、別 PR で書き直すかの判断。
- `#741` Azure deploy flaky は `PR #873` で `azure-deploy.yml` に workflow-level `concurrency` を追加して merge 済みで close。根本は npm flaky ではなく近接 main push による `ContainerAppOperationInProgress` だったので、serialization で一旦閉じた。[[issue-741-current-state-2026-05-26]]より
- deploy safety の残課題は `fetch_reports.py` 依存。current main の storage sync / restore 本線とずれており、`PUBLIC_API_KEY` 経由のため非公開レポートも救えない。旧 `#629` は close し、`#870`(script 降格) と `#871`(Blob Storage health check 置換) に分解した。実装順は `#871` を先、`#870` で docs / script 整理を後、が筋。[[fetch-reports-deprecation-and-storage-health-2026-05-26]]より
- `#870` 着手中: branch `codex/issue-870-fetch-reports-cleanup` で `azure-update-deployment` から `tools/scripts/fetch_reports.py` を外し、script 自体を削除。read/write 確認は既存 `apps/api/scripts/test_storage.py` を使う docs へ寄せた。PR はこれから作成。

### 3. 残 issue の優先順を live state で組み直し

- current open 121 件、`high priority` は `#221` と `#564` の 2 件。古い user-facing issue (`#11` `#79` `#97` `#292` `#391` 等) まで本文を読み直し、project-wide 優先順を組み直した: (1) `#221` 試行錯誤負担削減、(2) `#564` 活用事例公開、(3) 進行中 PR と Windows 導線の着地、(4) deploy / storage safety、(5) ラベル品質実験、(6) viewer UX (mobile 方針先決め)。[[remaining-issue-priority-2026-05-29]]より
- `#221` 系は「作成前確認 / API・billing preflight / 入力検証 / 実行中見通し / 再利用」の 5 面に分け、最初の slice は `apps/admin/app/create/page.tsx` の既存 `window.confirm` を作成前確認パネルへ置き換える。具体 issue として `#884` を起票し、`#11` `#79` `#97` `#292` `#391` へ整理コメントを追加した。[[trial-and-error-burden-reduction-2026-05-29]]より
- 残存 `[BUG]` title issue は `#741` close を反映済み。現在の `bug` ラベル open は `#731`(PR `#863` 対応中) / `#700`(他 contributor assigned) / `#477`(Azure model UI 不整合、直近最優先ではない)。

### 4. Windows setup guide のサポート境界 (#877)

- `#877` の本質は文言整理ではなく **サポート境界の問題**。Docker Desktop が入れられる Windows 10/11 を標準入口にし、組織ポリシーやライセンス制約で Docker Desktop / WSL2 が使えない貸与 PC は beginner guide の対象外、または別ルートとして明示する。[[issue-877-windows-setup-guide-scope]]より [[docker-desktop-license-2026-05-29]]より
- `PR #863`(`codex/issue-731-windows-setup-powershell`) も並行進行中で、`#731` 日本語 UX 戻しを担当。CodeRabbit 対応として API key 改行エラーの日本語化、`docker compose` を `$PSScriptRoot` で実行する修正、非対話失敗時の compose exit code 保持を追加済み。

### 5. パイプライン step 追加判断のフレーミング

- 直近研究で繰り返し出た「pipeline に step を足す」論点を、step 数ではなく「新しい成果物責務を first-class にすべきか」で判断する方針として整理した。`label_refinement` は default complexity として見せない optional 実験、境界・反例・bridge・未解決カードは `aggregation` に押し込まず `interpretation_artifacts` として切るのが筋。[[pipeline-step-addition-framing-2026-05-27]]より
- 適用例として `#874` の semantic island layout 生成は、`layouts` という named layout artifact を作る方向としては筋がよいが、標準パイプラインで常時走らせる理由は弱い。commit `51a7c77` で `hierarchical_layout_generation` を標準 workflow / specs / orchestrator / config defaults から外し、明示有効化される実験経路に戻した。標準 8 step contract と固定テストは維持。[[pipeline-step-default-policy-decision-2026-05-28]]より
- 関連 open PR の整理: `#866` LLM grouping は workflow として切る良い例、`#867` reuse-from は downstream 比較の基盤。[[open-pr-pipeline-step-observation-2026-05-28]]より

### 6. スマホ向け散布図と semantic island map

- `#121` `#283` を実機相当 viewport で再観測した結果、portrait では tap tooltip が plot 幅の大半 (363/390px) を覆い、`360x520` 等の小型では hover overlap が複数件再現する。responsive 微調整だけでは根本問題が残ると判断し、mobile では静的画像 / クラスタ一覧 / 簡略図など別ビュー方針を検討する `#872` を新規起票。両 issue の `bug` ラベルは外し、`#872` の参考課題に寄せた。[[remaining-bug-issues-2026-05-26]]より
- `worktree: codex/mst-visualization-prototype` で `LLM grouping` 済み 422 argument の可視化を MST overlay / supervised UMAP / semi-supervised UMAP / LDA / centroid-MDS と試したが、いずれも「離れすぎ」か「混ざりすぎ」で解決しなかった。embedding 由来散布図を主図にする発想をやめ、cluster 間配置と cluster 内配置を分離して点を所属島から出さない `semantic island map` を `LLM grouping` 向け cluster-first view の基準線にする方向にした。[[semantic-island-map-prototype-2026-05-26]]より

### 7. developer-wiki Pages の整備

- developer-wiki の GitHub Pages で、index や検索結果のリンクが project-site subpath と噛み合わず壊れる問題を再点検。Quartz 4 は `baseUrl` で project-site hosting を扱えるため、root 専用 `<base>` patch は撤去し、`scripts/check_pages_links.py` を CI に入れて build 後の全内部リンクが `/kouchou-ai-developer-wiki/` 配下に解決されることを検査する形に直した。[[wiki-pages-publishing-stack]]より
- Quartz + GitHub Pages project-site の設計メモを public Gist `https://gist.github.com/nishio/35d604f23a39aca369ac74db8b65b655` に外出しした。旧 Gist の `wiki/ -> content/` 変換は汎用 Obsidian vault には有効だが、この repo では `wiki/` direct build を維持する判断を明文化。

### 8. 新しい可視化アイデア (検討材料)

- `#879` `[FEATURE] クラスタと時刻の掛け合わせでヒートマップ表示したい` と `#880` `[FEATURE] [8, 64] の分析をマンダラートで可視化したい` を起票。`#879` はクラスタ別の時間的盛り上がりを読むビュー、`#880` は主要 8 観点と 64 下位要素を探索するビューとして、まず mock / prototype で読みやすさを確認するのが次の一手。優先 lane (`#221` / Windows / ラベル品質 / deploy safety) の整理を先に進める想定。

## Open Questions

- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-05-30: 月曜読み上げ用要約を冒頭に追加し、本文を 8 テーマへ束ね直した。Updates もテーマごとの最終判断だけを残す形へ整理
- 2026-05-30: 「別ツール」エコシステムへの答えとして **CLI + 共有コミュニティ** 二段構造を [[broadlistening-tool-ecosystem-vision]] で整理。tokoroten の DivCon や Long Context 再分類は CLI 拡張の位置づけ。Web UI に複雑機能を載せて DivCon 方向が抑制された反省を踏まえる
- 2026-05-30: 用語を descriptive な日本語に統一 (`contract A` → 全体傾向把握ユースケース、`β / α` → 構造把握スタンス / 定量分析スタンス、`β 装置` → 構造把握装置 など)。略号は時間が経つと読めなくなるため、内容で読める表現にした
- 2026-05-30: 構造把握装置の構造的限界「止まる現象」を [[slack-stance-discussion-2026-05-30]] / [[analysis-stance]] で整理。reader 側に prior model がない場合は突合素材があっても差異が生まれない。UX 指針としてデフォルトモード + 反応事後誘導型に倒し、「ざっくり / 詳細」モード切替とサンプル分析カタログを補助に
- 2026-05-30: tokoroten が全体傾向把握ユースケースを **「デカい見落とし / デカい違和感を見つける」** と operational に言い換え。「全体傾向把握」より具体的で判断軸として使いやすい
- 2026-05-30: core stance **「広聴AI は構造把握スタンスのツールであって、定量分析スタンスのツールではない」** を [[analysis-stance]] として明文化。KJ #3/#4/#5 と公開UI 7 要件 #5/#7 は別ツール側に倒れ、本体は構造把握装置 5 件 + 構造把握の評価軸 2 件 (解説素材性 / 突合素材性) を担う整理に
- 2026-05-30: nishio との対話でユースケース契約を **「全体傾向把握ユースケース」 1 本に確定**。Web UI 非露出、少数重要論点系は CLI 分析者責務、minority residual artifact なし。下流 4 レイヤ (sampling / rep args / judge / refinement) を全体傾向把握最適化で揃える方向に [[label-quality-redesign-reset-2026-05-30]]
- 2026-05-30: ラベル品質改善は仕切り直し方向に確定。sampling / rep args / judge / UI 表示責務を別々に検証する [[label-quality-redesign-reset-2026-05-30]]
- 2026-05-30: 実装済み rubric judge v0 は過去出力で甘いと確認。criteria 厳格化または evidence 抽出前処理が次の課題 [[label-quality-rubric-evaluation-2026-05-29]]
- 2026-05-29: open issue 121 件を再棚卸し。project-wide 優先を `#221` / `#564` に戻し、`#221` 系の起点として `#884` を起票 [[remaining-issue-priority-2026-05-29]] [[trial-and-error-burden-reduction-2026-05-29]]
- 2026-05-29: Windows setup `#877` をサポート境界問題として整理。Docker Desktop 不可環境は beginner guide 対象外として明示する方針 [[issue-877-windows-setup-guide-scope]]
- 2026-05-29: ラベル品質改善の上位トラッキング `#881` と KJ法 prompt 比較実験 `#882` を起票。`work/kouchou-ai/` の dirty 実験は branch `codex/remaining-experiment-artifacts-2026-05-29@b56ac9b` へ退避し常用 clone を clean に復帰
- 2026-05-31: PR `#883` は merge せず再構成する判断に切り替え。直近 1 週間の整理 (利用主体先行 / platform 安定性ティア / Docker Desktop license / データ量前提 / 構造把握スタンス) を docs に取り込んでから land する方針 [[pr-883-restructuring-2026-05-31]]
- 2026-05-29: PR `#883` を作成し、developer-quickstart で 4 モード分岐を 1 ページに集約。README は 92 行に trim
- 2026-05-29: `#870` 着手。`fetch_reports.py` を削除し deploy docs を Blob sync / `test_storage.py` 前提へ更新
- 2026-05-28: `#874` は実験経路に戻し、標準パイプラインは 8 step のまま維持する方針で commit `51a7c77` を push
- 2026-05-28: developer-wiki Pages の subpath 問題を Quartz `baseUrl` 方針へ戻し、生成物リンク検査を CI に追加。Quartz 設計メモは public Gist として外出し
- 2026-05-26: `#741` を `PR #873` (workflow `concurrency` 追加) で merge し close。残 deploy safety は `#870` / `#871` に分解
- 2026-05-26: スマホ別ビュー方針の検討 issue `#872` を起票。`#121` / `#283` の `bug` ラベルは除去し参考課題化
- 2026-05-26: MST / supervised UMAP の試作から、`LLM grouping` 可視化の主図は `semantic island map` を基準線にする判断
- 2026-05-27: pipeline step 追加判断を「step 数」ではなく「成果物責務」で判断する整理 [[pipeline-step-addition-framing-2026-05-27]]
- 2026-05-26: open PR review コメント対応として `#867` `#866` `#863` をそれぞれ更新済み
