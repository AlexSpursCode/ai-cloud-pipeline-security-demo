from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

from output import write_json, write_markdown
from parser import flatten_content, load_yaml_file
from rules import CONTROL_KEYWORDS, CONTROL_METADATA
from scoring import calculate_score, determine_gate


ROOT_DIR = Path(__file__).resolve().parents[1]
PIPELINE_DIR = ROOT_DIR / "pipelines"
REPORT_DIR = ROOT_DIR / "reports" / "generated"
INCLUDE_VULNERABLE = os.getenv("RISK_MAPPER_INCLUDE_VULNERABLE", "false").lower() == "true"


def detect_missing_controls(content: str) -> list[dict]:
    findings: list[dict] = []

    for control, keywords in CONTROL_KEYWORDS.items():
        present = any(keyword in content for keyword in keywords)
        if present:
            continue
        metadata = CONTROL_METADATA[control]
        findings.append(
            {
                "control": control,
                "title": metadata["title"],
                "severity": metadata["severity"],
                "owasp_llm": metadata["owasp_llm"],
                "cloud_controls": metadata["cloud"],
                "supply_chain_controls": metadata["supply_chain"],
                "summary": f"Missing {metadata['title'].lower()} control in pipeline definition.",
            }
        )

    return findings


def analyze_pipeline(path: Path) -> dict:
    data = load_yaml_file(path)
    flattened = flatten_content(data)
    findings = detect_missing_controls(flattened)
    score = calculate_score(findings)
    enforced = INCLUDE_VULNERABLE or not path.name.startswith("vulnerable-")
    return {
        "pipeline": path.name,
        "findings": findings,
        "score": score,
        "gate": determine_gate(score),
        "enforced": enforced,
    }


def build_markdown(report: dict) -> str:
    lines = [
        "# Risk Mapping Report",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Overall gate: **{report['overall_gate'].upper()}**",
        f"- Aggregate score: **{report['aggregate_score']}**",
        "",
    ]

    for pipeline in report["pipelines"]:
        lines.extend(
            [
                f"## {pipeline['pipeline']}",
                "",
                f"- Enforced in gate: {pipeline['enforced']}",
                f"- Score: {pipeline['score']}",
                f"- Gate: {pipeline['gate']}",
            ]
        )

        if not pipeline["findings"]:
            lines.extend(["- Findings: none", ""])
            continue

        lines.append("")
        for finding in pipeline["findings"]:
            lines.append(
                f"- {finding['title']} ({finding['severity']}): {finding['summary']} "
                f"OWASP LLM={', '.join(finding['owasp_llm'])}; "
                f"Cloud={', '.join(finding['cloud_controls'])}; "
                f"Supply chain={', '.join(finding['supply_chain_controls'])}"
            )
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    pipelines = sorted(PIPELINE_DIR.glob("*.yml"))
    analyses = [analyze_pipeline(path) for path in pipelines]
    enforced_analyses = [item for item in analyses if item["enforced"]]
    aggregate_score = min(sum(item["score"] for item in enforced_analyses), 100)
    overall_gate = determine_gate(aggregate_score)

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "aggregate_score": aggregate_score,
        "overall_gate": overall_gate,
        "pipelines": analyses,
    }

    write_json(REPORT_DIR / "risk-report.json", report)
    write_markdown(REPORT_DIR / "risk-report.md", build_markdown(report))


if __name__ == "__main__":
    main()
