#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a create_project_structure.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import os

project_structure = {
    "Blockchain-PoW-Consensus": {
        "__init__.py": "",
        "constants.py": """MARGIN_COEFFICIENT = 0.1
DEFAULT_MARGIN = 1
FONTSIZE = 12
HASH_BIT_LENGTH = 256
NONCE_BIT_LENGTH = 32
""",
        "config.py": """import yaml

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)
""",
        "main.py": """import logging
from BlockchainPoWConsensus.blockchain import Blockchain, collect_filtered_bit_difficulties
from BlockchainPoWConsensus.utils.logger_singleton import LoggerSingleton
from BlockchainPoWConsensus.utils.logging_utils import LogLevelCounterHandler
from BlockchainPoWConsensus.plotting import plot_blockchain_statistics

if __name__ == "__main__":
    logging.getLogger('matplotlib').setLevel(logging.INFO)
    logger = LoggerSingleton.get_instance().logger
    log_level_counter_handler = LogLevelCounterHandler()
    logger.addHandler(log_level_counter_handler)

    blockchains = {}
    for base in [2]:
        INITIAL_BIT_DIFFICULTY = 16
        ADJUSTMENT_INTERVAL = 10
        TARGET_BLOCK_TIME = 0.1
        NUMBER_BLOCKS_TO_ADD = 100
        CLAMP_FACTOR = 2
        SMALLEST_BIT_DIFFICULTY = 4

        blockchain = Blockchain(
            initial_bit_difficulty=INITIAL_BIT_DIFFICULTY,
            adjustment_interval=ADJUSTMENT_INTERVAL,
            target_block_time=TARGET_BLOCK_TIME,
        )
        logger.debug(f"Created: blockchain (base: {base}, initial bit difficulty: {INITIAL_BIT_DIFFICULTY})")
        logger.debug(f"##################")

        blockchain.add_blocks(number_of_blocks=NUMBER_BLOCKS_TO_ADD, clamp_factor=CLAMP_FACTOR,
                              smallest_bit_difficulty=SMALLEST_BIT_DIFFICULTY)

        filtered_difficulties = collect_filtered_bit_difficulties(blockchain, ADJUSTMENT_INTERVAL)
        blockchain.bit_difficulties = filtered_difficulties

        logger.info(f"Target block time: {TARGET_BLOCK_TIME}")
        average_mining_time_last_half_blocks = blockchain.get_average_mining_time(
            num_blocks=blockchain.blocks.__len__() // 2)
        logger.info(f"Average mining time of the last half of the blockchain: {average_mining_time_last_half_blocks}")

        blockchains[base] = blockchain

    plot_blockchain_statistics(blockchains)
    log_level_counter_handler.print_log_counts()
""",
        "blockchain.py": """class Blockchain:
    def __init__(self, initial_bit_difficulty, adjustment_interval, target_block_time):
        self.blocks = []
        self.bit_difficulties = [initial_bit_difficulty]
        self.adjustment_interval = adjustment_interval
        self.target_block_time = target_block_time

    def add_blocks(self, number_of_blocks, clamp_factor, smallest_bit_difficulty):
        for _ in range(number_of_blocks):
            # Simulate adding a block
            self.blocks.append("Block")
        self.bit_difficulties.append(smallest_bit_difficulty)

    def get_average_mining_time(self, num_blocks):
        return sum(range(num_blocks)) / num_blocks

    def is_chain_valid(self):
        return True

def collect_filtered_bit_difficulties(blockchain, adjustment_interval):
    return blockchain.bit_difficulties
""",
        "proof_of_work.py": """import hashlib
import math
import random
from Blockchain-PoW-Consensus.block import Block
from Blockchain-PoW-Consensus.utils.logging_utils import log_mined_block
from Blockchain-PoW-Consensus.constants import HASH_BIT_LENGTH, NONCE_BIT_LENGTH

class ProofOfWork:
    @staticmethod
    def find_nonce(block, bit_difficulty):
        max_nonce = 2 ** NONCE_BIT_LENGTH - 1
        block.nonce = random.randint(0, max_nonce)
        target_value = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1
        base_hash_data = (str(block.index) + str(block.timestamp) + str(block.data) + str(block.previous_hash)).encode('utf-8')

        while True:
            sha = hashlib.sha256()
            sha.update(base_hash_data + str(block.nonce).encode('utf-8'))
            block.hash = sha.hexdigest()
            if int(block.hash, 16) < target_value:
                break
            block.nonce += 1
        log_mined_block(block)

    @staticmethod
    def validate_proof(block, bit_difficulty):
        target_value = math.pow(2, HASH_BIT_LENGTH - bit_difficulty) - 1
        return int(block.hash, 16) < target_value
""",
        "plotting.py": """import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from screeninfo import get_monitors
from Blockchain-PoW-Consensus.blockchain import Blockchain
from Blockchain-PoW-Consensus.constants import MARGIN_COEFFICIENT, DEFAULT_MARGIN, FONTSIZE

def plot_blockchain_statistics(blockchains, scaling_factor=1.0, linewidth=1, number_blocks_to_add=100):
    if not blockchains:
        raise ValueError("No blockchains provided")

    monitor = get_monitors()[0]
    if not monitor:
        raise RuntimeError("No monitor found")

    fig_width = monitor.width * 0.9 / 100
    fig_height = monitor.height * 0.9 / 100

    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    mining_time_colors = ['green', 'green', 'green']
    difficulty_colors = ['cyan', 'cyan', 'cyan']
    all_difficulties = [2**bit_difficulty for blockchain in blockchains.values() for bit_difficulty in blockchain.bit_difficulties]

    min_difficulty = min(all_difficulties) * scaling_factor
    max_difficulty = max(all_difficulties) * scaling_factor

    if min_difficulty == max_difficulty:
        epsilon = 1e-9
        max_difficulty += epsilon

    bar_width = 0.8 / number_blocks_to_add
    marker_size = (bar_width * 72) ** 2

    def update_plot(frame):
        ax1.clear()
        ax2 = ax1.twinx()

        for i, (base, blockchain) in enumerate(blockchains.items()):
            mining_time_color = mining_time_colors[i % len(mining_time_colors)]
            difficulty_color = difficulty_colors[i % len(difficulty_colors)]

            plot_mining_times_bar(ax1, blockchain, mining_time_color, bar_width, marker_size)

            ax1.set_xlabel('Block Index', fontsize=FONTSIZE)
            ax1.set_ylabel('Mining Time, seconds', fontsize=FONTSIZE, color=mining_time_color)
            ax1.tick_params(axis='y', labelcolor=mining_time_color)
            ax1.grid(True, which='both', linestyle=':', linewidth=0.5, color=mining_time_color)
            ax1.relim()
            ax1.autoscale_view()

            difficulties = [2**bit_difficulty * scaling_factor for bit_difficulty in blockchain.bit_difficulties]

            ax2.plot(range(len(difficulties)), difficulties, color=difficulty_color, linewidth=linewidth, label=f'Difficulty (base={base})')

            min_difficulty = min(difficulties)
            max_difficulty = max(difficulties)

            margin = DEFAULT_MARGIN if min_difficulty == max_difficulty else (max_difficulty - min_difficulty) * MARGIN_COEFFICIENT

            ax2.set_ylim(min_difficulty - margin, max_difficulty + margin)
            ax2.set_ylabel('Difficulty', fontsize=FONTSIZE, color=difficulty_color)
            ax2.tick_params(axis='y', labelcolor=difficulty_color)
            ax2.grid(True, which='both', linestyle=':', linewidth=0.5, color=difficulty_color)
            ax2.relim()
            ax2.autoscale_view()

        fig.tight_layout()
        fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=10)
        plt.title('Blockchain Mining Statistics', fontsize=14, color='white')

    ani = FuncAnimation(fig, update_plot, interval=1000)
    plt.show()

def plot_mining_times_bar(ax1, blockchain, mining_time_color, bar_width, marker_size):
    mining_times = blockchain.mining_times

    ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=0.5), width=bar_width)
    ax1.scatter(range(len(mining_times)), mining_times, color='lime', s=marker_size, zorder=3)
""",
        "block.py": """class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = None
        self.nonce = None
""",
        "utils": {
            "__init__.py": "",
            "logging_utils.py": """import logging

class LogLevelCounterHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.error_count = 0
        self.critical_count = 0

    def emit(self, record):
        if record.levelno == logging.ERROR:
            self.error_count += 1
        elif record.levelno == logging.CRITICAL:
            self.critical_count += 1

    def print_log_counts(self):
        logger = logging.getLogger()
        logger.error(f"Error messages: {self.error_count}")
        logger.critical(f"Critical messages: {self.critical_count}")

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_colors = {
            'DEBUG': '\\033[94m',
            'INFO': '\\033[92m',
            'WARNING': '\\033[93m',
            'ERROR': '\\033[91m',
            'CRITICAL': '\\033[95m'
        }
        reset_color = '\\033[0m'
        log_color = log_colors.get(record.levelname, reset_color)
        record.msg = f"{log_color}{record.msg}{reset_color}"
        return super().format(record)

def log_mined_block(block):
    logger = logging.getLogger()
    logger.info(f"Block mined:")
    logger.info(f"Index: {block.index}")
    logger.debug(f"Timestamp: {block.timestamp}")
    logger.debug(f"Data: {block.data}")
    logger.debug(f"Previous hash: {block.previous_hash}")
    logger.debug(f"Nonce: {block.nonce}")
    logger.debug(f"Hash: {block.hash}")

def log_time(average_time, expected_time):
    logger = logging.getLogger()
    logger.info(f"Average time: {average_time}, Expected time: {expected_time}")

def log_validity(blockchain):
    logger = logging.getLogger()
    is_blockchain_valid = blockchain.is_chain_valid()
    if is_blockchain_valid:
        logger.info(f"Blockchain is valid: {is_blockchain_valid}")
    else:
        logger.critical(f"Blockchain validity: {is_blockchain_valid}")
""",
            "logger_singleton.py": """import logging
from Blockchain-PoW-Consensus.utils.logging_utils import ColorFormatter

class LoggerSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if LoggerSingleton._instance is None:
            LoggerSingleton()
        return LoggerSingleton._instance

    def __init__(self):
        if LoggerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LoggerSingleton._instance = self
            self.logger = self.setup_logger()

    @staticmethod
    def setup_logger(level=logging.DEBUG, console_level=logging.DEBUG):
        logger = logging.getLogger()
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
"""
        }
    },
    "tests": {
        "__init__.py": "",
        "test_blockchain.py": """import unittest
from Blockchain-PoW-Consensus.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def test_add_blocks(self):
        blockchain = Blockchain(16, 10, 0.1)
        blockchain.add_blocks(10, 2, 4)
        self.assertEqual(len(blockchain.blocks), 10)

if __name__ == '__main__':
    unittest.main()
""",
        "test_proof_of_work.py": """import unittest
from Blockchain-PoW-Consensus.block import Block
from Blockchain-PoW-Consensus.proof_of_work import ProofOfWork

class TestProofOfWork(unittest.TestCase):
    def test_find_nonce(self):
        block = Block(0, 0, "data", "0")
        ProofOfWork.find_nonce(block, 16)
        self.assertIsNotNone(block.hash)

if __name__ == '__main__':
    unittest.main()
"""
    },
    "config.yaml": """# YAML configuration file
key: value
""",
    "requirements.txt": """# List of dependencies
matplotlib
screeninfo
pyyaml
"""
}


def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w') as file:
                file.write(content)


create_project_structure('..', project_structure)
