---
type: analysis
summary: "pipeline step 追加設計をメンテナーと議論するための論点整理。主題は `#874` を optional にするかではなく、`8 steps` 固定テストを修正して default pipeline への step 追加を許容する設計判断に進むかどうか"
sources:
  - pipeline-step-addition-framing-2026-05-27.md
  - open-pr-pipeline-step-observation-2026-05-28.md
  - pipeline.md
  - strategic-development-order-2026-05-23.md
---

## 議論したい設計判断

主題は `#874` の実装を optional にするかどうかではない。  
本当に決めたいのは、**現在 CI で落ちている `8 steps` 固定テストを修正し、default pipeline への step 追加を許容する方向に進むかどうか** である。

`#874` は `hierarchical_layout_generation` を追加し、default hierarchical workflow / specs / plan が 8 step から 9 step になる。これに対して CI は次の固定期待で落ちている。[[open-pr-pipeline-step-observation-2026-05-28]]より

- `len(specs) == 8`
- `len(plan) == 8`
- `len(orchestrator.steps) == 8`

これは単なるテスト修正漏れではなく、**default pipeline は 8 step である** という暗黙の contract をテストが守っている状態と読むべきである。  
したがって、`#874` をこの形で進めるなら、まずメンテナー間で「その contract を変えるか」を合意する必要がある。

## 決めること

問いは次の 1 つに絞る。

> default pipeline は、durable artifact を追加するために step 数が増えることを許容するか？

この答えによって、テスト修正の意味が変わる。

- 許容するなら、`8` を `9` に直すだけでなく、テストを「固定 step 数」から「期待する step ID / dependency / artifact contract」を検証する形へ更新する。
- 許容しないなら、`8 steps` テストは正しく落ちている。`#874` は default workflow に step を足さない形へ設計変更する。

## 選択肢

### A. step 追加を許容しない

`8 steps` 固定テストを policy gate として維持する。  
`#874` は `hierarchical_visualization` の内部処理、または default plan 外の補助コマンド / optional path に戻す。

利点:

- 既存 pipeline mental model を維持できる
- status / rerun / docs / UI の追従を避けられる
- 「表示用の派生成果物」が default analysis 成否に影響しない

欠点:

- `layouts` を durable artifact として扱いにくい
- HTML を出さず layout artifact だけ欲しい研究用途に弱い
- 今後も新しい成果物責務が `aggregation` / `visualization` に押し込まれやすい

この選択をするなら、`#874` の CI failure は「直すべき失敗」ではなく「default step 追加を止めている正しい失敗」と扱う。

### B. `#874` に限って default 9 step 化を許容する

`hierarchical_layout_generation` を default pipeline の正式 step として認め、テストを 9 step 前提に更新する。

利点:

- `layouts` が default artifact contract になる
- `arguments[].x/y` を壊さず、複数 layout を viewer / report が選べる
- 表示 artifact を `visualization` から分離できる

欠点:

- status / rerun / docs / specs / mental model が 9 step へ変わる
- `layout_generation` の失敗を pipeline failure と見るか、display-only failure と見るかを決める必要がある
- 今回だけ 9 に直すと、次の step 追加時に同じ議論が再発する

この選択をするなら、テストは単に `8` を `9` に変えるだけでは弱い。少なくとも次を検証する形にする。

- default step ID の列挙に `hierarchical_layout_generation` が含まれる
- `hierarchical_layout_generation` は `hierarchical_aggregation` と `embedding` の後に来る
- `hierarchical_visualization` は `hierarchical_layout_generation` の後に来る
- `hierarchical_result.json.layouts` / `default_layout_id` が artifact contract として存在する
- rerun / reuse-from / skip 判定で layout step がどう扱われるか

### C. 今後も durable artifact なら default step 追加を許容する

今回だけでなく、今後も durable artifact と downstream consumer がある場合は default workflow の step 追加を許容する、という方針に変える。  
この場合、テストも `len(...) == N` ではなく、step graph の contract を見る形へ寄せる。

利点:

- `layout_generation` の次に `interpretation_artifacts` のような成果物責務が出ても、同じ基準で判断できる
- workflow が analysis / display / explanation artifact を扱う土台になる
- `aggregation` や `visualization` の多責務化を避けられる

欠点:

- default pipeline が徐々に長くなる可能性がある
- 非専門家向け Web UI に見せる progress / job list をどう整理するかが必要
- 「何でも step にする」方向へ倒れない gate が必要

この選択をするなら、step 追加 gate を明文化する必要がある。たとえば、

- 独立した durable artifact を出す
- downstream consumer が 2 つ以上ある、または現実的に見込める
- その step だけを再実行・検証したい
- 既存 step に入れると失敗モードや評価軸が混ざる
- ユーザ向け UI では step 数をそのまま露出しない

という条件を満たす場合だけ default step 追加を許容する。

### D. step graph は増やすが、ユーザ向け progress は固定カテゴリに畳む

技術的な workflow step は増やすが、Web UI / user-facing progress は `抽出 / 分析 / 表示生成` のような粗いカテゴリに畳む。  
これは C を採る場合の補助方針である。

利点:

- internal workflow は責務分離できる
- 非専門家ユーザには pipeline の複雑性を見せずに済む
- future step 追加への耐性が上がる

欠点:

- internal step と user-facing progress の mapping contract が必要
- status JSON / admin UI / report log の設計が一段増える

## 推奨

議論に出す暫定提案は **B か C** である。  
ただし、「とりあえず `8` を `9` に直す」は避ける。

自分の推奨は次。

1. `#874` の `layouts` は durable display artifact として価値があるので、default step 追加を **許容する方向** で検討する。
2. その代わり、テストを「step 数固定」から「step graph / artifact contract」へ更新する。
3. 同時に、今後の default step 追加 gate を軽く明文化する。
4. user-facing progress は internal step 数と分離する前提にする。

この判断を採るなら、`#874` の CI failure は「テストが古い」だけではなく、**テストが守っていた contract を意識的に変更する PR** として扱うべきである。PR 本文にも「default pipeline step set を拡張する設計判断」を明記した方がよい。

逆に、メンテナーが「default pipeline は今は増やさない」と判断するなら、`8 steps` テストは維持し、`#874` を default workflow 外へ戻すのが正しい。

## メンテナーに投げる文面案

```markdown
`#874` の CI failure について、単に `8` を `9` に直す前に設計判断を確認したいです。

今落ちている Pytest は `len(specs) == 8`, `len(plan) == 8`, `len(orchestrator.steps) == 8` という固定期待で、これは「default pipeline は 8 step」という暗黙の contract を守っているように見えます。

`#874` は `hierarchical_layout_generation` を追加して default workflow を 9 step にします。`arguments[].x/y` を壊さず `hierarchical_result.json.layouts` を追加する設計自体は良いと思っていますが、これは default pipeline の step set を拡張する判断でもあります。

決めたいのは次です。

- default pipeline は、`layouts` のような durable artifact を追加するために step 数が増えることを許容するか？

許容するなら、テストは単に `8 -> 9` に直すのではなく、以下を検証する形に変えるのがよいと思います。

- default step ID に `hierarchical_layout_generation` が含まれる
- `aggregation -> layout_generation -> visualization` の dependency が正しい
- `hierarchical_result.json.layouts` / `default_layout_id` が artifact contract として存在する
- rerun / reuse-from / skip で layout step がどう扱われるか

許容しないなら、今の `8 steps` テストは正しく落ちているので、`#874` は default workflow に step を足さない形へ戻すべきだと思います。

個人的には、`layouts` は durable display artifact として価値があるので default step 追加を許容する方向でよいと思います。ただし、その場合は「固定 8 step」から「step graph / artifact contract」を守るテストへ移る、という設計判断として扱いたいです。
```

## Open Questions

- default workflow の step set は public-ish contract と見るか、internal implementation detail と見るか。
- `hierarchical_result.json.layouts` は default output contract に含めるか。
- step 数が増えた時、Web UI の progress / status 表示も 9 step にするのか、internal step を user-facing category に畳むのか。
- `#867` reuse-from merge 後、new step の skip / seed semantics をどこまで必須 test にするか。

## Updates

- 2026-05-28: 初回作成。`#874` をメンテナーと議論するため、default 9 step 化 / optional display artifact / capability contract の選択肢と貼り付け用文面を整理した。
- 2026-05-28: ユーザ指摘を受け、論点を「`layout_generation` を optional にするか」ではなく「`8 steps` 固定テストを修正して default pipeline への step 追加を許容する方向へ進むか」に修正した。
