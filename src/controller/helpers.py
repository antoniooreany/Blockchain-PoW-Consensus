# #   Copyright (c) 2024, Anton Gorshkov
# #   All rights reserved.
# #   This code is for a helpers.py and its unit tests.
# #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
#
# import logging
# import math
# import time
#
# from src.model.block import Block
#
#
# # def create_genesis_block(blockchain, initial_bit_difficulty: float) -> Block: # todo redundant method, substituted by the Block constructor
# #     genesis_block = Block(
# #         # bit_difficulty=initial_bit_difficulty,
# #         bit_difficulty=0, #  todo implement it in the generic case, having bit_difficulty=0
# #         index=0,
# #         timestamp=time.time(),
# #         data=GENESIS_BLOCK_DATA,
# #         previous_hash=GENESIS_BLOCK_PREVIOUS_HASH,
# #     )
# #     genesis_block.hash = genesis_block.calculate_hash()
# #
# #     blockchain.bit_difficulties.append(initial_bit_difficulty)  # todo if 0 is added, the 1st element is 0,
# #     # todo but the 0th element is initial_bit_difficulty. Add 0 to the 0th element
# #     blockchain.bit_difficulties.append(
# #         initial_bit_difficulty)  # todo is it correct to append it twice? find a better approach
# #
# #     return genesis_block
#
#
# def add_blocks(blockchain, number_of_blocks_to_add: int, ):
#     for index in range(1, number_of_blocks_to_add + 1):  # add number_of_blocks blocks after the Genesis Block
#         block = Block(bit_difficulty=blockchain.bit_difficulties[-1], index=index, timestamp=time.time(),
#                       data=f"Block {index} Data")
#         blockchain.add_block(block, blockchain.clamp_factor, blockchain.smallest_bit_difficulty)
#
#
# def clamp(log_adjustment_factor: float, clamp_factor: float) -> float:
#     if log_adjustment_factor > clamp_factor:
#         log_adjustment_factor = clamp_factor
#     elif log_adjustment_factor < -clamp_factor:
#         log_adjustment_factor = -clamp_factor
#     return log_adjustment_factor
#
#
# def collect_filtered_bit_difficulties(blockchain, adjustment_interval):  # todo should it be done?
#     filtered_bit_difficulties = []
#     for i, difficulty in enumerate(blockchain.bit_difficulties):
#         if (i + 1) % adjustment_interval != 0:
#             # if i % adjustment_interval != 0:
#             # if (i - 1) % adjustment_interval != 0:
#             filtered_bit_difficulties.append(difficulty)
#     return filtered_bit_difficulties
#
#
# def adjust_difficulty(blockchain, clamp_factor, smallest_bit_difficulty):
#     # Check if the number of blocks is a multiple of the adjustment interval plus 1
#     if (len(blockchain.blocks) - 1) % blockchain.adjustment_block_interval == 0:
#         average_mining_time = blockchain.get_average_mining_time(blockchain.adjustment_block_interval)
#         logging.debug(f"Average mining time: {average_mining_time:.25f} seconds")
#         reversed_adjustment_factor = average_mining_time / blockchain.target_block_mining_time
#
#         logging.debug(f"Reversed adjustment factor: {reversed_adjustment_factor:.25f}")
#         last_bit_difficulty = blockchain.bit_difficulties[-1]
#
#         if reversed_adjustment_factor > 0:
#             log_adjustment_factor = math.log2(reversed_adjustment_factor)
#             clamped_log_adjustment_factor = clamp(log_adjustment_factor, clamp_factor)
#             new_difficulty = max(smallest_bit_difficulty, last_bit_difficulty - clamped_log_adjustment_factor)
#         else:
#             new_difficulty = smallest_bit_difficulty
#
#         # Update the last element instead of appending
#         blockchain.bit_difficulties[-1] = new_difficulty


import logging
import math
import time

from src.constants import AVERAGE_MINING_TIME_COLOR, AVERAGE_MINING_TIME_SLICE_KEY, \
    AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY
from src.model.block import Block

def add_blocks(blockchain, number_of_blocks_to_add: int):
    for index in range(1, number_of_blocks_to_add + 1):
        block = Block(bit_difficulty=blockchain.bit_difficulties[-1], index=index, timestamp=time.time(), data=f"Block {index} Data")
        blockchain.add_block(block, blockchain.clamp_factor, blockchain.smallest_bit_difficulty)

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

def adjust_difficulty(blockchain, clamp_factor, smallest_bit_difficulty,
                      ):
    if (len(blockchain.blocks) - 1) % blockchain.adjustment_block_interval == 0:
        average_mining_time_adjustment_interval = blockchain.get_average_mining_time(blockchain.adjustment_block_interval)
        logging.debug(f"{AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY}: {average_mining_time_adjustment_interval:.25f} seconds")
        reversed_adjustment_factor = average_mining_time_adjustment_interval / blockchain.target_block_mining_time

        logging.debug(f"Reversed adjustment factor: {reversed_adjustment_factor:.25f}")
        last_bit_difficulty = blockchain.bit_difficulties[-1]

        if reversed_adjustment_factor > 0:
            log_adjustment_factor = math.log2(reversed_adjustment_factor)
            clamped_log_adjustment_factor = clamp(log_adjustment_factor, clamp_factor)
            new_difficulty = max(smallest_bit_difficulty, last_bit_difficulty - clamped_log_adjustment_factor)
        else:
            new_difficulty = smallest_bit_difficulty

        blockchain.bit_difficulties[-1] = new_difficulty