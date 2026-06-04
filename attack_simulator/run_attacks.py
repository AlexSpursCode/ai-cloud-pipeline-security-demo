from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import httpx

from evaluator import evaluate_response


ROOT_DIR = Path(__file__).resolve().parents[1]
PAYLOAD_DIR = ROOT_DIR / "attack_simulator" / "payloads"
REPORT_DIR = ROOT_DIR / "reports" / "generated"
BASE_URL = "http://127.0.0.1:8000"


def load_payloads() -> list[dict]:
    payloads: list[dict] = []
    for path in sorted(PAYLOAD_DIR.glob("*.yml")):
        data: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.strip().startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
        payloads.append({"file": path.name, **data})
    return payloads


def build_markdown(report: dict) -> str:
    lines = [
        "# Attack Simulation Report",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Target: {report['target']}",
        f"- Gate: **{report['gate'].upper()}**",
        "",
    ]

    for result in report["results"]:
        lines.extend(
            [
                f"## {result['name']}",
                "",
                f"- Payload file: {result['file']}",
                f"- Status: {result['status']}",
                f"- Unsafe detected: {result['unsafe']}",
                f"- Response: `{result['response']}`",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    payloads = load_payloads()
    results: list[dict] = []

    with httpx.Client(timeout=5.0) as client:
        for payload in payloads:
            response = client.post(f"{BASE_URL}/chat", json={"prompt": payload["prompt"]})
            body = response.json()
            evaluation = evaluate_response(body["response"])
            results.append(
                {
                    "file": payload["file"],
                    "name": payload["name"],
                    "status": body["status"],
                    "response": body["response"],
                    "unsafe": evaluation["unsafe"],
                    "matches": evaluation["matches"],
                    "expected": payload["expected_behavior"],
                }
            )

    gate = "fail" if any(result["unsafe"] for result in results) else "pass"
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "target": BASE_URL,
        "gate": gate,
        "results": results,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "attack-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (REPORT_DIR / "attack-report.md").write_text(build_markdown(report), encoding="utf-8")


if __name__ == "__main__":
    main()
