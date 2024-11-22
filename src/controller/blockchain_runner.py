#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import time
from src.model.block import Block
from src.model.blockchain import Blockchain


def add_blocks(
        blockchain: Blockchain,
        number_of_blocks_to_add: int
) -> None:
    """
    Add blocks to the blockchain.

    This function adds the specified number of blocks to the blockchain.
    It creates a new block for each index in range from 1 to number_of_blocks_to_add,
    adds it to the blockchain and adjusts the difficulty of the blockchain.

    Args:
        blockchain (Blockchain): The blockchain to add blocks to.
        number_of_blocks_to_add (int): The number of blocks to add.

    Returns:
        None
    """
    for index in range(1, number_of_blocks_to_add + 1):
        # Create a new block with the bit difficulty of the last block in the blockchain
        # and the index of the block
        block = Block(
            bit_difficulty=blockchain.bit_difficulties[-1],
            index=index,
            data=f"Block {index} Data",  # todo mock data is used, it should be replaced with real data
            timestamp=time.time(),
            previous_hash=blockchain.blocks[-1].hash if blockchain.blocks else None,
        )
        # Add the block to the blockchain
        blockchain.add_block(block, blockchain.clamp_factor, blockchain.smallest_bit_difficulty)
