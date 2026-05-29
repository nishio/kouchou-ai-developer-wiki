---
type: analysis
summary: "`#221` 系は単一機能ではなく、作成前確認、API/billing preflight、入力検証、進捗可視化、再利用の5面で「怖くて試せない」「失敗理由が分からない」「やり直しが高い」を減らすテーマである"
sources:
  - github-dev-docs.md
  - source-code.md
  - remaining-issue-priority-2026-05-29.md
  - problem-list-from-open-issues-2026-05-19.md
  - development-priority-roadmap-2026-05-23.md
---

## 問い

残 Issue の優先順で 1 番目に置いた `#221` 系、つまり「試行錯誤の負担を減らす」は、具体的には何を優先して考えるべきか。

## 結論

`#221` は単一の feature issue として実装するより、**初回実行前・実行中・失敗後・再実行時**の不安を減らす上位テーマとして扱う方がよい。Issue 本文は、準備工数の認識ギャップ、プロンプトやクラスタ数の調整、サンプリング確認、1 万件投入で長時間待つ問題、extraction / embedding 後の高速な再試行をまとめて挙げている。[[github-dev-docs]]より

最初の具体 PR としては、`apps/admin/app/create/page.tsx` の送信前に **作成前確認パネル** を入れるのが一番筋がよい。ここに、入力件数、選択カラム、推奨/現在クラスタ数、概算時間、概算コスト帯、API 接続チェック結果を集める。既に CSV / spreadsheet / plugin のコメント配列は送信前に組み立てられており、現在も `comments.length < clusterLv2` の時だけ `window.confirm` で止めているため、差し込み点は明確である。[[source-code]]より

ただし「精密なコスト予測」を最初から作るべきではない。`#79` の問題は、数円単位で当てることではなく、「想定外に高額だったら怖い」を処理開始前に下げること。したがって最初は「小 / 中 / 大」や「100 円未満 / 100〜1000 円 / 1000 円以上」程度の粗い帯でよい。[[github-dev-docs]]より

## 分解

### 1. 作成前の go / no-go 判断

`#11` と `#79` は別 issue だが、ユーザー体験としては同じ面に出すべきである。ユーザーは「この CSV を入れて、今のクラスタ数とモデルで、どれくらい時間と費用がかかるか」を知りたい。時間は `#11` コメントに実測例があり、50 件で 29 秒、400 件で 1 分 35 秒、12,422 件で 55 分 51 秒という観測が残っている。ただし OpenAI API Tier によって 10 倍程度遅くなる可能性もコメントされているため、表示は範囲と注意書きに留めるのが安全である。[[github-dev-docs]]より

現行コードには実行後の token usage / estimated cost 表示があり、`LLMPricing` と `TokenUsage` も存在する。しかしこれは完了後の説明であり、開始前の不安解消には届いていない。[[source-code]]より

### 2. API / billing preflight

`#292` は ChatGPT Plus と OpenAI API 課金の混同、`#391` は API key 不備や quota の分かりにくい失敗を扱っている。現行 main には `EnvironmentCheckDialog` と `/admin/environment/verify` があり、OpenAI / Gemini などに軽い chat request を投げて `authentication_error`、`insufficient_quota`、`rate_limit_error` を返す実装がある。[[source-code]]より

つまり足りないのは API チェック機能そのものではなく、**レポート作成開始フローとの結合**である。今はユーザーが手で「API接続チェック」を押す形なので、作成前確認パネル内に「未確認 / OK / 残高不足 / rate limit / 不明」を表示し、fatal な失敗だけ開始前に止めるのが自然である。[[source-code]]より

### 3. 入力データの不安

`#97` は CSV フォーマットエラーの分かりにくさだが、現行 main では `parseCsv` が `chardet` と `iconv-lite` で文字コードを吸収し、`getBestCommentColumn` がコメント列を推定している。さらに CSV / spreadsheet 取得後に件数から推奨クラスタ数を自動設定する実装もある。[[source-code]]より

したがって `#97` 系を今やるなら、文字コード変換を追加するより、作成前確認パネルで「選ばれたコメント列」「非空コメント数」「属性列」「クラスタ数との関係」「極端に短い/空の行が多い」などを見せる方が current main に合っている。失敗後にエラー文を改善するより、失敗しやすい入力を開始前に気づかせる方が `#221` の目的に近い。[[problem-list-from-open-issues-2026-05-19]]より

### 4. 実行中の見通し

`#11` は開始前だけでなく、実行中の残り時間感にも関係する。pipeline は step ごとの duration と token usage を status に残しており、管理画面側にも progress polling がある。[[source-code]]より

ただし最初に入れるべきなのは精密な ETA ではなく、「今の step は重いのか」「extraction が長いのは正常範囲か」「API tier / rate limit で遅くなる可能性があるか」を表示する程度でよい。精密 ETA は外すと不信感につながるため、過去実測が十分に溜まるまで secondary に置く。

### 5. やり直しのコスト

`#221` 本文は、クラスタ数だけ変えるような試行錯誤では extraction / embedding 済みデータを使って高速に再実行できる、と書いている。関連する `#19` は既に close され、現行 main にはレポート再利用 UI、`duplicate` API、中間成果物再利用、`docs/user-guide/reuse-report.md` が入っている。[[github-dev-docs]]より [[source-code]]より

このため、再利用は「未実装の大物」ではなく、作成前確認パネルや失敗時 UI から誘導すべき既存能力と見るべきである。たとえば大きい CSV を初回投入する時に「まず少量で試す」「既存レポートから再利用する」導線を出せると、`#221` の試行錯誤負担削減に直結する。

## 優先順

1. **作成前確認パネルの shell を作る**  
   まず既存の `window.confirm` を置き換え、入力件数、選択カラム、クラスタ数、provider/model、警告一覧を表示する。ここだけでも `#97` とクラスタ数不安をまとめて下げられる。[[source-code]]より

2. **API 接続チェックを作成前フローに統合する**  
   既存 `/admin/environment/verify` を使い、未確認なら確認ボタン、失敗なら actionable message を出す。`#292` / `#391` への効きが大きい。[[source-code]]より

3. **時間・費用は粗い帯で表示する**  
   `LLMPricing` は実行後コスト計算に既に使われているが、作成前は token usage がない。最初は comment count / 文字数 / model から coarse bucket を出し、「目安」「API tier により変動」と明示する。[[source-code]]より [[github-dev-docs]]より

4. **大規模入力には sample-first / reuse を促す**  
   `#221` 本文の「100件、1000件とサンプリングする？黙ってやると有害、確認ダイアログがあるといい」は重要。自動で勝手に間引くのではなく、ユーザーに確認して少量実行を選ばせる。[[github-dev-docs]]より

5. **実行中 ETA は後段に回す**  
   progress UX は有用だが、先に go / no-go と fatal preflight を作った方が効果が大きい。ETA はデータ収集と表示責任が重いため、最初の PR には詰め込みすぎない。

## 最初のPR案

Issue を新しく切るなら、タイトルは `レポート作成前に入力・コスト・API状態を確認できるパネルを追加する` がよい。紐づけは `#221`, `#11`, `#79`, `#292`, `#391`, `#97`。

2026-05-29 にこの方針で `#884` `[FEATURE] レポート作成前に入力・コスト・API状態を確認できるパネルを追加する` を起票した。labels は `enhancement`, `Admin`, `API`, `design`, `high priority`。`#221` には concrete tracking issue としてコメントし、`#11`, `#79`, `#292`, `#391`, `#97` にも `#884` の下位論点として整理するコメントを追加した。`#391` は未分類だったため `enhancement`, `Admin`, `API` label も追加した。[[github-dev-docs]]より

完了条件の最小形:

- CSV / spreadsheet / plugin のどの入力でも、送信前に同じ確認パネルを通る
- コメント件数、選択コメント列、属性列、クラスタ数、provider/model が表示される
- コメント件数が第2階層クラスタ数を下回る既存警告が、パネル内警告として表示される
- API 接続チェックの結果を表示できる。未確認でも進めるかどうかは policy として明示する
- コスト/時間は「目安なし」でもよいが、表示領域を先に作る。入れる場合は粗い帯に留める

次の PR で、coarse cost estimator と time bucket を入れる。価格表は変わるので、金額の精度より「見積もりの粒度と責任範囲」を先に決めるべきである。[[source-code]]より

## 注意点

- 作成前確認を巨大な wizard にしない。目的は不安を下げることで、入力の儀式を増やすことではない。
- コスト見積もりは false precision を避ける。小数点のドル表示より、範囲と「高くなり得る条件」を示す方がよい。
- API preflight は万能ではない。接続チェックが OK でも、実行中の rate limit や provider 側障害は起こり得る。
- `#877` の Windows guide は `#221` と隣接するが、アプリ内の試行錯誤負担とは分ける。Windows は「起動前の導入摩擦」、作成前確認は「起動後の分析実行摩擦」である。[[remaining-issue-priority-2026-05-29]]より

## Open Questions

- API 接続チェック失敗時に、作成開始を完全 block するのか、警告付きで続行可能にするのか
- cost bucket は `円` で出すか、provider pricing に合わせて `USD` で出すか
- 大規模 CSV の sample-first は UI だけにするか、実際に N 件サンプルを作って新規レポート化する機能まで含めるか
- 再利用導線は作成前確認パネルに出すか、完了/失敗後のレポート一覧側に寄せるか

## Updates

- 2026-05-29: 方針に沿って GitHub issue `#884` を起票し、`#221`, `#11`, `#79`, `#292`, `#391`, `#97` へ相互リンクコメントを追加。`#391` には `enhancement`, `Admin`, `API` label を追加した。
- 2026-05-29: 初版作成。open issue 再棚卸し後の `#221` 系について、current main の作成画面、API 接続チェック、token/cost 表示、再利用機能と照合して整理した。
