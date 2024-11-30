#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a plotting and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# path: src/view/plotting.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from src.view.plot_difficulties import plot_difficulties
from src.view.plot_mining_times import plot_mining_times
from src.constants import (
    PLOT_TITLE_Y, PLOT_TITLE_FONT_SIZE,
    X_LEGEND_POSITION, Y_LEGEND_POSITION, LEGEND_LOCATION, LEGEND_FONT_SIZE, INITIAL_BIT_DIFFICULTY_KEY,
    TARGET_BLOCK_MINING_TIME_KEY, ADJUSTMENT_BLOCK_INTERVAL_KEY, CLAMP_FACTOR_KEY,
    SMALLEST_BIT_DIFFICULTY_KEY, NUMBER_BLOCKS_TO_ADD_KEY, NUMBER_BLOCKS_SLICE_KEY, FIGSIZE, LEGEND_TITLE,
    PLOT_TITLE_LABEL
)


from src.model.blockchain import Blockchain


def plot_blockchain_statistics(blockchain: Blockchain) -> None:
    """
    Plot mining times and bit difficulties for the blockchain statistics.

    This function first plots mining times and then plots bit difficulties for the blockchain statistics.

    Args:
        blockchain (Blockchain): The blockchain to plot statistics for.
    """
    fig, ax1 = plt.subplots(figsize=FIGSIZE)

    # Plot mining times and target mining time
    plot_mining_times(ax1, blockchain)

    # Plot bit difficulties
    plot_difficulties(ax1, blockchain)

    # Construct the legend information
    legend_info = (
        f"{INITIAL_BIT_DIFFICULTY_KEY}: {blockchain.initial_bit_difficulty}\n"
        f"{TARGET_BLOCK_MINING_TIME_KEY}: {blockchain.target_block_mining_time}\n"
        f"{ADJUSTMENT_BLOCK_INTERVAL_KEY}: {blockchain.adjustment_block_interval}\n"
        f"{CLAMP_FACTOR_KEY}: {blockchain.clamp_factor}\n"
        f"{SMALLEST_BIT_DIFFICULTY_KEY}: {blockchain.smallest_bit_difficulty}\n"
        f"{NUMBER_BLOCKS_TO_ADD_KEY}: {blockchain.number_blocks_to_add}\n"
        f"{NUMBER_BLOCKS_SLICE_KEY}: {blockchain.number_blocks_slice}\n"
    )

    # Create a legend patch
    legend_patch = mpatches.Patch(color='none', label=legend_info)

    # Plot the legend
    fig.legend(handles=[legend_patch], loc=LEGEND_LOCATION, bbox_to_anchor=(X_LEGEND_POSITION, Y_LEGEND_POSITION),
               fontsize=LEGEND_FONT_SIZE, title=LEGEND_TITLE, title_fontsize=LEGEND_FONT_SIZE)

    # Set the plot title
    plt.title(PLOT_TITLE_LABEL, fontsize=PLOT_TITLE_FONT_SIZE, y=PLOT_TITLE_Y)
    plt.show()
