#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a logging_utils.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# info: 0, debug: 10, warning: 20, error: 30, critical: 40


# class ErrorCriticalHandler(logging.Handler):
#     def __init__(self):
#         super().__init__()
#         self.error_occurred = False
#         self.critical_occurred = False
#         self.warning_occurred = False
#
#     def emit(self, record):
#         if record.levelno == logging.ERROR:
#             self.error_occurred = True
#         elif record.levelno == logging.CRITICAL:
#             self.critical_occurred = True
#         elif record.levelno == logging.WARNING:
#             self.warning_occurred = True


# # src/logging_utils.py
# import logging
#
#
# class ErrorCriticalHandler(logging.Handler):
#     def __init__(self):
#         super().__init__()
#         self.max_level = logging.NOTSET
#
#     def emit(self, record):
#         if record.levelno > self.max_level:
#             self.max_level = record.levelno


# src/logging_utils.py

# class ErrorCriticalHandler(logging.Handler):  # todo rename
#     def __init__(self):
#         super().__init__()
#         self.critical_occurred = 0
#         self.error_occurred = 0
#         self.info_count = 0
#         self.debug_count = 0
#         self.warning_count = 0
#         self.error_count = 0
#         self.critical_count = 0
#
#     def emit(self, record):
#         if record.levelno == logging.INFO:
#             self.info_count += 1
#         elif record.levelno == logging.DEBUG:
#             self.debug_count += 1
#         elif record.levelno == logging.WARNING:
#             self.warning_count += 1
#         elif record.levelno == logging.ERROR:
#             self.error_count += 1
#         elif record.levelno == logging.CRITICAL:
#             self.critical_count += 1


# src/logging_utils.py
import logging


class LogLevelCounterHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.notset_count = 0
        self.info_count = 0
        self.debug_count = 0
        self.warning_count = 0
        self.error_count = 0
        self.critical_count = 0

    def emit(self, record):
        if record.levelno == logging.NOTSET:
            self.notset_count += 1
        elif record.levelno == logging.INFO:
            self.info_count += 1
        elif record.levelno == logging.DEBUG:
            self.debug_count += 1
        elif record.levelno == logging.WARNING:
            self.warning_count += 1
        elif record.levelno == logging.ERROR:
            self.error_count += 1
        elif record.levelno == logging.CRITICAL:
            self.critical_count += 1

    def print_log_counts(self):
        logger = logging.getLogger()
        logger.info(f"NotSet messages: {self.notset_count}")
        logger.info(f"Info messages: {self.info_count}")
        logger.debug(f"Debug messages: {self.debug_count}")
        logger.warning(f"Warning messages: {self.warning_count}")
        logger.error(f"Error messages: {self.error_count}")
        logger.critical(f"Critical messages: {self.critical_count}")


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record and add color to it.

        Args:
            record: The log record to be formatted. Must not be null.

        Returns:
            The formatted log record as a string.
        """
        # Check for null pointer references and other potential issues
        assert record is not None, "Record cannot be null"
        assert record.msg is not None, "Record message cannot be null"
        assert record.levelname is not None, "Record levelname cannot be null"

        log_colors: dict = {
            'DEBUG': '\033[94m',  # Blue
            'INFO': '\033[92m',  # Green
            'WARNING': '\033[93m',  # Yellow
            'ERROR': '\033[91m',  # Red
            'CRITICAL': '\033[95m'  # Magenta
        }
        reset_color: str = '\033[0m'
        log_color: str = log_colors.get(record.levelname, reset_color)
        record.msg = f"{log_color}{record.msg}{reset_color}"
        return super().format(record)


def log_mined_block(block) -> None:
    """
    Log the given block as mined.

    Args:
        block: The block to log. Must not be null.

    Returns:
        None
    """
    assert block is not None, "Block cannot be null"
    assert block.index is not None, "Block index cannot be null"
    assert block.hash is not None, "Block hash cannot be null"
    logger: logging.Logger = logging.getLogger()
    logger.info(f"Mined block: (index: {block.index}, hash: {block.hash})")


def log_time(
        average_time: float,  # The actual time
        expected_time: float  # The expected time
) -> None:
    """
    Log the average time taken to mine a block and the expected time.

    Args:
        average_time (float): The actual time taken to mine a block. Must not be null.
        expected_time (float): The expected time taken to mine a block. Must not be null.

    Returns:
        None
    """
    logger: logging.Logger = logging.getLogger()
    assert average_time is not None, "Actual time cannot be null"
    assert expected_time is not None, "Expected time cannot be null"
    logger.info(f"Average time: {average_time}, Expected time: {expected_time}")


def log_validity(blockchain) -> None:
    """
    Log the validity of the given blockchain.

    Args:
        blockchain (Blockchain): The blockchain to check. Must not be null.

    Returns:
        None
    """
    assert blockchain is not None, "Blockchain cannot be null"
    logger: logging.Logger = logging.getLogger()
    # logger.setLevel(logging.CRITICAL)
    assert logger is not None, "Logger cannot be null"
    is_blockchain_valid: bool = blockchain.is_chain_valid()
    assert is_blockchain_valid is not None, "Blockchain validity cannot be null"
    if is_blockchain_valid:
        logger.info(f"Blockchain is valid: {is_blockchain_valid}")
    else:
        logger.critical(f"Blockchain validity: {is_blockchain_valid}")
