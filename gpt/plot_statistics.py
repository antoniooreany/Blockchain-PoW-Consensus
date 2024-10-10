#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a plot_statistics and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import matplotlib.pyplot as plt


def plot_statistics(blockchain):
    # График времени майнинга
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Номер блока')
    ax1.set_ylabel('Время майнинга, сек', color='green')
    ax1.plot(blockchain.mining_times, 'go-', label='Время майнинга', color='green')
    ax1.tick_params(axis='y', labelcolor='green')

    # Вторая ось для отображения сложности
    ax2 = ax1.twinx()
    ax2.set_ylabel('Линейная сложность', color='blue')
    ax2.plot(range(blockchain.blocks_to_adjust, len(blockchain.blocks)), blockchain.difficulties[1:], 'bo-',
             label='Сложность', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.title("Статистика майнинга и сложности блокчейна")
    fig.tight_layout()
    plt.show()
