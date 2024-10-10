#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from screeninfo import get_monitors


def plot_blockchain_statistics(
        blockchains: dict,
        scaling_factor: float = 1.0
) -> None:
    """
    Plot statistics for multiple blockchains.
    :param blockchains: A dictionary mapping the name of each blockchain to its Blockchain object.
    :param scaling_factor: An optional parameter to scale the y-axis for the bit difficulties, default 1.0
    :return: None
    """
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
    # all_base_difficulties = []
    all_bit_difficulties = []

    for blockchain in blockchains.values():
        # all_base_difficulties.extend(blockchain.base_difficulties)
        all_bit_difficulties.extend(blockchain.bit_difficulties)

    min_bit_difficulty = min(all_bit_difficulties) * scaling_factor
    max_bit_difficulty = max(all_bit_difficulties) * scaling_factor

    # Add a small epsilon if min and max are identical
    if min_bit_difficulty == max_bit_difficulty:
        epsilon = 1e-9
        max_bit_difficulty += epsilon

    # Determine the common y-axis range for difficulties only
    for i, (base, blockchain) in enumerate(blockchains.items()):
        bit_difficulty_base_factor = math.log2(base)
        mining_time_color = mining_time_colors[i % len(mining_time_colors)]
        difficulty_color = difficulty_colors[i % len(difficulty_colors)]
        linewidth = base * 0.5

        ax1.scatter(
            range(len(blockchain.mining_times)),
            blockchain.mining_times,
            color=mining_time_color,
            s=np.pi * (base / 2) ** 2,
            label=f'Mining Time (base={base})'
        )

        ax1.plot(
            range(len(blockchain.mining_times)),
            blockchain.mining_times,
            color=mcolors.to_rgba(mining_time_color, alpha=0.5),
            linewidth=linewidth
        )

        ax1.set_xlabel('Block Index', fontsize=12)
        ax1.set_ylabel('Mining Time, seconds', fontsize=12, color=mining_time_color)
        ax1.tick_params(axis='y', labelcolor=mining_time_color)
        ax1.grid(True, which='both', linestyle=':', linewidth=0.5)
        ax1.relim()
        ax1.autoscale_view()

        ax2 = ax1.twinx()
        bit_difficulties = [
            base_difficulty * bit_difficulty_base_factor * scaling_factor
            for base_difficulty in blockchain.base_difficulties
        ]
        ax2.plot(
            range(len(bit_difficulties)),
            bit_difficulties,
            color=difficulty_color,
            linewidth=linewidth,
            label=f'Bit Difficulty (base={base})'
        )
        ax2.set_ylabel('Bit Difficulty, bits', fontsize=12, color=difficulty_color)
        ax2.tick_params(axis='y', labelcolor=difficulty_color)
        ax2.set_ylim(min_bit_difficulty, max_bit_difficulty)

    fig.tight_layout()
    fig.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        fontsize=10
    )
    plt.title('Blockchain Mining Statistics Comparison', fontsize=14, color='white')
    plt.show()
