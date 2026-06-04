from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI
from pydantic import BaseModel

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent))
    from config import get_settings  # type: ignore  # noqa: E402
    from guardrails import inspect_prompt  # type: ignore  # noqa: E402
    from llm_client import generate_response  # type: ignore  # noqa: E402
else:
    from .config import get_settings  # noqa: E402
    from .guardrails import inspect_prompt  # noqa: E402
    from .llm_client import generate_response  # noqa: E402


app = FastAPI(title="AI Cloud Pipeline Security Demo")


class ChatRequest(BaseModel):
    prompt: str


@app.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "mode": settings.app_mode}


@app.post("/chat")
def chat(request: ChatRequest) -> dict[str, str]:
    settings = get_settings()

    if settings.hardened:
        guardrail_result = inspect_prompt(request.prompt)
        if guardrail_result.blocked:
            return {
                "status": "blocked",
                "mode": settings.app_mode,
                "response": guardrail_result.reason or "Request blocked.",
            }

    result = generate_response(request.prompt, settings.app_mode)
    return {"status": "ok", "mode": result.mode, "response": result.answer}
