#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a constants.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# properties of the execution:
INITIAL_BIT_DIFFICULTY = 16  # bit difficulty of the first block; todo is it better to use linear_difficulty?
# NUMBER_BLOCKS_TO_ADD = 10_000  # how many blocks do we plan to add; property of the current execution
NUMBER_BLOCKS_TO_ADD = 21  # how many blocks do we plan to add; property of the current execution

# properties of the blockchain:
BASE = 2  # base for the blockchain
TARGET_BLOCK_TIME = 0.1  # what is the desirable time to mine a block
# todo why Target block time: 0.10000000000000001 ???
# properties of the difficulty adjustment:
ADJUSTMENT_INTERVAL = 2  # how many blocks to wait before adjusting the difficulty
CLAMP_FACTOR = 2  # max adjustment factor to increase / decrease the difficulty
SMALLEST_BIT_DIFFICULTY = 4  # the smallest bit difficulty that we can adjust to; todo 4 bits; bin: 0b0000, hex: 0x0,

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
FIGURE_HEIGHT_SCALING_FACTOR = 0.9  # scaling factor for the plotting
FIGURE_WIDHT_SCALING_FACTOR = 0.9  # scaling factor for the plotting
PIXEL_TO_INCH_CONVERSION = 100  # conversion factor from pixels to inches
COLOR_LIST_LENGTH = 3  # length of the color list for the plotting
BAR_WIDTH = 0.8  # width of the bars in the bar plot
EPSILON = 1e-9  # epsilon for the floating point comparison
GRID_LINE_WIDTH = 0.5  # width of the grid lines in the plot
LEGEND_B_BOX_Y = -0.1  # y-coordinate of the legend bounding box
LEGEND_N_COL = 3  # number of columns in the legend
LEGEND_FONT_SIZE = 10  # font size of the legend
LEGEND_LOCATION = 'upper center'
PLOT_TITLE_FONT_SIZE = 14  # font size of the title
PLOT_TITLE_COLOR = 'white'
PLOT_TITLE_LABEL = 'Blockchain Mining Statistics'
PLOT_TITLE_Y = 1.0
MARKER_SIZE = 0.5  # size of the markers in the plot

# properties of the project: # todo correct the values
PROJECT_NAME = "Blockchain-PoW-Simulator"
PROJECT_AUTHOR = "Anton Gorshkov"
PROJECT_EMAIL = "antoniooreany@gmail.com"
PROJECT_YEAR = 2024
PROJECT_DESCRIPTION = "This code is for a blockchain and its unit tests."
PROJECT_COPYRIGHT = f"Copyright (c) {PROJECT_YEAR}, {PROJECT_AUTHOR}"
PROJECT_ALL_RIGHTS_RESERVED = "All rights reserved."
PROJECT_CONTACT = f"For any questions or concerns, please contact {PROJECT_AUTHOR} at {PROJECT_EMAIL}"
PROJECT_COPYRIGHT_NOTICE = f"{PROJECT_COPYRIGHT}\n\n{PROJECT_DESCRIPTION}\n{PROJECT_CONTACT}"

# properties of
ENCODING = "utf-8"  # encoding for the strings
GENESIS_BLOCK_HASH = "0"  # genesis block hash
GENESIS_BLOCK_PREVIOUS_HASH = "0"  # genesis block hash
GENESIS_BLOCK_DATA = "Genesis Block"  # genesis block data

# properties of the plotting: general:
SCALING_FACTOR = 1.0  # scaling factor for the plotting
LINE_WIDTH = 1  # width of the lines in the plot
PLOT_BACKGROUND = 'dark_background'  # background color of the plot
BIT_DIFFICULTY_COLORS = 'cyan'  # color of the bit difficulty plot
MINING_TIME_COLORS = 'green'  # color of the mining time plot

# properties of the plotting: axes:
AX1_GRID_BOOL = True
AX1_GRID_WHICH = 'both'
AX1_GRID_LINE_STYLE = ':'
AX1_TICK_PARAMS_AXIS = 'y'
AX1_X_LABEL_TEXT = 'Block Index'
AX1_Y_LABEL_TEXT = 'Mining Time, seconds'
AX1_SCATTER_Z_ORDER = 3
AX1_BAR_ALPHA = 0.5

# properties of the plotting: axes:
AX2_GRID_BOOL = True
AX2_GRID_WHICH = 'both'
AX2_GRID_LINE_STYLE = ':'
AX2_TICK_PARAMS_AXIS = 'y'
AX2_Y_LABEL_TEXT = 'Bit Difficulty, bits'
AX2_PLOT_LABEL = 'Bit Difficulty'

# properties of the plotting: scatter:
MINING_TIMES_SCATTER_COLOR = 'lime'
BIT_DIFFICULTY_SCATTER_COLOR = 'red'

AX2_SCATTER_Z_ORDER = 3

FIGURE_BASE = 0.5
