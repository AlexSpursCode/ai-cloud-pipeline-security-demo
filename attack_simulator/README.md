# Attack simulator

`attack_simulator` loads deterministic YAML payloads and sends them to the local `/chat` endpoint. It then evaluates whether the response indicates unsafe behavior.

Unsafe indicators include:

- synthetic secret disclosure
- system prompt leakage
- explicit bypass language

Reports are written to `reports/generated/`.
