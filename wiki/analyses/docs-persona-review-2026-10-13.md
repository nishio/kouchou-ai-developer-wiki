---
type: analysis
summary: "7 読者ペルソナ（A 閲覧者 / B 自治体担当 / C デモ役 / D WebUI開発者 / E CLI研究者 / F 非日本語話者 / G 方法論・信頼性）を subagent にして、docs 大掃除（v4.1.0）直後の本体 docs をトップページから読ませた usability レビューの synthesis。横断テーマ・quick win・構造的対応を優先度付きで整理。最大の発見は『nav/タイトルのラベル詐称』『閲覧者・実務者向け FAQ/読み方ページ不在』『導入検討者向けの費用・PII・相談先不在』『信頼性・責任所在ページ不在』と、import-quickstart の致命バグ"
sources:
  - docs-reader-coverage-audit-2026-10-13.md
  - kouchou-ai-docs-improvement-roadmap-2026-10-13.md
  - github-dev-docs.md
---

## 何のレビューか

docs 大掃除（Tier 0 + T1、[[kouchou-ai-docs-improvement-roadmap-2026-10-13]]、`v4.1.0`）が landing した直後の本体 docs を、**7 読者ペルソナを subagent にした dynamic workflow** でトップページ（`docs/index.md`）から読ませ、「気になる点」を収集した（nishio 依頼）。[[docs-reader-coverage-audit-2026-10-13]] が 5 読者像 × 機能カバレッジの静的照合だったのに対し、本ページは **実際にページを辿った読者体験**ベースのレビュー。

- 基準: `work/kouchou-ai origin/main@6ad727ee`（v4.1.0・demo-first 目的別ガイド入り）
- ペルソナ: A 閲覧者 / B 自治体担当（非技術） / C デモ役 / D WebUI開発者 / E CLI研究者 / F 非日本語話者 / G 方法論・信頼性・責任（実務者）
- 方法: 各ペルソナが index.md から nav/リンクを辿り、構造化フィードバック（concerns・dead_ends・top_fix）を返す → synthesis agent が横断クラスタリング

## 良かった点（landing した大掃除の効果）

- **目的別ガイド（demo-first router）は全ペルソナに好評**。A/B/C が「自分の行」で迷わず入口を選べたと明記。T1-a が効いている。
- `getting-started/windows-setup.md` の「開発者でない人向け・権限は IT 管理者へ」導線、`license.md` の AGPL 平易説明、`index.md` 免責の正直さ、散布図 3 モードの操作説明（T1-b）も個別に好評。

## 最優先（低コスト・verified）

1. **`import-quickstart.md` L265 の致命バグ**: `clusters_df['cluster-id-lv1']` は実在しない列。正しくは **`cluster-level-1-id`**（`packages/analysis-core/src/analysis_core/steps/hierarchical_aggregation.py:190` で定義、コード内 29 箇所 vs doc の typo 1 箇所）。研究者が最初にコピペする例が確実に `KeyError` で落ちる。理想は UMAP 再計算をやめ保存済み `x/y` 列を読む例にする（レポート座標と一致・再現性も正）。
2. **nav/タイトルのラベル詐称を一括改名**（6 ペルソナ横断の最頻離脱点・編集は軽微）:
   - `インポート方法`（nav）→ 実体は「Python スクリプトからの利用」。`Python API からの利用` に
   - `プロジェクト一覧`（misc/projects）→ 実体は「GitHub Projects ボード運用ポリシー」。`開発ボード運用ポリシー` に（活用事例ではない）
   - experiments `direct_win` → 「Windows 非 Docker セットアップ」と分かる名に（分析実験と誤認される）
   - `model-catalog.md` 冒頭に「本ページは WebUI 管理カタログ保守。CLI の model 指定は cli-quickstart 参照」の読者切り分け注記
   - `web-ui-node-runtime-dependencies` タイトルに「(監査スナップショット/#885)」
3. **`faq.md` は実体が「開発者向けトラブル 1 件」**。4 ペルソナが「ユーザーガイド > FAQ」をクリックして空振り。→ 開発者セクションへ移設（タイトルと中身は一致しているので移動だけ）。

## 高インパクト（構造的・新規ページ）

4. **閲覧者向け『渡されたレポートの読み方』独立ページ**: 現 `how-to-use.md` は冒頭「アプリを立ち上げた後」前提で、閲覧者本文の前に admin/CSV/AI詳細設定（L17-43）、後半に metadata.json/TSX（L84-121）が同居し、非技術者が難語と無関係情報に埋もれる。閲覧者専用ページを作り、「1 点/1 クラスタとは何か・近さと数字（件数/割合）の意味・結果を鵜呑みにしない」を専門用語抜きで。作成者・発行者向けは別ページへ分離。
5. **閲覧者・実務者向け FAQ 新設**（用語の意味 / 信頼性 / 数字の読み方 / 費用 / 個人情報 / 元発言への遡及 / 責任者）。公開ビューアの「よくあるご質問」メニュー（how-to-use が存在を約束）とユーザーガイド双方から導線。
6. **導入検討者（自治体・非技術者）向けページ新設**＋目的別ガイドに行追加。3 点に平易回答: (1) データの扱い＝既定で外部 LLM API 送信 / ollama で手元完結 / PII は庁内規程確認、(2) 費用＝無料 OSS＋API 従量課金の概算目安 / local は追加課金なし（OS ガイド間の課金注記不統一も是正）、(3) 相談先＝serverless 版・非技術者歓迎の窓口・支援者の探し方。`license.md` 冒頭に「利用自体にライセンス料は不要、発生し得るのは API 利用料・インフラ費のみ」の調達向け一文。
7. **信頼性・限界・倫理・責任所在ページ新設**（＝ [[kouchou-ai-docs-policy-history]] の #542 レーンの正統な拡張）。開発者タブ奥に死蔵された優れた注意書き（`opinion-classification` の「読み方の注意」＝サンプリングは代表でない・人手未検証・モデル間比較禁止、`extraction-prompts` の抽出失敗様式）を実務者語で昇格。トレーサビリティ（元発言遡及・原文不改変・全件保持）を信頼の根拠として明示。責任所在は **3 レイヤー**（OSS 開発者 / サービス運営者 / レポート作成者）で記述（#542 の nishio 整理）。「濃い（密度）」の定義と閾値トレードオフも注記。

## 中インパクト

8. **ゼロ構築の最短デモ導線**: サンプルレポートのライブ URL と serverless 版を目的別ガイドの「デモで見せる人」行へ昇格。`quickstart.md` を非開発者ファースト（release zip + `setup_win.bat`）に再構成し、git/docker/pnpm は「開発者向け」へ降格。非開発者向け「デモ用データの準備」ページ（Excel→CSV・UTF-8・comment-body・推奨件数/クラスタ数・個人情報）新設。
9. **CLI 研究者の実行可能性ギャップ**: 上記バグに加え、cli-quickstart に「ローカル LLM を使う」節（`provider: local` + `local_llm_address` + モデル文字列 + `is_embedded_at_local`）と「再現性の扱い」節（seed 固定・一部モデルは temperature 非送信、UMAP は確率的→`reuse_umap_model`、完全一致は非保証）、`config.json` 全フィールドの「設定リファレンス」ページ。experiments 空スタブは補充 or nav 除外。
10. **WebUI 開発者の最初の一歩**: `quickstart.md` のローカル開発節に public-viewer（`.env` / `pnpm install`（Node22・pnpm9.15.4）/ `pnpm dev` / port 3000 / api 未起動時）を追加。フロントアーキ（Key directories）と技術スタック（Next.js15/Chakra/Plotly/Biome）を AI 向け skill でなく `docs/development` に人間向けページ化。nav「開発者向け」20+ 項目を Web UI / API・分析 / プラグイン / 運用 にサブグループ化。アーキ図に static-site-builder（port 3200）追記。
11. **多言語導線の断絶**（F）: `docs/index.md` 冒頭に README.en/ko への言語リンク（GitHub と同じ `[English] | 日本語 | [한국어]`）、主要用語に英語併記、`site_description` 日英併記（quick win）。構造的には README.en/ko を `docs_hooks` で公開サイト複製 or en/ko ランディング化し Material の alternate に載せ、優先ページの英語版 or 各ページ冒頭に英語 TL;DR、`search.lang` を `['ja','en']` へ。
12. **活用事例ページ新設**（G/B/C 共通）: 実際の公開レポート・自治体/政党/NPO 導入例。misc/projects の改名（テーマ 2）とセットで混同解消。

## ペルソナ別の top_fix（1 行要約）

- **A 閲覧者**: 閲覧者専用「レポートの読み方」ページ（アプリ立ち上げ/admin/JSON を混ぜない・数字の意味を平易に）
- **B 自治体担当**: 費用・PII・相談先に答える導入検討ページ、FAQ の作り直し
- **C デモ役**: 最短デモ（サンプル URL/serverless）と非開発者 quickstart、デモ用データ準備
- **D WebUI開発者**: public-viewer ローカル開発手順＋フロントアーキ/技術スタックの人間向けページ
- **E CLI研究者**: import-quickstart のバグ修正＋ローカル LLM/再現性/設定リファレンス
- **F 非日本語話者**: docs 側の言語リンク・英語併記・英語コンテンツ
- **G 方法論・信頼性**: 信頼性・限界・責任所在ページ（dev 奥の注意書きを実務者語で昇格）

## ロードマップへの含意（重要）

persona レビューは **Tier 3 の優先順位を揺さぶる**。[[kouchou-ai-docs-improvement-roadmap-2026-10-13]] は Tier 3 本丸を #876 の `getting-started/` rename としていたが、**読者が実際に詰まるのは rename ではなく上記の content gap**（ラベル詐称・閲覧者/実務者 FAQ・読み方ページ・導入検討ページ・信頼性/責任ページ・CLI バグ）。rename は構造美化として価値はあるが reader impact は相対的に低い。→ **次フェーズは「rename を急ぐ」より「テーマ 1-7 の content を埋める」を優先すべき**。テーマ 7 は #542 の拡張として統合できる。

## Open Questions

- 閲覧者向け読み方ページ / 実務者 FAQ / 導入検討ページ / 信頼性・責任ページは、それぞれ独立ページか、1 つの「使う前に知る」束か。目的別ガイドの行をどこまで増やすか（router 肥大化の懸念）。
- F（多言語）は「docs 側の言語リンク + 用語英語併記」までを quick win とし、英語ページ本体の拡充は別途リソース判断。
- 活用事例ページの出典（公開可能な実レポート URL）をどこから取るか。公開境界（Azure デモ内部は不可）。

## 関連

- [[kouchou-ai-docs-improvement-roadmap-2026-10-13]]: 本レビューは roadmap の Tier 3 優先順位を再考させる現在地フィードバック
- [[docs-reader-coverage-audit-2026-10-13]]: 5 読者像 × 機能の静的カバレッジ（本ページは体験ベースの動的レビュー）
- [[kouchou-ai-docs-policy-history]]: #542 責任所在レーン（テーマ 7 がその拡張）
