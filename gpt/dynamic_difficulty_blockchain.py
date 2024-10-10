#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a dynamic_difficulty_blockchain and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import time
import math

# Начальные значения сложности и блока
INITIAL_BASE_DIFFICULTY = 16
BLOCKS_TO_ADJUST = 100  # Пересчитывать сложность каждые 100 блоков
TARGET_TIME_PER_BLOCK = 1  # Целевое время на блок — 1 секунда


class Blockchain:
    def __init__(self):
        self.blocks = []
        self.current_difficulty = INITIAL_BASE_DIFFICULTY
        self.start_time = time.time()  # Время начала майнинга для текущего периода

    def mine_block(self):
        # Логика майнинга блока
        block_time = time.time()  # Время добычи текущего блока
        self.blocks.append({
            'index': len(self.blocks) + 1,
            'difficulty': self.current_difficulty,
            'timestamp': block_time,
        })

        # Проверка, нужно ли пересчитывать сложность
        if len(self.blocks) % BLOCKS_TO_ADJUST == 0:
            self.adjust_difficulty()

    def adjust_difficulty(self):
        # Время добычи последних 100 блоков
        actual_time = time.time() - self.start_time
        expected_time = BLOCKS_TO_ADJUST * TARGET_TIME_PER_BLOCK

        # Корректировка сложности
        adjustment_factor = actual_time / expected_time
        self.current_difficulty = max(1, self.current_difficulty * adjustment_factor)

        print(f"Корректировка сложности: новая сложность {self.current_difficulty}")

        # Перезапуск отсчета времени для следующего периода
        self.start_time = time.time()

    def bit_difficulty(self):
        # Логарифмическая сложность
        return math.log2(self.current_difficulty)


# Создание блокчейна
blockchain = Blockchain()

# Майнинг блоков
for _ in range(1000):
    blockchain.mine_block()

# Вывод сложности
print(f"Сложность: {blockchain.bit_difficulty()}")

# Вывод блокчейна
for block in blockchain.blocks:
    print(block)

