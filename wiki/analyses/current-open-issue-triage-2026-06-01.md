---
type: analysis
summary: "2026-06-01 時点の open issue 124 件を subagent 5 分割で本文・コメントまで読み、current main と既存 wiki に照合した triage。短期優先は `#884` 作成前確認、`#885` Node runtime 排除、`#564/#696/#542` trust layer、`#877` Windows guide、`#881/#882/#869` ラベル品質実験で、`#871/#573/#558/#516/#513/#417/#379` などは close 候補"
sources:
  - github-dev-docs.md
  - source-code.md
  - remaining-issue-priority-2026-05-29.md
  - problem-list-from-open-issues-2026-05-19.md
  - trial-and-error-burden-reduction-2026-05-29.md
  - node-runtime-free-windows-exe-2026-05-31.md
  - label-quality-redesign-reset-2026-05-30.md
  - issue-877-windows-setup-guide-scope.md
  - public-ui-requirements-for-broadlistening.md
  - umap-seed-history.md
  - pr-887-production-deploy-observation-2026-06-01.md
---

# Current Open Issue Triage 2026-06-01

2026-06-01 17:10 JST 時点で `digitaldemocracy2030/kouchou-ai` の open issue は 124 件。5 つの subagent に issue 番号帯を分け、各 issue の本文・コメントを `gh issue view --comments` で読み、必要に応じて `work/kouchou-ai/` の current main (`0c294dafbe8cf1dc49b1532a3f7bb35740b5625b`) と既存 wiki を照合した。GitHub への close / comment / assign は行っていない。[[github-dev-docs]]より [[source-code]]より

同時点の open PR は `#887` と `#863` の 2 本。`#887` は `#886` を close する Plotly scattergl CSP 修正で checks は green だが merge は blocked。`#863` は `#731` を close する Windows setup の `.bat` / PowerShell 分離で、実機確認と review 判断が残る。[[github-dev-docs]]より

2026-06-01 17:50 JST 追記: `#887` は merge 済みで、open PR は `#863` の 1 本になった。ただし Azure Deployment success 後、デプロイ成功判定とユーザに見える反映状態が一時的にズレたため、deploy confirmation が new revision readiness を十分に確認していない可能性があると判断した。詳細は公開可能な粒度で [[issue-887-scattergl-csp-regression-2026-06-01]] に整理した。[[pr-887-production-deploy-observation-2026-06-01]]より

## 結論

前回 2026-05-29 の優先順位は大筋で有効だが、新規 issue と open PR を反映すると短期の扱いは次の順に見るのがよい。[[remaining-issue-priority-2026-05-29]]より

1. **進行中 PR の扱いを決める**: `#887 -> #886` は CSP 修正として checks green。`#863 -> #731` は Windows 実機確認と review 判断待ち。
2. **作成前確認パネルを first slice にする**: `#884` は `#221`, `#11`, `#79`, `#97`, `#292`, `#391` を束ねる concrete tracking issue。まず既存 `window.confirm` を置き換える小 PR がよい。[[trial-and-error-burden-reduction-2026-05-29]]より
3. **Windows / local 配布 route を分ける**: `#885` は Node runtime を build-time asset へ寄せる前提 issue、`#877` は current Windows guide のサポート境界整理。`#496`, `#287`, `#254`, `#289` はここへ吸収または参照化する。
4. **trust layer を docs / website で進める**: `#564` 活用事例、`#696` 誤読防止、`#542` 責任所在はセットで扱う。事例だけ出すと「何を保証しないか」が抜ける。
5. **ラベル品質は refinement 直行ではなく実験管理へ**: `#881` を tracking、`#882` を KJ prompt 比較、`#869` を label refinement 再構成候補として扱う。ただし現 wiki の判断どおり、まず sampling / rep args / judge の仕切り直しが先。[[label-quality-redesign-reset-2026-05-30]]より
6. **close cleanup を一度まとめて行う**: `#871`, `#573`, `#558`, `#516`, `#513`, `#417`, `#379` は、本文の主要目的が current main や調査コメントで満たされている可能性が高い。

## Close Candidates

強い close 候補は次の通り。実際に close する前には、人間が issue comment と current main の該当実装を最後に確認する。

| issue | 理由 | close 前の確認 |
|---|---|---|
| `#871` | current main の `azure-deploy.yml` は `fetch_reports` 依存ではなく Blob Storage health check に寄っている | 直近 CI で当該 check が通っているか |
| `#573` | PLaMo-Embedding-1B はコメント上の実験で品質・速度・互換性・`trust_remote_code` の面から非推奨 | 「現時点では採用しない」結論を issue に残す |
| `#558` | API testability は `TestSettings` と test fixture で主要改善が入っている | 実環境に触るテストがまだ残っていないか |
| `#516` | シルエットスコア調査結果と比較ページがコメントで揃っている | 結論が docs / wiki に残っているか |
| `#513` | seed は各所で記録済みというコメントがあり、再現性論点は `#514/#515` へ移せる | seed そのものの未記録箇所がないか |
| `#417` | CodeRabbit 導入は current main の `.coderabbit.yaml` と運用で満たされている | 運用改善を別 issue にするか |
| `#379` | E2E 導入計画は実装済み E2E と `#395` など個別拡張へ移った | 残 task を個別 issue に寄せる |
| `#323` | 多言語対応は prompt workaround がコメントで確認済み | UI 言語選択が必要なら別 issue に切る |
| `#308` | `wontfix` label 済みで、docs / 共有機能優先へ方針が寄っている | close コメントだけ準備 |
| `#289` | `wontfix` label 済み。単体 exe は `#885` の前提整理へ移った | `#885` への参照を残す |

## Assignee Respect

既に assignee がいる issue は、AI agent が独断で実装着手しない。今回の triage では `#876`, `#809`, `#731`, `#700`, `#643`, `#547`, `#519`, `#454`, `#370`, `#337`, `#324`, `#310`, `#280`, `#255`, `#11` などを assignee 尊重に分類した。[[github-dev-docs]]より

## Full Triage Table

| issue | 判断 | 次の一手 |
|---|---|---|
| `#886` | PR待ち | `#887` の review / merge 判断。WebGL fallback は別途必要なら follow-up |
| `#885` | 今すぐ進める | admin / public-viewer / static-site-builder の runtime Node 依存を棚卸し |
| `#884` | 今すぐ進める | 既存 confirm を作成前確認ダイアログへ置換する最小 PR |
| `#882` | 今すぐ進める | baseline / KJ / neutral structured prompt の固定条件比較を作る |
| `#881` | 今すぐ進める | 実験 matrix、採用判断基準、対象 issue を整理する |
| `#880` | 人間判断 | マンダラートの用途、対象要素、mobile / print 前提を決める |
| `#879` | 人間判断 | timestamp 必須/任意、bucket 粒度、集計値を決める |
| `#878` | 統合 | `#876` の developer docs 再構成に AI contributor 導線として吸収 |
| `#877` | 今すぐ進める | Windows guide 冒頭に対象環境、対象外環境、API key、失敗分岐を入れる |
| `#876` | assignee尊重 | nishio の新方針 PR 待ち。外からは草案レビューに留める |
| `#872` | 人間判断 | mobile 既定表示を散布図以外にするか product 判断する |
| `#871` | close候補 | Blob Storage health check が CI で通ることを確認して close |
| `#869` | 今すぐ進める | label refinement だけを clean scope で再構成する draft PR 範囲を作る |
| `#838` | 統合 | `#721` 側で tests-only か opt-in CLI 診断かを決める |
| `#809` | assignee尊重 | tokoroten / Copilot が「解消済みなら close、残るなら opt-in 再現性要件」判断 |
| `#731` | assignee尊重 | `#863` の Windows 実機確認と merge 判断 |
| `#700` | assignee尊重 | Devesh36 / 関連 PR の現状確認 |
| `#696` | 統合 | `#564/#542` と合わせて事例・限界・読み方 docs に分解 |
| `#690` | 今すぐ進める | `ts-node-dev` を `tsx` へ置換する小 PR |
| `#679` | 人間判断 | 旧 TTTC PR と削除 PR を読み、任意カテゴリ分類の仕様を 1 枚にする |
| `#669` | 今すぐ進める | Azure deploy workflow の build / deploy 責務分離を設計 |
| `#648` | 今すぐ進める | report list にチェックボックス選択と一括操作バーの shell を入れる |
| `#643` | assignee尊重 | rolzy 側で BuildKit secret 化か runtime env 化の方針確認 |
| `#641` | 人間判断 | Web 通知、API polling、CLI helper のどれを正式対象にするか決める |
| `#639` | 今すぐ進める | CSV D&D 時に title / intro が空なら basename を補完 |
| `#638` | 人間判断 | zoom 時のラベル表示ルールを決め、可視化刷新系へ接続 |
| `#592` | 今すぐ進める | Azure API version / deployment / endpoint 誤り候補を日本語で返す |
| `#586` | 人間判断 | pnpm + 共有 UI package 前提へ issue を更新するか決める |
| `#577` | 人間判断 | 自動クラスタ数調整の評価期間と継続判断基準を決める |
| `#576` | 今すぐ進める | 朝日 TTTC prompt を一覧化し、汎用流用 / 入力依存 / 不採用に分類 |
| `#573` | close候補 | PLaMo は現時点採用しない、または embedding benchmark umbrella へ移す |
| `#566` | 今すぐ進める | Storybook + Chromatic を admin empty state など 1 画面で spike |
| `#564` | 今すぐ進める | 公開可能な事例リストを作り、website 掲載粒度に整える |
| `#558` | close候補 | test fixture で実環境依存が消えているか確認して close |
| `#556` | 今すぐ進める | axe 等で admin / public-viewer を監査し小 issue に分割 |
| `#548` | 人間判断 | DB 化の範囲を中間 artifact / metadata / 編集履歴に分けて決める |
| `#547` | assignee尊重 | shgtkshruch の Server Action / API Route 方針待ち |
| `#546` | 今すぐ進める | exception handler / 共通エラー形式を小 PR 化 |
| `#542` | 人間判断 | 免責・責任範囲の文案を作り、運営/法務判断をもらう |
| `#537` | 今すぐ進める | OpenRouter 無料 chat model 1 個で current main の再現確認 |
| `#529` | 人間判断 | 説明画像の最終デザイン案待ち |
| `#528` | 人間判断 | 階層図下説明文の表示仕様とリンク仕様を確定 |
| `#519` | assignee尊重 | nishio の分析レポート公開作業待ち |
| `#518` | 今すぐ進める | public-viewer の export artifact / Pages 確認を scope 化 |
| `#517` | 人間判断 | welcome slide へ反映済みか確認し、済みなら close |
| `#516` | close候補 | 調査結果を docs / wiki に転記済みなら close |
| `#515` | 今すぐ進める | 保存済み UMAP / config を再利用する API / admin UI の最小設計 |
| `#514` | 今すぐ進める | extraction 結果を元 ID で安定ソートして保存する test を追加 |
| `#513` | close候補 | seed 論点を `#514/#515` へ寄せて close |
| `#507` | 人間判断 | report_status 互換コード削除を v3.0 milestone / TODO 管理へ移す |
| `#503` | 統合 | `#470` の PII 除去評価 slice として生成データセットと測定基準を定義 |
| `#496` | 統合 | `#877` / quickstart docs に WSL2 Docker Engine / Podman 導線として吸収 |
| `#493` | 今すぐ進める | PC wheel 問題だけ、短い遅延付き lock 解除と視覚 feedback で実装 |
| `#478` | 今すぐ進める | 日本語禁則対応の折返し helper と tooltip padding を試す |
| `#477` | 今すぐ進める | Azure 時は model select disabled + deployment env 説明を入れる |
| `#474` | 人間判断 | Bonsai 採用判断に必要な比較軸を決める。不要なら close |
| `#473` | 統合 | provider validation issue 側で Azure / OpenRouter / LocalLLM check path を揃える |
| `#471` | 今すぐ進める | local LLM benchmark の共通サンプルと計測指標を決める |
| `#470` | 人間判断 | PII masking policy と評価基準を先に決める |
| `#464` | 人間判断 | PO / 予算判断待ち。API key 確保は人間 attention 領域 |
| `#454` | assignee尊重 | masatosasano2 の進行待ち |
| `#452` | 今すぐ進める | LLM timeout を env 設定で外出しし、UI 化は後続 |
| `#450` | 統合 | provider capability 設計へ embedding model 選択として統合 |
| `#445` | 今すぐ進める | `.github/copilot-instructions.md` の最小版を draft |
| `#417` | close候補 | CodeRabbit 導入済み。運用改善は別 issue |
| `#395` | 統合 | `#379` / testing roadmap の具体 task へ分解 |
| `#393` | 今すぐ進める | howto / README の公開前 checklist に privacy policy URL 等を追記 |
| `#391` | 統合 | `#884` の API preflight に吸収 |
| `#379` | close候補 | E2E 導入済みなので個別拡張 issue へ移す |
| `#374` | 今すぐ進める | Batch API 化可能な LLM call step を PoC |
| `#370` | assignee尊重 | nishio の本物データ待ち判断 |
| `#367` | 今すぐ進める | extraction 失敗例を集め、プロンプト調整 guide 化 |
| `#366` | 人間判断 | 複数公開リストの実利用ニーズを確認 |
| `#364` | 人間判断 | private / unlisted / password の公開範囲方針を決める |
| `#346` | 今すぐ進める | 同一大量投稿対策の検証 approach ごとに sub issue 化 |
| `#345` | 人間判断 | `#346/#370` の結果を受けて技術・法務・UI 方針を整理 |
| `#342` | 統合 | raw data enrichment / input plugin 設計へ統合 |
| `#339` | 人間判断 | 同義語 map の効果を小データで検証 |
| `#337` | assignee尊重 | masatosasano2 の sandbox 試作待ち |
| `#324` | assignee尊重 | masatosasano2 の外部実験 repo 結果待ち |
| `#323` | close候補 | workaround を docs 化し、UI 言語選択は別 issue |
| `#318` | 今すぐ進める | `JSON list not found` 系の入力 / 出力ログを収集 |
| `#310` | assignee尊重 | nasuka が残要素を切り分け |
| `#308` | close候補 | `wontfix` 方針に沿って close コメント案を作る |
| `#306` | 今すぐ進める | 現 UI を見て zoom / 濃い意見 group の最小 UX 改善を切る |
| `#305` | 今すぐ進める | title / description optional or default の仕様確認 |
| `#295` | 今すぐ進める | retry / backoff と OpenAI Tier 案内を分離して進める |
| `#294` | 統合 | `#266` へ集約し、残要望だけ確認 |
| `#293` | 統合 | `#310` の編集機能残作業として整理 |
| `#292` | 統合 | `#884` の API preflight / billing confusion 表示へ吸収 |
| `#289` | close候補 | `wontfix` とし、単体 exe route は `#885` へ参照 |
| `#287` | 統合 | `#877` の Windows guide scope へ統合 |
| `#285` | 統合 | provider 戦略 issue へ集約 |
| `#283` | 今すぐ進める | current main で fullscreen tooltip / button overlap を再現確認 |
| `#280` | assignee尊重 | ei-blue のデータ整備待ち |
| `#266` | 今すぐ進める | ラベル衝突回避 / hover 強調案を現 UI で検証 |
| `#255` | assignee尊重 | nishio の OpenAI 代替 provider 整理待ち |
| `#254` | 統合 | `#877` に実行 route 別整理として集約 |
| `#253` | 今すぐ進める | file URL 検出と local server 誘導を実装検討 |
| `#250` | 人間判断 | 末端で原文を見せる policy と UI 仕様を決める |
| `#236` | 人間判断 | 回答案草案の用途、非保証表示、参照文書方針を決める |
| `#227` | 今すぐ進める | 濃い意見 group 設定画面の選択肢・説明 layout を小 PR 化 |
| `#223` | 今すぐ進める | sample result の置き場所と status 仕様を決める |
| `#221` | 今すぐ進める | `#884` の作成前確認パネルから具体化 |
| `#213` | 人間判断 | `5->50` 表記の認知順を PM / design で決める |
| `#211` | 今すぐ進める | status に pid / heartbeat / started_at を持たせ stale processing を error 化 |
| `#190` | 今すぐ進める | batch extraction の品質・失敗率・速度を短文/長文で再実験 |
| `#186` | 人間判断 | file upload API へ寄せるか、`#884` で入力不安を先に減らすか決める |
| `#176` | 今すぐ進める | extraction 後 LLM grouping の最小 script / branch を作る |
| `#173` | 統合 | `#172` のグラウンディング実験 task として扱い、単独 close 候補 |
| `#172` | 今すぐ進める | cluster 説明文と根拠 argument 対応を 2 案実験 |
| `#170` | 統合 | `#324` の実験完了後に実装 issue を切る運用へ整理 |
| `#143` | 今すぐ進める | 評価軸を 1 つに絞った LLM-as-judge / rubric 実験 |
| `#130` | 今すぐ進める | non-code contribution 要点を contribution guide / landing page へ移す |
| `#121` | 今すぐ進める | mobile / 狭幅時のラベル非表示または aspect 制約を小修正 |
| `#104` | 人間判断 | telemetry の収集項目、opt-in 既定、説明文を決める |
| `#97` | 統合 | `#884` で選択列、非空件数、クラスタ数関係を表示 |
| `#79` | 統合 | `#884` で粗い費用帯を作成前確認に入れる |
| `#60` | 今すぐ進める | 階層図 / list に density filter option を設計 |
| `#56` | 人間判断 | 元コメント再頒布可否 flag を input schema に持たせるか決める |
| `#55` | 今すぐ進める | report config / result metadata に default threshold を保存 |
| `#52` | 今すぐ進める | density 表示時だけ下部文言を表示中 cluster takeaway へ同期 |
| `#44` | 今すぐ進める | 近傍 cluster との差分情報を label prompt に入れる実験 |
| `#11` | assignee尊重 | `#884` 内で粗い時間帯表示、精密 ETA は後続 |

## Open Questions

- `#887` は checks green を根拠に review 後 merge でよいか、WebGL fallback を同時に求めるか。
- `#871` は current main の deploy health check で完全に満たされたと見て close してよいか。
- `#884` は API preflight 失敗時に作成開始を block するか、警告付きで続行可能にするか。
- `#564/#696/#542` の trust layer は kouchou-ai repo で持つか、website / docs 側へ移管するか。
- 古い umbrella issue を close する時、単純 close と「上位問題ページへの参照コメント」のどちらを標準運用にするか。

## Updates

- 2026-06-01: 初版作成。subagent 5 分割で open issue 124 件の本文・コメントを読み、current main、open PR、既存 wiki へ照合した。
