#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a full_blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
from venv import logger

from colorama import Fore, Style, init

from src.block import Block
from src.blockchain import Blockchain

logging.getLogger('matplotlib').setLevel(logging.INFO)

MAX_NONCE = (2 ** (2 ** (2 ** 3))) - 1  # todo 16^64 - 1 = 2^256 - 1, the maximum value of the nonce

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

    ch = logging.StreamHandler()
    ch.setLevel(console_level)

    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)

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


def log_time(actual_time: float, expected_time: float, block_indices: list) -> None:
    logger.error(
        f"Average mining time for blocks with indices: {block_indices}: {actual_time:.35f} seconds,\n "
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


MAX_NONCE = (2 ** (2 ** (2 ** 3))) - 1  # Maximum value of the nonce

import hashlib
import random

MAX_NONCE = (2 ** (2 ** (2 ** 3))) - 1  # Maximum value of the nonce


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
                'utf-8')
        )
        return sha.hexdigest()

    def mine(self, difficulty: int) -> None:
        self.nonce = random.randint(0, MAX_NONCE)  # Start from a random nonce

        target_value = (2 ** (256 - difficulty))

        base_hash_data = (
                str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        ).encode('utf-8')

        while True:
            sha = hashlib.sha256()
            sha.update(base_hash_data + str(self.nonce).encode('utf-8'))
            self.hash = sha.hexdigest()

            hash_value = int(self.hash, 16)

            if hash_value < target_value:
                break
            self.nonce += 1

        logging.info(f"Mined block hash: {self.hash}")


import time
import logging


class Blockchain:
    def __init__(self, initial_difficulty: int, target_block_time: float, adjustment_interval: int = 10) -> None:
        self.blocks = []
        self.difficulties = []
        self.mining_times = []  # Add this to track mining times
        self.current_difficulty = initial_difficulty
        self.target_block_time = target_block_time
        self.adjustment_interval = adjustment_interval
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.blocks.append(genesis_block)
        self.difficulties.append(self.current_difficulty)
        self.mining_times.append(0)  # Mining time for the genesis block

    def add_block(self, new_block: Block, mining_time: float) -> None:
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.blocks.append(new_block)
        self.difficulties.append(self.current_difficulty)
        self.mining_times.append(mining_time)  # Append mining time for the block

    def get_latest_block(self) -> Block:
        return self.blocks[-1]

    def adjust_difficulty(self) -> None:
        average_time = self.get_average_mining_time(self.adjustment_interval)
        if average_time < self.target_block_time:
            self.current_difficulty += 1
        elif average_time > self.target_block_time:
            self.current_difficulty -= 1

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            prev_block = self.blocks[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != prev_block.hash:
                return False
        return True

    def get_average_mining_time(self, num_blocks: int = 10) -> float:
        if len(self.blocks) < num_blocks:
            return 0
        total_time = 0
        for i in range(-num_blocks, -1):
            total_time += self.blocks[i + 1].timestamp - self.blocks[i].timestamp
        return total_time / num_blocks


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


def add_block(self, new_block: Block) -> None:
    if len(self.blocks) > 0:
        new_block.prev_hash = self.blocks[-1].hash
    else:
        new_block.prev_hash = "0"  # Manually set for the genesis block
    new_block.mine_block(self.base_difficulty)
    self.blocks.append(new_block)


def mine_blocks(blockchain: Blockchain, num_blocks: int) -> None:
    if len(blockchain.blocks) == 0:
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        blockchain.add_block(genesis_block, 0)  # Mining time for the genesis block is 0

    for i in range(1, num_blocks):
        new_block = Block(i, time.time(), f"Block {i}", blockchain.get_latest_block().hash)
        start_time = time.time()
        blockchain.add_block(new_block, time.time() - start_time)


import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
from screeninfo import get_monitors
import math


def plot_statistics(blockchains: dict, scaling_factor: float = 1.0) -> None:
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height

    fig_width = screen_width * 0.9 / 100  # 90% of screen width
    fig_height = screen_height * 0.9 / 100  # 90% of screen height

    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    mining_time_colors = ['#39FF14', '#39FF14', '#39FF14']  # Bright green
    difficulty_color = '#FF0000'  # Bright red

    all_difficulties = []

    for blockchain in blockchains.values():
        all_difficulties.extend(blockchain.bit_difficulties)

    min_difficulty = min(all_difficulties) * scaling_factor
    max_difficulty = max(all_difficulties) * scaling_factor

    margin = (max_difficulty - min_difficulty) * 0.1
    min_difficulty -= margin
    max_difficulty += margin

    for blockchain in blockchains.values():
        all_difficulties.extend(blockchain.bit_difficulties)

    plt.figure(figsize=(10, 6))
    for base, blockchain in blockchains.items():
        plt.plot(
            range(len(blockchain.bit_difficulties)),
            [difficulty * scaling_factor for difficulty in blockchain.bit_difficulties],
            label=f'Base {base}'
        )

    for i, (base, blockchain) in enumerate(blockchains.items()):
        mining_time_color = mining_time_colors[i % len(mining_time_colors)]
        linewidth = base * 2

        for j, mining_time in enumerate(blockchain.actual_mining_times):
            ax1.axvline(x=j, ymin=0, ymax=mining_time, color=mining_time_color, linewidth=linewidth,
                        label=f'Mining Time (BASE={base})' if j == 0 else "")

        ax1.set_xlabel('Block Index', fontsize=12)
        ax1.set_ylabel('Mining Time, seconds', fontsize=12, color=mining_time_color)
        ax1.tick_params(axis='y', labelcolor=mining_time_color)
        ax1.grid(True, which='both', linestyle=':', linewidth=0.5, color=mining_time_color)

        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

        ax1.relim()
        ax1.autoscale_view()

        ax1.set_xlim(left=0)
        ax1.set_ylim(bottom=0)

        ax2 = ax1.twinx()
        bit_difficulties = [base_difficulty * math.log2(base) * scaling_factor for base_difficulty in
                            blockchain.bit_difficulties]
        ax2.scatter(range(len(bit_difficulties)), bit_difficulties, s=[base * 50 for _ in bit_difficulties],
                    color=difficulty_color, label=f'Difficulty (BASE={base})', alpha=0.6)
        ax2.set_ylabel('Difficulty=2^Bit_Difficulty', fontsize=12, color=difficulty_color)
        ax2.tick_params(axis='y', labelcolor=difficulty_color)
        ax2.set_ylim(min_difficulty, max_difficulty)
        ax2.grid(True, which='both', linestyle=':', linewidth=0.5, color=difficulty_color)

        ax2.set_yscale('linear')
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'$2^{{{int(math.log2(x))}}}$' if x > 0 else '0'))

    fig.tight_layout(pad=3.0)  # Adjust padding to ensure text is fully visible

    plt.xlabel('Block Index')
    plt.ylabel('Difficulty')
    plt.title('Blockchain Difficulty Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    logger: logging.Logger = setup_logger(level=logging.DEBUG)

    blockchains = {}
    for BASE in [
        2,
    ]:
        INITIAL_BIT_DIFFICULTY = 16
        INITIAL_DIFFICULTY = round(INITIAL_BIT_DIFFICULTY / math.log2(BASE))
        ADJUSTMENT_INTERVAL = 3

        blockchain = Blockchain(
            initial_difficulty=INITIAL_DIFFICULTY,
            target_block_time=1,
            adjustment_interval=ADJUSTMENT_INTERVAL
        )

        log_validity(blockchain)

        mine_blocks(
            blockchain,
            num_blocks=21
        )

        blockchains[BASE] = blockchain

    plot_statistics(blockchains)
