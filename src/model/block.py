#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
import logging
import random
import time

from src.constants import MAX_NONCE
from src.utils.hash_utils import calculate_block_hash


class Block:
    def __init__(
            self,
            bit_difficulty: float,
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

        # Initialize the nonce with a random value within the possible range
        self.nonce: int = random.randint(0, MAX_NONCE)
        logging.info(f"Block {self.index} initial nonce search enter point: {self.nonce}")

        # Compute the hash of the block
        self.hash: str = calculate_block_hash(self.index, self.timestamp, self.data, self.previous_hash, self.nonce)
