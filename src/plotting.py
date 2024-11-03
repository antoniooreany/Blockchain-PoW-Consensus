#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


from matplotlib.axes import Axes
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from screeninfo import get_monitors

from constants import (
    SCALING_FACTOR,
    LINE_WIDTH,
    PLOT_BACKGROUND,
    MINING_TIME_COLOR,
    BIT_DIFFICULTY_COLOR,
    FONT_SIZE,
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
    FIGURE_BASE,
    FIGURE_WIDTH_SCALING_FACTOR,
    PLOT_TITLE_Y,
    BIT_DIFFICULTY_SCATTER_COLOR,
    AX2_SCATTER_Z_ORDER,
    INFINITY_0_DIFFICULTY_LABEL,
    TARGET_BLOCK_MINING_TIME,
    ADJUSTMENT_BLOCK_INTERVAL,
    CLAMP_FACTOR,
    SLICE_FACTOR,
    X_LEGEND_POSITION,
    Y_LEGEND_POSITION, INITIAL_BIT_DIFFICULTY, SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD,
)
from src.blockchain import Blockchain


def plot_blockchain_statistics(
        blockchain: Blockchain,
        scaling_factor: float = SCALING_FACTOR,
        # An optional parameter to scale the y-axis for the bit difficulties
        line_width: int = LINE_WIDTH,  # The width of the line to plot # todo remove from default
) -> None:
    if not blockchain:
        raise ValueError("No blockchain provided")

    monitor = get_monitors()[0]
    if not monitor:
        raise RuntimeError("No monitor found")

    (
        fig_width,
        fig_height
    ) = (
        monitor.width * FIGURE_WIDTH_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION,
        monitor.height * FIGURE_HEIGHT_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION,
    )

    plt.style.use(PLOT_BACKGROUND)
    ax1: Axes
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    all_bit_difficulties = blockchain.bit_difficulties

    min_bit_difficulty, max_bit_difficulty = (
        min(all_bit_difficulties) * scaling_factor,
        max(all_bit_difficulties) * scaling_factor
    )
    if min_bit_difficulty == max_bit_difficulty:
        max_bit_difficulty += EPSILON

    plot_mining_times_bar(
        ax1,
        blockchain,
        MINING_TIME_COLOR,  # todo singular?
    )  # todo Type 'Axes' doesn't have expected attributes 'set_xlabel', 'set_ylabel', 'tick_params', 'grid', 'relim', 'autoscale_view'
    plot_bit_difficulties(
        ax1,
        blockchain,
        BIT_DIFFICULTY_COLOR,  # todo singular?
        scaling_factor,
        line_width,
    )  # todo Type 'Axes' doesn't have expected attributes 'set_ylim', 'set_ylabel', 'tick_params', 'grid', 'relim', 'autoscale_view'

    legend_input_info: str = (
        f"Initial Bit Difficulty, bits: {blockchain.initial_bit_difficulty} \n"
        f"Target Block Mining Time, seconds: {blockchain.target_block_mining_time} \n"
        f"Adjustment Block Interval, blocks: {blockchain.adjustment_block_interval} \n"
        f"Number of Blocks to Add, blocks: {blockchain.number_blocks_to_add} \n"
        f"Clamp Factor, bits: {blockchain.clamp_factor} \n"
        f"Smallest Bit Difficulty, bits: {blockchain.smallest_bit_difficulty} \n"
        # f"Slice Factor, 1: {blockchain.slice_factor} \n"
        f"Number of Blocks Slice, blocks: {blockchain.number_blocks_slice} \n"
    )

    fig.tight_layout()
    fig.legend(
        loc=LEGEND_LOCATION,
        bbox_to_anchor=(
            FIGURE_BASE,
            LEGEND_B_BOX_Y
        ),
        ncol=LEGEND_N_COL,
        fontsize=LEGEND_FONT_SIZE,
        title="Input Information",
        title_fontsize=LEGEND_FONT_SIZE,
    )

    plt.figtext(
        x=X_LEGEND_POSITION,
        y=Y_LEGEND_POSITION,
        s=legend_input_info,
        wrap=True,
        # horizontalalignment='center',
        horizontalalignment='right',
        verticalalignment='top',
        fontsize=LEGEND_FONT_SIZE,
    )

    plt.title(
        PLOT_TITLE_LABEL,
        fontsize=PLOT_TITLE_FONT_SIZE,
        color=PLOT_TITLE_COLOR,
        y=PLOT_TITLE_Y,
    )
    plt.show()


def plot_mining_times_bar(ax1: Axes, blockchain: Blockchain, mining_time_color: str) -> None:
    mining_times = blockchain.mining_times

    ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA),
            width=BAR_WIDTH)
    ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE,
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
    ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0

# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in
#                     blockchain.bit_difficulties]  # todo is it ok to use bit_difficulty here?
#     bit_difficulties = [np.log2(d) if d > 0 else "- INF" for d in
#                         difficulties]  # Handle zero values todo do we need bit_difficulties here?
#
#     ax2.plot(range(len(difficulties)), difficulties, color=difficulty_color, linewidth=line_width,
#              label=AX2_PLOT_LABEL)
#     ax2.scatter(range(len(difficulties)), difficulties, color=BIT_DIFFICULTY_SCATTER_COLOR, s=MARKER_SIZE,
#                 zorder=AX2_SCATTER_Z_ORDER)  # Add dots
#
#     # ax2.set_xlabel(AX2_X_LABEL_TEXT, fontsize=FONT_SIZE)
#
#     min_difficulty, max_difficulty = min(difficulties), max(difficulties)
#     # margin = DEFAULT_MARGIN if min_difficulty == max_difficulty \
#     # margin = (max_difficulty - 0.0) * MARGIN_COEFFICIENT \
#     margin = max_difficulty * MARGIN_COEFFICIENT \
#         # if min_difficulty == max_difficulty \
#     # else (max_difficulty - min_difficulty) * MARGIN_COEFFICIENT  # todo do we need this? maybe margin = max_difficulty * MARGIN_COEFFICIENT?
#
#     # ax2.set_ylim(min_difficulty - margin, max_difficulty + margin)
#     ax2.set_ylim(0, max_difficulty + margin)
#     ax2.set_ylabel(AX2_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis=AX2_TICK_PARAMS_AXIS, labelcolor=difficulty_color)
#     ax2.grid(
#         AX2_GRID_BOOL,
#         which=AX2_GRID_WHICH,
#         linestyle=AX2_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=difficulty_color,
#     )
#     ax2.relim()
#     ax2.autoscale_view()
#
#     # Set the y-axis to be log scale
#     ax2.yaxis.set_major_formatter(
#         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0
#         else INFINITY_0_DIFFICULTY_LABEL))

def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
    ax2 = ax1.twinx()
    difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
    bit_difficulties = [np.log2(d) if d > 0 else "- INF" for d in difficulties]

    ax2.plot(range(1, len(difficulties) + 1), difficulties, color=difficulty_color, linewidth=line_width,
             label=AX2_PLOT_LABEL)
    ax2.scatter(range(1, len(difficulties) + 1), difficulties, color=BIT_DIFFICULTY_SCATTER_COLOR, s=MARKER_SIZE,
                zorder=AX2_SCATTER_Z_ORDER)

    min_difficulty, max_difficulty = min(difficulties), max(difficulties)
    margin = max_difficulty * MARGIN_COEFFICIENT

    ax2.set_ylim(0, max_difficulty + margin)
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
    ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0

    ax2.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0
        else INFINITY_0_DIFFICULTY_LABEL))

