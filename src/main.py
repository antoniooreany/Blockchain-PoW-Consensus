#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging

from blockchain import Blockchain, create_genesis_block
from logger_singleton import LoggerSingleton
from plotting import plot_blockchain_statistics
from src.logging_utils import log_mined_block

if __name__ == "__main__":
    # Set the logging level to INFO (or WARNING to reduce more output)
    logging.getLogger('matplotlib').setLevel(logging.INFO)

    logger = LoggerSingleton.get_instance().logger

    blockchains = {}
    for base in [
        2,
        # 4,
        # 8,
        # 16,
        # 32,
        # 64,
        # 128,
        # 256,
        # 512,
        # 1024,
    ]:
        INITIAL_BIT_DIFFICULTY = 13  # todo avoid base_difficulty, use bit_difficulty, better even linear_difficulty
        ADJUSTMENT_INTERVAL = 10
        TARGET_BLOCK_TIME = 0.001

        CLAMP_FACTOR = 2  # todo 2 bits; bin: 0b10, hex: 0x2, dec: 2: max adjustment factor
        SMALLEST_BIT_DIFFICULTY = 4  # todo 4 bits; bin: 0b0000, hex: 0x0, dec: 0: smallest bit difficulty

        NUMBER_BLOCKS_TO_ADD = 10000

        blockchain = Blockchain(
            initial_bit_difficulty=INITIAL_BIT_DIFFICULTY,
            adjustment_interval=ADJUSTMENT_INTERVAL,  # todo should it be a property of blockchain?
            target_block_time=TARGET_BLOCK_TIME,
        )
        logger.debug(f"Created: blockchain (base: {base}, initial bit difficulty: {INITIAL_BIT_DIFFICULTY})")
        logger.debug(f"##################")

        # Create the genesis block
        genesis_block = create_genesis_block()
        log_mined_block(genesis_block)
        logger.debug(f"##################")

        blockchain.mine_blocks(number_of_blocks=NUMBER_BLOCKS_TO_ADD, clamp_factor=CLAMP_FACTOR,
                               smallest_bit_difficulty=SMALLEST_BIT_DIFFICULTY)

        blockchains[base] = blockchain

    plot_blockchain_statistics(blockchains)
