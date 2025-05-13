import logging
from logging import Logger
from typing import Optional

DEFAULT_LOGGING_LEVEL = logging.INFO

class LoggingBuilder(object):
    def __init__(self, 
                 level: int = DEFAULT_LOGGING_LEVEL,
                 fmt: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
                 datefmt: str = "%Y-%m-%dT%H:%M:%S%z", 
                 log_file: Optional[str] = None):
        self.level = level
        self.fmt = fmt
        self.datefmt = datefmt
        self.log_file = log_file
        self._logger = None
        
    def get_logger(self, name: str) -> Logger:
        '''
        Builds and returns this module logging object
        '''
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            logger.setLevel(self.level)
            formatter = logging.Formatter(self.fmt, self.datefmt)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
            if self.log_file:
                file_handler = logging.FileHandler(self.log_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            logger.propagate = False
        return logger
