#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a blockchain and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import time

import numpy as np

from gpt.plot_statistics import plot_statistics


class Blockchain:
    def __init__(self, target_time_per_block=1, blocks_to_adjust=10):
        self.blocks = []
        self.target_time_per_block = target_time_per_block  # Целевое время на блок
        self.blocks_to_adjust = blocks_to_adjust  # Количество блоков до корректировки сложности
        self.difficulties = [1.0]  # Начальная сложность
        self.mining_times = []  # Время майнинга для каждого блока
        self.current_difficulty = 1.0
        self.start_time = time.time()

    def mine_block(self):
        if len(self.blocks) == 0:
            self.start_time = time.time()

        # Симуляция времени майнинга (случайные значения от 0.5 до 2.0 секунд)
        mining_time = np.random.uniform(0.5, 2.0)
        self.mining_times.append(mining_time)

        if len(self.blocks) >= self.blocks_to_adjust:
            self.adjust_difficulty()

        self.blocks.append(f"Block {len(self.blocks)}")

    def adjust_difficulty(self):
        # Среднее время последних блоков
        avg_mining_time = np.mean(self.mining_times[-self.blocks_to_adjust:])
        adjustment_factor = avg_mining_time / self.target_time_per_block
        self.current_difficulty *= adjustment_factor  # Корректировка сложности

        self.difficulties.append(self.current_difficulty)


# В блоке blockchain.py:
blockchain = Blockchain()

# Симуляция майнинга 30 блоков
for _ in range(300):
    blockchain.mine_block()

# В блоке plot_statistics.py:
plot_statistics(blockchain)
