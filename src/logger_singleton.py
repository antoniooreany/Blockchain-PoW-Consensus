#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a logger_singleton and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
from logging_utils import ColorFormatter


class LoggerSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if LoggerSingleton._instance is None:
            LoggerSingleton()
        return LoggerSingleton._instance

    def __init__(self):
        if LoggerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LoggerSingleton._instance = self
            self.logger = self.setup_logger()

    def setup_logger(self, level=logging.DEBUG, console_level=logging.DEBUG):
        logger = logging.getLogger()
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
