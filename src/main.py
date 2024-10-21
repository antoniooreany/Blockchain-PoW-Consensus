#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging

from blockchain import Blockchain
from constants import (
    BASE,
    INITIAL_BIT_DIFFICULTY,
    ADJUSTMENT_INTERVAL,
    TARGET_BLOCK_TIME,
    NUMBER_BLOCKS_TO_ADD,
    CLAMP_FACTOR,
    SMALLEST_BIT_DIFFICULTY,
)
from helpers import add_blocks
from logger_singleton import LoggerSingleton
from plotting import plot_blockchain_statistics
from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics

if __name__ == "__main__":
    # Set the logging level to INFO (or WARNING to reduce more output)
    logging.getLogger('matplotlib').setLevel(logging.INFO)

    logger = LoggerSingleton.get_instance().logger

    # Add custom handler to track errors and critical issues
    log_level_counter_handler = LogLevelCounterHandler()  # todo rename
    logger.addHandler(log_level_counter_handler)  # todo rename

    blockchains = {}
    for base in [
        BASE,
        # 4,
        # 8,
        # 16,
    ]:
        blockchain = Blockchain(
            initial_bit_difficulty=INITIAL_BIT_DIFFICULTY,
            adjustment_interval=ADJUSTMENT_INTERVAL,  # todo should it be a property of blockchain?
            target_block_mining_time=TARGET_BLOCK_TIME,
        )

        add_blocks(blockchain=blockchain, number_of_blocks=NUMBER_BLOCKS_TO_ADD, clamp_factor=CLAMP_FACTOR,
                   smallest_bit_difficulty=SMALLEST_BIT_DIFFICULTY)

        # Collect filtered bit difficulties
        # filtered_difficulties = collect_filtered_bit_difficulties(blockchain, ADJUSTMENT_INTERVAL)
        # blockchain.bit_difficulties = filtered_difficulties  # todo ??? should we: Update the blockchain with filtered difficulties for plotting

        log_blockchain_statistics(logger, blockchain)

        blockchains[base] = blockchain

    plot_blockchain_statistics(blockchains)

    log_level_counter_handler.print_log_counts()
