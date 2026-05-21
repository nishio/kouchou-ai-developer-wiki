---
name: agent-sandboxing-strategy
summary: "AI コーディングエージェント向けの開発環境分離方針 — host full access を標準にしない"
type: analysis
sources:
  - github-dev-docs.md
  - open-pr-observation-2026-05-18.md
---

2026-05 時点の `kouchou-ai` は、Docker Compose によるマルチサービス起動、`packages/analysis-core/` の Python 実装、`apps/*` の pnpm ワークスペース、Azure / PyPI / GitHub 操作が同じ開発面に共存している。[[github-dev-docs]]より

この構成で AI コーディングエージェントに **host machine full access** を与えると、「コード編集に必要な権限」と「本番・認証・他 repo まで壊せる権限」が同居しやすい。特に `.env` の build-time 焼き込み、Azure deploy ターゲット、PyPI publish、GitHub branch 操作は破壊半径が大きい。[[github-dev-docs]]より

## 結論

長期の標準形としては、**host full access を常態化しない** 方がよい。

推奨は次の 3 層分離：

1. **AI の作業面** — devcontainer または agent 専用 Docker コンテナ
2. **人間の確認面** — ローカル Docker Compose / ブラウザ / 必要ならネイティブ実行
3. **高権限操作** — CI または人間のみ（Azure deploy, PyPI publish, 長期 credential 利用）

## なぜ devcontainer / 専用コンテナが良いか

- `kouchou-ai` では Python / Node / pnpm / git / `gh` が同時に必要で、単純な read-only sandbox では作業しにくい。devcontainer なら **開発に必要な道具は入れつつ、ホスト全体への露出だけ絞れる**。[[github-dev-docs]]より
- Compose は「アプリを動かす基盤」として既に自然に存在している。そこへさらに「AI の編集面は別コンテナ」と分ければ、役割が明快になる。[[github-dev-docs]]より
- 2026-05-18 の PR review triage では GitHub branch 操作だけでも stale PR の head drift という運用事故があった。branch push のような日常操作でさえ repo 外まで広い権限は不要だった。[[open-pr-observation-2026-05-18]]より

## 推奨する収束形

### 1. 標準は devcontainer

- source checkout を mount
- Python / pnpm / git / `gh` / test dependency を同梱
- `.env` はダミー既定、実 credential は必要時だけ人間が注入
- AI は原則この中で `pytest`, `ruff`, `pnpm test`, 軽い `gh` 操作まで行う

### 2. Compose は実行基盤

- `docker compose up` は api / admin / public-viewer / ollama 等の起動に使う
- AI 用コンテナから Compose のサービスを叩いて動作確認する
- ブラウザ確認や手動 UX 確認は人間側のローカル環境に残す

### 3. 高権限操作は分離

- Azure deploy
- PyPI publish
- 長期 credential を使う cloud 操作
- 破壊的な repo 管理操作

これらは CI か人間のみの責務に寄せる。AI に「できる」状態を作らない方が安全。[[github-dev-docs]]より

## Docker only ではなく「編集面の隔離」が必要

Compose だけで全部を閉じても、実際にはホストの `$HOME`、他 repo、SSH key、ブラウザ cookie、永続 credential へのアクセス経路が残りやすい。問題は「Docker を使っているか」ではなく、**AI がどの filesystem / credential / deploy surface に触れられるか**。したがって「Compose があるから十分」ではない。

## 運用ルールの叩き台

- AI の標準権限は `workspace + devcontainer 内フルアクセス`
- host full access は例外運用にし、理由を明示する
- `.env` 実値や cloud credential は mount しない
- deploy / publish 系コマンドは CI workflow に寄せる
- review fix や branch push は可能でも、repo 設定変更や secrets 変更は人間だけに限定する

## Open Questions

- devcontainer を単一の重量級イメージにするか、`analysis-core` と front 用で分けるか
- `gh` を devcontainer に入れる場合、どこまでの GitHub write を許すか
- Browser automation と local container networking の標準接続手順

## Updates

- 2026-05-18: 初回作成
