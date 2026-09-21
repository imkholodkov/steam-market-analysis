import logging

from steam_market_analysis.logging_setup import setup_logging


def test_setup_logging_clears_existing_handlers() -> None:
    root = logging.getLogger()
    setup_logging("INFO")
    handlers_after_first = list(root.handlers)
    setup_logging("DEBUG")
    assert len(root.handlers) == len(handlers_after_first)
    assert root.level == logging.DEBUG


def test_setup_logging_writes_to_stderr() -> None:
    setup_logging("INFO")
    root = logging.getLogger()
    handler = root.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
