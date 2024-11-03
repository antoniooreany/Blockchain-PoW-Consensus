#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
import time

from blockchain import Blockchain
from constants import (
    BASE,
    INITIAL_BIT_DIFFICULTY,
    ADJUSTMENT_BLOCK_INTERVAL,
    TARGET_BLOCK_MINING_TIME,
    NUMBER_BLOCKS_TO_ADD,
    CLAMP_FACTOR,
    SMALLEST_BIT_DIFFICULTY,
)
from helpers import add_blocks
from logger_singleton import LoggerSingleton
from plotting import plot_blockchain_statistics
from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
from ui import config_ui  # Assuming the code is saved in ui.py

# Call the function to open the UI when needed
if __name__ == "__main__":

    # Set the logging level to INFO (or WARNING to reduce more output)
    logging.getLogger('matplotlib').setLevel(logging.INFO)

    logger = LoggerSingleton.get_instance().logger

    # Add custom handler to track errors and critical issues
    log_level_counter_handler = LogLevelCounterHandler()  # todo rename
    logger.addHandler(log_level_counter_handler)  # todo rename

    config_ui()
