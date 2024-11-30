#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# path: src/model/blockchain.py

import logging
import math
import time

from src.model.block import Block
from src.constants import DEFAULT_PRECISION, AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY, \
    REVERSED_ADJUSTMENT_FACTOR_KEY, GENESIS_BLOCK_BIT_DIFFICULTY
from src.utils.logging_utils import configure_logging
from src.utils.logging_utils import log_validity
from src.controller.proof_of_work import ProofOfWork
from src.constants import GENESIS_BLOCK_PREVIOUS_HASH, GENESIS_BLOCK_DATA
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

        self.logger: logging.Logger = configure_logging()

        self.initial_bit_difficulty: float = initial_bit_difficulty  # The initial difficulty level of the blockchain.
        self.target_block_mining_time: float = target_block_mining_time  # The target time to mine a block in seconds.
        self.adjustment_block_interval: int = adjustment_block_interval  # The number of blocks to wait before adjusting the difficulty.
        self.number_blocks_to_add: int = number_blocks_to_add  # The number of blocks to add to the blockchain.
        self.clamp_factor: float = clamp_factor  # The factor to clamp the adjustment of the difficulty.
        self.smallest_bit_difficulty: float = smallest_bit_difficulty  # The smallest bit difficulty that we can adjust to.
        self.number_blocks_slice: int = number_blocks_slice  # The number of blocks to slice the list of blocks to calculate the statistics.
        self.bit_difficulties: list[float] = [initial_bit_difficulty]  # The list of bit difficulties in the blockchain.
        self.proof_of_work: ProofOfWork = ProofOfWork()  # Create an instance of ProofOfWork

        # Create the Genesis Block
        start_time: float = time.time()
        genesis_block: Block = Block(
            bit_difficulty=GENESIS_BLOCK_BIT_DIFFICULTY,  # todo it might be initial_bit_difficulty
            index=0,
            data=GENESIS_BLOCK_DATA,
            previous_hash=GENESIS_BLOCK_PREVIOUS_HASH,
        )
        self.blocks: list[Block] = [genesis_block]  # The list of blocks in the blockchain.

        log_mined_block(genesis_block)
        log_validity(self)

        self.mining_times: list[float] = [genesis_block.timestamp - start_time]  # avoid the check for the Genesis Block
        # todo ugly, calculate the mining time for the Genesis Block in generic way.

        logging.debug("\n")

    def add_block(self, new_block: Block, clamp_factor: float, smallest_bit_difficulty: float) -> None:
        """
        Add a new block to the blockchain, validate it and update the blockchain state.
        """
        # Record the start time of mining
        mining_start_time = time.time()

        # Set the previous hash of the new block to the hash of the latest block in the blockchain
        new_block.previous_hash = self.get_latest_block().hash if self.blocks else GENESIS_BLOCK_PREVIOUS_HASH

        # Find a nonce for the new block to satisfy proof of work
        self.proof_of_work.find_nonce(new_block, self.bit_difficulties[-1])

        # Update the timestamp to the end of mining
        new_block.timestamp = time.time()
        actual_mining_time = new_block.timestamp - mining_start_time

        # Validate the new block's proof of work
        if not self.proof_of_work.validate_proof(new_block, self.bit_difficulties[-1]):
            self.logger.error(f"Block {new_block.index} was mined with an invalid hash")
            return

        # Add the new block to the blockchain
        self.blocks.append(new_block)

        # Append the actual mining time
        self.mining_times.append(actual_mining_time)

        # Adjust difficulty and log results
        self.bit_difficulties.append(self.bit_difficulties[-1])
        self.adjust_difficulty(clamp_factor, smallest_bit_difficulty)
        self.log_difficulty_anomalies()

        # Log validity and actual mining time
        log_validity(self)
        self.logger.debug(
            f"Actual mining time for block {new_block.index}: {actual_mining_time:.{DEFAULT_PRECISION}f} seconds\n")

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
                f"{average_mining_time_adjustment_interval:.{DEFAULT_PRECISION}f}"
                              f" seconds")
            self.logger.debug(f"{REVERSED_ADJUSTMENT_FACTOR_KEY}: "
                              f"{reversed_adjustment_factor:.{DEFAULT_PRECISION}f}")

            # Get the last bit difficulty
            last_bit_difficulty: float = self.bit_difficulties[-1]

            if reversed_adjustment_factor > 0:
                # Calculate the bit adjustment factor
                bit_adjustment_factor: float = math.log2(reversed_adjustment_factor)
                # Clamp the bit adjustment factor
                clamped_bit_adjustment_factor: float = self.proof_of_work.clamp_bit_adjustment_factor(
                    bit_adjustment_factor, bit_clamp_factor)
                # Calculate the new bit difficulty
                new_bit_difficulty: float = max(
        smallest_bit_difficulty, last_bit_difficulty - clamped_bit_adjustment_factor
                )
            else:
                # Set the new bit difficulty to the smallest bit difficulty if the reversed adjustment factor is 0 or negative
                new_bit_difficulty: float = smallest_bit_difficulty

            # Update the last bit difficulty in the blockchain
            self.bit_difficulties[-1] = new_bit_difficulty

    def log_difficulty_anomalies(self) -> None:
        """
        Logs any anomalies in the difficulty adjustments by comparing the actual bit difficulty values
        to the expected values calculated from the average mining times.

        The function iterates over the blocks in chunks of the adjustment block interval, calculates the
        average mining time for each chunk and the expected bit difficulty from the average mining time.
        If the actual bit difficulty value differs from the expected value, the function logs a warning.

        Returns:
            None
        """
        interval: int = self.adjustment_block_interval
        anomalies_detected: bool = False

        for i in range(interval, len(self.blocks), interval):
            avg_mining_time: float = sum(self.mining_times[i - interval + 1:i + 1]) / interval
            expected_factor: float = avg_mining_time / self.target_block_mining_time

            # Handle invalid expected_factor values
            if expected_factor <= 0:
                self.logger.error(f"Invalid expected_factor: {expected_factor}. Skipping log calculation.")
                continue

            expected_adjustment: float = math.log2(expected_factor)
            clamped_adjustment: float = self.proof_of_work.clamp_bit_adjustment_factor(expected_adjustment,
                                                                                       self.clamp_factor)
            expected_difficulty: float = max(self.smallest_bit_difficulty,
                self.bit_difficulties[i - interval] - clamped_adjustment)

            if abs(self.bit_difficulties[i] - expected_difficulty) > 1e-6:
                self.logger.critical(
                    f"Anomaly detected for blocks {i - interval + 1} to {i}:\n"
                    f"  Average Mining Time: {avg_mining_time:.6f}s\n"
                    f"  Expected Difficulty: {expected_difficulty:.6f}\n"
                    f"  Actual Difficulty: {self.bit_difficulties[i]:.6f}\n"
                )
                anomalies_detected = True

        if not anomalies_detected:
            self.logger.info("No adjust_difficulty anomalies detected")
