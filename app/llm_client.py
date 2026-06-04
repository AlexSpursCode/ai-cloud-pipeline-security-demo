from __future__ import annotations

from dataclasses import dataclass


FAKE_SECRET = "DEMO_SECRET=demo-sk-1234567890"
SYSTEM_PROMPT_SNIPPET = "SYSTEM_PROMPT=You are DemoCloudAI with internal deployment notes."


@dataclass(frozen=True)
class ChatResult:
    answer: str
    mode: str


def generate_response(prompt: str, app_mode: str) -> ChatResult:
    lowered = prompt.lower()

    if app_mode == "vulnerable":
        if "system prompt" in lowered or "hidden prompt" in lowered:
            return ChatResult(
                answer=f"Unsafe disclosure for demo purposes: {SYSTEM_PROMPT_SNIPPET}",
                mode=app_mode,
            )
        if any(term in lowered for term in ["secret", "api key", "credential", "token", "password"]):
            return ChatResult(
                answer=f"Unsafe disclosure for demo purposes: {FAKE_SECRET}",
                mode=app_mode,
            )
        if "ignore previous instructions" in lowered or "bypass guardrails" in lowered:
            return ChatResult(
                answer="Unsafe execution path enabled. Internal tools would now be exposed.",
                mode=app_mode,
            )

    return ChatResult(
        answer=(
            "Demo response: This assistant summarizes cloud AI pipeline security "
            "controls and avoids handling sensitive material."
        ),
        mode=app_mode,
    )
