---
type: analysis
summary: "Codex が Windows 環境で kouchou-ai / developer-wiki 作業を進めた時の環境構築メモ"
sources:
  - source-code.md
  - github-dev-docs.md
  - local-dev-setup.md
  - gotchas.md
  - coding-agents.md
  - contributing.md
---

# CodexによるWindows環境構築メモ

## Summary

今回の Windows 作業では、`work/kouchou-ai/` を一次参照として Issue #731 の `setup_win.bat` 文字化け問題を修正し、draft PR #858 まで作成した。あわせて developer-wiki 側では Python が未導入だったため、Python 3.14.5 と PyYAML を入れて `scripts/lint_wiki.py` を実行できる状態にした。[[source-code]]より [[github-dev-docs]]より

個人情報を残さないため、ローカルユーザー名、メールアドレス、絶対パス、端末固有の詳細はこのメモでは扱わない。公開される Issue / PR 番号、ブランチ名、ツール名、一般化した環境差分だけを記録する。

## What Happened

Windows 関連 Issue の中では、初回セットアップを直接塞ぐ #731 を優先した。`setup_win.bat` は Git 上では読める日本語を含んでいたが、Windows の実行環境ではコードページ差分により mojibake し、一部の行がコマンドとして解釈されるリスクがあった。そこでバッチファイルの実行時メッセージを ASCII に寄せ、詳しい日本語説明は docs 側へ任せる形にした。[[source-code]]より [[gotchas]]より

修正では API キー形式チェックの重複も整理した。`findstr` にパイプするより、バッチ内の prefix 比較へ寄せる方が今回の目的には単純だった。Docker が無い環境でも `cmd.exe` 経由で Docker 未起動/未インストール時の停止パスを確認できた。[[source-code]]より

developer-wiki 側では Python が PATH に無く、wiki lint が実行できなかった。公式 Windows installer で Python を current user に導入し、PyYAML を追加したところ、`scripts/lint_wiki.py` は動いた。ただし PowerShell の既定出力が cp932 のままだと `✓` の出力で `UnicodeEncodeError` になったため、`PYTHONIOENCODING=utf-8` を指定して解消した。[[local-dev-setup]]より

## Lessons

- Windows の `.bat` は、利用者向けメッセージに非 ASCII を含めるとコードページ差分で壊れやすい。特に「初回セットアップ」では、親切な日本語よりも、まず実行が止まらないことを優先する。
- 日本語の詳しい導線は docs に置き、`.bat` は短い ASCII の操作案内に寄せると、実行環境依存を減らしやすい。
- Windows で Python を入れた直後は、現在の shell に PATH 更新が反映されないことがある。絶対パスで一度確認し、その後にユーザー PATH を検査する。
- Python スクリプトが UTF-8 で正常でも、標準出力の encoding が cp932 だと記号や一部文字で落ちることがある。lint のような運用コマンドでは `PYTHONIOENCODING=utf-8` を併用すると安定する。
- Codex が環境構築メモを書く時は、再現性に必要な情報と個人情報を分ける。必要なのは OS 種別、ツール、エラー種別、解決手順であり、ローカルユーザー名やメールアドレスではない。

## Operational Notes

今後 Windows 系 Issue を扱う時は、まず assignee の有無を確認し、未担当なら自分を assign してから着手する。これは並行開発を避けるための運用ルールである。[[coding-agents]]より [[contributing]]より

実装後は、実機で Docker build まで通せない場合でも、少なくとも壊れていた入口の停止パスや文字化けの有無を `cmd.exe` で確認する。Windows 初回導入の問題は「ビルドできるか」以前に「案内が読めるか」「バッチが途中でコマンド誤解釈されないか」が重要になる。[[gotchas]]より

wiki 側の管理では、Python 導入後に `scripts/lint_wiki.py` を走らせ、broken wikilinks / index 未登録 / frontmatter parse errors を確認する。今回の lint ではいずれも 0 で、孤立ページ 11 件は既知かつ index 登録済みだった。

## Open Questions

- Windows 用 setup script は、長期的には `.bat` のまま維持するべきか、PowerShell script へ寄せるべきか。
- 非専門家向けの Windows 導線は、native Windows を厚く支えるより、Docker Desktop / WSL2 のどちらを正規入口として前面に出すべきか。
- `scripts/lint_wiki.py` 側で `PYTHONIOENCODING=utf-8` 前提を README 化するか、スクリプト自身が Windows console 出力をより安全に扱うべきか。

## Updates

- 2026-05-22: 初回作成。Issue #731 / draft PR #858 と、Windows 上で Python を導入して wiki lint を復旧した体験を、個人情報を除いて整理。
