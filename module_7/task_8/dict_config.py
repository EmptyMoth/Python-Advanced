import logging


class ASCIIFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.msg.isascii()


class IndividualFileHandler(logging.FileHandler):
    def __init__(self, file_name, mode: str = 'a') -> None:
        super().__init__(file_name, mode)
        self.file_name = file_name
        self.mode: str = mode

    def emit(self, record: logging.LogRecord) -> None:
        message: str = self.format(record)
        self.file_name = f"calc_{record.levelname.lower()}.log"
        with open(self.file_name, mode='a+') as log:
            log.write(f"{message}\n")


DICT_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(msg)s"
        },
    },
    "filters": {
        "ascii_filter": {
            "()": ASCIIFilter,
            "name": "ascii_filter"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
            "formatter": "base",
            "filters": ["ascii_filter"],
        },
        "file": {
            "()": IndividualFileHandler,
            "level": "DEBUG",
            "file_name": "calc_debug.log",
            "formatter": "base",
            "filters": ["ascii_filter"],
        },
        "timed_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "utils.log",
            "level": "INFO",
            "formatter": "base",
            "filters": ["ascii_filter"],
            "when": "h",
            "interval": 10,
            "backupCount": 1,
        },
        "server": {
            "class": "logging.handlers.HTTPHandler",
            "level": "INFO",
            "host": "localhost:5000",
            "url": "/save_log",
            "method": "POST",
        },
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "file", "server"],
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["timed_rotating_file"],
        },
    },
}