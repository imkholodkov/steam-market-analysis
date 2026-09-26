"""MkDocs-хук: подставляет метку версии сборки вместо {{ build_info }}."""

import hashlib
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path

DATASET = Path(__file__).resolve().parent.parent / "datasets" / "steam_sample.csv"


def _commit() -> str:
    sha = os.environ.get("GITHUB_SHA")
    if sha:
        return sha[:7]
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def on_page_markdown(markdown: str, **_: object) -> str:
    if "{{ build_info }}" not in markdown:
        return markdown
    dataset = hashlib.sha256(DATASET.read_bytes()).hexdigest()[:12]
    info = (
        f"Коммит: `{_commit()}` · "
        f"Сборка: {datetime.now(UTC):%Y-%m-%d %H:%M} UTC · "
        f"Датасет: Kaggle Steam Games v62, выборка `{dataset}`"
    )
    return markdown.replace("{{ build_info }}", info)
