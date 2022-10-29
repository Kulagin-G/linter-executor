"""
Module for defaults which will are being used in linter.py
"""

import sys

DEFAULTS = {
    "LOGURU_CONFIG": {
        "INFO": {
            "sink": sys.stdout,
            "level": "INFO",
            "format": "<level>{level}</level> - "
            "<level><c>{time:YYYY-MM-DD HH:mm:ss}</c></level> - "
            "<level>{message}</level>",
            "filter": None,
            "serialize": False,
            "colorize": True,
            "diagnose": False,
            "backtrace": False,
            "catch": False,
        },
        "DEBUG": {
            "sink": sys.stdout,
            "level": "DEBUG",
            "format": "<level>{level}</level> - "
            "<level><c>{time:YYYY-MM-DD HH:mm:ss}</c></level> - "
            "<level>{function}:{line}</level> - "
            "<level>{message}</level>",
            "filter": None,
            "serialize": False,
            "colorize": True,
            "diagnose": False,
            "backtrace": False,
            "catch": False,
        },
    }
}
