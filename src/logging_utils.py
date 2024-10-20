#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a logging_utils.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# info: 0, debug: 10, warning: 20, error: 30, critical: 40


import logging

from src.block import Block


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
        # Check for null pointer references and other potential issues
        assert record is not None, "Record cannot be null"
        assert record.msg is not None, "Record message cannot be null"
        assert record.levelname is not None, "Record level name cannot be null"

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


def log_mined_block(block: Block) -> None:
    assert block is not None, "Block cannot be null"
    assert block.index is not None, "Block index cannot be null"
    assert block.hash is not None, "Block hash cannot be null"
    logger: logging.Logger = logging.getLogger()
    logger.info(f"Block mined:")
    logger.info(f"Bit Difficulty: {block.bit_difficulty}")
    logger.info(f"Index: {block.index}")
    logger.info(f"Timestamp: {block.timestamp}")
    logger.info(f"Data: {block.data}")
    # logger.info(f"Previous hash: {block.previous_hash}")
    logger.info(f"Nonce: {block.nonce}")
    logger.info(f"Hash: {block.hash}")


# def log_time(
#         average_time: float,  # The actual time
#         expected_time: float  # The expected time
# ) -> None:
#     logger: logging.Logger = logging.getLogger()
#     assert average_time is not None, "Actual time cannot be null"
#     assert expected_time is not None, "Expected time cannot be null"
#     logger.info(f"Average time: {average_time}, Expected time: {expected_time}")


def log_validity(blockchain) -> None:
    assert blockchain is not None, "Blockchain cannot be null"
    logger: logging.Logger = logging.getLogger()
    assert logger is not None, "Logger cannot be null"
    is_blockchain_valid: bool = blockchain.is_chain_valid()
    assert is_blockchain_valid is not None, "Blockchain validity cannot be null"
    if is_blockchain_valid:
        logger.info(f"Blockchain is valid: {is_blockchain_valid}")
    else:
        logger.critical(f"Blockchain validity: {is_blockchain_valid}")


def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger
