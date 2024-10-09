#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a logging_utils.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import logging
import colorama

class ColorFormatter(logging.Formatter):
    def format(self, record):
        # Check for null pointer references and other potential issues
        assert record is not None, "Record cannot be null"
        assert record.msg is not None, "Record message cannot be null"
        assert record.levelname is not None, "Record levelname cannot be null"

        log_colors = {
            'DEBUG': '\033[94m',  # Blue
            'INFO': '\033[92m',  # Green
            'WARNING': '\033[93m',  # Yellow
            'ERROR': '\033[91m',  # Red
            'CRITICAL': '\033[95m'  # Magenta
        }
        reset_color = '\033[0m'
        log_color = log_colors.get(record.levelname, reset_color)
        record.msg = f"{log_color}{record.msg}{reset_color}"
        return super().format(record)


def log_mined_block(block):
    assert block is not None, "Block cannot be null"
    assert block.index is not None, "Block index cannot be null"
    assert block.hash is not None, "Block hash cannot be null"
    logger = logging.getLogger()
    logger.info(f"Block mined: {block.index} with hash {block.hash}")


def log_time(average_time, expected_time):
    logger = logging.getLogger()
    assert average_time is not None, "Actual time cannot be null"
    assert expected_time is not None, "Expected time cannot be null"
    logger.info(f"Average time: {average_time}, Expected time: {expected_time}")


def log_validity(blockchain):
    """
    Log the validity of the given blockchain.
    :param blockchain: The blockchain to check. Must not be null.
    """
    assert blockchain is not None, "Blockchain cannot be null"
    logger = logging.getLogger()
    assert logger is not None, "Logger cannot be null"
    is_valid = blockchain.is_chain_valid()
    assert is_valid is not None, "Blockchain validity cannot be null"
    logger.info(f"Blockchain validity: {is_valid}")
