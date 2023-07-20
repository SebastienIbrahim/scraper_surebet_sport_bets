import logging
from pathlib import Path


def setup_error_logger():
    """Setup the error logger"""
    logger = logging.getLogger("error_logger")
    logger.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        "*" * 39 + "\n%(asctime)s - %(levelname)s - %(message)s"
    )
    path = Path(__file__).parent.parent / "logs" / "errors.log"

    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def setup_captcha_logger():
    """Setup the captcha logger"""

    logger = logging.getLogger("captcha_logger")
    logger.setLevel(logging.WARNING)

    formatter = logging.Formatter(
        "-" * 39 + "\n%(asctime)s - %(levelname)s - %(message)s"
    )
    path = Path(__file__).parent.parent / "logs" / "captcha.log"
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def setup_scraper_logger():
    """Setup the scraper logger"""
    logger = logging.getLogger("scraper_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "=" * 39 + "\n%(asctime)s - %(levelname)s - %(message)s"
    )
    path = Path(__file__).parent.parent / "logs" / "scraper.log"
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
