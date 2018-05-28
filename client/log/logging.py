# -*- coding: utf-8 -*-
import logging.config
from client.settings import LOG_LEVEL

dictLogConfig = {
    "version": 1,
    "handlers": {
        "clientFileHandler": {
            "level": f"{LOG_LEVEL}",
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename": "client/log/messages/client.log"
        },
        "clientStreamHandler": {
            "level": f"{LOG_LEVEL}",
            "class": "logging.StreamHandler",
            "formatter": "formatter",
        }
    },
    "loggers": {
        "clientLogger": {
            "handlers": ["clientFileHandler", "clientStreamHandler"],
            "level": f"{LOG_LEVEL}",
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
