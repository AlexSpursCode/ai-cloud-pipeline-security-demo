#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from __future__ import annotations

import json
from pathlib import Path
import sys

report_dir = Path("reports/generated")
risk = json.loads((report_dir / "risk-report.json").read_text(encoding="utf-8"))
attack = json.loads((report_dir / "attack-report.json").read_text(encoding="utf-8"))

overall = "pass"
if risk["overall_gate"] != "pass" or attack["gate"] != "pass":
    overall = "fail"

summary = "\n".join(
    [
        "# Final Security Gate Summary",
        "",
        f"- Risk mapper gate: **{risk['overall_gate'].upper()}**",
        f"- Attack simulator gate: **{attack['gate'].upper()}**",
        f"- Final release decision: **{overall.upper()}**",
        "",
        "The release gate passes only when both the pipeline control posture and the AI attack simulation pass.",
        "",
    ]
)
(report_dir / "final-summary.md").write_text(summary, encoding="utf-8")
print(summary)

if overall != "pass":
    sys.exit(1)
PY
