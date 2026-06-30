---
type: analysis
summary: "8/2 イベントと横浜型ブロードリスニングを踏まえ、人間と衝突しにくく進める docs / wiki / demo readiness の整理"
sources:
  - meeting-2026-06-22-event-priority.md
  - slack-yokohama-hack-2026-06-26.md
  - slack-logs-repository.md
  - current-status-2026-06-30.md
  - broadlistening.md
  - usage-modes.md
  - public-ui-requirements-for-broadlistening.md
  - docs-issue-map-2026-06-30.md
  - event-2026-08-02-tech-tool-brief-draft-2026-06-30.md
  - event-2026-08-02-public-example-inventory-2026-06-30.md
  - public-broadlistening-artifacts-2026-06-30.md
  - issue-564-public-case-trust-layer-scope-2026-06-30.md
  - meeting-brand-compass-information-strategy-2026-06-30.md
  - slack-prance-event-broadlistening-session-2026-06-30.md
---

## Conclusion

8/2 イベント向けの次の一手は、すぐ新機能を実装することより、ブロードリスニングを「実践」「技術」「ツール」の各入口から説明できる状態にすること。議事録上の priority には情報発信と事例の積み上げが含まれており、Slack 上でも Codex は状況把握と LLM Wiki / docs 更新を中心に走らせる方針が共有されている。[[meeting-2026-06-22-event-priority]]より [[slack-logs-repository]]より

Brand Compass 文脈まで広げると、8/2 準備は「見せる demo を選ぶ」だけではない。stable v4 / M2 に向けて現行価値を安定化し、公開事例・レポートの読み方・A/B/C/D 配布形態・外部向けの「聞く能力」ストーリーを揃えることが、情報発信と事例積み上げの実務になる。[[meeting-brand-compass-information-strategy-2026-06-30]]より

## Event lanes

議事録のタイムライン案から見ると、8/2 イベントには少なくとも 4 つの説明 lane がある。

- 国会から見るブロードリスニング実践
- 地方政治とブロードリスニング実践
- ブロードリスニングの技術
- ブロードリスニングのツール

developer wiki と docs が短期で支援しやすいのは、後ろ 2 つの「技術」「ツール」lane である。ただし実践 lane と切り離すと、ツール説明が「何のために使うか」を失う。したがって、既存 docs では [[broadlistening]]、[[usage-modes]]、[[public-ui-requirements-for-broadlistening]] を束ね、実践から tool / viewer / pipeline へ降りる導線を作るのがよい。

19:04 JST の Slack mirror 再確認では、`#dd_prance_event2026` に国会 / 地方自治の実践 lane 計画が見えた。これは docs / wiki 側が「技術・ツールだけ」へ閉じないための lead だが、Slack-only の planning memo を外部 proof にはしない。実践 lane で奈良 / 舞鶴2040を扱う場合も、primary public source と session framing の確認に戻す。[[slack-prance-event-broadlistening-session-2026-06-30]]より

## Yokohama context

横浜型ブロードリスニングは、Slack 上の共有では市民の声の「収集」手法を中心にした課題解決として読まれている。PR TIMES 経由で確認できる横浜市行財政局リリースでも、段階的な実証の第一歩は収集手法の検証に寄っている。[[slack-yokohama-hack-2026-06-26]]より

このため、広聴AIの current pipeline だけを前面に出すと焦点がずれる可能性がある。docs では `collect / import / analyze / show / discuss` のように、意見収集と分析可視化を分けて説明し、広聴AIが強いのは現時点では `analyze / show` 側だと明示するほうがよい。

## Safe next actions

- 8/2 イベント向けに、公開可能な「ブロードリスニング技術・ツール入口」1 枚を draft 化する。初稿は [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] に固定した。最初の骨子は、ブロードリスニングとは何か、広聴AIが扱う入力、analysis / viewer が出すもの、現時点の配布形態、公開できる事例、未対応範囲。
- 公開可能事例の棚卸しは [[event-2026-08-02-public-example-inventory-2026-06-30]] に固定した。現時点では、渋谷区 official page / PDF を trust context、奈良 #全員市長 public viewer を primary viewer demo、八代市を political / policy context に注意する deep case、synthetic CSV を fallback として扱う。[[public-broadlistening-artifacts-2026-06-30]]より
- 公開事例は #564 単独ではなく、#696 誤読防止 / #542 責任所在と合わせて扱う。8/2 では「公開事例リスト + レポートの読み方 + 何を保証しないか」を最小単位にする。[[issue-564-public-case-trust-layer-scope-2026-06-30]]より
- [[docs-issue-map-2026-06-30]] の docs 群と接続し、#876 developer quickstart、#877 Windows setup、#885 Node runtime 排除をイベント説明に混ぜない。イベント向けには「利用者に見せる説明」と「開発者が整える前提」を分ける。
- Yokohama Hack! 文脈では、収集手法そのものを kouchou-ai 本体に取り込む判断を急がない。input plugin / data collection docs の候補として論点化し、owner と issue が見えたら実装 lane に移す。
- public examples / demo は公開境界を守る。実環境 URL、resource 名、revision、ログ、secret / access 周辺は developer wiki に書かず、公開 wiki では設計判断と公開可能な課題に留める。
- Brand Compass / 情報発信の観点では、A/B/C/D 配布形態を「誰に何を提供しているか」の説明として使う。8/2 の技術 / ツール lane では、研究者向け ipynb、エンジニア向け pip、デプロイできる組織向け Web UI、エンジニアがいない組織向け hosted trial を混ぜずに説明する。[[meeting-brand-compass-information-strategy-2026-06-30]]より

## Open Questions

- 8/2 イベントでの主 artifact は、既存 viewer の公開例、技術解説、ツール比較、運用事例のどれか。
- 国会 / 地方政治の実践 lane で使える公開可能事例はどれか。事例名だけでなく、どの artifact を見せてよいかの公開境界確認が必要。
- 奈良 / 渋谷区 / 八代市のどれを 8/2 の第一デモにするか。URL は public でも、スクリーンショット利用や政治文脈の話し方は別途確認が必要。
- 横浜型ブロードリスニングの「収集」中心の課題は、kouchou-ai の input plugin roadmap に入れるべきか、それとも周辺エコシステムとして docs で接続するだけにするべきか。
- Brand Compass 本体のどの項目を、8/2 の story / case / docs / demo selection に明示的に反映するか。

## Updates

- 2026-06-30 19:04 JST: `#dd_prance_event2026` の 8/2 実践 lane 計画を反映し、技術・ツール lane と国会 / 地方自治の実践 lane を接続しつつ、Slack-only lead を外部 proof にしない方針を追記。
- 2026-06-30: [[meeting-brand-compass-information-strategy-2026-06-30]] を追加し、8/2 readiness は first demo 選定だけでなく stable v4 / 情報発信 / A/B/C/D 配布形態の説明を揃える作業だと補正。
- 2026-06-30: [[issue-564-public-case-trust-layer-scope-2026-06-30]] を追加し、公開事例 demo を #564 / #696 / #542 の trust layer と接続。
- 2026-06-30: [[event-2026-08-02-public-example-inventory-2026-06-30]] を追加し、8/2 で使える公開事例 / demo 素材を public-ready、確認待ち、fallback に分けた。
- 2026-06-30: [[event-2026-08-02-tech-tool-brief-draft-2026-06-30]] を追加し、技術・ツール入口の 1 枚 draft を固定。
- 2026-06-30: 初回作成。2026-06-22 議事録の 8/2 イベント lane と、2026-06-26 Slack の横浜型ブロードリスニング共有を合わせ、次の docs-safe action を整理。
