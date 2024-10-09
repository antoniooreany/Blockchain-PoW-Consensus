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
            (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode(
                'utf-8'))
        return sha.hexdigest()

    def mine(self, difficulty: int, base: int = 2) -> None:
        max_nonce: int = 2 ** 256 - 1  # maximum value for nonce
        self.nonce = random.randint(0, max_nonce)  # Start from a random nonce

        target_zeros = '0' * difficulty  # Target string of zeros for leading characters
        base_hash_data = (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode(
            'utf-8')

        while True:
            sha = hashlib.sha256()
            sha.update(base_hash_data + str(self.nonce).encode('utf-8'))
            self.hash = sha.hexdigest()  # Get the hash as a hexadecimal string

            # Convert the hash based on the base provided
            if base == 2:
                converted_hash = bin(int(self.hash, 16))[2:].zfill(256)  # Binary (base-2)
            elif base == 4:
                converted_hash = self.convert_to_base4(int(self.hash, 16)).zfill(128)  # Quaternary (base-4)
            elif base == 8:
                converted_hash = oct(int(self.hash, 16))[2:].zfill(85)  # Octal (base-8)
            elif base == 16:
                converted_hash = self.hash  # Hexadecimal (base-16)

            # Check if the hash has the required number of leading zeros
            if converted_hash[:difficulty] == target_zeros:
                break

            self.nonce += 1

        log_mined_block(self)

    def convert_to_base4(self, num: int) -> str:
        """ Helper function to convert an integer to base-4. """
        if num == 0:
            return '0'
        digits = []
        while num:
            digits.append(str(num % 4))
            num //= 4
        return ''.join(digits[::-1])
