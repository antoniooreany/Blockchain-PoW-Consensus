#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from screeninfo import get_monitors

from src.blockchain import Blockchain

MARGIN_COEFFICIENT = 0.1
DEFAULT_MARGIN = 1
FONTSIZE = 12


def plot_blockchain_statistics(
        blockchains: dict[int, Blockchain],  # base as key, Blockchain as value
        scaling_factor: float = 1.0,  # An optional parameter to scale the y-axis for the bit difficulties
        linewidth: int = 1  # The width of the line to plot
) -> None:
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
    all_bit_difficulties = []

    for blockchain in blockchains.values():
        all_bit_difficulties.extend(blockchain.bit_difficulties)

    min_bit_difficulty = min(all_bit_difficulties) * scaling_factor
    max_bit_difficulty = max(all_bit_difficulties) * scaling_factor

    if min_bit_difficulty == max_bit_difficulty:
        epsilon = 1e-9
        max_bit_difficulty += epsilon

    for i, (base, blockchain) in enumerate(blockchains.items()):
        mining_time_color = mining_time_colors[i % len(mining_time_colors)]
        difficulty_color = difficulty_colors[i % len(difficulty_colors)]

        plot_mining_times_bar(ax1, blockchain, mining_time_color)

        ax1.set_xlabel('Block Index', fontsize=FONTSIZE)
        ax1.set_ylabel('Mining Time, seconds', fontsize=FONTSIZE, color=mining_time_color)
        ax1.tick_params(axis='y', labelcolor=mining_time_color)
        ax1.grid(True, which='both', linestyle=':', linewidth=0.5, color=mining_time_color)
        ax1.relim()
        ax1.autoscale_view()

        ax2 = ax1.twinx()
        bit_difficulties = [
            bit_difficulty * scaling_factor
            for bit_difficulty in blockchain.bit_difficulties
        ]

        ax2.plot(
            range(len(bit_difficulties)),
            bit_difficulties,
            color=difficulty_color,
            linewidth=linewidth,
            label=f'Bit Difficulty (base={base})'
        )

        min_bit_difficulty = min(blockchain.bit_difficulties)
        max_bit_difficulty = max(blockchain.bit_difficulties)

        if min_bit_difficulty == max_bit_difficulty:
            margin = DEFAULT_MARGIN
        else:
            margin = (max_bit_difficulty - min_bit_difficulty) * MARGIN_COEFFICIENT

        ax2.set_ylim(min_bit_difficulty - margin, max_bit_difficulty + margin)
        ax2.set_ylabel('Bit Difficulty, bits', fontsize=FONTSIZE, color=difficulty_color)
        ax2.tick_params(axis='y', labelcolor=difficulty_color)
        ax2.grid(True, which='both', linestyle=':', linewidth=0.5, color=difficulty_color)
        ax2.relim()
        ax2.autoscale_view()

    fig.tight_layout()
    fig.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        fontsize=10
    )
    plt.title('Blockchain Mining Statistics', fontsize=14, color='white')
    plt.show()
    plt.show()


def plot_mining_times_bar(ax1, blockchain, mining_time_color):
    mining_times = blockchain.mining_times
    num_bars = len(mining_times)
    bar_width = 0.8  # Default bar width in matplotlib
    # marker_size = (bar_width * 72) ** 2  # Convert bar width to points squared for marker size
    # marker_size = bar_width  # Convert bar width to points squared for marker size
    marker_size = bar_width  # Convert bar width to points squared for marker size

    ax1.bar(
        range(len(mining_times)),
        mining_times,
        color=mcolors.to_rgba(mining_time_color, alpha=0.5),
        width=bar_width
    )
    ax1.scatter(
        range(len(mining_times)),
        mining_times,
        color='lime',  # Brighter color for the markers
        s=marker_size,  # Size of the markers matching the bar width
        zorder=3  # Ensure markers are on top
    )
