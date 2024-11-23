#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
from src.constants import ENCODING

# def calculate_hash(index: int, timestamp: float, data: str, previous_hash: str, nonce: int) -> str: # todo make it take Block as an argument
#     """Compute the hash of the block by combining the various attributes together.
#
#     This function takes the attributes of a block, combines them together in a
#     single string, and then computes the SHA256 hash of that string. The resulting
#     hash is then returned as a hexadecimal string.
#
#     The attributes of the block used to compute the hash are:
#     - The index of the block in the blockchain
#     - The timestamp of when the block was created
#     - The data stored in the block
#     - The hash of the previous block in the chain
#     - The nonce for the proof of work algorithm
#
#     Args:
#         index (int): The position of the block in the blockchain.
#         timestamp (float): The time at which the block was created.
#         data (str): The data contained within the block.
#         previous_hash (str): The hash of the previous block in the chain.
#         nonce (int): The nonce for the proof of work algorithm.
#
#     Returns:
#         str: The hash of the block as a hexadecimal string.
#     """
#     sha = hashlib.sha256()
#     data_to_hash = (
#         str(index) +
#         str(timestamp) +
#         str(data) +
#         str(previous_hash) +
#         str(nonce)
#     ).encode(ENCODING)
#     sha.update(data_to_hash)
#     return sha.hexdigest()


# import hashlib
#
# def calculate_hash(index, timestamp, data, previous_hash, nonce):
#     """
#     Calculate the hash of a block.
#
#     Args:
#         index (int): The index of the block.
#         timestamp (float): The timestamp of the block.
#         data (str): The data of the block.
#         previous_hash (str): The hash of the previous block.
#         nonce (int): The nonce of the block.
#
#     Returns:
#         str: The calculated hash of the block.
#     """
#     value = f"{index}{timestamp}{data}{previous_hash}{nonce}"
#     return hashlib.sha256(value.encode()).hexdigest()


import hashlib

def calculate_hash(index, timestamp, data, previous_hash, nonce):
    """
    Calculate the hash of a block.

    Args:
        index (int): The index of the block.
        timestamp (float): The timestamp of the block.
        data (str): The data of the block.
        previous_hash (str): The hash of the previous block.
        nonce (int): The nonce of the block.

    Returns:
        str: The calculated hash of the block.
    """
    value = f"{index}{timestamp}{data}{previous_hash}{nonce}"
    return hashlib.sha256(value.encode()).hexdigest()


