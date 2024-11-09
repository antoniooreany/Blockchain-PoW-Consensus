#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging

# from .helpers import add_blocks
# from .logger_singleton import LoggerSingleton
# from .plotting import plot_blockchain_statistics
# from .logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# from .gui import config_gui  # Assuming the code is saved in gui.py

from src.view.logger_singleton import LoggerSingleton
from src.logging_utils import LogLevelCounterHandler
from src.view.gui import config_gui  # Assuming the code is saved in gui.py


# Call the function to open the UI when needed
if __name__ == "__main__":
    # Set the logging level to INFO (or WARNING to reduce more output)
    logging.getLogger('matplotlib').setLevel(logging.INFO)

    logger = LoggerSingleton.get_instance().logger

    # Add custom handler to track errors and critical issues
    log_level_counter_handler = LogLevelCounterHandler()  # todo rename
    logger.addHandler(log_level_counter_handler)  # todo rename

    config_gui()
