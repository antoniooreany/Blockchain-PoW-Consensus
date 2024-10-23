#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a logging_utils.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# info: 0, debug: 10, warning: 20, error: 30, critical: 40


import logging
from statistics import variance, covariance

from src.block import Block
from src.constants import (
    TARGET_BLOCK_TIME,
    STATISTICS_PARTITION_INTERVAL_FACTOR,
    NUMBER_BLOCKS_TO_ADD,
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
        logger.info(f"Log log-levels:")
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
    (
        num_blocks,
        absolute_deviation_mining_time,
        average_mining_time,
        correlation_mining_time_bit_difficulty,
        covariance_mining_time_bit_difficulty,
        relative_deviation_mining_time_last_blocks,
        standard_deviation_bit_difficulty,
        standard_deviation_mining_time,
        variance_bit_difficulty,
        variance_mining_time,
        zero_mining_time_blocks,
    ) = get_blockchain_statistics(
        blockchain, STATISTICS_PARTITION_INTERVAL_FACTOR)

    logger.info(f"Blockchain statistics:")
    logger.info(f"Target mining block time: {TARGET_BLOCK_TIME:.25f} seconds")
    logger.info(f"STATISTICS_PARTITION_INTERVAL_FACTOR: {STATISTICS_PARTITION_INTERVAL_FACTOR}")
    logger.info(f"Number of blocks in the statistical partition: {num_blocks}")
    logger.info(f"")

    logger.info(f"Average mining time of the statistical partition: "
                f"{average_mining_time: .25f} seconds")
    logger.info(f"Absolute deviation from the target block time of the statistical partition: "
                f"{absolute_deviation_mining_time: .25f} seconds")
    logger.info(f"Relative deviation from the target block time of the statistical partition: "
                f"{relative_deviation_mining_time_last_blocks: .25f} %")
    logger.info(f"")

    logger.info(f"Variance of the mining time of the statistical partition: "
                f"{variance_mining_time: .25f}")
    logger.info(f"Variance of the bit difficulty of the statistical partition: "
                f"{variance_bit_difficulty: .25f}")
    logger.info(f"Standard deviation of the mining time of the statistical partition: "
                f"{standard_deviation_mining_time: .25f}")
    logger.info(f"Standard deviation of the bit difficulty of the statistical partition: "
                f"{standard_deviation_bit_difficulty: .25f}")
    logger.info(f"Covariance of the mining time and the bit difficulty of the statistical partition: "
                f"{covariance_mining_time_bit_difficulty: .25f}")
    logger.info(f"Correlation of the mining time and the bit difficulty of the statistical partition: "
                f"{correlation_mining_time_bit_difficulty: .25f}")
    logger.info(f"")

    logger.info(f"Number of blocks mined with 0.0 seconds: "
                f"{zero_mining_time_blocks - 1}")  # -1 for the Genesis Block
    logger.info(f"Relative number of blocks mined with 0.0 seconds: "
                f"{((zero_mining_time_blocks - 1) / NUMBER_BLOCKS_TO_ADD) * 100:.25f} %")
    logger.info(f"")


def get_blockchain_statistics(blockchain, statistics_partition_interval_factor):
    num_blocks = int(len(blockchain.mining_times) / statistics_partition_interval_factor)
    # Slice the lists to the num_blocks length
    mining_times_slice = blockchain.mining_times[:num_blocks]
    bit_difficulties_slice = blockchain.bit_difficulties[:num_blocks]

    average_mining_time = blockchain.get_average_mining_time(num_blocks=num_blocks)
    absolute_deviation_mining_time = abs(average_mining_time - TARGET_BLOCK_TIME)
    relative_deviation_mining_time = (
                                             absolute_deviation_mining_time / TARGET_BLOCK_TIME) * 100.0
    variance_mining_time = variance(mining_times_slice)
    variance_bit_difficulty = variance(bit_difficulties_slice)
    standard_deviation_mining_time = variance_mining_time ** 0.5
    standard_deviation_bit_difficulty = variance_bit_difficulty ** 0.5
    covariance_mining_time_bit_difficulty = covariance(mining_times_slice, bit_difficulties_slice)
    # correlation_mining_time_bit_difficulty = (covariance_mining_time_bit_difficulty /
    #                                           (standard_deviation_mining_time * standard_deviation_bit_difficulty))

    if standard_deviation_mining_time == 0 or standard_deviation_bit_difficulty == 0:
        correlation_mining_time_bit_difficulty = 0
    else:
        correlation_mining_time_bit_difficulty = (covariance_mining_time_bit_difficulty /
                                                  (standard_deviation_mining_time * standard_deviation_bit_difficulty))

    # Number of blocks mined with 0.0 seconds:
    zero_mining_time_blocks = sum(1 for time in blockchain.mining_times if time == 0.0)

    return (
        num_blocks,
        absolute_deviation_mining_time,
        average_mining_time,
        correlation_mining_time_bit_difficulty,
        covariance_mining_time_bit_difficulty,
        relative_deviation_mining_time,
        standard_deviation_bit_difficulty,
        standard_deviation_mining_time,
        variance_bit_difficulty,
        variance_mining_time,
        zero_mining_time_blocks,
    )


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
