---
type: source
summary: "2026-05-31 Slack で tokoroten と nishio が、Windows ユーザー向けには単一実行バイナリが望ましく、Node runtime を同梱する代わりに Web UI を SPA/static assets 化してサーバ側 wrapper を Python に寄せる案を議論した"
sources:
  - slack-windows-single-exe-2026-05-31.txt
---

## 何のソースか

2026-05-31 の Slack 断片。tokoroten が「Windows ユーザ的には実行バイナリがいっこあるだけが嬉しい」と述べ、nishio は以前 GPT Pro に相談した時点では Web UI server-side の Node layer があるため Python と Node の両方同梱が必要で難しい、という整理だったと返した。[[slack-windows-single-exe-2026-05-31]]より

その場で nishio は、むしろ server を Python に移植すればよいのでは、と発想を切り替えた。tokoroten は「node はビルド済みバイナリにして、SPA」と補足し、nishio は frontend を assets にまとめ、server-side の薄い wrapper を Python に置き換える案として理解した。[[slack-windows-single-exe-2026-05-31]]より

## 含意

- 以前の [[windows-distribution-options]] は「完全単体 exe は別プロジェクト級で重い」と整理していたが、その主因の一つは Python runtime と Node runtime の二重同梱だった
- 今回の案は、Node を実行時 runtime として同梱するのではなく、build-time に frontend assets を作り、runtime は Python/FastAPI が API と静的配信を担う方向
- これは [[windows-distribution-options]] の段階 4 を即実装する話ではなく、段階 4 の難度を下げるための前提 refactor として扱うのがよい

## Updates

- 2026-05-31: 初版作成。Node runtime 排除による Windows 単一実行ファイル配布の再評価材料として source 化
