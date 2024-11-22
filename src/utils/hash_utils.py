#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
from src.constants import ENCODING

def calculate_hash(index: int, timestamp: float, data: str, previous_hash: str, nonce: int) -> str:
    """Compute the hash of the block by combining the various attributes together.

    Args:
        index (int): The position of the block in the blockchain.
        timestamp (float): The time at which the block was created.
        data (str): The data contained within the block.
        previous_hash (str): The hash of the previous block in the chain.
        nonce (int): The nonce for the proof of work algorithm.

    Returns:
        str: The hash of the block as a hexadecimal string.
    """
    sha = hashlib.sha256()
    data_to_hash = (
        str(index) +
        str(timestamp) +
        str(data) +
        str(previous_hash) +
        str(nonce)
    ).encode(ENCODING)
    sha.update(data_to_hash)
    return sha.hexdigest()
