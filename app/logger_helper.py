import logging
import sys
from typing import Optional, Union

from config import settings


def get_logger(name: str, level: Optional[Union[int, str]] = None) -> logging.Logger:
    """
    Создаёт и настраивает экземпляр логгера с указанным именем и уровнем логирования.

    Если уровень логирования не передан явно, он берётся из `settings.LOG_LEVEL`.

    :param name: Имя логгера.
    :type name: str
    :param level: Уровень логирования (например, `logging.DEBUG`, `logging.INFO` или строковое значение).
                  Если не задан, используется значение из `settings.LOG_LEVEL`.
    :type level: Optional[Union[int, str]]
    :return: Настроенный экземпляр логгера.
    :rtype: logging.Logger
    """
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
