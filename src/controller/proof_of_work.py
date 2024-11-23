# #   Copyright (c) 2024, Anton Gorshkov
# #   All rights reserved.
# #   This code is for a pow and its unit tests.
# #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
#
import logging
import math
import random

from src.model.block import Block
from src.constants import HASH_BIT_LENGTH, NONCE_BIT_LENGTH, BASE, HEXADECIMAL_BASE
from src.utils.hash_utils import calculate_hash
from src.utils.logging_utils import log_mined_block


class ProofOfWork:
    def __init__(self):  # use oop-style to be more flexible in the future
        pass

    def find_nonce(self, block: Block, bit_difficulty: float) -> None:
        """
        Finds a nonce for the given block to satisfy the proof of work algorithm.

        Args:
            block (Block): The block to find the nonce for.
            bit_difficulty (float): The difficulty level of the block.

        Returns:
            None
        """
        max_nonce: int = BASE ** NONCE_BIT_LENGTH - 1
        block.nonce = random.randint(0, max_nonce)

        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        while True:
            block.hash = calculate_hash(
                block.index, block.timestamp, block.data, block.previous_hash, block.nonce
            )

            if int(block.hash, HEXADECIMAL_BASE) < target_value:
                break

            block.nonce += 1

        log_mined_block(block)

    # def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
    #     """
    #     Checks if the given block satisfies the proof of work algorithm.
    #
    #     Args:
    #         block (Block): The block to check.
    #         bit_difficulty (float): The difficulty level of the block.
    #
    #     Returns:
    #         bool: True if the block is valid, False otherwise.
    #     """
    #     target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
    #     hash_value: int = int(block.hash, HEXADECIMAL_BASE)
    #     logging.info(f"Validating proof of work for block {block.index}...")
    #     logging.info(f"Target value: {target_value}")
    #     logging.info(f"Hash value: {hash_value}")
    #     logging.info(f"Is valid: {hash_value < target_value}")
    #     return hash_value < target_value

    def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
        """
        Validate the proof of work for a given block.

        Args:
            block (Block): The block to validate.
            bit_difficulty (float): The bit difficulty for the proof of work.

        Returns:
            bool: True if the proof of work is valid, False otherwise.
        """
        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
        hash_value: int = int(block.hash, HEXADECIMAL_BASE)

        logging.info(f"Validating proof of work for block {block.index}...")
        logging.info(f"Target value: {target_value}")
        logging.info(f"Hash value: {hash_value}")
        logging.info(f"Is valid: {hash_value < target_value}")

        return hash_value < target_value



    # def validate_proof(self, block, bit_difficulty):
    #     """
    #     Validate the proof of work for a given block.
    #
    #     Args:
    #         block (Block): The block to validate.
    #         bit_difficulty (float): The bit difficulty for the proof of work.
    #
    #     Returns:
    #         bool: True if the proof of work is valid, False otherwise.
    #     """
    #     target = (1 << (256 - int(bit_difficulty))) - 1
    #     return int(block.hash, 16) < target


    def clamp(self, bit_adjustment_factor: float, bit_clamp_factor: float) -> float:
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
