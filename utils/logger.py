import logging


class ShortNameFormatter(logging.Formatter):
    def format(self, record):
        record.name = record.name.split(".")[-1]
        return super().format(record)


def setup_logging() -> None:
    """Sets up the logging configuration of the application. Will be called in the main entry point."""
    handler = logging.StreamHandler()
    formatter = ShortNameFormatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    root.addHandler(handler)

    logging.getLogger("yfinance").setLevel(logging.WARNING)
    logging.getLogger("peewee").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("fontTools").setLevel(logging.WARNING)
    logging.getLogger("fontTools.subset").setLevel(logging.WARNING)
    logging.getLogger("fontTools.ttLib").setLevel(logging.WARNING)
    logging.getLogger("MARKDOWN").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
