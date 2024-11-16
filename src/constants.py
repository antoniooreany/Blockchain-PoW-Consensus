#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a constants.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

# properties of the execution:
INITIAL_BIT_DIFFICULTY = 16.0  # bit difficulty of the first block; todo is it better to use linear_difficulty?


# properties of the blockchain:
BASE = 2  # base for the blockchain
TARGET_BLOCK_MINING_TIME = 0.01  # what is the desirable time to mine a block
# todo why Target block time: 0.10000000000000001 ???
# properties of the difficulty adjustment:
# ADJUSTMENT_BLOCK_INTERVAL = 1  # how many blocks to wait before adjusting the difficulty
ADJUSTMENT_BLOCK_INTERVAL = 2  # how many blocks to wait before adjusting the difficulty
# ADJUSTMENT_BLOCK_INTERVAL = 3  # how many blocks to wait before adjusting the difficulty
# ADJUSTMENT_BLOCK_INTERVAL = 5  # how many blocks to wait before adjusting the difficulty
# ADJUSTMENT_BLOCK_INTERVAL = 10  # how many blocks to wait before adjusting the difficulty
# ADJUSTMENT_BLOCK_INTERVAL = 1000  # todo for static constant difficulty
CLAMP_FACTOR = 2.0  # max adjustment factor to increase / decrease the difficulty
SMALLEST_BIT_DIFFICULTY = 4.0  # the smallest bit difficulty that we can adjust to; todo 4 bits; bin: 0b0000, hex: 0x0,

# properties of the execution:
# NUMBER_BLOCKS_TO_ADD = 3  # how many blocks do we plan to add; property of the current execution
# NUMBER_BLOCKS_TO_ADD = 5  # how many blocks do we plan to add; property of the current execution
# NUMBER_BLOCKS_TO_ADD = 10  # how many blocks do we plan to add; property of the current execution
# NUMBER_BLOCKS_TO_ADD = 20  # how many blocks do we plan to add; property of the current execution
NUMBER_BLOCKS_TO_ADD = 100  # how many blocks do we plan to add; property of the current execution
# NUMBER_BLOCKS_TO_ADD = 1_000  # how many blocks do we plan to add; property of the current execution
# NUMBER_BLOCKS_TO_ADD = 10_000  # how many blocks do we plan to add; property of the current execution
# NUMBER_BLOCKS_TO_ADD = 100_000  # how many blocks do we plan to add; property of the current execution

# properties of statistics:
# SLICE_FACTOR = 2.0  # which last part of the blockchain to consider for the statistics
# SLICE_FACTOR = 2.3  # which last part of the blockchain to consider for the statistics
# SLICE_FACTOR = 2.5  # which last part of the blockchain to consider for the statistics

# NUMBER_BLOCKS_SLICE = 2  # todo how was rounded in logging_utils.py? how many blocks to consider for the statistics
NUMBER_BLOCKS_SLICE = 50  # todo how was rounded in logging_utils.py? how many blocks to consider for the statistics
# NUMBER_BLOCKS_SLICE = round(NUMBER_BLOCKS_TO_ADD / SLICE_FACTOR)  # todo how was rounded in logging_utils.py? how many blocks to consider for the statistics

# properties of the proof of work:
HASH_BIT_LENGTH = 256  # The length of the hash in bits
NONCE_BIT_LENGTH = 32  # The length of the nonce in bits

# properties of the plotting: bit_difficulties:
MARGIN_COEFFICIENT = 0.05  # margin coefficient for the plotting of bit_difficulties
DEFAULT_MARGIN = 0.1  # margin for the plotting of bit_difficulties when min_bit_difficulty == max_bit_difficulty

# properties for the statistics naming:
INITIAL_BIT_DIFFICULTY_KEY = "initial_bit_difficulty"
NUMBER_BLOCKS_TO_ADD_KEY = "number_blocks_to_add"
SLICE_FACTOR_KEY = "slice_factor"
NUMBER_BLOCKS_SLICE_KEY = "number_blocks_slice"
TARGET_BLOCK_MINING_TIME_KEY = "target_block_mining_time"
ADJUSTMENT_BLOCK_INTERVAL_KEY = "adjustment_block_interval"
CLAMP_FACTOR_KEY = "clamp_factor"
SMALLEST_BIT_DIFFICULTY_KEY = "smallest_bit_difficulty"

# properties for the statistics naming:
# mining time:
AVERAGE_MINING_TIME_SLICE_KEY = "average_mining_time_slice"
ABSOLUTE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY = "absolute_deviation_mining_time_average_from_target_slice"
RELATIVE_DEVIATION_MINING_TIME_AVERAGE_FROM_TARGET_SLICE_KEY = "relative_deviation_mining_time_average_from_target_slice"

VARIANCE_MINING_TIME_SLICE_KEY = "variance_mining_time_slice"
STANDARD_DEVIATION_MINING_TIME_SLICE_KEY = "standard_deviation_mining_time_slice"

# bit difficulty:
AVERAGE_BIT_DIFFICULTY_SLICE_KEY = "average_bit_difficulty_slice"
ABSOLUTE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY = "absolute_deviation_bit_difficulty_average_from_initial_slice"
RELATIVE_DEVIATION_BIT_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY = "relative_deviation_bit_difficulty_average_from_initial_slice"

VARIANCE_BIT_DIFFICULTY_SLICE_KEY = "variance_bit_difficulty_slice"
STANDARD_DEVIATION_BIT_DIFFICULTY_SLICE_KEY = "standard_deviation_bit_difficulty_slice"

# mining time and bit difficulty:
COVARIANCE_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY = "covariance_mining_time_bit_difficulty_slice"
CORRELATION_MINING_TIME_BIT_DIFFICULTY_SLICE_KEY = "correlation_mining_time_bit_difficulty_slice"



# difficulty:
AVERAGE_DIFFICULTY_SLICE_KEY = "average_difficulty_slice"
ABSOLUTE_DEVIATION_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY = "absolute_deviation_difficulty_average_from_initial_slice"
RELATIVE_DEVIATION_DIFFICULTY_AVERAGE_FROM_INITIAL_SLICE_KEY = "relative_deviation_difficulty_average_from_initial_slice"

VARIANCE_DIFFICULTY_SLICE_KEY = "variance_difficulty_slice"
STANDARD_DEVIATION_DIFFICULTY_SLICE_KEY = "standard_deviation_difficulty_slice"

# mining time and difficulty:
COVARIANCE_MINING_TIME_DIFFICULTY_SLICE_KEY = "covariance_mining_time_difficulty_slice"
CORRELATION_MINING_TIME_DIFFICULTY_SLICE_KEY = "correlation_mining_time_difficulty_slice"



# zero mining time:
ZERO_MINING_TIME_BLOCKS_NUMBER_KEY = "zero_mining_time_blocks_number"
RELATIVE_ZERO_MINING_TIME_BLOCKS_NUMBER_KEY = "relative_zero_mining_time_blocks_number"



# properties of the plotting: general:
FONT_SIZE = 16  # font size for the plotting: axes label titles
FIGURE_HEIGHT_SCALING_FACTOR = 0.9  # scaling factor for the plotting
FIGURE_WIDTH_SCALING_FACTOR = 0.9  # scaling factor for the plotting
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
# PLOT_TITLE_LABEL = 'Blockchain Mining Statistics'
PLOT_TITLE_LABEL = ''
PLOT_TITLE_Y = 1.0
# MARKER_SIZE = 0.5  # size of the markers in the plot
MARKER_SIZE = 20  # size of the markers in the plot
X_LEGEND_POSITION = 0.90  # x-coordinate of the legend position
Y_LEGEND_POSITION = 0.96  # y-coordinate of the legend position

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

# PLOT_BACKGROUND = 'dark_background'  # background color of the plot
PLOT_BACKGROUND = 'default'  # background color of the plot

# BIT_DIFFICULTY_COLORS = 'cyan'  # color of the bit difficulty plot
# BIT_DIFFICULTY_COLOR = 'blue'  # color of the bit difficulty plot
# Light blue: #ADD8E6
# BIT_DIFFICULTY_COLOR = '#ADD8E6'  # color of the bit difficulty plot

BIT_DIFFICULTY_COLOR = (173/255, 216/255, 230/255, 0.5)  # Light blue with 50% transparency

# MINING_TIME_COLOR = 'green'  # color of the mining time plot
MINING_TIME_COLOR = 'red'  # color of the mining time plot

# properties of the plotting: axes:
AX1_GRID_BOOL = True
AX1_GRID_WHICH = 'both'
AX1_GRID_LINE_STYLE = ':'
AX1_TICK_PARAMS_AXIS = 'y'
AX1_X_LABEL_TEXT = 'Block Index, 1'
AX1_Y_LABEL_TEXT = 'Block Mining Time, seconds'
AX1_SCATTER_Z_ORDER = 3
AX1_BAR_ALPHA = 0.5

# properties of the plotting: axes:
AX2_GRID_BOOL = True
AX2_GRID_WHICH = 'both'
AX2_GRID_LINE_STYLE = ':'
AX2_TICK_PARAMS_AXIS = 'y'
AX2_Y_LABEL_TEXT = 'Bit Difficulty, bits     /     Difficulty, 1'
AX2_PLOT_LABEL = 'Bit Difficulty'
# INFINITY_0_DIFFICULTY_LABEL = " -INFINITY  /  00_000"
# INFINITY_0_DIFFICULTY_LABEL = " - ∞  /  00_000"
INFINITY_0_DIFFICULTY_LABEL = " -∞  /  00_000"
# INFINITY_0_DIFFICULTY_LABEL = " <span style='font-size:20px;'>- ∞</span>  /  00_000"

# properties of the plotting: scatter:
MINING_TIMES_SCATTER_COLOR = 'lime'
BIT_DIFFICULTY_SCATTER_COLOR = 'red'

AX2_SCATTER_Z_ORDER = 3

FIGURE_BASE = 0.5

# properties of logging:
DEFAULT_PRECISION = 10  # default precision for the floating point numbers



# constants.py

# Colors for different plot elements
MINING_TIME_COLOR = 'red'  # Bar color for mining times
AVERAGE_MINING_TIME_COLOR = 'lightcoral'
MINING_TIMES_SCATTER_COLOR = 'red'  # Color for scatter plot of mining times

LABEL_DIFFICULTY_COLOR = 'blue'

DIFFICULTY_COLOR = (173/255, 216/255, 230/255, 0.7)  # Light blue for difficulty with 70% transparency

# Font sizes and styles
FONT_SIZE = 14  # General font size for labels
LEGEND_FONT_SIZE = 12  # Slightly increased for readability
PLOT_TITLE_FONT_SIZE = 16  # Increased for prominence

# Line widths and marker sizes
LINE_WIDTH = 2  # Thickness for difficulty lines
GRID_LINE_WIDTH = 0.3  # Reduced grid line width for subtlety
MARKER_SIZE = 10  # Marker size for scatter plot points

# Title and legend positions
PLOT_TITLE_Y = 1.05  # Adjusted title position for better visibility
X_LEGEND_POSITION = 0.9  # Move legend slightly to the right to avoid overlap
Y_LEGEND_POSITION = 0.88  # Position legend slightly below the title
LEGEND_B_BOX_Y = -0.15  # Position legend below the plot
# LEGEND_B_BOX_Y = -0.00  # Position legend below the plot
LEGEND_LOCATION = 'upper right'  # Adjusted legend location

GUI_TITLE = "Blockchain Configuration"
EXIT_BUTTON_TEXT = "Exit (Esc)"
CLEAR_LOG_BUTTON_TEXT = "Clear Log"
RUN_BLOCKCHAIN_BUTTON_TEXT = "Run Blockchain (Space)"
CLOSE_TYPE = "WM_DELETE_WINDOW"
CONFIGURATION_PARAMETERS_BUTTON_TEXT = "Configuration Parameters"
FIGSIZE = (14, 8)
HIGHT = "600"
WIDTH = "1200"
HEXADECIMAL_BASE = 16
SHA256_ENCODING = 'utf-8'
AVERAGE_MINING_TIME_ADJUSTMENT_INTERVAL_KEY = "average_mining_time_adjustment_interval"
LEGEND_TITLE = "Input Information"

REVERSED_ADJUSTMENT_FACTOR_KEY = "reversed_adjustment_factor"
