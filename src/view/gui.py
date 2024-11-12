#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import logging
import tkinter as tk
import time
from tkinter import messagebox

# from PIL.FontFile import WIDTH
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.model.blockchain import Blockchain
from src.controller.helpers import add_blocks
from src.utils.logger_singleton import LoggerSingleton
from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
    SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, NUMBER_BLOCKS_SLICE, INITIAL_BIT_DIFFICULTY_KEY, \
    TARGET_BLOCK_MINING_TIME_KEY, ADJUSTMENT_BLOCK_INTERVAL_KEY, CLAMP_FACTOR_KEY, SMALLEST_BIT_DIFFICULTY_KEY, \
    NUMBER_BLOCKS_TO_ADD_KEY, NUMBER_BLOCKS_SLICE_KEY, GUI_TITLE, EXIT_BUTTON_TEXT, CLEAR_LOG_BUTTON_TEXT, \
    RUN_BLOCKCHAIN_BUTTON_TEXT, CLOSE_TYPE, CONFIGURATION_PARAMETERS_BUTTON_TEXT, HIGHT, WIDTH
from src.utils.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
from src.view.plotting import plot_blockchain_statistics # todo why isn't used?


import re


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        # Remove ANSI escape codes
        msg = re.sub(r'\x1b\[[0-9;]*m', '', msg)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.yview(tk.END)



class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title(GUI_TITLE)
        self.root.geometry(f"{WIDTH}x{HIGHT}")  # Adjust window size

        # Bind the Esc key to the exit_app method
        self.root.bind('<Escape>', lambda event: self.exit_app())

        # Handle window close event
        self.root.protocol(CLOSE_TYPE, self.on_closing)

        # Define main frame with padding
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(side=tk.LEFT, fill="both", expand=True)

        # Create configuration frame with a label
        config_frame = tk.LabelFrame(main_frame, text=CONFIGURATION_PARAMETERS_BUTTON_TEXT, padx=10, pady=10)
        config_frame.pack(fill="x", pady=10)

        self.config_params = {
            INITIAL_BIT_DIFFICULTY_KEY: tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
            TARGET_BLOCK_MINING_TIME_KEY: tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
            ADJUSTMENT_BLOCK_INTERVAL_KEY: tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
            CLAMP_FACTOR_KEY: tk.DoubleVar(value=CLAMP_FACTOR),
            SMALLEST_BIT_DIFFICULTY_KEY: tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
            NUMBER_BLOCKS_TO_ADD_KEY: tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
            NUMBER_BLOCKS_SLICE_KEY: tk.IntVar(value=NUMBER_BLOCKS_SLICE)
        }

        # Place each parameter in the frame
        for idx, (label, var) in enumerate(self.config_params.items()):
            tk.Label(config_frame, text=label).grid(row=idx, column=0, sticky="w", pady=5, padx=5)
            tk.Entry(config_frame, textvariable=var, width=25).grid(row=idx, column=1, pady=5, padx=5)

        # Run, Clear Log, and Exit buttons in a separate frame
        button_frame = tk.Frame(main_frame, pady=10)
        button_frame.pack()

        self.run_button = tk.Button(button_frame, text=RUN_BLOCKCHAIN_BUTTON_TEXT, command=self.run_blockchain, width=25)
        self.run_button.grid(row=0, column=0, padx=10)
        self.root.after(100, self.run_button.focus_set)

        # self.clear_log_button = tk.Button(button_frame, text=CLEAR_LOG_BUTTON_TEXT, command=self.clear_log, width=15)
        # self.clear_log_button.grid(row=0, column=1, padx=10)

        self.exit_button = tk.Button(button_frame, text=EXIT_BUTTON_TEXT, command=self.exit_app, width=15)
        self.exit_button.grid(row=0, column=2, padx=10)

        # Create a frame for the logging Text widget
        log_frame = tk.Frame(self.root, padx=10, pady=10)
        log_frame.pack(side=tk.RIGHT, fill="both", expand=True)

        # Create a Text widget for displaying log information
        self.log_text = tk.Text(log_frame, height=10, wrap="word")
        self.log_text.pack(side=tk.LEFT, fill="both", expand=True)

        # Add a scrollbar to the Text widget
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Create a frame for the plot
        plot_frame = tk.Frame(main_frame, pady=10)
        plot_frame.pack(fill="both", expand=True)

        # Create a matplotlib figure and add it to the plot frame
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Set up logging to the ScrolledText widget
        self.text_handler = TextHandler(self.log_text)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.text_handler.setFormatter(formatter)
        logging.basicConfig(level=logging.DEBUG, handlers=[self.text_handler])

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def run_blockchain(self, event=None):
        self.root.update()  # Update the window to apply the fullscreen attribute

        # Disable the button to prevent multiple clicks
        self.run_button.config(state=tk.DISABLED)

        start_time = time.time()

        logger = LoggerSingleton.get_instance().logger
        log_level_counter_handler = LogLevelCounterHandler()
        logger.addHandler(log_level_counter_handler)

        initial_bit_difficulty = self.config_params[INITIAL_BIT_DIFFICULTY_KEY].get()  # todo init once, generalize in the loop
        target_block_mining_time = self.config_params[TARGET_BLOCK_MINING_TIME_KEY].get()
        adjustment_block_interval = self.config_params[ADJUSTMENT_BLOCK_INTERVAL_KEY].get()
        clamp_factor = self.config_params[CLAMP_FACTOR_KEY].get()
        smallest_bit_difficulty = self.config_params[SMALLEST_BIT_DIFFICULTY_KEY].get()
        number_blocks_to_add = self.config_params[NUMBER_BLOCKS_TO_ADD_KEY].get()
        number_blocks_slice = self.config_params[NUMBER_BLOCKS_SLICE_KEY].get()

        blockchain = Blockchain(
            initial_bit_difficulty=initial_bit_difficulty,
            target_block_mining_time=target_block_mining_time,
            adjustment_block_interval=adjustment_block_interval,
            number_blocks_to_add=number_blocks_to_add,
            clamp_factor=clamp_factor,
            smallest_bit_difficulty=smallest_bit_difficulty,
            number_blocks_slice=number_blocks_slice,
        )

        add_blocks(
            blockchain=blockchain,
            number_of_blocks_to_add=number_blocks_to_add,
        )

        log_blockchain_statistics(logger, blockchain)

        # Clear the previous plot
        self.figure.clear()

        # # Plot the blockchain statistics on the canvas
        # ax1 = self.figure.add_subplot(111)
        plot_blockchain_statistics(blockchain)
        #
        # self.canvas.draw()

        # # Display log information in the Text widget
        # self.log_text.delete(1.0, tk.END)
        # for handler in logger.handlers:
        #     if isinstance(handler, LogLevelCounterHandler):
        #         self.log_text.insert(tk.END, handler.get_log_contents())
        #
        log_level_counter_handler.print_log_counts()

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
        logger.info(f"")

        # Re-enable the button after the blockchain has been run
        self.run_button.config(state=tk.NORMAL)

    # def clear_log(self):
    #     self.log_text.config(state=tk.NORMAL)
    #     self.log_text.delete(1.0, tk.END)
    #     self.log_text.config(state=tk.DISABLED)
    #
    #     # Re-attach the text handler to the logger
    #     logger = LoggerSingleton.get_instance().logger
    #     logger.handlers = [h for h in logger.handlers if not isinstance(h, TextHandler)]
    #     logger.addHandler(self.text_handler)

    def exit_app(self):
        self.root.quit()
        self.root.destroy()

def config_gui():
    """Function to initialize and run the configuration UI."""
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Start the GUI in full screen
    app = GUI(root)
    root.mainloop()

