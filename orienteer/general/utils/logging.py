import datetime
import logging
import logging as plogging
import os
from contextlib import contextmanager
from loguru import logger

from typing import Generator

from jukebot.listeners import InterceptHandler
from orienteer.config.local import DEBUG_MODE


def set_logging(
    jukebot_loglevel: int,
    /,
    intercept_disnake_log: bool = True,
    disnake_loglevel: int = logging.INFO,
):
    logger.info(f'Debug mode is {"on" if DEBUG_MODE else "off"}.')
    logger.info(f'Jukebot log messages with level {
                plogging.getLevelName(jukebot_loglevel)}.')

    if intercept_disnake_log:
        logger.info(f'Intercepting disnake log messages with level {
                    plogging.getLevelName(disnake_loglevel)}.')
        logging.basicConfig(
            handlers=[InterceptHandler()], level=disnake_loglevel)

    if not DEBUG_MODE:
        logger.remove()
        fmt = "{time:YYYY-MM-DD at HH:mm:ss} || {level} || {name} || {message}"
        logger.add(
            f"./logs/log-{datetime.datetime.now():%Y-%m-%d}.log",
            level=jukebot_loglevel,
            format=fmt,
            rotation="01:00",
            retention="10 days",
            enqueue=True,
            mode="w",
            encoding="utf-8",
        )


@contextmanager
def disable_logging(name: str | None = None) -> Generator:
    """Temporary disable logging for a given module

    Parameters
    ----------
    name : str | None
        The module name where you want to disable logging
    Example
    _______
    ```
    class MyTest(unittest.TestCase):

        def test_do_something(self):
            with disable_logger('mypackage.mymodule'):
                mymodule.do_something()
    ```
    """
    name = "orienteer" if not name else name
    logger.disable(name)
    try:
        yield
    finally:
        logger.enable(name)
