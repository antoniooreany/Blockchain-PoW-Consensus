#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from screeninfo import get_monitors

from constants import (
    SCALING_FACTOR,
    LINE_WIDTH,
    PLOT_BACKGROUND,
    MINING_TIME_COLORS,
    BIT_DIFFICULTY_COLORS,
    FONT_SIZE,
    DEFAULT_MARGIN,
    MARGIN_COEFFICIENT,
    FIGURE_HEIGHT_SCALING_FACTOR,
    PIXEL_TO_INCH_CONVERSION,
    COLOR_LIST_LENGTH,
    BAR_WIDTH,
    EPSILON,
    GRID_LINE_WIDTH,
    LEGEND_B_BOX_Y,
    LEGEND_N_COL,
    LEGEND_FONT_SIZE,
    PLOT_TITLE_FONT_SIZE,
    MARKER_SIZE,

    AX1_GRID_LINE_STYLE,
    AX1_GRID_BOOL,
    AX1_GRID_WHICH,
    AX1_TICK_PARAMS_AXIS,
    AX1_Y_LABEL_TEXT,
    AX1_X_LABEL_TEXT,
    AX1_SCATTER_Z_ORDER,
    AX1_BAR_ALPHA,

    AX2_GRID_WHICH,
    AX2_GRID_BOOL,
    AX2_TICK_PARAMS_AXIS,
    AX2_Y_LABEL_TEXT,
    AX2_PLOT_LABEL,
    AX2_GRID_LINE_STYLE,

    MINING_TIMES_SCATTER_COLOR,
    PLOT_TITLE_COLOR,
    PLOT_TITLE_LABEL,
    LEGEND_LOCATION,
    FIGURE_BASE, FIGURE_WIDTH_SCALING_FACTOR, PLOT_TITLE_Y, BIT_DIFFICULTY_SCATTER_COLOR, AX2_SCATTER_Z_ORDER,

)
from src.blockchain import Blockchain


def plot_blockchain_statistics(
        blockchains: dict[int, Blockchain],
        scaling_factor: float = SCALING_FACTOR,
        # An optional parameter to scale the y-axis for the bit difficulties # todo remove from default
        line_width: int = LINE_WIDTH  # The width of the line to plot # todo remove from default
) -> None:
    if not blockchains:
        raise ValueError("No blockchains provided")

    monitor = get_monitors()[0]
    if not monitor:
        raise RuntimeError("No monitor found")

    (fig_width, fig_height) = (
        monitor.width * FIGURE_WIDTH_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION,
        monitor.height * FIGURE_HEIGHT_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION,
        # monitor.height * 3.0 / PIXEL_TO_INCH_CONVERSION,
    )

    plt.style.use(PLOT_BACKGROUND)
    ax1: Axes
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    mining_time_colors = [MINING_TIME_COLORS] * COLOR_LIST_LENGTH
    bit_difficulty_colors = [BIT_DIFFICULTY_COLORS] * COLOR_LIST_LENGTH
    all_bit_difficulties = [difficulty for blockchain in blockchains.values() for difficulty in
                            blockchain.bit_difficulties]

    min_bit_difficulty, max_bit_difficulty = (
        min(all_bit_difficulties) * scaling_factor,
        max(all_bit_difficulties) * scaling_factor
    )
    if min_bit_difficulty == max_bit_difficulty:
        max_bit_difficulty += EPSILON

    for i, (base, blockchain) in enumerate(blockchains.items()):
        plot_mining_times_bar(
            ax1,
            blockchain,
            mining_time_colors[i % len(mining_time_colors)],
        )  # todo Type 'Axes' doesn't have expected attributes 'set_xlabel', 'set_ylabel', 'tick_params', 'grid', 'relim', 'autoscale_view'
        plot_bit_difficulties(
            ax1,
            blockchain,
            bit_difficulty_colors[i % len(bit_difficulty_colors)],
            scaling_factor,
            line_width,
        )  # todo Type 'Axes' doesn't have expected attributes 'set_ylim', 'set_ylabel', 'tick_params', 'grid', 'relim', 'autoscale_view'

    fig.tight_layout()
    fig.legend(
        loc=LEGEND_LOCATION,
        bbox_to_anchor=(
            FIGURE_BASE,
            LEGEND_B_BOX_Y
        ),
        ncol=LEGEND_N_COL,
        fontsize=LEGEND_FONT_SIZE
    )
    plt.title(
        PLOT_TITLE_LABEL,
        fontsize=PLOT_TITLE_FONT_SIZE,
        color=PLOT_TITLE_COLOR,
        y=PLOT_TITLE_Y,
    )
    plt.show()


def plot_mining_times_bar(ax1, blockchain, mining_time_color):
    mining_times = blockchain.mining_times
    marker_size = MARKER_SIZE

    ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA),
            width=BAR_WIDTH)
    ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=marker_size,
                zorder=AX1_SCATTER_Z_ORDER)
    ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
    ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
    ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
    ax1.grid(
        AX1_GRID_BOOL,
        which=AX1_GRID_WHICH,
        linestyle=AX1_GRID_LINE_STYLE,
        linewidth=GRID_LINE_WIDTH,
        color=mining_time_color,
    )
    ax1.relim()
    ax1.autoscale_view()


def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
    ax2 = ax1.twinx()
    bit_difficulties = [difficulty * scaling_factor for difficulty in blockchain.bit_difficulties]

    ax2.plot(range(len(bit_difficulties)), bit_difficulties, color=difficulty_color, linewidth=line_width,
             label=AX2_PLOT_LABEL)
    ax2.scatter(range(len(bit_difficulties)), bit_difficulties, color=BIT_DIFFICULTY_SCATTER_COLOR, s=MARKER_SIZE,
                zorder=AX2_SCATTER_Z_ORDER)  # Add dots

    # ax2.set_xlabel(AX2_X_LABEL_TEXT, fontsize=FONT_SIZE)

    min_bit_difficulty, max_bit_difficulty = min(bit_difficulties), max(bit_difficulties)
    margin = DEFAULT_MARGIN if min_bit_difficulty == max_bit_difficulty \
        else (max_bit_difficulty - min_bit_difficulty) * MARGIN_COEFFICIENT

    # ax2.set_ylim(min_bit_difficulty - margin, max_bit_difficulty + margin)
    ax2.set_ylim(0, max_bit_difficulty + margin)
    # ax2.set_ylim(0, (max_bit_difficulty + margin) * 0.95)
    ax2.set_ylabel(AX2_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=difficulty_color)
    ax2.tick_params(axis=AX2_TICK_PARAMS_AXIS, labelcolor=difficulty_color)
    ax2.grid(
        AX2_GRID_BOOL,
        which=AX2_GRID_WHICH,
        linestyle=AX2_GRID_LINE_STYLE,
        linewidth=GRID_LINE_WIDTH,
        color=difficulty_color,
    )
    ax2.relim()
    ax2.autoscale_view()
