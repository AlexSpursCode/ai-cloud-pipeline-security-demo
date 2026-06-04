# App demo

The FastAPI app exposes:

- `GET /health`
- `POST /chat`

`APP_MODE` controls behavior:

- `vulnerable`: intentionally leaks fake secrets and echoes restricted instructions when prompted.
- `hardened`: applies deterministic guardrails that block prompt injection, system prompt leakage, and synthetic secret disclosure.

The app is designed for local demos and CI use. It does not call a real LLM provider.
