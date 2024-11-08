# # # #   Copyright (c) 2024, Anton Gorshkov
# # # #   All rights reserved.
# # # #   This code is for a block and its unit tests.
# # # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# #
# #
# import tkinter as tk
# import time
# from tkinter import messagebox
# from blockchain import Blockchain
# from helpers import add_blocks
# from logger_singleton import LoggerSingleton
# from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
#     SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
# from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# from plotting import plot_blockchain_statistics
#
#
# class GUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Blockchain Configuration")
#         self.root.geometry("600x400")  # Set window size for a more compact look
#
#         # Bind the Esc key to the exit_app method
#         self.root.bind('<Escape>', lambda event: self.exit_app())
#
#         # Handle window close event
#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
#
#         # Define main frame with padding
#         main_frame = tk.Frame(self.root, padx=10, pady=10)
#         main_frame.pack(fill="both", expand=True)
#
#         # Create configuration frame with a label
#         config_frame = tk.LabelFrame(main_frame, text="Configuration Parameters", padx=10, pady=10)
#         config_frame.pack(fill="x", pady=10)
#
#         self.config_params = {
#             "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
#             "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
#             "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
#             "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
#             "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
#             "number_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
#             "number_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
#         }
#
#         # Place each parameter in the frame
#         for idx, (label, var) in enumerate(self.config_params.items()):
#             tk.Label(config_frame, text=label).grid(row=idx, column=0, sticky="w", pady=5, padx=5)
#             tk.Entry(config_frame, textvariable=var, width=25).grid(row=idx, column=1, pady=5, padx=5)
#
#         # Run and Exit buttons in a separate frame
#         button_frame = tk.Frame(main_frame, pady=10)
#         button_frame.pack()
#
#         self.run_button = tk.Button(button_frame, text="Run Blockchain", command=self.run_blockchain, width=15)
#         self.run_button.grid(row=0, column=0, padx=10)
#         self.run_button.focus_set()
#
#         self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app, width=15)
#         self.exit_button.grid(row=0, column=1, padx=10)
#
#     def on_closing(self):
#         if messagebox.askokcancel("Quit", "Do you want to quit?"):
#             self.root.destroy()
#
#     def run_blockchain(self, event=None):
#         self.root.update()  # Update the window to apply the fullscreen attribute
#
#         # Disable the button to prevent multiple clicks
#         self.run_button.config(state=tk.DISABLED)
#
#         start_time = time.time()
#
#         logger = LoggerSingleton.get_instance().logger
#         log_level_counter_handler = LogLevelCounterHandler()
#         logger.addHandler(log_level_counter_handler)
#
#         # Collect values from the UI
#         initial_bit_difficulty = self.config_params["initial_bit_difficulty"].get()
#         target_block_mining_time = self.config_params["target_block_mining_time"].get()
#         adjustment_block_interval = self.config_params["adjustment_block_interval"].get()
#         clamp_factor = self.config_params["clamp_factor"].get()
#         smallest_bit_difficulty = self.config_params["smallest_bit_difficulty"].get()
#         number_blocks_to_add = self.config_params["number_blocks_to_add"].get()
#         number_blocks_slice = self.config_params["number_blocks_slice"].get()
#
#         blockchain = Blockchain(
#             initial_bit_difficulty=initial_bit_difficulty,
#             target_block_mining_time=target_block_mining_time,
#             adjustment_block_interval=adjustment_block_interval,
#             number_blocks_to_add=number_blocks_to_add,
#             clamp_factor=clamp_factor,
#             smallest_bit_difficulty=smallest_bit_difficulty,
#             number_blocks_slice=number_blocks_slice,
#         )
#
#         add_blocks(
#             blockchain=blockchain,
#             number_of_blocks_to_add=number_blocks_to_add,
#         )
#
#         log_blockchain_statistics(logger, blockchain)
#         plot_blockchain_statistics(blockchain)
#
#         log_level_counter_handler.print_log_counts()
#
#         end_time = time.time()
#         execution_time = end_time - start_time
#         logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
#         logger.info(f"")
#
#         # Re-enable the button after the blockchain has been run
#         self.run_button.config(state=tk.NORMAL)
#
#     def exit_app(self):
#         self.root.quit()
#         self.root.destroy()
#
#
# def config_gui():
#     """Function to initialize and run the configuration UI."""
#     root = tk.Tk()
#     app = GUI(root)
#     root.mainloop()
#


import tkinter as tk
import time
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from blockchain import Blockchain
from helpers import add_blocks
from logger_singleton import LoggerSingleton
from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
    SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
from plotting import plot_blockchain_statistics


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Configuration")
        self.root.geometry("800x600")  # Adjust window size to accommodate the plot

        # Bind the Esc key to the exit_app method
        self.root.bind('<Escape>', lambda event: self.exit_app())

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Define main frame with padding
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Create configuration frame with a label
        config_frame = tk.LabelFrame(main_frame, text="Configuration Parameters", padx=10, pady=10)
        config_frame.pack(fill="x", pady=10)

        self.config_params = {
            "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
            "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
            "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
            "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
            "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
            "number_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
            "number_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
        }

        # Place each parameter in the frame
        for idx, (label, var) in enumerate(self.config_params.items()):
            tk.Label(config_frame, text=label).grid(row=idx, column=0, sticky="w", pady=5, padx=5)
            tk.Entry(config_frame, textvariable=var, width=25).grid(row=idx, column=1, pady=5, padx=5)

        # Run and Exit buttons in a separate frame
        button_frame = tk.Frame(main_frame, pady=10)
        button_frame.pack()

        self.run_button = tk.Button(button_frame, text="Run Blockchain", command=self.run_blockchain, width=15)
        self.run_button.grid(row=0, column=0, padx=10)
        self.run_button.focus_set() # todo why does this not work?

        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app, width=15)
        self.exit_button.grid(row=0, column=1, padx=10)

        # Create a frame for the plot
        plot_frame = tk.Frame(main_frame, pady=10)
        plot_frame.pack(fill="both", expand=True)

        # Create a matplotlib figure and add it to the plot frame
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

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

        # Collect values from the UI
        initial_bit_difficulty = self.config_params["initial_bit_difficulty"].get()
        target_block_mining_time = self.config_params["target_block_mining_time"].get()
        adjustment_block_interval = self.config_params["adjustment_block_interval"].get()
        clamp_factor = self.config_params["clamp_factor"].get()
        smallest_bit_difficulty = self.config_params["smallest_bit_difficulty"].get()
        number_blocks_to_add = self.config_params["number_blocks_to_add"].get()
        number_blocks_slice = self.config_params["number_blocks_slice"].get()

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

        # Plot the blockchain statistics on the canvas
        ax1 = self.figure.add_subplot(111)
        plot_blockchain_statistics(blockchain, ax1=ax1)

        self.canvas.draw()

        log_level_counter_handler.print_log_counts()

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
        logger.info(f"")

        # Re-enable the button after the blockchain has been run
        self.run_button.config(state=tk.NORMAL)

    def exit_app(self):
        self.root.quit()
        self.root.destroy()


def config_gui():
    """Function to initialize and run the configuration UI."""
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Start the GUI in full screen
    app = GUI(root)
    root.mainloop()


