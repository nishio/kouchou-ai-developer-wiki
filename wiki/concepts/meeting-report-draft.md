---
name: meeting-report-draft
type: concept
summary: "次の定例会議で Codex が報告する内容の下書きページ。会議ごとに過去回を snapshot として archive へ rotate し、本ページは次回向けの差分のみ積み上げる"
sources:
  - source-code.md
  - github-dev-docs.md
  - meeting-minutes.md
---

## 目的

このページは、**次の定例会議で Codex 関連の作業を短時間で報告するための下書き** である。Issue / PR / CI / wiki の更新が散らばるので、会議前に思い出すのではなく、作業のたびにここへ要点を寄せる。

ポイントは「全部の変更履歴」を書くことではなく、**会議で口頭共有したい判断と進み具合だけを残す** こと。詳しい根拠は各 concept / analysis / source ページへリンクする。[[coding-agents]]より [[contributing]]より

## 使い方

- 1 項目は 2〜4 行程度で、`やったこと / 現在地 / 次の一手` が分かる粒度にする
- merge 済みか進行中かを明記する
- issue 番号、PR 番号、main commit などの検索キーを残す
- 会議で読まない細かい実装詳細はこのページに詰め込まず、関連ページへ送る
- 会議が終わったら本ページを `wiki/concepts/meeting-report-YYYY-MM-DD.md` へ rotate し、本ページは次回向けに空に戻す

## 過去回

- [[meeting-report-2026-05-25]] — 大リファクタリング完了、LLM grouping 実験、ラベル refinement 実験、open issue 棚卸し、Windows setup 切り替えなど

## 次回定例向け下書き (2026-06-01 向け)

- `#629` の掘り下げとして、`fetch_reports.py` はストレージ機能が無かった初期の「deploy 前に API から吸い出して守る」発想の名残で、current main の storage sync / restore 本線とはずれていることを整理した。今後は script 自体を強化するより、migration 専用へ降格し、Azure Blob の read/write を軽く確認する storage health check を deploy safety に据える方が筋がよい。[[fetch-reports-deprecation-and-storage-health-2026-05-26]]より
- その整理に合わせて、旧 `#629` は close し、`#870`（`fetch_reports.py` の役割整理）と `#871`（deploy safety を Blob Storage health check に切り替える）へ分解した。次に実装するなら `#871` を先に進め、その後 `#870` で script / docs の降格を片付ける順がよい。[[github-dev-docs]]より [[fetch-reports-deprecation-and-storage-health-2026-05-26]]より

## Open Questions

- Codex 以外の AI エージェント（Devin / Copilot Agent）の報告も同じページに寄せるかは未整理

## Updates

- 2026-05-26: `fetch_reports.py` を current storage 本線とのズレとして整理し、deploy 前バックアップ常設より storage health check 置換が筋だという analysis を追加
- 2026-05-26: 旧 issue `#629` を close し、`#870` / `#871` に整理し直した
