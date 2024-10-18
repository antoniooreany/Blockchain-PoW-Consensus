#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging

from blockchain import Blockchain, collect_filtered_bit_difficulties
from logger_singleton import LoggerSingleton
from plotting import plot_blockchain_statistics
from src.logging_utils import LogLevelCounterHandler

if __name__ == "__main__":
    # Set the logging level to INFO (or WARNING to reduce more output)
    logging.getLogger('matplotlib').setLevel(logging.INFO)

    logger = LoggerSingleton.get_instance().logger

    # Add custom handler to track errors and critical issues
    log_level_counter_handler = LogLevelCounterHandler()  # todo rename
    logger.addHandler(log_level_counter_handler)  # todo rename

    blockchains = {}
    for base in [
        2,
        # 4,
        # 8,
        # 16,
    ]:
        INITIAL_BIT_DIFFICULTY = 16  # todo use bit_difficulty, better even linear_difficulty
        ADJUSTMENT_INTERVAL = 10
        TARGET_BLOCK_TIME = 0.1
        NUMBER_BLOCKS_TO_ADD = 100

        CLAMP_FACTOR = 2  # todo 2 bits; bin: 0b10, hex: 0x2, dec: 2: max adjustment factor
        SMALLEST_BIT_DIFFICULTY = 4  # todo 4 bits; bin: 0b0000, hex: 0x0, dec: 0: smallest bit difficulty

        blockchain = Blockchain(
            initial_bit_difficulty=INITIAL_BIT_DIFFICULTY,
            adjustment_interval=ADJUSTMENT_INTERVAL,  # todo should it be a property of blockchain?
            target_block_time=TARGET_BLOCK_TIME,
        )
        logger.debug(f"Created: blockchain (base: {base}, initial bit difficulty: {INITIAL_BIT_DIFFICULTY})")
        logger.debug(f"##################")

        # # Create the genesis block todo move to Blockchain class
        # genesis_block = create_genesis_block()
        # log_mined_block(genesis_block)
        # logger.debug(f"##################")

        blockchain.add_blocks(number_of_blocks=NUMBER_BLOCKS_TO_ADD, clamp_factor=CLAMP_FACTOR,
                              smallest_bit_difficulty=SMALLEST_BIT_DIFFICULTY)

        # Collect filtered bit difficulties
        filtered_difficulties = collect_filtered_bit_difficulties(blockchain, ADJUSTMENT_INTERVAL)
        blockchain.bit_difficulties = filtered_difficulties  # Update the blockchain with filtered difficulties

        logger.info(f"Target block time: {TARGET_BLOCK_TIME}")
        average_mining_time_last_half_blocks = blockchain.get_average_mining_time(
            num_blocks=blockchain.blocks.__len__() // 2)
        logger.info(f"Average mining time of the last half of the blockchain: {average_mining_time_last_half_blocks}")

        blockchains[base] = blockchain

    plot_blockchain_statistics(blockchains)

    log_level_counter_handler.print_log_counts()
