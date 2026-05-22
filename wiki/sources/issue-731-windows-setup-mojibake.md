---
name: issue-731-windows-setup-mojibake
type: source
summary: "GitHub issue #731 の再現ログ。Windows で `setup_win.bat` 実行時に日本語が文字化けするだけでなく、一部行が別コマンドとして解釈されてセットアップが停止することを示す"
sources:
  - https://github.com/digitaldemocracy2030/kouchou-ai/issues/731
---

## 何のソースか

`digitaldemocracy2030/kouchou-ai` の issue #731「[BUG] Windows環境でインストールしようとすると文字化けが発生して中断する」を要約した source。`setup_win.bat` の日本語メッセージをどう扱うか、また `.bat` のまま押し切るか `PowerShell` などへ分離するか、という判断の一次根拠に使う。[[github-dev-docs]]より

## 観測できること

- 利用者は配布 zip を展開し、Docker を起動し、`setup_win.bat` を実行しただけで問題に遭遇している
- ログでは、日本語 `echo` の表示が壊れるだけでなく、日本語行そのものが **「内部コマンドまたは外部コマンドとして認識されていません」** に落ちている
- つまり症状は単なる UX 上の読みづらさではなく、`cmd.exe` による **バッチファイルの解釈自体が壊れている** タイプの不具合である
- 利用者メモには、Windows 上でも `WSL` 経由で `setup_linux.sh` を使えば起動には成功した、とある。Windows ネイティブ導線の問題と、kouchou-ai 全体の起動不能は分けて考える必要がある

## kouchou-ai への含意

- `setup_win.bat` に日本語文字列を直書きしたまま「表示だけ直す」発想では不十分で、**パース段階の安全性** を優先して設計を変える必要がある
- `.bat` だけで日本語対話を完結させるより、ASCII の薄いランチャーにして、対話処理を別実行基盤へ逃がす方が再発しにくい
- issue 自体が「Windows ネイティブ導線の品質問題」を示しているので、`setup_win.*` の整理は単なる翻訳や文言修正ではなく、配布戦略の一部として扱うべき

## Open Questions

- 利用者環境の codepage / terminal host / Windows version の詳細差分まで掘る必要があるか
- `PowerShell` 分離だけで十分か、将来的にはランチャー exe まで進むべきか

## Updates

- 2026-05-22: 初回作成。issue #731 のログから、「文字化け」ではなく `cmd.exe` のパース破綻が本質である点を抽出
