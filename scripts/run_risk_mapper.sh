#!/usr/bin/env bash
set -euo pipefail

python3 risk_mapper/mapper.py
echo "Risk mapper completed. Reports available in reports/generated/."

echo
echo "Risk Mapper Report:"
echo "=================================================="
cat reports/generated/risk-report.md
