from absl import logging


def log_called(fn):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {fn.__name__}")
        resp = fn(*args, **kwargs)
        logging.info(f"Finished calling {fn.__name__}")
        logging.info(f"Response: {resp}")
        return resp

    return wrapper
