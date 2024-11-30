#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# path: src/controller/proof_of_work.py

import math
from venv import logger

from src.model.block import Block
from src.constants import HASH_BIT_LENGTH, BASE, HEXADECIMAL_BASE, NONCE_INCREMENT
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
        Finds a nonce for a given block such that its hash is smaller than the target value.

        Args:
            block (Block): The block to find a nonce for.
            bit_difficulty (float): The difficulty level of the block.

        Returns:
            None
        """
        if block is None:
            raise ValueError("Block cannot be None")

        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        while True:
            block.hash = calculate_block_hash(
                index=block.index,
                timestamp=block.timestamp,  # Ensure consistent timestamp
                data=block.data,
                previous_block_hash=block.previous_hash,
                nonce=block.nonce,
            )
            if int(block.hash, HEXADECIMAL_BASE) < target_value:
                logger.debug(f"Found nonce for block {block.index}: {block.nonce}, Hash: {block.hash}")
                break
            block.nonce += 1
            if block.nonce % NONCE_INCREMENT == 0:
                logger.debug(f"Trying another {NONCE_INCREMENT} nonce {block.nonce} for block {block.index}, Hash: {block.hash}")


    def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
        """
        Validate the proof of work for a given block.

        Args:
            block (Block): The block to validate.
            bit_difficulty (float): The difficulty level for the block's proof of work.

        Returns:
            bool: True if the block's hash meets the required difficulty, False otherwise.
        """
        # Calculate the target value based on bit difficulty
        target_value: float = pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        # Convert the hash from hexadecimal to a numerical value
        hash_value: int = int(block.hash, HEXADECIMAL_BASE)

        # Format values with commas and ensure equal padding
        hash_value_str: str = f"{hash_value:,}"
        target_value_str: str = f"{int(target_value):,}"

        # Find the length of the longest string for alignment
        max_length: int = max(len(hash_value_str), len(target_value_str))

        # Add padding to align values
        hash_value_padded: str = hash_value_str.rjust(max_length)
        target_value_padded: str = target_value_str.rjust(max_length)

        # Log the values
        is_valid: bool = hash_value < target_value
        logger.debug(
            f"Validating Block {block.index}:\n"
            f"  Hash Value (int):   {hash_value_padded}\n"
            f"  Target Value (int): {target_value_padded}"
        )
        if is_valid:
            logger.info(f"Block {block.index} Validation: PASS")
            log_mined_block(block)
        else:
            logger.critical(f"Block {block.index} Validation: FAIL\n")

        # Return validation result
        return is_valid

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
        if not isinstance(bit_adjustment_factor, (int, float)) or not isinstance(bit_clamp_factor, (int, float)):
            raise TypeError("bit_adjustment_factor and bit_clamp_factor must be numbers")
        if bit_clamp_factor < 0:
            raise ValueError("bit_clamp_factor must be a positive number")

        clamped_bit_adjustment_factor: float = max(-bit_clamp_factor, min(bit_adjustment_factor, bit_clamp_factor))
        return clamped_bit_adjustment_factor
