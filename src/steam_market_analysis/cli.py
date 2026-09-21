import logging

import typer

from steam_market_analysis import __version__
from steam_market_analysis.config import get_settings
from steam_market_analysis.logging_setup import setup_logging

app = typer.Typer(help="Анализ рынка игр в Steam")
logger = logging.getLogger(__name__)


def _mask_token(token: str | None) -> str:
    if not token:
        return "не задан"
    if len(token) <= 8:
        return "*" * len(token)
    return f"{token[:4]}{'*' * (len(token) - 8)}{token[-4:]}"


@app.command()
def version() -> None:
    """Показать версию пакета."""
    typer.echo(__version__)


@app.command(name="check-config")
def check_config() -> None:
    """Загрузить настройки и вывести их сводку."""
    settings = get_settings()
    setup_logging(settings.log_level)
    logger.info("настройки загружены")

    typer.echo(f"data_dir: {settings.data_dir}")
    typer.echo(f"log_level: {settings.log_level}")
    typer.echo(f"request_timeout: {settings.request_timeout}")
    typer.echo(f"max_concurrency: {settings.max_concurrency}")
    typer.echo(f"github_token: {_mask_token(settings.github_token)}")


if __name__ == "__main__":
    app()
