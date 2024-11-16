#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import math

import numpy as np
from matplotlib import pyplot as plt

from src.constants import MINING_TIME_COLOR, FONT_SIZE, GRID_LINE_WIDTH, AVERAGE_MINING_TIME_COLOR, \
    TARGET_BLOCK_MINING_TIME, LINE_WIDTH, MINING_TIMES_SCATTER_COLOR, MARKER_SIZE, DIFFICULTY_COLOR, SCALING_FACTOR, \
    BASE, BAR_WIDTH, AX2_Y_LABEL_TEXT, LABEL_DIFFICULTY_COLOR, AX1_Y_LABEL_TEXT, AX1_X_LABEL_TEXT


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

    ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
    ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=MINING_TIME_COLOR)
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


