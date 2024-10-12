#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import hashlib
import math
import random
from venv import logger

from src.logging_utils import log_mined_block


# from src.logging_utils import log_mined_block


# from logging_utils import log_mined_block


class Block:
    def __init__(
            self,
            index: int,
            timestamp: float,
            data: str,
            previous_hash: str = '',
    ) -> None:
        """
        Block constructor.

        Args:
            index (int): The block number.
            timestamp (float): The timestamp for the block.
            data (str): The data stored in the block.
            previous_hash (str, optional): The hash of the previous block. Defaults to ''.
        """
        self.index: int = index
        self.timestamp: float = timestamp
        self.data: str = data
        self.previous_hash: str = previous_hash
        self.nonce: int = 0
        self.hash: str = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the block.

        Args:
            None

        Returns:
            str: The SHA-256 hash of the block
        """
        sha: hashlib.sha256 = hashlib.sha256()
        sha.update(
            (str(self.index) +
             str(self.timestamp) +
             str(self.data) +
             str(self.previous_hash) +
             str(self.nonce))
            .encode('utf-8'))
        return sha.hexdigest()

    def mine(
            self,
            bit_difficulty: float,
    ) -> None:
        """
        Mine a block.

        Args:
            bit_difficulty (int): The difficulty of the block as a number of bits.

        Returns:
            None
        """
        max_nonce: int = 2 ** 256 - 1  # maximum value for nonce
        self.nonce: int = random.randint(0, max_nonce)  # Start from a random nonce

        # Calculate the target value based on difficulty
        # target_value: int = (2 ** (256 - bit_difficulty)) - 1  # todo move to blockchain.py
        target_value: float = math.pow(2, 256 - bit_difficulty) - 1  # todo move to blockchain.py

        logger.debug(f"Target value: {target_value}")
        # log the target value in hexadecimal with leading zeros
        # logger.debug(f"Target value in hexadecimal with leading zeros: {hex(target_value)[2:]}")
        # logger.debug(f"Target value in hexadecimal: {hex(target_value)}")

        base_hash_data: bytes = ((str(self.index) +
                                  str(self.timestamp) +
                                  str(self.data) +
                                  str(self.previous_hash))
                                 .encode('utf-8'))

        while True:
            sha: hashlib.sha256 = hashlib.sha256()
            sha.update(base_hash_data + str(self.nonce).encode('utf-8'))
            self.hash: str = sha.hexdigest()  # Get the hash as a hexadecimal string

            # Convert the hash to an integer
            hash_value: int = int(self.hash, 16)

            # Check if the hash value is less than the target value: if so, the block is mined
            if hash_value < target_value:  # If the hash meets the target value, the block is mined
                break

            self.nonce += 1  # Increment the nonce to try a different hash
        log_mined_block(self)  # todo move to blockchain.py

    # def convert_to_base4(self, num: int) -> str:
    #     """ Helper function to convert an integer to base-4. """
    #     if num == 0:
    #         return '0'
    #     digits = []
    #     while num:
    #         digits.append(str(num % 4))
    #         num //= 4
    #     return ''.join(digits[::-1])
