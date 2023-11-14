import os
import logging
from fastapi.logger import logger as fastapi_logger


import logging
from fastapi.logger import logger as fastapi_logger

gunicorn_error_logger = logging.getLogger("gunicorn.error")
if os.getenv("ENV") == "prod":
    gunicorn_logger = logging.getLogger("gunicorn")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

    fastapi_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.setLevel(gunicorn_logger.level)
else:
    fastapi_logger.setLevel(logging.DEBUG)
logger = gunicorn_error_logger


def log_called(fn):
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {fn.__name__}")
        resp = fn(*args, **kwargs)
        logger.info(f"Finished calling {fn.__name__}")
        logger.info(f"Response: {resp}")
        return resp

    return wrapper
