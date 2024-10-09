# #   Copyright (c) 2024, Anton Gorshkov
# #   All rights reserved.
# #
# #   This code is for a main.py and its unit tests.
# #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import math
import time
import logging
from blockchain import Block, Blockchain
from logger_singleton import LoggerSingleton
from plotting import plot_blockchain_statistics

if __name__ == "__main__":
    # Set the logging level to INFO (or WARNING to reduce more output)
    logging.getLogger('matplotlib').setLevel(logging.INFO)

    logger = LoggerSingleton.get_instance().logger

    blockchains = {}
    for BASE in [
        2,
        4,
        16,
        # 32,
        # 64,
        # 128,
        # 256,
        # 512,
        # 1024,
    ]:
        INITIAL_BIT_DIFFICULTY = 16
        INITIAL_BASE_DIFFICULTY = round(INITIAL_BIT_DIFFICULTY / math.log2(BASE))
        ADJUSTMENT_INTERVAL = 3

        blockchain = Blockchain(
            initial_difficulty=INITIAL_BASE_DIFFICULTY,
            target_block_time=1,
            base=BASE,
            adjustment_interval=ADJUSTMENT_INTERVAL
        )

        for i in range(9):
            blockchain.add_block(Block(i, time.time(), f"Block {i} Data"))

        blockchains[BASE] = blockchain

    plot_blockchain_statistics(blockchains)
