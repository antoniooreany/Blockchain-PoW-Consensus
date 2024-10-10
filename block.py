#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import hashlib
import random

from logging_utils import log_mined_block


class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str = '') -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        sha = hashlib.sha256()
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
            bit_difficulty,
            # base=2, # todo don't use base as a property of blockchain, block etc.
    ):
        max_nonce = 2 ** 256 - 1  # maximum value for nonce
        self.nonce = random.randint(0, max_nonce)  # Start from a random nonce

        # Calculate the target value based on difficulty
        target_value = (2 ** (256 - bit_difficulty)) - 1

        base_hash_data = ((str(self.index) +
                           str(self.timestamp) +
                           str(self.data) +
                           str(self.previous_hash))
                          .encode('utf-8'))

        while True:
            sha = hashlib.sha256()
            sha.update(base_hash_data + str(self.nonce).encode('utf-8'))
            self.hash = sha.hexdigest()  # Get the hash as a hexadecimal string

            # Convert the hash to an integer
            hash_value = int(self.hash, 16)

            # Check if the hash value is less than the target value: if so, the block is mined
            if hash_value < target_value:
                break

            self.nonce += 1  # Increment the nonce to try a different hash
        log_mined_block(self)

    # def convert_to_base4(self, num: int) -> str:
    #     """ Helper function to convert an integer to base-4. """
    #     if num == 0:
    #         return '0'
    #     digits = []
    #     while num:
    #         digits.append(str(num % 4))
    #         num //= 4
    #     return ''.join(digits[::-1])
