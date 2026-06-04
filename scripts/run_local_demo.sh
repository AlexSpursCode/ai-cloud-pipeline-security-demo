#!/usr/bin/env bash
set -euo pipefail

APP_MODE="${APP_MODE:-vulnerable}"
uvicorn app.main:app --host 127.0.0.1 --port 8000
