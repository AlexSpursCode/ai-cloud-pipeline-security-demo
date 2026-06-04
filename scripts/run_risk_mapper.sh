#!/usr/bin/env bash
set -euo pipefail

python3 risk_mapper/mapper.py
echo "Risk mapper completed. Reports available in reports/generated/."
