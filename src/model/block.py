#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import time

from src.constants import ENCODING
from src.utils.hash_utils import calculate_hash

class Block:
    def __init__(
            self,
            bit_difficulty: float,
            index: int,
            data: str,
            timestamp: float, # timestamp is used in the constructor todo why it is grey?
            previous_hash: str,
    ) -> None:
        """Initialize a new block with its attributes.

        Args:
            bit_difficulty (float): The difficulty level of the block.
            index (int): The position of the block in the blockchain.
            timestamp (float): The time at which the block was created.
            data (str): The data contained within the block.
            previous_hash (str): The hash of the previous block in the chain.
        """
        # Set the difficulty level for the block
        self.bit_difficulty: float = bit_difficulty

        # Assign the block index
        self.index: int = index

        # Store the block's data
        self.data: str = data

        # Record the timestamp of block creation
        self.timestamp: float = time.time()

        # Store the hash of the previous block
        self.previous_hash: str = previous_hash

        # Initialize the nonce for the proof of work algorithm
        self.nonce: int = 0

        # Compute the hash of the block
        self.hash: str = calculate_hash(self.index, self.timestamp, self.data, self.previous_hash, self.nonce)
