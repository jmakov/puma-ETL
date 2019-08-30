import logging
from logging import handlers
import os
import time

from tools import path


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


def configure_logger(logger, log_fn):
    logger.setLevel(logging.DEBUG)
    log_path = path.get_etl_log_path() + os.sep + log_fn + ".log"
    fh = handlers.RotatingFileHandler(log_path, backupCount=10, maxBytes=1000000)

    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s.%(funcName)s:%(lineno)s:%(levelname)s:%(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logging.info("Logger configured")
