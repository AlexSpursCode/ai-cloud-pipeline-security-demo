# SANS talk notes

## Opening

AI features are now part of normal delivery pipelines, so control failures span application security, cloud security, and supply chain security simultaneously.

## Story arc

1. Map missing controls before deployment.
2. Prove exploitability with controlled attack simulation.
3. Apply guardrails and least privilege.
4. Enforce a final automated release decision.

## Talking points

- The vulnerable mode is intentionally unsafe and uses synthetic secrets only.
- The hardened mode demonstrates deterministic control outcomes suitable for CI.
- The value of the demo is the linkage from misconfiguration to exploit to release blocking.
