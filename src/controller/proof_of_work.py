#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math
import random
from venv import logger

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

        # Calculate the target value for the hash based on bit difficulty
        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1


        while True:
            block.hash = calculate_block_hash(
                index=block.index,
                timestamp=block.timestamp,
                data=block.data,
                previous_block_hash=block.previous_hash,
                nonce=block.nonce,
            )
            if int(block.hash, HEXADECIMAL_BASE) < target_value:
                logger.debug(f"Found nonce for block {block.index}: {block.nonce}, Hash: {block.hash}")
                break
            block.nonce += 1
            if block.nonce % 10_000 == 0:  # Log every 10,000 iterations
                logger.debug(f"Going through nonce for block {block.index}: {block.nonce}, Hash: {block.hash}")


        # Log the mined block details
        log_mined_block(block)

    # def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
    #     target_value = pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
    #     hash_value = int(block.hash, HEXADECIMAL_BASE)
    #     logger.debug(f"Validating Block {block.index} | Hash: {block.hash} | Target: {target_value}")
    #     return hash_value < target_value

    # def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
    #     # Calculate the target value based on bit difficulty
    #     target_value = pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
    #
    #     # Convert the hash from hexadecimal to a numerical value
    #     hash_value = int(block.hash, 16)  # 16 is the base for hexadecimal
    #
    #     # Log the relevant comparison details
    #     if hash_value < target_value:
    #         logger.debug(f"Block {block.index} Validation: PASS")
    #     else:
    #         logger.critical(f"Block {block.index} Validation: FAIL")
    #
    #     # Add clear log comparison
    #     logger.debug(
    #         f"Validating Block {block.index}: \n"
    #         f"  Hash Value: {hash_value} \n"
    #         f"  Target Value: {target_value} \n"
    #         f"  Comparison: {'Hash < Target (Valid)' if hash_value < target_value else 'Hash >= Target (Invalid)'}"
    #     )
    #
    #     # Return validation result
    #     return hash_value < target_value

    # def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
    #     # Calculate the target value based on bit difficulty
    #     target_value = pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
    #
    #     # Convert the hash from hexadecimal to a numerical value
    #     hash_value = int(block.hash, 16)
    #
    #     # Format values in both exponential and full precision
    #     target_value_exp = f"{target_value:.2e}"
    #     hash_value_exp = f"{hash_value:.2e}"
    #
    #     logger.debug(
    #         f"Validating Block {block.index}:\n"
    #         f"  Hash Value: {hash_value} ({hash_value_exp})\n"
    #         f"  Target Value: {target_value} ({target_value_exp})\n"
    #         f"  Comparison: {'Hash < Target (Valid)' if hash_value < target_value else 'Hash >= Target (Invalid)'}"
    #     )
    #
    #     # Return validation result
    #     return hash_value < target_value

    # def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
    #     # Calculate the target value based on bit difficulty
    #     target_value = pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
    #
    #     # Convert the hash from hexadecimal to a numerical value
    #     hash_value = int(block.hash, 16)
    #
    #     # Prepare values for aligned output
    #     hash_value_full = f"{hash_value:,}"  # Add commas for readability
    #     target_value_full = f"{int(target_value):,}"
    #     hash_value_exp = f"{hash_value:.3e}"  # Use exponential format with 3 decimal places
    #     target_value_exp = f"{target_value:.3e}"
    #
    #     # Log comparison
    #     logger.debug(
    #         f"Validating Block {block.index}:\n"
    #         f"  Hash Value:   {hash_value_full}\n"
    #         f"  Target Value: {target_value_full}\n"
    #         f"  Comparison: {'Hash < Target (Valid)' if hash_value < target_value else 'Hash >= Target (Invalid)'}"
    #     )
    #
    #     # Return validation result
    #     return hash_value < target_value

    def validate_proof(self, block: Block, bit_difficulty: float) -> bool:
        # Calculate the target value based on bit difficulty
        target_value = pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        # Convert the hash from hexadecimal to a numerical value
        hash_value = int(block.hash, 16)

        # Format values with commas and ensure equal padding
        hash_value_str = f"{hash_value:,}"
        target_value_str = f"{int(target_value):,}"

        # Find the length of the longest string for alignment
        max_length = max(len(hash_value_str), len(target_value_str))

        # Add padding to align values
        hash_value_padded = hash_value_str.rjust(max_length)
        target_value_padded = target_value_str.rjust(max_length)

        # Log the values
        is_valid = hash_value < target_value
        logger.debug(
            f"Validating Block {block.index}:\n"
            f"  Hash Value (int):   {hash_value_padded}\n"
            f"  Target Value (int): {target_value_padded}"
            # f"  Comparison:   {'Hash < Target (Valid)' if is_valid else 'Hash >= Target (Invalid)'}"
        )
        if is_valid:
            logger.info(f"Block {block.index} Validation: PASS\n")
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
        if bit_adjustment_factor is None or bit_clamp_factor is None:
            raise ValueError("bit_adjustment_factor or bit_clamp_factor cannot be None")
        if not isinstance(bit_adjustment_factor, (int, float)) or not isinstance(bit_clamp_factor, (int, float)):
            raise TypeError("bit_adjustment_factor and bit_clamp_factor must be numbers")
        if bit_clamp_factor < 0:
            raise ValueError("bit_clamp_factor must be a positive number")

        clamped_bit_adjustment_factor: float = max(-bit_clamp_factor, min(bit_adjustment_factor, bit_clamp_factor))
        return clamped_bit_adjustment_factor
