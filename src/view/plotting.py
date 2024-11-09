#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from ..constants import (
    MINING_TIME_COLOR, DIFFICULTY_COLOR, LINE_WIDTH, GRID_LINE_WIDTH,
    FONT_SIZE, MARKER_SIZE, BAR_WIDTH, PLOT_TITLE_Y, PLOT_TITLE_FONT_SIZE,
    X_LEGEND_POSITION, Y_LEGEND_POSITION, LEGEND_LOCATION, LEGEND_FONT_SIZE, MINING_TIMES_SCATTER_COLOR,
    TARGET_BLOCK_MINING_TIME, LABEL_DIFFICULTY_COLOR, AVERAGE_MINING_TIME_COLOR, AX2_Y_LABEL_TEXT,
    INITIAL_BIT_DIFFICULTY_KEY, TARGET_BLOCK_MINING_TIME_KEY, ADJUSTMENT_BLOCK_INTERVAL_KEY, CLAMP_FACTOR_KEY,
    SMALLEST_BIT_DIFFICULTY_KEY, NUMBER_BLOCKS_TO_ADD_KEY, NUMBER_BLOCKS_SLICE_KEY, BASE, SCALING_FACTOR, FIGSIZE
)


def plot_mining_times(ax1, blockchain, color=MINING_TIME_COLOR):
    mining_times = blockchain.mining_times
    block_indices = range(len(mining_times))

    # Plot each mining time as a bar and scatter
    plot_mining_times_bars(ax1, block_indices, color, mining_times)

    # Add a horizontal line for the target mining time
    plot_target_mining_time(ax1)

    # Calculate and plot the average mining time per adjustment interval
    adjustment_interval = blockchain.adjustment_block_interval
    for start in range(1, len(mining_times), adjustment_interval):
        interval_mining_times = mining_times[start:start + adjustment_interval]
        if interval_mining_times:
            avg_mining_time = np.mean(interval_mining_times)  # todo not ideal, have to be modified: this calculation had been made in the controller: get_average_mining_time
            # avg_mining_time = blockchain.get_average_mining_time(adjustment_interval) # todo incorrect. have to be modified, no pressure.

            plot_average_mining_time_on_interval(adjustment_interval, avg_mining_time, ax1, start)

    ax1.set_xlabel('Block Index', fontsize=FONT_SIZE)
    ax1.set_ylabel('Block Mining Time (seconds)', fontsize=FONT_SIZE, color=MINING_TIME_COLOR)
    ax1.tick_params(axis='y', labelcolor=MINING_TIME_COLOR)
    ax1.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=MINING_TIME_COLOR)
    ax1.relim()
    ax1.autoscale_view()
    ax1.set_xlim(left=-0.5)
    # ax1.set_xlim(left=-5)
    ax1.set_ylim(bottom=0)  # Ensure the y-axis starts from 0


def plot_average_mining_time_on_interval(adjustment_interval, avg_mining_time, ax1, start):
    ax1.bar(start - 0.5, avg_mining_time, width=adjustment_interval, color=AVERAGE_MINING_TIME_COLOR, alpha=0.5,
            align='edge', label='Average Mining Time' if start == 1 else "")


def plot_target_mining_time(ax1):
    ax1.axhline(y=TARGET_BLOCK_MINING_TIME, color=MINING_TIME_COLOR, linestyle='--', linewidth=LINE_WIDTH / 2,
                label='Target Mining Time')


def plot_mining_times_bars(ax1, block_indices, color, mining_times):
    for index in block_indices:
        ax1.plot([index, index], [0, mining_times[index]], color=color, linewidth=LINE_WIDTH)
    ax1.scatter(block_indices, mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=3)


def plot_difficulties(ax1, blockchain, color=DIFFICULTY_COLOR, scaling_factor=SCALING_FACTOR):
    ax2 = ax1.twinx()  # Create a second y-axis
    difficulty_values = [(BASE ** difficulty) * scaling_factor for difficulty in blockchain.bit_difficulties]

    # Prepend 0 for Genesis Block difficulty
    difficulty_values.insert(0, 0)

    # Plot bar chart for difficulties
    ax2.bar(range(len(difficulty_values)), difficulty_values, color=color, width=BAR_WIDTH)

    # Set labels and grid
    ax2.set_ylabel(AX2_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=LABEL_DIFFICULTY_COLOR)
    ax2.tick_params(axis='y', labelcolor=LABEL_DIFFICULTY_COLOR)
    ax2.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=LABEL_DIFFICULTY_COLOR)
    ax2.relim()
    ax2.autoscale_view()
    ax2.set_xlim(left=-0.5)

    # Custom y-axis formatter for difficulties
    def custom_y_formatter(value, _):
        if value == 0:
            return "-INF / 00_000"
        return f'{float(math.log(value, BASE)):.2f} / {value:_.0f}'

    ax2.yaxis.set_major_formatter(plt.FuncFormatter(custom_y_formatter))


def plot_blockchain_statistics(blockchain):
    """
    Plot mining times and bit difficulties for the blockchain statistics.
    """
    fig, ax1 = plt.subplots(figsize=FIGSIZE)

    plot_mining_times(ax1, blockchain)
    plot_difficulties(ax1, blockchain)

    legend_info = (
        f"{INITIAL_BIT_DIFFICULTY_KEY}: {blockchain.initial_bit_difficulty}\n"
        f"{TARGET_BLOCK_MINING_TIME_KEY}: {blockchain.target_block_mining_time}\n"
        f"{ADJUSTMENT_BLOCK_INTERVAL_KEY}: {blockchain.adjustment_block_interval}\n"
        f"{CLAMP_FACTOR_KEY}: {blockchain.clamp_factor}\n"
        f"{SMALLEST_BIT_DIFFICULTY_KEY}: {blockchain.smallest_bit_difficulty}\n"
        f"{NUMBER_BLOCKS_TO_ADD_KEY}: {blockchain.number_blocks_to_add}\n"
        f"{NUMBER_BLOCKS_SLICE_KEY}: {blockchain.number_blocks_slice}\n"
    )

    legend_patch = mpatches.Patch(color='none', label=legend_info)

    fig.legend(handles=[legend_patch], loc=LEGEND_LOCATION, bbox_to_anchor=(X_LEGEND_POSITION, Y_LEGEND_POSITION),
    # LEGEND_BBOX_ANCHOR,
               fontsize=LEGEND_FONT_SIZE, title="Input Information", title_fontsize=LEGEND_FONT_SIZE)

    plt.title('Blockchain Mining Statistics', fontsize=PLOT_TITLE_FONT_SIZE, y=PLOT_TITLE_Y)
    plt.show()
