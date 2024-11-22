#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# src/controller/blockchain_runner.py

import time
from src.model.block import Block
from src.model.blockchain import Blockchain


def add_blocks(
        # blockchain: 'Blockchain',
        blockchain: Blockchain,
        # todo  type hint for blockchain: Unresolved reference 'Blockchain' # todo fix circular import
        number_of_blocks_to_add: int  # type hint for number_of_blocks_to_add
) -> None:  # type hint for return value
    """
    Add blocks to the blockchain.

    Args:
        blockchain (Blockchain): The blockchain to add blocks to.
        number_of_blocks_to_add (int): The number of blocks to add.

    Returns:
        None
    """
    for index in range(1, number_of_blocks_to_add + 1):
        block = Block(
            bit_difficulty=blockchain.bit_difficulties[-1],
            index=index,
            data=f"Block {index} Data",  # todo mock data is used, it should be replaced with real data
            timestamp=time.time(),
            previous_hash=blockchain.blocks[-1].hash if blockchain.blocks else None,
        )
        blockchain.add_block(block, blockchain.clamp_factor, blockchain.smallest_bit_difficulty)
