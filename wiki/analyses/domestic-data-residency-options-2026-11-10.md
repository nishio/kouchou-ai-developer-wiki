---
title: "データ分析を国内だけで完結させる選択肢（2026-11-10）"
type: analysis
summary: "『意見データを国外に出したくない』要件への選択肢を、ローカル計算・Azure OpenAI の国内リージョン・Amazon Bedrock・Vertex AI 東京・源内で比べた整理。上位 Issue #1190 を立て、Bedrock 対応 #1169 をその子にした。結論は、データを出さないのが目的ならローカル計算が第一候補（『国内』の意味が事業者や庁内まで及ぶならクラウドは外れる）。Azure は今の機能のままデプロイ種別を Standard（リージョン単位）にすれば国内処理になるが、Japan East の従量課金で使えるチャットモデルは gpt-4o（2024-11-20）と gpt-4.1-mini だけで、どちらも 2027-04-14 に廃止予定"
sources:
  - source-code.md
---

## 経緯

2026-11-09〜10 に nishio と Claude Code が、shingo-ohki さん（[[ohki-shingo]]）の Bedrock 対応の提案（[#1169](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1169)、検証は [#1170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1170)）を読んだことから始まった。会話で論点が次のように動いた。

1. Bedrock 対応は boto3 を本体に入れるか → OpenAI 互換の経路なら不要、IAM 認証で Claude を呼ぶ場合だけ増えうる。[#1042](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1042)（Anthropic API 直）は boto3 と無関係で、`anthropic` を任意の依存にすれば本体は増えない
2. Azure は国内ではないのか → デプロイ種別しだいで国内になる（下記）
3. Google GenAI（Vertex AI）やブラウザ版は → どちらも国内または端末内の経路を持つ
4. nishio：「国外にデータが出て欲しくないならローカルで計算したらいいんでは？」→ この問いを上位に置き、Bedrock を実装案の一つにする整理に組み直した

成果物は上位 Issue [#1190](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1190)「データ分析が国内だけで完結できるようにしたい」（2026-11-10 作成、#1169 を GitHub の子 Issue に設定。#1170 は #1169 の本文から参照されるだけで、子 Issue の関係は付けていない）。比較の詳細は Issue 本文を正とし、ここには判断の筋と鮮度を残す。

## 要点

### 「国内」の意味を先に決める

| 段階 | 意味 | 満たせる案 |
|---|---|---|
| A | 処理と保存の場所が日本国内 | 全案（クラウドは設定次第） |
| B | A に加えて事業者も国内（米国法などの適用を避ける） | ローカル計算（または国内事業者の基盤） |
| C | 端末や庁内のネットワークから外に出さない | ローカル計算のみ |

クラウドの国内リージョンで満たせるのは A まで。B・C が要件なら Azure・Bedrock・Vertex は外れる。

### 案ごとの現在地

- **ローカル計算（第一候補）**：本体の provider `local` ＋ローカル埋め込み、ブラウザ版の Gemini Nano ＋ transformers.js、LLM を使わない経路（[[offline-local-clustering]]）がすでにある。[#471](https://github.com/digitaldemocracy2030/kouchou-ai/issues/471) にコミュニティの実測（RTX 3090 で 48 件が全工程 2 分 33 秒、GPU なし 4 コア 16GB で抽出 1 件約 8 秒、誤読約 3%）。足りないのは推奨スペックの案内、思考型モデルに `reasoning_effort` を渡す手段、CLI での抽出スキップと LLM なしの集計の正式化、[#898](https://github.com/digitaldemocracy2030/kouchou-ai/issues/898)
- **Azure OpenAI**：本体は対応済み（[[llm-providers]]）。推論が国内に収まるのは Standard（リージョン単位）と Regional Provisioned だけで、Global は任意のリージョン、Data Zone の APAC は Japan East から使う場合でもオーストラリア・韓国・東南アジア・インドを含む。Japan East の Standard で使えるチャットモデルは gpt-4o（2024-11-20、Legacy）と gpt-4.1-mini（Deprecated）だけで、どちらも 2027-04-14 に廃止予定。新しいモデルはリージョン単位に「最後に、時期の保証なく」来る。Regional Provisioned なら gpt-5 系も使えるが、最低 25〜50 PTU で単発の分析には重い。docs に「国内処理ならデプロイ種別を Standard に」という案内がない
- **Amazon Bedrock**：公式ドキュメント上、gpt-oss や Qwen3 は東京リージョン内で処理でき、OpenAI 互換 API と Bedrock API キーで呼べる（新しい依存なし）。Claude は日本限定の推論プロファイル（東京・大阪）。埋め込みは OpenAI 互換で呼べない見込み。ブラウザ版はすでに Bedrock（OpenAI 互換）に対応しているが、CORS のため国内に置いたプロキシが要る。いずれも実機では未確認（#1170 の対象）
- **Vertex AI 東京**：本体の Gemini は Developer API で地域を指定できない。同じ `google-genai` SDK の `vertexai=True` に切り替えれば東京を指定でき、新しい依存は要らない。日本での処理が明記されたモデルは Gemini 3.5 Flash と一部の埋め込みに限られ、従量課金での保証範囲は読み方があいまい
- **源内（デジタル庁）**：2026-04 に OSS 公開、2026-10 に自治体向け実証の参加募集。外部アプリから使える API は確認できていない

### 進め方（Issue での提案）

1. 「国内」の意味（A／B／C）を利用者の要件から決める
2. 今の機能で満たせる部分を docs にする（ローカル計算の推奨構成、Azure のデプロイ種別）
3. クラウドの国内リージョンを実機で検証する（#1170 の対象を Azure・Vertex に広げるか）。Bedrock はブラウザ版で本体を実装せずに検証を始められる
4. 本体に新しい接続先を足すかは 3 の結果で決める

## 情報鮮度

- Azure の仕様は Microsoft Learn の公式ページで 2026-11-10 に確認（deployment-types は 2026-08-12 更新、リージョン別一覧は 2026-10-19 更新、廃止予定表は 2026-09-23 更新）。Japan East の Standard の行と廃止予定は表を直接読んで照合した
- Bedrock・Vertex・源内・ISMAP は subagent の Web 調査（2026-11-09〜10）で、Issue 本文に出典 URL を付けた。Claude Code が自分で表を読み直したのは Azure だけ
- ブラウザ版の対応状況は tokoroten/kouchou-ai-serverless の README・`src/types/settings.ts`・`docs/DESIGN.md` を 2026-11-09 に読んだ（push は 2026-11-06）。動かしてはいない
- 本体のコードは main `ddd0bacd`（2026-11-08）で確認

## Open Questions

- 想定する利用者（自治体・官公庁）が求める「国内」は A・B・C のどれか。ISMAP 登録だけで足りるのか、管轄（米国 CLOUD Act など）まで問うのか
- Japan East で、新規のサブスクリプションから gpt-4o（2024-11-20）や gpt-4.1-mini の Standard を今も作れるか（Legacy／Deprecated の扱いと、リージョン別一覧の ✅ が食い違う可能性）
- Azure の 2027-04 以降、リージョン単位の Standard に後継モデルが来なければ、Azure での国内処理は Provisioned（高価）しか残らない
- Bedrock の gpt-oss-120b で json_schema の構造化出力が通るか（モデルカードに記載がない）
- 源内に外部アプリ向けの API があるか

## Updates

- 2026-11-10: 初回作成。上位 Issue [#1190](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1190) を作り、[#1169](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1169) を子 Issue にした
- 2026-11-10: 案 1（ローカル計算）の品質の材料が、同じ日の別の作業で増えた（[[team-mirai-local-llm-quality-2026-11-10]]）。チームみらいの公開データで、30B 級のオープンウェイト（gemma-4-31B、Qwen3.8-27B）は抽出・ラベルとも既定の gpt-4o-mini に劣らないと判定された。上の「要点」にある #471 の実測は速度の話で、品質はこちらを見る。普通の PC で動く 8B 級の品質はまだ測っておらず、判定役（Claude）を人の判定で較正する段も残る。#1190 の本文にはまだ反映していない
- 2026-11-10: 同じ日に、普通の PC で動く大きさのモデルの品質も測った（[[team-mirai-local-llm-quality-2026-11-10]] の結果 3）。gemma-4-E4B は抽出・ラベルとも gpt-4o-mini に劣らないと判定され、案 1 の品質の見通しは明るくなった。ELYZA-JP-8B は 200 件中 2 件でプロンプトの例文をそのまま返した。判定役の較正は残る
- 2026-11-10: Slack での議論の現状と、そこからの考察を追記した（slack-logs の mirror を 2026-11-10 10:24 JST の同期分まで読んだ。`raw/` の固定 snapshot はない）
  - **経緯**：[#1169](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1169)・[#1170](https://github.com/digitaldemocracy2030/kouchou-ai/issues/1170) は 2026-10-29 に [[ohki-shingo]] さんが GitHub に直接立てた。Slack に流れたのは GitHub 連携の通知だけで、Slack での議論は 2026-11-10 朝の nishio の投稿（#2_開発_広聴ai）が最初。「国内で完結したいニーズは追う価値がある。Bedrock を使っている想定顧客がいるならタッグを組んで検証してよいが、dd2030 がこれから Bedrock を契約して検証するのは何のためか。GPT-OSS 120B で十分かも分からない」とし、6 分後に #1169 を #1190 の実装案の一つとして整理すると続けた。同期の時点で返信はない。#1169・#1170 とも assignee なし、着手した PR もない
  - **対立は見かけより小さい**：#1169 の技術メモは「Bedrock 対応そのものを目的化しない」「東京のエンドポイント指定だけでは国内完結の証明にならない」と書いており、慎重さの点では #1190 と同じ立場にある。食い違っているのは「誰の、どの要件のために、誰の費用で検証するか」。同じ Slack 投稿で nishio 自身が、クラウドの国内リージョンが意味を持つ場面として「組織の共用サーバとして複数の人で使いたい」を挙げている。大木さんは 2026-10-28 に、いどばた・広聴AI を試せる独立の試験環境（運営は DD2030 と別）を Slack で紹介しており、提案がこの「共用サーバ」側の立場から来ている可能性がある（推測。本人に確認していない）。それなら、AWS を使う運用主体と組んで検証する、という nishio の条件にそのまま当てはまる
  - **品質の検証は Bedrock の契約と切り離せる**：#1170 の候補のうち GPT-OSS 120B と Qwen3 235B はオープンウェイトなので、品質は配信元によらず測れる。[[team-mirai-local-llm-quality-2026-11-10]] の評価の仕組み（公開データ・出どころを伏せた 2 案比較）に、どこかの配信元経由でそのまま足せる（公開データなので国外を通っても問題ない。配信元ごとの量子化の違いは残る）。同じ日の実験で 8B 級でも gpt-4o-mini に劣らないと判定されたので、「120B で十分か」は品質よりも構造化出力が通るかの問題になりそう。Bedrock で実機確認が要るのは、国内での処理経路、json_schema の構造化出力、API キー、スロットリングと費用に絞れる
  - **本体はコード変更なしで試せる可能性がある**：main `ddd0bacd` の provider `local` は、`https://` の URL をそのまま base URL に使い（`/v1` で終わらなければ補う）、`LOCAL_LLM_API_KEY` を `LOCAL_LLM_ALLOWED_BASE_URLS` に一致する接続先へ送る（`packages/analysis-core/src/analysis_core/services/llm.py` の `resolve_local_llm_base_url` / `resolve_local_llm_api_key`）。Bedrock の OpenAI 互換エンドポイントと Bedrock API キーをここに入れれば、チャットは今のまま呼べるかもしれない。構造化出力は OpenAI SDK の `parse()`（json_schema）を使うので、gpt-oss がそれを受け付けるかが分かれ目。埋め込みは同じ接続先に送られるので、Bedrock 側に OpenAI 互換の埋め込みがなければ、埋め込みは別の手段（ローカル）に分ける必要がある。いずれも実機では未確認
  - **残る問い**：大木さんの想定利用者は誰か（自治体本体か、共用の運用主体か）。自治体がすでに AWS 上で動かしている環境（ガバメントクラウドなど）を使いたい要件なのか。その場合「国内」は段階 A（＋ISMAP）で足りるのか
- 2026-11-10: 大木さんの返信と、その後の nishio の反応を読んだ（slack-logs の mirror を 2026-11-10 13:34 JST に手動で同期し、#2_開発_広聴ai の 11:05〜13:27 JST を読んだ。`raw/` の固定 snapshot はない）
  - **大木さんの背景**：自治体への導入を提案する事業者（SIer）2 社と話したところ、どちらも真っ先に Bedrock の話が出た。SIer にとっては、自治体から求められるセキュリティや運用の要件を満たすうえで、AWS のようなクラウド基盤のほうが提案しやすい。前提は保存だけでなく推論も国内で完結すること。GPT-OSS 120B は使いたいモデルだからではなく、Bedrock で国内推論ができるモデルが限られるから挙げた。DD2030 が優先度を上げる必要はなく、「Bedrock に対応すれば SIer 経由で採用されやすくなる」というシグナルを共有するために Issue にした。事業者の中から、個人として開発に参加したい人も出始めた。品質評価のやり方は知見を借りたい。将来はさくらのクラウドなど、GAFAM への依存を減らした構成も面白い
  - **nishio の反応**：「DD2030 では動作確認していないが、Bedrock ではこう構成できる。トラブルがあればフィードバックを」というプロトタイプ実装とドキュメントがあるとよい（12:58）。続けて「今サポートしている接続先も DD2030 が動作確認や保証をしているわけではないので、気にせず Bedrock 対応のコードを入れればいいだけな気もしてきた」（13:27）
  - **前回の推測の答え合わせ**：大木さん自身の試験環境ではなく、提案する側の SIer の要望だった。「誰の要件か」は「SIer が提案書に書けること」で、段階で言えば A（処理と保存が国内）を、自治体の調達で通る形で示すこと。技術的な国内完結より、構成として名前が挙がることが先に効く
  - **最小の対応**：main `ddd0bacd` では、埋め込みは「サーバー内蔵の埋め込み（`is_embedded_at_local`）」か「チャットと同じ接続先」のどちらかで、国外の接続先へ黙って切り替わる経路はない（`request_to_embed`）。provider `local` に Bedrock 東京の OpenAI 互換エンドポイントと Bedrock API キーを入れ、埋め込みをサーバー内蔵にすれば、構成のうえでは推論と埋め込みが国外に出ない見込み。nishio の言う「プロトタイプとドキュメント」は、まずこの構成を書いた docs で足り、管理画面に「Amazon Bedrock」と名前が出るようにするのは提案しやすさのための追加になる。IAM 認証で Claude を呼ぶ経路（boto3 が要る）は後回しにでき、入れるなら本体の依存にしない。gpt-oss が json_schema の構造化出力を通すかは、実機で確かめるまで分からない
  - **品質評価は手伝える**：大木さんが知見を借りたいと言った品質評価は、[[team-mirai-local-llm-quality-2026-11-10]] の仕組みにオープンウェイトの候補（GPT-OSS 120B、Qwen3 235B）を足せば、AWS の契約なしで測れる。#471 とつながる
  - **残る問い**：興味を持った事業者の人が、AWS の実機での検証（国内の処理経路、構造化出力、費用）を担えるか。「使おうとしたが導入に至らなかった理由」を開発側に届ける置き場をどうするか
