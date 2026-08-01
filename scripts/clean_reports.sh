#!/usr/bin/env bash
set -euo pipefail

find reports/generated \
  -type f \
  ! -name ".gitkeep" \
  -delete

echo "Generated reports cleaned."
