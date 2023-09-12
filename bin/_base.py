#!/bin/env python3
# coding: utf-8

import os
import sys
import logging.config
from pathlib import Path

WORKDIR = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(WORKDIR))
os.chdir(WORKDIR)

# 创建日志目录
LOG_DIR = WORKDIR.joinpath("logs")
if not LOG_DIR.exists():
    LOG_DIR.mkdir()


def is_systemd() -> bool:
    """判断是否是systemd"""
    if os.getenv("INVOCATION_ID"):
        return True
    if os.getppid() == "1":
        return True
    return False


IS_SYSTEMD = is_systemd()


def logging_configurator(
    name=__name__,
    console_print=True,
    console_level="DEBUG",
    file_level="INFO",
):
    """创建日志配置"""
    handlers = ["file"]
    if console_print:
        handlers.append("console")

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s %(name)s %(levelname)s - %(message)s"},
            "systemd": {"format": "%(name)s %(levelname)s - %(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "systemd" if is_systemd() else "simple",
                "level": console_level,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "simple",
                "filename": f"logs/{name}.log",
                "mode": "a+",
                "level": file_level,
            },
            "root": {
                "class": "logging.FileHandler",
                "formatter": "simple",
                "filename": "logs/root.log",
                "mode": "a+",
                "level": "DEBUG",
            },
        },
        "loggers": {
            "host-service": {
                "handlers": handlers,
                "level": "INFO",
            }
        },
        "root": {
            "handlers": ["root"],
            "level": "DEBUG",
        },
    }
    logging.config.dictConfig(log_config)


if __name__ == "__main__":
    logging.config.dictConfig(create_config())
    logger = logging.getLogger("host-service")
    print(logger.handlers)
