#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
import logging
import math
import time

from block import Block
from logging_utils import log_validity


# class Blockchain:
#     def __init__(self, bit_difficulty, adjustment_interval, target_block_time):
#         self.start_time = time.time()  # Initialize start_time
#         self.blocks = []
#         self.bit_difficulties = [bit_difficulty]
#         self.adjustment_interval = adjustment_interval
#         self.target_block_time = target_block_time
#         self.mining_times = []  # Initialize mining_times
#         self.blocks_to_adjust = adjustment_interval  # Initialize blocks_to_adjust
#         self.logger = logging.getLogger(__name__)
#
#         # self.blocks_to_adjust = adjustment_interval  # Initialize blocks_to_adjust
#         # self.chain: list[Block] = []
#         # self.mining_times: list[float] = []
#         # # self.base_difficulties: list[int] = []
#         # self.bit_difficulties: list[float] = []
#         # # self.base = base # todo don't use base as a property of blockchain, block etc.
#         # self.bit_difficulty: int = initial_bit_difficulty
#         # self.target_block_time: float = target_block_time
#         # self.adjustment_interval: int = adjustment_interval
#         # self.start_time: float = time.time()  # Start time for the current period
#
#     def create_genesis_block(self) -> Block:
#         genesis_block = Block(0, time.time(), "Genesis Block", "0")
#         genesis_block.hash = genesis_block.calculate_hash()  # Calculate hash without mining
#         log_mined_block(genesis_block)
#         log_time(0, 1)
#         return genesis_block
#
#     def get_latest_block(self) -> Block:
#         """
#         Get the latest block in the blockchain.
#
#         Returns:
#             Block: The latest block in the blockchain.
#         """
#         return self.blocks[-1] if self.blocks else None
#
#     def add_block(self, new_block: Block) -> None:
#         """
#         Add a block to the blockchain and update the difficulty.
#
#         Args:
#             new_block (Block): The block to be added to the blockchain.
#
#         Returns:
#             None
#         """
#         new_block.previous_hash = self.get_latest_block().hash if self.blocks else '0'
#         start_time = time.time()
#         new_block.mine(self.bit_difficulties[-1])
#         end_time = time.time()
#         actual_mining_time = end_time - start_time
#         self.blocks.append(new_block)
#         self.mining_times.append(actual_mining_time)
#         self.bit_difficulties.append(self.bit_difficulties[-1])  # Use the last difficulty value
#
#         # Check if difficulty needs to be adjusted
#         if len(self.blocks) % self.adjustment_interval == 0:
#             self.adjust_difficulty()
#
#         log_validity(self)
#         logger.debug(f"Bit Difficulty: {self.bit_difficulties[-1]}")
#         logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")
#
#     def get_average_mining_time(self, num_blocks: int = 10) -> float:
#         """
#         Calculate the average mining time for the last num_blocks blocks.
#
#         Args:
#             num_blocks (int): The number of blocks to consider for the average mining time.
#                 Defaults to 10.
#
#         Returns:
#             float: The average mining time in seconds.
#         """
#         if len(self.chain) < num_blocks + 1:
#             return self.target_block_time
#         total_time: float = 0.0
#         for i in range(-num_blocks, -1):
#             total_time += self.chain[i].timestamp - self.chain[i - 1].timestamp
#         return total_time / num_blocks
#
#     def adjust_difficulty(self) -> None:
#         """
#         Adjust the difficulty of the blockchain based on the actual mining time of the last
#         BLOCKS_TO_ADJUST blocks.
#
#         Args:
#             None
#
#         Returns:
#             None
#         """
#         # Time taken to mine the last BLOCKS_TO_ADJUST blocks
#         actual_time: float = time.time() - self.start_time
#         expected_time: float = self.adjustment_interval * self.target_block_time
#
#         # Adjust difficulty
#         adjustment_factor: float = actual_time / expected_time
#         # self.bit_difficulty: float = max(1, self.bit_difficulties[-1] * adjustment_factor)
#         new_bit_difficulty: float = max(1, self.bit_difficulties[-1] * adjustment_factor)
#         self.bit_difficulties.append(new_bit_difficulty)
#
#         # Restart the timer for the next period
#         self.start_time: float = time.time()
#
#         # Log intermediate results
#         avg_mining_time = self.get_average_mining_time(self.adjustment_interval)
#         self.logger.info(f"Average mining time for the last {self.adjustment_interval} blocks: {avg_mining_time:.25f} seconds")
#         self.logger.info(f"Indices of the last {self.adjustment_interval} blocks: {list(range(len(self.blocks) - self.adjustment_interval, len(self.blocks)))}")
#         self.logger.info(f"New difficulty: {new_bit_difficulty}")
#
#     def is_chain_valid(self) -> bool:
#         """
#         Checks if the blockchain is valid by verifying hashes and previous hashes.
#
#         Args:
#             None
#
#         Returns:
#             bool: True if the blockchain is valid, False otherwise
#         """
#         for i in range(1, len(self.blocks)):
#             current_block: Block = self.blocks[i]
#             previous_block: Block = self.blocks[i - 1]
#             if current_block.hash != current_block.calculate_hash():
#                 return False
#             if current_block.previous_hash != previous_block.hash:
#                 return False
#         return True


class Blockchain:
    def __init__(self, bit_difficulty, adjustment_interval, target_block_time):
        self.start_time = time.time()  # Initialize start_time
        self.blocks = []
        self.bit_difficulties = [bit_difficulty]
        self.adjustment_interval = adjustment_interval
        self.target_block_time = target_block_time
        self.mining_times = []  # Initialize mining_times
        self.blocks_to_adjust = adjustment_interval  # Initialize blocks_to_adjust
        self.logger = logging.getLogger(__name__)

    def create_genesis_block(self) -> Block:
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.hash = genesis_block.calculate_hash()  # Calculate hash without mining
        # log_mined_block(genesis_block)
        # log_time(0, 1)
        return genesis_block

    def get_latest_block(self) -> Block:
        return self.blocks[-1] if self.blocks else None

    def add_block(self, new_block: Block) -> None:
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else '0'
        start_time = time.time()
        new_block.mine(self.bit_difficulties[-1])  # Use the last difficulty value
        end_time = time.time()
        actual_mining_time = end_time - start_time
        self.blocks.append(new_block)
        self.mining_times.append(actual_mining_time)
        self.bit_difficulties.append(self.bit_difficulties[-1])  # Use the last difficulty value

        if len(self.blocks) % self.adjustment_interval == 0:
            self.adjust_difficulty()

        log_validity(self)
        self.logger.debug(f"Bit Difficulty: {self.bit_difficulties[-1]}")
        self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")
        self.logger.debug(f"##############################################")
        # self.logger.info(f"Block mined: {new_block.index} with hash {new_block.hash}")

    # def get_average_mining_time(self, num_blocks: int = 10) -> float:
    #     if len(self.blocks) < num_blocks + 1:
    #         return self.target_block_time
    #     total_time: float = 0.0
    #     for i in range(-num_blocks, -1):
    #         total_time += self.blocks[i].timestamp - self.blocks[i - 1].timestamp
    #     return total_time / num_blocks

    def get_average_mining_time(self, num_blocks: int = 5) -> float:
        if len(self.blocks) < num_blocks + 1:
            return sum(self.mining_times) / len(
                self.mining_times)  # Average for available blocks if fewer than num_blocks
        total_time = sum(self.mining_times[-num_blocks:])  # Only consider the last `num_blocks` mining times
        return total_time / num_blocks

    def adjust_difficulty(self) -> None:
        actual_time: float = time.time() - self.start_time
        expected_time: float = self.adjustment_interval * self.target_block_time
        adjustment_factor: float = actual_time / expected_time
        # new_difficulty: float = max(1, self.bit_difficulties[-1] * adjustment_factor)
        # new_difficulty: float = max(1, self.bit_difficulties[-1] / adjustment_factor)
        new_difficulty: float = max(1, self.bit_difficulties[-1] - math.log2(adjustment_factor))
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
        for i in range(1, len(self.blocks)):
            current_block: Block = self.blocks[i]
            previous_block: Block = self.blocks[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
