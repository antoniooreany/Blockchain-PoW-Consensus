#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a constants.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


# properties of the current execution:
INITIAL_BIT_DIFFICULTY = 16  # bit difficulty of the first block; todo is it better to use linear_difficulty?
NUMBER_BLOCKS_TO_ADD = 1_000  # how many blocks do we plan to add; property of the current execution

# properties of blockchain:
TARGET_BLOCK_TIME = 0.01  # what is the desirable time to mine a block

# properties of the difficulty adjustment:
ADJUSTMENT_INTERVAL = 10  # how many blocks to wait before adjusting the difficulty
CLAMP_FACTOR = 2  # max adjustment factor to increase / decrease the difficulty
SMALLEST_BIT_DIFFICULTY = 4  # todo 4 bits; bin: 0b0000, hex: 0x0, dec: 0: smallest bit difficulty

# properties of the proof of work:
HASH_BIT_LENGTH = 256  # The length of the hash in bits
NONCE_BIT_LENGTH = 32  # The length of the nonce in bits

# properties of statistics:
STATISTICS_PARTITION_INTERVAL_FACTOR = 2  # which last part of the blockchain to consider for the statistics

# properties of the plotting: bit_difficulties:
MARGIN_COEFFICIENT = 0.05  # margin coefficient for the plotting of bit_difficulties
DEFAULT_MARGIN = 0.1  # margin for the plotting of bit_difficulties when min_bit_difficulty == max_bit_difficulty

# properties of the plotting: general:
FONT_SIZE = 12  # font size for the plotting: axes label titles
FIGURE_SCALING_FACTOR = 0.9  # scaling factor for the plotting
PIXEL_TO_INCH_CONVERSION = 100  # conversion factor from pixels to inches
COLOR_LIST_LENGTH = 3  # length of the color list for the plotting
BAR_WIDTH = 0.8  # width of the bars in the bar plot
EPSILON = 1e-9  # epsilon for the floating point comparison
GRID_LINE_WIDTH = 0.5  # width of the grid lines in the plot
LEGEND_B_BOX_Y = -0.1  # y-coordinate of the legend bounding box
LEGEND_N_COL = 3  # number of columns in the legend
LEGEND_FONT_SIZE = 10  # font size of the legend
TITLE_FONT_SIZE = 14  # font size of the title
MARKER_SIZE = 0.5  # size of the markers in the plot
