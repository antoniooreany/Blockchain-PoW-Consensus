# # #   Copyright (c) 2024, Anton Gorshkov
# # #   All rights reserved.
# # #   This code is for a blockchain.py and its unit tests.
# # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import time
from venv import logger

from src.model.block import Block
from ..constants import HASH_BIT_LENGTH, GENESIS_BLOCK_HASH, BASE, DEFAULT_PRECISION
# from helpers import create_genesis_block
from src.utils.logging_utils import configure_logging
from src.utils.logging_utils import log_validity
from src.controller.proof_of_work import ProofOfWork
from src.constants import GENESIS_BLOCK_PREVIOUS_HASH, GENESIS_BLOCK_DATA
from src.controller.helpers import adjust_difficulty
from src.utils.logging_utils import log_mined_block


# class Blockchain:
#     def __init__(
#             self,
#             initial_bit_difficulty,
#             target_block_mining_time,
#             adjustment_block_interval,
#             number_blocks_to_add,
#             clamp_factor,
#             smallest_bit_difficulty,
#             number_blocks_slice,
#     ):
#         self.logger = configure_logging()
#
#         self.initial_bit_difficulty = initial_bit_difficulty
#         self.target_block_mining_time = target_block_mining_time
#         self.adjustment_block_interval = adjustment_block_interval
#         self.number_blocks_to_add = number_blocks_to_add
#         self.clamp_factor = clamp_factor
#         self.smallest_bit_difficulty = smallest_bit_difficulty
#         # self.slice_factor = slice_factor
#         # self.number_blocks_slice = int(number_blocks_to_add / slice_factor) if slice_factor != 0 else 0
#         self.number_blocks_slice = number_blocks_slice
#
#         self.block_indexes = list(range(number_blocks_to_add + 1))
#
#         self.bit_difficulties = [initial_bit_difficulty]
#
#         # genesis_block = create_genesis_block(self, initial_bit_difficulty)  # todo not introducing the create_genesis_block method
#         genesis_block = Block(0, 0, time.time(), GENESIS_BLOCK_DATA,
#                               GENESIS_BLOCK_PREVIOUS_HASH)  # todo intentionally generalized, I can see more pros than cons.
#         # todo Shouldn't be done in the generic case?
#
#         self.blocks = [genesis_block]  # todo duplicate of self.chain. Fix it
#         self.chain = [genesis_block]  # todo duplicate of self.blocks. Fix it
#
#         log_mined_block(genesis_block)
#         log_validity(self)
#         self.logger.debug(
#             f"Actual mining time for block {genesis_block.index}: {0.0:{DEFAULT_PRECISION}f} seconds")  # todo ugly, generalize it
#         self.logger.debug(f"")
#
#         self.mining_times = [0.0]  # todo generalize it, applying check mining time for the Genesis Block
#         # self.mining_times: list[float] = []  # todo generalize it, applying check mining time for the Genesis Block
#
#         logger.debug(f"Blockchain created")
#         logger.debug(f"")
#
#
#
#     def add_block(self, new_block: Block, clamp_factor, smallest_bit_difficulty) -> None:
#         new_block.previous_hash = self.get_latest_block().hash if self.blocks else GENESIS_BLOCK_HASH
#
#         new_block.timestamp = time.time()  # Set the timestamp at the time of block creation
#
#         ProofOfWork.find_nonce(new_block, self.bit_difficulties[-1])
#
#         actual_mining_time = new_block.timestamp - self.get_latest_block().timestamp
#
#
#         if not ProofOfWork.validate_proof(new_block, self.bit_difficulties[-1]):
#             self.logger.error(f"Block {new_block.index} was mined with a hash that does not meet the difficulty")
#             self.logger.error(f"Block hash: {new_block.hash}")
#             self.logger.error(f"Target value: {(BASE ** (HASH_BIT_LENGTH - self.bit_difficulties[-1])) - 1}")
#             return
#
#         self.blocks.append(new_block)
#         self.mining_times.append(actual_mining_time)
#         self.bit_difficulties.append(self.bit_difficulties[-1])
#
#         adjust_difficulty(self, clamp_factor, smallest_bit_difficulty)
#
#         log_validity(self)
#         self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.{DEFAULT_PRECISION}f} seconds")
#         self.logger.debug(f"")




class Blockchain:
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

        self.block_indexes = list(range(number_blocks_to_add + 1))

        self.bit_difficulties = [initial_bit_difficulty]

        genesis_block = Block(0, 0, GENESIS_BLOCK_DATA, time.time(), GENESIS_BLOCK_PREVIOUS_HASH)

        self.blocks = [genesis_block]
        self.chain = [genesis_block]

        log_mined_block(genesis_block)
        log_validity(self)

        # self.mining_times = [] # todo make it [0.0] to avoid the check for the Genesis Block
        self.mining_times = [0.0] # todo make it [0.0] to avoid the check for the Genesis Block

        logger.debug(f"Blockchain created")
        logger.debug(f"")

    def add_block(self, new_block: Block, clamp_factor, smallest_bit_difficulty) -> None:
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else GENESIS_BLOCK_HASH
        ProofOfWork.find_nonce(new_block, self.bit_difficulties[-1])
        new_block.timestamp = time.time()  # Set the timestamp at the time of block creation
        actual_mining_time = new_block.timestamp - self.get_latest_block().timestamp

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
        self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.{DEFAULT_PRECISION}f} seconds")
        self.logger.debug(f"")




    def get_latest_block(self) -> Block:
        return self.blocks[-1] if self.blocks else None

    def get_average_mining_time(self, num_last_blocks: int) -> float:
        """
        Calculate the average mining time for the last `num_blocks` blocks.

        Args:
        num_blocks: The number of blocks to calculate the average mining time for.

        Returns:
        The average mining time for the last `num_blocks` blocks.
        If the number of blocks in the blockchain is less than or equal to 1,
        or if the blockchain has less than `num_blocks+1` blocks, then
        the average mining time for all blocks (except the Genesis Block) is returned.
        """
        if len(self.blocks) <= 1:  # in the case of the Genesis Block
            return 0.0
        if len(self.blocks) < num_last_blocks + 1:  # (+1) to exclude the Genesis Block from the calculation
            return sum(self.mining_times[1:]) / (len(self.mining_times) - 1)
            # return sum(self.mining_times[1:]) / (len(self.mining_times)+1)
        total_time = sum(self.mining_times[-num_last_blocks:])
        return total_time / num_last_blocks

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
