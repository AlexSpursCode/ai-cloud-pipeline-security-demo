from __future__ import annotations

SEVERITY_POINTS = {
    "critical": 25,
    "high": 18,
    "medium": 10,
    "low": 5,
}


def calculate_score(findings: list[dict]) -> int:
    total = sum(SEVERITY_POINTS.get(finding["severity"], 0) for finding in findings)
    return min(total, 100)


def determine_gate(score: int) -> str:
    if score >= 60:
        return "fail"
    if score >= 30:
        return "warn"
    return "pass"
