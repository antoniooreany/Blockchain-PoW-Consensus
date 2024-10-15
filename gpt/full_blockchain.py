#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a full_blockchain and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import time


class Block:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return str(hash(str(self.index) + str(self.timestamp) + str(self.data) + str(self.prev_hash) + str(self.nonce)))


class Blockchain:
    def __init__(self, difficulty):
        self.blocks = []
        self.difficulty = difficulty
        self.target_time = 1  # in seconds
        self.mining_times = []
        self.difficulties = []
        self.start_time = time.time()

    def add_block(self, new_block, mining_time):
        self.blocks.append(new_block)
        self.mining_times.append(mining_time)
        self.difficulties.append(self.difficulty)
        print(f"Mined block {new_block.index} with hash: {new_block.hash}")

    def adjust_difficulty(self):
        if len(self.blocks) >= 10:
            actual_time = sum(self.mining_times[-10:])
            expected_time = self.target_time * 10
            adjustment_factor = actual_time / expected_time
            self.difficulty = max(1, self.difficulty * adjustment_factor)
            print(f"Adjusted difficulty to {self.difficulty}")

    def bit_difficulty(self):
        return math.log2(self.difficulty)


def mine_block(blockchain, index):
    start_time = time.time()
    new_block = Block(index, time.time(), f"Block {index}", blockchain.blocks[-1].hash if blockchain.blocks else '0')
    while not new_block.hash.startswith('0' * int(blockchain.difficulty)):
        new_block.nonce += 1
        new_block.hash = new_block.calculate_hash()
    mining_time = time.time() - start_time
    blockchain.add_block(new_block, mining_time)
    blockchain.adjust_difficulty()


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

    if min_difficulty == max_difficulty:
        max_difficulty += 1e-9  # Add a small epsilon value to avoid singular transformation

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
                    color=difficulty_color)
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
    blockchain = Blockchain(difficulty=16)

    for i in range(30):  # Mining 30 blocks for demonstration
        mine_block(blockchain, i)

    plot_statistics(blockchain)
