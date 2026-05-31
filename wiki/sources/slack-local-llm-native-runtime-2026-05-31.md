---
type: source
summary: "2026-05-31 Slack で nishio と tokoroten が、API 契約不要の local LLM 実行可能性について、20B 級モデルの現実化と Chrome / Windows の native LLM support を使う方向を議論した"
sources:
  - slack-local-llm-native-runtime-2026-05-31.txt
---

## 何のソースか

2026-05-31 の Slack 断片。nishio が local LLM で動かす現実性と、「学習に使われてもいいデータですか」という確認 UI の必要性を投げた。tokoroten は 20B class model がそろそろ現実的になっていること、Chrome や Windows が LLM を native support し始めているためそこを使えないか、という方向を出した。[[slack-local-llm-native-runtime-2026-05-31]]より

nishio はその後、Chrome / Windows 方向も検討軸になり得ると反応した。つまり [[node-runtime-free-windows-exe-2026-05-31]] の offline bundled-model route は、「自前で model/runtime を同梱する」だけでなく、「OS / browser 側の native local AI runtime を使う」route も含めて検討する必要が出た。[[slack-local-llm-native-runtime-2026-05-31]]より

## 含意

- local 完結の価値は、単に API key 入力を省くことではなく、入力データが外部 API の学習・保持・転送に使われる懸念を避けることにもある
- 20B class model は品質面の期待を上げる一方、Windows 一般ユーザー向けの package size / RAM / CPU latency / first-run model acquisition を product scope として抱える
- Chrome / Windows native support は、model lifecycle と hardware acceleration を platform 側に逃がせる可能性があるが、browser tab 依存・Copilot+ PC 依存・preview API などの制約を確認する必要がある

## Updates

- 2026-05-31: 初版作成。Windows 単一実行ファイル / local 完結 route の追加論点として source 化
