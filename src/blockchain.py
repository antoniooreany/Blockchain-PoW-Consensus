#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import logging
import math
import time

from block import Block
from logging_utils import log_validity
from src.proof_of_work import ProofOfWork

HASH_BIT_LENGTH = 256


def clamp(log_adjustment_factor: float, clamp_factor: float) -> float:
    if log_adjustment_factor > clamp_factor:
        log_adjustment_factor = clamp_factor
    elif log_adjustment_factor < -clamp_factor:
        log_adjustment_factor = -clamp_factor
    return log_adjustment_factor


def create_genesis_block() -> Block:
    genesis_block = Block(0, time.time(), "Genesis Block", "0")
    genesis_block.hash = genesis_block.calculate_hash()  # Calculate hash without mining
    return genesis_block


def collect_filtered_bit_difficulties(blockchain, adjustment_interval):
    filtered_bit_difficulties = []
    for i, difficulty in enumerate(blockchain.bit_difficulties):
        if (i + 1) % adjustment_interval != 0:
            filtered_bit_difficulties.append(difficulty)
    return filtered_bit_difficulties


class Blockchain:
    def __init__(self, initial_bit_difficulty, adjustment_interval, target_block_time):
        # self.start_time = time.time()  # Initialize start_time todo do we need this?
        self.blocks = []  # Initialize the blocks list todo fill with genesis block?
        self.chain = []  # Initialize the chain todo fill with genesis block?
        self.bit_difficulties = [initial_bit_difficulty]
        # self.bit_difficulty = initial_bit_difficulty  # Initialize difficulty todo do we need this?
        self.adjustment_interval = adjustment_interval  # Initialize adjustment_interval
        self.target_block_mining_time = target_block_time
        self.mining_times = []  # Initialize mining_times
        # self.blocks_to_adjust = adjustment_interval  # Initialize blocks_to_adjust
        self.logger = logging.getLogger(__name__)

        # # Create the genesis block
        # genesis_block = create_genesis_block()
        # self.add_block(genesis_block, clamp_factor=2, smallest_bit_difficulty=4)  # Example values for clamp_factor and smallest_bit_difficulty
        # log_mined_block(genesis_block)

    def add_blocks(self, number_of_blocks: int, clamp_factor, smallest_bit_difficulty):  # todo move to main.py?
        for i in range(1, number_of_blocks):
            block = Block(i, time.time(), f"Block {i} Data")
            self.add_block(block, clamp_factor, smallest_bit_difficulty)

    def get_latest_block(self) -> Block:
        return self.blocks[-1] if self.blocks else None

    def add_block(self, new_block: Block, clamp_factor, smallest_bit_difficulty) -> None:
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else '0'
        start_time = time.time()
        new_block.mine(self.bit_difficulties[-1])  # Use the last difficulty value
        end_time = time.time()
        actual_mining_time = end_time - start_time

        if not ProofOfWork.validate_proof(new_block, self.bit_difficulties[-1]):
            self.logger.error(f"Block {new_block.index} was mined with a hash that does not meet the difficulty")
            self.logger.error(f"Block hash: {new_block.hash}")
            self.logger.error(f"Target value: {(2 ** (HASH_BIT_LENGTH - self.bit_difficulties[-1])) - 1}")
            return

        self.blocks.append(new_block)
        self.mining_times.append(actual_mining_time)
        self.bit_difficulties.append(self.bit_difficulties[-1])  # Use the last difficulty value

        if len(self.blocks) % self.adjustment_interval == 0:
            self.adjust_difficulty(clamp_factor, smallest_bit_difficulty)  # todo smallest_bit_difficulty

        log_validity(self)
        self.logger.debug(f"Bit Difficulty: {self.bit_difficulties[-1]}")  # Log the bit difficulty
        # self.logger.debug(f"Expected mining time for block {new_block.index}: {self.target_block_time} seconds")
        self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")
        self.logger.debug(f"##############################################")
        # self.logger.info(f"Block mined: {new_block.index} with hash {new_block.hash}")

    def get_average_mining_time(self, num_blocks: int) -> float:
        if len(self.blocks) < num_blocks + 1:  # Ensure there are enough blocks to average
            return sum(self.mining_times) / len(
                self.mining_times)  # Average for available blocks if fewer than num_blocks
        total_time = sum(self.mining_times[-num_blocks:])  # Only consider the last `num_blocks` mining times
        return total_time / num_blocks

    def adjust_difficulty(
            self,
            clamp_factor: float,
            smallest_bit_difficulty: float,
    ) -> None:  # todo only adjust once per adjustment_interval blocks
        average_mining_time: float = self.get_average_mining_time(
            self.adjustment_interval)  # todo Average mining time for the last adjustment_interval blocks
        logging.debug(
            f"Average mining time: {average_mining_time}, Target block mining time: {self.target_block_mining_time}")

        # Calculate the adjustment factor
        adjustment_factor: float = average_mining_time / self.target_block_mining_time  # todo remove ": float"?
        logging.debug(f"Adjustment factor: {adjustment_factor}")

        last_bit_difficulty = self.bit_difficulties[-1]

        # Ensure adjustment_factor is greater than 0 to avoid math domain error
        if adjustment_factor > 0:
            log_adjustment_factor = math.log2(adjustment_factor)
            clamped_log_adjustment_factor = clamp(log_adjustment_factor, clamp_factor)
            new_difficulty = max(smallest_bit_difficulty, last_bit_difficulty - clamped_log_adjustment_factor)
        else:
            # If adjustment_factor is 0 or less, set new_difficulty to the smallest_bit_difficulty
            new_difficulty = smallest_bit_difficulty

        self.bit_difficulties.append(new_difficulty)
        self.start_time = time.time()

        # Log intermediate results
        avg_mining_time = self.get_average_mining_time(self.adjustment_interval)
        self.logger.info(
            f"Average mining time for the last {self.adjustment_interval} blocks: {avg_mining_time:.25f} seconds")
        self.logger.info(
            f"Indices of the last {self.adjustment_interval} blocks: {list(range(len(self.blocks) - self.adjustment_interval + 1, len(self.blocks) + 1))}")
        self.logger.info(f"New difficulty: {new_difficulty}")

    def is_chain_valid(self) -> bool:
        """
        Check if the blockchain is valid or not.

        Iterate through the blockchain and check if the hashes of the blocks match
        the expected hashes. Also, check if the previous hash of the current block
        matches the hash of the previous block.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not ProofOfWork.validate_proof(
                    current_block,
                    self.bit_difficulties[i],  # todo check if this is correct?
            ):
                return False

        return True
