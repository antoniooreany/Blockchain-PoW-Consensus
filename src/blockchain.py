# # #   Copyright (c) 2024, Anton Gorshkov
# # #   All rights reserved.
# # #   This code is for a blockchain.py and its unit tests.
# # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import time

from block import Block
from constants import HASH_BIT_LENGTH, GENESIS_BLOCK_HASH, BASE
from helpers import create_genesis_block
from logging_utils import configure_logging
from logging_utils import log_validity
from proof_of_work import ProofOfWork
from src.helpers import adjust_difficulty


class Blockchain:
    def __init__(self, initial_bit_difficulty, adjustment_interval, target_block_mining_time):
        self.logger = configure_logging()
        genesis_block = create_genesis_block(initial_bit_difficulty)
        self.blocks = [genesis_block]
        # self.chain = []
        self.chain = [genesis_block]
        self.bit_difficulties = [initial_bit_difficulty]
        self.adjustment_interval = adjustment_interval
        self.target_block_mining_time = target_block_mining_time
        # self.mining_times = []
        self.mining_times = [0.0]

    def get_latest_block(self) -> Block:
        return self.blocks[-1] if self.blocks else None

    def add_block(self, new_block: Block, clamp_factor, smallest_bit_difficulty) -> None:
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else GENESIS_BLOCK_HASH
        start_time = time.time()
        ProofOfWork.find_nonce(new_block, self.bit_difficulties[-1])
        end_time = time.time()
        actual_mining_time = end_time - start_time

        if not ProofOfWork.validate_proof(new_block, self.bit_difficulties[-1]):
            self.logger.error(f"Block {new_block.index} was mined with a hash that does not meet the difficulty")
            self.logger.error(f"Block hash: {new_block.hash}")
            self.logger.error(f"Target value: {(BASE ** (HASH_BIT_LENGTH - self.bit_difficulties[-1])) - 1}")
            return

        self.blocks.append(new_block)
        self.mining_times.append(actual_mining_time)
        self.bit_difficulties.append(self.bit_difficulties[-1])

        # if (len(self.blocks) - 1) % self.adjustment_interval == 0:

        # if len(self.blocks) % self.adjustment_interval == 0:
        #     adjust_difficulty(self, clamp_factor, smallest_bit_difficulty)

        adjust_difficulty(self, clamp_factor, smallest_bit_difficulty)

        log_validity(self)
        self.logger.debug(f"Bit Difficulty: {self.bit_difficulties[-1]}")
        self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")
        self.logger.debug(f"##############################################")

    # def get_average_mining_time(self, num_blocks: int) -> float:
    #     if len(self.blocks) < num_blocks + 1:
    #     # if len(self.blocks) < num_blocks:
    #         return sum(self.mining_times) / len(self.mining_times)
    #     total_time = sum(self.mining_times[-num_blocks:])
    #     return total_time / num_blocks

    def get_average_mining_time(self, num_blocks: int) -> float:
        if len(self.blocks) <= 1:
            return 0.0
        if len(self.blocks) < num_blocks + 1:
            return sum(self.mining_times[1:]) / (len(self.mining_times) - 1)
        total_time = sum(self.mining_times[-num_blocks:])
        return total_time / num_blocks

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not ProofOfWork.validate_proof(current_block, self.bit_difficulties[i]):
                return False

        return True
