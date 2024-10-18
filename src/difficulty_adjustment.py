#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a difficulty_adjustment.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# difficulty_adjustment.py
import math

from helpers import clamp


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
