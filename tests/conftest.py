import os
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[None]:
    for key in list(os.environ):
        if key.startswith("RG_"):
            monkeypatch.delenv(key, raising=False)
    monkeypatch.chdir(tmp_path)
    yield
