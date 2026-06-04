#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip
pip install -r requirements.txt
mkdir -p reports/generated
echo "Demo environment ready."
