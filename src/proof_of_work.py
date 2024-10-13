#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math

from block import Block

HASH_BIT_LENGTH = 256  # The length of the hash in bits
NONCE_BIT_LENGTH = 32  # The length of the nonce in bits


# todo redundant class, move methods to Block class
class ProofOfWork:
    @staticmethod
    def find_nonce(block: Block, bit_difficulty: float) -> int:  # todo implemented in Block
        """
        Finds a nonce for a given block such that the block's hash
        is less than the target value based on the difficulty.

        Args:
            block (Block): The block to find a nonce for.
            bit_difficulty (int): The number of leading zero bits required in the hash.

        Returns:
            int: The nonce that results in the block's hash meeting the difficulty requirement.
        """
        # target_value = (2 ** (256 - bit_difficulty)) - 1
        target_value = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1
        while int(block.hash, 16) >= target_value:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.nonce

    @staticmethod
    def validate_proof(block: Block, bit_difficulty: float) -> bool:  # todo move to Block class, where to use it?
        """
        Checks if a given block's hash is less than the target value based on the difficulty.

        Args:
            block (Block): The block to validate.
            bit_difficulty (int): The number of leading zero bits required in the hash.

        Returns:
            bool: True if the block's hash meets the difficulty requirement, False otherwise.
        """
        target_value = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1
        return int(block.hash, 16) < target_value
