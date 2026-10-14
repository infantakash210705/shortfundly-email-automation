"""Headless smoke test: the Streamlit app must start and render every tab without exceptions."""
from pathlib import Path

import pytest

pytest.importorskip("streamlit.testing.v1")
from streamlit.testing.v1 import AppTest  # noqa: E402

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def test_app_renders_without_errors(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "smoke.db"))
    monkeypatch.setenv("SEND_MODE", "test")
    monkeypatch.setenv("TEST_RECIPIENT", "internal-test@example.invalid")
    monkeypatch.setenv("SMTP_HOST", "smtp.example.invalid")
    monkeypatch.setenv("SMTP_FROM_EMAIL", "campus@example.invalid")
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert not at.exception, [e.value for e in at.exception]
    assert len(at.tabs) >= 5
