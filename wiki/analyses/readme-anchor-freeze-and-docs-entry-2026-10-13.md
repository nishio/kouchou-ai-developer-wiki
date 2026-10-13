---
type: analysis
summary: README への外部アンカーリンクを理由に README 改訂を止めるのは、README を永久凍結する footgun。外部リンクは安定した個別ドキュメントページに張らせ、README は改訂可能に保つ。非英語話者・非開発者の入口は英語UIの GitHub ではなく実在するドキュメントサイトに寄せる、という nishio の整理
sources:
  - slack-readme-language-docs-site-2026-10-13.md
---

## 何の判断か

2026-10 に [[kouchou-ai]] の README をデフォルト英語化（PR #966）→日本語へ差し戻し（PR #968）した事件をきっかけに、nishio が Slack で 2 つの設計判断を示した（[[slack-readme-language-docs-site-2026-10-13]]より）。

1. **README を外部アンカーリンクで凍結してはいけない**
2. **非英語話者・非開発者の入口は GitHub ではなくドキュメントサイトにする**

どちらも「README を何にどう使わせるか」という境界設定の話で、README の言語（日本語か英語か）そのものより上位の判断にあたる。

## 1. アンカーリンク凍結という footgun

### 問題の形

README の見出しには `#section-名` のアンカーが自動で振られる。外部（別リポジトリ、ブログ、他ドキュメント）がその `README.md#section-名` にディープリンクを張ると、見出しを変える・節を消す・README を書き換えると外部リンクが切れる。この「外部リンクが切れる」ことを理由に README 改訂を止めると、**一度でも外部からリンクされた README は金輪際改訂できなくなる**（nishio）。

これは README という、本来いちばん流動的であるべき入口ドキュメントに、最も硬い制約（安定 URL / 安定アンカー）を背負わせてしまう取り違えである。

### 解決方針

- 外部から恒久的にリンクしたい内容は、**README のアンカーではなく、専用の個別ドキュメントページ**（docs サイトの 1 ページ）に置き、そこへ張らせる
- README はあくまで改訂可能な入口として保ち、安定 URL を提供する責務は docs サイト側に移す
- 既存の README アンカー依存は、徐々にこの形へ置き換えていく（nishio「徐々にそういう形態に置き換えていきたい」）

安定 URL が必要なものと、流動的でよいものを別のレイヤーに分離する、という一般原則の README 版。

## 2. 入口はドキュメントサイト、GitHub ではない

### ohki の懸念と nishio の答え

ohki-shingo は README 英語化に対し「マニュアルを見ようとアクセスした人が全面英語のドキュメントで面食らって離脱する」「そもそも GitHub へのアクセス自体が脱落点になる」という UX 懸念を出した。

nishio の答えは、README の言語を調整して GitHub 上で全員を受け止めようとするのではなく、**読者の層ごとに着地すべき面を変える**こと：

- 英語 UI の GitHub は、本質的に開発者向けの面。ここで非開発者・非英語話者まで受け止めようとするのが無理筋
- 英語で怯む層・マニュアルを読みに来た層が着地すべきは、英語 UI の GitHub ではなく**ドキュメントサイト**

### ドキュメントサイトは実在する

nishio は「ドキュメントサイトも用意したような気がするが記憶の彼方」と言うが、これは実在する： `https://digitaldemocracy2030.github.io/kouchou-ai/`（mkdocs, site_name「広聴AI Documentation」）。README からも各 setup / user-guide ページがここへリンクしている。

したがって不足しているのは「ドキュメントサイト」そのものではなく、**非開発者・非英語話者が GitHub を経由せずに最初からドキュメントサイトへ着地する導線**。これは [[kouchou-ai-docs-entry-restructure-2026-06-03]] が提起した「docs 入口がセットアップ起点」「`getting-started/` というネーミング自体がバイアス」問題と同じ地層にある。README 言語の議論は、そこへ戻る。

## 多言語 README の現在の着地

差し戻し後の current main は、README の言語問題を次の形で一旦収めている（[[slack-readme-language-docs-site-2026-10-13]]より）：

- `README.md` は**日本語をデフォルト**にし、先頭行に `[English] | 日本語 | [한국어]` の言語リンク
- 英語版 `README.en.md`、韓国語版 `README.ko.md` を併存

nishio が 2026-10-09 に提案したのは「README.md を英語にして日本語版をリンク」だったが、ohki の UX 懸念を受けた差し戻しで「日本語デフォルト + 言語リンク」に落ち着いた。言語選択リンクという多言語導線自体は残り、デフォルト言語だけが日本語に戻った、と読むのが正確。これは「緊急避難的 OK」（nishio）な暫定であって、上の 2 判断（アンカー凍結回避・入口を docs へ）が本線の方向性。

## 関連

- **GitHub issue #977**（open / nishio 起票 / 2026-10-12）「docs: README 見出しアンカーへの外部直リンク依存をやめ、安定URL(docs)へ寄せる（PR #968 残件）」が、本判断 1 の root-cause 対応として実在する。issue 本文は、見出しアンカーは言語切替だけでなく**見出しの言い回し変更・絵文字追加・章の並べ替え**でも静かに切れること、切れても 404 でなく README トップに着地して気づきにくいこと、GitHub Markdown ではカスタム anchor id を固定できないことを挙げ、(1) 安定リンク宛先を docs の固定 URL に寄せる（例: `apps/public-viewer/components/reporter/ReporterContent.tsx` のリンク）、(2) README はトップ案内に留める運用、(3) README 内リンクは 1 箇所集約 + **Markdown リンク切れ検出を CI に入れる**、を提案している
- [[slack-readme-language-docs-site-2026-10-13]]: 一次ソース（Slack スレッド + PR 事件）
- [[kouchou-ai-docs-entry-restructure-2026-06-03]] / [[nishio-docs-entry-restructure-discussion-2026-06-03]]: docs 入口の spine 再設計。今回の「入口を docs サイトへ」はこの延長
- [[issue-876-developer-docs-gap-audit-2026-06-30]] / [[docs-issue-map-2026-06-30]]: README と docs の役割分担を整理する #876 系。アンカー凍結回避と「README は改訂可能に保つ」はこの役割分担の前提
- [[interview-feature-requests-2026-10-08]]: 全画面マップの日英韓切替（翻訳）。多言語化は README だけでなく成果物 viewer でも進んでいる

## Open Questions

- README アンカーへの既存外部リンクの実態（どこから何件張られているか）は未調査。issue #977 は少なくとも `apps/public-viewer/components/reporter/ReporterContent.tsx` を宛先候補に挙げるが、全量の棚卸しと移行先ページ・redirect 方針は未定。GitHub Markdown はカスタム anchor id を固定できないので README 内では安定化できず、宛先を docs 側へ移すしかない
- 非開発者を GitHub を経由させずドキュメントサイトへ着地させる具体導線（配布物・事例サイト・検索からの流入をどこへ向けるか）は未設計。docs 入口 spine 再設計（#876 系）と合流させる必要がある
- デフォルト言語を日本語に戻した現状を、国外注目増（nishio の英語化動機）とどう両立させるか。言語自動判定や docs サイト側の多言語化は未検討
