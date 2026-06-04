from __future__ import annotations

from pathlib import Path


def load_yaml_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flatten_content(data: str) -> str:
    return data.lower()
