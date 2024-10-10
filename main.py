# #   Copyright (c) 2024, Anton Gorshkov
# #   All rights reserved.
# #
# #   This code is for a main.py and its unit tests.
# #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
import math
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
        4,
        8,
        16,
        32,
        64,
        # 128,
        # 256,
        # 512,
        # 1024,
    ]:
        INITIAL_BIT_DIFFICULTY = 18  # todo avoid base_difficulty, use bit_difficulty, better even linear_difficulty
        INITIAL_BASE_DIFFICULTY = round(INITIAL_BIT_DIFFICULTY / math.log2(base))
        ADJUSTMENT_INTERVAL = 2

        blockchain = Blockchain(
            initial_base_difficulty=INITIAL_BASE_DIFFICULTY,
            target_block_time=1,
            # base=BASE, # todo don't use base as a property of blockchain, block etc.
            adjustment_interval=ADJUSTMENT_INTERVAL  # todo should it be a property of blockchain?
        )

        for i in range(5):
            blockchain.add_block(Block(i, time.time(), f"Block {i} Data"))

        blockchains[base] = blockchain

    plot_blockchain_statistics(blockchains)
