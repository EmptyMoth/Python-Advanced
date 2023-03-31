import logging


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
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
            "formatter": "base",
        },
        "file": {
            "()": IndividualFileHandler,
            "file_name": "calc_debug.log",
            "level": "DEBUG",
            "formatter": "base",
        },
        "timed_rotating_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "utils.log",
            "level": "INFO",
            "formatter": "base",
            "when": "h",
            "interval": 10,
            "backupCount": 1,
        },
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["timed_rotating_file"],
        },
    },
}
