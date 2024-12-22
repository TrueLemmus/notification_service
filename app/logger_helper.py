import logging
import sys
from config import settings


def get_logger(name, level=None):
    # Если уровень не передан явно, берём из config
    if level is None:
        level = settings.LOG_LEVEL

    formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
