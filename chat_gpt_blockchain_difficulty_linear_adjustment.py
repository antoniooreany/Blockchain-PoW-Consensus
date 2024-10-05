#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a blockchain_difficulty_adjusted and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import time
import logging


# Setting up logger
def setup_logger() -> logging.Logger:
    logger = logging.getLogger("BlockchainLogger")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger: logging.Logger = setup_logger()


class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str = "") -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        sha = hashlib.sha256()
        sha.update(
            (
                    str(self.index)
                    + str(self.timestamp)
                    + str(self.data)
                    + str(self.previous_hash)
                    + str(self.nonce)
            ).encode("utf-8")
        )
        return sha.hexdigest()

    def mine(self, difficulty: int) -> None:
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        logger.info(f"Block mined: {self.hash} with nonce {self.nonce}")


class Blockchain:
    def __init__(self, initial_difficulty: int, target_block_time: float) -> None:
        self.chain = [self.create_genesis_block()]
        self.difficulty = initial_difficulty
        self.target_block_time = target_block_time  # Target block time in seconds

    @staticmethod
    def create_genesis_block() -> Block:
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, new_block: Block, difficulty_coefficient: float) -> None:
        new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
        new_block.mine(int(self.difficulty))
        self.chain.append(new_block)
        self.adjust_difficulty(difficulty_coefficient)

    def adjust_difficulty(self, difficulty_coefficient) -> None:
        if len(self.chain) < 2:
            return  # No adjustment needed for genesis block
        last_block: Block = self.chain[-1]
        prev_block: Block = self.chain[-2]
        time_taken: float = last_block.timestamp - prev_block.timestamp
        expected_time: float = self.target_block_time  # Expected time in seconds
        logger.info(f"Actual mining time: {time_taken:.2f}s, Expected mining time: {expected_time:.2f}s")

        self.adjust_difficulty_by_coefficient(time_taken, expected_time, difficulty_coefficient)

    def adjust_difficulty_by_coefficient(self, time_taken, expected_time, difficulty_coefficient):
        # Calculate the ratio of actual time to expected time
        ratio = time_taken / expected_time

        # Adjust difficulty smoothly, reducing sudden large jumps
        if ratio < 1.0:  # If the block was mined too fast
            self.difficulty += (1.0 - ratio) * difficulty_coefficient  # Increase difficulty slightly todo why slightly?
        elif ratio > 1.0:  # If the block was mined too slowly
            self.difficulty -= (ratio - 1.0) * difficulty_coefficient  # Decrease difficulty slightly

        # Ensure difficulty stays above 1
        self.difficulty = max(1, self.difficulty)

        logger.info(f"New Difficulty: {self.difficulty}")

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


def mine_blocks(blockchain: Blockchain, num_blocks: int, difficulty_coefficient: float) -> None:
    for i in range(1, num_blocks + 1):
        new_block = Block(i, time.time(), f"Block {i} Data")
        blockchain.add_block(new_block, difficulty_coefficient)
        logger.info(f"Block {i} added to the chain")


if __name__ == "__main__":
    logger.warning("Starting mining process...")

    blockchain: Blockchain = Blockchain(
        initial_difficulty=4,  # Set the initial difficulty, number of leading zeroes
        target_block_time=10,  # Set the target block time, seconds
    )

    mine_blocks(blockchain,
                num_blocks=5,  # Number of blocks to mine
                difficulty_coefficient=0.1,  # Smoothing factor for difficulty adjustment
                )
