#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import math
import random
import logging

from src.model.block import Block
from src.constants import HASH_BIT_LENGTH, NONCE_BIT_LENGTH, BASE, HEXADECIMAL_BASE, SHA256_ENCODING
from src.logging_utils import log_mined_block

class ProofOfWork:
    @staticmethod
    def calculate_hash(base_hash_data: bytes, nonce: int) -> str:
        sha = hashlib.sha256()
        sha.update(base_hash_data + str(nonce).encode(SHA256_ENCODING))
        return sha.hexdigest()

    @staticmethod
    def find_nonce(block: Block, bit_difficulty: float) -> None:
        try:
            max_nonce = BASE ** NONCE_BIT_LENGTH - 1
            block.nonce = random.randint(0, max_nonce)
            target_value = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
            base_hash_data = (str(block.index) + str(block.timestamp) + str(block.data) + str(block.previous_hash)).encode(SHA256_ENCODING)

            while True:
                block.hash = ProofOfWork.calculate_hash(base_hash_data, block.nonce)
                if int(block.hash, HEXADECIMAL_BASE) < target_value:
                    break
                block.nonce += 1

            log_mined_block(block)
        except Exception as e:
            logging.error(f"Error finding nonce: {e}")

    @staticmethod
    def validate_proof(block: Block, bit_difficulty: float) -> bool:
        target_value: float = math.pow(BASE, HASH_BIT_LENGTH - bit_difficulty) - 1
        hash_value: int = int(block.hash, HEXADECIMAL_BASE)
        return hash_value < target_value


