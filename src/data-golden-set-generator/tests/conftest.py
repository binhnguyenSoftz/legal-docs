from pathlib import Path

import pytest

from generator import spec

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def example_procedure(monkeypatch):
    monkeypatch.setattr(spec, "TEMPLATES_DIR", FIXTURES)
    return spec.load_procedure("example")
