#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math
import random

from src.model.block import Block
from src.constants import HASH_BIT_LENGTH, NONCE_BIT_LENGTH, BASE, HEXADECIMAL_BASE
from src.utils.hash_utils import calculate_hash
from src.utils.logging_utils import log_mined_block

class ProofOfWork:

    @staticmethod
    def find_nonce(block: Block, bit_difficulty: float) -> None:
        """
        Finds a nonce for the given block to satisfy the proof of work algorithm.

        Args:
            block (Block): The block to find the nonce for.
            bit_difficulty (float): The difficulty level of the block.

        Returns:
            None
        """
        # Set a random nonce
        max_nonce: int = BASE ** NONCE_BIT_LENGTH - 1
        block.nonce = random.randint(0, max_nonce) # todo Non-self attribute could not be type hinted

        # Calculate the target value for the proof of work
        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        # Loop until a valid nonce is found
        while True:
            # Calculate the hash of the block with the current nonce
            block.hash = calculate_hash(
                block.index, block.timestamp, block.data, block.previous_hash, block.nonce
            ) # todo Non-self attribute could not be type hinted

            # Check if the hash is valid
            if int(block.hash, HEXADECIMAL_BASE) < target_value:
                break

            # Increment the nonce
            block.nonce += 1

        # Log the mined block
        log_mined_block(block)

    @staticmethod
    def validate_proof(block: Block, bit_difficulty: float) -> bool:
        """
        Checks if the given block satisfies the proof of work algorithm.

        Args:
            block (Block): The block to check.
            bit_difficulty (float): The difficulty level of the block.

        Returns:
            bool: True if the block is valid, False otherwise.
        """
        # Calculate the target value for the proof of work
        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        # Calculate the hash value of the block
        hash_value: int = int(block.hash, HEXADECIMAL_BASE)

        # Check if the hash value is less than the target value
        return hash_value < target_value


