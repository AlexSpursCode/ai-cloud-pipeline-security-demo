#!/usr/bin/env bash
set -euo pipefail

python3 risk_mapper/mapper.py
echo "Risk mapper completed. Reports available in reports/generated/."

echo
echo "Risk Mapper Report:"
echo "=================================================="
RED=$(printf '\033[31m')
RESET=$(printf '\033[0m')
sed "s/(high)/${RED}(high)${RESET}/g" reports/generated/risk-report.md
