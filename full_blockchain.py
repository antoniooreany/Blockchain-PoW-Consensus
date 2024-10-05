#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a full_blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import hashlib
import time
from venv import logger

import logging
from colorama import Fore, Style, init

MAX_INT = 2 ** 63 - 1

# Initialize colorama
init(autoreset=True)


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        log_message = super().format(record)
        return f"{log_color}{log_message}{Style.RESET_ALL}"


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger


# # Example usage
# if __name__ == "__main__":
#     logger = setup_logger('my_logger')
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")


# class Block:
#     def __init__(self, index: int, timestamp: float, data: str, previous_hash: str = '') -> None:
#         self.index = index
#         self.timestamp = timestamp
#         self.data = data
#         self.previous_hash = previous_hash
#         self.nonce = 0  # Initialize nonce before calculating hash
#         self.hash = self.calculate_hash()
#
#     def calculate_hash(self) -> str:
#         sha = hashlib.sha256()
#         sha.update(
#             (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode(
#                 'utf-8'))
#         return sha.hexdigest()
#
#     def mine_block(self, difficulty: int) -> None:
#         target = '0' * difficulty
#         while self.hash[:difficulty] != target:
#             self.nonce += 1
#             self.hash = self.calculate_hash()
#         logger.info(f"Block mined: {self.hash}")


import hashlib
import time
import random


class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str = '') -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Initialize nonce before calculating hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        sha = hashlib.sha256()
        sha.update(
            (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode(
                'utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty: int) -> None:
        self.nonce = random.randint(0, MAX_INT)  # Start from a random nonce
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        logger.info(f"Block mined: {self.hash}, nonce: {self.nonce}")


class Blockchain:
    def __init__(self, difficulty: int, target_block_time=0.01) -> None:
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.target_block_time = target_block_time  # Target block time in seconds

    @staticmethod
    def create_genesis_block() -> Block:
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.adjust_difficulty()

    def adjust_difficulty(self, coefficient=1.5) -> None:
        if len(self.chain) < 2:
            return  # No adjustment needed for genesis block
        last_block = self.chain[-1]
        prev_block = self.chain[-2]
        time_taken = last_block.timestamp - prev_block.timestamp
        expected_time = self.target_block_time
        logger.info(f"Time taken: {time_taken:.2f}s, Expected time: {expected_time}s")

        if time_taken < expected_time / coefficient:
            self.difficulty += 1
        elif time_taken > expected_time * coefficient and self.difficulty > 1:
            self.difficulty -= 1
        logger.error(f"Difficulty: {self.difficulty}")

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


class ProofOfWork:
    @staticmethod
    def find_nonce(block: Block, difficulty: int) -> int:
        target = '0' * difficulty
        while block.hash[:difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.nonce

    @staticmethod
    def validate_proof(block: Block, difficulty: int) -> bool:
        target = '0' * difficulty
        return block.hash[:difficulty] == target


def log_blockchain_state(blockchain_chain):
    logger.info("")
    logger.info("Blockchain of the current state:")
    for block in blockchain_chain:
        logger.info(
            f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Nonce: {block.nonce}")


if __name__ == "__main__":
    logger = setup_logger()
    blockchain = Blockchain(difficulty=3)  # Set the initial difficulty of the blockchain
    logger.error(f"Difficulty: {blockchain.difficulty}")
    logger.info(f"Blockchain valid? {blockchain.is_chain_valid()}")

    for i in range(1, 10):  # Limit the number of blocks to mine
        blockchain.add_block(Block(i, time.time(), f"Block {i} Data"))
        logger.info(f"Blockchain valid? {blockchain.is_chain_valid()}")
    log_blockchain_state(blockchain.chain)
