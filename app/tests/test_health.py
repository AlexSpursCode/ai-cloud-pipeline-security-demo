from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from main import app  # type: ignore  # noqa: E402


client = TestClient(app)


def test_health_endpoint_reports_mode() -> None:
    os.environ["APP_MODE"] = "hardened"
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "hardened"}
