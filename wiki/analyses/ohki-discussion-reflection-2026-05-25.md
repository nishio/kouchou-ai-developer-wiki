---
type: analysis
summary: "ohki-shingo との議論は、散布図互換の技術判断を、自治体利用で公開UIが担うべき説明責務へ引き戻したものとして読める"
sources:
  - slack-public-ui-requirements-2026-05-23.md
  - kouchou-ai-direction-2025-12-06.md
  - kouchou-ai-direction-2-2025-12-13.md
  - public-ui-requirements-for-broadlistening.md
  - jigsaw-sensemaker-history.md
---

2026-05-23 の [[slack-public-ui-requirements-2026-05-23]] での [[ohki-shingo]] との議論は、「散布図を残すか捨てるか」ではなく、**散布図が公開UIで担っていた説明責務をどう再実装するか** という問いとして読むのがよい。[[slack-public-ui-requirements-2026-05-23]]より

## Takeaway

[[nishio]] の整理は、短期には embedding を前提としない分析様式でも散布図互換を維持し、長期には散布図必須の view をやめる、という二段構えだった。[[jigsaw-sensemaker-history]]より  
これに対して [[ohki-shingo]] は、散布図の是非を直接裁くのではなく、まず「なぜ現状の散布図が人間には受け入れられやすいのか」「広聴結果の公開UIに求められるものは何なのか」と問いを分けた。[[slack-public-ui-requirements-2026-05-23]]より

この分け方が重要なのは、議論の評価軸を **技術方式の優劣** から **利用者に対する説明責務** へ移しているからである。散布図は本質ではないが、量感、整理されている感覚、全体探索、個別意見への到達、恣意性の低さを一画面で示しやすかった。したがって代替 view は「散布図でないこと」ではなく、これらの役割を満たすことで評価されるべきである。[[slack-public-ui-requirements-2026-05-23]]より [[public-ui-requirements-for-broadlistening]]より

## 以前からの連続性

この発言は、ohki-shingo の以前からの問題意識とかなり連続している。

2025-12-06 の方向性議論では、[[ohki-shingo]] は「ユーザのいるものを作りたい」と発言し、現状広聴AIが「何に使えて何に使えないのか」が分かっていないことも論点にしていた。さらに、まず手動でも実課題の解き方が分かれば、それをツール化して多くの人が効率的にできる可能性がある、という順序を示している。[[kouchou-ai-direction-2025-12-06]]より

2025-12-13 の続きの議論でも、[[ohki-shingo]] は「本の話と広聴AIの今後の話は独立できないか」「想定すべきユーザーは自治体なのか」と問い、最後には「自治体などのユーザーの問題を解決するためのプロダクト」ではなく「材料」としてツールを提供する可能性を出している。[[kouchou-ai-direction-2-2025-12-13]]より

つまり 2026-05-23 の公開UI要件の整理は、急に出た UI 論ではない。**ユーザー、実課題、運用、説明責任の側から技術論を問い直す** という、以前からの ohki-shingo の姿勢が、散布図 / embedding / view 分離の論点に適用されたものと見える。

## 技術判断への含意

第一に、`analysis_mode` / `view` の独立化は、単なる plugin architecture の美しさではなく、公開UIの説明責務を守るための分離として説明できる。下位契約はデータ構造や capability だが、上位契約は量、観点、論点、個別意見、少数意見、恣意性、次の問いを示せることになる。[[public-ui-requirements-for-broadlistening]]より

第二に、短期の散布図互換案で必要なのは、embedding 距離の精密な再現ではなく、同じ論点グループが自然にまとまって見え、根拠や限界や原意見へ辿れることである。これは `llm_grouping` 系を scatter-compatible に載せる技術的ハードルを下げる一方で、配置の説明可能性や少数意見の扱いをレビュー対象にする必要がある。[[slack-public-ui-requirements-2026-05-23]]より [[jigsaw-sensemaker-history]]より

第三に、長期的には「散布図をやめる」よりも「散布図が満たしていた信頼形成の機能を別 UI で満たす」が正しい表現になる。散布図を外しても個別意見に戻れない、分類根拠が見えない、少数意見が消える、次の議論が見えないなら、公開UIとしては後退しうる。[[public-ui-requirements-for-broadlistening]]より

## 自分たちへの反省

この議論で刺さるのは、開発側が「embedding は不要か」「散布図互換をどう作るか」「analysis mode をどう切るか」に寄りやすいのに対して、ohki-shingo は「それは自治体や住民が確認すべき何を満たすのか」に戻している点である。[[slack-public-ui-requirements-2026-05-23]]より

したがって次の実験は、geometry 指標や label judge だけでなく、公開UI 7 要件を明示したレビューを併用する方がよい。たとえば group-first view / hierarchy-list view / scatter-compatible view を比べるなら、`距離がそれらしいか` だけではなく、`分類の根拠が見えるか`、`少数意見へ辿れるか`、`次に深掘りすべき問いが出るか` を評価軸に入れるべきである。[[public-ui-requirements-for-broadlistening]]より

また、「材料として提供する」という 2025-12-13 の発想を真面目に読むなら、プロダクト本体だけで完結させるより、自治体の前後工程、入力データの集め方、職員が説明する場面、住民に公開する場面を含む運用パッケージとして考える必要がある。[[kouchou-ai-direction-2-2025-12-13]]より

## Open Questions

- 公開UI 7 要件は自治体利用では強いが、政党、社内アンケート、研究用途でも同じ重みでよいのか
- 「恣意的に見えない」ことを、UI 表現、データ公開、アルゴリズム説明、監査ログのどれで担保すべきか
- `llm_grouping` のような非 embedding 系分析を scatter-compatible に置く時、配置の決まり方をどこまで公開すれば説明責任を満たすか
- ohki-shingo の「材料として提供する」発想を、`analysis-core` / CLI / viewer / 運用ドキュメントのどの境界に落とすのがよいか

## Updates

- 2026-05-25: 初版作成。2026-05-23 の公開UI thread を、2025-12 の方向性議論にあった ohki-shingo の「ユーザー」「自治体」「材料」「実課題」志向と接続して考察
