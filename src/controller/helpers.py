#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a helpers.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
import math
import time

from src.constants import AVERAGE_MINING_TIME_COLOR, AVERAGE_MINING_TIME_SLICE_KEY, \
    AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY, REVERSED_ADJUSTMENT_FACTOR_KEY, DEFAULT_PRECISION
from src.model.block import Block
# from src.model.blockchain import Blockchain


# def add_blocks(
#         blockchain: 'Blockchain',  # type hint for blockchain: Unresolved reference 'Blockchain' # todo fix circular import
#         number_of_blocks_to_add: int  # type hint for number_of_blocks_to_add
# ) -> None:  # type hint for return value
#     """
#     Add blocks to the blockchain.
#
#     Args:
#         blockchain (Blockchain): The blockchain to add blocks to.
#         number_of_blocks_to_add (int): The number of blocks to add.
#
#     Returns:
#         None
#     """
#     for index in range(1, number_of_blocks_to_add + 1):
#         block = Block(
#             bit_difficulty=blockchain.bit_difficulties[-1],
#             index=index,
#             data=f"Block {index} Data",  # todo mock data is used, it should be replaced with real data
#             timestamp=time.time(),
#             previous_hash=blockchain.blocks[-1].hash if blockchain.blocks else None,
#         )
#         blockchain.add_block(block, blockchain.clamp_factor, blockchain.smallest_bit_difficulty)


def clamp(
        bit_adjustment_factor: float,  # type hint for bit_adjustment_factor
        bit_clamp_factor: float  # type hint for bit_clamp_factor
) -> float:  # type hint for return value
    """
    Clamp the bit adjustment factor within the range determined by the bit clamp factor.

    Args:
        bit_adjustment_factor (float): The factor by which the bit difficulty is adjusted.
        bit_clamp_factor (float): The maximum allowable adjustment factor.

    Returns:
        float: The clamped bit adjustment factor.
    """
    if bit_adjustment_factor > bit_clamp_factor:
        bit_adjustment_factor = bit_clamp_factor
    elif bit_adjustment_factor < -bit_clamp_factor:
        bit_adjustment_factor = -bit_clamp_factor
    return bit_adjustment_factor


# def adjust_difficulty(
#         blockchain: 'Blockchain',  # type hint for blockchain: Unresolved reference 'Blockchain' # todo fix circular import
#         bit_clamp_factor: float,  # type hint for bit_clamp_factor
#         smallest_bit_difficulty: float  # type hint for smallest_bit_difficulty
# ) -> None:  # type hint for return value
#     """
#     Adjust the difficulty of the blockchain.
#
#     This function is called every time a new block is added to the blockchain.
#     It checks if the number of blocks in the blockchain is a multiple of the
#     adjustment block interval. If it is, it calculates the average mining time
#     of the last adjustment block interval and adjusts the difficulty of the
#     blockchain accordingly.
#
#     Args:
#         blockchain (Blockchain): The blockchain object.
#         bit_clamp_factor (float): The maximum allowable adjustment factor.
#         smallest_bit_difficulty (float): The smallest bit difficulty that we can adjust to.
#
#     Returns:
#         None
#     """
#     if (len(blockchain.blocks) - 1) % blockchain.adjustment_block_interval == 0:
#         # Calculate the average mining time of the last adjustment block interval
#         average_mining_time_adjustment_interval: float = blockchain.get_average_mining_time(
#             blockchain.adjustment_block_interval)
#         # Calculate the reversed adjustment factor
#         reversed_adjustment_factor: float = average_mining_time_adjustment_interval / blockchain.target_block_mining_time
#
#         # Log the average mining time and the reversed adjustment factor
#         logging.debug(f"{AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY}: "
#                       f"{average_mining_time_adjustment_interval:.{DEFAULT_PRECISION}f} seconds")
#         logging.debug(f"{REVERSED_ADJUSTMENT_FACTOR_KEY}: {reversed_adjustment_factor:.{DEFAULT_PRECISION}f}")
#
#         # Get the last bit difficulty
#         last_bit_difficulty: float = blockchain.bit_difficulties[-1]
#
#         if reversed_adjustment_factor > 0:
#             # Calculate the bit adjustment factor
#             bit_adjustment_factor: float = math.log2(reversed_adjustment_factor)
#             # Clamp the bit adjustment factor
#             clamped_bit_adjustment_factor: float = clamp(bit_adjustment_factor, bit_clamp_factor)
#             # Calculate the new bit difficulty
#             new_bit_difficulty: float = max(smallest_bit_difficulty, last_bit_difficulty - clamped_bit_adjustment_factor)
#         else:
#             # Set the new bit difficulty to the smallest bit difficulty if the reversed adjustment factor is 0 or negative
#             new_bit_difficulty: float = smallest_bit_difficulty
#
#         # Update the last bit difficulty in the blockchain
#         blockchain.bit_difficulties[-1] = new_bit_difficulty
