#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math
import time
from venv import logger

from block import Block
from logging_utils import log_mined_block, log_time, log_validity


class Blockchain:
    def __init__(
            self,
            initial_base_difficulty,
            target_block_time,
            # base, # todo don't use base as a property of blockchain, block etc.
            adjustment_interval
    ):
        self.chain = []
        self.mining_times = []
        self.base_difficulties = []
        self.bit_difficulties = []
        # self.base = base # todo don't use base as a property of blockchain, block etc.
        self.base_difficulty = initial_base_difficulty
        self.target_block_time = target_block_time
        self.adjustment_interval = adjustment_interval
        self.start_time = time.time()  # Start time for the current period

    def create_genesis_block(self) -> Block:
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.hash = genesis_block.calculate_hash()  # Calculate hash without mining
        log_mined_block(genesis_block)
        log_time(0, 1)
        return genesis_block

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash if self.chain else '0'
        start_time = time.time()
        new_block.mine(
            self.base_difficulty,
            # self.base,
        )
        end_time = time.time()
        actual_mining_time = end_time - start_time
        self.chain.append(new_block)
        self.mining_times.append(actual_mining_time)
        self.base_difficulties.append(self.base_difficulty)
        self.bit_difficulties.append(self.bit_difficulty())

        # Check if difficulty needs to be adjusted
        if len(self.chain) % self.adjustment_interval == 0:
            self.adjust_difficulty()

        log_validity(self)
        logger.debug(f"Bit Difficulty "
                     # f"[base={self.base}]:"
                     f" {self.bit_difficulty()}")
        logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def get_average_mining_time(self, num_blocks: int = 10) -> float:
        if len(self.chain) < num_blocks + 1:
            return self.target_block_time
        total_time = 0.0
        for i in range(-num_blocks, -1):
            total_time += self.chain[i].timestamp - self.chain[i - 1].timestamp
        return total_time / num_blocks

    def adjust_difficulty(self):
        # Time taken to mine the last BLOCKS_TO_ADJUST blocks
        actual_time = time.time() - self.start_time
        expected_time = self.adjustment_interval * self.target_block_time

        # Adjust difficulty
        adjustment_factor = actual_time / expected_time
        self.base_difficulty = max(1, self.base_difficulty * adjustment_factor)

        # print(f"Difficulty adjustment: new difficulty {self.base_difficulty}")

        # Restart the timer for the next period
        self.start_time = time.time()

    def bit_difficulty(self):
        # Logarithmic difficulty
        return math.log2(self.base_difficulty)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
