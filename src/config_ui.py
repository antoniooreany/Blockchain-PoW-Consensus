#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import tkinter as tk
import time
from blockchain import Blockchain
from helpers import add_blocks
from logger_singleton import LoggerSingleton
from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
    SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
from plotting import plot_blockchain_statistics


class BlockchainConfigUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Configuration")
        self.root.focus_force()
        self.root.attributes('-fullscreen', True)

        self.config_params = {
            "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
            "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
            "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
            "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
            "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
            "number_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
            "slice_factor": tk.DoubleVar(value=SLICE_FACTOR),
            "number_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
        }

        for idx, (label, var) in enumerate(self.config_params.items()):
            tk.Label(root, text=label.replace('_', ' ').title()).grid(row=idx, column=0)
            tk.Entry(root, textvariable=var).grid(row=idx, column=1)

        self.config_params["number_blocks_to_add"].trace_add("write", self.update_number_blocks_slice)
        self.config_params["slice_factor"].trace_add("write", self.update_number_blocks_slice)

        self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
        self.run_button.grid(row=len(self.config_params), column=0, columnspan=2)
        self.run_button.focus_set()

        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=len(self.config_params) + 1, column=0, columnspan=2)

    def update_number_blocks_slice(self, *args):
        try:
            number_blocks_to_add = self.config_params["number_blocks_to_add"].get()
            slice_factor = self.config_params["slice_factor"].get()
            number_blocks_slice = int(number_blocks_to_add / slice_factor)
            self.config_params["number_blocks_slice"].set(number_blocks_slice)
        except (tk.TclError, ZeroDivisionError):
            self.config_params["number_blocks_slice"].set(0)

    def run_blockchain(self, event=None):

        self.root.attributes('-fullscreen', True)  # Allow the window to go behind others
        self.root.update()  # Update the window to apply the fullscreen attribute

        # Recalculate number_of_blocks_slice before running the blockchain
        self.update_number_blocks_slice()

        # Disable the button to prevent multiple clicks
        self.run_button.config(state=tk.DISABLED)

        start_time = time.time()

        logger = LoggerSingleton.get_instance().logger
        log_level_counter_handler = LogLevelCounterHandler()
        logger.addHandler(log_level_counter_handler)

        # Collect values from the UI
        initial_bit_difficulty = self.config_params["initial_bit_difficulty"].get()
        target_block_mining_time = self.config_params["target_block_mining_time"].get()
        adjustment_block_interval = self.config_params["adjustment_block_interval"].get()
        clamp_factor = self.config_params["clamp_factor"].get()
        smallest_bit_difficulty = self.config_params["smallest_bit_difficulty"].get()
        number_blocks_to_add = self.config_params["number_blocks_to_add"].get()
        slice_factor = self.config_params["slice_factor"].get()
        number_blocks_slice = self.config_params["number_blocks_slice"].get()

        # Log the collected values
        # logger.info(f"Initial Bit Difficulty: {initial_bit_difficulty}")
        # logger.info(f"Target Block Mining Time: {target_block_mining_time}")
        # logger.info(f"Adjustment Block Interval: {adjustment_block_interval}")
        # logger.info(f"Clamp Factor: {clamp_factor}")
        # logger.info(f"Smallest Bit Difficulty: {smallest_bit_difficulty}")
        # logger.info(f"Number of Blocks to Add: {number_blocks_to_add}")
        # logger.info(f"Slice Factor: {slice_factor}")
        # logger.info(f"Number of Blocks Slice: {number_of_blocks_slice}")

        blockchain = Blockchain(
            initial_bit_difficulty=initial_bit_difficulty,
            target_block_mining_time=target_block_mining_time,
            adjustment_block_interval=adjustment_block_interval,
            number_blocks_to_add=number_blocks_to_add,
            clamp_factor=clamp_factor,
            smallest_bit_difficulty=smallest_bit_difficulty,
            slice_factor=slice_factor,
        )

        add_blocks(
            blockchain=blockchain,
            number_of_blocks_to_add=number_blocks_to_add,
        )

        log_blockchain_statistics(logger, blockchain)
        plot_blockchain_statistics(blockchain)

        log_level_counter_handler.print_log_counts()

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
        logger.info(f"")

        # Re-enable the button after the blockchain has been run
        self.run_button.config(state=tk.NORMAL)

    def exit_app(self):
        self.root.quit()


def config_ui():
    """Function to initialize and run the configuration UI."""
    root = tk.Tk()
    app = BlockchainConfigUI(root)
    root.mainloop()
