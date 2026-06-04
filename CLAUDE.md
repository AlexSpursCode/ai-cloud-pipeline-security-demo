# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A deterministic SANS conference demo showing how to secure AI/LLM workloads in CI/CD pipelines. The full demo storyline is:

`risk map → exploit simulation → guardrail fix → final security gate`

There is **no external LLM dependency** — the synthetic response layer (`app/llm_client.py`) is deterministic so the demo is offline-safe and repeatable.

## Setup and running

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./scripts/setup_demo.sh
./scripts/run_local_demo.sh          # starts FastAPI on port 8000
```

In a second terminal (app must be running first):

```bash
source .venv/bin/activate
./scripts/run_risk_mapper.sh         # writes reports/generated/risk-report.*
./scripts/run_attack_simulation.sh   # writes reports/generated/attack-report.*
./scripts/generate_report.sh         # writes reports/generated/final-summary.md
```

## Tests

```bash
pytest                               # runs app/tests/
pytest app/tests/test_guardrails.py  # single test file
```

## Application modes

Controlled by the `APP_MODE` environment variable (default: `vulnerable`):

- `APP_MODE=vulnerable` — guardrails are bypassed; prompt injection and secret disclosure succeed.
- `APP_MODE=hardened` — `guardrails.inspect_prompt()` runs before every `/chat` request and blocks injections.

`app/config.py` reads this (and other env vars) on every request via `get_settings()` (no caching), so you can switch modes without restarting.

## Architecture

### `app/`
FastAPI service with two endpoints: `GET /health` and `POST /chat`. In hardened mode, `guardrails.py` regex-matches the prompt for injection and secret-disclosure patterns before passing to `llm_client.py`, which returns a deterministic synthetic response.

### `risk_mapper/`
Scans `pipelines/*.yml` for missing security controls. Flow: `parser.py` flattens YAML → `rules.py` defines control keywords and metadata (OWASP LLM, cloud, supply chain mappings) → `mapper.py` detects gaps and calls `scoring.py` → `output.py` writes JSON and Markdown reports.

By default, pipelines whose filenames start with `vulnerable-` are excluded from the aggregate gate so the hardened path passes in CI. Set `RISK_MAPPER_INCLUDE_VULNERABLE=true` to include them.

### `attack_simulator/`
Loads YAML payloads from `attack_simulator/payloads/`, POSTs each to the running app's `/chat` endpoint, then `evaluator.py` checks the response for unsafe patterns. Gate fails if any result is marked unsafe.

### `pipelines/`
Contains `vulnerable-github-actions.yml`, `hardened-github-actions.yml`, and `sample-gitlab-ci.yml` — used as inputs to the risk mapper, not executed locally.

### `reports/`
`reports/generated/` is git-ignored and written at runtime. `reports/` contains pre-generated samples for use if the live demo can't run.

## Key environment variables

| Variable | Default | Purpose |
|---|---|---|
| `APP_MODE` | `vulnerable` | `vulnerable` or `hardened` |
| `APP_HOST` | `127.0.0.1` | Bind address |
| `APP_PORT` | `8000` | Bind port |
| `SYSTEM_PROMPT` | (built-in) | Injected system prompt text |
| `RISK_MAPPER_INCLUDE_VULNERABLE` | `false` | Include `vulnerable-*` pipelines in gate |
