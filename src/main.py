#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
import time

from blockchain import Block, Blockchain
from logger_singleton import LoggerSingleton
from plotting import plot_blockchain_statistics

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
        INITIAL_BIT_DIFFICULTY = 18  # todo avoid base_difficulty, use bit_difficulty, better even linear_difficulty
        # INITIAL_BASE_DIFFICULTY = round(INITIAL_BIT_DIFFICULTY / math.log2(base))
        ADJUSTMENT_INTERVAL = 10
        NUMBER_BLOCKS_TO_ADD = 100
        TARGET_BLOCK_TIME = 1

        blockchain = Blockchain(
            # initial_base_difficulty=INITIAL_BASE_DIFFICULTY,
            bit_difficulty=INITIAL_BIT_DIFFICULTY,
            adjustment_interval=ADJUSTMENT_INTERVAL,  # todo should it be a property of blockchain?
            target_block_time=TARGET_BLOCK_TIME,
        )
        logger.debug(f"Created: blockchain (base: {base}, initial bit difficulty: {INITIAL_BIT_DIFFICULTY})")
        logger.debug(f"##################")

        # Create the genesis block
        genesis_block = blockchain.create_genesis_block()
        logger.info(f"Created: Genesis block; index: {genesis_block.index}, hash: {genesis_block.hash}")
        logger.debug(f"##################")

        # Now mine other blocks
        for i in range(1, NUMBER_BLOCKS_TO_ADD):
            blockchain.add_block(Block(i, time.time(), f"Block {i} Data"))

        blockchains[base] = blockchain

    plot_blockchain_statistics(blockchains)

    # logger.debug(f"##################")
    # # log all blockchains
    # for blockchain in blockchains.values():
    #     # logger.debug(f"Blockchain with base {blockchain.base}")
    #     for block in blockchain.blocks:
    #         logger.debug(f"Block {block.index} with hash {block.hash}")
    #     logger.debug(f"##################")
