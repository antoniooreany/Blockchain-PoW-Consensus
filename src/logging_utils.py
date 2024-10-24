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
    STATISTICS_PARTITION_INTERVAL_FACTOR,
    NUMBER_BLOCKS_TO_ADD,
    INITIAL_BIT_DIFFICULTY,
    ADJUSTMENT_INTERVAL,
    CLAMP_FACTOR,
    SMALLEST_BIT_DIFFICULTY,

    INITIAL_BIT_DIFFICULTY_KEY,
    NUMBER_BLOCKS_TO_ADD_KEY,
    STATISTICS_PARTITION_INTERVAL_FACTOR_KEY,
    NUMBER_BLOCKS_SLICE_KEY,
    TARGET_BLOCK_MINING_TIME_KEY,
    ADJUSTMENT_INTERVAL_KEY,
    CLAMP_FACTOR_KEY,
    SMALLEST_BIT_DIFFICULTY_KEY,
    AVERAGE_MINING_TIME_KEY,
    ABSOLUTE_DEVIATION_FROM_TARGET_MINING_TIME_KEY,
    RELATIVE_DEVIATION_FROM_TARGET_MINING_TIME_KEY,
    AVERAGE_BIT_DIFFICULTY_KEY,
    # ABSOLUTE_DEVIATION_BIT_DIFFICULTY_KEY,
    # RELATIVE_DEVIATION_BIT_DIFFICULTY_KEY,
    VARIANCE_MINING_TIME_KEY,
    VARIANCE_BIT_DIFFICULTY_KEY,
    STANDARD_DEVIATION_MINING_TIME_KEY,
    STANDARD_DEVIATION_BIT_DIFFICULTY_KEY,
    COVARIANCE_MINING_TIME_BIT_DIFFICULTY_KEY,
    CORRELATION_MINING_TIME_BIT_DIFFICULTY_KEY,
    ZERO_MINING_TIME_BLOCKS_KEY, RELATIVE_ZERO_MINING_TIME_BLOCKS_KEY,
    # ZERO_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_VARIANCE_MINING_TIME_BLOCKS_KEY,
    # ZERO_VARIANCE_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_STANDARD_DEVIATION_MINING_TIME_BLOCKS_KEY,
    # ZERO_STANDARD_DEVIATION_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_COVARIANCE_MINING_TIME_BIT_DIFFICULTY_BLOCKS_KEY,
    # ZERO_CORRELATION_MINING_TIME_BIT_DIFFICULTY_BLOCKS_KEY,
)


# INITIAL_BIT_DIFFICULTY_KEY = "initial_bit_difficulty"
# NUMBER_BLOCKS_TO_ADD_KEY = "number_of_blocks_to_add"
# STATISTICS_PARTITION_INTERVAL_FACTOR_KEY = "statistics_partition_interval_factor"


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
    # (
    #     initial_bit_difficulty,
    #     number_of_blocks_to_add,
    #     statistics_partition_interval_factor,
    #     num_blocks_slice,
    #     target_block_mining_time,
    #     adjustment_interval,
    #     clamp_factor,
    #     smallest_bit_difficulty,
    #
    #     average_mining_time,
    #     absolute_deviation_from_target_mining_time,
    #     relative_deviation_from_target_mining_time,
    #
    #     average_bit_difficulty,
    #     # absolute_deviation_bit_difficulty,
    #     # relative_deviation_bit_difficulty,
    #
    #     variance_mining_time,
    #     variance_bit_difficulty,
    #
    #     standard_deviation_mining_time,
    #     standard_deviation_bit_difficulty,
    #
    #     covariance_mining_time_bit_difficulty,
    #
    #     correlation_mining_time_bit_difficulty,
    #
    #     zero_mining_time_blocks,
    #
    # ) \

    blockchain_stats = get_blockchain_statistics(
        blockchain=blockchain,
        statistics_partition_interval_factor=STATISTICS_PARTITION_INTERVAL_FACTOR,
    )

    logger.info(f"Blockchain statistics:")
    logger.info(f"")

    # logger.info(f"initial_bit_difficulty: {blockchain_stats["initial_bit_difficulty"]:.25f} bits")

    logger.info(create_log_message(INITIAL_BIT_DIFFICULTY_KEY, blockchain_stats, "bits"))
    logger.info(create_log_message(TARGET_BLOCK_MINING_TIME_KEY, blockchain_stats, "seconds"))
    logger.info(create_log_message(ADJUSTMENT_INTERVAL_KEY, blockchain_stats, "seconds"))
    logger.info(create_log_message(CLAMP_FACTOR_KEY, blockchain_stats, "bits"))
    logger.info(create_log_message(SMALLEST_BIT_DIFFICULTY_KEY, blockchain_stats, "bits"))
    logger.info(f"")

    logger.info(create_log_message(NUMBER_BLOCKS_TO_ADD_KEY, blockchain_stats, ""))
    logger.info(f"")

    logger.info(create_log_message(STATISTICS_PARTITION_INTERVAL_FACTOR_KEY, blockchain_stats, ""))
    logger.info(create_log_message(NUMBER_BLOCKS_SLICE_KEY, blockchain_stats, ""))
    logger.info(f"")

    # todo for the statistical partition
    logger.info(create_log_message(AVERAGE_MINING_TIME_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(ABSOLUTE_DEVIATION_FROM_TARGET_MINING_TIME_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(RELATIVE_DEVIATION_FROM_TARGET_MINING_TIME_KEY, blockchain_stats, "%"))
    logger.info(f"")

    logger.info(create_log_message(AVERAGE_BIT_DIFFICULTY_KEY, blockchain_stats, "bits"))
    # logger.info(create_log_message(ABSOLUTE_DEVIATION_BIT_DIFFICULTY_KEY, blockchain_stats, "bit"))
    # logger.info(create_log_message(RELATIVE_DEVIATION_BIT_DIFFICULTY_KEY, blockchain_stats, "%"))
    logger.info(f"")

    logger.info(create_log_message(VARIANCE_MINING_TIME_KEY, blockchain_stats, "second*second"))
    logger.info(create_log_message(VARIANCE_BIT_DIFFICULTY_KEY, blockchain_stats, "bit*bit"))
    logger.info(f"")

    logger.info(create_log_message(STANDARD_DEVIATION_MINING_TIME_KEY, blockchain_stats, "second"))
    logger.info(create_log_message(STANDARD_DEVIATION_BIT_DIFFICULTY_KEY, blockchain_stats, "bits"))
    logger.info(f"")

    logger.info(create_log_message(COVARIANCE_MINING_TIME_BIT_DIFFICULTY_KEY, blockchain_stats, "second*bit"))
    logger.info(create_log_message(CORRELATION_MINING_TIME_BIT_DIFFICULTY_KEY, blockchain_stats, ""))
    logger.info(f"")

    logger.info(create_log_message(ZERO_MINING_TIME_BLOCKS_KEY, blockchain_stats, ""))
    logger.info(create_log_message(RELATIVE_ZERO_MINING_TIME_BLOCKS_KEY, blockchain_stats, "%"))
    logger.info(f"")

    # logger.info(f"Inital bit difficulty: {initial_bit_difficulty:.25f} bits")
    # logger.info(f"Target block mining time: {target_block_mining_time:.25f} seconds")
    #
    # logger.info(f"Adjustment interval: {adjustment_interval:.25f} seconds")
    # logger.info(f"Clamp factor: {clamp_factor:.25f} ")
    # logger.info(f"Smallest bit difficulty: {smallest_bit_difficulty:.25f} bits")
    # logger.info(f"")
    #
    # logger.info(f"Number of blocks to add: {NUMBER_BLOCKS_TO_ADD}")
    # logger.info(f"")
    #
    # # logger.info(f"Number of blocks in the statistical partition: {num_blocks_slice}")
    # logger.info(f"Statistics partition interval factor: {statistics_partition_interval_factor}")
    # logger.info(f"Number of blocks in the statistical partition: {num_blocks_slice}")
    # logger.info(f"")
    #
    # logger.info(f"Average mining time of the statistical partition: "
    #             f"{average_mining_time: .25f} seconds")
    # logger.info(f"Absolute deviation of the average from the target block time of the statistical partition: "
    #             f"{absolute_deviation_from_target_mining_time: .25f} seconds")
    # logger.info(f"Relative deviation of the average from the target block time of the statistical partition: "
    #             f"{relative_deviation_from_target_mining_time: .25f} %")
    # logger.info(f"")
    #
    # logger.info(f"Average bit difficulty of the statistical partition: "
    #             f"{average_bit_difficulty: .25f} bits")
    # # logger.info(f"Absolute deviation from the bit difficulty of the statistical partition: "
    # #             f"{absolute_deviation_bit_difficulty: .25f} bits")
    # # logger.info(f"Relative deviation from the bit difficulty of the statistical partition: "
    # #             f"{relative_deviation_bit_difficulty: .25f} %")
    # logger.info(f"")
    #
    # logger.info(f"Variance of the mining time of the statistical partition: "
    #             f"{variance_mining_time: .25f}")
    # logger.info(f"Variance of the bit difficulty of the statistical partition: "
    #             f"{variance_bit_difficulty: .25f}")
    #
    # logger.info(f"Standard deviation of the mining time of the statistical partition: "
    #             f"{standard_deviation_mining_time: .25f}")
    # logger.info(f"Standard deviation of the bit difficulty of the statistical partition: "
    #             f"{standard_deviation_bit_difficulty: .25f}")
    #
    # logger.info(f"Covariance of the mining time and the bit difficulty of the statistical partition: "
    #             f"{covariance_mining_time_bit_difficulty: .25f}")
    #
    # logger.info(f"Correlation of the mining time and the bit difficulty of the statistical partition: "
    #             f"{correlation_mining_time_bit_difficulty: .25f}")
    #
    # logger.info(f"")
    #
    # logger.info(f"Number of blocks mined with 0.0 seconds: "
    #             f"{zero_mining_time_blocks - 1}")  # -1 for the Genesis Block
    # logger.info(f"Relative number of blocks mined with 0.0 seconds: "
    #             f"{((zero_mining_time_blocks - 1) / NUMBER_BLOCKS_TO_ADD) * 100:.25f} %")
    # logger.info(f"")

    # logger.info(f"{INITIAL_BIT_DIFFICULTY_KEY}: {blockchain_stats[INITIAL_BIT_DIFFICULTY_KEY]:.25f} bits")
    # logger.info(f"{TARGET_BLOCK_MINING_TIME_KEY}: {blockchain_stats[TARGET_BLOCK_MINING_TIME_KEY]:.25f} seconds")


def create_log_message(key: str, blockchain_stats: dict[str, float], unit: str) -> str:
    return f"{key}: {blockchain_stats[key]:.25f}, {unit}"


def get_blockchain_statistics(blockchain, statistics_partition_interval_factor):
    num_blocks_slice = int(len(blockchain.mining_times) / statistics_partition_interval_factor)
    # Slice the lists to the num_blocks_slice length
    mining_times_slice = blockchain.mining_times[:num_blocks_slice]
    bit_difficulties_slice = blockchain.bit_difficulties[:num_blocks_slice]

    average_mining_time = blockchain.get_average_mining_time(num_blocks=num_blocks_slice)
    absolute_deviation_from_target_mining_time = abs(average_mining_time - TARGET_BLOCK_MINING_TIME)
    relative_deviation_from_target_mining_time = (
                                                         absolute_deviation_from_target_mining_time / TARGET_BLOCK_MINING_TIME) * 100.0

    average_bit_difficulty = sum(bit_difficulties_slice) / num_blocks_slice
    # absolute_deviation_bit_difficulty = abs(average_bit_difficulty - blockchain.bit_difficulties[-1])
    # relative_deviation_bit_difficulty = (
    #                                             absolute_deviation_bit_difficulty / blockchain.bit_difficulties[
    #                                         -1]) * 100.0

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
    zero_mining_time_blocks = sum(1 for time in blockchain.mining_times if time == 0.0) - 1  # -1 for the Genesis Block
    relative_zero_mining_time_blocks = (zero_mining_time_blocks / NUMBER_BLOCKS_TO_ADD) * 100.0

    # return (
    #     INITIAL_BIT_DIFFICULTY,
    #     NUMBER_BLOCKS_TO_ADD,
    #     STATISTICS_PARTITION_INTERVAL_FACTOR,
    #     num_blocks_slice,
    #     TARGET_BLOCK_MINING_TIME,
    #     ADJUSTMENT_INTERVAL,
    #     CLAMP_FACTOR,
    #     SMALLEST_BIT_DIFFICULTY,
    #
    #     average_mining_time,
    #     absolute_deviation_from_target_mining_time,
    #     relative_deviation_from_target_mining_time,
    #
    #     average_bit_difficulty,
    #     # absolute_deviation_bit_difficulty,
    #     # relative_deviation_bit_difficulty,
    #
    #     variance_mining_time,
    #     variance_bit_difficulty,
    #
    #     standard_deviation_mining_time,
    #     standard_deviation_bit_difficulty,
    #
    #     covariance_mining_time_bit_difficulty,
    #
    #     correlation_mining_time_bit_difficulty,
    #
    #     zero_mining_time_blocks,
    # )

    return {
        INITIAL_BIT_DIFFICULTY_KEY: INITIAL_BIT_DIFFICULTY,
        NUMBER_BLOCKS_TO_ADD_KEY: NUMBER_BLOCKS_TO_ADD,
        STATISTICS_PARTITION_INTERVAL_FACTOR_KEY: STATISTICS_PARTITION_INTERVAL_FACTOR,
        NUMBER_BLOCKS_SLICE_KEY: num_blocks_slice,
        TARGET_BLOCK_MINING_TIME_KEY: TARGET_BLOCK_MINING_TIME,
        ADJUSTMENT_INTERVAL_KEY: ADJUSTMENT_INTERVAL,
        CLAMP_FACTOR_KEY: CLAMP_FACTOR,
        SMALLEST_BIT_DIFFICULTY_KEY: SMALLEST_BIT_DIFFICULTY,
        AVERAGE_MINING_TIME_KEY: average_mining_time,
        ABSOLUTE_DEVIATION_FROM_TARGET_MINING_TIME_KEY: absolute_deviation_from_target_mining_time,
        RELATIVE_DEVIATION_FROM_TARGET_MINING_TIME_KEY: relative_deviation_from_target_mining_time,
        AVERAGE_BIT_DIFFICULTY_KEY: average_bit_difficulty,
        VARIANCE_MINING_TIME_KEY: variance_mining_time,
        VARIANCE_BIT_DIFFICULTY_KEY: variance_bit_difficulty,
        STANDARD_DEVIATION_MINING_TIME_KEY: standard_deviation_mining_time,
        STANDARD_DEVIATION_BIT_DIFFICULTY_KEY: standard_deviation_bit_difficulty,
        COVARIANCE_MINING_TIME_BIT_DIFFICULTY_KEY: covariance_mining_time_bit_difficulty,
        CORRELATION_MINING_TIME_BIT_DIFFICULTY_KEY: correlation_mining_time_bit_difficulty,
        ZERO_MINING_TIME_BLOCKS_KEY: zero_mining_time_blocks,
        RELATIVE_ZERO_MINING_TIME_BLOCKS_KEY: relative_zero_mining_time_blocks,

        # "number_of_blocks_to_add": NUMBER_BLOCKS_TO_ADD,
        # "statistics_partition_interval_factor": STATISTICS_PARTITION_INTERVAL_FACTOR,
        # "num_blocks_slice": num_blocks_slice,
        # "target_block_mining_time": TARGET_BLOCK_MINING_TIME,
        # "adjustment_interval": ADJUSTMENT_INTERVAL,
        # "clamp_factor": CLAMP_FACTOR,
        # "smallest_bit_difficulty": SMALLEST_BIT_DIFFICULTY,
        # "average_mining_time": average_mining_time,
        # "absolute_deviation_from_target_mining_time": absolute_deviation_from_target_mining_time,
        # "relative_deviation_from_target_mining_time": relative_deviation_from_target_mining_time,
        # "average_bit_difficulty": average_bit_difficulty,
        # "variance_mining_time": variance_mining_time,
        # "variance_bit_difficulty": variance_bit_difficulty,
        # "standard_deviation_mining_time": standard_deviation_mining_time,
        # "standard_deviation_bit_difficulty": standard_deviation_bit_difficulty,
        # "covariance_mining_time_bit_difficulty": covariance_mining_time_bit_difficulty,
        # "correlation_mining_time_bit_difficulty": correlation_mining_time_bit_difficulty,
        # "zero_mining_time_blocks": zero_mining_time_blocks,
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
