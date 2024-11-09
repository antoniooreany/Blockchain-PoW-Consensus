#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from .plotting_utils import plot_mining_times, plot_difficulties
from ..constants import (
    PLOT_TITLE_Y, PLOT_TITLE_FONT_SIZE,
    X_LEGEND_POSITION, Y_LEGEND_POSITION, LEGEND_LOCATION, LEGEND_FONT_SIZE, INITIAL_BIT_DIFFICULTY_KEY,
    TARGET_BLOCK_MINING_TIME_KEY, ADJUSTMENT_BLOCK_INTERVAL_KEY, CLAMP_FACTOR_KEY,
    SMALLEST_BIT_DIFFICULTY_KEY, NUMBER_BLOCKS_TO_ADD_KEY, NUMBER_BLOCKS_SLICE_KEY, FIGSIZE, LEGEND_TITLE, PLOT_TITLE_LABEL
)


def plot_blockchain_statistics(blockchain):
    """
    Plot mining times and bit difficulties for the blockchain statistics.
    """
    fig, ax1 = plt.subplots(figsize=FIGSIZE)

    plot_mining_times(ax1, blockchain)
    plot_difficulties(ax1, blockchain)

    legend_info = (
        f"{INITIAL_BIT_DIFFICULTY_KEY}: {blockchain.initial_bit_difficulty}\n"  # todo init once, generalize in the loop
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
               fontsize=LEGEND_FONT_SIZE, title=LEGEND_TITLE, title_fontsize=LEGEND_FONT_SIZE)

    plt.title(PLOT_TITLE_LABEL, fontsize=PLOT_TITLE_FONT_SIZE, y=PLOT_TITLE_Y)
    plt.show()
