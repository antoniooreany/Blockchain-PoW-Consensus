#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import random
import time

from src.constants import NONCE_BIT_LENGTH, BASE
from src.controller.proof_of_work import find_nonce
from src.utils.hash_utils import calculate_block_hash

class Block:
    def __init__(
            self,
            bit_difficulty: float,  # todo ? should we remove it to the blockchain level?
            index: int,
            data: str,
            previous_hash: str,
    ) -> None:
        """
        Initialize a new block with its attributes.

        Args:
            bit_difficulty (float): The difficulty level of the block.
            index (int): The position of the block in the blockchain.
            data (str): The data contained within the block.
            previous_hash (str): The hash of the previous block in the chain.
        """
        self.bit_difficulty = bit_difficulty
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        # self.nonce = random.randint(0, BASE ** NONCE_BIT_LENGTH - 1)
        # self.nonce = 111 # todo remove this line after implementing the proof of work algorithm
        # self.hash = calculate_block_hash(
        #     self.index, self.timestamp, self.data, self.previous_hash, self.nonce
        # )
        self.nonce = find_nonce(self, self.bit_difficulty)
        self.hash = calculate_block_hash(
            self.index, self.timestamp, self.data, self.previous_hash, self.nonce
        )

# I removed the debugging statement and the unnecessary comment. I also standardized the variable names and formatting.
