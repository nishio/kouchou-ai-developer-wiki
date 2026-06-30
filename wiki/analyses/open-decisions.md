---
name: open-decisions
summary: "未着地の論点・課題の整理 — 未定／方針決定済み未着手／着手済み未完了の三分類"
type: analysis
sources:
  - meeting-minutes.md
  - github-dev-docs.md
  - source-code.md
  - slack-dev-kouchouai-2026-q1.md
  - pr-824-local-llm-https-observation-2026-05-19.md
  - pr-825-standalone-html-observation-2026-05-19.md
  - report-html-non-web-canonical-decision-2026-05-23.md
  - pr-840-workflow-defaultization-observation-2026-05-20.md
  - current-status-2026-06-30.md
  - azure-demo-visibility-thread-resolution-2026-06-05.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - public-case-page-skeleton-2026-06-30.md
  - report-reading-guide-minimum-wording-2026-06-30.md
  - docs-issue-map-2026-06-30.md
---

[[kouchou-ai]] には進行中の作業が多数あり、`docs/` や [[meeting-minutes]] が断片的に語る状態を新規コントリビュータが追いづらい。本ページでは課題を **3 つの状態** に分類して並べる。

- **A. 未定** — 方向性が定まっておらず議論中、または対立する意見が残っている
- **B. 方針決定済み・未着手** — 何をすべきかは合意があるが、誰も手を付けていない／着手者待ち
- **C. 着手済み・未完了** — コードや PR としては存在するが production パスに乗っていない or マージ未済

「やります」「やりません」を Wiki 自身が判断するのではなく、**現在の合意状態を観測** して整理する。状態が変わったら本ページを更新する。

加えて 2026-05-19 以降は、[[usage-modes]] に合わせて各論点を次の 3 軸でも読む。

- **Web UI** — 非専門家向け運用プロダクト (`admin` / `api` / `public-viewer` / 共有・公開)
- **CLI** — 研究者・データサイエンティスト・agent 向け (`analysis-core` / 中間成果物 / PyPI / 観察用HTML)
- **共通コア** — 両モードに跨る分析品質・provider・出力スキーマ・plugin 基盤

2026-05-17 時点では `gh pr list -R digitaldemocracy2030/kouchou-ai --state open` も参照し、main にまだ無いが open PR として存在する作業を C に含めている。

---

## 2026-06-30 current overlay

このページ本体は 2026-05 の棚卸しを含むため、下の件数や分類だけで現在地を判断しない。2026-06-30 の `work/kouchou-ai/main@d5c9ece`、GitHub live state、議事録、`work/slack-logs/main@341cf80` を合わせた最新の短期未決は次の 4 つである。[[current-status-2026-06-30]]より

1. **公開事例と trust layer の placement**: #564 の公開事例ページ、#696 の誤読防止、#542 の責任所在は、別々の docs issue ではなく「公開事例リスト + レポートの読み方 + 何を保証しないか」の 3 点セットとして扱う必要がある。最小文言案は [[report-reading-guide-minimum-wording-2026-06-30]] にあり、未決なのは canonical copy の置き場所と承認者。
2. **8/2 first demo**: 公式性、viewer demo、deep case のどれを主 artifact にするかが未決。候補は渋谷区 / 宇多津町 / 舞鶴2040 / 奈良 / 八代などに広がったが、source strength と政治文脈を分ける必要がある。[[public-case-page-skeleton-2026-06-30]]より
3. **docs-safe PR 順序**: #876 developer docs、#877 Windows setup、#885 Node runtime 排除、#696/#542 reading guide は、同じ docs 群でも reader contract が違う。次に本体 repo へ出す PR を 1 本選ぶ必要がある。[[docs-issue-map-2026-06-30]]より
4. **Azure demo / SaaS 境界**: 6/5 に viewer 公開と admin 共用は進める方向へ倒れ、1 ヶ月専用試用環境は優先度低、365 日 SaaS は提供主体・責任範囲の整理項目として残った。したがって A2 は「全部未定」ではなく、公開事例 / サンプルレポート / reading guide で参照環境の価値を補う段階に移っている。[[azure-demo-visibility-thread-resolution-2026-06-05]]より

この overlay は下の A/B/C 棚卸しを置き換えるものではなく、2026-06-30 時点で人間の判断を使うと次の作業が動く場所を示す。思考ハブは [[thinking-targets]]。

## A. 未定（合意なし／対立あり）

### A-Web UI

### A1. 散布図の維持 vs 廃止

[[meeting-minutes]] 2025-10-08, 2025-10-01：

- ken-san：「散布図を見て満足する時代ではない、インサイト発見を中心にせよ」
- [[nishio]]：少なくとも 2026-09 の書籍版リリース時点までは現行の散布図を温存する。より良い可視化が見つかれば、まずは併用し、最終的にデフォルトをそちらへ移すこともあり得る、というスタンス。

技術的にも UMAP→クラスタリングは精度トレードオフを抱えており（[[pipeline]]）、代替を [[plugin-system|解析 plugin]] で実装するのか／散布図そのものを縮退させるのか **未決**。

### A2. 静的 HTML のホスト先戦略

非エンジニアユーザが [[deployment|静的書き出し HTML]] をどこに置くかは 2025-04 〜 2026-05 で毎週議論され続けて未着地。候補：

- SaaS ホスト `kouchou-ai.dd2030.org`（[[dd2030]] の体制不足で先送り、anno: 「少なくとも 7 月末まで実現困難」2025-04-09）
- 埋め込み fetch 型 HTML
- BASIC 認証付き Azure ホスティング

「広く使ってもらう」上で最大の摩擦点だが、責任主体が定まらない。

2026-06-01 定例では、developer-quickstart の読者像整理と合わせて **「自治体担当本人 / 組織内デモ役が一番欲しいのは、自分で構築しなくても触れる環境」** という論点が明示された。nishio は少なくとも現 Azure 環境で「見せる」ことは手軽にした方がよいとしつつ、課金して秘密情報を入れて分析する SaaS 本番運用とは別問題として切り分けた。[[meeting-minutes]]より

同じ議論で、1 つのインスタンスに複数ユーザの秘密情報を入れるのは避けるべきで、やるならユーザごとに現 Azure デモ環境相当を丸ごと複製する方向が示された。一方、ユーザに admin を触らせず、データ投入は運営側が行い、report viewer だけ見せる案も出たが、admin 画面で試行錯誤する体験自体に価値があるかどうかは未決のまま残った。[[meeting-minutes]]より

2026-06-04 に nishio が dd2030 Slack で Ohki さん宛に 4 問の具体質問として整理した。(Q1) viewer 公開、(Q2) admin 画面共用 + 「共用環境なので秘密情報を入れないで」明示、(Q3) Github admin (大木さん他) がワンクリックで上げる 1 ヶ月専用試用環境、(Q4) 365 日稼働 SaaS は大木さん不参加の確認、の 4 層。Q3 は「ユーザごとに現 Azure デモ環境相当を丸ごと複製」案を on-demand provisioning + Github admin トリガー + 1 ヶ月期限つき、として具体化したもの。[[azure-demo-public-visibility-proposal-2026-06-04]] / [[nishio-slack-azure-demo-visibility-proposal-2026-06-04]]より

2026-06-05 に大木さんから返答があり、nishio 決定として着地した。**viewer 公開と admin 共用は進める** (前提: container の dd2030 フォールバック `OPENAI_API_KEY` を外す。公開時に「共用 / 機微情報禁止 / データ保存・継続稼働非保証」の 3 点明示)。**1 ヶ月専用試用環境は優先度低**で保留し、代わりに「公開事例 / サンプルレポート / サンプル CSV を見せる導線の充実」が自治体ユーザ向けの優先方向となった。**365 日 SaaS は提供主体・責任範囲の整理項目化** とし、責任を持って継続運用・サポートできる主体を立てる方向で未着地のまま残す。あわせて、デモ環境の現時点の価値は「自分たちのデータを投入して試す場所」よりも「使い方や準備すべきデータを理解するための参照環境」として見直す再フレームが出ている。[[azure-demo-visibility-thread-resolution-2026-06-05]] / [[azure-demo-public-visibility-proposal-2026-06-04]]より

### A3. DB 導入のタイミング

[[meeting-minutes]] 2025-05-21, 2025-06-25 で毎回「v4.0 のあたり」と言いつつ毎回先送り。**ファイルストレージ継続が暗黙の現状維持**。SQLite 候補が [[nasuka]] の cluster-title 編集 (PR #545) で検討されたが採用されず。

### A4. private-by-default にすべきか

[[meeting-minutes]] 2025-04-23 / Issue #341：YouTube 風 unlisted は PR #500 で実装済み。ただし **「unlisted default」と「private default + unlisted opt-in」のどちらが正しいか** は議論残存。

### A5. 多言語 i18n の扱い

[[meeting-minutes]] 2026-01-26：「v5.0 リリースは日本語ユーザにフォーカス」が方針だが、Polis など外部ツール への plugin 経由ブリッジは "maybe"。**英語版書籍／英語ユーザベース** との関係はオープン。

### A6. レビュー／マージ基準

[[meeting-minutes]] 2025-05-07 〜：「壊れても OK」スタンスは採用されたが、[[ohki-shingo]] のレビュー困難度マトリクス（A: スキルセット / B: 工数 / C: 環境 / D: 基準なし）は分類どまり。**具体的なマージ基準** は PR テンプレ以上には固まっていない（[[contributing]]）。

### A7. モバイルでの散布図表示

[[meeting-minutes]] 2025-07-30（チームみらい 61 レポート運用フィードバック）：30,000 点散布図のスマホ表示は構造的に難しい。「共有時にズーム済みビューを送る」の部分解決のみで根本未定。

2026-05 の追加論点として、**スマホでは散布図を最初から interative chart として出さず、静的画像やサムネイルで提示し、タップ時だけ全体インタラクティブビューに遷移させる** 案がある。これは PC 向けの wheel / hover 問題とは別設計にできる一方、画像生成コスト、遷移先 UI、アクセシビリティ、共有 URL 設計を伴うため未着手。[[chart-scroll-ux-decision]]より

### A8. パブコメ攻撃対策のステップ 3〜4

[[meeting-minutes]] 2025-03-26, 2025-04-23：4 段階対策（効率化 → 検証可能性 → フィルタリング → 認証）のうち、**ステップ 1-2 のみ着手**（[[nishio]] の `pubcom-seiri` 等）。3-4 は未定。

### A-CLI

### A9. ipynb 研究の置き場所

[[meeting-minutes]] 2025-10-08 で [[nishio]] の「A: ipynb / B: CLI / C: WebUI / D: ホスト型デモ」分類は議論されたが、リサーチ ipynb をリポジトリ内のどこに置くか／別リポジトリにするか **未決**（現在は外部 `nishio/broadlistening-research/` などに散在）。

### A-共通コア

### A10. 可視化 plugin の Python 化

[[plugin-system]]：`docs/development/why-plugin-system.md` は「3 軸目」として可視化を挙げるが、**バックエンド側に Python plugin システムは存在しない**。フロント側 `apps/public-viewer/` の ChartType extensible 化（commit `05b6c11`）が先行している。バックエンド／フロントどちらで提供するかの設計判断は未決。

### A11. 「LOCAL LLM」というカテゴリ名

[[gotchas|2026-05 の HTTPS バグ]]を受けて「`LOCAL` という命名が実装にバイアスを与えていた」教訓があるが、リネーム提案までは至っていない（[[llm-providers]]）。

### A12. 広聴AI紹介論文の投稿戦略

[[kouchou-ai-paper-draft-strategy]]で整理した通り、広聴AIを紹介する論文を書く価値自体は高いが、**日本語論文を主成果物にするのか、英語投稿を主成果物にするのか** は未決である。Polis / vTaiwan 型の制度・プロセス記述に寄せるのか、Birdwatch / Community Notes 型の評価論文に寄せるのかでも必要データが変わる。[[kouchou-ai-paper-draft-strategy]]より

---

## B. 方針決定済み・未着手

### B-CLI

### B1. `extraction.skip: true` オプション

[[meeting-minutes]] 2026-05-18 見出し：「整形済みデータで extraction を skip したい」を [[nishio]] が AI からの示唆で発議、合意感あるが PR は未提出。複数回希望されているが手付かず（[[gotchas]]）。

### B2. クラスタ数のデフォルト自動算出

[[meeting-minutes]] 2026-05-18 見出し：「クラスタ数を optional にし、データ件数から `∛n` で自動算出」方向で合意。`PR #832` は merge され、`analysis-core` で `cluster_nums` 未指定時に extraction 後の `argument` 数から cube-root rule を使う実装が入った。したがってこの項目は **「未着手」ではなく一旦着地済み**。  
残る open question は、README / getting-started / how-to-use の「コメント数ベース」説明を `argument` 数ベースへ揃えるかどうか、と読む方が正確。詳細は [[auto-cluster-defaults]]。

### B3. PyPI リリース運用の硬化

`analysis-core-v*` tag push 起点の `.github/workflows/publish-analysis-core.yml` は current `main` にあり、`analysis-core-v0.1.2` で publish success も観測済み。したがって「自動 publish が無い」は古い。  
未完なのは、`apps/api` 互換テストまで release gate に入れるか、`PYPI_API_TOKEN` 維持のまま行くか Trusted Publishing へ寄せるか、package slimming 後の release gate をどこまで厳しくするか、という **運用の硬化** である。[[pypi-auto-release-requirements]]より [[pypi-release-trigger]]より

なお「tag 付けまで自動化するか（merge to main で自動 release するか）」については、2026-05 時点では **しない方が良い** と整理した。0.1.x 段階で破壊的変更が頻繁なこと、release gate が package 内 test のみで `apps/api` 互換まで張れていないこと、書籍リリース等で release 時期を握りたいことが理由。先にやるべきは Trusted Publishing 移行と TestPyPI 経路の整備。[[pypi-release-timing-automation]]より

### B7. 外部 `plugins/analysis/` ディレクトリの実利用

loader (`plugin/loader.py`) は `Path.cwd() / "plugins" / "analysis"` と `ANALYSIS_PLUGINS_PATH` 環境変数を探す実装になっているが、リポジトリにこのディレクトリは無く、外部 analysis plugin の同梱もゼロ。**枠だけ用意して利用例なし**。

### B8. `--without-html` / `--skip-interaction` argparse バグ修正

[[cli]]：`action="store_true"` + `default=True` で CLI から False に戻せない問題。**既知だが修正未着手**。修正方針自体は単純（`store_false` 化など）。

### B-Web UI

### B9. `packages/ui-shared/` 共有 UI パッケージ

歴史的には refactoring phase docs と `naming_convention.md` に計画記載があったが、current source tree に残るのは `naming_convention.md` のみで、**ディレクトリ自体は未作成**。`apps/public-viewer/` と `apps/admin/` の共通コンポーネント整理（Issue #586）と紐づくはずだが進んでいない。

### B-共通運用

### B10. ルート `CHANGELOG.md` 整備

`docs/development/pypi-release.md` などからの参照はあるが、**ファイル自体が存在しない**。バージョン履歴は git log のみ。

### B11. CodeRabbit 運用の深掘り

`main@3809a7a` には既に **`.coderabbit.yaml`** があり、`reviews.auto_review.drafts: true` の最小設定は入っている。したがって「未配線」は古い。  
一方で、レビュー対象の絞り込み、除外ルール、コメント運用方針はまだ薄く、**導入後の運用設計** は詰め切れていない。

### B12. YAML ベース workflow 定義

`packages/analysis-core/src/analysis_core/plugin/loader.py` は YAML manifest を読む実装になっているが、実態の workflow は `workflows/hierarchical_default.py`（Python のみ）。current source tree に YAML workflow 定義の実例はない。

### B13. PR レビュー責任の AI 生成 PR への拡張

[[coding-agents]]：Devin / Copilot Agent の PR をどこまで人間が引き取るかの線引きは PR テンプレ以上に明文化されていない。draft 扱い＋ CLA 範囲は決まっているが、**マージ判断者の責任範囲は曖昧**。

### B14. LLM grouping 系 LLM 分類の互換枝

[[slack-dev-kouchouai-2026-q1]] 2026-02-11, 2026-02-25：**まずは `extraction, embedding` の後ろで LLM クラスタリングに分岐する** 方針が語られている。理由は、既存のパイプラインや可視化との両立を保ったまま分析プロセス切り替え部分を検証したいから。

同 source ではさらに「既存のカテゴリーツリーをパラメータとして与える亜種」も明示されており、自治体の予算カテゴリに合わせたいという具体的ニーズがある。**意図はかなり明確だが、main / open PR にまだ対応実装は見えない**。

2026-05-18 時点では open PR `#827` が source repo ルートに `PLAN_llm_grouping_capabilities.md` を追加し、`analysis_mode=llm_grouping`、`analysis_capabilities` 自動導出、viewer 側 `requirements` 判定まで含む段階計画を具体化している。したがって **「意図しかない」段階は脱したが、なお doc-only で実装未着手** と見るのが正確。[[pr-827-llm-grouping-capabilities-plan-2026-05-18]]より

---

## C. 着手済み・未完了（実装あり／production 未到達）

整理のため Phase 進行中／PR 出てる項目もここにまとめる。詳細は [[refactoring-status]]。

### C-Web UI

### C1. PR #824 — LOCAL LLM の HTTPS 対応

`PR #824` は 2026-05-18 に merge 済みで、current `packages/analysis-core/src/analysis_core/services/llm.py` は `local_llm_address` に full URL を受け取れる helper と `LOCAL_LLM_API_KEY` 対応を持つ。`apps/api/src/services/report_launcher.py` も analysis 実行自体はこの `analysis-core` を subprocess 起動するため、**実際の分析経路は current `main` で HTTPS/full-URL 対応済み** と読める。[[pr-824-local-llm-https-observation-2026-05-19]]より

ただし current `apps/api/src/services/llm_models.py` の `/admin/models` 用 LocalLLM model list probe はなお `host:port` + `http://.../v1` 前提で、admin 画面のモデル取得 UX は full URL gateway に追随していない。したがって「基幹処理は完了、admin 補助経路は未統一」という意味で C に残すのが近い。[[pr-824-local-llm-https-observation-2026-05-19]]より

### C-共通コア

### C2. フロント側可視化 plugin 基盤

`apps/public-viewer/components/charts/plugins/` に registry / types / validation と built-in plugin (`scatter`, `treemap`, `hierarchy-list`) がある。**基盤自体は既に main にある**。  
未完なのは、外部 plugin ロードやバックエンドの「第 3 軸」としての統一設計まで含めた完成形。

---

## 進行のスナップショット（2026-05 時点）

| カテゴリ | 件数 |
|---|---|
| A. 未定 | 11 |
| B. 方針決定済み・未着手 | 11 |
| C. 着手済み・未完了 | 2 |

「決まったが手が無い」(B) が最多、というのは **コントリビュータ募集をかける際にここから候補を引くと効率的** であることを示唆する。加えて [[usage-modes]] の軸で見ると、Web UI 専任の人は A-Web UI / B-Web UI / C-Web UI を、分析コア寄りの人は A-CLI / B-CLI / C-共通コア を優先的に追うと読みやすい。

## 観測手順

このページのステータスは状況依存。月単位で見直すには：

1. [[meeting-minutes]] の最新数回をスキャン（特に「Open Questions」や「次回に向けて」項目）
2. main の tip と PR 一覧（`gh pr list -R digitaldemocracy2030/kouchou-ai`）を確認
3. current source tree と [[refactoring-status]] を照合し、削除済みの phase docs を前提にした stale claim が残っていないかチェック
4. 該当する [[refactoring-status]] と本ページを同期して更新

## Updates

- 2026-06-30: [[current-status-2026-06-30]] をもとに current overlay を追加し、#564/#696/#542 trust layer、8/2 first demo、docs-safe PR 順序、Azure demo / SaaS 境界を短期未決として明示。
- 2026-05-17: 初回作成 — 議事メモ＋コードリーディング結果を 3 分類で整理
- 2026-05-17: `main@3809a7a` を再確認し、CodeRabbit は「未配線」ではなく最小導入済みへ修正
- 2026-05-17: `apps/api/src/services/report_duplicate.py` / `docs/user-guide/reuse-report.md` / admin UI を確認し、レポート再利用機能は C から除外
- 2026-05-17: 可視化 plugin 基盤は frontend 側で実装済み、LOCAL LLM HTTPS は main では未完了寄りに補正
- 2026-05-17: `gh pr list` で open PR を確認し、C カテゴリが「main 未反映だが open PR に存在するもの」を含むことを明記
- 2026-05-17: `#2_開発_広聴ai` ログから、LLM grouping 系 LLM 分類の互換枝と taxonomy-guided 亜種を B に追加
- 2026-05-18: A7 に、モバイルでは「静的画像 → 全体インタラクティブビュー」案も候補であることを追記
- 2026-05-18: PR `#827` により、LLM grouping 系 LLM 分類の互換枝は doc-only の計画 PR として具体化した、と B14 を更新
- 2026-05-19: `PR #825` / `PR #824` merge 後の current `main@55e93e1` を確認し、前者は CLI 観察用HTMLと Web 主経路を分けて整理し直し、後者は analysis 実行完了だが `/admin/models` が旧前提のまま、と補正
- 2026-05-19: [[usage-modes]] に合わせ、各状態の中を Web UI / CLI / 共通コア の読み筋でグルーピング
- 2026-05-21: Phase 3b の完了判定を議論しやすくするため、[[phase3b-exit-criteria]] への導線を追加
- 2026-06-01: A2 に、自治体担当本人 / 組織内デモ役向けの Azure 体験環境 priority、秘密情報を扱う SaaS 本番運用との切り分け、ユーザ単位環境複製 vs viewer-only デモ vs admin 試行錯誤体験の未決論点を追記
- 2026-05-21: `main@0e1552d` を確認し、PR #840 相当 merge 後は Phase 3b を B から除外。残課題は Phase 8 / extras 分割 / status semantics follow-up 側へ移ったと整理
- 2026-05-21: `main@42d2afb` で PR #843 merge を確認し、B4 の extras 分割を除外。あわせて open PR `#844` の analysis-core CLI preflight を C4 として追加
- 2026-05-21: `main@5d591ef` で PR #844 merge と Issue `#836` / `#837` close を確認し、C4 の analysis-core CLI preflight 項目を除外
- 2026-05-23: maintainer 判断 [[report-html-non-web-canonical-decision-2026-05-23]] を反映し、`report.html` の Web canonical 化を open decision から外した
- 2026-05-24: `work/kouchou-ai/main@e5ed743` を確認し、legacy cleanup merge 後は Phase 8 が open decision ではなくなったため B5 を除外。current tree から消えた phase docs への参照も補正
- 2026-05-25: A1 の [[nishio]] スタンスを訂正。「チームみらい等の宣伝用途」という外部顧客像に紐づけた表現は不適切で、実際は「少なくとも 2026-09 書籍版リリース時点までは温存」「より良い可視化が見つかれば併用→デフォルト切替も可」という時間軸のある立場である
- 2026-06-04: A2 に [[azure-demo-public-visibility-proposal-2026-06-04]] への接続を追記。nishio が Ohki さん宛に Slack で 4 問 ((Q1) viewer 公開 / (Q2) admin 共用 + 秘密情報禁止明示 / (Q3) Github admin ワンクリックの 1 ヶ月専用試用環境 / (Q4) 365 日 SaaS 不参加確認) として decompose した
- 2026-06-05: A2 に [[azure-demo-visibility-thread-resolution-2026-06-05]] による着地を追記。viewer 公開と admin 共用は進める (前提: container の dd2030 フォールバックキー除去、3 点明示文言)、1 ヶ月専用試用環境は優先度低 + 公開事例導線が代替方向、365 日 SaaS は提供主体・責任範囲の整理項目化、デモ環境の価値は「参照環境」へ再フレーム
