---
type: source
summary: "GitHub / CodeQL 公式ドキュメントから見た CodeQL の役割と GitHub code scanning での位置づけ"
sources:
  - https://codeql.github.com/docs/codeql-overview/about-codeql/
  - https://docs.github.com/en/code-security/concepts/code-scanning/codeql/about-code-scanning-with-codeql
---

GitHub / CodeQL の公式ドキュメントを要約した source。概念説明の一次参照として使う。実装固有の運用判断ではなく、CodeQL 一般の説明に限定する。[About CodeQL](https://codeql.github.com/docs/codeql-overview/about-codeql/) より

## Findings

- CodeQL は、コードをデータベース化してクエリで解析する GitHub の静的解析エンジンで、主に security checks と variant analysis に使われる。[About CodeQL](https://codeql.github.com/docs/codeql-overview/about-codeql/) より
- GitHub の code scanning では、`github/codeql-action` を含む workflow を通じて CodeQL CLI が実行され、脆弱性やセキュリティ品質上の問題を検出する。[About code scanning with CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/about-code-scanning-with-codeql) より
- CodeQL のスキャンは push / pull request / scheduled run / manual run などの GitHub Actions trigger に載せられる。[About code scanning with CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/about-code-scanning-with-codeql) より

## Open Questions

- `kouchou-ai` で CodeQL が実際にどの程度 alert を出しているかは、この source だけでは分からない

## Updates

- 2026-05-18: 初版作成
