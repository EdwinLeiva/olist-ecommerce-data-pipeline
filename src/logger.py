import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"


def setup_logger():
    """Configure and return the project logger."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("olist_pipeline")
    logger.setLevel(logging.DEBUG)

    # Allow Prefect to capture and display log messages.
    logger.propagate = False

    # Avoid adding duplicate handlers.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Log to file.
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger