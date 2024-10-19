# # #   Copyright (c) 2024, Anton Gorshkov
# # #   All rights reserved.
# # #
# # #   This code is for a plotting and its unit tests.
# # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# #
# #
# # import matplotlib.colors as mcolors
# # import matplotlib.pyplot as plt
# # from screeninfo import get_monitors
# #
# # from constants import FONTSIZE, DEFAULT_MARGIN, MARGIN_COEFFICIENT
# # from src.blockchain import Blockchain
# #
# #
# # def plot_blockchain_statistics(
# #         blockchains: dict[int, Blockchain],  # base as key, Blockchain as value
# #         scaling_factor: float = 1.0,  # An optional parameter to scale the y-axis for the bit difficulties
# #         line_width: int = 1  # The width of the line to plot
# # ) -> None:
# #     if not blockchains:
# #         raise ValueError("No blockchains provided")
# #
# #     monitor = get_monitors()[0]
# #     if not monitor:
# #         raise RuntimeError("No monitor found")
# #
# #     fig_width = monitor.width * 0.9 / 100
# #     fig_height = monitor.height * 0.9 / 100
# #
# #     plt.style.use('dark_background')
# #     fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
# #
# #     mining_time_colors = ['green', 'green', 'green']
# #     difficulty_colors = ['cyan', 'cyan', 'cyan']
# #     all_bit_difficulties = []
# #
# #     for blockchain in blockchains.values():
# #         all_bit_difficulties.extend(blockchain.bit_difficulties)
# #
# #     min_bit_difficulty = min(all_bit_difficulties) * scaling_factor
# #     max_bit_difficulty = max(all_bit_difficulties) * scaling_factor
# #
# #     if min_bit_difficulty == max_bit_difficulty:
# #         epsilon = 1e-9
# #         max_bit_difficulty += epsilon
# #
# #     for i, (base, blockchain) in enumerate(blockchains.items()):
# #         mining_time_color = mining_time_colors[i % len(mining_time_colors)]
# #         difficulty_color = difficulty_colors[i % len(difficulty_colors)]
# #
# #         plot_mining_times_bar(ax1, blockchain, mining_time_color)
# #
# #         ax1.set_xlabel('Block Index', fontsize=FONTSIZE)
# #         ax1.set_ylabel('Mining Time, seconds', fontsize=FONTSIZE, color=mining_time_color)
# #         ax1.tick_params(axis='y', labelcolor=mining_time_color)
# #         ax1.grid(True, which='both', linestyle=':', linewidth=0.5, color=mining_time_color)
# #         ax1.relim()
# #         ax1.autoscale_view()
# #
# #         ax2 = ax1.twinx()
# #         bit_difficulties = [
# #             bit_difficulty * scaling_factor
# #             for bit_difficulty in blockchain.bit_difficulties
# #         ]
# #
# #         ax2.plot(
# #             range(len(bit_difficulties)),
# #             bit_difficulties,
# #             color=difficulty_color,
# #             linewidth=line_width,
# #             label=f'Bit Difficulty (base={base})'
# #         )
# #
# #         min_bit_difficulty = min(blockchain.bit_difficulties)
# #         max_bit_difficulty = max(blockchain.bit_difficulties)
# #
# #         if min_bit_difficulty == max_bit_difficulty:
# #             margin = DEFAULT_MARGIN
# #         else:
# #             margin = (max_bit_difficulty - min_bit_difficulty) * MARGIN_COEFFICIENT
# #
# #         ax2.set_ylim(min_bit_difficulty - margin, max_bit_difficulty + margin)
# #         ax2.set_ylabel('Bit Difficulty, bits', fontsize=FONTSIZE, color=difficulty_color)
# #         ax2.tick_params(axis='y', labelcolor=difficulty_color)
# #         ax2.grid(True, which='both', linestyle=':', linewidth=0.5, color=difficulty_color)
# #         ax2.relim()
# #         ax2.autoscale_view()
# #
# #     fig.tight_layout()
# #     fig.legend(
# #         loc='upper center',
# #         bbox_to_anchor=(0.5, -0.1),
# #         ncol=3,
# #         fontsize=10
# #     )
# #     plt.title('Blockchain Mining Statistics', fontsize=14, color='white')
# #     plt.show()
# #     plt.show()
# #
# #
# # def plot_mining_times_bar(ax1, blockchain, mining_time_color):
# #     mining_times = blockchain.mining_times
# #     num_bars = len(mining_times)
# #     bar_width = 0.8  # Default bar width in matplotlib
# #     marker_size = bar_width  # Convert bar width to points squared for marker size
# #
# #     ax1.bar(
# #         range(num_bars),
# #         mining_times,
# #         color=mcolors.to_rgba(mining_time_color, alpha=0.5),
# #         width=bar_width
# #     )
# #     ax1.scatter(
# #         range(num_bars),
# #         mining_times,
# #         color='lime',  # Brighter color for the markers
# #         s=marker_size,  # Size of the markers matching the bar width
# #         zorder=3  # Ensure markers are on top
# #     )
#
#
# import matplotlib.colors as mcolors
# import matplotlib.pyplot as plt
# from screeninfo import get_monitors
#
# from constants import FONTSIZE, DEFAULT_MARGIN, MARGIN_COEFFICIENT
# from src.blockchain import Blockchain
#
#
# def plot_blockchain_statistics(
#         blockchains: dict[int, Blockchain],
#         scaling_factor: float = 1.0,
#         line_width: int = 1
# ) -> None:
#     if not blockchains:
#         raise ValueError("No blockchains provided")
#
#     monitor = get_monitors()[0]
#     if not monitor:
#         raise RuntimeError("No monitor found")
#
#     fig_width, fig_height = monitor.width * 0.9 / 100, monitor.height * 0.9 / 100
#
#     plt.style.use('dark_background')
#     fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
#
#     mining_time_colors = ['green'] * 3
#     difficulty_colors = ['cyan'] * 3
#     all_bit_difficulties = [difficulty for blockchain in blockchains.values() for difficulty in
#                             blockchain.bit_difficulties]
#
#     min_bit_difficulty, max_bit_difficulty = min(all_bit_difficulties) * scaling_factor, max(
#         all_bit_difficulties) * scaling_factor
#     if min_bit_difficulty == max_bit_difficulty:
#         max_bit_difficulty += 1e-9
#
#     for i, (base, blockchain) in enumerate(blockchains.items()):
#         plot_mining_times_bar(ax1, blockchain, mining_time_colors[i % len(mining_time_colors)])
#         plot_bit_difficulties(ax1, blockchain, difficulty_colors[i % len(difficulty_colors)], base, scaling_factor,
#                               line_width)
#
#     fig.tight_layout()
#     fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=10)
#     plt.title('Blockchain Mining Statistics', fontsize=14, color='white')
#     plt.show()
#
#
# def plot_mining_times_bar(ax1, blockchain, mining_time_color):
#     mining_times = blockchain.mining_times
#     bar_width = 0.8
#     marker_size = bar_width
#
#     ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=0.5),
#             width=bar_width)
#     ax1.scatter(range(len(mining_times)), mining_times, color='lime', s=marker_size, zorder=3)
#     ax1.set_xlabel('Block Index', fontsize=FONTSIZE)
#     ax1.set_ylabel('Mining Time, seconds', fontsize=FONTSIZE, color=mining_time_color)
#     ax1.tick_params(axis='y', labelcolor=mining_time_color)
#     ax1.grid(True, which='both', linestyle=':', linewidth=0.5, color=mining_time_color)
#     ax1.relim()
#     ax1.autoscale_view()
#
#
# def plot_bit_difficulties(ax1, blockchain, difficulty_color, base, scaling_factor, line_width):
#     ax2 = ax1.twinx()
#     bit_difficulties = [difficulty * scaling_factor for difficulty in blockchain.bit_difficulties]
#
#     ax2.plot(range(len(bit_difficulties)), bit_difficulties, color=difficulty_color, linewidth=line_width,
#              label=f'Bit Difficulty (base={base})')
#
#     min_bit_difficulty, max_bit_difficulty = min(bit_difficulties), max(bit_difficulties)
#     margin = DEFAULT_MARGIN if min_bit_difficulty == max_bit_difficulty else (
#                                                                                      max_bit_difficulty - min_bit_difficulty) * MARGIN_COEFFICIENT
#
#     ax2.set_ylim(min_bit_difficulty - margin, max_bit_difficulty + margin)
#     ax2.set_ylabel('Bit Difficulty, bits', fontsize=FONTSIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(True, which='both', linestyle=':', linewidth=0.5, color=difficulty_color)
#     ax2.relim()
#     ax2.autoscale_view()


import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
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
    FIGURE_SCALING_FACTOR,
    PIXEL_TO_INCH_CONVERSION,
    COLOR_LIST_LENGTH,
    BAR_WIDTH,
    EPSILON,
    GRID_LINE_WIDTH,
    LEGEND_B_BOX_Y,
    LEGEND_N_COL,
    LEGEND_FONT_SIZE,
    TITLE_FONT_SIZE,
    MARKER_SIZE,
)
from src.blockchain import Blockchain

PLOT_TITLE_COLOR = 'white'

PLOT_TITLE_LABEL = 'Blockchain Mining Statistics'

FIGURE_BASE = 0.5

LEGEND_LOCATION = 'upper center'


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
        monitor.width * FIGURE_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION,
        monitor.height * FIGURE_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION
    )

    plt.style.use(PLOT_BACKGROUND)
    fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))

    mining_time_colors = [MINING_TIME_COLORS] * COLOR_LIST_LENGTH
    bit_difficulty_colors = [BIT_DIFFICULTY_COLORS] * COLOR_LIST_LENGTH
    all_bit_difficulties = [difficulty for blockchain in blockchains.values() for difficulty in
                            blockchain.bit_difficulties]

    min_bit_difficulty, max_bit_difficulty = min(all_bit_difficulties) * scaling_factor, max(
        all_bit_difficulties) * scaling_factor
    if min_bit_difficulty == max_bit_difficulty:
        max_bit_difficulty += EPSILON

    for i, (base, blockchain) in enumerate(blockchains.items()):
        plot_mining_times_bar(ax1, blockchain, mining_time_colors[i % len(mining_time_colors)])
        plot_bit_difficulties(ax1, blockchain, bit_difficulty_colors[i % len(bit_difficulty_colors)], base,
                              scaling_factor,
                              line_width)

    fig.tight_layout()
    fig.legend(loc=LEGEND_LOCATION, bbox_to_anchor=(FIGURE_BASE, LEGEND_B_BOX_Y), ncol=LEGEND_N_COL,
               fontsize=LEGEND_FONT_SIZE)
    plt.title(PLOT_TITLE_LABEL, fontsize=TITLE_FONT_SIZE, color=PLOT_TITLE_COLOR)
    plt.show()


def plot_mining_times_bar(ax1, blockchain, mining_time_color):
    mining_times = blockchain.mining_times
    marker_size = MARKER_SIZE

    ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=0.5),
            width=BAR_WIDTH)
    ax1.scatter(range(len(mining_times)), mining_times, color='lime', s=marker_size, zorder=3)
    ax1.set_xlabel('Block Index', fontsize=FONT_SIZE)
    ax1.set_ylabel('Mining Time, seconds', fontsize=FONT_SIZE, color=mining_time_color)
    ax1.tick_params(axis='y', labelcolor=mining_time_color)
    ax1.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=mining_time_color)
    ax1.relim()
    ax1.autoscale_view()


def plot_bit_difficulties(ax1, blockchain, difficulty_color, base, scaling_factor, line_width):
    ax2 = ax1.twinx()
    bit_difficulties = [difficulty * scaling_factor for difficulty in blockchain.bit_difficulties]

    ax2.plot(range(len(bit_difficulties)), bit_difficulties, color=difficulty_color, linewidth=line_width,
             label=f'Bit Difficulty (base={base})')

    min_bit_difficulty, max_bit_difficulty = min(bit_difficulties), max(bit_difficulties)
    margin = DEFAULT_MARGIN \
        if min_bit_difficulty == max_bit_difficulty \
        else (max_bit_difficulty - min_bit_difficulty) * MARGIN_COEFFICIENT

    ax2.set_ylim(min_bit_difficulty - margin, max_bit_difficulty + margin)
    ax2.set_ylabel('Bit Difficulty, bits', fontsize=FONT_SIZE, color=difficulty_color)
    ax2.tick_params(axis='y', labelcolor=difficulty_color)
    ax2.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=difficulty_color)
    ax2.relim()
    ax2.autoscale_view()
