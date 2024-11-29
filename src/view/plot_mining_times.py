#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import math

import matplotlib
import numpy as np

from src.constants import MINING_TIME_COLOR, FONT_SIZE, GRID_LINE_WIDTH, AVERAGE_MINING_TIME_COLOR, \
    TARGET_BLOCK_MINING_TIME, LINE_WIDTH, MINING_TIMES_SCATTER_COLOR, MARKER_SIZE, AX1_Y_LABEL_TEXT, AX1_X_LABEL_TEXT

def plot_mining_times(ax1, blockchain, color=MINING_TIME_COLOR):
    """
    Plot the mining times for each block in the blockchain.

    Args:
        ax1: The matplotlib axis to plot on.
        blockchain: The blockchain object containing mining times.
        color: The color to use for the mining times plot.

    This function plots bars and scatter points for each block's mining time,
    adds a horizontal line for the target mining time, and calculates and plots
    the average mining time per adjustment interval.
    """
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
            # Calculate the average mining time for the current interval
            avg_mining_time = np.mean(interval_mining_times)  # todo not ideal, need to modify based on controller calculation

            # Plot the average mining time on the interval
            plot_average_mining_time_on_interval(adjustment_interval, avg_mining_time, ax1, start)

    # Set axis labels and grid properties
    ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
    ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=MINING_TIME_COLOR)
    ax1.tick_params(axis='y', labelcolor=MINING_TIME_COLOR)
    ax1.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=MINING_TIME_COLOR)
    ax1.relim()
    ax1.autoscale_view()
    ax1.set_xlim(left=-0.5)
    ax1.set_ylim(bottom=0)  # Ensure the y-axis starts from 0


def plot_average_mining_time_on_interval(
        adjustment_interval: int,  # The number of blocks in the interval.
        avg_mining_time: float,  # The average mining time for the interval.
        ax1: matplotlib.axes.Axes,  # The matplotlib axis to plot on.
        start: int  # The starting block index of the interval.
) -> None:
    """
    Plot the average mining time as a bar on the given interval.

    Args:
        adjustment_interval (int): The number of blocks in the interval.
        avg_mining_time (float): The average mining time for the interval.
        ax1 (matplotlib.axes.Axes): The matplotlib axis to plot on.
        start (int): The starting block index of the interval.

    Returns:
        None
    """
    # Plot the average mining time as a bar on the interval
    ax1.bar(start - 0.5, avg_mining_time, width=adjustment_interval, color=AVERAGE_MINING_TIME_COLOR, alpha=0.5,
            align='edge', label='Average Mining Time' if start == 1 else "")


def plot_target_mining_time(ax1: matplotlib.axes.Axes) -> None:
    """
    Plot the target mining time as a horizontal line on the given axis.

    Args:
        ax1 (matplotlib.axes.Axes): The matplotlib axis to plot on.

    Returns:
        None
    """
    ax1.axhline(y=TARGET_BLOCK_MINING_TIME, color=MINING_TIME_COLOR, linestyle='--', linewidth=LINE_WIDTH / 2,
                label='Target Mining Time')


def plot_mining_times_bars(ax1: matplotlib.axes.Axes, block_indices: list[int], color: str, mining_times: list[float]) -> None:
    """
    Plot mining times as bars and scatter points on the given axis.

    Args:
        ax1 (matplotlib.axes.Axes): The matplotlib axis to plot on.
        block_indices (list[int]): The indices of the blocks to plot.
        color (str): The color for the bars.
        mining_times (list[float]): The list of mining times for each block.

    Returns:
        None
    """
    for index in block_indices:
        ax1.plot([index, index], [0, mining_times[index]], color=color, linewidth=LINE_WIDTH)
    ax1.scatter(block_indices, mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=3)


