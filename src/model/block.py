#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import time

from ..constants import ENCODING

class Block:
    def __init__(
            self,
            bit_difficulty: float,
            index: int,
            data: str,
            timestamp: float,
            previous_hash: str = ''
    ) -> None:
        """Initialize a new block with its attributes.

        Args:
            bit_difficulty (float): The difficulty level of the block.
            index (int): The position of the block in the blockchain.
            timestamp (float): The time at which the block was created.
            data (str): The data contained within the block.
            previous_hash (str): The hash of the previous block in the chain.
        """
        # Assign the block index
        self.index: int = index

        # Set the difficulty level for the block
        self.bit_difficulty: float = bit_difficulty

        # Record the timestamp of block creation
        self.timestamp: float = time.time()

        # Store the block's data
        self.data: str = data

        # Store the hash of the previous block
        self.previous_hash: str = previous_hash

        # Initialize the nonce for the proof of work algorithm
        self.nonce: int = 0

        # Compute the initial hash of the block
        self.hash: str = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Compute the hash of the block by combining the various attributes together.

        The hash is computed by concatenating the index, timestamp, data, previous hash, and nonce, and then
        hashing the result.

        Returns:
            str: The hash of the block as a hexadecimal string.
        """
        # Create a SHA256 hash object
        sha: hashlib.sha256 = hashlib.sha256()

        # Concatenate the block's attributes and encode the result as bytes
        data_to_hash: bytes = (
                str(self.index) +  # The index of the block in the blockchain
                str(self.timestamp) +  # The time at which the block was created
                str(self.data) +  # The data contained within the block
                str(self.previous_hash) +  # The hash of the previous block in the chain
                str(self.nonce)  # The nonce for the proof of work algorithm
        ).encode(ENCODING)

        # Update the hash object with the concatenated data
        sha.update(data_to_hash)

        # Return the hash as a hexadecimal string
        return sha.hexdigest()
