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
        logger.debug(f"Difficulty Level[base={self.base}]: {self.difficulty}")
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


from screeninfo import get_monitors
import logging

# Set the logging level to INFO (or WARNING to reduce more output)
logging.getLogger('matplotlib').setLevel(logging.INFO)

import matplotlib.pyplot as plt
from screeninfo import get_monitors
import numpy as np
import matplotlib.colors as mcolors


# def plot_statistics(blockchains: dict, scaling_factor: float = 1.0) -> None:
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
#     # Custom colors for mining time and difficulty
#     mining_time_colors = ['green', 'green', 'green']
#     difficulty_colors = ['cyan', 'cyan', 'cyan']
#
#     # bit_difficulty_base_factor = math.log2(base)
#
#     # To store min/max values for y-axis scaling for difficulties only
#     all_difficulties = []
#
#     # Collect all difficulty values for consistent scaling
#     for blockchain in blockchains.values():
#         all_difficulties.extend(blockchain.difficulties)
#
#     # Determine the common y-axis range for difficulties only
#     min_difficulty = min(all_difficulties)
#     max_difficulty = max(all_difficulties) * scaling_factor
#     # min_difficulty = min(all_difficulties) * bit_difficulty_base_factor
#     # max_difficulty = max(all_difficulties) * bit_difficulty_base_factor * scaling_factor
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         bit_difficulty_base_factor = math.log2(base)
#         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
#         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
#         linewidth = base * 0.9
#
#         # Plot circles for mining times
#         ax1.scatter(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color,
#                     s=np.pi * (base / 2) ** 2, label=f'Mining Time (BASE={base})')
#
#         # Connect circles with lines
#         less_saturated_color = mcolors.to_rgba(mining_time_color, alpha=0.5)
#         ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=less_saturated_color,
#                  linewidth=linewidth)
#
#         ax1.set_xlabel('Block Index', fontsize=12)
#         ax1.set_ylabel('Mining Time (s)', fontsize=12, color='green')
#         ax1.tick_params(axis='y', labelcolor=mining_time_color)
#         ax1.grid(True, which='both', linestyle=':', linewidth=0.5)
#
#         # Allow independent scaling for Mining Time
#         ax1.relim()
#         ax1.autoscale_view()
#
#         # Plot base difficulties on the same graph with a secondary y-axis
#         ax2 = ax1.twinx()
#         # bit_difficulties = [d * scaling_factor for d in blockchain.difficulties]
#         bit_difficulties = [d * bit_difficulty_base_factor * scaling_factor for d in blockchain.difficulties]
#         ax2.plot(range(len(bit_difficulties)), bit_difficulties, color=difficulty_color,
#                  linewidth=linewidth, label=f'Base Difficulty (BASE={base})')
#         ax2.set_ylabel('Base Difficulty', fontsize=12, color='cyan')
#         ax2.tick_params(axis='y', labelcolor=difficulty_color)
#         ax2.set_ylim(min_difficulty, max_difficulty)
#
#     fig.tight_layout()
#
#     # Adjust legend to be outside of the plot to avoid overlap
#     fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=10)
#     plt.title('Blockchain Mining Statistics Comparison', fontsize=14, color='white')
#     plt.show()


# def plot_difficulty_grid(blockchains: dict) -> None:
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
#     fig, ax = plt.subplots(figsize=(fig_width, fig_height))
#
#     # Collect difficulty values for each blockchain
#     difficulty_grid = []
#     for base, blockchain in blockchains.items():
#         difficulty_grid.append(blockchain.difficulties)
#
#     # Convert the list to a numpy array for plotting
#     difficulty_grid = np.array(difficulty_grid)
#
#     # Plot the heatmap
#     cax = ax.matshow(difficulty_grid, cmap='viridis')
#     fig.colorbar(cax)
#
#     # Set axis labels
#     ax.set_xlabel('Block Index', fontsize=12)
#     ax.set_ylabel('Base', fontsize=12)
#     ax.set_yticks(range(len(blockchains)))
#     ax.set_yticklabels([f'BASE={base}' for base in blockchains.keys()])
#
#     plt.title('Difficulty Grid', fontsize=14, color='white')
#     plt.show()



import matplotlib.pyplot as plt
from screeninfo import get_monitors
import numpy as np
import matplotlib.colors as mcolors
import math

def plot_statistics(blockchains: dict, scaling_factor: float = 1.0) -> None:
    # Get the screen dimensions
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height

    # Set the figure size proportional to the screen size
    fig_width = screen_width * 0.9 / 100  # 90% of screen width
    fig_height = screen_height * 0.9 / 100  # 90% of screen height

    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    # Custom colors for mining time and difficulty
    mining_time_colors = ['green', 'green', 'green']
    difficulty_colors = ['cyan', 'cyan', 'cyan']

    # To store min/max values for y-axis scaling for difficulties only
    all_difficulties = []

    # Collect all difficulty values for consistent scaling
    for blockchain in blockchains.values():
        all_difficulties.extend(blockchain.difficulties)

    # Determine the common y-axis range for difficulties only
    min_difficulty = min(all_difficulties)
    max_difficulty = max(all_difficulties) * scaling_factor

    # Adjust the minimum difficulty to be a certain percentage below the actual minimum value
    min_difficulty *= 0.9  # Adjust to 90% of the actual minimum value

    for i, (base, blockchain) in enumerate(blockchains.items()):
        bit_difficulty_base_factor = math.log2(base)
        mining_time_color = mining_time_colors[i % len(mining_time_colors)]
        difficulty_color = difficulty_colors[i % len(difficulty_colors)]
        linewidth = base * 0.9

        # Plot circles for mining times
        ax1.scatter(range(len(blockchain.mining_times)), blockchain.mining_times, color=mining_time_color,
                    s=np.pi * (base / 2) ** 2, label=f'Mining Time (BASE={base})')

        # Connect circles with lines
        less_saturated_color = mcolors.to_rgba(mining_time_color, alpha=0.5)
        ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, color=less_saturated_color,
                 linewidth=linewidth)

        ax1.set_xlabel('Block Index', fontsize=12)
        ax1.set_ylabel('Mining Time, seconds', fontsize=12, color='green')
        ax1.tick_params(axis='y', labelcolor=mining_time_color)
        ax1.grid(True, which='both', linestyle=':', linewidth=0.5)

        # Allow independent scaling for Mining Time
        ax1.relim()
        ax1.autoscale_view()

        # Plot base difficulties on the same graph with a secondary y-axis
        ax2 = ax1.twinx()
        bit_difficulties = [d * bit_difficulty_base_factor * scaling_factor for d in blockchain.difficulties]
        ax2.plot(range(len(bit_difficulties)), bit_difficulties, color=difficulty_color,
                 linewidth=linewidth, label=f'Bit Difficulty (base={base})')
        ax2.set_ylabel('Bit Difficulty, bits', fontsize=12, color='cyan')
        ax2.tick_params(axis='y', labelcolor=difficulty_color)
        ax2.set_ylim(min_difficulty, max_difficulty)

    fig.tight_layout()

    # Adjust legend to be outside of the plot to avoid overlap
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=10)
    plt.title('Blockchain Mining Statistics Comparison', fontsize=14, color='white')
    plt.show()


if __name__ == "__main__":
    logger: logging.Logger = setup_logger(level=logging.DEBUG)

    blockchains = {}
    for BASE in [2, 4, 16]:
        INITIAL_BIT_DIFFICULTY = 16
        INITIAL_BASE_DIFFICULTY = round(INITIAL_BIT_DIFFICULTY / math.log2(BASE))
        ADJUSTMENT_INTERVAL = 5

        blockchain = Blockchain(
            initial_difficulty=INITIAL_BASE_DIFFICULTY,
            target_block_time=1,
            base=BASE,
            adjustment_interval=ADJUSTMENT_INTERVAL
        )

        log_validity(blockchain)

        mine_blocks(
            blockchain,
            num_blocks=12
        )

        blockchains[BASE] = blockchain

    plot_statistics(blockchains)

    # plot_difficulty_grid(blockchains)
