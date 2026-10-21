---
title: "analysis-core の MIT 表記の経緯 2026-10-12"
type: source
summary: "大木さんの2026-10-11の質問を起点に、analysis-coreのMIT表記が2026-01-19の雛形作成で入り、既存コード移植・PR #746・PyPI配布へ継承された経緯を確認"
sources:
  - slack-logs-repository.md
  - meeting-minutes.md
  - source-code.md
  - ユーザー（西尾）の2026-10-12の明示指示
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/970
  - https://github.com/digitaldemocracy2030/kouchou-ai/commit/48cf3c1d67c1936c88fc437700d2b2f1c587a3b9
  - https://github.com/digitaldemocracy2030/kouchou-ai/pull/746
  - https://pypi.org/project/kouchou-ai-analysis-core/0.1.2/
---

## 鮮度と範囲

- 最終読解: 2026-10-12 JST。Slack cloneをfetch/pullし `2704083d45697d2aff6f1441a7718cf584a8c50e` を確認。mirror同期は2026-10-12 06:43 JST（UTC 2026-10-11T21:43:57）、実際の窓は75日。`#2_開発_広聴ai`（`C08F7JZPD63`）の直近発言と、rawの2025-12〜2026-01のパッケージ化関連発言を読解。raw全channelのAGPL / MIT License / MITライセンス / ライセンス変更も補助検索した。
- 選択したSlack発言4件と同期metadataを `raw/analysis-core-license-2026-10-12/` に固定。全channelや全threadの完全snapshotではない。発言者はmirror/users.jsonで大木真吾（truego）・西尾さんを解決。
- 本体はfetch/pull後のmain `c297bc97bb2bbce42964a90d7501c2d3592aeaf0`。導入コミット・移植差分・当時計画書、PR [#746](https://github.com/digitaldemocracy2030/kouchou-ai/issues/746)本文/コメント/review/inline comments、[#831](https://github.com/digitaldemocracy2030/kouchou-ai/issues/831)、open PR全10件の一覧、license / ライセンス / AGPLのissue/PR検索を確認。
- 議事録は2026-10-12にtxt再取得、先頭見出し `2026/07/27`、7744行。1月19日周辺とライセンス語の検索結果を確認。html再取得はtimeoutのため、今回の根拠には使用していない。[[meeting-minutes]]より。
- PyPIはJSON APIと0.1.0 / 0.1.2のwheel内METADATAを直接確認。外部配布の現状は2026-10-12時点。

## 質問

大木さんは2026-10-11 16:54 JST、広聴AI全体のAGPL-3.0とanalysis-coreのREADME / pyproject.tomlのMIT表記の違いを挙げ、独立したMITライセンスのライブラリとして提供する意図なのかを西尾さんへ質問した。[Slack原文](https://dd2030.slack.com/archives/C08F7JZPD63/p1791705288377159)。同期時点のこのmessageには返信情報がなく、snapshot内に回答は見つからなかった。Slackの同期後の状態は未確認。[[slack-logs-repository]]より。

## 時系列

1. **2025-12-27**: 西尾さんが[リファクタリング計画gist](https://gist.github.com/nishio/0a1812750627620ff6ede948f13c993b)をSlackに共有。計画は分析処理をPyPI配布し、他のBIツールから再利用できること、CLIとライブラリAPIの提供を目的にする。取得した計画文にはMIT / AGPL / ライセンス変更の記述を検出しなかった。
2. **2026-01-19 12:16 JST**: [48cf3c1](https://github.com/digitaldemocracy2030/kouchou-ai/commit/48cf3c1d67c1936c88fc437700d2b2f1c587a3b9)でパッケージ雛形を作成。README末尾の `MIT License`、pyproject.tomlの `license = { text = "MIT" }`、MIT classifierが同時に入った。authorはNISHIO Hirokazu、commitにはClaude Code生成・Claude Opus 4.5共同著者の記録がある。commit説明とLOG.mdは構造作成・後続の既存コード移植を述べ、MITを選ぶ理由は説明していない。
3. **同日12:29 JST**: [01df36a](https://github.com/digitaldemocracy2030/kouchou-ai/commit/01df36a9b16389ff115f5c5f4eb1cf87c62054e5)で旧pipelineのcore utilities・services・8 stepsを移植。例として旧 `apps/api/broadlistening/pipeline/steps/embedding.py` と新packageの同名ファイルの差分は、`request_to_embed` のimport先の変更だけだった。独立パッケージ化は既存実装の移植を含む。
4. **同日15:50 JST**: PyPI 0.1.0をupload。15:51のSlackで西尾さんが公開を報告。1月19日の議事録にもCLI / import利用、pipは別repoではないこと、0.1.0がとりあえずできた段階であることが記録される。MIT変更の決定はその箇所にはない。[[meeting-minutes]]より。
5. **2026-01-23 13:02 JST**: [PR #746](https://github.com/digitaldemocracy2030/kouchou-ai/pull/746)をmerge。本文の目的は安定コアと実験的拡張の分離、CLI/PyPI再利用。[西尾さんのコメント](https://github.com/digitaldemocracy2030/kouchou-ai/pull/746#issuecomment-3788078753)は大木さんからSlackでself-mergeの了承を得たと述べる。ただし、これはPR全体のmergeに関する記録で、MIT化への合意を示す記録ではない。取得したPR本文・コメントにMIT変更の説明はなく、reviews / inline commentsは空だった。
6. **2026-05-18〜19 JST**: [PR #831](https://github.com/digitaldemocracy2030/kouchou-ai/pull/831)で配布自動化、0.1.2公開。MIT表記の導入はこの時ではなく1月。[[pypi-release-observation-2026-05-19]]より。
7. **2026-10-12確認**: root LICENSEはAGPL v3。packageのREADME / pyproject.tomlのMIT表記は残っている。これらのlicense関連行を変更した履歴は初回作成以外に検出せず、package専用LICENSEは存在しない。PyPI最新は0.1.2で、0.1.0と0.1.2の両wheelに `License: MIT` とMIT classifierがある。両wheelにLICENSE / COPYING / NOTICEという名前のファイルはない。[PyPI公開表示](https://pypi.org/project/kouchou-ai-analysis-core/0.1.2/)でもMITと表示される。

## Open Questions

- MIT表記が人間の明示指示に基づくものか、雛形生成時の誤記か。commitのAI共同著者記録だけでは原因を確定できない。
- 別ライセンス化に関する未確認のDM・会話・権利確認資料があるか。公開PRと取得できたSlack/議事録で未発見という範囲に留まる。
- 今後どのライセンス表記へ統一するか、既存PyPI配布への説明をどうするか。

## Updates

- 2026-10-12: 初回調査。判断と返答の材料は [[analysis-core-license-intent-2026-10-12]] に分離。コード・GitHub issue/PR・Slackは変更していない。

## Updates — 2026-10-12 AGPLが正しいとの確認と修正PR

- 上記調査後、西尾さんから「AGPLが正しい、修正して」と明示指示を受領。独立パッケージのMIT表記を誤記として訂正する方針が確定した。上のOpen Questionsにある今後のライセンス方針は、この指示により解決。表記が入った際のAI/人間の具体的な指示履歴は引き続き未確認。
- 本体main `c297bc9` を起点に `fix/analysis-core-agpl-license` / commit `5513855` / [PR #970](https://github.com/digitaldemocracy2030/kouchou-ai/pull/970)を作成。README、pyproject.tomlのlicense/classifierをAGPL-3.0に訂正し、rootと同一のLICENSE本文をpackageに追加。READMEに旧PyPI 0.1.0 / 0.1.2のMIT表記の訂正を明記し、配布チェックリストにも同梱確認を追加した。
- `python -m build`でsdistを生成し、そのsdistからwheelをビルド（hatchling 1.32.4）。両配布物のAGPL metadata/classifier、LICENSE全文のrootとのバイト一致、`twine check`成功を確認。Python実装変更はなく、ローカルで解析処理・実APIテストは行っていない。
- 状態はPR作成済み・未merge。公開済みPyPIファイルは未更新で、新版リリースが残る。Slack返信は未実施。

## Updates — 2026-10-12 利用者向け解説とCLI出力へ修正範囲を拡張

- 西尾さんの追加指示で、[PR #970](https://github.com/digitaldemocracy2030/kouchou-ai/pull/970)にcommit `d09976e`を追加。`docs/user-guide/license.md`と各入口へのリンク、CLI出力HTMLのライセンス全文・表示ソースZIP自動同梱を実装した。先の「Python実装変更はない」は `5513855` 時点の説明で、今回から生成処理の変更を含む。
- HTML生成16テスト、ZIPから隔離Pythonで同一HTMLを再生成、ローカル改造ソース保存、wheel単体の生成、sdist/wheelライセンス一致、twine・Ruff・docs strict buildを確認。案内を利用者が手で作らずに済む方針と制限は [[agpl-output-and-plugin-boundaries-2026-10-12]]より。
- 未merge・PyPI未更新。リリースチェックリストではライセンス検証をタグpushより前へ移した。
