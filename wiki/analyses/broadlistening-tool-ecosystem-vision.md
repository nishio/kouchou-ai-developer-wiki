---
type: analysis
summary: "広聴AI Web UI を simple な default モードに絞り、CLI に多様な実験機能を追加し、新しい分析手法が試行錯誤され共有されるコミュニティを育てる、という二段構造のエコシステムビジョン。analysis-stance で『別ツールで補完』とした空き地に対する nishio の答え"
sources:
  - slack-stance-discussion-2026-05-30.md
  - analysis-stance.md
  - usage-modes.md
---

## 結論

広聴AI のツール戦略は **二段構造のエコシステム** として設計する。

- **Web UI**: 全体傾向把握ユースケース一本の simple モード。デフォルトで「デカい見落とし / デカい違和感を見つける」ビューを提供し、設計判断は反応事後誘導型に倒す
- **CLI / analysis-core**: 実験機能の追加場所。tokoroten の DivCon、Long Context 再分類によるマッピング不能抽出、ユーザカスタム prompt 経路、KJ #3/#4/#5 系の補完 artifact など、多様な手法を実験できる空間
- **コミュニティ**: CLI で試行錯誤された新しい分析が共有・比較・継承されるコミュニティを育てる

これが [[analysis-stance]] / [[label-quality-redesign-reset-2026-05-30]] で「別ツールで補完」「少数重要論点系は CLI 分析者責務」と整理した空き地に対する設計上の答えになる。[[slack-stance-discussion-2026-05-30]]より

## なぜこの構造か

### Web UI を simple に絞る理由

[[analysis-stance]] が言語化したとおり、広聴AI = 構造把握装置で、reader は「自分の事前 mental model と突き合わせて構造を読み、他者に解説する」主体である。ところが Web UI の主たる reader (政策担当 / 自治体 / 一般ユーザ) は、自分のしたいことを「全体傾向把握 / 少数論点発見 / 構造把握 / 詳細探索」のような解像度で区別できない。したがって `(やりたいこと)` を選ばせる UI は機能しない。[[slack-stance-discussion-2026-05-30]]より

代わりに、**default mode を提供 → 反応を見て別 view を案内する** という事後誘導型 UX に倒す。「ざっくりモード / 詳細モード」程度の切替は用意しうるが、選択を強制しない。

### CLI を実験機能の場所にする理由

データサイエンティスト的な素養を持つ分析者は、ユーザのデータを直接観察し、「重要とは何か」を言語化し、適切な手法を選べる。Web UI に複雑機能を載せると、(1) 一般ユーザの simple さを壊し、(2) 分析者の自由度も逆に下げる。両立しない。

CLI は分析者向けなので、複雑機能を載せても simple さは壊れない。tokoroten が提案した Long Context 再分類による少数意見救出、DivCon 由来の自治体カテゴリ突合、ユーザカスタム prompt による「重要」定義の言語化、ohki-shingo 公開UI 7 要件のうち #5 #7 を担う実験 artifact、などすべて CLI 機能として実装できる。[[slack-stance-discussion-2026-05-30]]より

### コミュニティを育てる理由

「DivCon を広聴AI の WebUI に搭載するのは複雑すぎる」という理由で DivCon 方向の発展が抑制されている、と nishio は観察している。これは Web UI と CLI の二段構造を維持しつつ、CLI 側の実験が **共有・比較・継承される場** がないと結局単発で終わる、という構造的問題を示す。[[slack-stance-discussion-2026-05-30]]より

したがってツール戦略の第三層として「**新しい分析が多種多様に試行錯誤されて共有されるコミュニティ**」を育てる必要がある。これは技術ではなく場と運営の問題で、product 単体では解けない。

## 直近で示唆される具体アクション

エコシステムビジョンの実装着手点として、現時点で見えるもの:

- **default mode の具体形** を「デカい見落とし / デカい違和感を見つける」ビューとして定義し、これと「詳細モード (上位 cluster 30 程度 + ツリービュー)」を Web UI 上で切替可能にする (新規 issue 候補)
- **サンプル分析結果カタログ**: 同じ入力データを複数手法 / 複数 cluster 数で分析した結果を並べて見比べられる教育コンテンツ。ユーザが「どっちを選んだらいいですか」と聞いてきた時の補助になる
- **DivCon / Long Context 再分類 / カスタム prompt** の CLI 機能化のスコーピング (tokoroten / 別 contributor との連携)
- **コミュニティ場の整備**: GitHub discussions、Zenn / note、Slack 等で「自分の分析を共有する」型のコンテンツを促す仕組み

## Open Questions

- 「コミュニティ」は具体的にどの場でどの形でやるか (GitHub discussions / Slack / 別 forum / 書籍 13 章末尾の cookbook?)
- CLI 実験の入り口 = `kouchou-analyze` だけで足りるか、ipynb / Jupyter 経路も同等に整える必要があるか ([[open-decisions]] A9 と関連)
- サンプル分析カタログをどこに置くか (docs サイト / 別 repo / Web UI 内ギャラリー)
- 「ざっくり / 詳細」モード切替を Web UI に入れる時、命名と分かりやすさのバランス (`(やりたいこと)` 言語化の難しさを考えると、ラベルを工夫しないと「どっちを選べばいい」問題が再現する)

## Updates

- 2026-05-30: 初版。[[slack-stance-discussion-2026-05-30]] で nishio が言語化した CLI + コミュニティビジョンを、[[analysis-stance]] / [[label-quality-redesign-reset-2026-05-30]] が残した「別ツールで補完」の空き地に対する答えとして整理
