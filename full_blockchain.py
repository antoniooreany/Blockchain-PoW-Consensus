#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a full_blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


from venv import logger

import hashlib
import time
import random

import logging
from colorama import Fore, Style, init

TARGET_BLOCK_TIME = 0.01

MAX_INT = 2 ** 63 - 1

# Initialize colorama
init(autoreset=True)


class ColorFormatter(logging.Formatter):
    COLORS: dict = {
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


def setup_logger(level=logging.DEBUG, console_level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(console_level)

    # Create formatter
    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger


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

    def mine(self, difficulty: int) -> None:
        self.nonce = random.randint(0, MAX_INT)  # Start from a random nonce
        target = '0' * difficulty
        base_hash_data = (
                str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        ).encode('utf-8')
        while self.hash[:difficulty] != target:
            self.nonce += 1
            sha = hashlib.sha256()
            sha.update(base_hash_data + str(self.nonce).encode('utf-8'))
            self.hash = sha.hexdigest()  # how many letters in that hashcode alphabet? 16
        logger.info(
            f"Mined: Block(index:{self.index}, hash:{self.hash}, prev_hash:{self.previous_hash}, nonce:{self.nonce})")


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
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.adjust_difficulty(difficulty_coefficient)

    def adjust_difficulty(self, difficulty_coefficient) -> None:
        if len(self.chain) < 2:
            return  # No adjustment needed for genesis block
        last_block: Block = self.chain[-1]
        prev_block: Block = self.chain[-2]
        time_taken: float = last_block.timestamp - prev_block.timestamp
        expected_time: float = self.target_block_time  # Expected time in seconds
        logger.error(
            f"Time taken: {time_taken:.2f}s, Expected time: {expected_time}s")  # todo adjust by coefficient = log n (expected_time / time_taken),
        # todo n - number of letters in the hashcode alphabet, e.g. "0b116fa85b68ce2b6445bcb6c986acfdb4d10e31655c9d7ff9eef5e8bf9ba191", -> n = 16

        if time_taken < expected_time / difficulty_coefficient:
            self.difficulty += 1
        elif time_taken > expected_time * difficulty_coefficient and self.difficulty > 1:
            self.difficulty -= 1

        logger.warning(
            "##################################################################################################################################################")

        log_validity(blockchain)

        logger.debug(f"Current difficulty: {self.difficulty}")

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
        target: str = '0' * difficulty
        return block.hash[:difficulty] == target


def log_blockchain_state(blockchain_chain: list) -> None:
    logger.info("")
    logger.info("Current state of the Blockchain:")
    for block in blockchain_chain:
        logger.info(
            f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Nonce: {block.nonce}")


def mine_blocks(blockchain: Blockchain, num_blocks: int, difficulty_coefficient: float) -> None:
    for i in range(1, num_blocks):  # Start from 1 to avoid mining a genesis block twice
        blockchain.add_block(Block(i, time.time(), f"Block {i} Data"), difficulty_coefficient)


def log_validity(blockchain: Blockchain) -> None:
    if blockchain.is_chain_valid():
        logger.info(f"Blockchain valid")
    else:
        logger.error(f"!!!Blockchain invalid!!!")


if __name__ == "__main__":
    logger: logging.Logger = setup_logger()

    blockchain: Blockchain = Blockchain(initial_difficulty=4,
                                        target_block_time=0.01,
                                        # target_block_time=TARGET_BLOCK_TIME,
                                        )  # Set the initial difficulty and target block time
    log_validity(blockchain)
    logger.debug(f"Initial difficulty: {blockchain.difficulty}")

    mine_blocks(blockchain, num_blocks=5, difficulty_coefficient=1.5)
    log_blockchain_state(blockchain.chain)
