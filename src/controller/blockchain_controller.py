#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a logging_utils.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
import time
from statistics import variance

import numpy as np

from src.model.block import Block
from src.utils.constants import INITIAL_BIT_DIFFICULTY_KEY, TARGET_BLOCK_MINING_TIME_KEY, ADJUSTMENT_BLOCK_INTERVAL_KEY, \
    NUMBER_BLOCKS_TO_ADD_KEY, CLAMP_FACTOR_KEY, SMALLEST_BIT_DIFFICULTY_KEY, NUMBER_BLOCKS_SLICE_KEY, \
    AVERAGE_MINING_TIME_SLICE_KEY, ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY, \
    RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY, AVERAGE_BIT_DIFFICULTY_SLICE_KEY, \
    ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY, \
    RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY, VARIANCE_MINING_TIME_SLICE_KEY, \
    STANDARD_DEVIATION_MINING_TIME_SLICE_KEY, VARIANCE_BIT_DIFFICULTY_SLICE_KEY, \
    STANDARD_DEVIATION_BIT_DIFFICULTY_SLICE_KEY, COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY, \
    CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY, ZERO_MINING_TIME_BLOCKS_NUMBER_KEY, \
    RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY


def get_blockchain_statistics(blockchain, slice_factor):
    num_blocks_slice = int(len(blockchain.mining_times) / slice_factor)
    # Slice the lists to the num_blocks_slice length
    mining_times_slice = blockchain.mining_times[:num_blocks_slice]
    bit_difficulties_slice = blockchain.bit_difficulties[:num_blocks_slice]

    average_mining_time_slice = blockchain.get_average_mining_time(num_last_blocks=num_blocks_slice)
    absolute_deviation_mining_time_average_from_target_slice = abs(
        average_mining_time_slice - blockchain.target_block_mining_time)
    relative_deviation_mining_time_average_from_target_slice = (
                                                                       absolute_deviation_mining_time_average_from_target_slice / blockchain.target_block_mining_time) * 100.0

    average_bit_difficulty_slice = sum(bit_difficulties_slice) / num_blocks_slice
    absolute_deviation_bit_difficulty_average_from_initial_slice = abs(
        average_bit_difficulty_slice - blockchain.initial_bit_difficulty)
    relative_deviation_bit_difficulty_average_from_initial_slice = (
                                                                           absolute_deviation_bit_difficulty_average_from_initial_slice / blockchain.initial_bit_difficulty) * 100.0

    variance_mining_time_slice = variance(mining_times_slice)
    variance_bit_difficulty_slice = variance(bit_difficulties_slice)
    standard_deviation_mining_time_slice = variance_mining_time_slice ** 0.5
    standard_deviation_bit_difficulty_slice = variance_bit_difficulty_slice ** 0.5
    # covariance_mining_time_bit_difficulty_slice = covariance(mining_times_slice, bit_difficulties_slice)
    covariance_mining_time_bit_difficulty_slice = np.cov(mining_times_slice, bit_difficulties_slice)[0, 1]

    if standard_deviation_mining_time_slice == 0 or standard_deviation_bit_difficulty_slice == 0:
        correlation_mining_time_bit_difficulty_slice = 0
    else:
        correlation_mining_time_bit_difficulty_slice = (covariance_mining_time_bit_difficulty_slice /
                                                        (
                                                                standard_deviation_mining_time_slice * standard_deviation_bit_difficulty_slice))

    # Number of blocks mined with 0.0 seconds:
    zero_mining_time_blocks_number = sum(
        1 for time in blockchain.mining_times if time == 0.0) - 1  # -1 for the Genesis Block
    relative_zero_mining_time_blocks_number = (zero_mining_time_blocks_number / blockchain.number_blocks_to_add) * 100.0

    return {
        INITIAL_BIT_DIFFICULTY_KEY: blockchain.initial_bit_difficulty,
        TARGET_BLOCK_MINING_TIME_KEY: blockchain.target_block_mining_time,
        ADJUSTMENT_BLOCK_INTERVAL_KEY: blockchain.adjustment_block_interval,
        NUMBER_BLOCKS_TO_ADD_KEY: blockchain.number_blocks_to_add,
        CLAMP_FACTOR_KEY: blockchain.clamp_factor,
        SMALLEST_BIT_DIFFICULTY_KEY: blockchain.smallest_bit_difficulty,
        # SLICE_FACTOR_KEY: blockchain.slice_factor,
        NUMBER_BLOCKS_SLICE_KEY: num_blocks_slice,  # todo should blockchain.num_blocks_slice be created?

        AVERAGE_MINING_TIME_SLICE_KEY: average_mining_time_slice,
        # todo should blockchain.average_mining_time_slice be created?
        ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: absolute_deviation_mining_time_average_from_target_slice,
        # todo should blockchain.absolute_deviation_mining_time_average_from_target_slice be created?
        RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY: relative_deviation_mining_time_average_from_target_slice,
        # todo should blockchain.relative_deviation_mining_time_average_from_target_slice be created?

        AVERAGE_BIT_DIFFICULTY_SLICE_KEY: average_bit_difficulty_slice,
        # todo should blockchain.average_bit_difficulty_slice be created?
        ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: absolute_deviation_bit_difficulty_average_from_initial_slice,
        # todo should blockchain.absolute_deviation_bit_difficulty_average_from_initial_slice be created?
        RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY: relative_deviation_bit_difficulty_average_from_initial_slice,
        # todo should blockchain.relative_deviation_bit_difficulty_average_from_initial_slice be created?

        VARIANCE_MINING_TIME_SLICE_KEY: variance_mining_time_slice,
        # todo should blockchain.variance_mining_time_slice be created?
        STANDARD_DEVIATION_MINING_TIME_SLICE_KEY: standard_deviation_mining_time_slice,
        # todo should blockchain.standard_deviation_mining_time_slice be created?

        VARIANCE_BIT_DIFFICULTY_SLICE_KEY: variance_bit_difficulty_slice,
        # todo should blockchain.variance_bit_difficulty_slice be created?
        STANDARD_DEVIATION_BIT_DIFFICULTY_SLICE_KEY: standard_deviation_bit_difficulty_slice,
        # todo should blockchain.standard_deviation_bit_difficulty_slice be created?

        COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY: covariance_mining_time_bit_difficulty_slice,
        # todo should blockchain.covariance_mining_time_bit_difficulty_slice be created?
        CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY: correlation_mining_time_bit_difficulty_slice,
        # todo should blockchain.correlation_mining_time_bit_difficulty_slice be created?

        ZERO_MINING_TIME_BLOCKS_NUMBER_KEY: zero_mining_time_blocks_number,
        # todo should blockchain.zero_mining_time_blocks_number be created?
        RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY: relative_zero_mining_time_blocks_number,
        # todo should blockchain.relative_zero_mining_time_blocks_number be created?
    }


def add_blocks(blockchain, number_of_blocks_to_add: int):
    for index in range(1, number_of_blocks_to_add + 1):
        block = Block(bit_difficulty=blockchain.bit_difficulties[-1], index=index, timestamp=time.time(),
                      data=f"Block {index} Data")
        blockchain.add_block(block, blockchain.clamp_factor, blockchain.smallest_bit_difficulty)


def clamp(log_adjustment_factor: float, clamp_factor: float) -> float:
    if log_adjustment_factor > clamp_factor:
        log_adjustment_factor = clamp_factor
    elif log_adjustment_factor < -clamp_factor:
        log_adjustment_factor = -clamp_factor
    return log_adjustment_factor
