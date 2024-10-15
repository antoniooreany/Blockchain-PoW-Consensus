#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import logging
import math
import time

from block import Block, HASH_BIT_LENGTH
from src.logging_utils import log_validity
from src.proof_of_work import ProofOfWork


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


# def collect_filtered_bit_difficulties(blockchain, adjustment_interval):
#     # Remove the last bit difficulty of the adjustment interval,
#     # to avoid having +1 at the end of each adjustment interval.
#     # Filter out the bit difficulties for the proper plotting.
#     filtered_bit_difficulties = []
#     for i, bit_difficulty in enumerate(blockchain.bit_difficulties):
#         if (i + 1) % adjustment_interval != 0:
#             filtered_bit_difficulties.append(bit_difficulty)
#     return filtered_bit_difficulties


def collect_filtered_bit_difficulties(blockchain, adjustment_interval):
    filtered_bit_difficulties = []
    current_difficulty = blockchain.bit_difficulties[0]  # Start with the first difficulty

    for i in range(1, len(blockchain.bit_difficulties)):
        filtered_bit_difficulties.append(current_difficulty)
        if i % adjustment_interval == 0:
            # Only update difficulty at the adjustment interval, not before
            current_difficulty = blockchain.bit_difficulties[i]

    # Ensure the filtered difficulties match the length of mining times
    return filtered_bit_difficulties[:len(blockchain.actual_mining_times)]


class Blockchain:
    def __init__(self, initial_bit_difficulty: float, adjustment_interval: int, target_mining_time: float) -> None:
        # self.start_time = time.time()  # Initialize start_time todo should be initialized here?
        self.blocks = []  # the same as self.chain
        # self.blocks = [create_genesis_block()]  #  todo should genesis be created here instead in main.py?
        self.bit_difficulties: list[float] = [initial_bit_difficulty]
        # self.initial_bit_difficulty = initial_bit_difficulty  # todo do we need it?
        self.adjustment_interval = adjustment_interval  # todo do we need it? isn't enough to use only bit_difficulties?
        self.target_mining_time = target_mining_time
        self.actual_mining_times = []  # Initialize mining_times
        self.logger = logging.getLogger(__name__)  # todo should be initialized here?

        # # Create the genesis block todo should be created here, not in main.py
        # genesis_block = create_genesis_block()
        # self.add_block(genesis_block, clamp_factor=2, smallest_bit_difficulty=4)  # Example values for clamp_factor and smallest_bit_difficulty
        # log_mined_block(genesis_block)

    def mine_blocks(self, number_of_blocks: int, clamp_factor: float,
                    smallest_bit_difficulty: float) -> None:  # todo should it be moved to main.py?
        for i in range(1, number_of_blocks):
            block = Block(i, time.time(), f"Block {i} Data")  # todo add data is not yet checked for validity,
            # todo should be checked in the more sophisticated implementation
            self.add_block(block, clamp_factor, smallest_bit_difficulty)  # todo smallest_bit_difficulty

    def get_latest_block(self) -> Block:
        return self.blocks[-1] if self.blocks else None

    def add_block(self, new_block: Block, clamp_factor: float, smallest_bit_difficulty: float) -> None:
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else '0'  # todo '0' for the Genesis block
        start_time: float = time.time()  # todo can be taken from new_block.timestamp
        new_block.mine(self.bit_difficulties[-1])  # Use the last difficulty value
        end_time: float = time.time()  # todo can be taken from new_block.timestamp
        actual_mining_time: float = end_time - start_time

        self.blocks.append(new_block)
        self.actual_mining_times.append(actual_mining_time)
        self.bit_difficulties.append(self.bit_difficulties[-1])  # Use the last difficulty value

        if len(self.blocks) % self.adjustment_interval == 0:
            self.adjust_difficulty(clamp_factor, smallest_bit_difficulty)  # todo smallest_bit_difficulty

        is_blockchain_valid = self.is_chain_valid()  # todo if not valid, don't add block
        log_validity(is_blockchain_valid)  # todo why invalid?

        self.logger.debug(f"Bit Difficulty: {self.bit_difficulties[-1]}")
        self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")
        self.logger.debug(f"##############################################")

    def get_average_mining_time(self, num_blocks: int) -> float:
        if len(self.blocks) < num_blocks + 1:  # Ensure there are enough blocks to average
            return sum(self.actual_mining_times) / len(self.actual_mining_times)
        total_time = sum(self.actual_mining_times[-num_blocks:])  # Only consider the last `num_blocks` mining times
        return total_time / num_blocks

    def adjust_difficulty(
            self,
            clamp_factor: float,
            smallest_bit_difficulty: float,
    ) -> None:  # todo only adjust once per adjustment_interval blocks
        average_mining_time: float = self.get_average_mining_time(self.adjustment_interval)
        logging.debug(
            f"Average mining time: {average_mining_time}, "
            f"Target mining time: {self.target_mining_time}"
        )

        # Calculate the adjustment factor
        adjustment_factor: float = self.target_mining_time / average_mining_time
        logging.debug(f"Adjustment factor: {adjustment_factor}")

        last_bit_difficulty: float = self.bit_difficulties[-1]

        # Ensure adjustment_factor is greater than 0 to avoid math domain error
        if adjustment_factor > 0:
            log_adjustment_factor = math.log2(adjustment_factor)
            clamped_log_adjustment_factor = clamp(log_adjustment_factor, clamp_factor)
            new_bit_difficulty = max(smallest_bit_difficulty, last_bit_difficulty + clamped_log_adjustment_factor)
        else:
            new_bit_difficulty = smallest_bit_difficulty

        self.bit_difficulties.append(new_bit_difficulty)
        # self.start_time = time.time()  # todo should be updated here, not in the add_block: before mine?

        # Log intermediate results
        avg_mining_time = self.get_average_mining_time(self.adjustment_interval)
        self.logger.info(
            f"Average mining time for the last {self.adjustment_interval} blocks: "
            f"{avg_mining_time:.25f} seconds"
        )
        self.logger.info(
            f"Indices of the last {self.adjustment_interval} blocks: "
            f"{list(range(len(self.blocks) - self.adjustment_interval + 1, len(self.blocks) + 1))}"
        )
        self.logger.info(f"New difficulty: {new_bit_difficulty}")

    # def is_chain_valid(self) -> bool:
    #     for i in range(1, len(self.blocks)):
    #         current_block: Block = self.blocks[i]
    #         previous_block: Block = self.blocks[i - 1]
    #
    #         if current_block.hash != current_block.calculate_hash():  # todo false
    #             return False
    #
    #         if current_block.previous_hash != previous_block.hash:  # todo false
    #             return False
    #
    #         if not ProofOfWork.validate_proof(current_block,
    #                                           self.bit_difficulties[i], ):  # todo check if this is correct?
    #             return False
    #
    #     return True

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.blocks)):
            current_block: Block = self.blocks[i]
            previous_block: Block = self.blocks[i - 1]

            if current_block.hash != current_block.calculate_hash():
                self.logger.error(f"Block {i} has an invalid hash.")
                return False

            if current_block.previous_hash != previous_block.hash:
                self.logger.error(f"Block {i} has an invalid previous hash.")
                return False

            # if not ProofOfWork.validate_proof(current_block, self.bit_difficulties[i]):
            #     self.logger.error(f"Block {i} has an invalid proof of work.")
            #     return False

            self.logger.error(
                f"Block index: {i} has an invalid proof of work. \n"  # todo i + 1 or i?
                f"Bit difficulty: {self.bit_difficulties[i]}, \n"
                # f"Target value: {hex(int(math.pow(2, 256 - self.bit_difficulties[i]) - 1))}, \n"
                f"Block nonce: {current_block.nonce}, \n"
                f"Block hash: {current_block.hash}, \n"
                f"Block int_hash: {int(current_block.hash, 16)}, \n"
                # Calculate the target value based on difficulty
                # max_target_hash_value: float = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1  
                f"max_target_hash: {(math.pow(2, HASH_BIT_LENGTH - self.bit_difficulties[i]) - 1)}, \n"
                f"int_max_target_hash: {(int(math.pow(2, HASH_BIT_LENGTH - self.bit_difficulties[i]) - 1))}, \n"
                f"hex_int_max_target_hash: {hex(int(math.pow(2, HASH_BIT_LENGTH - self.bit_difficulties[i]) - 1))}, \n"
                f"valid = {int(current_block.hash, 16) < int(math.pow(2, HASH_BIT_LENGTH - self.bit_difficulties[i]) - 1)}, \n"
                f"diff = {int(current_block.hash, 16) - int(math.pow(2, HASH_BIT_LENGTH - self.bit_difficulties[i]) - 1)}, \n"
                f"ratio = {int(current_block.hash, 16) / int(math.pow(2, HASH_BIT_LENGTH - self.bit_difficulties[i]) - 1)}, \n"
            )
            if not ProofOfWork.validate_proof(current_block, self.bit_difficulties[i]):  # todo i or (i-1)?
                return False

        return True

    # def get_average_block_creation_time(self) -> float:
    #     if not self.actual_mining_times:
    #         return 0
    #     return sum(self.actual_mining_times) / len(self.actual_mining_times)
