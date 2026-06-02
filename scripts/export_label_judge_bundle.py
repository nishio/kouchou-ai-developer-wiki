"""Export a human/Claude-readable label-judge bundle from analysis-core outputs.

Usage:
  python3 scripts/export_label_judge_bundle.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "work" / "kouchou-ai" / "packages" / "analysis-core" / "outputs"
DEST = ROOT / "wiki" / "sources" / "label-refinement-judge-bundle-2026-05-25.md"


@dataclass(frozen=True)
class Candidate:
    key: str
    label: str
    relative_dir: str
    note: str


CANDIDATES = [
    Candidate(
        key="none",
        label="hierarchical [8,40] baseline (`none`)",
        relative_dir="llm_grouping_sample_comments_400_hierarchical_8_40_refine_none",
        note="`merge_labelling` の結果をそのまま使う baseline。",
    ),
    Candidate(
        key="setwise",
        label="setwise_refine",
        relative_dir="llm_grouping_sample_comments_400_hierarchical_8_40_refine_setwise",
        note="sibling 全体を見て代表性と重複抑制を両立させる最初の refinement。",
    ),
    Candidate(
        key="contrast",
        label="contrast",
        relative_dir="llm_grouping_sample_comments_400_hierarchical_8_40_refine_contrast",
        note="sibling 差分を前半に出し、短くしつつ意味差を残す prompt variant。",
    ),
    Candidate(
        key="balanced",
        label="balanced",
        relative_dir="llm_grouping_sample_comments_400_hierarchical_8_40_refine_balanced",
        note="短さと読みやすさを優先し、一覧 heading として揃えやすい prompt variant。",
    ),
]


def top_level_clusters(result: dict) -> list[dict]:
    return [cluster for cluster in result["clusters"] if cluster["level"] == 1]


def cluster_examples(arguments: list[dict], cluster_id: str, limit: int = 3) -> list[str]:
    picked = []
    for argument in arguments:
        cluster_ids = argument.get("cluster_ids") or []
        if len(cluster_ids) > 1 and cluster_ids[1] == cluster_id:
            picked.append(argument["argument"].strip())
            if len(picked) >= limit:
                break
    return picked


def load_candidate(candidate: Candidate) -> dict:
    result_path = OUTPUTS / candidate.relative_dir / "hierarchical_result.json"
    return json.loads(result_path.read_text(encoding="utf-8"))


def build_markdown() -> str:
    lines: list[str] = [
        "---",
        "type: source",
        'summary: "Claude Code や人間が同じ材料で top-level label set を比較できるよう、`[8,40]` の label refinement 候補 4 本を同一フォーマットで並べた judge bundle"',
        "sources:",
        "  - source-code.md",
        "  - llm-grouping-experiment-output-2026-05-25.md",
        "---",
        "",
        "このページは、`[8,40]` の top-level label refinement 候補を **Claude Code judge** と **人間 judge** が同じ材料で比較できるように整形した bundle である。現状の OpenAI judge は同系統 LLM による self-evaluation バイアスを疑うべきなので、まず判断対象を固定した上で別 judge を差し込める形にした。[[llm-grouping-experiment-output-2026-05-25]]より",
        "",
        "## Judge Instructions",
        "",
        "候補を比べる時は、少なくとも次の 3 軸を分けて見る。",
        "",
        "1. 個別クラスタの代表性",
        "2. ラベル集合全体の読みやすさ",
        "3. 隣接ラベルとの区別のしやすさ",
        "",
        "OpenAI judge の cluster 平均点と direct judge はこの 3 軸を混ぜると winner が割れた。したがって、この bundle でも **1 cluster ずつの妥当性** と **一覧で並べた時の scanability** を意図的に分けて判断する必要がある。[[llm-grouping-experiment-output-2026-05-25]]より",
        "",
        "## Common Setup",
        "",
        "- 入力データ: `apps/admin/public/sample_comments.csv` 由来の日本語コメント 400 件",
        "- 抽出 argument 数: 422",
        "- clustering 構造: `cluster_nums = [8, 40]` を固定",
        "- 差し替えているのは `merge_labelling` 後の top-level label / description だけ",
        "- 代表意見例は各 top-level cluster に属する argument の先頭 3 件",
        "",
    ]

    for candidate in CANDIDATES:
        result = load_candidate(candidate)
        top_clusters = top_level_clusters(result)
        lines.extend(
            [
                f"## {candidate.label}",
                "",
                candidate.note,
                "",
                f"- output dir: `{candidate.relative_dir}`",
                f"- top-level cluster count: {len(top_clusters)}",
                "",
            ]
        )
        for index, cluster in enumerate(top_clusters, start=1):
            examples = cluster_examples(result["arguments"], cluster["id"])
            lines.extend(
                [
                    f"### {index}. {cluster['label']}",
                    "",
                    f"- size: `{cluster['value']}`",
                    f"- description: {cluster['takeaway'].strip()}",
                    "- representative arguments:",
                ]
            )
            for example in examples:
                lines.append(f"  - {example}")
            lines.append("")

    lines.extend(
        [
            "## Open Questions",
            "",
            "- OpenAI judge と Claude judge と人間 judge で、どの候補の順位が一致するか",
            "- cluster 単位の代表性と、一覧 UI としての読みやすさのどちらを product で優先すべきか",
            "- この bundle の代表意見例 3 件で十分か、それとも各 cluster 5 件以上を見せるべきか",
            "",
            "## Updates",
            "",
            "- 2026-05-25: 初版作成。`none / setwise / contrast / balanced` の 4 候補を同一フォーマットで並べ、Claude Code judge と人間 judge がそのまま使える比較 bundle を追加",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    DEST.write_text(build_markdown(), encoding="utf-8")
    print(f"Wrote {DEST}")


if __name__ == "__main__":
    main()
