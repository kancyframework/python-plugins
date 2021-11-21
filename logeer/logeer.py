from typing import Any
from loguru import logger
import fileer
import timeer
import os


def addLogFile(topic: str, level: str = "INFO", sync: bool = False):
    log_handler_key = "log_handler_key_{topic}"
    handler_id = os.environ.get(log_handler_key)
    if not handler_id:
        logFileName = f"{topic}_{timeer.today()}.log"
        logdir = fileer.getUserWorkspace(f"logs/{topic}")
        logPath = fileer.paths(logdir, logFileName)
        handler_id = logger.add(logPath, rotation="1 days", retention="30 days", backtrace=True, diagnose=True,
                                enqueue=sync,
                                level=level)
        os.environ[log_handler_key] = str(handler_id)


def removeLogFile(handler_id: int):
    logger.remove(handler_id)
    for key in os.environ:
        if key.startswith("log_handler_key_") and os.environ.get(key) == str(handler_id):
            del os.environ[key]


def trace(message: str, *args: Any, **kwargs: Any) -> None:
    logger.trace(message, *args, **kwargs)


def debug(message: str, *args: Any, **kwargs: Any) -> None:
    logger.debug(message, *args, **kwargs)


def info(message: str, *args: Any, **kwargs: Any) -> None:
    logger.info(message, *args, **kwargs)


def warn(message: str, *args: Any, **kwargs: Any) -> None:
    logger.warning(message, *args, **kwargs)


def error(message: str, *args: Any, **kwargs: Any) -> None:
    logger.error(message, *args, **kwargs)


def success(message: str, *args: Any, **kwargs: Any) -> None:
    logger.success(message, *args, **kwargs)


def catch(exception):
    """
    注解的形式捕获异常，不阻塞执行流程
    put @logeer.catch on fun
    :param exception: 异常
    :return:
    """
    return logger.catch(exception)
