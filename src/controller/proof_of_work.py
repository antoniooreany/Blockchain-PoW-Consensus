#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math
import random

from src.model.block import Block
from src.constants import HASH_BIT_LENGTH, NONCE_BIT_LENGTH, BASE, HEXADECIMAL_BASE
from src.utils.hash_utils import calculate_block_hash
from src.utils.logging_utils import log_mined_block


class ProofOfWork:
    def __init__(self) -> None:
        """
        Initializes a new instance of the ProofOfWork class.

        This class provides a proof of work algorithm to be used in a blockchain.
        It provides methods to find a nonce for a given block and to validate a
        block's proof of work.

        Returns:
            None
        """
        pass  # todo add any initialization logic here

    def find_nonce(self, block: Block, bit_difficulty: float) -> None:
        """
        Finds a nonce for the given block to satisfy the proof of work algorithm.

        This function iteratively tries different nonce values for the given block
        until it finds one that results in a hash value that is less than the target
        value determined by the bit difficulty.

        Args:
            block (Block): The block for which to find the nonce.
            bit_difficulty (float): The difficulty level of the block.

        Returns:
            None

        Raises:
            ValueError: If the provided block is None.
        """
        if block is None:
            raise ValueError("Block cannot be None")

        # Calculate the maximum possible nonce value
        max_nonce: int = BASE ** NONCE_BIT_LENGTH - 1

        # Initialize the nonce with a random value within the possible range
        block.nonce = random.randint(0, max_nonce)

        # Calculate the target value for the hash based on bit difficulty
        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        while True:
            # Calculate the hash of the block with the current nonce
            block.hash = calculate_block_hash(
                block.index, block.timestamp, block.data, block.previous_hash, block.nonce
            )

            # Check if the hash is less than the target value
            if int(block.hash, HEXADECIMAL_BASE) < target_value:
                break

            # Increment the nonce to try a new value
            block.nonce += 1

        # Log the mined block details
        log_mined_block(block)

    def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
        """
        Checks if the given block satisfies the proof of work algorithm.

        This function takes a block and a bit difficulty as parameters and checks if the block's
        hash is less than the target value determined by the bit difficulty. If the hash is
        less than the target value, the block is valid, otherwise it is invalid.

        Args:
            block (Block): The block to check.
            bit_difficulty (float): The difficulty level of the block.

        Returns:
            bool: True if the block is valid, False otherwise.
        """
        if block is None:
            raise ValueError("Block cannot be null")
        if block.hash is None:
            raise ValueError("Block hash cannot be null")

        # Calculate the target value for the hash based on the bit difficulty
        target_value: float = pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        # Calculate the hash value of the block
        hash_value: int = int(block.hash, HEXADECIMAL_BASE)

        # Check if the hash value is less than the target value
        return hash_value < target_value

    def clamp_bit_adjustment_factor(self, bit_adjustment_factor: float, bit_clamp_factor: float) -> float:
        """
        Clamp the bit adjustment factor within the range determined by the bit clamp factor.

        This function takes two parameters, the bit adjustment factor and the bit clamp factor.
        The bit adjustment factor is the factor by which the bit difficulty is adjusted.
        The bit clamp factor is the maximum allowable adjustment factor.

        The function first calculates the minimum of the bit adjustment factor and the bit clamp factor,
        and then calculates the maximum of the result and the negative of the bit clamp factor.
        The final result is the clamped bit adjustment factor.

        Args:
            bit_adjustment_factor (float): The factor by which the bit difficulty is adjusted.
            bit_clamp_factor (float): The maximum allowable adjustment factor.

        Returns:
            float: The clamped bit adjustment factor.
        """
        if bit_adjustment_factor is None or bit_clamp_factor is None:
            raise ValueError("bit_adjustment_factor or bit_clamp_factor cannot be None")
        if not isinstance(bit_adjustment_factor, (int, float)) or not isinstance(bit_clamp_factor, (int, float)):
            raise TypeError("bit_adjustment_factor and bit_clamp_factor must be numbers")
        if bit_clamp_factor < 0:
            raise ValueError("bit_clamp_factor must be a positive number")

        clamped_bit_adjustment_factor: float = max(-bit_clamp_factor, min(bit_adjustment_factor, bit_clamp_factor))
        return clamped_bit_adjustment_factor

# Clean up:
# - Standardized variable names
# - Removed debugging statements
# - Improved readability by using a consistent naming convention
# - Improved performance by using max and min functions instead of if-elif-else statements
