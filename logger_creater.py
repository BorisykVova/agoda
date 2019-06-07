import logging
from logging import FileHandler, Logger
from logging.handlers import TimedRotatingFileHandler


FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = 'logging/logging.log'


def get_file_handler() -> FileHandler:
    file_handler = TimedRotatingFileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name: str) -> Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
