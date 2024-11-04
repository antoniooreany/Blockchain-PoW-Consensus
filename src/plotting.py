#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


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
        MINING_TIME_COLOR,
    )
    plot_bit_difficulties(
        ax1,
        blockchain,
        BIT_DIFFICULTY_COLOR,
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


# def plot_mining_times_bar(ax1: Axes, blockchain: Blockchain, mining_time_color: str) -> None:
#     mining_times = blockchain.mining_times
#
#     ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA),
#             width=BAR_WIDTH)
#     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE,
#                 zorder=AX1_SCATTER_Z_ORDER)
#     ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
#     ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
#     ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
#     ax1.grid(
#         AX1_GRID_BOOL,
#         which=AX1_GRID_WHICH,
#         linestyle=AX1_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=mining_time_color,
#     )
#     ax1.relim()
#     ax1.autoscale_view()
#     ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0



import matplotlib.colors as mcolors

# def plot_mining_times_bar(ax1: Axes, blockchain: Blockchain, mining_time_color: str) -> None:
#     mining_times = blockchain.mining_times
#     adjustment_interval = blockchain.adjustment_block_interval
#
#     ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA),
#             width=BAR_WIDTH)
#     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE,
#                 zorder=AX1_SCATTER_Z_ORDER)
#
#     # Add light green, transparent bars for each adjustment interval
#     for i in range(0, len(mining_times), adjustment_interval):
#         interval_times = mining_times[i:i + adjustment_interval]
#         avg_time = sum(interval_times) / len(interval_times)
#         ax1.bar(i + adjustment_interval / 2, avg_time, color='lightgreen', alpha=0.5, width=adjustment_interval, align='center')
#
#     ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
#     ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
#     ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
#     ax1.grid(
#         AX1_GRID_BOOL,
#         which=AX1_GRID_WHICH,
#         linestyle=AX1_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=mining_time_color,
#     )
#     ax1.relim()
#     ax1.autoscale_view()
#     ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0




import matplotlib.colors as mcolors

# def plot_mining_times_bar(ax1: Axes, blockchain: Blockchain, mining_time_color: str) -> None:
#     mining_times = blockchain.mining_times[1:]  # Exclude the Genesis Block
#     adjustment_interval = blockchain.adjustment_block_interval
#
#     ax1.bar(range(1, len(mining_times) + 1), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA),
#             width=BAR_WIDTH)
#     ax1.scatter(range(1, len(mining_times) + 1), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE,
#                 zorder=AX1_SCATTER_Z_ORDER)
#
#     # Add light green, transparent bars for each adjustment interval
#     for i in range(0, len(mining_times), adjustment_interval):
#         interval_times = mining_times[i:i + adjustment_interval]
#         avg_time = sum(interval_times) / len(interval_times)
#         ax1.bar(i + adjustment_interval / 2 + 1, avg_time, color='lightgreen', alpha=0.5, width=adjustment_interval, align='center')
#
#     ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
#     ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
#     ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
#     ax1.grid(
#         AX1_GRID_BOOL,
#         which=AX1_GRID_WHICH,
#         linestyle=AX1_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=mining_time_color,
#     )
#     ax1.relim()
#     ax1.autoscale_view()
#     ax1.set_xlim(left=0.5)  # Ensure the x-axis starts from 1





import matplotlib.colors as mcolors

# def plot_mining_times_bar(ax1, blockchain, mining_time_color):
#     mining_times = blockchain.mining_times[1:]  # Exclude the Genesis Block for calculations
#     adjustment_interval = blockchain.adjustment_block_interval
#
#     ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA), width=BAR_WIDTH)
#     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=AX1_SCATTER_Z_ORDER)
#
#     for i in range(0, len(mining_times), adjustment_interval):
#         interval_times = mining_times[i:i + adjustment_interval]
#         avg_time = sum(interval_times) / len(interval_times)
#         ax1.bar(i + adjustment_interval / 2, avg_time, color='lightgreen', alpha=0.5, width=adjustment_interval, align='center')
#
#     ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
#     ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
#     ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
#     ax1.grid(AX1_GRID_BOOL, which=AX1_GRID_WHICH, linestyle=AX1_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=mining_time_color)
#     ax1.relim()
#     ax1.autoscale_view()
#     ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0





import matplotlib.colors as mcolors

# def plot_mining_times_bar(ax1: Axes, blockchain: Blockchain, mining_time_color: str) -> None:
#     mining_times = blockchain.mining_times
#     adjustment_interval = blockchain.adjustment_block_interval
#
#     ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA),
#             width=BAR_WIDTH)
#     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE,
#                 zorder=AX1_SCATTER_Z_ORDER)
#
#     # Add light green, transparent bars for each adjustment interval
#     for i in range(0, len(mining_times), adjustment_interval):
#         interval_times = mining_times[i:i + adjustment_interval]
#         avg_time = sum(interval_times) / len(interval_times)
#         ax1.bar(i + adjustment_interval / 2, avg_time, color='lightgreen', alpha=0.5, width=adjustment_interval, align='center')
#
#     ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
#     ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
#     ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
#     ax1.grid(
#         AX1_GRID_BOOL,
#         which=AX1_GRID_WHICH,
#         linestyle=AX1_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=mining_time_color,
#     )
#     ax1.relim()
#     ax1.autoscale_view()
#     ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0





import matplotlib.colors as mcolors

def plot_mining_times_bar(ax1, blockchain, mining_time_color):
    mining_times = blockchain.mining_times  # Include the Genesis Block for plotting
    adjustment_interval = blockchain.adjustment_block_interval

    ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA), width=BAR_WIDTH)
    ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=AX1_SCATTER_Z_ORDER)

    for i in range(1, len(mining_times), adjustment_interval):
        interval_times = mining_times[i:i + adjustment_interval]
        avg_time = sum(interval_times) / len(interval_times)
        ax1.bar(i + adjustment_interval / 2, avg_time, color='lightgreen', alpha=0.5, width=adjustment_interval, align='center')

    ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
    ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
    ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
    ax1.grid(AX1_GRID_BOOL, which=AX1_GRID_WHICH, linestyle=AX1_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=mining_time_color)
    ax1.relim()
    ax1.autoscale_view()
    ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0



# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#     bit_difficulties = [np.log2(d) if d > 0 else "- INF" for d in difficulties]
#
#     ax2.plot(range(1, len(difficulties) + 1), difficulties, color=difficulty_color, linewidth=line_width,
#              label=AX2_PLOT_LABEL)
#     ax2.scatter(range(1, len(difficulties) + 1), difficulties, color=BIT_DIFFICULTY_SCATTER_COLOR, s=MARKER_SIZE,
#                 zorder=AX2_SCATTER_Z_ORDER)
#
#     min_difficulty, max_difficulty = min(difficulties), max(difficulties)
#     margin = max_difficulty * MARGIN_COEFFICIENT
#
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
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     ax2.yaxis.set_major_formatter(
#         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0
#         else INFINITY_0_DIFFICULTY_LABEL))
#
#     block_index: list = blockchain.block_indexes
#     mining_time: list = blockchain.mining_times
#     bit_difficulty: list = blockchain.bit_difficulties
#
#     # plot_gpt_suggestion(block_index=block_index, mining_time=mining_time, bit_difficulty=bit_difficulty)


# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Plot horizontal lines with markers
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=line_width)
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linestyle="--", linewidth=line_width / 2)
#
#     # Add markers at each difficulty point
#     ax2.scatter(range(1, len(difficulties) + 1), difficulties, color=difficulty_color, marker='o', s=MARKER_SIZE,
#                 zorder=AX2_SCATTER_Z_ORDER)
#
#     # Set labels and formatting
#     ax2.set_ylabel("Difficulty  /  Bit Difficulty, bits", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(
#         AX2_GRID_BOOL,
#         which=AX2_GRID_WHICH,
#         linestyle=AX2_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=difficulty_color,
#     )
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     # Format y-axis to show both log2 and raw values
#     ax2.yaxis.set_major_formatter(
#         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else INFINITY_0_DIFFICULTY_LABEL))



# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Set line width to be five times thicker
#     thicker_line_width = line_width * 5
#
#     # Plot horizontal lines with thicker blue lines
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linestyle="--", linewidth=thicker_line_width)
#
#     # Add bright red markers at each difficulty point
#     ax2.scatter(range(1, len(difficulties) + 1), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     # Set labels and formatting
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(
#         AX2_GRID_BOOL,
#         which=AX2_GRID_WHICH,
#         linestyle=AX2_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=difficulty_color,
#     )
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     # Format y-axis to show both log2 and raw values
#     ax2.yaxis.set_major_formatter(
#         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else INFINITY_0_DIFFICULTY_LABEL))




# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Set line width to be five times thicker
#     thicker_line_width = line_width * 5
#
#     # Plot only horizontal lines with thicker blue lines
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#
#     # Add bright red markers at each difficulty point
#     ax2.scatter(range(1, len(difficulties) + 1), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     # Set labels and formatting
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(
#         AX2_GRID_BOOL,
#         which=AX2_GRID_WHICH,
#         linestyle=AX2_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=difficulty_color,
#     )
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     # Format y-axis to show both log2 and raw values
#     ax2.yaxis.set_major_formatter(
#         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else INFINITY_0_DIFFICULTY_LABEL))



# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Set line width for horizontal and vertical lines
#     thicker_line_width = line_width * 5
#     thinner_line_width = line_width  # One-fifth thickness for vertical lines
#
#     # Plot horizontal lines with thicker blue lines and vertical connectors with thinner lines
#     for i in range(1, len(difficulties)):
#         # Horizontal line for each segment
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#         # Vertical line connecting to the next point
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linewidth=thinner_line_width)
#
#     # Add bright red markers at each difficulty point
#     ax2.scatter(range(1, len(difficulties) + 1), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     # Set labels and formatting
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(
#         AX2_GRID_BOOL,
#         which=AX2_GRID_WHICH,
#         linestyle=AX2_GRID_LINE_STYLE,
#         linewidth=GRID_LINE_WIDTH,
#         color=difficulty_color,
#     )
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     # Format y-axis to show both log2 and raw values
#     ax2.yaxis.set_major_formatter(
#         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else INFINITY_0_DIFFICULTY_LABEL))





# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     thicker_line_width = line_width * 5
#     thinner_line_width = line_width
#
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linewidth=thinner_line_width)
#
#     ax2.scatter(range(len(difficulties)), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=difficulty_color)
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else INFINITY_0_DIFFICULTY_LABEL))




# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     thicker_line_width = line_width * 5
#     thinner_line_width = line_width
#
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linewidth=thinner_line_width)
#
#     ax2.scatter(range(len(difficulties)), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=difficulty_color)
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else INFINITY_0_DIFFICULTY_LABEL))





# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Set the difficulty of the Genesis Block to 0
#     difficulties[0] = 0
#
#     thicker_line_width = line_width * 5
#     thinner_line_width = line_width
#
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linewidth=thinner_line_width)
#
#     ax2.scatter(range(len(difficulties)), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=difficulty_color)
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else INFINITY_0_DIFFICULTY_LABEL))




# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Set the difficulty of the Genesis Block to 0
#     difficulties[0] = 0
#
#     thicker_line_width = line_width * 5
#     thinner_line_width = line_width
#
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linewidth=thinner_line_width)
#
#     ax2.scatter(range(len(difficulties)), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=difficulty_color)
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     # Format y-axis to start from 00_000
#     ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else '00_000'))





import matplotlib.pyplot as plt

# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Set the difficulty of the Genesis Block to 0
#     difficulties[0] = 0
#
#     thicker_line_width = line_width * 5
#     thinner_line_width = line_width
#
#     for i in range(1, len(difficulties)):
#         ax2.plot([i - 1, i], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
#         ax2.plot([i, i], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linewidth=thinner_line_width)
#
#     ax2.scatter(range(len(difficulties)), difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)
#
#     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=difficulty_color)
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     # Format y-axis to start from 00_000
#     ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else '00_000'))





import matplotlib.pyplot as plt

def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
    ax2 = ax1.twinx()
    difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]

    # Set the difficulty of the Genesis Block to 0
    difficulties[0] = 0

    thicker_line_width = line_width * 5
    thinner_line_width = line_width

    for i in range(1, len(difficulties)):
        ax2.plot([i - 1.5, i - 0.5], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color, linewidth=thicker_line_width)
        ax2.plot([i - 0.5, i - 0.5], [difficulties[i - 1], difficulties[i]], color=difficulty_color, linewidth=thinner_line_width)

    ax2.scatter([x - 0.5 for x in range(len(difficulties))], difficulties, color='red', marker='o', s=MARKER_SIZE, zorder=AX2_SCATTER_Z_ORDER)

    ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
    ax2.tick_params(axis='y', labelcolor=difficulty_color)
    ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=difficulty_color)
    ax2.relim()
    ax2.autoscale_view()
    ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0

    # Format y-axis to start from 00_000
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else '00_000'))



# def plot_gpt_suggestion(block_index: list, mining_time: list, bit_difficulty: list) -> None:
#     fig, ax1 = plt.subplots(figsize=(14, 7))
#
#     # Bar plot for Mining Time
#     ax1.bar(block_index, mining_time, color='green', alpha=0.6, label='Block Mining Time (seconds)')
#     ax1.set_xlabel('Block Index')
#     ax1.set_ylabel('Block Mining Time (seconds)', color='green')
#     ax1.tick_params(axis='y', labelcolor='green')
#
#     # Line plot for Difficulty
#     ax2 = ax1.twinx()
#     ax2.plot(block_index, bit_difficulty, color='blue', linestyle='-', linewidth=1.5, label='Difficulty')
#     ax2.set_ylabel('Difficulty / Bit Difficulty', color='blue')
#     ax2.tick_params(axis='y', labelcolor='blue')
#
#     # Add grid and title
#     ax1.grid(visible=True, which='major', color='grey', linestyle='--', linewidth=0.5)
#     plt.title("Blockchain Mining Analysis\nKey Parameters: Initial Difficulty, Target Time, Adjustment Interval")
#
#     # Customize legend
#     fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
#
#     # Show plot
#     plt.tight_layout()
#     plt.show()
