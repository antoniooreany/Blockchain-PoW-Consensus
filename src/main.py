#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import logging
# from src.utils.logger_singleton import LoggerSingleton
from src.utils.logging_utils import LogLevelCounterHandler
from src.view.gui import config_gui
from src.view.plotting import plot_blockchain_statistics

if __name__ == "__main__":
    logging.getLogger('matplotlib').setLevel(logging.INFO)
    # logger = LoggerSingleton.get_instance().logger
    log_level_counter_handler = LogLevelCounterHandler()
    # logger.addHandler(log_level_counter_handler)

    config_gui()
