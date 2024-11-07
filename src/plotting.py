#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import matplotlib.pyplot as plt
import numpy as np

from constants import (
    MINING_TIME_COLOR, DIFFICULTY_COLOR, LINE_WIDTH, GRID_LINE_WIDTH,
    FONT_SIZE, MARKER_SIZE, BAR_WIDTH, PLOT_TITLE_Y, PLOT_TITLE_FONT_SIZE,
    X_LEGEND_POSITION, Y_LEGEND_POSITION, LEGEND_LOCATION, LEGEND_FONT_SIZE, MINING_TIMES_SCATTER_COLOR,
    TARGET_BLOCK_MINING_TIME
)


def plot_mining_times(ax1, blockchain):
    mining_times = blockchain.mining_times

    # Plot each mining time as a bar and scatter
    for i in range(len(mining_times)):
        ax1.plot([i, i], [0, mining_times[i]], color=MINING_TIME_COLOR, linewidth=LINE_WIDTH)
    ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=3)

    # Add a horizontal line at the height of the target mining time
    ax1.axhline(y=TARGET_BLOCK_MINING_TIME, color='blue', linestyle='--', linewidth=LINE_WIDTH / 2,
                label='Target Mining Time')

    ax1.set_xlabel('Block Index', fontsize=FONT_SIZE)
    ax1.set_ylabel('Block Mining Time (seconds)', fontsize=FONT_SIZE, color=MINING_TIME_COLOR)
    ax1.tick_params(axis='y', labelcolor=MINING_TIME_COLOR)
    ax1.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=MINING_TIME_COLOR)
    ax1.relim()
    ax1.autoscale_view()
    ax1.set_xlim(left=-0.5)
    ax1.set_ylim(bottom=0)  # Ensure the y-axis starts from 0


def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor):
    ax2 = ax1.twinx()
    difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]

    # Set the difficulty of the Genesis Block to 0. It was not rewritten, but added
    difficulties = [0] + difficulties

    # Create bar plot for bit difficulties
    ax2.bar(range(len(difficulties)), difficulties, color=difficulty_color, width=BAR_WIDTH)

    ax2.set_ylabel('Difficulty / Bit Difficulty', fontsize=FONT_SIZE, color=difficulty_color)
    ax2.tick_params(axis='y', labelcolor=difficulty_color)
    ax2.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=difficulty_color)
    ax2.relim()
    ax2.autoscale_view()
    ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0

    # Ensure that 0 is labeled as "-INF / 00_000"
    def custom_y_formatter(x, _):
        if x == 0:
            return "-INF / 00_000"
        else:
            return f'{float(np.log2(x)):.2f} / {x:_.0f}'

    ax2.yaxis.set_major_formatter(plt.FuncFormatter(custom_y_formatter))


def plot_blockchain_statistics(blockchain, scaling_factor=1.0):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot mining times and bit difficulties with updated functions
    plot_mining_times(ax1, blockchain)
    plot_bit_difficulties(ax1, blockchain, DIFFICULTY_COLOR,
                          scaling_factor)  # Corrected function call with DIFFICULTY_COLOR and scaling_factor

    # Legend adjustments
    legend_info = (
        f"Initial Bit Difficulty: {blockchain.initial_bit_difficulty}\n"
        f"Target Block Mining Time: {blockchain.target_block_mining_time}\n"
        f"Adjustment Interval: {blockchain.adjustment_block_interval}\n"
        f"Blocks to Add: {blockchain.number_blocks_to_add}\n"
        f"Clamp Factor: {blockchain.clamp_factor}\n"
        f"Min Bit Difficulty: {blockchain.smallest_bit_difficulty}\n"
        f"Blocks Slice: {blockchain.number_blocks_slice}\n"
    )

    # Legend with adjusted position
    fig.legend([legend_info], loc=LEGEND_LOCATION, bbox_to_anchor=(X_LEGEND_POSITION, Y_LEGEND_POSITION),
               fontsize=LEGEND_FONT_SIZE, title="Input Information", title_fontsize=LEGEND_FONT_SIZE)

    # Title with adjusted position
    plt.title('Blockchain Mining Statistics', fontsize=PLOT_TITLE_FONT_SIZE, y=PLOT_TITLE_Y)
    plt.show()
