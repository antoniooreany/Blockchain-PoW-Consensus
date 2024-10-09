#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import logging
import time

from block import Block
from logging_utils import log_mined_block, log_time, log_validity


class Blockchain:
    def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2,
                 adjustment_interval: int = 10) -> None:
        self.chain = [self.create_genesis_block()]
        self.difficulty = initial_difficulty
        self.target_block_time = target_block_time
        self.base = base
        self.adjustment_interval = adjustment_interval
        self.mining_times = []
        self.difficulties = []

    def create_genesis_block(self) -> Block:
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.hash = genesis_block.calculate_hash()  # Calculate hash without mining
        log_mined_block(genesis_block)
        log_time(0, 1)
        return genesis_block

    def add_block(self, new_block: Block) -> None:
        if new_block.index == 0:
            return  # Skip mining if it's the genesis block
        new_block.previous_hash = self.get_latest_block().hash
        start_time = time.time()
        new_block.mine(self.difficulty, self.base)
        end_time = time.time()
        actual_mining_time = end_time - start_time
        self.chain.append(new_block)
        self.mining_times.append(actual_mining_time)
        self.difficulties.append(self.difficulty)
        if len(self.chain) % self.adjustment_interval == 0:
            self.adjust_difficulty()
        log_validity(self)
        logger = logging.getLogger('venv')
        logger.debug(f"Difficulty Level[base={self.base}]: {self.difficulty}")
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

    def adjust_difficulty(self) -> None:
        if len(self.chain) < 2:
            return
        average_time = self.get_average_mining_time(self.adjustment_interval)
        expected_time = self.target_block_time
        log_time(average_time, expected_time)
        if average_time < expected_time:
            self.difficulty += 1
        elif average_time > expected_time and self.difficulty > 1:
            self.difficulty -= 1

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
