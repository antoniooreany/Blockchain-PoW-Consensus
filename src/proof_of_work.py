#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import math
import random
from venv import logger

from block import Block
from src.logging_utils import log_mined_block

HASH_BIT_LENGTH = 256  # The length of the hash in bits
NONCE_BIT_LENGTH = 32  # The length of the nonce in bits


# todo redundant class, move methods to Block class
class ProofOfWork:
    @staticmethod
    def find_nonce(
            block,
            bit_difficulty: float,
    ) -> None:
        max_nonce: int = 2 ** NONCE_BIT_LENGTH - 1  # maximum value for nonce
        block.nonce = random.randint(0, max_nonce)  # Start from a random nonce (int)

        # Calculate the target value based on difficulty
        target_value: float = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1  # todo move to blockchain.py

        # logger.debug(f"target value: {target_value}")
        logger.debug(f"target value: {int(target_value)}")
        logger.debug(f"target value in hex: {hex(int(target_value))}")
        # logger.debug(f"nonce: {block.nonce}")
        # logger.debug(f"nonce / max_nonce: {block.nonce / max_nonce}")

        base_hash_data: bytes = ((str(block.index) +
                                  str(block.timestamp) +
                                  str(block.data) +
                                  str(block.previous_hash))
                                 .encode('utf-8'))

        while True:
            sha: hashlib.sha256 = hashlib.sha256()
            sha.update(base_hash_data + str(block.nonce).encode('utf-8'))
            block.hash = sha.hexdigest()  # Get the hash as a hexadecimal string

            # Convert the hash to an integer
            hash_value: int = int(block.hash, 16)

            # Check if the hash value is less than the target value: if so, the block is mined
            if hash_value < target_value:  # If the hash meets the target value, the block is mined
                break

            block.nonce += 1  # Increment the nonce to try a different hash
        log_mined_block(block)  # todo move to blockchain.py or proof_of_work.py

    @staticmethod
    def validate_proof(block: Block, bit_difficulty: float) -> bool:  # todo move to Block class, where to use it?
        target_value = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1
        return int(block.hash, 16) < target_value
