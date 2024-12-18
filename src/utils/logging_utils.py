#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a logging_utils.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# path: src/utils/logging_utils.py

import logging

from statistics import variance
from typing import List, Dict

import numpy as np

from src.model.block import Block
from src.constants import (
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

    DEFAULT_PRECISION, BASE, AVERAGE_DIFFICULTY_SLICE_KEY,
    ABSOLUTE_DEVIATION_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY,
    RELATIVE_DEVIATION_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY, VARIANCE_DIFFICULTY_SLICE_KEY,
    STANDARD_DEVIATION_DIFFICULTY_SLICE_KEY, COVARIANCE_MINING_TIME_DIFFICULTY_SLICE_KEY,
    CORRELATION_MINING_TIME_DIFFICULTY_SLICE_KEY, ZERO_MINING_TIME_BLOCKS_INDEXES_KEY,
)


class LogLevelCounterHandler(logging.Handler):
    def __init__(self) -> None:
        """
        Initialize a new LogLevelCounterHandler.

        Sets all log level counters to 0.

        Attributes:
            notset_count (int): Counter for logs with level NOTSET.
            info_count (int): Counter for logs with level INFO.
            debug_count (int): Counter for logs with level DEBUG.
            warning_count (int): Counter for logs with level WARNING.
            error_count (int): Counter for logs with level ERROR.
            critical_count (int): Counter for logs with level CRITICAL.
            difficulty_anomalies_count (int): Counter for difficulty anomaly logs.
            log_contents (List[str]): List to store log messages.
        """
        super().__init__()
        self.notset_count: int = 0
        self.info_count: int = 0
        self.debug_count: int = 0
        self.warning_count: int = 0
        self.error_count: int = 0
        self.critical_count: int = 0
        self.difficulty_anomalies_count: int = 0
        self.log_contents: List[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        """
        Handle a log record.

        The method increments the corresponding log level counter and stores the log message in log_contents.

        Args:
            record: The log record to handle.
        """
        # Increment the corresponding log level counter
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

        # Count difficulty anomalies
        if "Anomaly detected for blocks" in record.msg:
            self.difficulty_anomalies_count += 1

        # Store the log message
        log_entry: str = self.format(record)
        self.log_contents.append(log_entry)

    def print_log_counts(self) -> None:
        """
        Print the counts of log messages with different log levels.

        Args:
            None

        Returns:
            None
        """
        logger: logging.Logger = logging.getLogger()
        logger.info(f"Log levels:")
        logger.info(f"NotSet messages: {self.notset_count}")
        logger.info(f"Info messages: {self.info_count}")
        logger.debug(f"Debug messages: {self.debug_count}")
        logger.warning(f"Warning messages: {self.warning_count}")
        logger.error(f"Error messages: {self.error_count}")
        logger.critical(f"Critical messages: {self.critical_count}\n")
        if self.difficulty_anomalies_count > 0:
            logger.critical(f"Difficulty adjustment anomalies number: {self.difficulty_anomalies_count}")
        else:
            logger.info(f"No anomalies detected for blocks.")


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a logging record.

        This formatting is the same as the standard logging format, but with
        colors added for the different log levels.

        Args:
            record (logging.LogRecord): The logging record to format

        Returns:
            str: The formatted string
        """
        assert isinstance(record, logging.LogRecord), "Record must be of type logging.LogRecord"
        assert record.msg is not None, "Record message cannot be null"
        assert record.levelname is not None, "Record level name cannot be null"

        log_colors: Dict[str, str] = {
            'DEBUG': '\033[94m',  # Blue
            'INFO': '\033[92m',  # Green
            'WARNING': '\033[93m',  # Yellow
            'ERROR': '\033[91m',  # Red
            'CRITICAL': '\033[95m'  # Magenta
        }
        reset_color: str = '\033[0m'  # Reset color
        log_color: str = log_colors.get(record.levelname, reset_color)
        record.msg = f"{log_color}{record.msg}{reset_color}"
        return super().format(record)  # type: ignore[no-any-return]


def log_mined_block(block: Block) -> None:
    """
    Log the details of a mined block.

    Args:
        block: The block that was mined (Block)
    """
    assert block is not None, "Block cannot be null"
    assert block.index is not None, "Block index cannot be null"
    assert block.hash is not None, "Block hash cannot be null"
    logger: logging.Logger = logging.getLogger()
    logger.info(f"Block mined:")
    logger.info(f"Bit Difficulty: {block.bit_difficulty}")
    logger.info(f"Difficulty: {BASE ** block.bit_difficulty}")
    logger.info(f"Index: {block.index}")
    logger.info(f"Timestamp at the beginning of the block {block.index}: {block.timestamp}")
    logger.info(f"Data: {block.data}")
    logger.info(f"Previous hash: {block.previous_hash}")
    logger.info(f"Nonce: {block.nonce}")
    logger.info(f"Hash: {block.hash}")


def log_blockchain_statistics(logger: logging.Logger, blockchain: 'Blockchain') -> None:
    """
    Log the blockchain statistics.

    Args:
        logger (logging.Logger): The logger to use.
        blockchain (Blockchain): The blockchain to get the statistics from.
    """
    blockchain_stats: Dict[str, float] = get_blockchain_statistics(
        blockchain=blockchain,
        number_blocks_slice=blockchain.number_blocks_slice,
    )

    logger.info("Blockchain statistics:")
    logger.info("")

    logger.info(create_log_message(INITIAL_BIT_DIFFICULTY_KEY, blockchain_stats, "bit"))
    logger.info(create_log_message(TARGET_BLOCK_MINING_TIME_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(ADJUSTMENT_BLOCK_INTERVAL_KEY, blockchain_stats, "block", precision=0))
    logger.info(create_log_message(CLAMP_FACTOR_KEY, blockchain_stats, "bit"))
    logger.info(create_log_message(SMALLEST_BIT_DIFFICULTY_KEY, blockchain_stats, "bit"))
    logger.info("")

    logger.info(create_log_message(NUMBER_BLOCKS_TO_ADD_KEY, blockchain_stats, "block", precision=0))
    logger.info(create_log_message(NUMBER_BLOCKS_SLICE_KEY, blockchain_stats, "block", precision=0))
    logger.info("")

    # for the number of blocks mined with 0.0 seconds (anomalies)
    logger.info(create_log_message(ZERO_MINING_TIME_BLOCKS_INDEXES_KEY, blockchain_stats, ""))  # todo ?
    logger.info(create_log_message(ZERO_MINING_TIME_BLOCKS_NUMBER_KEY, blockchain_stats, ""))
    logger.info(create_log_message(RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY, blockchain_stats, "%"))
    logger.info("")

    # for the statistical partition of the mining time
    logger.info(create_log_message(AVERAGE_MINING_TIME_SLICE_KEY, blockchain_stats, "second"))
    logger.info(
        create_log_message(ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY, blockchain_stats, "%"))
    logger.info(create_log_message(VARIANCE_MINING_TIME_SLICE_KEY, blockchain_stats, "second*second"))
    logger.info(create_log_message(STANDARD_DEVIATION_MINING_TIME_SLICE_KEY, blockchain_stats, "second"))
    logger.info("")

    logger.info(create_log_message(AVERAGE_DIFFICULTY_SLICE_KEY, blockchain_stats, ""))
    logger.info(create_log_message(VARIANCE_DIFFICULTY_SLICE_KEY, blockchain_stats, ""))
    logger.info(create_log_message(STANDARD_DEVIATION_DIFFICULTY_SLICE_KEY, blockchain_stats, ""))
    logger.info("")

    # for the linear relation between the mining time and the difficulty
    logger.info(create_log_message(COVARIANCE_MINING_TIME_DIFFICULTY_SLICE_KEY, blockchain_stats, "second*1"))
    logger.info(create_log_message(CORRELATION_MINING_TIME_DIFFICULTY_SLICE_KEY, blockchain_stats, "\n"))


def create_log_message(
        key: str, blockchain_stats: Dict[str, float], unit: str, precision: int = DEFAULT_PRECISION
) -> str:
    """
    Creates a log message with the given key, value, unit and precision.

    The function takes a key, a dictionary containing the value associated with the key,
    a unit and an optional precision. The function returns a log message in the form:
    "<key>: <value> <unit>".

    Args:
        key (str): The key to use in the log message.
        blockchain_stats (Dict[str, float]): The dictionary containing the value associated with the key.
        unit (str): The unit of the value.
        precision (int, optional): The precision of the value. Defaults to DEFAULT_PRECISION.

    Returns:
        str: The log message.
    """
    value: float = blockchain_stats[key]
    if isinstance(value, (int, float)):
        return f"{key}: {value:.{precision}f} {unit}"
    else:
        return f"{key}: {value} {unit}"


def get_blockchain_statistics(
        blockchain: 'Blockchain',
        number_blocks_slice: int,
) -> Dict[str, float]:
    """
    Compute and return the statistics for the blockchain.

    Args:
        blockchain (Blockchain): The blockchain to compute the statistics for.
        number_blocks_slice (int): The number of last blocks to consider for the statistics.

    Returns:
        Dict[str, float]: A dictionary containing the statistics. The keys are defined in the constants.py module.
    """
    assert blockchain is not None
    assert number_blocks_slice > 0

    mining_times_slice = blockchain.mining_times[:number_blocks_slice]
    assert mining_times_slice is not None
    assert mining_times_slice != []

    bit_difficulties_slice = blockchain.bit_difficulties[:number_blocks_slice]
    assert bit_difficulties_slice is not None
    assert bit_difficulties_slice != []

    average_mining_time_slice = blockchain.get_average_mining_time(num_last_blocks=number_blocks_slice)
    assert average_mining_time_slice is not None
    assert average_mining_time_slice >= 0

    absolute_deviation_mining_time_average_from_target_slice = abs(
        average_mining_time_slice - blockchain.target_block_mining_time)
    assert absolute_deviation_mining_time_average_from_target_slice >= 0

    relative_deviation_mining_time_average_from_target_slice = (
                                                                       absolute_deviation_mining_time_average_from_target_slice / blockchain.target_block_mining_time) * 100.0
    assert relative_deviation_mining_time_average_from_target_slice >= 0

    variance_mining_time_slice = variance(mining_times_slice)
    assert variance_mining_time_slice is not None
    assert variance_mining_time_slice >= 0

    standard_deviation_mining_time_slice = variance_mining_time_slice ** 0.5
    assert standard_deviation_mining_time_slice is not None
    assert standard_deviation_mining_time_slice >= 0

    # Statistics for the bit_difficulty
    average_bit_difficulty_slice = sum(bit_difficulties_slice) / number_blocks_slice
    assert average_bit_difficulty_slice is not None
    assert average_bit_difficulty_slice >= 0

    absolute_deviation_bit_difficulty_average_from_initial_slice = abs(
        average_bit_difficulty_slice - blockchain.initial_bit_difficulty)
    assert absolute_deviation_bit_difficulty_average_from_initial_slice >= 0

    relative_deviation_bit_difficulty_average_from_initial_slice = (
                                                                           absolute_deviation_bit_difficulty_average_from_initial_slice / blockchain.initial_bit_difficulty) * 100.0
    assert relative_deviation_bit_difficulty_average_from_initial_slice >= 0

    variance_bit_difficulty_slice = variance(bit_difficulties_slice)
    assert variance_bit_difficulty_slice is not None
    assert variance_bit_difficulty_slice >= 0

    standard_deviation_bit_difficulty_slice = variance_bit_difficulty_slice ** 0.5
    assert standard_deviation_bit_difficulty_slice is not None
    assert standard_deviation_bit_difficulty_slice >= 0

    # covariance_mining_time_bit_difficulty_slice = covariance(mining_times_slice, bit_difficulties_slice)
    covariance_mining_time_bit_difficulty_slice = np.cov(mining_times_slice, bit_difficulties_slice)[
        0, 1]

    if standard_deviation_mining_time_slice == 0 or standard_deviation_bit_difficulty_slice == 0:
        correlation_mining_time_bit_difficulty_slice = 0  # todo is it correct from the math point of view?
    else:
        correlation_mining_time_bit_difficulty_slice = (covariance_mining_time_bit_difficulty_slice / (
                standard_deviation_mining_time_slice * standard_deviation_bit_difficulty_slice))

    zero_mining_time_blocks_indexes = [index for index, time in enumerate(blockchain.mining_times) if time == 0.0]
    # zero_mining_time_blocks_number = sum(1 for time in blockchain.mining_times if time == 0.0)  # todo should be a property?
    zero_mining_time_blocks_number = len(zero_mining_time_blocks_indexes)
    assert zero_mining_time_blocks_number >= 0

    relative_zero_mining_time_blocks_number = (zero_mining_time_blocks_number / blockchain.number_blocks_to_add) * 100.0
    assert relative_zero_mining_time_blocks_number >= 0

    # create difficulties from blockchain.bit_difficulties
    difficulties = [BASE ** bit_difficulty for bit_difficulty in
                    blockchain.bit_difficulties]  # todo should a blockchain.difficulties or block.difficulty be created?
    assert difficulties is not None
    assert difficulties != []

    difficulties_slice = difficulties[:number_blocks_slice]

    average_difficulty_slice = sum(difficulties_slice) / number_blocks_slice
    assert average_difficulty_slice is not None
    assert average_difficulty_slice >= 0

    absolute_deviation_difficulty_average_from_initial_slice = abs(
        average_difficulty_slice - BASE ** blockchain.initial_bit_difficulty)
    assert absolute_deviation_difficulty_average_from_initial_slice >= 0

    relative_deviation_difficulty_average_from_initial_slice = (
                                                                       absolute_deviation_difficulty_average_from_initial_slice / BASE ** blockchain.initial_bit_difficulty) * 100.0
    assert relative_deviation_difficulty_average_from_initial_slice >= 0

    variance_difficulty_slice = variance(difficulties_slice)
    assert variance_difficulty_slice is not None
    assert variance_difficulty_slice >= 0

    standard_deviation_difficulty_slice = variance_difficulty_slice ** 0.5
    assert standard_deviation_difficulty_slice is not None
    assert standard_deviation_difficulty_slice >= 0

    # covariance_mining_time_difficulty_slice = covariance(mining_times_slice, difficulties_slice)
    covariance_mining_time_difficulty_slice = np.cov(mining_times_slice, difficulties_slice)[0, 1]

    if standard_deviation_mining_time_slice == 0 or standard_deviation_difficulty_slice == 0:
        correlation_mining_time_difficulty_slice = 0  # todo is it correct from the math point of view?
    else:
        correlation_mining_time_difficulty_slice = (covariance_mining_time_difficulty_slice / (
                standard_deviation_mining_time_slice * standard_deviation_difficulty_slice))

    assert correlation_mining_time_difficulty_slice is not None
    assert correlation_mining_time_difficulty_slice >= -1
    assert correlation_mining_time_difficulty_slice <= 1

    return {
        INITIAL_BIT_DIFFICULTY_KEY: blockchain.initial_bit_difficulty,
        TARGET_BLOCK_MINING_TIME_KEY: blockchain.target_block_mining_time,
        ADJUSTMENT_BLOCK_INTERVAL_KEY: blockchain.adjustment_block_interval,
        NUMBER_BLOCKS_TO_ADD_KEY: blockchain.number_blocks_to_add,
        CLAMP_FACTOR_KEY: blockchain.clamp_factor,
        SMALLEST_BIT_DIFFICULTY_KEY: blockchain.smallest_bit_difficulty,
        NUMBER_BLOCKS_SLICE_KEY: number_blocks_slice,
        # todo should blockchain.num_blocks_slice,
        #  blockchain.average_mining_time_slice,
        #  blockchain.absolute_deviation_mining_time_average_from_target_slice etc.
        #  be created?

        # mining time
        AVERAGE_MINING_TIME_SLICE_KEY: average_mining_time_slice,
        ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: absolute_deviation_mining_time_average_from_target_slice,
        RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: relative_deviation_mining_time_average_from_target_slice,

        VARIANCE_MINING_TIME_SLICE_KEY: variance_mining_time_slice,
        STANDARD_DEVIATION_MINING_TIME_SLICE_KEY: standard_deviation_mining_time_slice,

        # bit difficulty
        AVERAGE_BIT_DIFFICULTY_SLICE_KEY: average_bit_difficulty_slice,
        ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: absolute_deviation_bit_difficulty_average_from_initial_slice,
        RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: relative_deviation_bit_difficulty_average_from_initial_slice,

        VARIANCE_BIT_DIFFICULTY_SLICE_KEY: variance_bit_difficulty_slice,
        STANDARD_DEVIATION_BIT_DIFFICULTY_SLICE_KEY: standard_deviation_bit_difficulty_slice,

        # mining time and bit difficulty
        COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY: covariance_mining_time_bit_difficulty_slice,
        CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY: correlation_mining_time_bit_difficulty_slice,

        # difficulty
        AVERAGE_DIFFICULTY_SLICE_KEY: average_difficulty_slice,
        ABSOLUTE_DEVIATION_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: absolute_deviation_difficulty_average_from_initial_slice,
        RELATIVE_DEVIATION_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: relative_deviation_difficulty_average_from_initial_slice,

        VARIANCE_DIFFICULTY_SLICE_KEY: variance_difficulty_slice,
        STANDARD_DEVIATION_DIFFICULTY_SLICE_KEY: standard_deviation_difficulty_slice,

        # mining time and difficulty
        COVARIANCE_MINING_TIME_DIFFICULTY_SLICE_KEY: covariance_mining_time_difficulty_slice,
        CORRELATION_MINING_TIME_DIFFICULTY_SLICE_KEY: correlation_mining_time_difficulty_slice,

        # zero mining time
        ZERO_MINING_TIME_BLOCKS_INDEXES_KEY: zero_mining_time_blocks_indexes,
        ZERO_MINING_TIME_BLOCKS_NUMBER_KEY: zero_mining_time_blocks_number,
        RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY: relative_zero_mining_time_blocks_number,
    }


def log_validity(blockchain) -> None:
    assert blockchain is not None, "Blockchain cannot be null"
    logger: logging.Logger = logging.getLogger()
    assert logger is not None, "Logger cannot be null"
    # is_blockchain_valid: bool = blockchain.is_chain_valid()  # todo should be a property?
    # assert is_blockchain_valid is not None, "Blockchain validity cannot be null"
    # if is_blockchain_valid:
    #     logger.info(f"Blockchain is valid: {is_blockchain_valid}")
    # else:
    #     logger.critical(f"Blockchain validity: {is_blockchain_valid}")


def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger
