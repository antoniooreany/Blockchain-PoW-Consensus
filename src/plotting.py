# # #   Copyright (c) 2024, Anton Gorshkov
# # #   All rights reserved.
# # #   This code is for a plotting and its unit tests.
# # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# #
# #
# # import matplotlib.colors as mcolors
# # import matplotlib.pyplot as plt
# # import numpy as np
# # from matplotlib.axes import Axes
# # from screeninfo import get_monitors
# #
# # from constants import (
# #     SCALING_FACTOR,
# #     LINE_WIDTH,
# #     PLOT_BACKGROUND,
# #     MINING_TIME_COLOR,
# #     BIT_DIFFICULTY_COLOR,
# #     FONT_SIZE,
# #     MARGIN_COEFFICIENT,
# #     FIGURE_HEIGHT_SCALING_FACTOR,
# #     PIXEL_TO_INCH_CONVERSION,
# #     COLOR_LIST_LENGTH,
# #     BAR_WIDTH,
# #     EPSILON,
# #     GRID_LINE_WIDTH,
# #     LEGEND_B_BOX_Y,
# #     LEGEND_N_COL,
# #     LEGEND_FONT_SIZE,
# #     PLOT_TITLE_FONT_SIZE,
# #     MARKER_SIZE,
# #
# #     AX1_GRID_LINE_STYLE,
# #     AX1_GRID_BOOL,
# #     AX1_GRID_WHICH,
# #     AX1_TICK_PARAMS_AXIS,
# #     AX1_Y_LABEL_TEXT,
# #     AX1_X_LABEL_TEXT,
# #     AX1_SCATTER_Z_ORDER,
# #     AX1_BAR_ALPHA,
# #
# #     AX2_GRID_WHICH,
# #     AX2_GRID_BOOL,
# #     AX2_TICK_PARAMS_AXIS,
# #     AX2_Y_LABEL_TEXT,
# #     AX2_PLOT_LABEL,
# #     AX2_GRID_LINE_STYLE,
# #
# #     MINING_TIMES_SCATTER_COLOR,
# #     PLOT_TITLE_COLOR,
# #     PLOT_TITLE_LABEL,
# #     LEGEND_LOCATION,
# #     FIGURE_BASE,
# #     FIGURE_WIDTH_SCALING_FACTOR,
# #     PLOT_TITLE_Y,
# #     BIT_DIFFICULTY_SCATTER_COLOR,
# #     AX2_SCATTER_Z_ORDER,
# #     INFINITY_0_DIFFICULTY_LABEL,
# #     TARGET_BLOCK_MINING_TIME,
# #     ADJUSTMENT_BLOCK_INTERVAL,
# #     CLAMP_FACTOR,
# #     SLICE_FACTOR,
# #     X_LEGEND_POSITION,
# #     Y_LEGEND_POSITION, INITIAL_BIT_DIFFICULTY, SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD,
# # )
# # from src.blockchain import Blockchain
# #
# #
# # def plot_blockchain_statistics(
# #         blockchain: Blockchain,
# #         scaling_factor: float = SCALING_FACTOR,
# #         # An optional parameter to scale the y-axis for the bit difficulties
# #         line_width: int = LINE_WIDTH,  # The width of the line to plot # todo remove from default
# # ) -> None:
# #     if not blockchain:
# #         raise ValueError("No blockchain provided")
# #
# #     monitor = get_monitors()[0]
# #     if not monitor:
# #         raise RuntimeError("No monitor found")
# #
# #     (
# #         fig_width,
# #         fig_height
# #     ) = (
# #         monitor.width * FIGURE_WIDTH_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION,
# #         monitor.height * FIGURE_HEIGHT_SCALING_FACTOR / PIXEL_TO_INCH_CONVERSION,
# #     )
# #
# #     plt.style.use(PLOT_BACKGROUND)
# #     ax1: Axes
# #     fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
# #
# #     all_bit_difficulties = blockchain.bit_difficulties
# #
# #     min_bit_difficulty, max_bit_difficulty = (
# #         min(all_bit_difficulties) * scaling_factor,
# #         max(all_bit_difficulties) * scaling_factor
# #     )
# #     if min_bit_difficulty == max_bit_difficulty:
# #         max_bit_difficulty += EPSILON
# #
# #     plot_mining_times_bar(
# #         ax1,
# #         blockchain,
# #         MINING_TIME_COLOR,
# #     )
# #     plot_bit_difficulties(
# #         ax1,
# #         blockchain,
# #         BIT_DIFFICULTY_COLOR,
# #         scaling_factor,
# #         line_width,
# #     )  # todo Type 'Axes' doesn't have expected attributes 'set_ylim', 'set_ylabel', 'tick_params', 'grid', 'relim', 'autoscale_view'
# #
# #     legend_input_info: str = (
# #         f"Initial Bit Difficulty, bits: {blockchain.initial_bit_difficulty} \n"
# #         f"Target Block Mining Time, seconds: {blockchain.target_block_mining_time} \n"
# #         f"Adjustment Block Interval, blocks: {blockchain.adjustment_block_interval} \n"
# #         f"Number of Blocks to Add, blocks: {blockchain.number_blocks_to_add} \n"
# #         f"Clamp Factor, bits: {blockchain.clamp_factor} \n"
# #         f"Smallest Bit Difficulty, bits: {blockchain.smallest_bit_difficulty} \n"
# #         # f"Slice Factor, 1: {blockchain.slice_factor} \n"
# #         f"Number of Blocks Slice, blocks: {blockchain.number_blocks_slice} \n"
# #     )
# #
# #     fig.tight_layout()
# #     fig.legend(
# #         loc=LEGEND_LOCATION,
# #         bbox_to_anchor=(
# #             FIGURE_BASE,
# #             LEGEND_B_BOX_Y
# #         ),
# #         ncol=LEGEND_N_COL,
# #         fontsize=LEGEND_FONT_SIZE,
# #         title="Input Information",
# #         title_fontsize=LEGEND_FONT_SIZE,
# #     )
# #
# #     plt.figtext(
# #         x=X_LEGEND_POSITION,
# #         y=Y_LEGEND_POSITION,
# #         s=legend_input_info,
# #         wrap=True,
# #         # horizontalalignment='center',
# #         horizontalalignment='right',
# #         verticalalignment='top',
# #         fontsize=LEGEND_FONT_SIZE,
# #     )
# #
# #     plt.title(
# #         PLOT_TITLE_LABEL,
# #         fontsize=PLOT_TITLE_FONT_SIZE,
# #         color=PLOT_TITLE_COLOR,
# #         y=PLOT_TITLE_Y,
# #     )
# #     plt.show()
# #
# #
# # #
# # #
# # # def plot_mining_times_bar(ax1, blockchain, mining_time_color):
# # #     mining_times = blockchain.mining_times  # Include the Genesis Block for plotting
# # #     adjustment_interval = blockchain.adjustment_block_interval
# # #
# # #     ax1.bar(range(len(mining_times)), mining_times, color=mcolors.to_rgba(mining_time_color, alpha=AX1_BAR_ALPHA),
# # #             width=BAR_WIDTH)
# # #     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE,
# # #                 zorder=AX1_SCATTER_Z_ORDER)
# # #
# # #     for i in range(1, len(mining_times), adjustment_interval):
# # #         interval_times = mining_times[i:i + adjustment_interval]
# # #         avg_time = sum(interval_times) / len(interval_times)
# # #         ax1.bar(i + adjustment_interval / 2, avg_time, color='lightgreen', alpha=0.5, width=adjustment_interval,
# # #                 align='center')
# # #
# # #     ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
# # #     ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
# # #     ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
# # #     ax1.grid(AX1_GRID_BOOL, which=AX1_GRID_WHICH, linestyle=AX1_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH,
# # #              color=mining_time_color)
# # #     ax1.relim()
# # #     ax1.autoscale_view()
# # #     ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
# # #
# # #
# # # def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
# # #     ax2 = ax1.twinx()
# # #     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
# # #
# # #     # Set the difficulty of the Genesis Block to 0
# # #     difficulties[0] = 0
# # #
# # #     thicker_line_width = line_width * 5
# # #     thinner_line_width = line_width
# # #
# # #     for i in range(1, len(difficulties)):
# # #         ax2.plot([i - 1.5, i - 0.5], [difficulties[i - 1], difficulties[i - 1]], color=difficulty_color,
# # #                  linewidth=thicker_line_width)
# # #         ax2.plot([i - 0.5, i - 0.5], [difficulties[i - 1], difficulties[i]], color=difficulty_color,
# # #                  linewidth=thinner_line_width)
# # #
# # #     ax2.scatter([x - 0.5 for x in range(len(difficulties))], difficulties, color='red', marker='o', s=MARKER_SIZE,
# # #                 zorder=AX2_SCATTER_Z_ORDER)
# # #
# # #     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
# # #     ax2.tick_params(axis='y', labelcolor=difficulty_color)
# # #     ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH,
# # #              color=difficulty_color)
# # #     ax2.relim()
# # #     ax2.autoscale_view()
# # #     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
# # #
# # #     # Format y-axis to start from 00_000
# # #     ax2.yaxis.set_major_formatter(
# # #         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else '00_000'))
# #
# #
# # import matplotlib.pyplot as plt
# # import matplotlib.colors as mcolors
# #
# # def plot_mining_times_bar(ax1, blockchain, mining_time_color):
# #     mining_times = blockchain.mining_times  # Include the Genesis Block for plotting
# #     adjustment_interval = blockchain.adjustment_block_interval
# #
# #     for i in range(len(mining_times)):
# #         ax1.plot([i, i], [0, mining_times[i]], color=mining_time_color, linewidth=LINE_WIDTH)
# #
# #     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=AX1_SCATTER_Z_ORDER)
# #
# #     ax1.set_xlabel(AX1_X_LABEL_TEXT, fontsize=FONT_SIZE)
# #     ax1.set_ylabel(AX1_Y_LABEL_TEXT, fontsize=FONT_SIZE, color=mining_time_color)
# #     ax1.tick_params(axis=AX1_TICK_PARAMS_AXIS, labelcolor=mining_time_color)
# #     ax1.grid(AX1_GRID_BOOL, which=AX1_GRID_WHICH, linestyle=AX1_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=mining_time_color)
# #     ax1.relim()
# #     ax1.autoscale_view()
# #     ax1.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
# #
# # def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor, line_width):
# #     ax2 = ax1.twinx()
# #     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
# #
# #     # Set the difficulty of the Genesis Block to 0
# #     difficulties[0] = 0
# #
# #     ax2.bar(range(len(difficulties)), difficulties, color=difficulty_color, width=BAR_WIDTH)
# #
# #     ax2.set_ylabel("Difficulty / Bit Difficulty", fontsize=FONT_SIZE, color=difficulty_color)
# #     ax2.tick_params(axis='y', labelcolor=difficulty_color)
# #     ax2.grid(AX2_GRID_BOOL, which=AX2_GRID_WHICH, linestyle=AX2_GRID_LINE_STYLE, linewidth=GRID_LINE_WIDTH, color=difficulty_color)
# #     ax2.relim()
# #     ax2.autoscale_view()
# #     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
# #
# #     # Format y-axis to start from 00_000
# #     ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else '00_000'))
# #
# #
#
#
# # plotting.py
#
# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.colors as mcolors
# from constants import (
#     MINING_TIME_COLOR, DIFFICULTY_COLOR, LINE_WIDTH, GRID_LINE_WIDTH,
#     FONT_SIZE, MARKER_SIZE, BAR_WIDTH, PLOT_TITLE_Y, PLOT_TITLE_FONT_SIZE,
#     X_LEGEND_POSITION, Y_LEGEND_POSITION, LEGEND_LOCATION, LEGEND_FONT_SIZE, MINING_TIMES_SCATTER_COLOR
# )
#
#
# # def plot_mining_times_bar(ax1, blockchain):
# #     mining_times = blockchain.mining_times
# #
# #     # Plot each mining time as a bar and scatter
# #     for i in range(len(mining_times)):
# #         ax1.plot([i, i], [0, mining_times[i]], color=MINING_TIME_COLOR, linewidth=LINE_WIDTH)
# #     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=3)
# #
# #     ax1.set_xlabel('Block Index', fontsize=FONT_SIZE)
# #     ax1.set_ylabel('Block Mining Time (seconds)', fontsize=FONT_SIZE, color=MINING_TIME_COLOR)
# #     ax1.tick_params(axis='y', labelcolor=MINING_TIME_COLOR)
# #     ax1.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=MINING_TIME_COLOR)
# #     ax1.relim()
# #     ax1.autoscale_view()
# #     ax1.set_xlim(left=-0.5)
#
#
#
#
#
# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.colors as mcolors
# from constants import (
#     MINING_TIME_COLOR, DIFFICULTY_COLOR, LINE_WIDTH, GRID_LINE_WIDTH,
#     FONT_SIZE, MARKER_SIZE, BAR_WIDTH, PLOT_TITLE_Y, PLOT_TITLE_FONT_SIZE,
#     X_LEGEND_POSITION, Y_LEGEND_POSITION, LEGEND_LOCATION, LEGEND_FONT_SIZE, MINING_TIMES_SCATTER_COLOR
# )
#
# def plot_mining_times_bar(ax1, blockchain):
#     mining_times = blockchain.mining_times
#
#     # Plot each mining time as a bar and scatter
#     for i in range(len(mining_times)):
#         ax1.plot([i, i], [0, mining_times[i]], color=MINING_TIME_COLOR, linewidth=LINE_WIDTH)
#     ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=3)
#
#     ax1.set_xlabel('Block Index', fontsize=FONT_SIZE)
#     ax1.set_ylabel('Block Mining Time (seconds)', fontsize=FONT_SIZE, color=MINING_TIME_COLOR)
#     ax1.tick_params(axis='y', labelcolor=MINING_TIME_COLOR)
#     ax1.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=MINING_TIME_COLOR)
#     ax1.relim()
#     ax1.autoscale_view()
#     ax1.set_xlim(left=-0.5)
#     ax1.set_ylim(bottom=0)  # Ensure the y-axis starts from 0
#
#
#
#
# # def plot_bit_difficulties(ax1, blockchain, scaling_factor):
# #     ax2 = ax1.twinx()
# #     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
# #     difficulties[0] = 0  # Set Genesis Block difficulty to 0 for clarity
# #
# #     # Bar plot for difficulties
# #     ax2.bar(range(len(difficulties)), difficulties, color=DIFFICULTY_COLOR, width=BAR_WIDTH)
# #
# #     ax2.set_ylabel('Difficulty / Bit Difficulty', fontsize=FONT_SIZE, color=DIFFICULTY_COLOR)
# #     ax2.tick_params(axis='y', labelcolor=DIFFICULTY_COLOR)
# #     ax2.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=DIFFICULTY_COLOR)
# #     ax2.relim()
# #     ax2.autoscale_view()
# #     ax2.set_xlim(left=-0.5)
# #     ax2.yaxis.set_major_formatter(
# #         plt.FuncFormatter(lambda x, _: f'{float(np.log2(x)):.2f} / {x:_.0f}' if x > 0 else '00_000')
# #     )
#
#
# # plotting.py
#
# import matplotlib.pyplot as plt
# import numpy as np
#
# def plot_bit_difficulties(ax1, blockchain, difficulty_color, scaling_factor):
#     ax2 = ax1.twinx()
#     difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
#
#     # Set the difficulty of the Genesis Block to 0
#     difficulties[0] = 0
#
#     # Create bar plot for bit difficulties
#     ax2.bar(range(len(difficulties)), difficulties, color=difficulty_color, width=BAR_WIDTH)
#
#     ax2.set_ylabel('Difficulty / Bit Difficulty', fontsize=FONT_SIZE, color=difficulty_color)
#     ax2.tick_params(axis='y', labelcolor=difficulty_color)
#     ax2.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color=difficulty_color)
#     ax2.relim()
#     ax2.autoscale_view()
#     ax2.set_xlim(left=-0.5)  # Ensure the x-axis starts from 0
#
#     # Ensure that 0 is labeled as "00_000"
#     def custom_y_formatter(x, _):
#         if x == 0:
#             return "00_000"
#         else:
#             return f'{float(np.log2(x)):.2f} / {x:_.0f}'
#
#     ax2.yaxis.set_major_formatter(plt.FuncFormatter(custom_y_formatter))
#
#
#
#
# # def plot_blockchain_statistics(blockchain, scaling_factor=1.0):
# #     fig, ax1 = plt.subplots(figsize=(12, 8))
# #
# #     # Plotting mining times and difficulties with updated functions
# #     plot_mining_times_bar(ax1, blockchain)
# #     plot_bit_difficulties(ax1, blockchain, scaling_factor)
# #
# #     # Legend adjustments
# #     legend_info = (
# #         f"Initial Bit Difficulty: {blockchain.initial_bit_difficulty}\n"
# #         f"Target Block Mining Time: {blockchain.target_block_mining_time}\n"
# #         f"Adjustment Interval: {blockchain.adjustment_block_interval}\n"
# #         f"Blocks to Add: {blockchain.number_blocks_to_add}\n"
# #         f"Clamp Factor: {blockchain.clamp_factor}\n"
# #         f"Min Bit Difficulty: {blockchain.smallest_bit_difficulty}\n"
# #         f"Blocks Slice: {blockchain.number_blocks_slice}\n"
# #     )
# #     fig.legend(loc=LEGEND_LOCATION, bbox_to_anchor=(X_LEGEND_POSITION, Y_LEGEND_POSITION),
# #                fontsize=LEGEND_FONT_SIZE, title="Input Information", title_fontsize=LEGEND_FONT_SIZE)
# #
# #     # Title with adjusted position
# #     plt.title('Blockchain Mining Statistics', fontsize=PLOT_TITLE_FONT_SIZE, y=PLOT_TITLE_Y)
# #     plt.show()
#
#
# def plot_blockchain_statistics(blockchain, scaling_factor=1.0):
#     fig, ax1 = plt.subplots(figsize=(12, 8))
#
#     # Plot mining times and bit difficulties with updated functions
#     plot_mining_times_bar(ax1, blockchain)
#     plot_bit_difficulties(ax1, blockchain, DIFFICULTY_COLOR,
#                           scaling_factor)  # Corrected function call with DIFFICULTY_COLOR and scaling_factor
#
#     # Legend adjustments
#     legend_info = (
#         f"Initial Bit Difficulty: {blockchain.initial_bit_difficulty}\n"
#         f"Target Block Mining Time: {blockchain.target_block_mining_time}\n"
#         f"Adjustment Interval: {blockchain.adjustment_block_interval}\n"
#         f"Blocks to Add: {blockchain.number_blocks_to_add}\n"
#         f"Clamp Factor: {blockchain.clamp_factor}\n"
#         f"Min Bit Difficulty: {blockchain.smallest_bit_difficulty}\n"
#         f"Blocks Slice: {blockchain.number_blocks_slice}\n"
#     )
#     fig.legend(loc=LEGEND_LOCATION, bbox_to_anchor=(X_LEGEND_POSITION, Y_LEGEND_POSITION),
#                fontsize=LEGEND_FONT_SIZE, title="Input Information", title_fontsize=LEGEND_FONT_SIZE)
#
#     # Title with adjusted position
#     plt.title('Blockchain Mining Statistics', fontsize=PLOT_TITLE_FONT_SIZE, y=PLOT_TITLE_Y)
#     plt.show()
#
#




import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from constants import (
    FONT_SIZE, LINE_WIDTH, GRID_LINE_WIDTH, MARKER_SIZE, BAR_WIDTH,
    LEGEND_LOCATION, LEGEND_FONT_SIZE, PLOT_TITLE_FONT_SIZE, PLOT_TITLE_Y,
    X_LEGEND_POSITION, Y_LEGEND_POSITION, MINING_TIMES_SCATTER_COLOR
)

def plot_mining_times_bar(ax1, blockchain):
    mining_times = blockchain.mining_times
    cmap = plt.get_cmap('Blues')
    colors = [cmap(i / len(mining_times)) for i in range(len(mining_times))]

    for i in range(len(mining_times)):
        ax1.plot([i, i], [0, mining_times[i]], color=colors[i], linewidth=LINE_WIDTH)
    ax1.scatter(range(len(mining_times)), mining_times, color=MINING_TIMES_SCATTER_COLOR, s=MARKER_SIZE, zorder=3)

    ax1.set_xlabel('Block Index', fontsize=FONT_SIZE)
    ax1.set_ylabel('Block Mining Time (seconds)', fontsize=FONT_SIZE, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color='blue')
    ax1.relim()
    ax1.autoscale_view()
    ax1.set_xlim(left=-0.5)
    ax1.set_ylim(bottom=0)

def plot_bit_difficulties(ax1, blockchain, scaling_factor):
    ax2 = ax1.twinx()
    difficulties = [(2 ** bit_difficulty) * scaling_factor for bit_difficulty in blockchain.bit_difficulties]
    difficulties[0] = 0
    cmap = plt.get_cmap('Blues')
    colors = [cmap(i / len(difficulties)) for i in range(len(difficulties))]

    ax2.bar(range(len(difficulties)), difficulties, color=colors, width=BAR_WIDTH)

    ax2.set_ylabel('Difficulty / Bit Difficulty', fontsize=FONT_SIZE, color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.grid(True, which='both', linestyle=':', linewidth=GRID_LINE_WIDTH, color='blue')
    ax2.relim()
    ax2.autoscale_view()
    ax2.set_xlim(left=-0.5)

    def custom_y_formatter(x, _):
        if x == 0:
            return "00_000"
        else:
            return f'{float(np.log2(x)):.2f} / {x:_.0f}'

    ax2.yaxis.set_major_formatter(plt.FuncFormatter(custom_y_formatter))

def plot_blockchain_statistics(blockchain, scaling_factor=1.0):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    plot_mining_times_bar(ax1, blockchain)
    plot_bit_difficulties(ax1, blockchain, scaling_factor)

    legend_info = (
        f"Initial Bit Difficulty: {blockchain.initial_bit_difficulty}\n"
        f"Target Block Mining Time: {blockchain.target_block_mining_time}\n"
        f"Adjustment Interval: {blockchain.adjustment_block_interval}\n"
        f"Blocks to Add: {blockchain.number_blocks_to_add}\n"
        f"Clamp Factor: {blockchain.clamp_factor}\n"
        f"Min Bit Difficulty: {blockchain.smallest_bit_difficulty}\n"
        f"Blocks Slice: {blockchain.number_blocks_slice}\n"
    )
    fig.legend(loc=LEGEND_LOCATION, bbox_to_anchor=(X_LEGEND_POSITION, Y_LEGEND_POSITION),
               fontsize=LEGEND_FONT_SIZE, title="Input Information", title_fontsize=LEGEND_FONT_SIZE)

    plt.title('Blockchain Mining Statistics', fontsize=PLOT_TITLE_FONT_SIZE, y=PLOT_TITLE_Y)
    plt.show()

