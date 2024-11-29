#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import time
from venv import logger

from src.constants import GENESIS_BLOCK_PREVIOUS_HASH
from src.model.block import Block
from src.model.blockchain import Blockchain

from typing import Optional

def add_blocks(
        blockchain: Optional[Blockchain],
        number_of_blocks_to_add: int
) -> None:
    """
    Add blocks to the blockchain.

    This function adds the specified number of blocks to the blockchain.
    It creates a new block for each index in range from 1 to number_of_blocks_to_add,
    adds it to the blockchain and adjusts the difficulty of the blockchain.

    The process of adding a block to the blockchain is as follows:
    1. Create a new block with the bit difficulty of the last block in the blockchain
       and the index of the block.
    2. Add the block to the blockchain.
    3. Adjust the difficulty of the blockchain.

    Args:
        blockchain (Optional[Blockchain]): The blockchain to add blocks to.
        number_of_blocks_to_add (int): The number of blocks to add.

    Returns:
        None
    """
    if blockchain is None:
        raise ValueError("blockchain cannot be None")
    if number_of_blocks_to_add < 0:
        raise ValueError("number_of_blocks_to_add cannot be negative")

    for index in range(1, number_of_blocks_to_add + 1):
        # 1. Create a new block with the bit difficulty of the last block in the blockchain
        #    and the index of the block.
        block = Block(
            bit_difficulty=blockchain.bit_difficulties[-1] if blockchain.bit_difficulties else 0,
            index=index,
            data=f"Block {index} Data",  # todo mock data is used, it should be replaced with real data
            previous_hash=blockchain.blocks[-1].hash if blockchain.blocks else GENESIS_BLOCK_PREVIOUS_HASH,
        )
        # 2. Add the block to the blockchain.
        blockchain.add_block(block, blockchain.clamp_factor, blockchain.smallest_bit_difficulty)
