# # #   Copyright (c) 2024, Anton Gorshkov
# # #   All rights reserved.
# # #   This code is for a blockchain.py and its unit tests.
# # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import time
from venv import logger

from block import Block
from constants import HASH_BIT_LENGTH, GENESIS_BLOCK_HASH, BASE
from helpers import create_genesis_block
from logging_utils import configure_logging
from logging_utils import log_validity
from proof_of_work import ProofOfWork
from src.constants import GENESIS_BLOCK_PREVIOUS_HASH, GENESIS_BLOCK_DATA
from src.helpers import adjust_difficulty
from src.logging_utils import log_mined_block


class Blockchain:
    # def __init__(
    #         self,
    #         initial_bit_difficulty,
    #         target_block_mining_time,
    #         adjustment_block_interval,
    #         number_blocks_to_add,
    #         clamp_factor,
    #         smallest_bit_difficulty,
    #         slice_factor,
    # ):
    #     self.logger = configure_logging()
    #
    #     self.initial_bit_difficulty = initial_bit_difficulty
    #     self.target_block_mining_time = target_block_mining_time
    #     self.adjustment_block_interval = adjustment_block_interval
    #     self.number_blocks_to_add = number_blocks_to_add
    #     self.clamp_factor = clamp_factor
    #     self.smallest_bit_difficulty = smallest_bit_difficulty
    #     self.slice_factor = slice_factor
    #
    #     self.number_blocks_slice = int(number_blocks_to_add / slice_factor) if slice_factor != 0 else 0
    #
    #     self.bit_difficulties = [initial_bit_difficulty]
    #     # genesis_block = create_genesis_block(self, initial_bit_difficulty)
    #     genesis_block = Block(0, 0, time.time(), GENESIS_BLOCK_DATA, GENESIS_BLOCK_PREVIOUS_HASH)
    #
    #     self.blocks = [genesis_block]
    #     self.chain = [genesis_block]  # todo duplicate of self.blocks. Fix it
    #
    #     log_mined_block(genesis_block)
    #     log_validity(self)
    #     self.logger.debug(f"Actual mining time for block {genesis_block.index}: {0.0:.25f} seconds") # todo ugly, fix it
    #     self.logger.debug(f"")
    #
    #     self.mining_times = [0.0]
    #
    #     logger.debug(f"Blockchain created")
    #     logger.debug(f"")


# class Blockchain:
    def __init__(
            self,
            initial_bit_difficulty,
            target_block_mining_time,
            adjustment_block_interval,
            number_blocks_to_add,
            clamp_factor,
            smallest_bit_difficulty,
            number_blocks_slice,
    ):
        self.logger = configure_logging()

        self.initial_bit_difficulty = initial_bit_difficulty
        self.target_block_mining_time = target_block_mining_time
        self.adjustment_block_interval = adjustment_block_interval
        self.number_blocks_to_add = number_blocks_to_add
        self.clamp_factor = clamp_factor
        self.smallest_bit_difficulty = smallest_bit_difficulty
        self.number_blocks_slice = number_blocks_slice

        self.bit_difficulties = [initial_bit_difficulty]
        genesis_block = create_genesis_block(self, initial_bit_difficulty)
        self.blocks = [genesis_block]
        self.chain = [genesis_block]

        log_mined_block(genesis_block)
        log_validity(self)
        self.logger.debug(f"Actual mining time for block {genesis_block.index}: {0.0:.25f} seconds")
        self.logger.debug(f"")

        self.mining_times = [0.0]

        logger.debug(f"Blockchain created")
        logger.debug(f"")



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

        adjust_difficulty(self, clamp_factor, smallest_bit_difficulty)

        log_validity(self)
        self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")
        self.logger.debug(f"")

    def get_average_mining_time(self, num_blocks: int) -> float:
        if len(self.blocks) <= 1:
            return 0.0
        if len(self.blocks) < num_blocks + 1:
            return sum(self.mining_times[1:]) / (len(self.mining_times) - 1)
            # return sum(self.mining_times[1:]) / (len(self.mining_times)+1)
        total_time = sum(self.mining_times[-num_blocks:])
        return total_time / num_blocks

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):  # todo why doesn't work with self.blocks ?
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not ProofOfWork.validate_proof(current_block, self.bit_difficulties[i]):
                return False

        return True
