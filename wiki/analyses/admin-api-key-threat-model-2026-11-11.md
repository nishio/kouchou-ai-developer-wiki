---
title: 管理画面の API キーは脅威か、Windows 版の都合を Web に持ち込むか 2026-11-11
type: analysis
summary: "#547（管理画面の API キーをサーバー側に隠す）と #885（Node をなくしてブラウザから FastAPI を直接呼ぶ）の衝突を #1197 で 1 つの選択として立てたが、nishio の指摘で前提を見直した。キーを見られるのは Basic 認証を通った人だけでできることも増えないので脅威と呼ぶほどではなく、Windows 版は Web の管理画面とは別の配布物として考える。#885 で 10-22 から返答待ちの (a)/(b) の確認には、この整理から (a)（Route Handler を残す）が導ける"
sources:
  - source-code.md
---

## 観測範囲と鮮度

- コード: `work/kouchou-ai` の main。議論した時点は `67bc798d`（2026-11-11）で、filing back の時点（2026-11-14）は `4f506750`。ブラウザ側でキーを読んでいる 3 か所と、middleware に matcher がないことはどちらの時点でも同じ
- GitHub: 2026-11-14 に [#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547)・[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885)・[#1197](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1197) を確認。3 件とも open で、2026-11-11 以降の動きはない
- ここで言う「キー」は、管理画面が FastAPI の管理用 API を呼ぶときの `ADMIN_API_KEY` を指す。2026-10 に漏洩が見つかった、利用者が入力する LLM の API キー（[[user-api-key-leak-2026-10]]）とは別物

## 問い

[#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547) は「キーをブラウザに配らないよう、呼び出しを Next.js のサーバー側に移す」。[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) は「Windows 向けに単一の実行ファイルで配るため、管理画面を静的ファイルに寄せ、ブラウザから FastAPI を直接呼ぶ」。片方を進めるともう片方と逆向きになるので、2026-11-11 に [#1197](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1197) を作り、A（隠す）／B（見えてよいとする）／C（FastAPI 側にログインを持つ）から選ぶ問いとして立てた。

## 結論

nishio の指摘を受けて、[#1197](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1197) の問いの前提を取り下げた（[2026-11-11 のコメント](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1197#issuecomment-6786018843)）。

1. **1 つのコードベースで両方のニーズを満たそうとしない。** 設計として無理がある
2. **管理画面にアクセスできる人がキーを知り得ることは、脅威と呼ぶほどではない。** [#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547) を安全上の問題として扱う理由は薄い
3. **Windows 版の都合を Web サービスに押し付けない。** Web の管理画面は今の形（Next.js と FastAPI）を保ち、Windows 版は別の配布物として考える

## キーを見られるのは誰で、何ができるようになるか

- キーは `NEXT_PUBLIC_ADMIN_API_KEY` として admin のビルド時に JS に埋め込まれる。ブラウザ側のコードで読んでいるのは、進捗の確認（`useReportProgressPolling.ts`）、スプレッドシートの取り込み（`create/api/spreadsheet.ts`）、モデル一覧（`useModelCatalog.ts`）の 3 か所。2025-07 の Server Actions 化（[#614](https://github.com/digitaldemocracy2030/kouchou-ai/issues/614)〜[#676](https://github.com/digitaldemocracy2030/kouchou-ai/issues/676)）で、それ以外の呼び出しはサーバー側に移っている
- 管理画面の Basic 認証（`apps/admin/middleware.ts`）には matcher がないので、ビルド済みの JS（`/_next/static`）も含めて全部のパスにかかる。**キーを見られるのは、Basic 認証を通った人だけ**
- その人たちは、キーがなくても管理画面からレポートの作成・削除・CSV のダウンロードができる。**キーを手に入れても、できることは増えない**
- Basic 認証をオフにしている環境（既定はオフ）では、管理画面に届く人は誰でも画面を操作できる。この場合も、キーが余分な権限を与えるわけではない。既定の `HOST_BIND_ADDRESS=127.0.0.1` なら、そもそも自分の PC からしか届かない

違いが残るのは次の 2 点で、どちらも「信頼して管理権限を渡した人」への対策にあたる。

- アクセスを取り上げた後も、admin を再ビルドしてキーを変えるまで使える
- 画面を通らず FastAPI を直接呼べる

今の Basic 認証自体が全員で 1 つのパスワードを共有する方式なので、キーだけを厳しく守っても守りの強さが揃わない。人ごとに取り消せるようにしたいなら、キーではなく認証の仕組みから変える話になる。

### それでも [#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547) に残る整理

`NEXT_PUBLIC_ADMIN_API_KEY`（ブラウザ側）と `ADMIN_API_KEY`（サーバー側の 2 経路）に同じ値を入れる運用は、事故の元になっている。[#1087](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1087) では、Azure と `.env-sample` で片方しか渡しておらず、再利用設定の取得と複製が 500 になった。これは安全ではなく運用の話なので、[#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547) を残すならこの整理に範囲を絞り、優先度を下げる。

## Web と Windows 版を分ける

- **Web サービス**: Next.js の管理画面と FastAPI の今の形を保つ。[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) を理由に Node をなくすことはしない
- **Windows 版**: 管理画面の作り直しではなく、別の配布物として考える。たとえば analysis-core の CLI と静的 HTML のレポートを核にし、必要なら薄い専用の画面を付ける。高度な機能を CLI から先に入れる今の進め方（[#515](https://github.com/digitaldemocracy2030/kouchou-ai/issues/515)、[#176](https://github.com/digitaldemocracy2030/kouchou-ai/issues/176)）とも合う

これまでの整理（[[node-runtime-free-windows-exe-2026-05-31]]、[[windows-distribution-options]] の段階 4a）は、Web の管理画面そのものから Node をなくす前提だった。この結論は、その前提を「Windows 版は別の配布物」に置き換える。

## [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) の進行中の作業への影響

[#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) は yasumorishima が 2026-10-22 から担当し、同日に次の計画を出して方針の確認を求めている。2026-11-14 時点で返答はない。

1. FastAPI に静的書き出しのエンドポイント（`POST /admin/reports/static-export`）を足す。既存の経路は変えない
2. 静的ファイル一式（shell）を API のイメージでビルドし、admin の呼び先を環境変数で切り替えられるようにする
3. 既定を切り替え、static-site-builder を退役させる

このうち確認を求められているのは、admin から書き出しを呼ぶ経路の選び方。

- (a) `/api/download` の Route Handler（Node）を残して中継する
- (b) 進捗の確認と同じく、ブラウザから `NEXT_PUBLIC_ADMIN_API_KEY` で直接呼び、Route Handler をなくす

担当者は [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) の完了条件（Node をなくす）を理由に (b) を推していた。この結論からは **(a)** が導ける。(a) を避ける理由として挙がっていた「Azure の admin にはサーバー側の `ADMIN_API_KEY` が渡っていない」は、[#1087](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1087)（2026-10-23 merge）で解消済み。1 の FastAPI 側のエンドポイントと、3 の static-site-builder の退役は、Web の形を変えないのでこの結論と衝突しない。

## 次の手（2026-11-14 時点で未実施）

- [#1197](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1197): 「1 つのコードベースで両立させない。キーの露出は脅威として扱わない」で閉じる
- [#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547): 2 つの変数を 1 つにまとめる整理に範囲を絞って優先度を下げるか、閉じる。担当はいない（2026-11-08 に前の担当者が外れた）
- [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885): 完了条件の「Web UI の Node 依存をなくす」を見直す。10-22 の確認には (a) で答える。担当者に届く文面なので、出す前に nishio が確認する

## Open Questions

- Windows 版を「CLI と静的 HTML」にした場合、非専門家の Windows 利用者が CSV を入れてレポートを作るまでの画面をどこまで用意するか。[[windows-distribution-options]] の段階 2〜3（ランチャー、デスクトップアプリ）との関係は未整理
- リモート運用で人ごとに管理権限を取り消したい需要（自治体で担当者が異動する、など）が実際にあるか。あるなら、キーではなく管理画面の認証の作り直しとして別に扱う
- [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) の完了条件を変える場合、すでに merge 済みの shell ビルド（[#935](https://github.com/digitaldemocracy2030/kouchou-ai/issues/935)）と Node 依存一覧の docs（[#903](https://github.com/digitaldemocracy2030/kouchou-ai/issues/903)）は Web 側の改善として残るのか

## 関連

- [[stale-issue-disposition-2026-11-02]] — [#547](https://github.com/digitaldemocracy2030/kouchou-ai/issues/547) の担当確認（棚卸し D 群）
- [[github-issue-885-pr-903-live-2026-06-30]] — [#885](https://github.com/digitaldemocracy2030/kouchou-ai/issues/885) の 2026-06 時点の状態
- [[meeting-report-draft]] — 定例の議題候補
