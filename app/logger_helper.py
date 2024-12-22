import logging
import sys


def get_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
