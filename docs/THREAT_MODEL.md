# Threat model

## Primary threats

- Prompt injection against the `/chat` interface
- System prompt leakage
- Synthetic secret disclosure
- Over-privileged CI permissions
- Supply chain risk from unscanned dependencies
- Missing validation before release

## Demo assumptions

- Attackers can submit hostile prompts through the application interface.
- CI/CD definitions are treated as code and may contain dangerous defaults.
- A secure release requires both infrastructure controls and application-layer guardrails.
