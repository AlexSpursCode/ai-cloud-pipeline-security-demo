# Architecture

The demo uses a deliberately simple architecture so the audience can focus on control placement instead of platform complexity.

## Components

- `app/`: deterministic FastAPI interface that stands in for an LLM-enabled service.
- `risk_mapper/`: scans CI/CD definitions and maps missing controls to security frameworks.
- `attack_simulator/`: replays adversarial prompts against the local app endpoint.
- `reports/`: stores pre-generated and generated outputs for presentation and pipeline evidence.
- `scripts/`: orchestrates the local demo and CI entry points.

## Trust boundaries

- Source control to CI runner
- CI runner to build and deployment logic
- Application runtime to model interaction layer
- Security tooling to release decision

## Design choice

There is no external LLM dependency. The synthetic response layer keeps the demo deterministic, offline-safe, and suitable for live conference environments.
