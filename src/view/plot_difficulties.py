#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# path: src/view/plot_difficulties.py

import math

from matplotlib import pyplot as plt

from src.constants import DIFFICULTY_COLOR, SCALING_FACTOR, BASE, BAR_WIDTH, LABEL_DIFFICULTY_COLOR, AX2_Y_LABEL_TEXT, \
    FONT_SIZE, GRID_LINE_WIDTH, INFINITY_0_DIFFICULTY_LABEL

from typing import List

def plot_difficulties(ax1: plt.Axes, blockchain: 'Blockchain', color: str = DIFFICULTY_COLOR, scaling_factor: float = SCALING_FACTOR) -> None:
    """
    Plot the bit difficulties of the blockchain using a bar chart.

    Parameters:
        ax1 (plt.Axes): The first axis to plot the mining times
        blockchain (Blockchain): The blockchain to plot the difficulties from
        color (str): The color of the bar chart (default: DIFFICULTY_COLOR)
        scaling_factor (float): The factor to scale the y-axis of the bar chart (default: SCALING_FACTOR)
    """
    ax2 = ax1.twinx()  # Create a second y-axis
    difficulty_values: List[float] = [(BASE ** difficulty) * scaling_factor for difficulty in blockchain.bit_difficulties]

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
    def custom_y_formatter(value: float, _) -> str:
        if value == 0:
            # return "-INF / 00_000"
            return INFINITY_0_DIFFICULTY_LABEL
        return f'{float(math.log(value, BASE)):.2f} / {value:_.0f}'

    ax2.yaxis.set_major_formatter(plt.FuncFormatter(custom_y_formatter))
