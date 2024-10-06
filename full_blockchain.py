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

from block import Block

MAX_INT = (2 ** (2 ** (2 ** 3))) - 1  # todo 16^64 - 1 = 2^256 - 1, the maximum value of the nonce

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


def log_mined_block(block: Block) -> None:
    logger.info(
        f"Mined: Block(\n"
        f"                                                     index:{block.index}, \n"
        f"                                                     hash:{block.hash}, \n"
        f"                                                     prev_hash:{block.previous_hash}, \n"
        f"                                                     nonce:{block.nonce}\n)"
        f"                                                     ")


def log_time(actual_time: float, expected_time: float) -> None:
    logger.debug(
        f"Actual mining time: {actual_time:.35f}s,\n "
        f"                                        Expected mining time: {expected_time:.35f}s\n"
    )


def separator(symbol: str = "#", length: int = 50) -> None:
    logger.warning(symbol * length)


class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str = '') -> None:
        self.index = index
        self.timestamp = time.perf_counter()  # Use high precision timer
        # self.timestamp = timestamp
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
        target = '0' * difficulty  # todo Target hash with leading zeroes, can be changed to any float number, meaning the number of leading zeroes
        # todo be rewritten not an integer number of leading zeroes, but as a number, as a maximum barrier (even as a float number) of the hashcode
        # todo to be found by the miner.
        base_hash_data = (
                str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        ).encode('utf-8')
        while self.hash[:difficulty] != target:
            self.nonce += 1
            sha = hashlib.sha256()
            sha.update(base_hash_data + str(self.nonce).encode('utf-8'))
            self.hash = sha.hexdigest()  # how many letters in that hashcode alphabet? 16
        log_mined_block(self)  # todo Mined: Block(


class Blockchain:
    def __init__(self, initial_difficulty: int, target_block_time: float) -> None:
        # logger.debug("#" * 50)
        genesis_block = create_genesis_block()
        self.chain = [genesis_block]
        self.difficulty = initial_difficulty
        self.target_block_time = target_block_time  # Target block time in seconds

    def add_block(self, new_block: Block, difficulty_coefficient: float) -> None:
        new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.adjust_difficulty(difficulty_coefficient)
        log_validity(self)
        logger.debug(f"Difficulty: {self.difficulty}")

    def adjust_difficulty(self, difficulty_coefficient: float) -> None:
        if len(self.chain) < 2:
            return  # No adjustment needed for genesis block
        last_block: Block = self.chain[-1]
        prev_block: Block = self.chain[-2]
        actual_time: float = last_block.timestamp - prev_block.timestamp
        expected_time: float = self.target_block_time  # Expected time in seconds
        log_time(actual_time, expected_time)
        self.adjust_difficulty_by_coefficient(actual_time, expected_time, difficulty_coefficient)

    def adjust_difficulty_by_coefficient(self, time_taken, expected_time, difficulty_coefficient):
        if time_taken < expected_time / difficulty_coefficient:
            self.difficulty += 1
        elif time_taken > expected_time * difficulty_coefficient and self.difficulty > 1:
            self.difficulty -= 1

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def get_latest_block(self) -> Block:
        return self.chain[-1]


def create_genesis_block() -> Block:
    genesis_block = Block(0, time.time(), "Genesis Block", "0")
    log_mined_block(genesis_block)
    actual_time = 0  # Genesis block has no previous block, so actual time is 0
    expected_time = 1  # Set the expected time for the genesis block
    log_time(actual_time, expected_time)
    return genesis_block


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

    blockchain: Blockchain = Blockchain(
        initial_difficulty=3,  # Set the initial difficulty, number of leading zeroes
        target_block_time=1,  # Set the target block time, seconds
    )  # Set the initial difficulty and target block time

    log_validity(blockchain)
    logger.debug(f"Difficulty: {blockchain.difficulty}")

    mine_blocks(blockchain,
                num_blocks=3,  # Number of blocks to mine
                difficulty_coefficient=16,  # The number of leading zeroes in the hashcode
                )
