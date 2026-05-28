---
type: analysis
summary: "2026-05-26 時点で open の `[BUG]` タイトル issue と周辺ラベルを current `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` で見直すと、`#741` だけが `bug` ラベルを保ち、`#121` `#283` `#478` は上位検討 issue `#872` の参考課題として bug ラベルを外し、`#731` は stale 寄りで再観測または close 判断が必要"
sources:
  - source-code.md
  - github-dev-docs.md
---

## 問い

2026-05-26 時点で、まだ open の `[BUG]` タイトル issue とその周辺ラベル状態はどうなっており、current `origin/main` を一次参照するとどれが実装課題として強く残っているか。[[github-dev-docs]]より [[source-code]]より

## 結論

GitHub live state では `[BUG]` title の open issue は `#741` `#731` `#478` `#283` `#121` の 5 件だったが、このうち `#478` `#283` `#121` は triage の結果 `bug` ラベルを外した。current `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` を照合すると、`#283` `#121` は散布図 UI の未解決課題としてそのまま残っており、`#741` も Azure deploy workflow の構造上まだ再発余地がある。ただし `#121` `#283` `#478` は新規 issue `#872` の参考課題として位置づけ直しており、緊急 bug ではなく mobile / scatter UX の検討材料として扱う。`#478` は原因コードこそ current main に残るが、解法が禁則処理実装か HTML tooltip への作り直しに寄るため、性質としては改善 feature に近く優先度は低い。一方 `#731` は main 側の `setup_win.bat` から issue 本文の原因だった日本語バッチ行が既に消えており、open PR `#863` もあるため、少なくとも「issue 本文の症状そのもの」は stale 寄りである。[[github-dev-docs]]より [[source-code]]より

## GitHub live state

- `#741 [BUG] main ブランチへのマージ時に実行される Azure への deploy が失敗する` (`bug` ラベルあり)
- `#731 [BUG] Windows環境でインストールしようとすると文字化けが発生して中断する` (`bug` ラベルあり)
- `#478 [BUG] Clientの意見の説明が禁則処理ができていない` (`bug` ラベルは 2026-05-26 に除去)
- `#283 [BUG] ScatterChartの全画面表示で要約文が「全画面終了」ボタンの後ろに隠れないようにする処理が不安定` (`bug` ラベルは 2026-05-26 に除去)
- `#121 [BUG] 縦長画面での散布図の表示がおかしい` (`bug` ラベルは 2026-05-26 に除去)

なお `#477` は `bug` ラベル付きで open だが、タイトルは `[REFACTOR]` であり、このページでは `[BUG]` prefix 残件とは分けて扱う。[[github-dev-docs]]より

## Issue 別整理

### `#741` は current workflow でも再発余地が残る運用バグ

current `.github/workflows/azure-deploy.yml` は、今も `docker build` 4 本と `docker push` 4 本を並列実行している。issue 本文の failure は `npm ci` の `ECONNRESET` で、恒常的な依存不整合というより CI 上のネットワーク不安定に見えるが、workflow 側には retry も fetch timeout 調整も直列化も入っていない。したがって「たまに落ちる deploy」は current main でもまだ説明できる。[[source-code]]より

さらに deploy 前 safety check が今も `fetch_reports.py` に依存しており、こちらは別途 `#871` で Blob Storage health check へ切り替える論点として分離済みである。`#741` 自体は build/push の flakiness として残しつつ、storage safety 論点と混ぜない方がよい。[[source-code]]より [[github-dev-docs]]より

### `#731` は live では open だが、current main 基準だと stale 寄り

issue 本文の症状は、`setup_win.bat` 内の日本語行が文字化けし、その崩れた文字列が別コマンドとして解釈されて停止するものだった。しかし current `origin/main:setup_win.bat` は `chcp 65001` を入れた上でメッセージを英語に寄せており、問題の日本語バッチ行は残っていない。少なくとも、issue に貼られた failure と同じ壊れ方は current main の静的読解からは見えない。[[source-code]]より

一方で GitHub 上では `Fixes #731` を含む open PR `#863` が残っており、方針としては `setup_win.bat` を ASCII ランチャーにして本体を `setup_win.ps1` へ分離する案が提案されている。つまり `#731` は「現 main の英語化で実害がもう消えているなら close 候補」「日本語 UX を戻したいなら PR #863 を merge」という二段構えで考えるのがよい。[[github-dev-docs]]より [[source-code]]より

### `#478` は原因コードは残るが、扱いとしては改善 feature 寄り

current `apps/public-viewer/components/charts/ScatterChart.tsx` では hover text 生成時に `arg.argument.replace(/(.{30})/g, "$1<br />")` を 2 箇所で使っており、30 文字ごとの機械改行から進んでいない。issue 本文が指摘している禁則処理失敗の原因コードが current main にそのまま存在するので、これは stale ではなく明確な未実装である。[[source-code]]より

ただし解決手段は、実質的に「禁則処理を伴う折り返し helper を自前実装する」か「SVG hover をやめて HTML tooltip へ作り直す」かのどちらかである。どちらもコストは軽くなく、得られる改善は hover 文言の読みやすさに限られる。そのため、issue ラベルは `[BUG]` でも、優先度判断としては改善 feature に近い低優先先として扱うのが妥当である。[[source-code]]より

### `#283` は one-shot DOM 補正のままで、issue 本文の「不安定」がまだ説明できる

current `Chart.tsx` と `ScatterChart.tsx` には、hover text や modebar が全画面終了ボタンに重なったときに DOM を後からずらす補正が入っている。だがどちらも overlap 判定後に一度 `transform` / `top` を書き換える構造で、viewport resize や hover state 変化に対して継続追従する設計ではない。issue 本文の「ブラウザを極小にしてマウスを動かし続けると不安定」という指摘は、current 実装でもまだ起こりうる。[[source-code]]より

つまり `#283` は「未対策」ではなく「局所 patch は入ったが deterministic ではない」状態で残っている。close 判定より、browser 上で再観測して DOM patch の延命を続けるか、ボタン配置ごと変えるかを決める段階に見える。[[source-code]]より

### `#121` は縦長レイアウト向けの明示設計がまだ見えない

current `ScatterChart` は `useResizeHandler` と `responsive: true` で全面リサイズ任せになっており、縦長 viewport で散布図のアスペクト比やラベル干渉をどう制御するかの専用ロジックは見当たらない。`Chart.tsx` 側も non-fullscreen では高さ固定 `500px`、fullscreen では `100vh` を与えるだけで、portrait 時の表示優先順位を定義していない。したがって issue 本文の「縦長で表示がおかしい」は current code から見ても未整理のままである。[[source-code]]より

`#121` と `#283` はどちらも散布図のレイアウト制御だが、`#121` は viewport 比率の基本設計、`#283` は全画面 hover/button 衝突の局所挙動であり、同じ一件にまとめず別論点として扱う方が実装しやすい。[[source-code]]より

Browser で `http://localhost:3000/example` を fullscreen 表示し、`390x844` / `360x640` / `844x390` / `1280x720` を比較すると、portrait では散布図が viewport 全体いっぱいの `390x844` や `360x640` になり、10 個の annotation はすべて bounds 内には収まるものの、横幅 249px のラベルが狭い画面幅に対してかなり大きい比率を占める。一方 landscape `844x390` や desktop `1280x720` では、同じ 249px ラベルでも相対的な圧迫感はかなり下がる。つまり current main は「縦長で壊れてはいない」が、「縦長で情報密度がきつく、散布図の余白が少ない」寄りの問題を抱えている。[[source-code]]より

さらに mobile-sized viewport で tap 相当の操作を試すと、tooltip は `#283` のようにボタン裏へ潜るのではなく、button 下端の `y=70` 付近から表示される。その代わり `390x844` portrait では tooltip 幅が `363-366px` と plot 幅 `390px` のほぼ全体を覆っており、1 回の tap で上部の散布図領域を大きく隠す。したがって実スマホ寄りの体験では、「hover の重なり」よりも「tap tooltip が広すぎて散布図を読み続けにくい」方が本質的な使いづらさとして現れやすい。[[source-code]]より

## 優先度の考え方

### 1. 先に判断だけ済ませたいものは `#731`

これは実装優先度というより triage 優先度が高い。current main で issue 本文の症状が消えているなら close 候補であり、日本語案内の復元まで要求するなら PR `#863` の扱いを決めればよい。放置すると「既に症状が薄い bug」が backlog に残り続ける。[[github-dev-docs]]より [[source-code]]より

### 2. 優先度を下げてよいのは `#478`

原因コードは明確だが、解法は禁則処理実装か tooltip 再設計に寄るため、修正コストに対してユーザー価値の伸びが大きくない。したがって backlog には残してよいが、積極的な先行着手対象にはしない方がよい。[[source-code]]より

### 3. レイアウト系は `#121` と `#283` をセット観察してから分けて直す

両方とも current code 上で不安定さの説明はつくが、修正案は browser での再観測なしに決め切りにくい。先に fullscreen / portrait の観測条件を固定し、どこまでを CSS と Plotly 設定で吸収し、どこからを DOM patch で受けるかを決める必要がある。現在は `#872` の参考課題としてぶら下げ、mobile では別ビューを既定にする選択肢も含めて検討する。[[source-code]]より [[github-dev-docs]]より

### 4. `#741` はプロダクト bug というより運用信頼性改善として別枠で扱う

利用者向け UI bug と同じ棚で考えるより、GitHub Actions の flakiness 改善として retry / timeout / 並列度を評価する方が筋がよい。`#871` と合わせて deploy safety の残課題群として見ると整理しやすい。[[github-dev-docs]]より [[source-code]]より

## Open Questions

- `#731` は current main の英語化だけで close してよいか、それとも日本語 UX の回復まで bug fix の完了条件に含めるか
- `#478` は title の `[BUG]` まで直すか、それとも label だけ外して issue 本文は据え置くか
- `#121` と `#283` は Plotly の layout 設定でどこまで解けるか、あるいは fullscreen UI のボタン配置変更が先か
- `#741` は retry 設定追加で十分か、それとも build/push 並列度を下げるべきか

## Updates

- 2026-05-26: GitHub live state と current `origin/main@e5ed74380b6a18bb3d1e7d5f6408c7f4b3b55381` を照合し、残存 `[BUG]` 5 件のうち `#731` が stale 寄りで、他 4 件が現役論点として残ることを整理
- 2026-05-26: `#478` は解法が禁則処理実装か HTML tooltip 再設計に限られ、コストに対する効果が小さいため、bug というより改善 feature 寄りの低優先先として扱う判断を追記
- 2026-05-26: `#478` から `bug` ラベルを外し、live state 記述も「`[BUG]` title は残るが label は外れた」状態へ更新
- 2026-05-26: Browser で `http://localhost:3000/example` を fullscreen 表示し、viewport `360x520` 相当まで縮めると `fullScreenButtons` (`x=284..340, y=20..70`) と hover text が重なる座標を少なくとも 7 点確認した。`420x720` では明確な overlap は出にくく、極小 viewport 条件で再発しやすい edge case と観測した
- 2026-05-26: viewport を複数再確認したところ、desktop hover 前提の観測では `390x844` で overlap 4 件、`393x852` で 5 件、`412x915` で 3 件、`430x932` では 0 件、`360x640` で 8 件、`360x520` で 7 件だった。したがって「かなり小さい画面ほどだけ」ではなく、一般的なスマホ幅相当でも右上 hover が発生する条件では overlap しうる。ただしこれは touch 操作の再現ではなく、mobile-sized viewport 上で mouse hover を当てた観測である
- 2026-05-26: `#121` の再観測として portrait / landscape / desktop を比較したところ、portrait では annotation 自体は bounds 内に収まるが、249px 幅ラベルが狭い画面に対して大きく、tap tooltip も `390px` 幅中 `363-366px` を占めて上部散布図を大きく覆った。実スマホ寄りには「縦長で壊れる」より「縦長で読みづらく、tap tooltip が広すぎる」問題として現れやすい
- 2026-05-26: 上位検討 issue `#872` を立てたのに合わせて、`#121` と `#283` からも `bug` ラベルを外し、mobile/scatter UX の参考課題として位置づけ直した
