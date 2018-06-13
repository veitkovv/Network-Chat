# -*- coding: utf-8 -*-
import logging.config
from client.settings import CONSOLE_LOG_LEVEL

dictLogConfig = {
    "version": 1,
    "handlers": {
        "clientFileHandler": {
            "level": "DEBUG",  # always debug
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename": "client/log/messages/client.log"
        },
        "clientStreamHandler": {
            "level": f"{CONSOLE_LOG_LEVEL}",  # console output
            "class": "logging.StreamHandler",
            "formatter": "formatter",
        }
    },
    "loggers": {
        "clientLogger": {
            "handlers": ["clientFileHandler", "clientStreamHandler"],
            "level": "DEBUG",
        }
    },
    "formatters": {
        "formatter": {
            "format": "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
        }
    }
}

logging.config.dictConfig(dictLogConfig)
client_logger = logging.getLogger("clientLogger")
