from __future__ import annotations

import re
from dataclasses import dataclass


INJECTION_PATTERNS = [
    r"ignore (all|previous) instructions",
    r"reveal (the )?system prompt",
    r"print the hidden prompt",
    r"developer mode",
    r"bypass guardrails",
]

SECRET_PATTERNS = [
    r"secret",
    r"api key",
    r"credential",
    r"token",
    r"password",
]


@dataclass(frozen=True)
class GuardrailResult:
    blocked: bool
    reason: str | None = None


def inspect_prompt(prompt: str) -> GuardrailResult:
    lowered = prompt.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            return GuardrailResult(True, "Prompt injection attempt detected.")

    for pattern in SECRET_PATTERNS:
        if re.search(pattern, lowered):
            return GuardrailResult(True, "Synthetic secret disclosure request blocked.")

    return GuardrailResult(False, None)
