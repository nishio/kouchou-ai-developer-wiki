---
title: "本体 docs 改善スプリント振り返り 2026-10"
type: analysis
summary: "2026-10 に実施した kouchou-ai 本体 docs（mkdocs サイト + README）の改善スプリントの retrospective。setup-first で読者を振り落としていた入口を demo-first に組み替え、閲覧者・自治体・実務者向けの空白ページを埋め、レポートの責任所在を 3 レイヤーで明文化し、入口ディレクトリ改称・README アンカー脱却・リンク切れ CI までを 13 PR で landing させた。通底する設計原則と、live 検証→ペルソナ監査→discover-fix-gate という再利用可能な進め方をまとめる"
sources:
  - kouchou-ai-docs-improvement-roadmap-2026-10-13.md
  - docs-persona-review-2026-10-13.md
  - kouchou-ai-docs-policy-history.md
  - github-dev-docs.md
---

## 何のスプリントか

2026-10、[[kouchou-ai]] 本体ドキュメント（mkdocs サイト `digitaldemocracy2030.github.io/kouchou-ai/` と `README.md`）を、散発的な改善でなく **一連のスプリント**としてまとめて改善した。起点は「docs 方針が [[kouchou-ai-docs-policy-history]] に系譜として集約されていたが、実装は追いついていなかった」こと。計画は [[kouchou-ai-docs-improvement-roadmap-2026-10-13]] に、読者体験の監査は [[docs-persona-review-2026-10-13]] にある。本ページはその **読み物としての総括**（何を・なぜ・どうなったか・どう進めたか）。

結果として本体 repo に **PR [#998](https://github.com/digitaldemocracy2030/kouchou-ai/issues/998)〜[#1006](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1006) / [#1008](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1008)〜[#1010](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1010)（計 13 本）** を投入・merge し、`v4.1.0` を発行、issue **[#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542) / [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) / [#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)** を決着させた。

## 出発点：なぜ docs を直したか

- **入口が setup 起点**：docs が `getting-started/`（＝セットアップ手順）から始まり、「興味を持った人＝自分でツールを建てる開発者」というバイアスを産んでいた。レポートの閲覧者・自治体担当・方法論に関心のある人が最初の数行で振り落とされていた。
- **書いたのに届かない**：`docs/` にあるのに nav 未登録で公開サイトから辿れないページが 6 本。しかも nav 劣化を検知する仕組みがなかった。
- **content gap**：閲覧者向けの「レポートの読み方」、自治体向けの「費用・個人情報・相談先」、実務者向けの「結果の信頼性・責任の所在」が存在しなかった。FAQ は実体が開発者トラブル 1 件だった。
- **責任所在が未明文化**：レポートの免責は「LLM バイアス注意」だけで、「誰が何に責任を負うのか」が書かれていなかった（issue [#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)）。
- **壊れやすいリンク**：レポート閲覧画面が README の見出しアンカーに外部直リンクしており、見出しの言い回し変更で静かに切れる構造だった（issue [#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)）。

背景の最上流には、2026-05 の気づき「**kouchou-ai の docs は説明資料であると同時に、AI コーディングエージェントにとっての reusable prompt / template でもある**」がある（[[auto-cluster-defaults]]）。docs の質は人間だけでなく AI の既定値も左右する。

## どう進めたか（フェーズと PR）

| フェーズ | 中身 | 主な PR |
|---|---|---|
| **Tier 0** | nav 未登録 6 ページ登録＋`validation.nav.omitted_files: warn` の **rot-gate**（以後の orphan を CI が検知）、CLI の embedding モデル設定を明記 | [#998](https://github.com/digitaldemocracy2030/kouchou-ai/issues/998)、`v4.1.0` 発行 |
| **T1（入口の reader-facing）** | `index.md` を **demo-first の「目的別ガイド」**（読者像で分岐）に、`how-to-use` を最新 WebUI に追従、WebUI 変更時に how-to-use 更新を促す**非ブロッキング reminder** | [#999](https://github.com/digitaldemocracy2030/kouchou-ai/issues/999) / [#1000](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1000) / [#1001](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1001) |
| **content gap** | 「レポートの読み方」「導入を検討する方へ（費用・PII・相談先）」「結果の信頼性・限界・責任の所在」を新設、FAQ を閲覧者向けに刷新 | [#1002](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1002)（quick fix）/ [#1003](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1003) |
| **責任所在（[#542](https://github.com/digitaldemocracy2030/kouchou-ai/issues/542)）** | 免責に **責任の 3 レイヤー**（OSS 開発者／サービス運営者／レポート作成者）を明記（footer 2 コピー＋README 日英韓） | [#1004](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1004) / [#1008](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1008) |
| **Tier 3（構造の本丸）** | `getting-started/` → `self-hosting/` 改称＋**mkdocs-redirects で旧 URL 救済**、README アンカー直リンクを安定 docs ページへ移行 | [#1005](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1005)（[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)）/ [#1006](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1006)（[#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)） |
| **仕上げ** | 内部リンク/アンカー切れを **CI で検知**（mkdocs link validation ＋ GitHub 互換 slugify）、起動モードの canonical「始め方の選び方」ページ | [#1009](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1009)（[#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977)）/ [#1010](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1010)（[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876)） |

## 何が変わったか（現在 live）

- **入口が demo-first**：トップは「何をしたいか」で分岐する目的別ガイド。setup は「自分で建てる人」が辿り着く先に降格。`getting-started/` は `self-hosting/` に改称（旧 URL は redirect で温存）。
- **読者の空白が埋まった**：閲覧者（読み方）・自治体（導入判断）・実務者（信頼性・責任）・CLI 研究者（バグ修正と設定）に、それぞれ着地できるページがある。
- **腐らない仕組み**：nav 未登録・内部リンク/アンカー切れを **CI（`mkdocs build --strict`）が検知**。WebUI 変更が how-to-use を取り残すと reminder が出る。
- **責任が明文化**：レポートの責任所在が 3 レイヤーで日英韓の免責に明記。
- **安定 URL 責務が docs 側へ**：外部に張らせる stable link は README アンカーでなく docs ページに。

## 通底する設計原則

スプリント全体を貫く原則は [[kouchou-ai-docs-policy-history]] に系譜としてまとまっている。要点のみ：

- **docs は AI の default / template**：具体例は「読者がコピペするか」だけでなく「AI が既定値と見なすか」で評価する。
- **setup 起点をやめ、読者像で分岐する（demo-first）**：入口はレポート閲覧。
- **「開発者」を一括りにしない**：読者像ごとに着地面を変える。
- **安定 URL 責務は docs ページ、README は改訂可能な入口**。
- **公開境界**：Azure デモの実 URL・resource・secret・手順は docs に書かない。免責・案内の粒度に留める。
- **責任は 3 レイヤー**：OSS 開発者（無保証提供）／サービス運営者（運用）／レポート作成者（内容）。

## 再利用できる進め方（方法論）

このスプリントで有効だった進め方は、他の改善にも転用できる。

1. **live 検証を前提にする**：wiki の方針記述は stale しうるので、着手前に `work/kouchou-ai` の current main と GitHub の issue/PR 状態を照合してから動く。実際、着手前の照合で「audit が [#450](https://github.com/digitaldemocracy2030/kouchou-ai/issues/450) を『記載あり』と誤記」「[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) は議論停止でなく umbrella 再スコープ」等の stale を複数発見した。
2. **ペルソナ監査で content gap を見つける**：完成した docs を複数の読者ペルソナの視点で「トップから辿って詰まる点」を洗い出す（[[docs-persona-review-2026-10-13]]）。「書いた側の想定」でなく「読む側の経路」でギャップが出る。
3. **discover → fix → gate**：構造的な劣化（nav orphan、リンク切れ）は、まず現状の違反を洗い出して直し、その上で **CI ゲートを立てて再発を止める**。gate だけ先に入れると main が赤くなり、fix だけだと再び腐る——両方を同じ PR に。
4. **content は起草 → レビュー → コードで裏取り**：新規ページは下書きを作り、主張（費用・データ送信先・挙動）を実装（`services/llm.py` 等）で裏取りしてから出す。捏造しない（具体的な金額は「従量課金の考え方」まで）。
5. **破壊的変更は救済とセット**：ディレクトリ改称は mkdocs-redirects で旧 URL を温存してから。外部リンクを切らない。
6. **多言語・法務文面は逆翻訳で検証**：免責の en/ko 翻訳は、日本語への逆翻訳で原文と一致を確認してから反映。
7. **大きな umbrella は de-bundle**：[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) は複数 issue を束ねていたため、headline 達成で close する際に、独立課題（[#496](https://github.com/digitaldemocracy2030/kouchou-ai/issues/496) Docker なし／[#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921) ブラウザ版本流化）を切り離し、残細目は小さな follow-up（[#1012](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1012)）へ引き継いだ。

## 残りと今後

- **[#1012](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1012)**（OPEN・任意）：README スリム化、起動モード別の落とし穴集約、Docker Desktop 代替・構造把握スタンス・Mode 4 データ量前提。[#876](https://github.com/digitaldemocracy2030/kouchou-ai/issues/876) の残細目。
- **[#496](https://github.com/digitaldemocracy2030/kouchou-ai/issues/496) / [#921](https://github.com/digitaldemocracy2030/kouchou-ai/issues/921)**（OPEN・独立）：Docker なし配布（エンジニアリング）／ブラウザ版を本流とするか（戦略）。docs 入口とは別テーマ。
- **保守の持続**：rot-gate・link-check・how-to-use reminder が入ったので、今後は「feature と一緒に docs が腐らない」かを運用で見ていく。

## 関連

- [[kouchou-ai-v4-1-0-release-2026-10]]：本 docs 改善を含む v4.1.0 リリース全体の総括（feature/fix/基盤も含む）
- [[kouchou-ai-docs-improvement-roadmap-2026-10-13]]：計画と各 Tier の意思決定・実行ログ（本ページの詳細版）
- [[docs-persona-review-2026-10-13]]：7 ペルソナによる読者体験監査（content gap の出所）
- [[kouchou-ai-docs-policy-history]]：docs 方針の系譜と横断原則
- [[kouchou-ai-docs-entry-restructure-2026-06-03]]：demo-first spine の原案
- [[readme-anchor-freeze-and-docs-entry-2026-10-13]]：[#977](https://github.com/digitaldemocracy2030/kouchou-ai/issues/977) アンカー凍結回避の判断
