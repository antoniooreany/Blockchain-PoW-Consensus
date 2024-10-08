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
    logger.error(
        f"Average mining time: {actual_time:.35f} seconds,\n "
        f"                                        Expected mining time: {expected_time:.35f} seconds\n"
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


import matplotlib.pyplot as plt


# class Blockchain:
#     def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2,
#                  adjustment_interval: int = 10) -> None:
#         self.chain = [self.create_genesis_block()]
#         self.difficulty = initial_difficulty
#         self.target_block_time = target_block_time  # Target block time in seconds
#         self.base = base  # Base for numeral system
#         self.adjustment_interval = adjustment_interval  # Number of blocks between difficulty adjustments
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
#         start_time = time.time()
#         new_block.mine(self.difficulty, self.base)  # Pass the chosen numeral system
#         end_time = time.time()
#         actual_mining_time = end_time - start_time
#         self.chain.append(new_block)
#         if len(self.chain) % self.adjustment_interval == 0:
#             self.adjust_difficulty()
#         log_validity(self)
#         logger.debug(f"Difficulty[base={self.base}]: {self.difficulty}")
#         logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")


class Blockchain:
    def __init__(self, initial_difficulty: int, target_block_time: float, base: int = 2,
                 adjustment_interval: int = 10) -> None:
        self.chain = [self.create_genesis_block()]
        self.difficulty = initial_difficulty
        self.target_block_time = target_block_time  # Target block time in seconds
        self.base = base  # Base for numeral system
        self.adjustment_interval = adjustment_interval  # Number of blocks between difficulty adjustments
        self.mining_times = []  # List to store mining times
        self.difficulties = []  # List to store difficulties

    def create_genesis_block(self) -> Block:
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        log_mined_block(genesis_block)
        actual_time = 0  # Genesis block has no previous block, so actual time is 0
        expected_time = 1  # Set the expected time for the genesis block
        log_time(actual_time, expected_time)
        return genesis_block

    def add_block(self, new_block: Block) -> None:
        new_block.previous_hash = self.get_latest_block().hash  # Set the previous hash of the new block to the hash of the latest block
        start_time = time.time()
        new_block.mine(self.difficulty, self.base)  # Pass the chosen numeral system
        end_time = time.time()
        actual_mining_time = end_time - start_time
        self.chain.append(new_block)
        self.mining_times.append(actual_mining_time)
        self.difficulties.append(self.difficulty)
        if len(self.chain) % self.adjustment_interval == 0:
            self.adjust_difficulty()
        log_validity(self)
        logger.debug(f"Difficulty[base={self.base}]: {self.difficulty}")
        logger.debug(f"Actual mining time for block {new_block.index}: {actual_mining_time:.25f} seconds")

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

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:  # Remove parentheses here
                return False
        return True

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


def mine_blocks(blockchain: Blockchain, num_blocks: int) -> None:
    for i in range(1, num_blocks):  # Start from 1 to avoid mining a genesis block twice
        new_block = Block(i, time.time(), f"Block {i}", blockchain.get_latest_block().hash)
        blockchain.add_block(new_block)


# def plot_statistics(blockchain: Blockchain) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     color = 'tab:blue'
#     ax1.set_xlabel('Block Index')
#     ax1.set_ylabel('Mining Time (s)', color=color)
#     ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=color)
#     ax1.tick_params(axis='y', labelcolor=color)
#
#     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#     color = 'tab:red'
#     ax2.set_ylabel('Difficulty', color=color)  # we already handled the x-label with ax1
#     ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=color)
#     ax2.tick_params(axis='y', labelcolor=color)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics')
#     plt.show()
#
#
#
# if __name__ == "__main__":
#     logger: logging.Logger = setup_logger()
#
#     BASE = 2
#     INITIAL_DUAL_DIFFICULTY = 16
#     INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
#     ADJUSTMENT_INTERVAL = 5  # Number of blocks between difficulty adjustments
#
#     logger.debug(f"BASE: {BASE}")
#     logger.debug(f"INITIAL_DUAL_DIFFICULTY: {INITIAL_DUAL_DIFFICULTY}")
#     logger.debug(f"INITIAL_BASE_DIFFICULTY: {INITIAL_BASE_DIFFICULTY}")
#     logger.debug(f"ADJUSTMENT_INTERVAL: {ADJUSTMENT_INTERVAL}")
#
#     blockchain: Blockchain = Blockchain(
#         initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
#         target_block_time=1,  # Set the target block time in seconds
#         base=BASE,  # Use binary system by default
#         adjustment_interval=ADJUSTMENT_INTERVAL  # Set the adjustment interval
#     )
#
#     log_validity(blockchain)
#     logger.debug(f"Difficulty[base={BASE}]: {blockchain.difficulty}")
#
#     mine_blocks(
#         blockchain,
#         num_blocks=100
#     )
#
#     plot_statistics(blockchain)


import matplotlib.pyplot as plt


# def plot_statistics(blockchain: Blockchain) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     color = 'tab:blue'
#     ax1.set_xlabel('Block Index')
#     ax1.set_ylabel('Mining Time (s)', color=color)
#     ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=color)
#     ax1.tick_params(axis='y', labelcolor=color)
#
#     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#     color = 'tab:red'
#     ax2.set_ylabel('Dual Difficulty', color=color)  # we already handled the x-label with ax1
#     ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=color)
#     ax2.tick_params(axis='y', labelcolor=color)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics')
#     plt.show()


# import matplotlib.pyplot as plt
#
# def plot_statistics(blockchain: Blockchain, base: int) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     # Custom colors
#     mining_time_color = 'cyan'
#     difficulty_color = 'magenta'
#
#     ax1.set_xlabel('Block Index')
#     ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#     ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color)
#     ax1.tick_params(axis='y', labelcolor=mining_time_color)
#
#     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#     ax2.set_ylabel('Dual Difficulty', color=difficulty_color)  # we already handled the x-label with ax1
#     ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title(f'Blockchain Mining Statistics (BASE={base})')
#     plt.show()
#
#
# if __name__ == "__main__":
#     logger: logging.Logger = setup_logger()
#
#     BASE = 2
#     INITIAL_DUAL_DIFFICULTY = 16
#     INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
#     ADJUSTMENT_INTERVAL = 5  # Number of blocks between difficulty adjustments
#
#     logger.debug(f"BASE: {BASE}")
#     logger.debug(f"INITIAL_DUAL_DIFFICULTY: {INITIAL_DUAL_DIFFICULTY}")
#     logger.debug(f"INITIAL_BASE_DIFFICULTY: {INITIAL_BASE_DIFFICULTY}")
#     logger.debug(f"ADJUSTMENT_INTERVAL: {ADJUSTMENT_INTERVAL}")
#
#     blockchain: Blockchain = Blockchain(
#         initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
#         target_block_time=1,  # Set the target block time in seconds
#         base=BASE,  # Use binary system by default
#         adjustment_interval=ADJUSTMENT_INTERVAL  # Set the adjustment interval
#     )
#
#     log_validity(blockchain)
#     logger.debug(f"Difficulty[base={BASE}]: {blockchain.difficulty}")
#
#     mine_blocks(
#         blockchain,
#         num_blocks=100
#     )
#
#     plot_statistics(blockchain, BASE)


import matplotlib.pyplot as plt

# def plot_statistics(blockchain: Blockchain, base: int) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     # Custom colors
#     mining_time_color = 'cyan'
#     difficulty_color = 'magenta'
#
#     ax1.set_xlabel('Block Index')
#     ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#     ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color)
#     ax1.tick_params(axis='y', labelcolor=mining_time_color)
#
#     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#     ax2.set_ylabel('Dual Difficulty', color=difficulty_color)  # we already handled the x-label with ax1
#     ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title(f'Blockchain Mining Statistics (BASE={base})')
#     plt.show()
#
# if __name__ == "__main__":
#     logger: logging.Logger = setup_logger()
#
#     for BASE in [2, 4]:
#         INITIAL_DUAL_DIFFICULTY = 16
#         INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
#         ADJUSTMENT_INTERVAL = 5  # Number of blocks between difficulty adjustments
#
#         blockchain: Blockchain = Blockchain(
#             initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
#             target_block_time=1,  # Set the target block time in seconds
#             base=BASE,  # Use the current base
#             adjustment_interval=ADJUSTMENT_INTERVAL  # Set the adjustment interval
#         )
#
#         log_validity(blockchain)
#
#         mine_blocks(
#             blockchain,
#             num_blocks=30
#         )
#
#         plot_statistics(blockchain, BASE)


# import matplotlib.pyplot as plt
#
# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     # Custom colors
#     colors = ['cyan', 'magenta', 'yellow', 'green']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = colors[i % len(colors)]
#         difficulty_color = colors[(i + 1) % len(colors)]
#
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.tick_params(axis='y')
#
#         ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()
#
# if __name__ == "__main__":
#     logger: logging.Logger = setup_logger()
#
#     blockchains = {}
#     for BASE in [2, 4]:
#         INITIAL_DUAL_DIFFICULTY = 16
#         INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
#         ADJUSTMENT_INTERVAL = 5  # Number of blocks between difficulty adjustments
#
#         blockchain = Blockchain(
#             initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
#             target_block_time=1,  # Set the target block time in seconds
#             base=BASE,  # Use the current base
#             adjustment_interval=ADJUSTMENT_INTERVAL  # Set the adjustment interval
#         )
#
#         log_validity(blockchain)
#
#         mine_blocks(
#             blockchain,
#             num_blocks=30
#         )
#
#         blockchains[BASE] = blockchain
#
#     plot_statistics(blockchains)
#


# import matplotlib.pyplot as plt
#
# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     # Custom colors
#     colors = ['cyan', 'magenta', 'yellow', 'green']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = colors[i % len(colors)]
#         difficulty_color = colors[(i + 1) % len(colors)]
#
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.tick_params(axis='y')
#
#         ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()
#
# if __name__ == "__main__":
#     logger: logging.Logger = setup_logger()
#
#     blockchains = {}
#     for BASE in [2, 4]:
#         INITIAL_DUAL_DIFFICULTY = 16
#         INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
#         ADJUSTMENT_INTERVAL = 5  # Number of blocks between difficulty adjustments
#
#         blockchain = Blockchain(
#             initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
#             target_block_time=1,  # Set the target block time in seconds
#             base=BASE,  # Use the current base
#             adjustment_interval=ADJUSTMENT_INTERVAL  # Set the adjustment interval
#         )
#
#         log_validity(blockchain)
#
#         mine_blocks(
#             blockchain,
#             num_blocks=0
#         )
#
#         blockchains[BASE] = blockchain
#
#     plot_statistics(blockchains)



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     # Custom colors
#     colors = ['cyan', 'magenta', 'yellow', 'green']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = colors[i % len(colors)]
#         difficulty_color = colors[(i + 1) % len(colors)]
#
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.tick_params(axis='y')
#
#         ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()


import logging
import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict) -> None:
#     # Save the current logging level
#     original_logging_level = logging.getLogger('matplotlib.font_manager').getEffectiveLevel()
#
#     # Set matplotlib font manager logging level to WARNING
#     logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
#
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     # Custom colors
#     colors = ['cyan', 'magenta', 'yellow', 'green']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = colors[i % len(colors)]
#         difficulty_color = colors[(i + 1) % len(colors)]
#
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.tick_params(axis='y')
#
#         ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()
#
#     # Restore the original logging level
#     logging.getLogger('matplotlib.font_manager').setLevel(original_logging_level)


import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots()
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.tick_params(axis='y')
#
#         ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig = plt.figure(figsize=(20, 15))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     ax1 = fig.add_subplot(1, 2, 1, projection='3d')
#     ax2 = fig.add_subplot(1, 2, 2, projection='3d')
#     ax3 = fig.add_subplot(1, 1, 1)  # New axis for dual difficulty
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, zs=i, zdir='z', color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.set_zlabel('Blockchain Index')
#         ax1.tick_params(axis='y')
#
#         # Plot difficulties
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, zs=i, zdir='z', color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_xlabel('Block Index')
#         ax2.set_ylabel('Difficulty')
#         ax2.set_zlabel('Blockchain Index')
#         ax2.tick_params(axis='y')
#
#         # Plot dual difficulty on the new axis
#         ax3.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#
#     ax3.set_xlabel('Block Index')
#     ax3.set_ylabel('Dual Difficulty')
#     ax3.legend()
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.suptitle('Blockchain Mining Statistics Comparison')
#     plt.show()


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig = plt.figure(figsize=(20, 15))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     ax1 = fig.add_subplot(1, 2, 1, projection='3d')
#     ax2 = fig.add_subplot(1, 2, 2, projection='3d')
#     ax3 = fig.add_subplot(1, 1, 1)  # New axis for dual difficulty
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, zs=i, zdir='z', color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.set_zlabel('Blockchain Index')
#         ax1.tick_params(axis='y')
#
#         # Plot difficulties
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, zs=i, zdir='z', color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_xlabel('Block Index')
#         ax2.set_ylabel('Difficulty')
#         ax2.set_zlabel('Blockchain Index')
#         ax2.tick_params(axis='y')
#
#         # Plot dual difficulty on the new axis
#         ax3.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#
#     # Plot mining times for both blockchains in the same graph
#     fig, ax = plt.subplots()
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         ax.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#     ax.set_xlabel('Block Index')
#     ax.set_ylabel('Mining Time (s)')
#     ax.legend()
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.suptitle('Blockchain Mining Statistics Comparison')
#     plt.show()



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20, 15))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#     # Customize legend labels
#     lines, labels = ax1.get_legend_handles_labels()
#     lines2, labels2 = ax2.get_legend_handles_labels()
#     ax1.legend(lines + lines2, labels + labels2, loc='upper left')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     plt.show()



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#     # Customize legend labels
#     lines, labels = ax1.get_legend_handles_labels()
#     lines2, labels2 = ax2.get_legend_handles_labels()
#     ax1.legend(lines + lines2, labels + labels2, loc='upper left')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     plt.show()


import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)  # Add grid to ax1
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)  # Add grid to ax2
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)  # Add grid to ax1
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)  # Add grid to ax2
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()




import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)  # Add grid to ax1
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)  # Add grid to ax2
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()




import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     plt.style.use('dark_background')
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)  # Add grid to ax1
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)  # Add grid to ax2
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     plt.style.use('seaborn-darkgrid')  # Apply a predefined style
#
#     fig, ax1 = plt.subplots(figsize=(18, 12), dpi=100, facecolor='lightgrey', edgecolor='black')
#
#     # Custom colors and styles
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']
#     markers = ['o', 's', 'D', '^']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#         marker = markers[i % len(markers)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, marker=marker, markersize=8, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index', fontsize=14)
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color, fontsize=14)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True, linestyle='--', color='grey', alpha=0.7)
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, marker=marker, markersize=8, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color, fontsize=14)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True, linestyle='--', color='grey', alpha=0.7)
#
#     # Customize legend labels
#     lines, labels = ax1.get_legend_handles_labels()
#     lines2, labels2 = ax2.get_legend_handles_labels()
#     ax1.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=12)
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison', fontsize=16)
#     plt.show()



import matplotlib.pyplot as plt

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     # Check available styles
#     available_styles = plt.style.available
#     print("Available styles:", available_styles)
#
#     # Use a valid style
#     plt.style.use('dark_background')  # Change to a valid style
#
#     fig, ax1 = plt.subplots(figsize=(20*0.9, 15*0.9))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)  # Add grid to ax1
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)  # Add grid to ax2
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt
from screeninfo import get_monitors

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     # Get the screen dimensions
#     monitor = get_monitors()[0]
#     screen_width = monitor.width
#     screen_height = monitor.height
#
#     # Set the figure size proportional to the screen size
#     fig_width = screen_width * 0.9 / 100  # 90% of screen width
#     fig_height = screen_height * 0.9 / 100  # 90% of screen height
#
#     plt.style.use('dark_background')
#     fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)  # Add grid to ax1
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)  # Add grid to ax2
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()



import matplotlib.pyplot as plt
from screeninfo import get_monitors

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     # Get the screen dimensions for dynamic figure sizing
#     monitor = get_monitors()[0]
#     screen_width = monitor.width
#     screen_height = monitor.height
#
#     # Set the figure size proportional to the screen size
#     fig_width = screen_width * 0.9 / 100  # 90% of screen width
#     fig_height = screen_height * 0.9 / 100  # 90% of screen height
#
#     plt.style.use('dark_background')
#     fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
#
#     # Custom colors for different lines
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     # Iterate over blockchains and plot their statistics
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times on the primary y-axis
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)
#
#         # Plot scaled difficulties on the secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]  # Apply scaling to difficulties
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)
#
#     # Combine legends from both axes
#     lines, labels = ax1.get_legend_handles_labels()
#     lines2, labels2 = ax2.get_legend_handles_labels()
#     ax1.legend(lines + lines2, labels + labels2, loc='upper left')
#
#     # Adjust layout to prevent overlap
#     fig.tight_layout()
#     plt.title('Blockchain Mining Statistics Comparison')
#     plt.show()



import matplotlib.pyplot as plt
from screeninfo import get_monitors

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     # Get the screen dimensions
#     monitor = get_monitors()[0]
#     screen_width = monitor.width
#     screen_height = monitor.height
#
#     # Set the figure size proportional to the screen size
#     fig_width = screen_width * 0.9 / 100  # 90% of screen width
#     fig_height = screen_height * 0.9 / 100  # 90% of screen height
#
#     plt.style.use('dark_background')
#     fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     # To store min/max values for y-axis scaling
#     all_mining_times = []
#     all_difficulties = []
#
#     # Collect all values for global scaling
#     for blockchain in blockchains.values():
#         all_mining_times.extend(blockchain.mining_times)
#         all_difficulties.extend(blockchain.difficulties)
#
#     # Determine the common y-axis range for both mining times and difficulties
#     min_mining_time = min(all_mining_times)
#     max_mining_time = max(all_mining_times)
#     min_difficulty = min(all_difficulties)
#     max_difficulty = max(all_difficulties) * scaling_factor
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)  # Add grid to ax1
#
#         # Set consistent y-axis limits for mining times
#         ax1.set_ylim(min(min_mining_time, min_difficulty), max(max_mining_time, max_difficulty))
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#
#         # Set consistent y-axis limits for difficulties
#         ax2.set_ylim(min(min_mining_time, min_difficulty), max(max_mining_time, max_difficulty))
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.title('Blockchain Mining Statistics Comparison')
#     fig.legend(loc='upper left')
#     plt.show()


import matplotlib.pyplot as plt
from screeninfo import get_monitors

# def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
#     # Get the screen dimensions
#     monitor = get_monitors()[0]
#     screen_width = monitor.width
#     screen_height = monitor.height
#
#     # Set the figure size proportional to the screen size
#     fig_width = screen_width * 0.9 / 100  # 90% of screen width
#     fig_height = screen_height * 0.9 / 100  # 90% of screen height
#
#     plt.style.use('dark_background')
#     fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#     line_styles = ['-', '--', '-.', ':']  # Different line styles
#
#     # To store min/max values for y-axis scaling
#     all_mining_times = []
#     all_difficulties = []
#
#     # Collect all values for global scaling
#     for blockchain in blockchains.values():
#         all_mining_times.extend(blockchain.mining_times)
#         all_difficulties.extend(blockchain.difficulties)
#
#     # Determine the common y-axis range for both mining times and difficulties
#     min_mining_time = min(all_mining_times)
#     max_mining_time = max(all_mining_times)
#     min_difficulty = min(all_difficulties)
#     max_difficulty = max(all_difficulties) * scaling_factor
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         line_style = line_styles[i % len(line_styles)]
#
#         # Plot mining times
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True)
#         ax1.set_ylim(min_mining_time, max_mining_time)  # Set y-axis limits for mining times
#
#         # Plot dual difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
#         ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.grid(True)
#         ax2.set_ylim(min_difficulty * scaling_factor, max_difficulty)  # Set y-axis limits for dual difficulties
#
#     # Combine legends from both axes
#     lines, labels = ax1.get_legend_handles_labels()
#     lines2, labels2 = ax2.get_legend_handles_labels()
#     ax1.legend(lines + lines2, labels + labels2, loc='upper left')
#
#     # Adjust layout to prevent overlap
#     fig.tight_layout()
#     plt.title('Blockchain Mining Statistics Comparison')
#     plt.show()



import matplotlib.pyplot as plt
from screeninfo import get_monitors

import matplotlib
import logging

# Set the logging level to INFO (or WARNING to reduce more output)
logging.getLogger('matplotlib').setLevel(logging.INFO)

# Your plotting code here




def plot_statistics(blockchains: dict, scaling_factor: float = 10.0) -> None:
    # Get the screen dimensions
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height

    # Set the figure size proportional to the screen size
    fig_width = screen_width * 0.9 / 100  # 90% of screen width
    fig_height = screen_height * 0.9 / 100  # 90% of screen height

    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    # Custom colors
    mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
    difficulty_colors = ['blue', 'red', 'orange', 'purple']
    line_styles = ['-', '--', '-.', ':']  # Different line styles

    # To store min/max values for y-axis scaling for difficulties only
    all_difficulties = []

    # Collect all difficulty values for consistent scaling
    for blockchain in blockchains.values():
        all_difficulties.extend(blockchain.difficulties)

    # Determine the common y-axis range for difficulties only
    min_difficulty = min(all_difficulties)
    max_difficulty = max(all_difficulties) * scaling_factor

    for i, (base, blockchain) in enumerate(blockchains.items()):
        mining_time_color = mining_time_colors[i % len(mining_time_colors)]
        difficulty_color = difficulty_colors[i % len(difficulty_colors)]
        line_style = line_styles[i % len(line_styles)]

        # Plot mining times
        ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color, linestyle=line_style, label=f'Mining Time (BASE={base})')
        ax1.set_xlabel('Block Index')
        ax1.set_ylabel('Mining Time (s)', color=mining_time_color)
        ax1.tick_params(axis='y', labelcolor=mining_time_color)
        ax1.grid(True)  # Add grid to ax1

        # Allow independent scaling for Mining Time
        ax1.relim()
        ax1.autoscale_view()

        # Plot dual difficulties on the same graph with a secondary y-axis
        ax2 = ax1.twinx()
        scaled_difficulties = [d * scaling_factor for d in blockchain.difficulties]
        ax2.plot(range(len(scaled_difficulties)), scaled_difficulties, color=difficulty_color, linestyle=line_style, label=f'Dual Difficulty (BASE={base})')
        ax2.set_ylabel('Dual Difficulty', color=difficulty_color)
        ax2.tick_params(axis='y', labelcolor=difficulty_color)

        # Set consistent y-axis limits for difficulties across all blockchains
        ax2.set_ylim(min_difficulty, max_difficulty)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Blockchain Mining Statistics Comparison')
    fig.legend(loc='upper left')
    plt.show()




import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig = plt.figure(figsize=(20, 15))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Create 3D subplot for mining times
#         ax1 = fig.add_subplot(2, 2, i*2+1, projection='3d')
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, zs=0, zdir='y', color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.set_zlabel('Value')
#         ax1.tick_params(axis='y')
#
#         # Create 3D subplot for difficulties
#         ax2 = fig.add_subplot(2, 2, i*2+2, projection='3d')
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, zs=0, zdir='y', color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_xlabel('Block Index')
#         ax2.set_ylabel('Difficulty')
#         ax2.set_zlabel('Value')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.suptitle('Blockchain Mining Statistics Comparison')
#     plt.show()



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig = plt.figure(figsize=(20, 15))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Create 3D subplot for mining times
#         ax1 = fig.add_subplot(1, 2, 1, projection='3d')
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, zs=i, zdir='z', color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.set_zlabel('Blockchain Index')
#         ax1.tick_params(axis='y')
#
#         # Create 3D subplot for difficulties
#         ax2 = fig.add_subplot(1, 2, 2, projection='3d')
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, zs=i, zdir='z', color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_xlabel('Block Index')
#         ax2.set_ylabel('Difficulty')
#         ax2.set_zlabel('Blockchain Index')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.suptitle('Blockchain Mining Statistics Comparison')
#     plt.show()


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# def plot_statistics(blockchains: dict) -> None:
#     plt.style.use('dark_background')
#
#     fig = plt.figure(figsize=(20, 15))
#
#     # Custom colors
#     mining_time_colors = ['cyan', 'magenta', 'yellow', 'green']
#     difficulty_colors = ['blue', 'red', 'orange', 'purple']
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#
#         # Create 3D subplot for mining times
#         ax1 = fig.add_subplot(1, 2, 1, projection='3d')
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, zs=i, zdir='z', color=mining_time_color, label=f'Mining Time (BASE={base})')
#         ax1.set_xlabel('Block Index')
#         ax1.set_ylabel('Mining Time (s)')
#         ax1.set_zlabel('Blockchain Index')
#         ax1.tick_params(axis='y')
#
#         # Create 3D subplot for difficulties
#         ax2 = fig.add_subplot(1, 2, 2, projection='3d')
#         ax2.plot(range(len(blockchain.difficulties)), blockchain.difficulties, zs=i, zdir='z', color=difficulty_color, label=f'Difficulty (BASE={base})')
#         ax2.set_xlabel('Block Index')
#         ax2.set_ylabel('Difficulty')
#         ax2.set_zlabel('Blockchain Index')
#         ax2.tick_params(axis='y')
#
#     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     plt.suptitle('Blockchain Mining Statistics Comparison')
#     plt.show()

if __name__ == "__main__":
    logger: logging.Logger = setup_logger(level=logging.DEBUG)

    blockchains = {}
    for BASE in [2, 16]:
        INITIAL_DUAL_DIFFICULTY = 16
        INITIAL_BASE_DIFFICULTY = round(INITIAL_DUAL_DIFFICULTY / math.log2(BASE))
        ADJUSTMENT_INTERVAL = 5  # Number of blocks between difficulty adjustments

        blockchain = Blockchain(
            initial_difficulty=INITIAL_BASE_DIFFICULTY,  # Set the initial difficulty
            target_block_time=1,  # Set the target block time in seconds
            base=BASE,  # Use the current base
            adjustment_interval=ADJUSTMENT_INTERVAL  # Set the adjustment interval
        )

        log_validity(blockchain)

        mine_blocks(
            blockchain,
            num_blocks=12
        )

        blockchains[BASE] = blockchain

    plot_statistics(blockchains)


