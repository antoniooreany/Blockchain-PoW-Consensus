#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a full_blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math
from venv import logger

import time

import logging
from colorama import Fore, Style, init

import hashlib
import random

from block import Block
from blockchain import Blockchain

MAX_NONCE = (2 ** (2 ** (2 ** 3))) - 1  # todo 16^64 - 1 = 2^256 - 1, the maximum value of the nonce

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


def log_validity(blockchain: Blockchain) -> None:
    if blockchain.is_chain_valid():
        logger.info(f"Blockchain valid")
    else:
        logger.error(f"!!!Blockchain invalid!!!")


def log_blockchain_state(blockchain_chain: list) -> None:
    logger.info("")
    logger.info("Current state of the Blockchain:")
    for block in blockchain_chain:
        logger.info(
            f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Nonce: {block.nonce}")


def separator(symbol: str = "#", length: int = 50) -> None:
    logger.warning(symbol * length)


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

    def mine(self, difficulty: int, base: int = 2) -> None:
        self.nonce = random.randint(0, MAX_NONCE)  # Start from a random nonce

        # Set the target number of leading zeros in the chosen numeral system
        target_zeros = '0' * difficulty  # todo why 0?

        base_hash_data = (
                str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        ).encode('utf-8')

        while True:
            sha = hashlib.sha256()
            sha.update(base_hash_data + str(self.nonce).encode('utf-8'))
            self.hash = sha.hexdigest()

            # Convert the hash to the chosen numeral system (base = 2, 4, 8, 16)
            if base == 2:
                # Convert hash to binary
                converted_hash = bin(int(self.hash, 16))[2:].zfill(256)  # ~256 characters
                # logger.debug(f"Converted hash[{base}]: {converted_hash}")
            elif base == 4:
                # Convert hash to quaternary
                converted_hash = oct(int(self.hash, 16))[2:].zfill(128)  # ~128 characters
            # elif base == 8: # todo not possible, because 16/log2(8) = 5.33
            #     # Convert hash to octal
            #     converted_hash = oct(int(self.hash, 16))[2:].zfill(85)  # ~85 characters todo why 85?
            elif base == 16:
                # Use hexadecimal (default)
                converted_hash = self.hash

            # Check leading zeros in the chosen system
            if converted_hash[:difficulty] == target_zeros:  # todo why 0?
                break

            self.nonce += 1

        log_mined_block(self)

#
# class Blockchain:
#     def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2) -> None:
#         self.chain = [self.create_genesis_block()]
#         # self.chain = [create_genesis_block()]
#         self.difficulty = initial_difficulty
#         self.target_block_time = target_block_time  # Target block time in seconds
#         self.base = base  # Base for numeral system
#
#     def create_genesis_block(self) -> Block:
#         genesis_block = Block(0, time.time(), "Genesis Block", "0")
#         log_mined_block(genesis_block)
#         actual_time = 0  # Genesis block has no previous block, so actual time is 0
#         expected_time = 1  # Set the expected time for the genesis block
#         log_time(actual_time, expected_time)
#         return genesis_block
#
#     def add_block(self, new_block: Block, difficulty_coefficient: float) -> None:
#         new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
#         new_block.mine(self.difficulty, self.base)  # Pass the chosen numeral system
#         self.chain.append(new_block)
#         self.adjust_difficulty(difficulty_coefficient)
#         log_validity(self)
#         logger.debug(f"Difficulty[base={self.base}]: {self.difficulty}")
#
#     def get_block_mining_time(self):
#         return self.chain[-1].timestamp - self.chain[-2].timestamp
#
#     def adjust_difficulty(self, difficulty_coefficient: float) -> None:
#         if len(self.chain) < 2:
#             return  # No adjustment needed for genesis block
#         actual_time = self.get_block_mining_time()
#         expected_time: float = self.target_block_time  # Expected time in seconds
#         log_time(actual_time, expected_time)
#         self.adjust_difficulty_by_coefficient(actual_time, expected_time, difficulty_coefficient)  # todo remove self?
#
#     def adjust_difficulty_by_coefficient(self, time_taken, expected_time, difficulty_coefficient):
#         if time_taken < expected_time / difficulty_coefficient:
#             self.difficulty += 1  # todo why += 1?
#         elif time_taken > expected_time * difficulty_coefficient and self.difficulty > 1:
#             self.difficulty -= 1  # todo why -= 1?
#
#     def is_chain_valid(self) -> bool:
#         for i in range(1, len(self.chain)):
#             current_block: Block = self.chain[i]
#             previous_block: Block = self.chain[i - 1]
#             if current_block.hash != current_block.calculate_hash():
#                 return False
#             if current_block.previous_hash != previous_block.hash:
#                 return False
#         return True
#
#     def get_latest_block(self) -> Block:
#         return self.chain[-1]



# class Blockchain:
#     def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2) -> None:
#         self.chain = [self.create_genesis_block()]
#         self.difficulty = initial_difficulty
#         self.target_block_time = target_block_time  # Target block time in seconds
#         self.base = base  # Base for numeral system
#
#     def create_genesis_block(self) -> Block:
#         genesis_block = Block(0, time.time(), "Genesis Block", "0")
#         log_mined_block(genesis_block)
#         actual_time = 0  # Genesis block has no previous block, so actual time is 0
#         expected_time = 1  # Set the expected time for the genesis block
#         log_time(actual_time, expected_time)
#         return genesis_block
#
#     def add_block(self, new_block: Block) -> None:
#         new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
#         new_block.mine(self.difficulty, self.base)  # Pass the chosen numeral system
#         self.chain.append(new_block)
#         self.adjust_difficulty()
#         log_validity(self)
#         logger.debug(f"Difficulty[base={self.base}]: {self.difficulty}")
#
#     def get_average_mining_time(self, num_blocks: int = 10) -> float:
#         if len(self.chain) < num_blocks + 1:
#             return self.target_block_time  # Not enough blocks to calculate average, return target time
#         total_time = 0.0
#         for i in range(-num_blocks, -1):
#             total_time += self.chain[i].timestamp - self.chain[i - 1].timestamp
#         return total_time / num_blocks
#
#     def adjust_difficulty(self) -> None:
#         if len(self.chain) < 2:
#             return  # No adjustment needed for genesis block
#         actual_time = self.get_average_mining_time()
#         expected_time: float = self.target_block_time  # Expected time in seconds
#         log_time(actual_time, expected_time)
#         if actual_time < expected_time:
#             self.difficulty += 1
#         elif actual_time > expected_time and self.difficulty > 1:
#             self.difficulty -= 1
#
#     def is_chain_valid(self) -> bool:
#         for i in range(1, len(self.chain)):
#             current_block: Block = self.chain[i]
#             previous_block: Block = self.chain[i - 1]
#             if current_block.hash != current_block.calculate_hash():
#                 return False
#             if current_block.previous_hash != previous_block.hash:
#                 return False
#         return True
#
#     def get_latest_block(self) -> Block:
#         return self.chain[-1]



# class Blockchain:
#     def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2) -> None:
#         self.chain = [self.create_genesis_block()]
#         self.difficulty = initial_difficulty
#         self.target_block_time = target_block_time  # Target block time in seconds
#         self.base = base  # Base for numeral system
#
#     def create_genesis_block(self) -> Block:
#         genesis_block = Block(0, time.time(), "Genesis Block", "0")
#         log_mined_block(genesis_block)
#         actual_time = 0  # Genesis block has no previous block, so actual time is 0
#         expected_time = 1  # Set the expected time for the genesis block
#         log_time(actual_time, expected_time)
#         return genesis_block
#
#     def add_block(self, new_block: Block) -> None:
#         new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
#         new_block.mine(self.difficulty, self.base)  # Pass the chosen numeral system
#         self.chain.append(new_block)
#         self.adjust_difficulty()
#         log_validity(self)
#         logger.debug(f"Difficulty[base={self.base}]: {self.difficulty}")
#
#     def get_average_mining_time(self, num_blocks: int = 10) -> float:
#         if len(self.chain) < num_blocks + 1:
#             return self.target_block_time  # Not enough blocks to calculate average, return target time
#         total_time = 0.0
#         for i in range(-num_blocks, -1):
#             total_time += self.chain[i].timestamp - self.chain[i - 1].timestamp
#         return total_time / num_blocks
#
#     def adjust_difficulty(self) -> None:
#         if len(self.chain) < 2:
#             return  # No adjustment needed for genesis block
#         actual_time = self.get_average_mining_time()
#         expected_time: float = self.target_block_time  # Expected time in seconds
#         log_time(actual_time, expected_time)
#         if actual_time < expected_time:
#             self.difficulty += 1
#         elif actual_time > expected_time and self.difficulty > 1:
#             self.difficulty -= 1
#
#     def is_chain_valid(self) -> bool:
#         for i in range(1, len(self.chain)):
#             current_block: Block = self.chain[i]
#             previous_block: Block = self.chain[i - 1]
#             if current_block.hash != current_block.calculate_hash():
#                 return False
#             if current_block.previous_hash != previous_block.hash:
#                 return False
#         return True
#
#     def get_latest_block(self) -> Block:
#         return self.chain[-1]


# class Blockchain:
#     def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2) -> None:
#         self.chain = [self.create_genesis_block()]
#         self.difficulty = initial_difficulty
#         self.target_block_time = target_block_time  # Target block time in seconds
#         self.base = base  # Base for numeral system
#
#     def create_genesis_block(self) -> Block:
#         genesis_block = Block(0, time.time(), "Genesis Block", "0")
#         log_mined_block(genesis_block)
#         actual_time = 0  # Genesis block has no previous block, so actual time is 0
#         expected_time = 1  # Set the expected time for the genesis block
#         log_time(actual_time, expected_time)
#         return genesis_block
#
#     def add_block(self, new_block: Block) -> None:
#         new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
#         new_block.mine(self.difficulty, self.base)  # Pass the chosen numeral system
#         self.chain.append(new_block)
#         if len(self.chain) % 10 == 0:
#             self.adjust_difficulty()
#         log_validity(self)
#         logger.debug(f"Difficulty[base={self.base}]: {self.difficulty}")
#
#     def get_average_mining_time(self, num_blocks: int = 10) -> float:
#         if len(self.chain) < num_blocks + 1:
#             return self.target_block_time  # Not enough blocks to calculate average, return target time
#         total_time = 0.0
#         for i in range(-num_blocks, -1):
#             total_time += self.chain[i].timestamp - self.chain[i - 1].timestamp
#         return total_time / num_blocks
#
#     def adjust_difficulty(self) -> None:
#         if len(self.chain) < 2:
#             return  # No adjustment needed for genesis block
#         actual_time = self.get_average_mining_time()
#         expected_time: float = self.target_block_time  # Expected time in seconds
#         log_time(actual_time, expected_time)
#         if actual_time < expected_time:
#             self.difficulty += 1
#         elif actual_time > expected_time and self.difficulty > 1:
#             self.difficulty -= 1
#
#     def is_chain_valid(self) -> bool:
#         for i in range(1, len(self.chain)):
#             current_block: Block = self.chain[i]
#             previous_block: Block = self.chain[i - 1]
#             if current_block.hash != current_block.calculate_hash():
#                 return False
#             if current_block.previous_hash != previous_block.hash:
#                 return False
#         return True
#
#     def get_latest_block(self) -> Block:
#         return self.chain[-1]



class Blockchain:
    def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2, adjustment_interval: int = 10) -> None:
        self.chain = [self.create_genesis_block()]
        self.difficulty = initial_difficulty
        self.target_block_time = target_block_time  # Target block time in seconds
        self.base = base  # Base for numeral system
        self.adjustment_interval = adjustment_interval  # Number of blocks between difficulty adjustments

    def create_genesis_block(self) -> Block:
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        log_mined_block(genesis_block)
        actual_time = 0  # Genesis block has no previous block, so actual time is 0
        expected_time = 1  # Set the expected time for the genesis block
        log_time(actual_time, expected_time)
        return genesis_block

    def add_block(self, new_block: Block) -> None:
        new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
        new_block.mine(self.difficulty, self.base)  # Pass the chosen numeral system
        self.chain.append(new_block)
        if len(self.chain) % self.adjustment_interval == 0:
            self.adjust_difficulty()
        log_validity(self)
        logger.debug(f"Difficulty[base={self.base}]: {self.difficulty}")

    def get_average_mining_time(self, num_blocks: int = 10) -> float:
        if len(self.chain) < num_blocks + 1:
            return self.target_block_time  # Not enough blocks to calculate average, return target time
        total_time = 0.0
        for i in range(-num_blocks, -1):
            total_time += self.chain[i].timestamp - self.chain[i - 1].timestamp
        return total_time / num_blocks

    def adjust_difficulty(self) -> None:
        if len(self.chain) < 2:
            return  # No adjustment needed for genesis block
        actual_time = self.get_average_mining_time(self.adjustment_interval)
        expected_time: float = self.target_block_time  # Expected time in seconds
        log_time(actual_time, expected_time)
        if actual_time < expected_time:
            self.difficulty += 1
        elif actual_time > expected_time and self.difficulty > 1:
            self.difficulty -= 1

    # def is_chain_valid(self) -> bool:
    #     for i in range(1, len(self.chain)):
    #         current_block: Block = self.chain[i]
    #         previous_block: Block = self.chain[i - 1]
    #         if current_block.hash != current_block.calculate_hash():
    #             return False
    #         if current_block.previous_hash != previous_block.hash():
    #             return False
    #     return True

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:  # Remove parentheses here
                return False
        return True


    # def get_latest_block(self) -> Block:
    def get_latest_block(self) -> Block:
        return self.chain[-1]



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


# def mine_blocks(blockchain: Blockchain, num_blocks: int, difficulty_change_coefficient: float) -> None:
#     for i in range(1, num_blocks):  # Start from 1 to avoid mining a genesis block twice
#         new_block = Block(i, time.time(), f"Block {i}", blockchain.get_latest_block().hash)
#         blockchain.add_block(new_block, difficulty_change_coefficient)


def mine_blocks(blockchain: Blockchain, num_blocks: int) -> None:
    for i in range(1, num_blocks):  # Start from 1 to avoid mining a genesis block twice
        new_block = Block(i, time.time(), f"Block {i}", blockchain.get_latest_block().hash)
        blockchain.add_block(new_block)


# if __name__ == "__main__":
#     logger: logging.Logger = setup_logger()
#
#     BASE = 2
#     INITIAL_DUAL_DIFFICULTY = 16
#     INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
#
#     logger.debug(f"BASE: {BASE}")
#     logger.debug(f"INITIAL_DUAL_DIFFICULTY: {INITIAL_DUAL_DIFFICULTY}")
#     logger.debug(f"INITIAL_BASE_DIFFICULTY: {INITIAL_BASE_DIFFICULTY}")
#
#     blockchain: Blockchain = Blockchain(
#         initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial
#         target_block_time=1,  # Set the target block time in seconds
#         base=BASE  # Use binary system by default
#     )
#
#     log_validity(blockchain)
#     logger.debug(f"Difficulty[base={BASE}]: {blockchain.difficulty}")
#
#     mine_blocks(
#         blockchain,
#         num_blocks=10,
#         difficulty_change_coefficient=BASE,  # todo why 1.5 not 2?
#     )


# if __name__ == "__main__":
#     logger: logging.Logger = setup_logger()
#
#     BASE = 2
#     INITIAL_DUAL_DIFFICULTY = 16
#     INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
#
#     logger.debug(f"BASE: {BASE}")
#     logger.debug(f"INITIAL_DUAL_DIFFICULTY: {INITIAL_DUAL_DIFFICULTY}")
#     logger.debug(f"INITIAL_BASE_DIFFICULTY: {INITIAL_BASE_DIFFICULTY}")
#
#     blockchain: Blockchain = Blockchain(
#         initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
#         target_block_time=1,  # Set the target block time in seconds
#         base=BASE  # Use binary system by default
#     )
#
#     log_validity(blockchain)
#     logger.debug(f"Difficulty[base={BASE}]: {blockchain.difficulty}")
#
#     mine_blocks(
#         blockchain,
#         num_blocks=100
#     )


if __name__ == "__main__":
    logger: logging.Logger = setup_logger()

    BASE = 2
    INITIAL_DUAL_DIFFICULTY = 16
    INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
    ADJUSTMENT_INTERVAL = 10  # Number of blocks between difficulty adjustments

    logger.debug(f"BASE: {BASE}")
    logger.debug(f"INITIAL_DUAL_DIFFICULTY: {INITIAL_DUAL_DIFFICULTY}")
    logger.debug(f"INITIAL_BASE_DIFFICULTY: {INITIAL_BASE_DIFFICULTY}")

    blockchain: Blockchain = Blockchain(
        initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
        target_block_time=1,  # Set the target block time in seconds
        base=BASE,  # Use binary system by default
        adjustment_interval=ADJUSTMENT_INTERVAL  # Set the adjustment interval
    )

    log_validity(blockchain)
    logger.debug(f"Difficulty[base={BASE}]: {blockchain.difficulty}")

    mine_blocks(
        blockchain,
        num_blocks=100
    )

