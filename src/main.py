#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# path: src/main.py

import logging
from src.utils.logger_singleton import LoggerSingleton
from src.utils.logging_utils import LogLevelCounterHandler
from src.view.gui import config_gui

if __name__ == "__main__":
    logging.getLogger('matplotlib').setLevel(logging.INFO)
    logger = LoggerSingleton.get_instance().logger
    log_level_counter_handler = LogLevelCounterHandler()
    logger.addHandler(log_level_counter_handler)

    try:
        logger.info("Starting the GUI application.")
        config_gui()  # Start the GUI
    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C). Exiting gracefully.")
        # Perform any necessary cleanup here
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # Add any additional logging or error handling as needed
    finally:
        log_level_counter_handler.print_log_counts()
        logger.info("Application exiting.")
