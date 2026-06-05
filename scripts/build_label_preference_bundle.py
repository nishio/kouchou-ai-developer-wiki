"""Build blind A/B label preference bundles from a raw experiment corpus.

The generated bundles are for human review. They intentionally do not show
which labelling process produced candidate A or B.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXPERIMENT_ROOT = (
    ROOT
    / "raw"
    / "experiments"
    / "2026-06-02-llm-grouping-400-tree-label-corpus"
)
DEFAULT_CANDIDATES = (
    "labelling:hierarchical_8_40_refine_none",
    "labelling:hierarchical_8_40_refine_setwise",
)
DEFAULT_PRESENTATION_CONTEXTS = (
    "label_only",
    "sibling_label_set",
    "label_with_representatives",
)
REASON_TAGS = (
    "covers_more",
    "distinguishes_siblings",
    "more_concise",
    "less_unsupported",
    "better_heading",
)

HTML_INTERACTION_JS = r"""
const forms = Array.from(document.querySelectorAll(".response"));
const output = document.getElementById("answers-jsonl");
const stats = document.getElementById("answer-stats");
const evaluator = document.getElementById("evaluator-id");
const copyButton = document.getElementById("copy-answers");

function selectedValue(form, field) {
  const selected = form.querySelector(`input[name="${field}-${form.dataset.preferenceId}"]:checked`);
  return selected ? selected.value : "";
}

function selectedTags(form) {
  return Array.from(
    form.querySelectorAll(`input[name="reason-${form.dataset.preferenceId}"]:checked`)
  ).map((input) => input.value);
}

function updateOutput() {
  const rows = [];
  let touched = 0;
  let incomplete = 0;
  const evaluatorId = evaluator.value.trim();

  for (const form of forms) {
    const winner = selectedValue(form, "winner");
    const confidenceText = selectedValue(form, "confidence");
    const reasonTags = selectedTags(form);
    const freeText = form.querySelector("textarea").value.trim();
    const hasAnyAnswer = winner || confidenceText || reasonTags.length || freeText;
    const isComplete = Boolean(winner && confidenceText);

    form.classList.toggle("is-complete", isComplete);
    form.classList.toggle("is-incomplete", Boolean(hasAnyAnswer && !isComplete));

    if (hasAnyAnswer) {
      touched += 1;
    }
    if (hasAnyAnswer && !isComplete) {
      incomplete += 1;
    }
    if (!isComplete) {
      continue;
    }

    const row = {
      schema_version: "kouchou-ai.human-preference.v1",
      preference_id: form.dataset.preferenceId,
      comparison_id: form.dataset.comparisonId,
      presentation_context: form.dataset.presentationContext,
      cluster_id: form.dataset.clusterId,
      winner,
      confidence: Number(confidenceText),
      reason_tags: reasonTags,
      free_text: freeText || null,
    };
    if (evaluatorId) {
      row.evaluator_id = evaluatorId;
    }
    rows.push(row);
  }

  output.value = rows.map((row) => JSON.stringify(row)).join("\n");
  if (output.value) {
    output.value += "\n";
  }
  stats.textContent = `${rows.length}/${forms.length} complete, ${incomplete} incomplete, ${touched} touched`;
}

document.addEventListener("input", updateOutput);
copyButton.addEventListener("click", async () => {
  output.select();
  try {
    await navigator.clipboard.writeText(output.value);
    copyButton.textContent = "Copied";
    setTimeout(() => {
      copyButton.textContent = "Copy JSONL";
    }, 1200);
  } catch {
    document.execCommand("copy");
  }
});
updateOutput();
"""


@dataclass(frozen=True)
class LabellingRun:
    labelling_run_id: str
    tree_run_id: str
    process: str
    params: dict[str, Any]
    artifact_path: Path


@dataclass(frozen=True)
class LabelRow:
    cluster_id: str
    label: str
    description: str
    value: str
    parent: str


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            f.write("\n")


def load_labelling_runs(experiment_root: Path) -> dict[str, LabellingRun]:
    runs: dict[str, LabellingRun] = {}
    for row in read_jsonl(experiment_root / "labelling_runs.jsonl"):
        runs[row["labelling_run_id"]] = LabellingRun(
            labelling_run_id=row["labelling_run_id"],
            tree_run_id=row["tree_run_id"],
            process=row["process"],
            params=row.get("params", {}),
            artifact_path=experiment_root / row["artifact_path"],
        )
    return runs


def load_top_labels(path: Path) -> dict[str, LabelRow]:
    labels: dict[str, LabelRow] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("level") != "1":
                continue
            cluster_id = row["id"]
            labels[cluster_id] = LabelRow(
                cluster_id=cluster_id,
                label=row.get("label", "").strip(),
                description=row.get("description", "").strip(),
                value=row.get("value", "").strip(),
                parent=row.get("parent", "").strip(),
            )
    return labels


def load_examples(
    experiment_root: Path, tree_run_key: str, limit: int
) -> dict[str, list[str]]:
    path = experiment_root / "artifacts" / "runs" / tree_run_key / "hierarchical_clusters.csv"
    examples: dict[str, list[str]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cluster_id = row.get("cluster-level-1-id")
            argument = row.get("argument", "").strip()
            if not cluster_id or not argument:
                continue
            bucket = examples.setdefault(cluster_id, [])
            if len(bucket) < limit:
                bucket.append(argument)
    return examples


def stable_bool(seed: int, *parts: str) -> bool:
    key = "|".join(str(part) for part in parts)
    digest = hashlib.sha256(f"{seed}:{key}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 2 == 0


def build_comparisons(
    experiment_root: Path,
    tree_run_id: str,
    candidate_ids: tuple[str, str],
    presentation_contexts: tuple[str, ...],
    seed: int,
    example_limit: int,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, LabelRow]], dict[str, list[str]]]:
    labelling_runs = load_labelling_runs(experiment_root)
    missing = [run_id for run_id in candidate_ids if run_id not in labelling_runs]
    if missing:
        raise SystemExit(f"Missing labelling_run_id(s): {', '.join(missing)}")

    candidates = [labelling_runs[run_id] for run_id in candidate_ids]
    for candidate in candidates:
        if candidate.tree_run_id != tree_run_id:
            raise SystemExit(
                f"{candidate.labelling_run_id} uses {candidate.tree_run_id}, "
                f"expected {tree_run_id}"
            )

    labels_by_run = {
        candidate.labelling_run_id: load_top_labels(candidate.artifact_path)
        for candidate in candidates
    }
    cluster_ids = sorted(set.intersection(*(set(v) for v in labels_by_run.values())))
    tree_run_key = tree_run_id.removeprefix("tree:")
    examples_by_cluster = load_examples(experiment_root, tree_run_key, example_limit)

    rows: list[dict[str, Any]] = []
    for presentation_context in presentation_contexts:
        for index, cluster_id in enumerate(cluster_ids, start=1):
            swap = stable_bool(seed, presentation_context, cluster_id, *candidate_ids)
            a_run_id, b_run_id = (candidate_ids[1], candidate_ids[0]) if swap else candidate_ids
            row = {
                "schema_version": "kouchou-ai.human-preference.v1",
                "experiment_id": json.loads(
                    (experiment_root / "manifest.json").read_text(encoding="utf-8")
                )["experiment_id"],
                "preference_id": f"pref-{presentation_context}-{index:02d}",
                "comparison_id": f"cmp-{tree_run_key}-{presentation_context}-{index:02d}",
                "status": "pending",
                "tree_run_id": tree_run_id,
                "cluster_id": cluster_id,
                "presentation_context": presentation_context,
                "ui_surface": None,
                "algorithm_origin_visible": False,
                "candidate_a_labelling_run_id": a_run_id,
                "candidate_b_labelling_run_id": b_run_id,
                "candidate_a_display_position": "left",
                "candidate_b_display_position": "right",
                "factor_under_test": "labelling_process",
                "fixed_inputs": [
                    "dataset",
                    "extracted_arguments",
                    "embeddings",
                    "tree_run",
                    "presentation_context",
                ],
                "changed_inputs": ["labelling_process"],
                "winner": None,
                "confidence": None,
                "reason_tags": [],
                "free_text": None,
                "allowed_winners": ["a", "b", "tie", "unsure"],
                "allowed_reason_tags": list(REASON_TAGS),
                "example_arguments_source": (
                    "first_rows_from_hierarchical_clusters_csv; "
                    "not a calibrated representative artifact"
                ),
            }
            rows.append(row)
    return rows, labels_by_run, examples_by_cluster


def label_for(
    labels_by_run: dict[str, dict[str, LabelRow]], run_id: str, cluster_id: str
) -> LabelRow:
    return labels_by_run[run_id][cluster_id]


def format_candidate_md(
    title: str,
    label: LabelRow,
    presentation_context: str,
    labels_by_run: dict[str, dict[str, LabelRow]],
    run_id: str,
    examples: list[str],
) -> list[str]:
    lines = [f"#### Candidate {title}", "", f"**{label.label}**", ""]
    if presentation_context == "label_only":
        return lines
    if presentation_context == "sibling_label_set":
        lines.append("Sibling label set:")
        for sibling in labels_by_run[run_id].values():
            marker = " (focus)" if sibling.cluster_id == label.cluster_id else ""
            lines.append(f"- {sibling.cluster_id}{marker}: {sibling.label}")
        lines.append("")
        return lines
    if presentation_context == "label_with_representatives":
        lines.extend([f"Description: {label.description}", "", "Example arguments:"])
        for example in examples:
            lines.append(f"- {example}")
        lines.append("")
        return lines
    raise ValueError(f"Unsupported presentation_context: {presentation_context}")


def build_markdown(
    rows: list[dict[str, Any]],
    labels_by_run: dict[str, dict[str, LabelRow]],
    examples_by_cluster: dict[str, list[str]],
) -> str:
    lines = [
        "# Blind Label Preference A/B Bundle",
        "",
        "Evaluator instructions:",
        "",
        "- Do not try to infer which algorithm or prompt produced A or B.",
        "- Choose `A`, `B`, `tie`, or `unsure`.",
        "- Confidence: `1` low, `2` medium, `3` high.",
        "- Reason tags are optional: "
        + ", ".join(f"`{tag}`" for tag in REASON_TAGS),
        "",
        "The bundle does not show algorithm/process origins. "
        "Origins are stored only in JSONL metadata for later analysis.",
        "",
    ]
    for row in rows:
        a_label = label_for(labels_by_run, row["candidate_a_labelling_run_id"], row["cluster_id"])
        b_label = label_for(labels_by_run, row["candidate_b_labelling_run_id"], row["cluster_id"])
        examples = examples_by_cluster.get(row["cluster_id"], [])
        lines.extend(
            [
                f"## {row['comparison_id']}",
                "",
                f"- presentation_context: `{row['presentation_context']}`",
                f"- cluster_id: `{row['cluster_id']}`",
                f"- cluster_size: `{a_label.value}`",
                "",
            ]
        )
        lines.extend(
            format_candidate_md(
                "A",
                a_label,
                row["presentation_context"],
                labels_by_run,
                row["candidate_a_labelling_run_id"],
                examples,
            )
        )
        lines.extend(
            format_candidate_md(
                "B",
                b_label,
                row["presentation_context"],
                labels_by_run,
                row["candidate_b_labelling_run_id"],
                examples,
            )
        )
        lines.extend(
            [
                "Response:",
                "",
                "- winner: [ ] A  [ ] B  [ ] tie  [ ] unsure",
                "- confidence (1 低 / 2 中 / 3 高): [ ] 1  [ ] 2  [ ] 3",
                "- reason_tags:",
                "  - [ ] covers_more",
                "  - [ ] distinguishes_siblings",
                "  - [ ] more_concise",
                "  - [ ] less_unsupported",
                "  - [ ] better_heading",
                "- free_text:",
                "",
            ]
        )
    return "\n".join(lines)


def html_candidate_block(
    title: str,
    label: LabelRow,
    presentation_context: str,
    labels_by_run: dict[str, dict[str, LabelRow]],
    run_id: str,
    examples: list[str],
) -> str:
    parts = [
        f'<section class="candidate"><h4>Candidate {title}</h4>',
        f"<h5>{html.escape(label.label)}</h5>",
    ]
    if presentation_context == "sibling_label_set":
        parts.append("<ul>")
        for sibling in labels_by_run[run_id].values():
            focus = " <strong>(focus)</strong>" if sibling.cluster_id == label.cluster_id else ""
            parts.append(
                "<li>"
                + html.escape(sibling.cluster_id)
                + focus
                + ": "
                + html.escape(sibling.label)
                + "</li>"
            )
        parts.append("</ul>")
    elif presentation_context == "label_with_representatives":
        parts.append(f"<p>{html.escape(label.description)}</p>")
        parts.append("<ul>")
        for example in examples:
            parts.append(f"<li>{html.escape(example)}</li>")
        parts.append("</ul>")
    parts.append("</section>")
    return "\n".join(parts)


def build_html(
    rows: list[dict[str, Any]],
    labels_by_run: dict[str, dict[str, LabelRow]],
    examples_by_cluster: dict[str, list[str]],
) -> str:
    sections = []
    for row in rows:
        a_label = label_for(labels_by_run, row["candidate_a_labelling_run_id"], row["cluster_id"])
        b_label = label_for(labels_by_run, row["candidate_b_labelling_run_id"], row["cluster_id"])
        examples = examples_by_cluster.get(row["cluster_id"], [])
        preference_id = html.escape(row["preference_id"], quote=True)
        comparison_id = html.escape(row["comparison_id"], quote=True)
        presentation_context = html.escape(row["presentation_context"], quote=True)
        cluster_id = html.escape(row["cluster_id"], quote=True)
        winner_name = f"winner-{preference_id}"
        confidence_name = f"confidence-{preference_id}"
        reason_name = f"reason-{preference_id}"
        sections.append(
            "\n".join(
                [
                    '<article class="comparison">',
                    f"<h2>{html.escape(row['comparison_id'])}</h2>",
                    '<div class="meta">'
                    f"presentation_context: <code>{html.escape(row['presentation_context'])}</code> "
                    f"cluster_id: <code>{html.escape(row['cluster_id'])}</code> "
                    f"cluster_size: <code>{html.escape(a_label.value)}</code>"
                    "</div>",
                    '<div class="candidates">',
                    html_candidate_block(
                        "A",
                        a_label,
                        row["presentation_context"],
                        labels_by_run,
                        row["candidate_a_labelling_run_id"],
                        examples,
                    ),
                    html_candidate_block(
                        "B",
                        b_label,
                        row["presentation_context"],
                        labels_by_run,
                        row["candidate_b_labelling_run_id"],
                        examples,
                    ),
                    "</div>",
                    (
                        '<fieldset class="response" '
                        f'data-preference-id="{preference_id}" '
                        f'data-comparison-id="{comparison_id}" '
                        f'data-presentation-context="{presentation_context}" '
                        f'data-cluster-id="{cluster_id}">'
                    ),
                    "<legend>Response</legend>",
                    '<div class="control-row">',
                    "<span>winner</span>",
                    f'<label><input type="radio" name="{winner_name}" value="a"> A</label>',
                    f'<label><input type="radio" name="{winner_name}" value="b"> B</label>',
                    f'<label><input type="radio" name="{winner_name}" value="tie"> tie</label>',
                    f'<label><input type="radio" name="{winner_name}" value="unsure"> unsure</label>',
                    "</div>",
                    '<div class="control-row">',
                    "<span>confidence (1 低 / 2 中 / 3 高)</span>",
                    f'<label><input type="radio" name="{confidence_name}" value="1"> 1 低</label>',
                    f'<label><input type="radio" name="{confidence_name}" value="2"> 2 中</label>',
                    f'<label><input type="radio" name="{confidence_name}" value="3"> 3 高</label>',
                    "</div>",
                    '<div class="control-row reason-row">',
                    "<span>reason_tags</span>",
                    *[
                        f'<label><input type="checkbox" name="{reason_name}" value="{tag}"> {tag}</label>'
                        for tag in REASON_TAGS
                    ],
                    "</div>",
                    '<label class="free-text">free_text<textarea rows="2"></textarea></label>',
                    "</fieldset>",
                    "</article>",
                ]
            )
        )
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            "<title>Blind Label Preference A/B Bundle</title>",
            "<style>",
            "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.5;margin:32px;}",
            ".output-panel{position:sticky;top:0;background:#fff;border-bottom:1px solid #bbb;padding:12px 0 16px;z-index:1;}",
            ".output-controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:8px 0;}",
            ".output-controls input{padding:6px 8px;border:1px solid #aaa;border-radius:4px;}",
            "button{padding:7px 10px;border:1px solid #777;border-radius:4px;background:#f2f2f2;cursor:pointer;}",
            "#answer-stats{color:#444;}",
            "#answers-jsonl{box-sizing:border-box;width:100%;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;}",
            ".comparison{border-top:1px solid #ccc;padding:24px 0;}",
            ".meta{color:#555;margin-bottom:12px;}",
            ".candidates{display:grid;grid-template-columns:1fr 1fr;gap:20px;}",
            ".candidate{border:1px solid #ddd;border-radius:6px;padding:14px;}",
            ".candidate h4{margin:0 0 8px}.candidate h5{font-size:1rem;margin:0 0 12px;}",
            ".response{background:#f6f6f6;border:1px solid #ddd;padding:12px;margin-top:12px;}",
            ".response.is-complete{border-color:#2b7a4b;background:#f1faf5;}",
            ".response.is-incomplete{border-color:#9b6a00;background:#fff9ea;}",
            ".control-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:8px 0;}",
            ".control-row span{font-weight:600;min-width:96px;}",
            ".free-text{display:block;margin-top:10px;font-weight:600;}",
            ".free-text textarea{box-sizing:border-box;display:block;width:100%;margin-top:4px;font:inherit;font-weight:400;}",
            "code{background:#eee;padding:1px 4px;border-radius:3px;}",
            "@media (max-width: 760px){body{margin:16px}.candidates{grid-template-columns:1fr}.output-panel{position:static}}",
            "</style>",
            "</head>",
            "<body>",
            "<h1>Blind Label Preference A/B Bundle</h1>",
            "<p>Algorithm/process origins are intentionally hidden from this review bundle.</p>",
            '<section class="output-panel">',
            "<h2>Collected Answers JSONL</h2>",
            "<p>Only rows with both winner and confidence selected are exported here.</p>",
            '<div class="output-controls">',
            '<label>evaluator_id <input id="evaluator-id" type="text" autocomplete="off"></label>',
            '<button id="copy-answers" type="button">Copy JSONL</button>',
            '<span id="answer-stats"></span>',
            "</div>",
            '<textarea id="answers-jsonl" rows="8" spellcheck="false"></textarea>',
            "</section>",
            *sections,
            "<script>",
            HTML_INTERACTION_JS,
            "</script>",
            "</body></html>",
        ]
    )


def update_manifest(experiment_root: Path, question_count: int) -> None:
    manifest_path = experiment_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest.setdefault("records", {})
    records["human_preference_questions"] = question_count
    records.setdefault("human_preferences", 0)
    artifact_roots = manifest.setdefault("artifact_roots", {})
    artifact_roots.setdefault("preferences", "bundles/")
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-root", type=Path, default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--tree-run-id", default="tree:hierarchical_8_40")
    parser.add_argument("--candidate", action="append", dest="candidates")
    parser.add_argument("--presentation-context", action="append", dest="contexts")
    parser.add_argument("--seed", type=int, default=20260603)
    parser.add_argument("--example-limit", type=int, default=3)
    parser.add_argument("--output-stem", default="label_preference_ab")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = args.experiment_root.resolve()
    candidate_ids = tuple(args.candidates or DEFAULT_CANDIDATES)
    if len(candidate_ids) != 2:
        raise SystemExit("Exactly two --candidate values are required")
    contexts = tuple(args.contexts or DEFAULT_PRESENTATION_CONTEXTS)
    unsupported = set(contexts) - set(DEFAULT_PRESENTATION_CONTEXTS)
    if unsupported:
        raise SystemExit(f"Unsupported presentation_context(s): {sorted(unsupported)}")

    rows, labels_by_run, examples_by_cluster = build_comparisons(
        experiment_root,
        args.tree_run_id,
        candidate_ids,  # type: ignore[arg-type]
        contexts,
        args.seed,
        args.example_limit,
    )

    bundles_dir = experiment_root / "bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)

    questions_path = experiment_root / "human_preference_questions.jsonl"
    preferences_path = experiment_root / "human_preferences.jsonl"
    schema_path = experiment_root / "human_preferences.schema.json"
    md_path = bundles_dir / f"{args.output_stem}.md"
    html_path = bundles_dir / f"{args.output_stem}.html"

    write_jsonl(questions_path, rows)
    if not preferences_path.exists():
        preferences_path.write_text("", encoding="utf-8")
    schema_path.write_text(
        json.dumps(
            {
                "schema_version": "kouchou-ai.human-preference.v1",
                "required_fields": [
                    "preference_id",
                    "comparison_id",
                    "winner",
                    "confidence",
                    "reason_tags",
                ],
                "optional_fields": [
                    "schema_version",
                    "presentation_context",
                    "cluster_id",
                    "free_text",
                    "evaluator_id",
                ],
                "allowed_winners": ["a", "b", "tie", "unsure"],
                "allowed_reason_tags": list(REASON_TAGS),
                "presentation_contexts": list(DEFAULT_PRESENTATION_CONTEXTS),
                "notes": [
                    "human_preference_questions.jsonl stores hidden origins and display metadata.",
                    "human_preferences.jsonl stores collected answers and may be joined by preference_id.",
                    "The HTML bundle emits completed answers as JSONL in its textarea.",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, labels_by_run, examples_by_cluster), encoding="utf-8")
    html_path.write_text(build_html(rows, labels_by_run, examples_by_cluster), encoding="utf-8")
    update_manifest(experiment_root, len(rows))

    print(f"Wrote {questions_path.relative_to(ROOT)} ({len(rows)} questions)")
    print(f"Wrote {preferences_path.relative_to(ROOT)}")
    print(f"Wrote {schema_path.relative_to(ROOT)}")
    print(f"Wrote {md_path.relative_to(ROOT)}")
    print(f"Wrote {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
