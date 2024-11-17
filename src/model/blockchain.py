#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

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

class Blockchain:
    def __init__(
            self,
            initial_bit_difficulty: float,
            target_block_mining_time: float,
            adjustment_block_interval: int,
            number_blocks_to_add: int,
            clamp_factor: float,
            smallest_bit_difficulty: float,
            number_blocks_slice: int,
    ) -> None:
        """
        Initialize a new blockchain with the given parameters.

        Parameters:
            initial_bit_difficulty (float): The initial difficulty level of the blockchain.
            target_block_mining_time (float): The target time to mine a block in seconds.
            adjustment_block_interval (int): The number of blocks to wait before adjusting the difficulty.
            number_blocks_to_add (int): The number of blocks to add to the blockchain.
            clamp_factor (float): The factor to clamp the adjustment of the difficulty.
            smallest_bit_difficulty (float): The smallest bit difficulty that we can adjust to.
            number_blocks_slice (int): The number of blocks to slice the list of blocks to calculate the statistics.

        Notes:
            The number of blocks to add is the number of blocks to add to the blockchain after the Genesis Block.
            The number of blocks slice is the number of blocks to slice the list of blocks to calculate the statistics.
        """

        self.logger = configure_logging()

        self.initial_bit_difficulty: float = initial_bit_difficulty
        self.target_block_mining_time: float = target_block_mining_time
        self.adjustment_block_interval: int = adjustment_block_interval
        self.number_blocks_to_add: int = number_blocks_to_add
        self.clamp_factor: float = clamp_factor
        self.smallest_bit_difficulty: float = smallest_bit_difficulty
        self.number_blocks_slice: int = number_blocks_slice

        # self.block_indexes: list[int] = list(range(number_blocks_to_add + 1))


        genesis_block: Block = Block(
            bit_difficulty=0, index=0, data=GENESIS_BLOCK_DATA, timestamp=time.time(), previous_hash=GENESIS_BLOCK_PREVIOUS_HASH
        )

        self.blocks: list[Block] = [genesis_block]
        self.chain: list[Block] = [genesis_block]  # todo why do we need it if we have self.blocks? try to remove it

        log_mined_block(genesis_block)
        log_validity(self)

        self.bit_difficulties: list[float] = [initial_bit_difficulty]

        self.mining_times: list[float] = [0.0]  # avoid the check for the Genesis Block todo ugly, calculate the mining time for the Genesis Block in generic way.

        logger.debug("Blockchain created")
        logger.debug("")

    def add_block(
        self,
        new_block: Block,
        clamp_factor: float,
        smallest_bit_difficulty: float
    ) -> None:
        """
        Add a new block to the blockchain, validate it and update the blockchain state.

        Args:
            new_block (Block): The new block to add.
            clamp_factor (float): The factor to clamp the adjustment of the difficulty.
            smallest_bit_difficulty (float): The smallest bit difficulty that we can adjust to.

        Returns:
            None
        """

        # Set the previous hash of the new block to the hash of the latest block in the blockchain
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else GENESIS_BLOCK_HASH
        # Find a nonce for the new block
        ProofOfWork.find_nonce(new_block, self.bit_difficulties[-1])
        # Set the timestamp of the new block to the current time
        new_block.timestamp = time.time()
        # Calculate the actual mining time of the new block
        actual_mining_time = new_block.timestamp - self.get_latest_block().timestamp

        # Validate the new block
        if not ProofOfWork.validate_proof(new_block, self.bit_difficulties[-1]):
            # If the block is invalid, log an error and return
            self.logger.error(f"Block {new_block.index} was mined with a hash that does not meet the difficulty")
            self.logger.error(f"Block hash: {new_block.hash}")
            self.logger.error(f"Target value: {(BASE ** (HASH_BIT_LENGTH - self.bit_difficulties[-1])) - 1}")
            return

        # Add the new block to the blockchain
        self.blocks.append(new_block)
        # Add the actual mining time of the new block to the list of mining times
        self.mining_times.append(actual_mining_time)
        # Update the list of bit difficulties
        self.bit_difficulties.append(self.bit_difficulties[-1])

        # Adjust the difficulty of the blockchain
        adjust_difficulty(self, clamp_factor, smallest_bit_difficulty)

        # Log the validity of the blockchain
        log_validity(self)
        # Log the actual mining time of the new block
        self.logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.{DEFAULT_PRECISION}f} seconds")
        # Log a newline
        self.logger.debug(f"")


    def get_latest_block(self) -> Block | None:
        """
        Get the latest block in the blockchain.

        Returns:
            Block | None: The latest block in the blockchain, or None if the blockchain is empty.
        """
        return self.blocks[-1] if self.blocks else None

    def get_average_mining_time(self, num_last_blocks: int) -> float:
        """
        Calculate the average mining time for the last `num_last_blocks` blocks.

        Args:
            num_last_blocks (int): The number of blocks to calculate the average mining time for.

        Returns:
            float: The average mining time for the last `num_last_blocks` blocks.

        Notes:
            If the number of blocks in the blockchain is less than or equal to 1,
            or if the blockchain has less than `num_last_blocks+1` blocks, then
            the average mining time for all blocks (except the Genesis Block) is returned.
        """
        # If the number of blocks in the blockchain is less than or equal to 1,
        # or if the blockchain has less than `num_last_blocks+1` blocks, then
        # the average mining time for all blocks (except the Genesis Block) is returned
        if len(self.blocks) <= 1:  # in the case of the Genesis Block
            return 0.0
        if len(self.blocks) < num_last_blocks + 1:  # (+1) to exclude the Genesis Block from the calculation
            return sum(self.mining_times[1:]) / (len(self.mining_times) - 1)
        total_time: float = sum(self.mining_times[-num_last_blocks:])  # type hint
        return total_time / num_last_blocks

    def is_chain_valid(self) -> bool:
        """
        Validate the blockchain by checking each block's integrity and proof of work.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        # Iterate over each block in the chain, starting from the second block
        for i in range(1, len(self.chain)):
            # Get the current block and the previous block
            current_block: Block = self.chain[i]  # type hint
            previous_block: Block = self.chain[i - 1]  # type hint

            # Check if the current block's hash matches its calculated hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the current block's previous hash matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                return False

            # Validate the proof of work for the current block
            if not ProofOfWork.validate_proof(current_block, self.bit_difficulties[i]):
                return False

        # All blocks are valid
        return True
