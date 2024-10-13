#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from screeninfo import get_monitors

from src.blockchain import Blockchain

MARGIN_COEFFICIENT = 0.1

DEFAULT_MARGIN = 1

FONTSIZE = 12


def plot_blockchain_statistics(
        blockchains: dict[int, Blockchain],  # base as key, Blockchain as value
        scaling_factor: float = 1.0,  # An optional parameter to scale the y-axis for the bit difficulties
        linewidth: int = 1  # The width of the line to plot
) -> None:  # returns None
    """
    Plot statistics for multiple blockchains.

    :param linewidth: The width of the line to plot
    :param blockchains: A dictionary mapping the name of each blockchain to its Blockchain object
    :param scaling_factor: An optional parameter to scale the y-axis for the bit difficulties, default 1.0
    :return: None
    """
    if not blockchains:
        raise ValueError("No blockchains provided")

    monitor: get_monitors()[0] = get_monitors()[0]
    if not monitor:
        raise RuntimeError("No monitor found")

    fig_width: float = monitor.width * 0.9 / 100
    fig_height: float = monitor.height * 0.9 / 100

    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    mining_time_colors: list[str] = ['green', 'green', 'green']
    difficulty_colors: list[str] = ['cyan', 'cyan', 'cyan']
    all_bit_difficulties: list[float] = []

    for blockchain in blockchains.values():
        all_bit_difficulties.extend(blockchain.bit_difficulties)  # todo no property bit_difficulties in Blockchain

    min_bit_difficulty = min(all_bit_difficulties) * scaling_factor
    max_bit_difficulty = max(all_bit_difficulties) * scaling_factor

    # Add a small epsilon if min and max are identical
    if min_bit_difficulty == max_bit_difficulty:
        epsilon = 1e-9
        max_bit_difficulty += epsilon

    # Determine the common y-axis range for difficulties only
    for i, (base, blockchain) in enumerate(blockchains.items()):
        mining_time_color: str = mining_time_colors[i % len(mining_time_colors)]
        difficulty_color: str = difficulty_colors[i % len(difficulty_colors)]

        # Plot mining times
        scatter_mining_times(ax1, base, blockchain, mining_time_color)

        # Plot mining times as vertical lines
        # plt.vlines(x=block_indices, ymin=0, ymax=mining_times, color='r', label='Mining Time')

        plot_mining_times(ax1, blockchain, linewidth, mining_time_color)

        ax1.set_xlabel('Block Index', fontsize=FONTSIZE)
        ax1.set_ylabel('Mining Time, seconds', fontsize=FONTSIZE, color=mining_time_color)

        ax1.tick_params(axis='y', labelcolor=mining_time_color)
        ax1.grid(True, which='both', linestyle=':', linewidth=0.5, color=mining_time_color)
        ax1.relim()

        ax1.autoscale_view()

        # # Plot Mining Time as vertical segments
        # color = 'tab:green'
        # ax1.set_xlabel('Block Index')
        # ax1.set_ylabel('Mining Time (s)', color=color)
        # ax1.vlines(range(len(blockchain.mining_times)), 0, blockchain.mining_times, color=color, linewidth=2)
        # ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        bit_difficulties = [
            bit_difficulty * scaling_factor
            for bit_difficulty in blockchain.bit_difficulties  # todo no property bit_difficulties in Blockchain
        ]

        # Plot difficulties
        ax2.plot(
            range(len(bit_difficulties)),
            bit_difficulties,
            # 'o-',
            color=difficulty_color,
            linewidth=linewidth,
            label=f'Bit Difficulty (base={base})'
        )

        # Add a small margin to the y-axis limits for Bit Difficulty
        min_bit_difficulty = min(blockchain.bit_difficulties)
        max_bit_difficulty = max(blockchain.bit_difficulties)

        # Ensure that min_bit_difficulty and max_bit_difficulty are not identical
        if min_bit_difficulty == max_bit_difficulty:
            margin = DEFAULT_MARGIN  # or any small value to create a difference
        else:
            margin = (max_bit_difficulty - min_bit_difficulty) * MARGIN_COEFFICIENT  # 10% margin

        ax2.set_ylim(min_bit_difficulty - margin, max_bit_difficulty + margin)

        ax2.set_ylabel('Bit Difficulty, bits', fontsize=FONTSIZE, color=difficulty_color)
        ax2.tick_params(axis='y', labelcolor=difficulty_color)

        ax2.grid(True, which='both', linestyle=':', linewidth=0.5, color=difficulty_color)
        ax2.relim()
        ax2.autoscale_view()

        # # Plot difficulties as a lines collection:
        # ax2.plot(
        #     range(len(bit_difficulties)),
        #     bit_difficulties,
        #     color=difficulty_color,
        #     linewidth=linewidth,
        #     label=f'Bit Difficulty (base={base})'
        # )

    fig.tight_layout()
    fig.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        fontsize=10
    )
    plt.title('Blockchain Mining Statistics', fontsize=14, color='white')
    plt.show()


def plot_mining_times(ax1, blockchain, linewidth, mining_time_color):
    ax1.plot(
        range(len(blockchain.mining_times)),
        # ymin=0,
        blockchain.mining_times,
        color=mcolors.to_rgba(mining_time_color, alpha=0.5),
        linewidth=linewidth,
    )


def scatter_mining_times(ax1, base, blockchain, mining_time_color):
    ax1.scatter(
        range(len(blockchain.mining_times)),
        blockchain.mining_times,
        color=mining_time_color,
        s=np.pi * (base / 2) ** 2,  # todo base is not a property of blockchain
        label=f'Mining Time (base={base})'  # todo base is not a property of blockchain
    )
