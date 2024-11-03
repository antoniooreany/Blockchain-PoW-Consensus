# # # # # import tkinter as tk
# # # # # from tkinter import messagebox
# # # # #
# # # # # # Default values
# # # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # #
# # # # #
# # # # # class BlockchainConfigUI:
# # # # #     def __init__(self, root):
# # # # #         self.root = root
# # # # #         self.root.title("Blockchain Configuration")
# # # # #
# # # # #         # Labels and entry fields for constants
# # # # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # # # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # # # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # # # #
# # # # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # # # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # # # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # # # #
# # # # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # # # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # # # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # # # #
# # # # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # # # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # # # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # # # #
# # # # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # # # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # # # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # # # #
# # # # #         # Save button
# # # # #         tk.Button(root, text="Save Configuration", command=self.save_config).grid(row=5, column=0, columnspan=2)
# # # # #
# # # # #     def save_config(self):
# # # # #         # Collect values from the UI and save them in a dictionary or directly use them to configure the blockchain
# # # # #         config = {
# # # # #             "initial_bit_difficulty": self.initial_bit_difficulty.get(),
# # # # #             "adjustment_block_interval": self.adjustment_block_interval.get(),
# # # # #             "target_block_mining_time": self.target_block_mining_time.get(),
# # # # #             "clamp_factor": self.clamp_factor.get(),
# # # # #             "smallest_bit_difficulty": self.smallest_bit_difficulty.get(),
# # # # #         }
# # # # #
# # # # #         # Display a confirmation dialog
# # # # #         messagebox.showinfo("Configuration Saved", "The configuration has been successfully saved.")
# # # # #
# # # # #         # Here, you would typically pass `config` to the rest of your application.
# # # # #         print("Configuration:", config)  # For demonstration purposes only
# # # # #
# # # # #
# # # # # def open_config_ui():
# # # # #     """Function to initialize and run the configuration UI."""
# # # # #     root = tk.Tk()
# # # # #     app = BlockchainConfigUI(root)
# # # # #     root.mainloop()
# # # # #
# # # #
# # # #
# # # # import tkinter as tk
# # # # from tkinter import messagebox
# # # # import logging
# # # # import time
# # # # from blockchain import Blockchain
# # # # from helpers import add_blocks
# # # # from logger_singleton import LoggerSingleton
# # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # from plotting import plot_blockchain_statistics
# # # #
# # # # # Default values
# # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # DEFAULT_NUMBER_BLOCKS_TO_ADD = 10000
# # # #
# # # # class BlockchainConfigUI:
# # # #     def __init__(self, root):
# # # #         self.root = root
# # # #         self.root.title("Blockchain Configuration")
# # # #
# # # #         # Labels and entry fields for constants
# # # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # # #
# # # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # # #
# # # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # # #
# # # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # # #
# # # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # # #
# # # #         # Save button
# # # #         tk.Button(root, text="Save Configuration", command=self.save_config).grid(row=5, column=0, columnspan=2)
# # # #
# # # #         # Run Blockchain button
# # # #         tk.Button(root, text="Run Blockchain", command=self.run_blockchain).grid(row=6, column=0, columnspan=2)
# # # #
# # # #     def save_config(self):
# # # #         # Collect values from the UI and save them in a dictionary or directly use them to configure the blockchain
# # # #         config = {
# # # #             "initial_bit_difficulty": self.initial_bit_difficulty.get(),
# # # #             "adjustment_block_interval": self.adjustment_block_interval.get(),
# # # #             "target_block_mining_time": self.target_block_mining_time.get(),
# # # #             "clamp_factor": self.clamp_factor.get(),
# # # #             "smallest_bit_difficulty": self.smallest_bit_difficulty.get(),
# # # #         }
# # # #
# # # #         # Display a confirmation dialog
# # # #         messagebox.showinfo("Configuration Saved", "The configuration has been successfully saved.")
# # # #
# # # #         # Here, you would typically pass `config` to the rest of your application.
# # # #         print("Configuration:", config)  # For demonstration purposes only
# # # #
# # # #     def run_blockchain(self):
# # # #         # Collect values from the UI
# # # #         initial_bit_difficulty = self.initial_bit_difficulty.get()
# # # #         adjustment_block_interval = self.adjustment_block_interval.get()
# # # #         target_block_mining_time = self.target_block_mining_time.get()
# # # #         clamp_factor = self.clamp_factor.get()
# # # #         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
# # # #
# # # #         # Record the start time
# # # #         start_time = time.time()
# # # #
# # # #         # Set the logging level to INFO (or WARNING to reduce more output)
# # # #         logging.getLogger('matplotlib').setLevel(logging.INFO)
# # # #
# # # #         logger = LoggerSingleton.get_instance().logger
# # # #
# # # #         # Add custom handler to track errors and critical issues
# # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # #         logger.addHandler(log_level_counter_handler)
# # # #
# # # #         blockchain = Blockchain(
# # # #             initial_bit_difficulty=initial_bit_difficulty,
# # # #             adjustment_block_interval=adjustment_block_interval,
# # # #             target_block_mining_time=target_block_mining_time,
# # # #         )
# # # #
# # # #         add_blocks(
# # # #             blockchain=blockchain,
# # # #             number_of_blocks_to_add=DEFAULT_NUMBER_BLOCKS_TO_ADD,
# # # #             clamp_factor=clamp_factor,
# # # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # # #         )
# # # #
# # # #         log_blockchain_statistics(logger, blockchain)
# # # #         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
# # # #
# # # #         log_level_counter_handler.print_log_counts()
# # # #
# # # #         # Record the end time
# # # #         end_time = time.time()
# # # #
# # # #         # Calculate and print the execution time
# # # #         execution_time = end_time - start_time
# # # #         logger.info(f"Program execution time: {execution_time:.2f} seconds")
# # # #
# # # #         # Display a confirmation dialog
# # # #         messagebox.showinfo("Blockchain Run", "The blockchain has been successfully run.")
# # # #
# # # # def open_config_ui():
# # # #     """Function to initialize and run the configuration UI."""
# # # #     root = tk.Tk()
# # # #     app = BlockchainConfigUI(root)
# # # #     root.mainloop()
# # # #
# # # #
# # #
# # #
# # # import tkinter as tk
# # # from tkinter import messagebox
# # # import logging
# # # import time
# # # from blockchain import Blockchain
# # # from helpers import add_blocks
# # # from logger_singleton import LoggerSingleton
# # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # from plotting import plot_blockchain_statistics
# # #
# # # # Default values
# # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # DEFAULT_CLAMP_FACTOR = 2.0
# # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # DEFAULT_NUMBER_BLOCKS_TO_ADD = 100
# # #
# # # class BlockchainConfigUI:
# # #     def __init__(self, root):
# # #         self.root = root
# # #         self.root.title("Blockchain Configuration")
# # #
# # #         # Labels and entry fields for constants
# # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # #
# # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # #
# # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # #
# # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # #
# # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # #
# # #         # Run Blockchain button
# # #         tk.Button(root, text="Run Blockchain", command=self.run_blockchain).grid(row=5, column=0, columnspan=2)
# # #
# # #     def run_blockchain(self):
# # #         # Collect values from the UI
# # #         initial_bit_difficulty = self.initial_bit_difficulty.get()
# # #         adjustment_block_interval = self.adjustment_block_interval.get()
# # #         target_block_mining_time = self.target_block_mining_time.get()
# # #         clamp_factor = self.clamp_factor.get()
# # #         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
# # #
# # #         # Record the start time
# # #         start_time = time.time()
# # #
# # #         # Set the logging level to INFO (or WARNING to reduce more output)
# # #         logging.getLogger('matplotlib').setLevel(logging.INFO)
# # #
# # #         logger = LoggerSingleton.get_instance().logger
# # #
# # #         # Add custom handler to track errors and critical issues
# # #         log_level_counter_handler = LogLevelCounterHandler()
# # #         logger.addHandler(log_level_counter_handler)
# # #
# # #         blockchain = Blockchain(
# # #             initial_bit_difficulty=initial_bit_difficulty,
# # #             adjustment_block_interval=adjustment_block_interval,
# # #             target_block_mining_time=target_block_mining_time,
# # #         )
# # #
# # #         add_blocks(
# # #             blockchain=blockchain,
# # #             number_of_blocks_to_add=DEFAULT_NUMBER_BLOCKS_TO_ADD,
# # #             clamp_factor=clamp_factor,
# # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # #         )
# # #
# # #         log_blockchain_statistics(logger, blockchain)
# # #         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
# # #
# # #         log_level_counter_handler.print_log_counts()
# # #
# # #         # Record the end time
# # #         end_time = time.time()
# # #
# # #         # Calculate and print the execution time
# # #         execution_time = end_time - start_time
# # #         logger.info(f"Program execution time: {execution_time:.2f} seconds")
# # #
# # #         # # Display a confirmation dialog
# # #         # messagebox.showinfo("Blockchain Run")
# # #
# # # def open_config_ui():
# # #     """Function to initialize and run the configuration UI."""
# # #     root = tk.Tk()
# # #     app = BlockchainConfigUI(root)
# # #     root.mainloop()
# # #
# #
# #
# #
# # import tkinter as tk
# # from tkinter import messagebox
# # import logging
# # import time
# # from blockchain import Blockchain
# # from helpers import add_blocks
# # from logger_singleton import LoggerSingleton
# # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # from plotting import plot_blockchain_statistics
# #
# # # Default values
# # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # DEFAULT_CLAMP_FACTOR = 2.0
# # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # DEFAULT_NUMBER_BLOCKS_TO_ADD = 100
# #
# # class BlockchainConfigUI:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Blockchain Configuration")
# #
# #         # Labels and entry fields for constants
# #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# #
# #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# #
# #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# #
# #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# #
# #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# #
# #         tk.Label(root, text="Number of Blocks to Add").grid(row=5, column=0)
# #         self.number_of_blocks_to_add = tk.IntVar(value=DEFAULT_NUMBER_BLOCKS_TO_ADD)
# #         tk.Entry(root, textvariable=self.number_of_blocks_to_add).grid(row=5, column=1)
# #
# #         # Run Blockchain button
# #         tk.Button(root, text="Run Blockchain", command=self.run_blockchain).grid(row=6, column=0, columnspan=2)
# #
# #     def run_blockchain(self):
# #         # Collect values from the UI
# #         initial_bit_difficulty = self.initial_bit_difficulty.get()
# #         adjustment_block_interval = self.adjustment_block_interval.get()
# #         target_block_mining_time = self.target_block_mining_time.get()
# #         clamp_factor = self.clamp_factor.get()
# #         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
# #         number_of_blocks_to_add = self.number_of_blocks_to_add.get()
# #
# #         # Record the start time
# #         start_time = time.time()
# #
# #         # Set the logging level to INFO (or WARNING to reduce more output)
# #         logging.getLogger('matplotlib').setLevel(logging.INFO)
# #
# #         logger = LoggerSingleton.get_instance().logger
# #
# #         # Add custom handler to track errors and critical issues
# #         log_level_counter_handler = LogLevelCounterHandler()
# #         logger.addHandler(log_level_counter_handler)
# #
# #         blockchain = Blockchain(
# #             initial_bit_difficulty=initial_bit_difficulty,
# #             adjustment_block_interval=adjustment_block_interval,
# #             target_block_mining_time=target_block_mining_time,
# #         )
# #
# #         add_blocks(
# #             blockchain=blockchain,
# #             number_of_blocks_to_add=number_of_blocks_to_add,
# #             clamp_factor=clamp_factor,
# #             smallest_bit_difficulty=smallest_bit_difficulty,
# #         )
# #
# #         log_blockchain_statistics(logger, blockchain)
# #         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
# #
# #         log_level_counter_handler.print_log_counts()
# #
# #         # Record the end time
# #         end_time = time.time()
# #
# #         # Calculate and print the execution time
# #         execution_time = end_time - start_time
# #         logger.info(f"Program execution time: {execution_time:.2f} seconds")
# #
# #         # # Display a confirmation dialog
# #         # messagebox.showinfo("Blockchain Run", "The blockchain has been successfully run.")
# #
# # def open_config_ui():
# #     """Function to initialize and run the configuration UI."""
# #     root = tk.Tk()
# #     app = BlockchainConfigUI(root)
# #     root.mainloop()
# #     exit(0) # todo exit(0) is added to prevent the error: _tkinter.TclError: can't invoke "event" command: application has been destroyed
# #
#
#
# import tkinter as tk
# from tkinter import messagebox
# import logging
# import time
# from blockchain import Blockchain
# from helpers import add_blocks
# from logger_singleton import LoggerSingleton
# from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# from plotting import plot_blockchain_statistics
#
# # Default values
# DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# DEFAULT_CLAMP_FACTOR = 2.0
# DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# DEFAULT_NUMBER_BLOCKS_TO_ADD = 100
#
# class BlockchainConfigUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Blockchain Configuration")
#
#         # Labels and entry fields for constants
#         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
#         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
#         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
#
#         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
#         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
#         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
#
#         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
#         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
#         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
#
#         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
#         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
#         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
#
#         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
#         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
#         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
#
#         tk.Label(root, text="Number of Blocks to Add").grid(row=5, column=0)
#         self.number_of_blocks_to_add = tk.IntVar(value=DEFAULT_NUMBER_BLOCKS_TO_ADD)
#         tk.Entry(root, textvariable=self.number_of_blocks_to_add).grid(row=5, column=1)
#
#         # Run Blockchain button
#         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
#         self.run_button.grid(row=6, column=0, columnspan=2)
#         self.run_button.focus_set()
#
#         # Bind Enter and Space keys to the Run Blockchain button, make it pressed when the keys are pressed
#         # self.root.bind('<Return>', lambda event: self.run_blockchain())
#         # self.root.bind('<space>', lambda event: self.run_blockchain())
#         self.run_button.bind('<Return>', lambda event: self.run_blockchain(), add='+')
#         self.run_button.bind('<space>', lambda event: self.run_blockchain(), add='+')
#
#     def run_blockchain(self):
#         # Collect values from the UI
#         initial_bit_difficulty = self.initial_bit_difficulty.get()
#         adjustment_block_interval = self.adjustment_block_interval.get()
#         target_block_mining_time = self.target_block_mining_time.get()
#         clamp_factor = self.clamp_factor.get()
#         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
#         number_of_blocks_to_add = self.number_of_blocks_to_add.get()
#
#         # Record the start time
#         start_time = time.time()
#
#         # Set the logging level to INFO (or WARNING to reduce more output)
#         logging.getLogger('matplotlib').setLevel(logging.INFO)
#
#         logger = LoggerSingleton.get_instance().logger
#
#         # Add custom handler to track errors and critical issues
#         log_level_counter_handler = LogLevelCounterHandler()
#         logger.addHandler(log_level_counter_handler)
#
#         blockchain = Blockchain(
#             initial_bit_difficulty=initial_bit_difficulty,
#             adjustment_block_interval=adjustment_block_interval,
#             target_block_mining_time=target_block_mining_time,
#         )
#
#         add_blocks(
#             blockchain=blockchain,
#             number_of_blocks_to_add=number_of_blocks_to_add,
#             clamp_factor=clamp_factor,
#             smallest_bit_difficulty=smallest_bit_difficulty,
#         )
#
#         log_blockchain_statistics(logger, blockchain)
#         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
#
#         log_level_counter_handler.print_log_counts()
#
#         # Record the end time
#         end_time = time.time()
#
#         # Calculate and print the execution time
#         execution_time = end_time - start_time
#         logger.info(f"Program execution time: {execution_time:.2f} seconds")
#
#         # # Display a confirmation dialog
#         # messagebox.showinfo("Blockchain Run", "The blockchain has been successfully run.")
#
# def open_config_ui():
#     """Function to initialize and run the configuration UI."""
#     root = tk.Tk()
#     app = BlockchainConfigUI(root)
#     root.mainloop()
#     exit(0)
#


import tkinter as tk
from tkinter import messagebox
import logging
import time
from blockchain import Blockchain
from helpers import add_blocks
from logger_singleton import LoggerSingleton
from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
from plotting import plot_blockchain_statistics

# Default values
DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
DEFAULT_CLAMP_FACTOR = 2.0
DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
DEFAULT_NUMBER_BLOCKS_TO_ADD = 100

class BlockchainConfigUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Configuration")
        # self.root.geometry("400x300")  # Set a fixed size for the window
        self.root.focus_force()  # Make the window focused
        # self.root.attributes('-topmost', True)  # Keep the window on top of others
        self.root.attributes('-fullscreen', True)  # Allow the window to go behind others

        # Labels and entry fields for constants
        tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
        self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
        tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)

        tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
        self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
        tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)

        tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
        self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
        tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)

        tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
        self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
        tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)

        tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
        self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
        tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)

        tk.Label(root, text="Number of Blocks to Add").grid(row=5, column=0)
        self.number_of_blocks_to_add = tk.IntVar(value=DEFAULT_NUMBER_BLOCKS_TO_ADD)
        tk.Entry(root, textvariable=self.number_of_blocks_to_add).grid(row=5, column=1)

        # Run Blockchain button
        self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
        self.run_button.grid(row=6, column=0, columnspan=2)
        self.run_button.focus_set()

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=7, column=0, columnspan=2)

        # Bind Enter and Space keys to the Run Blockchain button, make it pressed when the keys are pressed
        self.run_button.bind('<Return>', lambda event: self.run_blockchain(), add='+')
        self.run_button.bind('<space>', lambda event: self.run_blockchain(), add='+')

    def run_blockchain(self):
        # Collect values from the UI
        initial_bit_difficulty = self.initial_bit_difficulty.get()
        adjustment_block_interval = self.adjustment_block_interval.get()
        target_block_mining_time = self.target_block_mining_time.get()
        clamp_factor = self.clamp_factor.get()
        smallest_bit_difficulty = self.smallest_bit_difficulty.get()
        number_of_blocks_to_add = self.number_of_blocks_to_add.get()

        # Record the start time
        start_time = time.time()

        # Set the logging level to INFO (or WARNING to reduce more output)
        logging.getLogger('matplotlib').setLevel(logging.INFO)

        logger = LoggerSingleton.get_instance().logger

        # Add custom handler to track errors and critical issues
        log_level_counter_handler = LogLevelCounterHandler()
        logger.addHandler(log_level_counter_handler)

        blockchain = Blockchain(
            initial_bit_difficulty=initial_bit_difficulty,
            adjustment_block_interval=adjustment_block_interval,
            target_block_mining_time=target_block_mining_time,
        )

        add_blocks(
            blockchain=blockchain,
            number_of_blocks_to_add=number_of_blocks_to_add,
            clamp_factor=clamp_factor,
            smallest_bit_difficulty=smallest_bit_difficulty,
        )

        log_blockchain_statistics(logger, blockchain)
        plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity

        log_level_counter_handler.print_log_counts()

        # Record the end time
        end_time = time.time()

        # Calculate and print the execution time
        execution_time = end_time - start_time
        logger.info(f"Program execution time: {execution_time:.2f} seconds")

        # # Display a confirmation dialog
        # messagebox.showinfo("Blockchain Run", "The blockchain has been successfully run.")

    def exit_app(self):
        self.root.quit()

def open_config_ui():
    """Function to initialize and run the configuration UI."""
    root = tk.Tk()
    app = BlockchainConfigUI(root)
    root.mainloop()
    # exit(0)

