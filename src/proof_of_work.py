#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import math
import random

from block import Block
from constants import (
    HASH_BIT_LENGTH,
    NONCE_BIT_LENGTH,
)
from src.logging_utils import log_mined_block


class ProofOfWork:

    @staticmethod
    def find_nonce(
            block: Block,
            bit_difficulty: float,
    ) -> None:
        """
        Perform the proof of work algorithm to find a valid nonce for the block.

        This method attempts to find a nonce such that the block's hash is less than the target
        value derived from the given bit difficulty.

        Args:
            block (Block): The block for which the nonce is to be found.
            bit_difficulty (float): The difficulty level which determines the target value.

        Returns:
            None
        """
        max_nonce: int = 2 ** NONCE_BIT_LENGTH - 1  # Maximum possible nonce value
        block.nonce = random.randint(0, max_nonce)  # Start with a random nonce

        # Calculate the target value based on difficulty
        target_value: float = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1

        # Concatenate block attributes to create base data for hashing
        base_hash_data: bytes = (
            (str(block.index) +
             str(block.timestamp) +
             str(block.data) +
             str(block.previous_hash))
            .encode('utf-8')
        )

        while True:
            sha: hashlib.sha256 = hashlib.sha256()  # Create a new SHA256 hash object
            sha.update(base_hash_data + str(block.nonce).encode('utf-8'))  # Hash the nonce combined with base data
            block.hash = sha.hexdigest()  # Store the hash as a hexadecimal string

            hash_value: int = int(block.hash, 16)  # Convert the hash to an integer

            # Check if the hash value meets the target; if so, the block is mined
            if hash_value < target_value:
                break  # Exit loop when a valid nonce is found

            block.nonce += 1  # Increment nonce to try different hash

        log_mined_block(block)  # Log the mined block information


    @staticmethod
    def validate_proof(block: Block, bit_difficulty: float) -> bool:
        """
        Check if the hash of the block meets the target value derived from the given bit difficulty.

        Args:
            block (Block): The block for which the nonce is to be validated.
            bit_difficulty (float): The difficulty level which determines the target value.

        Returns:
            bool: True if the hash value meets the target; False otherwise.
        """
        target_value: float = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1
        hash_value: int = int(block.hash, 16)
        return hash_value < target_value
