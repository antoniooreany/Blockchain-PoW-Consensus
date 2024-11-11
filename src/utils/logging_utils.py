#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a logging_utils.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
# from statistics import variance, covariance

from src.controller.blockchain_controller import get_blockchain_statistics
from src.model.block import Block
from src.utils.constants import (
    SLICE_FACTOR,
    INITIAL_BIT_DIFFICULTY_KEY,
    NUMBER_BLOCKS_TO_ADD_KEY,

    NUMBER_BLOCKS_SLICE_KEY,
    TARGET_BLOCK_MINING_TIME_KEY,
    ADJUSTMENT_BLOCK_INTERVAL_KEY,
    CLAMP_FACTOR_KEY,
    SMALLEST_BIT_DIFFICULTY_KEY,

    AVERAGE_MINING_TIME_SLICE_KEY,
    ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY,
    RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY,

    AVERAGE_BIT_DIFFICULTY_SLICE_KEY,
    # ABSOLUTE_DEVIATION_BIT_DIFFICULTY_SLICE_FROM_INITIAL_KEY,
    # RELATIVE_DEVIATION_BIT_DIFFICULTY_SLICE_FROM_INITIAL_KEY,
    ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY,
    RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY,

    VARIANCE_MINING_TIME_SLICE_KEY,
    VARIANCE_BIT_DIFFICULTY_SLICE_KEY,

    STANDARD_DEVIATION_MINING_TIME_SLICE_KEY,
    STANDARD_DEVIATION_BIT_DIFFICULTY_SLICE_KEY,

    COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY,
    CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY,

    ZERO_MINING_TIME_BLOCKS_NUMBER_KEY,
    RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY,

    DEFAULT_PRECISION,

    # ZERO_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_VARIANCE_MINING_TIME_BLOCKS_KEY,
    # ZERO_VARIANCE_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_STANDARD_DEVIATION_MINING_TIME_BLOCKS_KEY,
    # ZERO_STANDARD_DEVIATION_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_COVARIANCE_MINING_TIME_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_CORRELATION_MINING_TIME_BIT_DIFFICULTY_BLOCKS_KEY,
)


class LogLevelCounterHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.notset_count = 0
        self.info_count = 0
        self.debug_count = 0
        self.warning_count = 0
        self.error_count = 0
        self.critical_count = 0
        self.log_contents = []  # Add this attribute to store log entries


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

        log_entry = self.format(record)
        self.log_contents.append(log_entry)  # Store the log entry


    def get_log_contents(self):
        return "\n".join(self.log_contents)


    def print_log_counts(self):
        logger = logging.getLogger()
        logger.info(f"Log log-levels:")
        logger.info(f"")
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
        reset_color: str = '\033[0m'  # Reset color
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


def log_blockchain_statistics(logger, blockchain):
    blockchain_stats = get_blockchain_statistics(
        blockchain=blockchain,
        slice_factor=SLICE_FACTOR,  # todo remove it
        # number_blocks_slice=NUMBER_BLOCKS_SLICE, # todo use it
    )

    logger.info(f"Blockchain statistics:")
    logger.info(f"")

    logger.info(create_log_message(INITIAL_BIT_DIFFICULTY_KEY, blockchain_stats, "bit"))
    logger.info(create_log_message(TARGET_BLOCK_MINING_TIME_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(ADJUSTMENT_BLOCK_INTERVAL_KEY, blockchain_stats, "block", precision=0))
    logger.info(create_log_message(CLAMP_FACTOR_KEY, blockchain_stats, "bit"))
    logger.info(create_log_message(SMALLEST_BIT_DIFFICULTY_KEY, blockchain_stats, "bit"))
    logger.info(f"")

    logger.info(create_log_message(NUMBER_BLOCKS_TO_ADD_KEY, blockchain_stats, "block", precision=0))

    # logger.info(create_log_message(SLICE_FACTOR_KEY, blockchain_stats, ""))
    logger.info(create_log_message(NUMBER_BLOCKS_SLICE_KEY, blockchain_stats, "block", precision=0))
    logger.info(f"")

    # for the statistical partition
    logger.info(create_log_message(AVERAGE_MINING_TIME_SLICE_KEY, blockchain_stats, "second"))
    logger.info(
        create_log_message(ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY, blockchain_stats, "%"))
    logger.info(create_log_message(VARIANCE_MINING_TIME_SLICE_KEY, blockchain_stats, "second*second"))
    logger.info(create_log_message(STANDARD_DEVIATION_MINING_TIME_SLICE_KEY, blockchain_stats, "second"))
    logger.info(f"")

    logger.info(create_log_message(AVERAGE_BIT_DIFFICULTY_SLICE_KEY, blockchain_stats, "bit"))
    logger.info(
        create_log_message(ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY, blockchain_stats, "bit"))
    logger.info(
        create_log_message(RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY, blockchain_stats, "%"))
    logger.info(create_log_message(VARIANCE_BIT_DIFFICULTY_SLICE_KEY, blockchain_stats, "bit*bit"))
    logger.info(create_log_message(STANDARD_DEVIATION_BIT_DIFFICULTY_SLICE_KEY, blockchain_stats, "bits"))
    logger.info(f"")

    logger.info(create_log_message(COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY, blockchain_stats, "second*bit"))
    logger.info(create_log_message(CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY, blockchain_stats, ""))
    logger.info(f"")

    logger.info(create_log_message(ZERO_MINING_TIME_BLOCKS_NUMBER_KEY, blockchain_stats, ""))
    logger.info(create_log_message(RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY, blockchain_stats, "%"))
    logger.info(f"")


def create_log_message(key: str, blockchain_stats: dict[str, float], unit: str,
                       precision: int = DEFAULT_PRECISION) -> str:
    return f"{key}: {blockchain_stats[key]:.{precision}f} {unit}"


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
