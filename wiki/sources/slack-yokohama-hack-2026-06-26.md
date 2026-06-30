---
type: source
summary: "2026-06-26 Slack で共有された Yokohama Hack! / 横浜型ブロードリスニングの観測。市民の声の収集手法を中心にした AI 実証募集として読む"
url: https://hack.city.yokohama.lg.jp/news/10021
sources:
  - slack-logs-repository.md
  - https://prtimes.jp/main/html/rd/p/000000143.000099300.html
---

## What it is

2026-06-26 に `#2_開発_広聴ai` で共有された、Yokohama Hack! の「横浜型ブロードリスニング」情報を固定する source。Slack raw の一次 source は `digitaldemocracy2030/slack-logs` の mirror で、詳細な読み方は [[slack-logs-repository]] を参照する。

## Freshness marker

この source の鮮度基準は、2026-06-30 に `work/slack-logs` を `main@341cf8022d3233f24d619052f6aca32edac5126a` まで pull し、`mirror/slack/C08F7JZPD63.jsonl.gz` を確認した時点。mirror の `synced_at` は `2026-06-30T04:12:50Z`、window は `2026-06-16T04:12:50Z` から `2026-06-30T04:12:50Z`。[[slack-logs-repository]]より

## Observation

2026-06-26 09:32 JST に Hal Seki が、「横浜型ブロードリスニング」および Yokohama Hack! の官民連携プロジェクトとして共有している。Slack 上では、市民意見の収集・分析・検討に係る課題のうち、市民の声の「収集」手法を中心にした課題解決ソリューション募集として引用されている。[[slack-logs-repository]]より

公開 web では、同じ公式リンクを参照する PR TIMES の横浜市行財政局リリースが 2026-06-23 に出ている。そこでは、横浜型ブロードリスニングは市民の声を「広く・多く・深く収集」し、声に基づく分析・検討につなげる実証プロジェクトとして説明されている。PR TIMES リリースより

## Reading

広聴AI側から見ると、この Slack 観測は「分析 pipeline をすぐ置き換える」要求ではない。初回募集の中心は市民の声の収集手法であり、広聴AIの current asset である analysis / viewer / docs は、収集後の分析・検討・フィードバック段階でどう接続するかを整理しておくのがよい。

## Open Questions

- 横浜型ブロードリスニングへの関与は、広聴AIの input plugin / data collection docs へ接続するのか、それとも既存分析・可視化のデモ素材整備に留めるのか。
- 市民の声の「収集」手法に関する知見を developer wiki に入れる場合、kouchou-ai 本体の設計判断として扱う範囲と、外部プロジェクト事例として扱う範囲をどう分けるか。
- Slack mirror は rolling snapshot なので、重要な観測はこの source と commit hash で固定する。必要なら後で `raw/` canonical 月次ログへ差し替える。
