#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a helpers.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math
import time

from block import Block
from logging_utils import log_mined_block


def create_genesis_block():
    genesis_block = Block(0, time.time(), "Genesis Block", "0")
    genesis_block.hash = genesis_block.calculate_hash()
    log_mined_block(genesis_block)
    return genesis_block


def add_blocks(blockchain, number_of_blocks: int, clamp_factor, smallest_bit_difficulty):
    for i in range(1, number_of_blocks):
        block = Block(i, time.time(), f"Block {i} Data")
        blockchain.add_block(block, clamp_factor, smallest_bit_difficulty)


# helpers.py
def clamp(log_adjustment_factor: float, clamp_factor: float) -> float:
    if log_adjustment_factor > clamp_factor:
        log_adjustment_factor = clamp_factor
    elif log_adjustment_factor < -clamp_factor:
        log_adjustment_factor = -clamp_factor
    return log_adjustment_factor


def collect_filtered_bit_difficulties(blockchain, adjustment_interval):
    filtered_bit_difficulties = []
    for i, difficulty in enumerate(blockchain.bit_difficulties):
        if (i + 1) % adjustment_interval != 0:
            filtered_bit_difficulties.append(difficulty)
    return filtered_bit_difficulties


def adjust_difficulty(blockchain, clamp_factor, smallest_bit_difficulty):
    average_mining_time = blockchain.get_average_mining_time(blockchain.adjustment_interval)
    adjustment_factor = average_mining_time / blockchain.target_block_mining_time

    last_bit_difficulty = blockchain.bit_difficulties[-1]

    if adjustment_factor > 0:
        log_adjustment_factor = math.log2(adjustment_factor)
        clamped_log_adjustment_factor = clamp(log_adjustment_factor, clamp_factor)
        new_difficulty = max(smallest_bit_difficulty, last_bit_difficulty - clamped_log_adjustment_factor)
    else:
        new_difficulty = smallest_bit_difficulty

    blockchain.bit_difficulties.append(new_difficulty)
