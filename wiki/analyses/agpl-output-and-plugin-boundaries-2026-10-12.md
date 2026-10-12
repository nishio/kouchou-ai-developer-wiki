---
type: analysis
summary: "AGPLの生成データ公開は原則としてソース提供義務を生まないが、コード入りHTMLと結合プラグインは別判断。独立プラグインや互換ライセンスの選択と、結合物としての義務を分ける"
sources:
  - analysis-core-license-history-2026-10-12.md
  - source-code.md
  - https://opensource.org/license/agpl-3-0
  - https://www.gnu.org/licenses/gpl-faq.en.html
---

## 問いと位置づけ

2026-10-12、ユーザーから「AGPLツールで生成したデータのWeb掲示にはソース公開義務がないか」「他の人が作るプラグインをAGPLにする義務はないか」と質問。AGPLを正とする確認は [[analysis-core-license-history-2026-10-12]]より。本ページは条文・FSF解説と現行コードを突き合わせた一般的整理で、個別の法的結論や新しいライセンス例外の承認ではない。

2026-10-12に本体をfetch/pullしmain `c297bc97bb2bbce42964a90d7501c2d3592aeaf0` を確認。open PR一覧ではライセンス訂正PR #970は未merge。AGPL本文はOSI掲載の全文とrepoのLICENSEを参照。GNU FAQの直接取得はtimeoutしたが、公式ページの検索結果から `GPLOutput` / `GPLPlugins` / `GPLAndPlugins` の本文抜粋を確認した。

## Q1: 生成データだけの公開なら原則その理解でよい

[AGPL第2条](https://opensource.org/license/agpl-3-0)は、出力がその内容上AGPL対象著作物となる場合に限り、出力にも適用されると定める。単に解析にAGPLソフトウェアを使っただけで、結果データや独自の掲示サイトがAGPLになるわけではない。[GNU FAQ: GPLOutput](https://www.gnu.org/licenses/gpl-faq.en.html#GPLOutput)も、入力の変換結果とプログラムの実質的な部分をコピーした出力を区別する。

例として、手元でCSVを分析し、生成したJSONを自作サイトで表示するだけなら、その事実だけを理由に分析ツールの改造ソースやサイトのソースを提供する義務は生じない。入力データ・第三者素材などの権利は別問題。

ただし広聴AIの `report.html` はデータだけではない。`packages/analysis-core/src/analysis_core/steps/hierarchical_visualization.py` は `_TEMPLATE.format(...)` でHTMLを生成し、表示・操作用JavaScriptも埋め込む。公開する物がこのHTMLやpublic-viewerの配布物なら、含まれるプログラム部分のライセンス条件を確認する必要がある。これはコード内容からの注意点であり、出力データ自体を一律AGPLとする判断ではない。[[source-code]]より。

改造したAGPLプログラム自体をネットワーク越しに利用させる場合は[第13条](https://opensource.org/license/agpl-3-0)の別の論点。条件を満たす利用者にCorresponding Sourceを取得できるようにする義務であり、結果の静的掲示とは区別する。対象は対応するプログラムのソースで、あらゆる周辺システム・入力データを一律に公開するという意味ではない。

## Q2: 一律AGPL必須ではないが、一律に制約なしでもない

[GNU FAQ: GPLPlugins / GPLAndPlugins](https://www.gnu.org/licenses/gpl-faq.en.html#GPLPlugins)は、独立したプログラムか、共有アドレス空間の関数呼び出し・データ構造の共有等を通じた一体のプログラムかで扱いを分ける。これはFSFのGPL解釈であり、AGPLでも第5条の結合物の条件と第13条を合わせて検討する材料になる。

- **独立プログラム**: 生成JSONを読む独自viewerなど、本体コードを取り込まず独立して動くものには、本体AGPLであることだけを理由にAGPLを要求しない。
- **一体となる拡張**: 配布時には結合物全体としてAGPLの条件を満たす必要がある。プラグインのオリジナルな部分をMIT等の互換ライセンスで提供する余地はあるが、それにより結合物のソース提供義務を消せるわけではない。本体のAGPLコードをコピーした部分を勝手にMIT化する意味でもない。
- **作成・手元での私的実行**: それだけで全世界公開の義務にはならない。配布や、改造版のネットワーク利用を提供する時の条件を別に判断する。

現行analysis pluginは `plugin/loader.py` がimportlibで同一プロセスに読み込み、`AnalysisStepPlugin` を要求する。`plugin/decorator.py` のrunは `StepContext` / `StepInputs` / configを渡して関数を直接呼ぶ。したがって、この実装を「プラグインという名前だから独立」と説明するのは適切でなく、FSFの整理では一体の拡張に近いと考えられる。これは実装からの推論で、法的境界の確定ではない。[[source-code]]より。

## 今後の説明・設計の候補（未決）

- データの利用、コード入り成果物の配布、AGPLソフトウェアのサービス提供をFAQで分ける。
- 第三者拡張を促す際は「AGPLまたは互換ライセンスで提供できる拡張」と「独立した外部ツール」を分け、非公開の結合プラグインが無条件で許されるとは案内しない。
- 非公開拡張まで許す方針を採りたい場合は、独立した外部ツールとしての境界設計や、権利者が許諾できる範囲での例外条項を別途検討する。単にHTTP / subprocessに変更しただけで独立性が確定するわけではない。

## Open Questions

- コード入り `report.html` / 静的viewerについて、現在のlicense notice・対応ソース導線が適切か。今回、充足性の監査まではしていない。堅牢性の既知の残件は Issue #978（後述の Updates 参照）。
- プラグインの結合度・コード由来に応じた実際の配布条件と、プロジェクトとして案内するライセンス方針。
- 例外条項を設けたい場合の必要性と権利範囲。AGPL訂正指示は例外許諾を意味しない。

## Updates

- 2026-10-12: 初版。条文、FSF解説、mainのplugin loaderとHTML生成を確認して質問への回答を記録。本体やPR #970の内容は変更していない。

## Updates — 2026-10-12 義務が生じる条件の補足

ユーザーの「そもそもサービスを提供する場合は、ということだよね」という指摘を受け、前の回答の表では条件が省略されていた点を訂正する。「一体で動く」だけで直ちにソース公開義務が生じるわけではない。

- 手元でプラグインを作成・結合し、自分で実行するだけなら、それだけでソース公開義務は生じない。結果データだけを掲示・納品する場合も、前述Q1の条件で扱う。
- プログラムまたはその派生物を他者へ配布・納品する場合には、第4〜6条の配布条件を検討する。サービス提供だけが発生条件ではない。
- プラグインとの結合物が改造版に当たり、その改造版をネットワーク越しに利用させる場合は、第13条により当該利用者への対応ソース提供が必要になる。有料・一般公開のSaaSに限る条件ではない。

根拠は[AGPL第2条・第4〜6条・第13条](https://opensource.org/license/agpl-3-0)。ソース提供の対象は受領者・該当利用者であり、常に全世界へ公開する義務という意味ではない。前述の「非公開拡張」の設計論は、配布・ネットワーク利用提供を行う場合の検討で、私的なローカル実行まで禁止する趣旨ではない。

## Updates — 2026-10-12 利用者向け解説の所在

最新化後のmain `c297bc9` のREADME各言語版、docs、analysis-core README、CONTRIBUTING、skillsを検索し、`docs/user-guide/faq.md` の全文も確認した。Q1/Q2と義務発生条件を利用者のケース別に説明する文書は見つからなかった。既存FAQは「開発者向けFAQ」でAPI接続エラーへの対処のみ。CLAは貢献者との契約で、この利用者向け説明を代替しない。公開docsサイトの直接取得は失敗したため、これはmainの文書ソースについての観測である。

外部の参照先として[GNU公式FAQ日本語版](https://www.gnu.org/licenses/gpl-faq.ja.html)があり、`WhatCaseIsOutputGPL` / `GPLOutput` / `GPLPlugins` / `GPLAndPlugins` で出力とプラグインを扱う。公式検索結果で本文抜粋を確認。一般GPLの説明を含むため、AGPL第13条のネットワーク利用条件を併読する必要がある。広聴AIの一般利用者向けには、手元で分析・結果データの掲載納品・自作プラグインの私的利用・プログラムの配布/サービス提供・コード入りHTML、のケース別FAQが不足している。今回そのFAQの本体追加は行っていない。

## Updates — 2026-10-12 出力HTML公開の利用者向け説明案

「出力HTMLには、分析結果のデータと、それを表示・操作するプログラムが一緒に入っています。HTMLは公開できます。表示プログラムの著作権・ライセンス等の案内を保ち、対応するソースコードを入手できるようにしてください。表示プログラムを変更した場合には、変更後のソースと変更の説明も必要です。元CSVや分析用の自作プラグインまで一律に公開する、という意味ではありません。」という説明案を整理した。

根拠は[AGPL第1・2・4〜6条](https://opensource.org/license/agpl-3-0)。対応ソースには、配布するプログラムを変更・生成するために必要なテンプレートや生成手順等が含まれる場合がある。「GitHubのトップページを貼れば常に十分」「出力HTMLを公開すれば必ずソース提供も完了」とは断定しない。

製品側の改善案として、生成HTMLに著作権・ライセンス・無保証の案内と必要なライセンス本文、生成版に対応するソースの取得導線を自動付与すると、通常利用者はそれらを残して公開すればよい形にできる。変更した表示コードは変更版の取得先に合わせる必要がある。これは未実装の提案であり、現行HTMLに案内が揃っているとの確認ではない。

## Updates — 2026-10-12 CLI側で案内・対応ソースを自動同梱（PR進行中）

西尾さんの「やさしい解説ドキュメントを作って」「CLI出力HTMLにライセンス案内が入るべき」という指示を受け、[PR #970](https://github.com/digitaldemocracy2030/kouchou-ai/pull/970)（`fix/analysis-core-agpl-license`、`d09976e`）に実装した。上記の未実装・文書未整備という観測はmainについては引き続き該当するが、PRには以下の変更がある。[[analysis-core-license-history-2026-10-12]]より。

- [利用者向けガイド](https://github.com/digitaldemocracy2030/kouchou-ai/blob/d09976e/docs/user-guide/license.md)を追加し、README・利用ガイド・プラグインガイド・ドキュメント目次から案内。手元利用、結果データ、HTML、拡張、配布・ネットワーク利用をケース別に説明する。
- `report.html` の末尾に「ライセンス・表示プログラムのソース」を自動付与。AGPL全文・無保証の説明・元プロジェクトへのリンクと、生成に使った表示ソースをZIPでHTML内へ埋め込む。通常利用者は案内とダウンロード機能を残して公開する運用とする。

## Updates — 2026-10-12 PR #970 の HTML 案内に対するフォローアップ Issue

- [Issue #978](https://github.com/digitaldemocracy2030/kouchou-ai/issues/978)（open・低優先）: 上記 PR #970 の `report.html` ライセンス案内実装（`hierarchical_visualization.py` の `_report_license_notice`）は、ライセンス資源（wheel 同梱の `AGPL-3.0.txt`、または editable/source 実行時の repo `LICENSE` フォールバック）が見つからないと `FileNotFoundError` を raise し、**`report.html` 生成全体がライセンス資源の存在に hard-fail で依存**する。現行 wheel 構成では顕在化しないが、将来 packaging から force-include が落ちた場合や旧 wheel をクリーン環境へ入れた場合に壊れうる。方針は「資源欠如時は案内を link-only へ degrade し hard-fail を回避」。
- 位置づけ: PR #970（repo 側 AGPL 訂正＋案内同梱）とは別の堅牢性 Issue で、上の Open Questions「現在の license notice・対応ソース導線が適切か」に対応する具体的な残件。本 wiki はこの issue の存在を記録するのみで、本体コードは変更していない。別途の PyPI 訂正版公開（version bump ＋ tag）と旧 0.1.0/0.1.2 の扱いは [[analysis-core-license-history-2026-10-12]] / [[analysis-core-license-intent-2026-10-12]] で追跡。
- ZIPは実際の `hierarchical_visualization.py`（HTML/CSS/JSテンプレートを含む）、AGPL本文、実行方法の3ファイル。結果データ・入力CSVをZIPには含めず、更新されるmainへのリンクや、改造前のタグとの不一致を避ける。生成済みHTMLのJS直接編集はZIPと不一致になるため、表示ソースから再生成するよう案内する。
- 16件の生成テスト、追加パッケージなしの隔離PythonでZIPから同一HTMLを再生成、改造ソース保存、wheel資源とsdistの同梱、twine、Ruff、docs strict buildを確認。ブラウザー目視はローカルURLがクライアント側でブロックされ未確認。

対象はCLIのHTML生成経路であり、Web版の静的サイト出力は別途確認が必要。未merge・未リリースなので、既存PyPIや過去生成済みHTMLに案内が追加されたわけではない。新CLIで結果JSONから再生成すると案内を付けられる。

## Updates — 2026-10-12 全文表示を短い案内とリンクへ変更

西尾さんの「AGPL全文は長すぎるのでリンクでよい」という指摘を受け、PR #970のHTML末尾を「表示プログラム: 広聴AI · AGPL-3.0 · ソース（ZIP）」と短い無保証・利用条件の注記に変更。ライセンス全文の折りたたみ表示は削除し、GNUの本文へのリンクにした。配布用のライセンス本文は対応ソースZIP内の `AGPL-3.0.txt` として維持する。[AGPL第0条・第4条](https://opensource.org/license/agpl-3-0)の閲覧導線・ライセンス写しと、レポート画面への長文表示を区別した。利用者向けガイドも合わせて更新し、生成16テストとRuffに成功。未merge・未リリース。

## Updates — 2026-10-12 #978 に link-only degrade の PR #980（merge 済み・#978 close）

- 上記 #978 の方針（資源欠如時は link-only へ degrade し hard-fail を回避）を実装した [PR #980](https://github.com/digitaldemocracy2030/kouchou-ai/pull/980) を **2026-10-12 に main merge 済み**（squash `478cd1a0`、CI 全 pass、nishio 判断で admin merge）。これにより **Issue #978 は自動 close**。
- 変更内容: `_report_license_notice` はライセンス資源（sibling `AGPL-3.0.txt` も repo `LICENSE` フォールバックも）を解決できない場合、`FileNotFoundError` を raise せず、GNU 本文へのリンクのみ（ソース ZIP なし）の `_report_license_notice_link_only()` へ早期 return する。happy path（資源あり＝ZIP 同梱）の挙動・文言は不変。degrade path の回帰テストを追加。
- 検証: `pytest tests/test_hierarchical_visualization.py` → 17 passed（新テスト含む、Python 3.12）、変更ファイルの `ruff check` パス。`clustering` optional extra 未導入環境のため `tests/` 全体では当該 extra 依存の 4 件が落ちるが、本変更（stdlib のみの可視化ステップ）とは無関係の環境起因。
- ZIP 同梱の本流（資源あり時）は変えていないので、[[analysis-core-license-intent-2026-10-12]] の運用判断（#979 の yank 方針含む）には影響しない。
