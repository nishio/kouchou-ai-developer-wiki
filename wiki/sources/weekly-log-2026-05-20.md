---
name: weekly-log-2026-05-20
summary: "nishio/oss_weekly_reporter の週次ダンプ (2026-05-20 〜 2026-05-27) — kouchou-ai の refactor / Windows / CSP / LLM grouping と、Slack の公開UI・MST可視化・実験保存方針"
type: source
url: https://github.com/nishio/oss_weekly_reporter/tree/data/data/2026-05-20_to_2026-05-27
last_read: 2026-06-02
coverage: "2026-05-20_to_2026-05-27 raw GitHub / Slack, oss_weekly_reporter data@d0e340c96c05"
sources:
  - oss_weekly_reporter data@d0e340c96c05
---

## What it is

[[nishio]] が運用する `oss_weekly_reporter` の 2026-05-20 〜 2026-05-27 週次ダンプ。2026-06-02 に `work/oss_weekly_reporter` を `data@d0e340c96c05` まで fast-forward し、次を読んだ。

- `data/2026-05-20_to_2026-05-27/ai_reports/kouchou-ai.md`
- `data/2026-05-20_to_2026-05-27/ai_reports/slack.md`
- `data/2026-05-20_to_2026-05-27/markdown/slack/all_summary.md`
- `data/2026-05-20_to_2026-05-27/raw/slack/2_開発_広聴ai.json`
- `data/2026-05-20_to_2026-05-27/raw/slack/2_開発_広聴ai_アルゴリズム開発.json`
- `data/2026-05-20_to_2026-05-27/markdown/github/github_report-kouchou-ai.md`

この週は、GitHub 側では大リファクタリング後の workflow / Windows / CSP / LocalLLM / CLI 整備が集中し、Slack 側では公開 UI 要件、LLM grouping 実験、MST / bridge 可視化、実験 artifact 保存方針がまとまって出ている。

## kouchou-ai GitHub

GitHub report では、2026-05-20 〜 2026-05-27 に kouchou-ai で 19 件の PR が merge 済みとしてまとまっている。主な束は次の通り。

- workflow default 化と大規模整理: `#840`, `#865`
- analysis-core / CLI: `#843` extras 分離、`#844` preflight validation、`#864` subprocess smoke 経路修正
- Windows 導線: `#858`, `#861`, `#862`, `#863`
- CSP / public IP / static hosting: `#847`, `#848`, `#849`, `#851`
- LocalLLM / API key / error visibility: `#850`, `#853`, `#852`
- open work: `#866` LLM grouping、`#867` `--reuse-from`、`#874` semantic island layout、`#873` Azure deploy concurrency

この週の GitHub snapshot は、[[refactoring-status]] / [[windows-distribution-options]] / [[public-ui-requirements-for-broadlistening]] / [[llm-grouping-experiment]] の current state を読む時の補助線になる。

## Slack: #2_開発_広聴ai

`#2_開発_広聴ai` は 63 件で、この週の最活発 channel だった。kouchou-ai 開発者 wiki に関係する高信号トピックは次。

- **WebUI と analysis-core の呼び分け**: 外部向けには「広聴AI = WebUI から使えるプロダクト」と見える方が自治体職員や一般ユーザーの混乱が少ない、という指摘が出た。
- **AI agent 運用境界**: Codex が勝手に review request した事案が共有され、人間 attention を使う操作を agent が独断で行わない運用の必要性が再確認された。
- **Windows 導線**: 生 Windows では Git / Python / PowerShell encoding / Docker Desktop などが障壁になり、Codex を Windows ユーザー役として使う実験と `.bat` から PowerShell へ逃がす判断が進んだ。
- **Azure deploy success の過信**: deploy が success でも実際の build / runtime が正常とは限らないという観測が Slack 上でも共有された。
- **公開 UI 要件**: [[ohki-shingo]] が、散布図が受け入れられる理由を「大量意見・整理感・探索性・個別意見への戻り・透明性」に分解し、公開 UI に必要な 7 要件を整理した。これは [[slack-public-ui-requirements-2026-05-23]] の公式 weekly dump 側での確認になった。
- **LLM grouping 実験**: `K=8` では LLM grouping が label quality で有利、`K=20` では従来 hierarchical も強くなり、`[8,40]` は一貫性 / 網羅性が上がるが見出しが長くなりやすい、という比較が共有された。
- **LLM Wiki の事実帰属**: 人名・所属・役割・発言帰属・決定事項では、原文にある事実 / AI 推定 / 人間確認 / 正式決定を分けるべきという指摘が出た。[[ohki-shingo]] の漢字表記確認が具体例になっている。

## Slack: #2_開発_広聴ai_アルゴリズム開発

`#2_開発_広聴ai_アルゴリズム開発` は 13 件。量は少ないが、可視化と実験保存の論点が濃い。

- **MST / bridge 可視化の seed**: `1 意見 = 1 点` の点群を保ちつつ、UMAP 2D と意味クラスタリングの衝突を避けるため、クラスタ内 MST とクラスタ間 bridge edge を組み合わせる案が出た。これは [[graph-visualization-proposal-2026-05-25]] の元発想にあたる。
- **小規模ケース向け LLM pairwise / MST**: 100 件未満の小規模ケースでは、10,000 件超向けの散布図ツールをそのまま使うより、LLM で N:N 類似関係を抽出し、強い関係から木や graph を作る方向が示された。
- **HyDE**: 条文や計画をベースにした Hypothetical Document Embeddings は試す価値がある、という反応があった。
- **Supervised UMAP の見た目限界**: supervised UMAP は明瞭に分かれても他グループに混ざって見えるため、この週の観測では採用しにくいとされた。
- **実験 artifact 保存**: 生成データを永続化して後から確認できるようにするには、実験は本体 output だけでなく別 repo / 別保存場所で扱うべきという気づきが出た。これは [[experiment-result-storage-policy-2026-06-02]] の前段にあたる。

## Implications

- [[slack-public-ui-requirements-2026-05-23]] は、raw 手元ログだけでなく `oss_weekly_reporter` 公式 weekly dump でも確認済みにできる。
- [[graph-visualization-proposal-2026-05-25]] は外部 GPT との brainstorm だけでなく、Slack algorithm channel の実際の seed 発言と接続できる。
- [[experiment-result-storage-policy-2026-06-02]] は、2026-06-02 の user 指摘だけでなく、2026-05-26 Slack の「生成データを永続化したい」という問題意識とも整合する。
- `weekly-log-2026-05-06` で薄かった kouchou-ai Slack coverage は、この週で大きく更新された。以後、Slack 由来の 2026-05 下旬論点は本 source を freshness marker として扱う。

## Open Questions

- 2026 Q2 の `#2_開発_広聴ai` / `#2_開発_広聴ai_アルゴリズム開発` を quarter source として切るか、当面は週次 source のまま扱うか。
- `oss_weekly_reporter` の weekly dump が増えるたびに source ページを作るか、kouchou-ai 関連の高信号週だけ source 化するか。
- Slack 上の GitHub / wiki への self-reference は、source としてどこまで採用するか。AI report の要約は便利だが、重要判断は raw Slack / raw GitHub で確認してから使う。

## Updates

- 2026-06-02: 初版作成。`work/oss_weekly_reporter` を `data@d0e340c96c05` まで更新し、2026-05-20_to_2026-05-27 の kouchou-ai / Slack weekly dump を読んだ。
