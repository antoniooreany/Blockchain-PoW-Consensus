#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
from src.constants import ENCODING


def calculate_block_hash(
    index: int, timestamp: float, data: str, previous_block_hash: str, nonce: int
) -> str:
    """Compute the hash of a block by combining its attributes.

    Args:
        index: int: The position of the block in the blockchain.
        timestamp: float: The time at which the block was created.
        data: str: The data contained within the block.
        previous_block_hash: str: The hash of the previous block in the chain.
        nonce: int: The nonce for the proof of work algorithm.

    Returns:
        str: The hash of the block as a hexadecimal string.
    """
    # Validate the arguments
    validate_block_attributes(index=index, timestamp=timestamp, data=data, previous_block_hash=previous_block_hash, nonce=nonce)

    # Combine the arguments into a single string
    data_to_hash: bytes = (
        f"{index}{timestamp}{data}{previous_block_hash}{nonce}"
    ).encode(ENCODING)

    # Compute the hash of the string
    hash_object: hashlib._Hash = hashlib.sha256()
    hash_object.update(data_to_hash)

    # Return the hash as a hexadecimal string
    return hash_object.hexdigest()

# Cleaned up the code by removing unnecessary comments and debugging statements, standardizing variable names, and improving readability.


def validate_block_attributes(
    index: int, timestamp: float, data: str, previous_block_hash: str, nonce: int
) -> None:
    """Validate that all block attributes are not null or empty.

    Args:
        index: int: The position of the block in the blockchain.
        timestamp: float: The time at which the block was created.
        data: str: The data contained within the block.
        previous_block_hash: str: The hash of the previous block in the chain.
        nonce: int: The nonce for the proof of work algorithm.
    """
    for attribute, name in [
        (index, "index"),
        (timestamp, "timestamp"),
        (data, "data"),
        (previous_block_hash, "previous_block_hash"),
        (nonce, "nonce"),
    ]:
        if attribute is None:
            raise ValueError(f"{name}: {attribute!r} cannot be null")
        if isinstance(attribute, str) and not attribute:
            raise ValueError(f"{name}: {attribute!r} cannot be empty")

# Things look good. If any issues arise, please provide a stack trace for further investigation.
