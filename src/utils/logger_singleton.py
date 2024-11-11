#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a logger_singleton and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging

from src.utils.logging_utils import ColorFormatter


class LoggerSingleton(object):
    _instance = None

    @staticmethod
    def get_instance() -> 'LoggerSingleton':
        """
        Get the logger singleton.

        Returns:
            LoggerSingleton: The logger singleton instance.
        """
        if LoggerSingleton._instance is None:
            LoggerSingleton()
        return LoggerSingleton._instance

    def __init__(self) -> None:
        """
        Initialize the logger singleton.

        If the singleton is already initialized, raise an exception.
        Otherwise, set the singleton instance to this and set up the logger.
        """
        if LoggerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LoggerSingleton._instance = self
            self.logger = self.setup_logger()

    @staticmethod
    def setup_logger(level: int = logging.DEBUG, console_level: int = logging.DEBUG) -> logging.Logger:
        """
        Set up the logger.

        Args:
            level (int): The logging level. Defaults to logging.DEBUG.
            console_level (int): The logging level for the console. Defaults to logging.DEBUG.

        Returns:
            logging.Logger: The configured logger.
        """
        logger: logging.Logger = logging.getLogger()
        logger.setLevel(level)
        ch: logging.StreamHandler = logging.StreamHandler()
        ch.setLevel(console_level)
        formatter: logging.Formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
