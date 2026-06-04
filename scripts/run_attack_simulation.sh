#!/usr/bin/env bash
set -euo pipefail

python3 attack_simulator/run_attacks.py
echo "Attack simulation completed. Reports available in reports/generated/."
