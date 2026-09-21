import pytest
from typer.testing import CliRunner

from steam_market_analysis.cli import app

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip()


def test_check_config_hides_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RG_GITHUB_TOKEN", "ghp_supersecretvalue")
    result = runner.invoke(app, ["check-config"])
    assert result.exit_code == 0
    assert "ghp_supersecretvalue" not in result.stdout


def test_check_config_shows_none_without_token() -> None:
    result = runner.invoke(app, ["check-config"])
    assert result.exit_code == 0
    assert "github_token: не задан" in result.stdout
