# ai-cloud-pipeline-security-demo

Deterministic SANS conference demo showing how to secure AI/LLM workloads in CI/CD with three stages:

1. `risk map`
2. `exploit simulation`
3. `guardrail fix` plus a `final security gate`

The repository contains:

- A small FastAPI app with `vulnerable` and `hardened` modes.
- A `risk_mapper` that inspects CI/CD YAML and maps missing controls to AI, cloud, and supply chain risks.
- An `attack_simulator` that exercises the local `/chat` endpoint with safe synthetic payloads.
- GitHub Actions workflows that run the demo and block pull requests when the security gate fails.
- Pre-generated reports and diagrams so the talk can proceed even without a live run.

## Demo flow

The primary storyline is:

`risk map -> exploit simulation -> guardrail fix -> final security gate`

1. Start the app in `vulnerable` mode.
2. Run the risk mapper against the sample pipelines.
3. Run the attack simulator and show successful prompt injection and synthetic secret disclosure.
4. Switch to `hardened` mode.
5. Re-run the attacks and show the final gate passing.

## Quick start

```bash
cd ai-cloud-pipeline-security-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/setup_demo.sh
./scripts/run_local_demo.sh
```

In another terminal:

```bash
cd ai-cloud-pipeline-security-demo
source .venv/bin/activate
./scripts/run_risk_mapper.sh
./scripts/run_attack_simulation.sh
./scripts/generate_report.sh
```

## Application modes

- `APP_MODE=vulnerable`: intentionally demonstrates unsafe behavior using only synthetic demo secrets.
- `APP_MODE=hardened`: blocks prompt injection, system prompt leakage, and fake secret disclosure.

## Outputs

Generated reports are written to `reports/generated/`:

- `risk-report.json`
- `risk-report.md`
- `attack-report.json`
- `attack-report.md`
- `final-summary.md`

By default, `risk_mapper` still analyzes `vulnerable-*` sample pipelines but excludes them from the enforced aggregate gate so the hardened path can pass in CI. Set `RISK_MAPPER_INCLUDE_VULNERABLE=true` to force them into the gate.

## Safety

- All secrets are fake and clearly marked as demo data.
- No real API keys or credentials are included.
- Payloads and responses are deterministic for repeatable presentations.

## Repository map

- `app/`: FastAPI demo application and tests.
- `pipelines/`: vulnerable and hardened CI/CD examples.
- `risk_mapper/`: control detection, mapping, scoring, and report generation.
- `attack_simulator/`: payload runner and response evaluator.
- `reports/`: pre-generated examples and Mermaid diagrams.
- `docs/`: presentation-facing architecture, controls, and talk notes.
- `scripts/`: local setup and execution helpers.
