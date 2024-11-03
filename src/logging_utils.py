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
    TARGET_BLOCK_MINING_TIME,
    SLICE_FACTOR,
    NUMBER_BLOCKS_TO_ADD,
    INITIAL_BIT_DIFFICULTY,
    ADJUSTMENT_BLOCK_INTERVAL,
    CLAMP_FACTOR,
    SMALLEST_BIT_DIFFICULTY,

    INITIAL_BIT_DIFFICULTY_KEY,
    NUMBER_BLOCKS_TO_ADD_KEY,

    SLICE_FACTOR_KEY,
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
    # ZERO_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_VARIANCE_MINING_TIME_BLOCKS_KEY,
    # ZERO_VARIANCE_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_STANDARD_DEVIATION_MINING_TIME_BLOCKS_KEY,
    # ZERO_STANDARD_DEVIATION_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_COVARIANCE_MINING_TIME_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_CORRELATION_MINING_TIME_BIT_DIFFICULTY_BLOCKS_KEY,
)

DEFAULT_PRECISION = 25


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
        slice_factor=SLICE_FACTOR,
    )

    logger.info(f"Blockchain statistics:")
    logger.info(f"")

    # logger.info(f"initial_bit_difficulty: {blockchain_stats["initial_bit_difficulty"]:.25f} bits")

    logger.info(create_log_message(INITIAL_BIT_DIFFICULTY_KEY, blockchain_stats, "bit"))
    logger.info(create_log_message(TARGET_BLOCK_MINING_TIME_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(ADJUSTMENT_BLOCK_INTERVAL_KEY, blockchain_stats, "block", precision=0))
    logger.info(create_log_message(CLAMP_FACTOR_KEY, blockchain_stats, "bit"))
    logger.info(create_log_message(SMALLEST_BIT_DIFFICULTY_KEY, blockchain_stats, "bit"))
    logger.info(f"")

    logger.info(create_log_message(NUMBER_BLOCKS_TO_ADD_KEY, blockchain_stats, "block", precision=0))
    # logger.info(f"")

    logger.info(create_log_message(SLICE_FACTOR_KEY, blockchain_stats, ""))
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

    # logger.info(f"")

    # logger.info(f"")

    logger.info(create_log_message(COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY, blockchain_stats, "second*bit"))
    logger.info(create_log_message(CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY, blockchain_stats, ""))
    logger.info(f"")

    logger.info(create_log_message(ZERO_MINING_TIME_BLOCKS_NUMBER_KEY, blockchain_stats, ""))
    logger.info(create_log_message(RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY, blockchain_stats, "%"))
    logger.info(f"")


def create_log_message(key: str, blockchain_stats: dict[str, float], unit: str,
                       precision: int = DEFAULT_PRECISION) -> str:
    return f"{key}: {blockchain_stats[key]:.{precision}f} {unit}"


def get_blockchain_statistics(blockchain, slice_factor):
    num_blocks_slice = int(len(blockchain.mining_times) / slice_factor)
    # Slice the lists to the num_blocks_slice length
    mining_times_slice = blockchain.mining_times[:num_blocks_slice]
    bit_difficulties_slice = blockchain.bit_difficulties[:num_blocks_slice]

    average_mining_time_slice = blockchain.get_average_mining_time(num_blocks=num_blocks_slice)
    # absolute_deviation_mining_time_average_from_target_slice = abs(average_mining_time_slice - TARGET_BLOCK_MINING_TIME)
    # relative_deviation_mining_time_average_from_target_slice = (absolute_deviation_mining_time_average_from_target_slice / TARGET_BLOCK_MINING_TIME) * 100.0
    absolute_deviation_mining_time_average_from_target_slice = abs(average_mining_time_slice - blockchain.target_block_mining_time)
    relative_deviation_mining_time_average_from_target_slice = (absolute_deviation_mining_time_average_from_target_slice / blockchain.target_block_mining_time) * 100.0

    average_bit_difficulty_slice = sum(bit_difficulties_slice) / num_blocks_slice
    # absolute_deviation_bit_difficulty_average_from_initial_slice = abs(average_bit_difficulty_slice - INITIAL_BIT_DIFFICULTY)
    # relative_deviation_bit_difficulty_average_from_initial_slice = (absolute_deviation_bit_difficulty_average_from_initial_slice / INITIAL_BIT_DIFFICULTY) * 100.0
    absolute_deviation_bit_difficulty_average_from_initial_slice = abs(average_bit_difficulty_slice - blockchain.initial_bit_difficulty)
    relative_deviation_bit_difficulty_average_from_initial_slice = (absolute_deviation_bit_difficulty_average_from_initial_slice / blockchain.initial_bit_difficulty) * 100.0

    variance_mining_time_slice = variance(mining_times_slice)
    variance_bit_difficulty_slice = variance(bit_difficulties_slice)
    standard_deviation_mining_time_slice = variance_mining_time_slice ** 0.5
    standard_deviation_bit_difficulty_slice = variance_bit_difficulty_slice ** 0.5
    covariance_mining_time_bit_difficulty_slice = covariance(mining_times_slice, bit_difficulties_slice)

    if standard_deviation_mining_time_slice == 0 or standard_deviation_bit_difficulty_slice == 0:
        correlation_mining_time_bit_difficulty_slice = 0
    else:
        correlation_mining_time_bit_difficulty_slice = (covariance_mining_time_bit_difficulty_slice /
                                                        (
                                                                standard_deviation_mining_time_slice * standard_deviation_bit_difficulty_slice))

    # Number of blocks mined with 0.0 seconds:
    zero_mining_time_blocks_number = sum(
        1 for time in blockchain.mining_times if time == 0.0) - 1  # -1 for the Genesis Block
    # relative_zero_mining_time_blocks_number = (zero_mining_time_blocks_number / NUMBER_BLOCKS_TO_ADD) * 100.0
    relative_zero_mining_time_blocks_number = (zero_mining_time_blocks_number / blockchain.number_blocks_to_add) * 100.0

    return {
        # INITIAL_BIT_DIFFICULTY_KEY: INITIAL_BIT_DIFFICULTY,
        # NUMBER_BLOCKS_TO_ADD_KEY: NUMBER_BLOCKS_TO_ADD, # todo it should be taken from the blockchain.num_blocks_to_add
        # SLICE_FACTOR_KEY: SLICE_FACTOR,
        # NUMBER_BLOCKS_SLICE_KEY: num_blocks_slice,
        # TARGET_BLOCK_MINING_TIME_KEY: TARGET_BLOCK_MINING_TIME,
        # ADJUSTMENT_BLOCK_INTERVAL_KEY: ADJUSTMENT_BLOCK_INTERVAL,
        # CLAMP_FACTOR_KEY: CLAMP_FACTOR,
        # SMALLEST_BIT_DIFFICULTY_KEY: SMALLEST_BIT_DIFFICULTY,

        # AVERAGE_MINING_TIME_SLICE_KEY: average_mining_time_slice,
        # ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: absolute_deviation_mining_time_average_from_target_slice,
        # RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: relative_deviation_mining_time_average_from_target_slice,

        # AVERAGE_BIT_DIFFICULTY_SLICE_KEY: average_bit_difficulty_slice,
        # ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: absolute_deviation_bit_difficulty_average_from_initial_slice,
        # RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: relative_deviation_bit_difficulty_average_from_initial_slice,


        INITIAL_BIT_DIFFICULTY_KEY: blockchain.initial_bit_difficulty,
        TARGET_BLOCK_MINING_TIME_KEY: blockchain.target_block_mining_time,
        ADJUSTMENT_BLOCK_INTERVAL_KEY: blockchain.adjustment_block_interval,
        NUMBER_BLOCKS_TO_ADD_KEY: blockchain.number_blocks_to_add,
        CLAMP_FACTOR_KEY: blockchain.clamp_factor,
        SMALLEST_BIT_DIFFICULTY_KEY: blockchain.smallest_bit_difficulty,
        SLICE_FACTOR_KEY: blockchain.slice_factor,
        NUMBER_BLOCKS_SLICE_KEY: num_blocks_slice, # todo should blockchain.num_blocks_slice be created?

        AVERAGE_MINING_TIME_SLICE_KEY: average_mining_time_slice, # todo should blockchain.average_mining_time_slice be created?
        ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: absolute_deviation_mining_time_average_from_target_slice, # todo should blockchain.absolute_deviation_mining_time_average_from_target_slice be created?
        RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: relative_deviation_mining_time_average_from_target_slice, # todo should blockchain.relative_deviation_mining_time_average_from_target_slice be created?

        AVERAGE_BIT_DIFFICULTY_SLICE_KEY: average_bit_difficulty_slice, # todo should blockchain.average_bit_difficulty_slice be created?
        ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: absolute_deviation_bit_difficulty_average_from_initial_slice, # todo should blockchain.absolute_deviation_bit_difficulty_average_from_initial_slice be created?
        RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: relative_deviation_bit_difficulty_average_from_initial_slice, # todo should blockchain.relative_deviation_bit_difficulty_average_from_initial_slice be created?

        VARIANCE_MINING_TIME_SLICE_KEY: variance_mining_time_slice, # todo should blockchain.variance_mining_time_slice be created?
        STANDARD_DEVIATION_MINING_TIME_SLICE_KEY: standard_deviation_mining_time_slice, # todo should blockchain.standard_deviation_mining_time_slice be created?

        VARIANCE_BIT_DIFFICULTY_SLICE_KEY: variance_bit_difficulty_slice, # todo should blockchain.variance_bit_difficulty_slice be created?
        STANDARD_DEVIATION_BIT_DIFFICULTY_SLICE_KEY: standard_deviation_bit_difficulty_slice, # todo should blockchain.standard_deviation_bit_difficulty_slice be created?

        COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY: covariance_mining_time_bit_difficulty_slice, # todo should blockchain.covariance_mining_time_bit_difficulty_slice be created?
        CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY: correlation_mining_time_bit_difficulty_slice, # todo should blockchain.correlation_mining_time_bit_difficulty_slice be created?

        ZERO_MINING_TIME_BLOCKS_NUMBER_KEY: zero_mining_time_blocks_number, # todo should blockchain.zero_mining_time_blocks_number be created?
        RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY: relative_zero_mining_time_blocks_number, # todo should blockchain.relative_zero_mining_time_blocks_number be created?


    }


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
