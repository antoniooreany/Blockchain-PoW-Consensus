#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import math
import random
import logging

from src.model.block import Block
from src.constants import HASH_BIT_LENGTH, NONCE_BIT_LENGTH, BASE, HEXADECIMAL_BASE, SHA256_ENCODING
from src.utils.logging_utils import log_mined_block

class ProofOfWork:
    @staticmethod
    def calculate_hash(base_hash_data: bytes, nonce: int) -> str:
        """
        Compute the hash of a block by combining the various attributes together.

        The hash is computed by concatenating the index, timestamp, data, previous hash, and nonce, and then
        hashing the result.

        Args:
            base_hash_data (bytes): The concatenated data without the nonce.
            nonce (int): The nonce used in the proof of work algorithm.

        Returns:
            str: The hash of the block as a hexadecimal string.
        """
        sha = hashlib.sha256()
        sha.update(base_hash_data + str(nonce).encode(SHA256_ENCODING))
        return sha.hexdigest()

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
        max_nonce = BASE ** NONCE_BIT_LENGTH - 1
        block.nonce = random.randint(0, max_nonce)

        # Calculate the target value for the proof of work
        target_value = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1

        # Calculate the base hash data without the nonce
        base_hash_data = (str(block.index) + str(block.timestamp) + str(block.data) + str(block.previous_hash)).encode(SHA256_ENCODING)

        # Loop until a valid nonce is found
        while True:
            # Calculate the hash of the block with the current nonce
            block.hash = ProofOfWork.calculate_hash(base_hash_data, block.nonce)

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


