#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import logging
import math
import time

from src.model.block import Block
from src.constants import HASH_BIT_LENGTH, BASE, DEFAULT_PRECISION, AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY, \
    REVERSED_ADJUSTMENT_FACTOR_KEY
from src.utils.logging_utils import configure_logging
from src.utils.logging_utils import log_validity
from src.controller.proof_of_work import ProofOfWork
from src.constants import GENESIS_BLOCK_PREVIOUS_HASH, GENESIS_BLOCK_DATA
from src.utils.logging_utils import log_mined_block
from src.utils.hash_utils import calculate_block_hash


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

        self.initial_bit_difficulty: float = initial_bit_difficulty  # The initial difficulty level of the blockchain.
        self.target_block_mining_time: float = target_block_mining_time  # The target time to mine a block in seconds.
        self.adjustment_block_interval: int = adjustment_block_interval  # The number of blocks to wait before adjusting the difficulty.
        self.number_blocks_to_add: int = number_blocks_to_add  # The number of blocks to add to the blockchain.
        self.clamp_factor: float = clamp_factor  # The factor to clamp the adjustment of the difficulty.
        self.smallest_bit_difficulty: float = smallest_bit_difficulty  # The smallest bit difficulty that we can adjust to.
        self.number_blocks_slice: int = number_blocks_slice  # The number of blocks to slice the list of blocks to calculate the statistics.

        self.proof_of_work = ProofOfWork()  # Create an instance of ProofOfWork

        # self.block_indexes: list[int] = list(range(number_blocks_to_add + 1))

        genesis_block: Block = Block(
            bit_difficulty=0,  # todo it might be initial_bit_difficulty
            index=0,
            data=GENESIS_BLOCK_DATA,
            timestamp=time.time(),
            previous_hash=GENESIS_BLOCK_PREVIOUS_HASH,
        )

        self.blocks: list[Block] = [genesis_block]  # The list of blocks in the blockchain.
        self.chain: list[Block] = [genesis_block]  # The list of blocks in the blockchain.

        log_mined_block(genesis_block)
        log_validity(self)

        self.bit_difficulties: list[float] = [initial_bit_difficulty]  # The list of bit difficulties in the blockchain.

        self.mining_times: list[float] = [0.0]  # avoid the check for the Genesis Block
        # todo ugly, calculate the mining time for the Genesis Block in generic way.

        logging.debug("Blockchain created")
        logging.debug("")

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
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else GENESIS_BLOCK_PREVIOUS_HASH

        # Find a nonce for the new block to satisfy proof of work
        self.proof_of_work.find_nonce(new_block, self.bit_difficulties[-1])

        # Set the timestamp of the new block to the current time
        new_block.timestamp = time.time()

        # Calculate the actual mining time of the new block
        actual_mining_time = new_block.timestamp - self.get_latest_block().timestamp

        # Validate the new block's proof of work
        if not self.proof_of_work.validate_proof(new_block, self.bit_difficulties[-1]):
            # If the block is invalid, log an error and return
            self.logger.error(f"Block {new_block.index} was mined with a hash that does not meet the difficulty")
            self.logger.error(f"Block hash: {new_block.hash}")
            self.logger.error(f"Target value: {(BASE ** (HASH_BIT_LENGTH - self.bit_difficulties[-1])) - 1}")
            return

        # Add the new block to the blockchain
        self.blocks.append(new_block)

        # Append the actual mining time of the new block to the list of mining times
        self.mining_times.append(actual_mining_time)

        # Update the bit difficulties list to include the new block's difficulty
        self.bit_difficulties.append(self.bit_difficulties[-1])

        # Adjust the difficulty of the blockchain
        self.adjust_difficulty(clamp_factor, smallest_bit_difficulty)

        # Log the validity of the blockchain
        log_validity(self)

        # Log the actual mining time of the new block
        self.logger.debug(
            f"Actual mining time for block {new_block.index}: {actual_mining_time:.{DEFAULT_PRECISION}f} seconds")

        # Log a newline for separation in the logs
        self.logger.debug("")

    def get_latest_block(self) -> Block | None:
        """
        Retrieve the latest block from the blockchain.

        Returns:
            Block | None: The latest block if available, otherwise None if the blockchain is empty.

        Notes:
            This function provides a way to access the most recent block in the blockchain.
            If the blockchain has no blocks, it returns None.
        """
        # Check if there are any blocks in the blockchain
        if self.blocks:
            # Return the last block in the list, which is the latest block
            return self.blocks[-1]
        # Return None if the blockchain is empty
        return None

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
            return 0.0  # return 0.0 as the average mining time
        if len(self.blocks) < num_last_blocks + 1:  # (+1) to exclude the Genesis Block from the calculation
            return sum(self.mining_times[1:]) / (len(self.mining_times) - 1)
        total_time: float = sum(
            self.mining_times[-num_last_blocks:])  # sum the mining times of the last `num_last_blocks` blocks
        return total_time / num_last_blocks  # calculate the average mining time

    def is_chain_valid(self) -> bool:
        """
        Validate the blockchain by checking each block's integrity and proof of work.

        This function checks each block in the chain to ensure that its hash matches its calculated hash,
        its previous hash matches the hash of the previous block, and its proof of work is valid.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        # Iterate over each block in the chain, starting from the second block
        for i in range(1, len(self.chain)):
            # Get the current block and the previous block
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]

            # Check if the current block's hash matches its calculated hash
            expected_hash: str = calculate_block_hash(
                index=current_block.index,
                timestamp=current_block.timestamp,
                data=current_block.data,
                previous_hash=current_block.previous_hash,
                nonce=current_block.nonce,
            )
            if current_block.hash != expected_hash:
                logging.error(
                    f"Block with index {current_block.index} "
                    f"has an invalid hash: {current_block.hash}, "
                    f"expected hash: {expected_hash}",
                )
                # If the hash does not match, return False
                return False

            # Check if the current block's previous hash matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                logging.error(
                    f"Block with index {current_block.index} "
                    f"has an invalid previous hash: {current_block.previous_hash}, "
                    f"expected previous hash: {previous_block.hash}",
                )
                # If the previous hash does not match, return False
                return False

            # Validate the proof of work for the current block
            if not self.proof_of_work.validate_proof(current_block, self.bit_difficulties[i]):
                logging.error(
                    f"Block with index {current_block.index} "
                    f"has an invalid proof of work",
                )
                # If the proof of work is invalid, return False
                return False

        # All blocks are valid
        return True

    def adjust_difficulty(self, bit_clamp_factor: float, smallest_bit_difficulty: float) -> None:
        """
        Adjust the difficulty of the blockchain.

        This function is called every time a new block is added to the blockchain.
        It checks if the number of blocks in the blockchain is a multiple of the
        adjustment block interval. If it is, it calculates the average mining time
        of the last adjustment block interval and adjusts the difficulty of the
        blockchain accordingly.

        Args:
            bit_clamp_factor (float): The maximum allowable adjustment factor.
            smallest_bit_difficulty (float): The smallest bit difficulty that we can adjust to.

        Returns:
            None
        """
        if (len(self.blocks) - 1) % self.adjustment_block_interval == 0:
            # Calculate the average mining time of the last adjustment block interval
            average_mining_time_adjustment_interval: float = self.get_average_mining_time(
                self.adjustment_block_interval)
            # Calculate the reversed adjustment factor
            reversed_adjustment_factor: float = average_mining_time_adjustment_interval / self.target_block_mining_time

            # Log the average mining time and the reversed adjustment factor
            self.logger.debug(f"{AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY}: "
                              f"{average_mining_time_adjustment_interval:.{DEFAULT_PRECISION}f} seconds")
            self.logger.debug(f"{REVERSED_ADJUSTMENT_FACTOR_KEY}: {reversed_adjustment_factor:.{DEFAULT_PRECISION}f}")

            # Get the last bit difficulty
            last_bit_difficulty: float = self.bit_difficulties[-1]

            if reversed_adjustment_factor > 0:
                # Calculate the bit adjustment factor
                bit_adjustment_factor: float = math.log2(reversed_adjustment_factor)
                # Clamp the bit adjustment factor
                clamped_bit_adjustment_factor: float = self.proof_of_work.clamp_bit_adjustment_factor(bit_adjustment_factor, bit_clamp_factor)
                # Calculate the new bit difficulty
                new_bit_difficulty: float = max(smallest_bit_difficulty,
                                                last_bit_difficulty - clamped_bit_adjustment_factor)
            else:
                # Set the new bit difficulty to the smallest bit difficulty if the reversed adjustment factor is 0 or negative
                new_bit_difficulty: float = smallest_bit_difficulty

            # Update the last bit difficulty in the blockchain
            self.bit_difficulties[-1] = new_bit_difficulty
