#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib


class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str = '') -> None:
        """
        Initialize a Block object.

        Args:
            index (int): The index of the block in the blockchain.
            timestamp (float): The timestamp of the block.
            data (str): The data stored in the block.
            previous_hash (str, optional): The hash of the previous block. Defaults to ''.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Initialize nonce before calculating hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block.

        This function takes no arguments and returns a string.

        The hash is calculated by concatenating the block's index, timestamp,
        data, previous hash, and nonce. The concatenated string is then
        encoded to bytes and the hash is calculated using the SHA-256
        algorithm.

        :return: The hash of the block as a hexadecimal string.
        """
        sha = hashlib.sha256()
        sha.update(
            (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode(
                'utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Mine a block until the hash of the block starts with 'difficulty' zeros.

        Args:
            difficulty (int): The number of zeros that the block's hash
                should start with.

        Returns:
            None
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")
