#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
import random
import time

from src.constants import NONCE_BIT_LENGTH, BASE
from src.utils.hash_utils import calculate_block_hash

class Block:
    def __init__(
            self,
            bit_difficulty: float,
            index: int,
            data: str,
            timestamp: float,  # timestamp is used in the constructor todo why it is grey in intellij?
            previous_hash: str,
    ) -> None:
        """Initialize a new block with its attributes.

        Args:
            bit_difficulty (float): The difficulty level of the block.
            index (int): The position of the block in the blockchain.
            data (str): The data contained within the block.
            previous_hash (str): The hash of the previous block in the chain.
            timestamp (float): The time at which the block was created. This is not used in the
                constructor, but is used in the hash calculation.
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
        # self.nonce: int = 0

        # Calculate the maximum possible nonce value
        max_nonce: int = BASE ** NONCE_BIT_LENGTH - 1

        # Initialize the nonce with a random value within the possible range
        self.nonce = random.randint(0, max_nonce)


        # Compute the hash of the block
        self.hash: str = calculate_block_hash(self.index, self.timestamp, self.data, self.previous_hash, self.nonce)
