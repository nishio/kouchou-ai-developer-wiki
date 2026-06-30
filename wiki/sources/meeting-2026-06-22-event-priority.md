---
type: source
summary: "2026-06-22 議事録から見た 8/2 イベント、Brand Compass、high priority issue、情報発信、運用ポリシーの優先軸"
sources:
  - meeting-minutes.md
  - meeting_minutes.txt
  - meeting-brand-compass-information-strategy-2026-06-30.md
---

## What it is

2026-06-22 先頭見出しの議事録から、8/2 イベントと直近の開発優先軸に関係する部分を抜き出した source。議事録全体の freshness と refresh protocol は [[meeting-minutes]] を参照する。

## Freshness marker

この source の鮮度基準は、2026-06-30 に再取得した `raw/meeting_minutes.txt` を 2026-06-30 17:15 JST に確認した時点。先頭見出しは `2026/06/22`、txt は 7702 行だった。`2026/06/29` 見出しはまだ export 内に見当たらない。[[meeting-minutes]]より

## Observations

議事録冒頭の「今後追求する事」は、Brand Compass に沿った開発、high priority issues の消化、情報発信と事例の積み上げ、運用ポリシーの改善の 4 本になっている。これは 8/2 イベントだけの一時的な話ではなく、直近の開発定例で繰り返されている priority 軸として読むのがよい。[[meeting-minutes]]より

tokoroten は 8/2 イベントについて、ブロードリスニングで何か出したいと共有している。タイムライン案には、主会場で「国会から見るブロードリスニング実践」と「地方政治とブロードリスニング実践」、第二会場で「ブロードリスニングの技術」と「ブロードリスニングのツール」が置かれている。[[meeting-minutes]]より

同じ議事録では Issues 確認もあり、既存 issue のうち high priority にすべきもの、good first issue にすべきものが確認対象になっている。したがって、8/2 イベント向けの準備も、いきなり人間 authored branch や未確認 issue に手を入れるより、docs / wiki / source 整理で共通認識を作るほうが衝突しにくい。[[meeting-minutes]]より

## Reading

8/2 イベントの文脈は、単一の新機能要求ではなく、ブロードリスニングの実践・技術・ツールを人に説明できる状態へ近づける要求として読むのが自然。特に「情報発信と事例の積み上げ」が priority 軸に含まれているため、既存 viewer / docs / public examples の入口を整理する作業は、実装を急がなくても価値がある。

Brand Compass に沿った開発は、単独の設計文書名としてだけではなく、M2 / stable v4、情報発信、外部向けの物語、自治体利用者課題調査、A/B/C/D 配布形態の説明を合わせる判断フィルタとして読むとよい。詳細は [[meeting-brand-compass-information-strategy-2026-06-30]] に切り出した。

## Open Questions

- 8/2 イベントで実際に出す artifact は、既存 viewer の公開例、技術解説、ツール紹介、運用事例のどれを主軸にするのか。
- 4 トラックのうち、広聴AI developer wiki が短期で支援しやすいのは「技術」と「ツール」だが、「国会」「地方政治」実践側の公開可能事例をどこまで接続できるか。
- イベント向けの docs は広聴AI本体 repo、dd2030.org、broadlisteningbook.com、developer wiki のどこを canonical にするのか。

## Updates

- 2026-06-30: freshness marker を 16:33 export の 7702 行に揃え、Brand Compass / 情報発信の議事録文脈を [[meeting-brand-compass-information-strategy-2026-06-30]] に切り出した。
