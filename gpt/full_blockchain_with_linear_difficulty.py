#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a full_blockchain_with_linear_difficulty and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import time

import matplotlib.pyplot as plt


class Block:
    def __init__(self, index, timestamp, data, previous_hash="0"):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode(
                'utf-8')
        )
        return sha.hexdigest()

    def mine_block(self, blockchain):
        print(f"Начинается майнинг блока {self.index}...")
        start_time = time.time()
        while not self.hash.startswith('0' * int(blockchain.current_difficulty)):
            self.nonce += 1
            self.hash = self.calculate_hash()
        mining_time = time.time() - start_time
        blockchain.add_block(self, mining_time)
        blockchain.adjust_difficulty()
        print(f"Майнинг блока {self.index} завершен.")


class Blockchain:
    def __init__(self, initial_difficulty, target_block_time, adjustment_interval=10):
        self.blocks = []
        self.difficulties = []
        self.mining_times = []
        self.current_difficulty = initial_difficulty
        self.target_block_time = target_block_time
        self.adjustment_interval = adjustment_interval
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.blocks.append(genesis_block)
        self.difficulties.append(self.current_difficulty)
        self.mining_times.append(0)

    def add_block(self, new_block, mining_time):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.blocks.append(new_block)
        self.difficulties.append(self.current_difficulty)
        self.mining_times.append(mining_time)

    def get_latest_block(self):
        return self.blocks[-1]

    def adjust_difficulty(self):
        average_time = self.get_average_mining_time(self.adjustment_interval)
        if average_time < self.target_block_time:
            self.current_difficulty += 1
        elif average_time > self.target_block_time:
            self.current_difficulty -= 1

    def get_average_mining_time(self, num_blocks=10):
        if len(self.mining_times) < num_blocks:
            return sum(self.mining_times) / len(self.mining_times)
        return sum(self.mining_times[-num_blocks:]) / num_blocks


def mine_blocks(blockchain, num_blocks):
    if len(blockchain.blocks) == 0:
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        blockchain.add_block(genesis_block, 0)

    for i in range(1, num_blocks + 1):
        new_block = Block(i, time.time(), f"Block {i}", blockchain.get_latest_block().hash)
        new_block.mine_block(blockchain)


def plot_statistics(blockchain):
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Block Index')
    ax1.set_ylabel('Mining Time (s)', color='green')
    ax1.plot(range(len(blockchain.mining_times)), blockchain.mining_times, 'o-', color='green')
    ax1.tick_params(axis='y', labelcolor='green')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Difficulty', color='cyan')
    ax2.plot(range(len(blockchain.bit_difficulties)), blockchain.bit_difficulties, 'o-', color='cyan')
    ax2.tick_params(axis='y', labelcolor='cyan')

    fig.tight_layout()
    plt.title('Blockchain Mining Statistics Comparison')
    plt.show()


if __name__ == "__main__":
    blockchain = Blockchain(initial_difficulty=6, target_block_time=1, adjustment_interval=10)
    mine_blocks(blockchain, num_blocks=30)
    plot_statistics(blockchain)
