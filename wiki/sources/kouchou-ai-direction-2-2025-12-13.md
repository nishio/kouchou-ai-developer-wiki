---
type: source
summary: "2025-12-13 の『広聴AIの方向性について2』メモ。選択肢比較のうえで、書籍まで現行系を stable v4 として保ち、次世代化は別軸で進める判断が固まった"
sources:
  - meeting-minutes.md
---

## What It Is

2025-12-13 の Google Docs 「広聴AIの方向性について2」の export を要約した source。初回メモで出た問題設定を踏まえ、現行広聴AIをどこまで育てるか、plugin platform をどう進めるか、書籍出版までの時間軸で何を凍結し何を先送りするか、を選択肢比較で整理した会議メモである。[[meeting-minutes]]より

## Key Points

- 会議では大きく 4 つの方向が並べられている
  - 現行広聴AIの強みであるアジェンダ発見に寄せる
  - 現行広聴AIをそのまま platform / plugin 化する
  - 新 platform を別に作り、現行広聴AIをその plugin として載せる
  - **現行広聴AIは stable v4 として維持し、より広い問題解決系は別軸で進める**
- 議論の収束点は 4 に近く、**書籍出版まで大規模リファクタを main に入れず、現行の見た目や導線に価値を感じている利用者を守る** 判断が実務的だと整理されている
- その一方で、長期的には plugin system や別分析方式を見据えており、**全部入り platform をいきなり作るより、まず分析部分を pip package として切り出す** 方が現実的という発想が出ている
- Web UI の現行構成は「管理者が生成し、一般利用者は結果を見る」前提で作られており、利用者自身が見方を切り替えたり深掘りしたりするには制約がある、という問題意識も明示されている
- 自治体の実務では、ツール単体よりも「どう声を集めるか」「何を次に議論すべきか」が重要で、広聴AIはそれ単体で完結する製品ではない、という視点が強い

## Why It Matters

このメモは [[versioning-strategy]] の中核根拠であり、後の

- 書籍時点の `main` を stable v4 とみなす
- `analysis-core` を package / CLI / PyPI として切り出す
- plugin 化は v5 側の探索枝として進める

という三段構えを直接支えている。[[meeting-minutes]]より [[source-code]]より

## Open Questions

- この時点では、pip package 化がどこまで短期でできるかは見積り段階で、`analysis-core` という具体名もまだ出ていない
- stable v4 と次世代枝をどう共存させるかは、その後の [[refactoring-status]] が示す Phase 移行で具体化された

## Updates

- 2026-05-25: Google Docs export から初回作成
