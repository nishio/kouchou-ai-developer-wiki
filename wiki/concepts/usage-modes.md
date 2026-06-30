---
name: usage-modes
summary: "kouchou-ai の主要利用モード — 非専門家向け Web UI と、研究者・データサイエンティスト向け CLI / analysis-core を分けて捉えるための整理"
type: concept
sources:
  - meeting-minutes.md
  - github-dev-docs.md
  - source-code.md
  - analysis-core-web-ui-separation-decision-2026-05-23.md
  - pr-825-standalone-html-observation-2026-05-19.md
  - report-html-non-web-canonical-decision-2026-05-23.md
  - meeting-brand-compass-information-strategy-2026-06-30.md
---

## なぜ分けて考えるか

`kouchou-ai` には「同じ解析コアを別の入口から使う」複数モードがある。これを混ぜると、**ある PR が Web プロダクト改善なのか、CLI / 研究用途の改善なのか** を誤読しやすい。特に `PR #825` のような「CLI では重要だが Web の主経路は変えない」変更は、利用モードを分けていないと整理を誤る。

この分岐は後付けの分類ではなく、**TTTC の clone / CUI 前提 → Web UI 包装 → `analysis-core` / PyPI への再切り出し** という歴史の結果でもある。詳細は [[tttc-to-analysis-core-history]]。[[meeting-minutes]]より
歴史ではなく現在の設計判断として読むなら [[analysis-core-and-web-ui]]。[[analysis-core-web-ui-separation-decision-2026-05-23]]より

## 主要 2 モード

### 1. 非専門家向け Web UI モード

対象:

- 自治体・政党・運用担当者
- CSV をアップロードして試行錯誤したい人
- 分析結果を共有 URL や公開レポートとして扱いたい人
- Git や CLI を前提にせず使いたい人

主経路:

- `apps/admin/` でレポート作成
- `apps/api/` が `analysis-core` を subprocess 実行
- `apps/public-viewer/` が `/reports/{slug}` から `hierarchical_result.json` を fetch して描画

関心事:

- 公開 / 非公開 / unlisted
- 共有・ホスティング・静的配布
- admin での再利用、権限、運用フロー
- 非エンジニアが迷わない UI
- できるだけ Web UI だけで完結すること
- 配布時に `Zip` 展開と `setup.bat` 起動程度で始められること

典型成果物:

- `hierarchical_result.json`
- `hierarchical_overview.txt`
- `public-viewer` での表示結果

注意点:

- Web の主経路は **JSON + `public-viewer`** であり、CLI が出す `report.html` ではない
- `apps/api/src/services/report_launcher.py` が `python -m analysis_core ... --without-html` を固定しているのは、CLI 変更への追随漏れではなく、この artifact 契約を守るための意図的な分岐として読むのが自然
- `apps/api/src/services/report_sync.py` の保持対象もこの前提で決まっている
- 理想の入口は「Git clone して手で環境を組む」ことではなく、最小限のローカル操作で Web UI を起動し、その後は UI 上で試行錯誤できること
- このモードでは、CLI を前提にするより **`Zip` で配布物を落として `setup.bat` を起動すれば試せる** くらいの friction が目標に近い

### 2. 研究者・データサイエンティスト向け CLI モード

対象:

- 研究者
- データサイエンティスト
- AI coding agent / 開発者
- ローカルで分析条件を変えながら再実行したい人

主経路:

- `kouchou-analyze` / `python -m analysis_core`
- `packages/analysis-core/` を直接使う
- 必要なら出力物を手元で読む、加工する、再配布する

関心事:

- 再現実験
- `config.json` / 中間成果物 / 速度 / コスト
- LLM provider 切替
- 分析手順の差し替えや新方式の試作

典型成果物:

- `args.csv`
- `embeddings.pkl`
- `hierarchical_clusters.csv`
- `hierarchical_result.json`
- `report.html` (`PR #825` 以降の観察用HTML)

注意点:

- `report.html` は **CLI 側の自己完結型観察用HTML**。Web の主経路とは別
- 2026-05-23 の maintainer 判断でも、`report.html` は Web canonical にしない。Web は引き続き `hierarchical_result.json` + `public-viewer` を canonical path とする。[[report-html-non-web-canonical-decision-2026-05-23]]より
- したがって `CLI 既定では HTML を生成するのに、なぜ API は `--without-html` 固定なのか` という疑問への答えは、「同じ解析コアでも利用モードごとに保持・配信したい artifact が違うから」である
- CLI の改善が、そのまま Web プロダクトの改善とは限らない
- このモードでは `Mac` / `Linux` で CLI を使えることをほぼ前提にしてよい
- `Windows` 利用者でも研究者・開発者側のユースケースなら、ネイティブ対応を最優先せず `WSL2` か `Docker` を使ってください、という運用で割り切る余地が大きい

## 運用上の含意

- 研究者・データサイエンティスト向けには、カスタマイズ性の高い CLI パイプラインがあればよい
- 非エンジニアの試行錯誤ユースケースでは、CLI 作業は最小限にし、レポート作成から確認まで Web UI で閉じる必要がある
- したがって「CLI をきれいにする」と「非エンジニア向け入口を良くする」は別問題として優先度を付けた方がよい
- A/B/C/D の分類は、実装の配布形態だけでなく対外説明にも使える。研究者向け ipynb、エンジニア向け pip、デプロイできる組織向け Web UI、エンジニアがいない組織向け hosted trial は、8/2 や #564 の説明で混ぜずに出すと、誰に何を提供しているかが伝わりやすい。[[meeting-brand-compass-information-strategy-2026-06-30]]より

## 共有コアと分岐点

両モードは完全に別製品ではなく、**共通コアは `packages/analysis-core/`**。分岐するのは主に「入口」と「表示経路」。

- 共通:
  extraction → embedding → clustering → labelling → aggregation
- Web UI 側の分岐:
  API / `public-viewer` / visibility / hosting
- CLI 側の分岐:
  ローカル実行 / 中間成果物 / `report.html` / 実験的再利用

## PR や論点をどう分類するか

まず「どちらの利用モードの改善か」を見る。

- **Web UI 側改善**
  `public-viewer`、`admin`、`/reports/{slug}`、公開設定、ホスティング、共有 UX
- **CLI 側改善**
  `analysis-core` CLI、PyPI、`config.json`、中間成果物、standalone `report.html`
- **両方に跨る改善**
  `analysis-core` の分析品質、provider 対応、出力スキーマ

`PR #825` は、この分類では **CLI 側改善**。  
`PR #824` は **共通コア改善だが、admin の model list UX は未追随** と読むのが自然。

## この整理を使うページ

- プロジェクト全体像: [[kouchou-ai]]
- ランタイム構成: [[architecture-overview]]
- 解析手順: [[pipeline]]
- CLI の使い方: [[cli]]
- Web 配信 / ホスティング: [[deployment]]
- 未着地論点: [[open-decisions]]

## Open Questions

- Jupyter Notebook を「CLI モードの一部」とみなすか、独立した第 3 モードとして切り出すか
- 非専門家向け配布形として、`Zip + setup.bat + browser open` をどこまで正式サポート対象にするか — 段階整理は [[windows-distribution-options]]

## Updates

- 2026-06-30: [[meeting-brand-compass-information-strategy-2026-06-30]] を追加し、A/B/C/D 分類は実装構成だけでなく Brand Compass / 情報発信上の説明軸でもあると追記。
- 2026-05-19: 初版作成。Web UI と CLI / analysis-core を分ける軸を明文化
- 2026-05-19: 研究者・データサイエンティスト向けは `Mac/Linux + CLI` を正規入口とし、`Windows` は `WSL2/Docker` 寄せでよい一方、非専門家向けは `Zip + setup.bat + Web UI` に近い入口を目標形として追う整理を追記
- 2026-05-19: 会話中の整理を反映し、「研究者向けの CLI 改善」と「非エンジニア向け Web UI 完結導線」は別の最適化問題だと明記
- 2026-05-23: この二分が生まれた歴史的経緯への導線として [[tttc-to-analysis-core-history]] を追加
- 2026-05-23: maintainer 判断 [[report-html-non-web-canonical-decision-2026-05-23]] を反映し、`report.html` は Web canonical にしないと明記
