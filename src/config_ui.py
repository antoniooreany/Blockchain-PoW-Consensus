# # # # # # # # # # # import tkinter as tk
# # # # # # # # # # # from tkinter import messagebox
# # # # # # # # # # #
# # # # # # # # # # # # Default values
# # # # # # # # # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # # # # # # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # # # # # # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # # # # # # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # # # # # # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # # # # # # # #
# # # # # # # # # # #
# # # # # # # # # # # class BlockchainConfigUI:
# # # # # # # # # # #     def __init__(self, root):
# # # # # # # # # # #         self.root = root
# # # # # # # # # # #         self.root.title("Blockchain Configuration")
# # # # # # # # # # #
# # # # # # # # # # #         # Labels and entry fields for constants
# # # # # # # # # # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # # # # # # # # # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # # # # # # # # # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # # # # # # # # # #
# # # # # # # # # # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # # # # # # # # # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # # # # # # # # # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # # # # # # # # # #
# # # # # # # # # # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # # # # # # # # # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # # # # # # # # # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # # # # # # # # # #
# # # # # # # # # # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # # # # # # # # # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # # # # # # # # # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # # # # # # # # # #
# # # # # # # # # # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # # # # # # # # # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # # # # # # # # # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # # # # # # # # # #
# # # # # # # # # # #         # Save button
# # # # # # # # # # #         tk.Button(root, text="Save Configuration", command=self.save_config).grid(row=5, column=0, columnspan=2)
# # # # # # # # # # #
# # # # # # # # # # #     def save_config(self):
# # # # # # # # # # #         # Collect values from the UI and save them in a dictionary or directly use them to configure the blockchain
# # # # # # # # # # #         config = {
# # # # # # # # # # #             "initial_bit_difficulty": self.initial_bit_difficulty.get(),
# # # # # # # # # # #             "adjustment_block_interval": self.adjustment_block_interval.get(),
# # # # # # # # # # #             "target_block_mining_time": self.target_block_mining_time.get(),
# # # # # # # # # # #             "clamp_factor": self.clamp_factor.get(),
# # # # # # # # # # #             "smallest_bit_difficulty": self.smallest_bit_difficulty.get(),
# # # # # # # # # # #         }
# # # # # # # # # # #
# # # # # # # # # # #         # Display a confirmation dialog
# # # # # # # # # # #         messagebox.showinfo("Configuration Saved", "The configuration has been successfully saved.")
# # # # # # # # # # #
# # # # # # # # # # #         # Here, you would typically pass `config` to the rest of your application.
# # # # # # # # # # #         print("Configuration:", config)  # For demonstration purposes only
# # # # # # # # # # #
# # # # # # # # # # #
# # # # # # # # # # # def open_config_ui():
# # # # # # # # # # #     """Function to initialize and run the configuration UI."""
# # # # # # # # # # #     root = tk.Tk()
# # # # # # # # # # #     app = BlockchainConfigUI(root)
# # # # # # # # # # #     root.mainloop()
# # # # # # # # # # #
# # # # # # # # # #
# # # # # # # # # #
# # # # # # # # # # import tkinter as tk
# # # # # # # # # # from tkinter import messagebox
# # # # # # # # # # import logging
# # # # # # # # # # import time
# # # # # # # # # # from blockchain import Blockchain
# # # # # # # # # # from helpers import add_blocks
# # # # # # # # # # from logger_singleton import LoggerSingleton
# # # # # # # # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # # # # # # # from plotting import plot_blockchain_statistics
# # # # # # # # # #
# # # # # # # # # # # Default values
# # # # # # # # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # # # # # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # # # # # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # # # # # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # # # # # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # # # # # # # DEFAULT_NUMBER_BLOCKS_TO_ADD = 10000
# # # # # # # # # #
# # # # # # # # # # class BlockchainConfigUI:
# # # # # # # # # #     def __init__(self, root):
# # # # # # # # # #         self.root = root
# # # # # # # # # #         self.root.title("Blockchain Configuration")
# # # # # # # # # #
# # # # # # # # # #         # Labels and entry fields for constants
# # # # # # # # # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # # # # # # # # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # # # # # # # # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # # # # # # # # #
# # # # # # # # # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # # # # # # # # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # # # # # # # # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # # # # # # # # #
# # # # # # # # # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # # # # # # # # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # # # # # # # # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # # # # # # # # #
# # # # # # # # # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # # # # # # # # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # # # # # # # # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # # # # # # # # #
# # # # # # # # # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # # # # # # # # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # # # # # # # # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # # # # # # # # #
# # # # # # # # # #         # Save button
# # # # # # # # # #         tk.Button(root, text="Save Configuration", command=self.save_config).grid(row=5, column=0, columnspan=2)
# # # # # # # # # #
# # # # # # # # # #         # Run Blockchain button
# # # # # # # # # #         tk.Button(root, text="Run Blockchain", command=self.run_blockchain).grid(row=6, column=0, columnspan=2)
# # # # # # # # # #
# # # # # # # # # #     def save_config(self):
# # # # # # # # # #         # Collect values from the UI and save them in a dictionary or directly use them to configure the blockchain
# # # # # # # # # #         config = {
# # # # # # # # # #             "initial_bit_difficulty": self.initial_bit_difficulty.get(),
# # # # # # # # # #             "adjustment_block_interval": self.adjustment_block_interval.get(),
# # # # # # # # # #             "target_block_mining_time": self.target_block_mining_time.get(),
# # # # # # # # # #             "clamp_factor": self.clamp_factor.get(),
# # # # # # # # # #             "smallest_bit_difficulty": self.smallest_bit_difficulty.get(),
# # # # # # # # # #         }
# # # # # # # # # #
# # # # # # # # # #         # Display a confirmation dialog
# # # # # # # # # #         messagebox.showinfo("Configuration Saved", "The configuration has been successfully saved.")
# # # # # # # # # #
# # # # # # # # # #         # Here, you would typically pass `config` to the rest of your application.
# # # # # # # # # #         print("Configuration:", config)  # For demonstration purposes only
# # # # # # # # # #
# # # # # # # # # #     def run_blockchain(self):
# # # # # # # # # #         # Collect values from the UI
# # # # # # # # # #         initial_bit_difficulty = self.initial_bit_difficulty.get()
# # # # # # # # # #         adjustment_block_interval = self.adjustment_block_interval.get()
# # # # # # # # # #         target_block_mining_time = self.target_block_mining_time.get()
# # # # # # # # # #         clamp_factor = self.clamp_factor.get()
# # # # # # # # # #         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
# # # # # # # # # #
# # # # # # # # # #         # Record the start time
# # # # # # # # # #         start_time = time.time()
# # # # # # # # # #
# # # # # # # # # #         # Set the logging level to INFO (or WARNING to reduce more output)
# # # # # # # # # #         logging.getLogger('matplotlib').setLevel(logging.INFO)
# # # # # # # # # #
# # # # # # # # # #         logger = LoggerSingleton.get_instance().logger
# # # # # # # # # #
# # # # # # # # # #         # Add custom handler to track errors and critical issues
# # # # # # # # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # # # # # # # #         logger.addHandler(log_level_counter_handler)
# # # # # # # # # #
# # # # # # # # # #         blockchain = Blockchain(
# # # # # # # # # #             initial_bit_difficulty=initial_bit_difficulty,
# # # # # # # # # #             adjustment_block_interval=adjustment_block_interval,
# # # # # # # # # #             target_block_mining_time=target_block_mining_time,
# # # # # # # # # #         )
# # # # # # # # # #
# # # # # # # # # #         add_blocks(
# # # # # # # # # #             blockchain=blockchain,
# # # # # # # # # #             number_of_blocks_to_add=DEFAULT_NUMBER_BLOCKS_TO_ADD,
# # # # # # # # # #             clamp_factor=clamp_factor,
# # # # # # # # # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # # # # # # # # #         )
# # # # # # # # # #
# # # # # # # # # #         log_blockchain_statistics(logger, blockchain)
# # # # # # # # # #         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
# # # # # # # # # #
# # # # # # # # # #         log_level_counter_handler.print_log_counts()
# # # # # # # # # #
# # # # # # # # # #         # Record the end time
# # # # # # # # # #         end_time = time.time()
# # # # # # # # # #
# # # # # # # # # #         # Calculate and print the execution time
# # # # # # # # # #         execution_time = end_time - start_time
# # # # # # # # # #         logger.info(f"Program execution time: {execution_time:.2f} seconds")
# # # # # # # # # #
# # # # # # # # # #         # Display a confirmation dialog
# # # # # # # # # #         messagebox.showinfo("Blockchain Run", "The blockchain has been successfully run.")
# # # # # # # # # #
# # # # # # # # # # def open_config_ui():
# # # # # # # # # #     """Function to initialize and run the configuration UI."""
# # # # # # # # # #     root = tk.Tk()
# # # # # # # # # #     app = BlockchainConfigUI(root)
# # # # # # # # # #     root.mainloop()
# # # # # # # # # #
# # # # # # # # # #
# # # # # # # # #
# # # # # # # # #
# # # # # # # # # import tkinter as tk
# # # # # # # # # from tkinter import messagebox
# # # # # # # # # import logging
# # # # # # # # # import time
# # # # # # # # # from blockchain import Blockchain
# # # # # # # # # from helpers import add_blocks
# # # # # # # # # from logger_singleton import LoggerSingleton
# # # # # # # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # # # # # # from plotting import plot_blockchain_statistics
# # # # # # # # #
# # # # # # # # # # Default values
# # # # # # # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # # # # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # # # # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # # # # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # # # # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # # # # # # DEFAULT_NUMBER_BLOCKS_TO_ADD = 100
# # # # # # # # #
# # # # # # # # # class BlockchainConfigUI:
# # # # # # # # #     def __init__(self, root):
# # # # # # # # #         self.root = root
# # # # # # # # #         self.root.title("Blockchain Configuration")
# # # # # # # # #
# # # # # # # # #         # Labels and entry fields for constants
# # # # # # # # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # # # # # # # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # # # # # # # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # # # # # # # #
# # # # # # # # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # # # # # # # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # # # # # # # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # # # # # # # #
# # # # # # # # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # # # # # # # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # # # # # # # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # # # # # # # #
# # # # # # # # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # # # # # # # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # # # # # # # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # # # # # # # #
# # # # # # # # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # # # # # # # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # # # # # # # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # # # # # # # #
# # # # # # # # #         # Run Blockchain button
# # # # # # # # #         tk.Button(root, text="Run Blockchain", command=self.run_blockchain).grid(row=5, column=0, columnspan=2)
# # # # # # # # #
# # # # # # # # #     def run_blockchain(self):
# # # # # # # # #         # Collect values from the UI
# # # # # # # # #         initial_bit_difficulty = self.initial_bit_difficulty.get()
# # # # # # # # #         adjustment_block_interval = self.adjustment_block_interval.get()
# # # # # # # # #         target_block_mining_time = self.target_block_mining_time.get()
# # # # # # # # #         clamp_factor = self.clamp_factor.get()
# # # # # # # # #         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
# # # # # # # # #
# # # # # # # # #         # Record the start time
# # # # # # # # #         start_time = time.time()
# # # # # # # # #
# # # # # # # # #         # Set the logging level to INFO (or WARNING to reduce more output)
# # # # # # # # #         logging.getLogger('matplotlib').setLevel(logging.INFO)
# # # # # # # # #
# # # # # # # # #         logger = LoggerSingleton.get_instance().logger
# # # # # # # # #
# # # # # # # # #         # Add custom handler to track errors and critical issues
# # # # # # # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # # # # # # #         logger.addHandler(log_level_counter_handler)
# # # # # # # # #
# # # # # # # # #         blockchain = Blockchain(
# # # # # # # # #             initial_bit_difficulty=initial_bit_difficulty,
# # # # # # # # #             adjustment_block_interval=adjustment_block_interval,
# # # # # # # # #             target_block_mining_time=target_block_mining_time,
# # # # # # # # #         )
# # # # # # # # #
# # # # # # # # #         add_blocks(
# # # # # # # # #             blockchain=blockchain,
# # # # # # # # #             number_of_blocks_to_add=DEFAULT_NUMBER_BLOCKS_TO_ADD,
# # # # # # # # #             clamp_factor=clamp_factor,
# # # # # # # # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # # # # # # # #         )
# # # # # # # # #
# # # # # # # # #         log_blockchain_statistics(logger, blockchain)
# # # # # # # # #         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
# # # # # # # # #
# # # # # # # # #         log_level_counter_handler.print_log_counts()
# # # # # # # # #
# # # # # # # # #         # Record the end time
# # # # # # # # #         end_time = time.time()
# # # # # # # # #
# # # # # # # # #         # Calculate and print the execution time
# # # # # # # # #         execution_time = end_time - start_time
# # # # # # # # #         logger.info(f"Program execution time: {execution_time:.2f} seconds")
# # # # # # # # #
# # # # # # # # #         # # Display a confirmation dialog
# # # # # # # # #         # messagebox.showinfo("Blockchain Run")
# # # # # # # # #
# # # # # # # # # def open_config_ui():
# # # # # # # # #     """Function to initialize and run the configuration UI."""
# # # # # # # # #     root = tk.Tk()
# # # # # # # # #     app = BlockchainConfigUI(root)
# # # # # # # # #     root.mainloop()
# # # # # # # # #
# # # # # # # #
# # # # # # # #
# # # # # # # #
# # # # # # # # import tkinter as tk
# # # # # # # # from tkinter import messagebox
# # # # # # # # import logging
# # # # # # # # import time
# # # # # # # # from blockchain import Blockchain
# # # # # # # # from helpers import add_blocks
# # # # # # # # from logger_singleton import LoggerSingleton
# # # # # # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # # # # # from plotting import plot_blockchain_statistics
# # # # # # # #
# # # # # # # # # Default values
# # # # # # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # # # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # # # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # # # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # # # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # # # # # DEFAULT_NUMBER_BLOCKS_TO_ADD = 100
# # # # # # # #
# # # # # # # # class BlockchainConfigUI:
# # # # # # # #     def __init__(self, root):
# # # # # # # #         self.root = root
# # # # # # # #         self.root.title("Blockchain Configuration")
# # # # # # # #
# # # # # # # #         # Labels and entry fields for constants
# # # # # # # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # # # # # # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # # # # # # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # # # # # # #
# # # # # # # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # # # # # # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # # # # # # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # # # # # # #
# # # # # # # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # # # # # # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # # # # # # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # # # # # # #
# # # # # # # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # # # # # # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # # # # # # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # # # # # # #
# # # # # # # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # # # # # # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # # # # # # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # # # # # # #
# # # # # # # #         tk.Label(root, text="Number of Blocks to Add").grid(row=5, column=0)
# # # # # # # #         self.number_of_blocks_to_add = tk.IntVar(value=DEFAULT_NUMBER_BLOCKS_TO_ADD)
# # # # # # # #         tk.Entry(root, textvariable=self.number_of_blocks_to_add).grid(row=5, column=1)
# # # # # # # #
# # # # # # # #         # Run Blockchain button
# # # # # # # #         tk.Button(root, text="Run Blockchain", command=self.run_blockchain).grid(row=6, column=0, columnspan=2)
# # # # # # # #
# # # # # # # #     def run_blockchain(self):
# # # # # # # #         # Collect values from the UI
# # # # # # # #         initial_bit_difficulty = self.initial_bit_difficulty.get()
# # # # # # # #         adjustment_block_interval = self.adjustment_block_interval.get()
# # # # # # # #         target_block_mining_time = self.target_block_mining_time.get()
# # # # # # # #         clamp_factor = self.clamp_factor.get()
# # # # # # # #         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
# # # # # # # #         number_of_blocks_to_add = self.number_of_blocks_to_add.get()
# # # # # # # #
# # # # # # # #         # Record the start time
# # # # # # # #         start_time = time.time()
# # # # # # # #
# # # # # # # #         # Set the logging level to INFO (or WARNING to reduce more output)
# # # # # # # #         logging.getLogger('matplotlib').setLevel(logging.INFO)
# # # # # # # #
# # # # # # # #         logger = LoggerSingleton.get_instance().logger
# # # # # # # #
# # # # # # # #         # Add custom handler to track errors and critical issues
# # # # # # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # # # # # #         logger.addHandler(log_level_counter_handler)
# # # # # # # #
# # # # # # # #         blockchain = Blockchain(
# # # # # # # #             initial_bit_difficulty=initial_bit_difficulty,
# # # # # # # #             adjustment_block_interval=adjustment_block_interval,
# # # # # # # #             target_block_mining_time=target_block_mining_time,
# # # # # # # #         )
# # # # # # # #
# # # # # # # #         add_blocks(
# # # # # # # #             blockchain=blockchain,
# # # # # # # #             number_of_blocks_to_add=number_of_blocks_to_add,
# # # # # # # #             clamp_factor=clamp_factor,
# # # # # # # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # # # # # # #         )
# # # # # # # #
# # # # # # # #         log_blockchain_statistics(logger, blockchain)
# # # # # # # #         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
# # # # # # # #
# # # # # # # #         log_level_counter_handler.print_log_counts()
# # # # # # # #
# # # # # # # #         # Record the end time
# # # # # # # #         end_time = time.time()
# # # # # # # #
# # # # # # # #         # Calculate and print the execution time
# # # # # # # #         execution_time = end_time - start_time
# # # # # # # #         logger.info(f"Program execution time: {execution_time:.2f} seconds")
# # # # # # # #
# # # # # # # #         # # Display a confirmation dialog
# # # # # # # #         # messagebox.showinfo("Blockchain Run", "The blockchain has been successfully run.")
# # # # # # # #
# # # # # # # # def open_config_ui():
# # # # # # # #     """Function to initialize and run the configuration UI."""
# # # # # # # #     root = tk.Tk()
# # # # # # # #     app = BlockchainConfigUI(root)
# # # # # # # #     root.mainloop()
# # # # # # # #     exit(0) # todo exit(0) is added to prevent the error: _tkinter.TclError: can't invoke "event" command: application has been destroyed
# # # # # # # #
# # # # # # #
# # # # # # #
# # # # # # # import tkinter as tk
# # # # # # # from tkinter import messagebox
# # # # # # # import logging
# # # # # # # import time
# # # # # # # from blockchain import Blockchain
# # # # # # # from helpers import add_blocks
# # # # # # # from logger_singleton import LoggerSingleton
# # # # # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # # # # from plotting import plot_blockchain_statistics
# # # # # # #
# # # # # # # # Default values
# # # # # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # # # # DEFAULT_NUMBER_BLOCKS_TO_ADD = 100
# # # # # # #
# # # # # # # class BlockchainConfigUI:
# # # # # # #     def __init__(self, root):
# # # # # # #         self.root = root
# # # # # # #         self.root.title("Blockchain Configuration")
# # # # # # #
# # # # # # #         # Labels and entry fields for constants
# # # # # # #         tk.Label(root, text="Initial Bit Difficulty").grid(row=0, column=0)
# # # # # # #         self.initial_bit_difficulty = tk.DoubleVar(value=DEFAULT_INITIAL_BIT_DIFFICULTY)
# # # # # # #         tk.Entry(root, textvariable=self.initial_bit_difficulty).grid(row=0, column=1)
# # # # # # #
# # # # # # #         tk.Label(root, text="Adjustment Block Interval").grid(row=1, column=0)
# # # # # # #         self.adjustment_block_interval = tk.IntVar(value=DEFAULT_ADJUSTMENT_BLOCK_INTERVAL)
# # # # # # #         tk.Entry(root, textvariable=self.adjustment_block_interval).grid(row=1, column=1)
# # # # # # #
# # # # # # #         tk.Label(root, text="Target Block Mining Time (seconds)").grid(row=2, column=0)
# # # # # # #         self.target_block_mining_time = tk.DoubleVar(value=DEFAULT_TARGET_BLOCK_MINING_TIME)
# # # # # # #         tk.Entry(root, textvariable=self.target_block_mining_time).grid(row=2, column=1)
# # # # # # #
# # # # # # #         tk.Label(root, text="Clamp Factor").grid(row=3, column=0)
# # # # # # #         self.clamp_factor = tk.DoubleVar(value=DEFAULT_CLAMP_FACTOR)
# # # # # # #         tk.Entry(root, textvariable=self.clamp_factor).grid(row=3, column=1)
# # # # # # #
# # # # # # #         tk.Label(root, text="Smallest Bit Difficulty").grid(row=4, column=0)
# # # # # # #         self.smallest_bit_difficulty = tk.DoubleVar(value=DEFAULT_SMALLEST_BIT_DIFFICULTY)
# # # # # # #         tk.Entry(root, textvariable=self.smallest_bit_difficulty).grid(row=4, column=1)
# # # # # # #
# # # # # # #         tk.Label(root, text="Number of Blocks to Add").grid(row=5, column=0)
# # # # # # #         self.number_of_blocks_to_add = tk.IntVar(value=DEFAULT_NUMBER_BLOCKS_TO_ADD)
# # # # # # #         tk.Entry(root, textvariable=self.number_of_blocks_to_add).grid(row=5, column=1)
# # # # # # #
# # # # # # #         # Run Blockchain button
# # # # # # #         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
# # # # # # #         self.run_button.grid(row=6, column=0, columnspan=2)
# # # # # # #         self.run_button.focus_set()
# # # # # # #
# # # # # # #         # Bind Enter and Space keys to the Run Blockchain button, make it pressed when the keys are pressed
# # # # # # #         # self.root.bind('<Return>', lambda event: self.run_blockchain())
# # # # # # #         # self.root.bind('<space>', lambda event: self.run_blockchain())
# # # # # # #         self.run_button.bind('<Return>', lambda event: self.run_blockchain(), add='+')
# # # # # # #         self.run_button.bind('<space>', lambda event: self.run_blockchain(), add='+')
# # # # # # #
# # # # # # #     def run_blockchain(self):
# # # # # # #         # Collect values from the UI
# # # # # # #         initial_bit_difficulty = self.initial_bit_difficulty.get()
# # # # # # #         adjustment_block_interval = self.adjustment_block_interval.get()
# # # # # # #         target_block_mining_time = self.target_block_mining_time.get()
# # # # # # #         clamp_factor = self.clamp_factor.get()
# # # # # # #         smallest_bit_difficulty = self.smallest_bit_difficulty.get()
# # # # # # #         number_of_blocks_to_add = self.number_of_blocks_to_add.get()
# # # # # # #
# # # # # # #         # Record the start time
# # # # # # #         start_time = time.time()
# # # # # # #
# # # # # # #         # Set the logging level to INFO (or WARNING to reduce more output)
# # # # # # #         logging.getLogger('matplotlib').setLevel(logging.INFO)
# # # # # # #
# # # # # # #         logger = LoggerSingleton.get_instance().logger
# # # # # # #
# # # # # # #         # Add custom handler to track errors and critical issues
# # # # # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # # # # #         logger.addHandler(log_level_counter_handler)
# # # # # # #
# # # # # # #         blockchain = Blockchain(
# # # # # # #             initial_bit_difficulty=initial_bit_difficulty,
# # # # # # #             adjustment_block_interval=adjustment_block_interval,
# # # # # # #             target_block_mining_time=target_block_mining_time,
# # # # # # #         )
# # # # # # #
# # # # # # #         add_blocks(
# # # # # # #             blockchain=blockchain,
# # # # # # #             number_of_blocks_to_add=number_of_blocks_to_add,
# # # # # # #             clamp_factor=clamp_factor,
# # # # # # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # # # # # #         )
# # # # # # #
# # # # # # #         log_blockchain_statistics(logger, blockchain)
# # # # # # #         plot_blockchain_statistics({2: blockchain})  # Assuming base 2 for simplicity
# # # # # # #
# # # # # # #         log_level_counter_handler.print_log_counts()
# # # # # # #
# # # # # # #         # Record the end time
# # # # # # #         end_time = time.time()
# # # # # # #
# # # # # # #         # Calculate and print the execution time
# # # # # # #         execution_time = end_time - start_time
# # # # # # #         logger.info(f"Program execution time: {execution_time:.2f} seconds")
# # # # # # #
# # # # # # #         # # Display a confirmation dialog
# # # # # # #         # messagebox.showinfo("Blockchain Run", "The blockchain has been successfully run.")
# # # # # # #
# # # # # # # def open_config_ui():
# # # # # # #     """Function to initialize and run the configuration UI."""
# # # # # # #     root = tk.Tk()
# # # # # # #     app = BlockchainConfigUI(root)
# # # # # # #     root.mainloop()
# # # # # # #     exit(0)
# # # # # # #
# # # # # #
# # # # # #
# # # # # # import tkinter as tk
# # # # # # from tkinter import messagebox
# # # # # # import logging
# # # # # # import time
# # # # # # from blockchain import Blockchain
# # # # # # from helpers import add_blocks
# # # # # # from logger_singleton import LoggerSingleton
# # # # # # from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
# # # # # #     SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
# # # # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # # # from plotting import plot_blockchain_statistics
# # # # # #
# # # # # # # # Default values
# # # # # # # DEFAULT_INITIAL_BIT_DIFFICULTY = 16.0
# # # # # # # DEFAULT_ADJUSTMENT_BLOCK_INTERVAL = 10
# # # # # # # DEFAULT_TARGET_BLOCK_MINING_TIME = 0.01
# # # # # # # DEFAULT_CLAMP_FACTOR = 2.0
# # # # # # # DEFAULT_SMALLEST_BIT_DIFFICULTY = 4.0
# # # # # # # DEFAULT_NUMBER_BLOCKS_TO_ADD = 30
# # # # # #
# # # # # # class BlockchainConfigUI:
# # # # # #
# # # # # #     def __init__(self, root):
# # # # # #         self.root = root
# # # # # #         self.root.title("Blockchain Configuration")
# # # # # #         self.root.focus_force()  # Make the window focused
# # # # # #         self.root.attributes('-fullscreen', True)  # Allow the window to go behind others
# # # # # #
# # # # # #         # Define labels and entry fields with standardized variable names
# # # # # #         config_params = [
# # # # # #             ("Initial Bit Difficulty, bits", tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY)),
# # # # # #             ("Target Block Mining Time, seconds", tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME)),
# # # # # #             ("Adjustment Block Interval, blocks", tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL)),
# # # # # #             ("Clamp Factor, bits", tk.DoubleVar(value=CLAMP_FACTOR)),
# # # # # #             ("Smallest Bit Difficulty, bits", tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY)),
# # # # # #             ("Number of Blocks to Add, blocks", tk.IntVar(value=NUMBER_BLOCKS_TO_ADD)),
# # # # # #             ("Slice Factor", tk.DoubleVar(value=SLICE_FACTOR)),
# # # # # #             ("Number of Block Slices, blocks", tk.IntVar(value=NUMBER_BLOCKS_SLICE))
# # # # # #         ]
# # # # # #
# # # # # #         for idx, (label_text, var) in enumerate(config_params):
# # # # # #             tk.Label(root, text=label_text).grid(row=idx, column=0)
# # # # # #             tk.Entry(root, textvariable=var).grid(row=idx, column=1)
# # # # # #
# # # # # #         # Run Blockchain button
# # # # # #         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
# # # # # #         self.run_button.grid(row=len(config_params), column=0, columnspan=2)
# # # # # #         self.run_button.focus_set()
# # # # # #
# # # # # #         # Exit button
# # # # # #         self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
# # # # # #         self.exit_button.grid(row=len(config_params) + 1, column=0, columnspan=2)
# # # # # #
# # # # # #         # Bind Enter and Space keys to the Run Blockchain button
# # # # # #         self.run_button.bind('<Return>', lambda event: self.run_blockchain())
# # # # # #         self.run_button.bind('<space>', lambda event: self.run_blockchain())
# # # # # #
# # # # # #     def run_blockchain(self, event=None):
# # # # # #         # Disable the button to prevent multiple clicks
# # # # # #         self.run_button.config(state=tk.DISABLED)
# # # # # #
# # # # # #         start_time = time.time()
# # # # # #
# # # # # #         logger = LoggerSingleton.get_instance().logger
# # # # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # # # #         logger.addHandler(log_level_counter_handler)
# # # # # #
# # # # # #         blockchain = Blockchain(
# # # # # #             initial_bit_difficulty=INITIAL_BIT_DIFFICULTY,
# # # # # #             adjustment_block_interval=ADJUSTMENT_BLOCK_INTERVAL,
# # # # # #             target_block_mining_time=TARGET_BLOCK_MINING_TIME,
# # # # # #         )
# # # # # #
# # # # # #         add_blocks(
# # # # # #             blockchain=blockchain,
# # # # # #             number_of_blocks_to_add=NUMBER_BLOCKS_TO_ADD,
# # # # # #             clamp_factor=CLAMP_FACTOR,
# # # # # #             smallest_bit_difficulty=SMALLEST_BIT_DIFFICULTY,
# # # # # #         )
# # # # # #
# # # # # #         log_blockchain_statistics(logger, blockchain)
# # # # # #         plot_blockchain_statistics(blockchain)
# # # # # #
# # # # # #         log_level_counter_handler.print_log_counts()
# # # # # #
# # # # # #         end_time = time.time()
# # # # # #         execution_time = end_time - start_time
# # # # # #         logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
# # # # # #
# # # # # #         # Re-enable the button after the blockchain has been run
# # # # # #         self.run_button.config(state=tk.NORMAL)
# # # # # #
# # # # # #     def exit_app(self):
# # # # # #         self.root.quit()
# # # # # #
# # # # # # def config_ui():
# # # # # #     """Function to initialize and run the configuration UI."""
# # # # # #     root = tk.Tk()
# # # # # #     app = BlockchainConfigUI(root)
# # # # # #     root.mainloop()
# # # # # #
# # # # #
# # # # #
# # # # # import tkinter as tk
# # # # # from tkinter import messagebox
# # # # # import logging
# # # # # import time
# # # # # from blockchain import Blockchain
# # # # # from helpers import add_blocks
# # # # # from logger_singleton import LoggerSingleton
# # # # # from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
# # # # #     SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
# # # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # # from plotting import plot_blockchain_statistics
# # # # #
# # # # # class BlockchainConfigUI:
# # # # #
# # # # #     def __init__(self, root):
# # # # #         self.root = root
# # # # #         self.root.title("Blockchain Configuration")
# # # # #         self.root.focus_force()  # Make the window focused
# # # # #         self.root.attributes('-fullscreen', True)  # Allow the window to go behind others
# # # # #
# # # # #         # Define labels and entry fields with standardized variable names
# # # # #         config_params = [
# # # # #             ("Initial Bit Difficulty, bits", tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY)),
# # # # #             ("Target Block Mining Time, seconds", tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME)),
# # # # #             ("Adjustment Block Interval, blocks", tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL)),
# # # # #             ("Clamp Factor, bits", tk.DoubleVar(value=CLAMP_FACTOR)),
# # # # #             ("Smallest Bit Difficulty, bits", tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY)),
# # # # #             ("Number of Blocks to Add, blocks", tk.IntVar(value=NUMBER_BLOCKS_TO_ADD)),
# # # # #             ("Slice Factor", tk.DoubleVar(value=SLICE_FACTOR)),
# # # # #             ("Number of Block Slices, blocks", tk.IntVar(value=NUMBER_BLOCKS_SLICE))
# # # # #         ]
# # # # #
# # # # #         for idx, (label_text, var) in enumerate(config_params):
# # # # #             tk.Label(root, text=label_text).grid(row=idx, column=0)
# # # # #             tk.Entry(root, textvariable=var).grid(row=idx, column=1)
# # # # #
# # # # #         # Run Blockchain button
# # # # #         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
# # # # #         self.run_button.grid(row=len(config_params), column=0, columnspan=2)
# # # # #         self.run_button.focus_set()
# # # # #
# # # # #         # Exit button
# # # # #         self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
# # # # #         self.exit_button.grid(row=len(config_params) + 1, column=0, columnspan=2)
# # # # #
# # # # #         # # Bind Enter and Space keys to the Run Blockchain button
# # # # #         # self.run_button.bind('<Return>', lambda event: self.run_blockchain())
# # # # #         # self.run_button.bind('<space>', lambda event: self.run_blockchain())
# # # # #
# # # # #         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
# # # # #         self.run_button.grid(row=len(config_params), column=0, columnspan=2)
# # # # #         self.run_button.focus_set()
# # # # #
# # # # #
# # # # #     def run_blockchain(self, event=None):
# # # # #         # # Disable the button to prevent multiple clicks
# # # # #         # self.run_button.config(state=tk.DISABLED)
# # # # #
# # # # #         start_time = time.time()
# # # # #
# # # # #         logger = LoggerSingleton.get_instance().logger
# # # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # # #         logger.addHandler(log_level_counter_handler)
# # # # #
# # # # #         blockchain = Blockchain(
# # # # #             initial_bit_difficulty=INITIAL_BIT_DIFFICULTY,
# # # # #             adjustment_block_interval=ADJUSTMENT_BLOCK_INTERVAL,
# # # # #             target_block_mining_time=TARGET_BLOCK_MINING_TIME,
# # # # #         )
# # # # #
# # # # #         add_blocks(
# # # # #             blockchain=blockchain,
# # # # #             number_of_blocks_to_add=NUMBER_BLOCKS_TO_ADD,
# # # # #             clamp_factor=CLAMP_FACTOR,
# # # # #             smallest_bit_difficulty=SMALLEST_BIT_DIFFICULTY,
# # # # #         )
# # # # #
# # # # #         log_blockchain_statistics(logger, blockchain)
# # # # #         plot_blockchain_statistics(blockchain)
# # # # #
# # # # #         log_level_counter_handler.print_log_counts()
# # # # #
# # # # #         end_time = time.time()
# # # # #         execution_time = end_time - start_time
# # # # #         logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
# # # # #
# # # # #         # # Re-enable the button after the blockchain has been run
# # # # #         # self.run_button.config(state=tk.NORMAL)
# # # # #
# # # # #     def exit_app(self):
# # # # #         self.root.quit()
# # # # #
# # # # # def config_ui():
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
# # # # from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
# # # #     SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
# # # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # # from plotting import plot_blockchain_statistics
# # # #
# # # # class BlockchainConfigUI:
# # # #
# # # #     def __init__(self, root):
# # # #         self.root = root
# # # #         self.root.title("Blockchain Configuration")
# # # #         self.root.focus_force()  # Make the window focused
# # # #         self.root.attributes('-fullscreen', True)  # Allow the window to go behind others
# # # #
# # # #         # Define labels and entry fields with standardized variable names
# # # #         self.config_params = {
# # # #             "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
# # # #             "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
# # # #             "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
# # # #             "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
# # # #             "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
# # # #             "number_of_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
# # # #             "slice_factor": tk.DoubleVar(value=SLICE_FACTOR),
# # # #             "number_of_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
# # # #         }
# # # #
# # # #         for idx, (label_text, var) in enumerate(self.config_params.items()):
# # # #             tk.Label(root, text=label_text.replace('_', ' ').title()).grid(row=idx, column=0)
# # # #             tk.Entry(root, textvariable=var).grid(row=idx, column=1)
# # # #
# # # #         # Run Blockchain button
# # # #         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
# # # #         self.run_button.grid(row=len(self.config_params), column=0, columnspan=2)
# # # #         self.run_button.focus_set()
# # # #
# # # #         # Exit button
# # # #         self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
# # # #         self.exit_button.grid(row=len(self.config_params) + 1, column=0, columnspan=2)
# # # #
# # # #     def run_blockchain(self, event=None):
# # # #         # Disable the button to prevent multiple clicks
# # # #         self.run_button.config(state=tk.DISABLED)
# # # #
# # # #         start_time = time.time()
# # # #
# # # #         logger = LoggerSingleton.get_instance().logger
# # # #         log_level_counter_handler = LogLevelCounterHandler()
# # # #         logger.addHandler(log_level_counter_handler)
# # # #
# # # #         # Collect values from the UI
# # # #         initial_bit_difficulty = self.config_params["initial_bit_difficulty"].get()
# # # #         target_block_mining_time = self.config_params["target_block_mining_time"].get()
# # # #         adjustment_block_interval = self.config_params["adjustment_block_interval"].get()
# # # #         clamp_factor = self.config_params["clamp_factor"].get()
# # # #         smallest_bit_difficulty = self.config_params["smallest_bit_difficulty"].get()
# # # #         number_of_blocks_to_add = self.config_params["number_of_blocks_to_add"].get()
# # # #         slice_factor = self.config_params["slice_factor"].get()
# # # #
# # # #         blockchain = Blockchain(
# # # #             initial_bit_difficulty=initial_bit_difficulty,
# # # #             adjustment_block_interval=adjustment_block_interval,
# # # #             target_block_mining_time=target_block_mining_time,
# # # #         )
# # # #
# # # #         add_blocks(
# # # #             blockchain=blockchain,
# # # #             number_of_blocks_to_add=number_of_blocks_to_add,
# # # #             clamp_factor=clamp_factor,
# # # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # # #         )
# # # #
# # # #         log_blockchain_statistics(logger, blockchain)
# # # #         plot_blockchain_statistics(blockchain)
# # # #
# # # #         log_level_counter_handler.print_log_counts()
# # # #
# # # #         end_time = time.time()
# # # #         execution_time = end_time - start_time
# # # #         logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
# # # #
# # # #         # Re-enable the button after the blockchain has been run
# # # #         self.run_button.config(state=tk.NORMAL)
# # # #
# # # #     def exit_app(self):
# # # #         self.root.quit()
# # # #
# # # # def config_ui():
# # # #     """Function to initialize and run the configuration UI."""
# # # #     root = tk.Tk()
# # # #     app = BlockchainConfigUI(root)
# # # #     root.mainloop()
# # #
# # # import tkinter as tk
# # # from tkinter import messagebox
# # # import logging
# # # import time
# # # from blockchain import Blockchain
# # # from helpers import add_blocks
# # # from logger_singleton import LoggerSingleton
# # # from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
# # #     SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
# # # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # # from plotting import plot_blockchain_statistics
# # #
# # # class BlockchainConfigUI:
# # #
# # #     def __init__(self, root):
# # #         self.root = root
# # #         self.root.title("Blockchain Configuration")
# # #         self.root.focus_force()  # Make the window focused
# # #         self.root.attributes('-fullscreen', True)  # Allow the window to go behind others
# # #
# # #         # Define labels and entry fields with standardized variable names
# # #         self.config_params = {
# # #             "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
# # #             "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
# # #             "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
# # #             "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
# # #             "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
# # #             "number_of_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
# # #             "slice_factor": tk.DoubleVar(value=SLICE_FACTOR),
# # #             "number_of_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
# # #         }
# # #
# # #         for idx, (label_text, var) in enumerate(self.config_params.items()):
# # #             tk.Label(root, text=label_text.replace('_', ' ').title()).grid(row=idx, column=0)
# # #             tk.Entry(root, textvariable=var).grid(row=idx, column=1)
# # #
# # #         # Run Blockchain button
# # #         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
# # #         self.run_button.grid(row=len(self.config_params), column=0, columnspan=2)
# # #         self.run_button.focus_set()
# # #
# # #         # Exit button
# # #         self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
# # #         self.exit_button.grid(row=len(self.config_params) + 1, column=0, columnspan=2)
# # #
# # #     def run_blockchain(self, event=None):
# # #         # Disable the button to prevent multiple clicks
# # #         self.run_button.config(state=tk.DISABLED)
# # #
# # #         start_time = time.time()
# # #
# # #         logger = LoggerSingleton.get_instance().logger
# # #         log_level_counter_handler = LogLevelCounterHandler()
# # #         logger.addHandler(log_level_counter_handler)
# # #
# # #         # Collect values from the UI
# # #         initial_bit_difficulty = self.config_params["initial_bit_difficulty"].get()
# # #         target_block_mining_time = self.config_params["target_block_mining_time"].get()
# # #         adjustment_block_interval = self.config_params["adjustment_block_interval"].get()
# # #         clamp_factor = self.config_params["clamp_factor"].get()
# # #         smallest_bit_difficulty = self.config_params["smallest_bit_difficulty"].get()
# # #         number_of_blocks_to_add = self.config_params["number_of_blocks_to_add"].get()
# # #         slice_factor = self.config_params["slice_factor"].get()
# # #         number_of_blocks_slice = self.config_params["number_of_blocks_slice"].get()
# # #
# # #         # Log the collected values
# # #         logger.info(f"Initial Bit Difficulty: {initial_bit_difficulty}")
# # #         logger.info(f"Target Block Mining Time: {target_block_mining_time}")
# # #         logger.info(f"Adjustment Block Interval: {adjustment_block_interval}")
# # #         logger.info(f"Clamp Factor: {clamp_factor}")
# # #         logger.info(f"Smallest Bit Difficulty: {smallest_bit_difficulty}")
# # #         logger.info(f"Number of Blocks to Add: {number_of_blocks_to_add}")
# # #         logger.info(f"Slice Factor: {slice_factor}")
# # #         logger.info(f"Number of Blocks Slice: {number_of_blocks_slice}")
# # #
# # #         blockchain = Blockchain(
# # #             initial_bit_difficulty=initial_bit_difficulty,
# # #             adjustment_block_interval=adjustment_block_interval,
# # #             target_block_mining_time=target_block_mining_time,
# # #         )
# # #
# # #         add_blocks(
# # #             blockchain=blockchain,
# # #             number_of_blocks_to_add=number_of_blocks_to_add,
# # #             clamp_factor=clamp_factor,
# # #             smallest_bit_difficulty=smallest_bit_difficulty,
# # #         )
# # #
# # #         log_blockchain_statistics(logger, blockchain)
# # #         plot_blockchain_statistics(blockchain)
# # #
# # #         log_level_counter_handler.print_log_counts()
# # #
# # #         end_time = time.time()
# # #         execution_time = end_time - start_time
# # #         logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
# # #
# # #         # Re-enable the button after the blockchain has been run
# # #         self.run_button.config(state=tk.NORMAL)
# # #
# # #     def exit_app(self):
# # #         self.root.quit()
# # #
# # # def config_ui():
# # #     """Function to initialize and run the configuration UI."""
# # #     root = tk.Tk()
# # #     app = BlockchainConfigUI(root)
# # #     root.mainloop()
# # #
# #
# # import tkinter as tk
# # from tkinter import messagebox
# # import logging
# # import time
# # from blockchain import Blockchain
# # from helpers import add_blocks
# # from logger_singleton import LoggerSingleton
# # from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
# #     SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
# # from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# # from plotting import plot_blockchain_statistics
# #
# # class BlockchainConfigUI:
# #
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Blockchain Configuration")
# #         self.root.focus_force()  # Make the window focused
# #         self.root.attributes('-fullscreen', True)  # Allow the window to go behind others
# #
# #         # Define labels and entry fields with standardized variable names
# #         self.config_params = {
# #             "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
# #             "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
# #             "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
# #             "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
# #             "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
# #             "number_of_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),  # todo change to number_blocks_to_add
# #             "slice_factor": tk.DoubleVar(value=SLICE_FACTOR),
# #             "number_of_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
# #         }
# #
# #         for idx, (label_text, var) in enumerate(self.config_params.items()):
# #             tk.Label(root, text=label_text.replace('_', ' ').title()).grid(row=idx, column=0)
# #             tk.Entry(root, textvariable=var).grid(row=idx, column=1)
# #
# #         # Run Blockchain button
# #         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
# #         self.run_button.grid(row=len(self.config_params), column=0, columnspan=2)
# #         self.run_button.focus_set()
# #
# #         # Exit button
# #         self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
# #         self.exit_button.grid(row=len(self.config_params) + 1, column=0, columnspan=2)
# #
# #     def run_blockchain(self, event=None):
# #         # Disable the button to prevent multiple clicks
# #         self.run_button.config(state=tk.DISABLED)
# #
# #         start_time = time.time()
# #
# #         logger = LoggerSingleton.get_instance().logger
# #         log_level_counter_handler = LogLevelCounterHandler()
# #         logger.addHandler(log_level_counter_handler)
# #
# #         # Collect values from the UI
# #         initial_bit_difficulty = self.config_params["initial_bit_difficulty"].get()
# #         target_block_mining_time = self.config_params["target_block_mining_time"].get()
# #         adjustment_block_interval = self.config_params["adjustment_block_interval"].get()
# #         clamp_factor = self.config_params["clamp_factor"].get()
# #         smallest_bit_difficulty = self.config_params["smallest_bit_difficulty"].get()
# #         number_of_blocks_to_add = self.config_params["number_of_blocks_to_add"].get()
# #         slice_factor = self.config_params["slice_factor"].get()
# #         number_of_blocks_slice = self.config_params["number_of_blocks_slice"].get()
# #
# #         # Log the collected values
# #         logger.info(f"Initial Bit Difficulty: {initial_bit_difficulty}")
# #         logger.info(f"Target Block Mining Time: {target_block_mining_time}")
# #         logger.info(f"Adjustment Block Interval: {adjustment_block_interval}")
# #         logger.info(f"Clamp Factor: {clamp_factor}")
# #         logger.info(f"Smallest Bit Difficulty: {smallest_bit_difficulty}")
# #         logger.info(f"Number of Blocks to Add: {number_of_blocks_to_add}")
# #         logger.info(f"Slice Factor: {slice_factor}")
# #         logger.info(f"Number of Blocks Slice: {number_of_blocks_slice}")
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
# #         plot_blockchain_statistics(blockchain)
# #
# #         log_level_counter_handler.print_log_counts()
# #
# #         end_time = time.time()
# #         execution_time = end_time - start_time
# #         logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
# #         logger.info(f"")
# #
# #         # Re-enable the button after the blockchain has been run
# #         self.run_button.config(state=tk.NORMAL)
# #
# #     def exit_app(self):
# #         self.root.quit()
# #
# # def config_ui():
# #     """Function to initialize and run the configuration UI."""
# #     root = tk.Tk()
# #     app = BlockchainConfigUI(root)
# #     root.mainloop()
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
# from src.constants import INITIAL_BIT_DIFFICULTY, TARGET_BLOCK_MINING_TIME, ADJUSTMENT_BLOCK_INTERVAL, CLAMP_FACTOR, \
#     SMALLEST_BIT_DIFFICULTY, NUMBER_BLOCKS_TO_ADD, SLICE_FACTOR, NUMBER_BLOCKS_SLICE
# from src.logging_utils import LogLevelCounterHandler, log_blockchain_statistics
# from plotting import plot_blockchain_statistics
#
# class BlockchainConfigUI:
#
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Blockchain Configuration")
#         self.root.focus_force()  # Make the window focused
#         self.root.attributes('-fullscreen', True)  # Allow the window to go behind others
#
#         # Define labels and entry fields with standardized variable names
#         self.config_params = {
#             "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
#             "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
#             "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
#             "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
#             "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
#             "number_of_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
#             "slice_factor": tk.DoubleVar(value=SLICE_FACTOR),
#             "number_of_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
#         }
#
#         for idx, (label_text, var) in enumerate(self.config_params.items()):
#             tk.Label(root, text=label_text.replace('_', ' ').title()).grid(row=idx, column=0)
#             tk.Entry(root, textvariable=var).grid(row=idx, column=1)
#
#         # Add trace callbacks to update number_of_blocks_slice
#         self.config_params["number_of_blocks_to_add"].trace_add("write", self.update_number_of_blocks_slice)
#         self.config_params["slice_factor"].trace_add("write", self.update_number_of_blocks_slice)
#
#         # Run Blockchain button
#         self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
#         self.run_button.grid(row=len(self.config_params), column=0, columnspan=2)
#         self.run_button.focus_set()
#
#         # Exit button
#         self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
#         self.exit_button.grid(row=len(self.config_params) + 1, column=0, columnspan=2)
#
#     def update_number_of_blocks_slice(self, *args):
#         number_of_blocks_to_add = self.config_params["number_of_blocks_to_add"].get()
#         slice_factor = self.config_params["slice_factor"].get()
#         number_of_blocks_slice = int(round(number_of_blocks_to_add / slice_factor))
#         self.config_params["number_of_blocks_slice"].set(number_of_blocks_slice)
#
#     def run_blockchain(self, event=None):
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
#         number_of_blocks_to_add = self.config_params["number_of_blocks_to_add"].get()
#         slice_factor = self.config_params["slice_factor"].get()
#         number_of_blocks_slice = self.config_params["number_of_blocks_slice"].get()
#
#         # Log the collected values
#         logger.info(f"Initial Bit Difficulty: {initial_bit_difficulty}")
#         logger.info(f"Target Block Mining Time: {target_block_mining_time}")
#         logger.info(f"Adjustment Block Interval: {adjustment_block_interval}")
#         logger.info(f"Clamp Factor: {clamp_factor}")
#         logger.info(f"Smallest Bit Difficulty: {smallest_bit_difficulty}")
#         logger.info(f"Number of Blocks to Add: {number_of_blocks_to_add}")
#         logger.info(f"Slice Factor: {slice_factor}")
#         logger.info(f"Number of Blocks Slice: {number_of_blocks_slice}")
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
#         plot_blockchain_statistics(blockchain)
#
#         log_level_counter_handler.print_log_counts()
#
#         end_time = time.time()
#         execution_time = end_time - start_time
#         logger.info(f"Blockchain execution time: {execution_time:.2f} seconds")
#
#         # Re-enable the button after the blockchain has been run
#         self.run_button.config(state=tk.NORMAL)
#
#     def exit_app(self):
#         self.root.quit()
#
# def config_ui():
#     """Function to initialize and run the configuration UI."""
#     root = tk.Tk()
#     app = BlockchainConfigUI(root)
#     root.mainloop()
#
#
#


import tkinter as tk
from tkinter import messagebox
import logging
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
        self.root.focus_force()  # Make the window focused
        self.root.attributes('-fullscreen', True)  # Allow the window to go behind others

        # Define labels and entry fields with standardized variable names
        self.config_params = {
            "initial_bit_difficulty": tk.DoubleVar(value=INITIAL_BIT_DIFFICULTY),
            "target_block_mining_time": tk.DoubleVar(value=TARGET_BLOCK_MINING_TIME),
            "adjustment_block_interval": tk.IntVar(value=ADJUSTMENT_BLOCK_INTERVAL),
            "clamp_factor": tk.DoubleVar(value=CLAMP_FACTOR),
            "smallest_bit_difficulty": tk.DoubleVar(value=SMALLEST_BIT_DIFFICULTY),
            "number_blocks_to_add": tk.IntVar(value=NUMBER_BLOCKS_TO_ADD),
            "slice_factor": tk.DoubleVar(value=SLICE_FACTOR),
            "number_of_blocks_slice": tk.IntVar(value=NUMBER_BLOCKS_SLICE)
        }

        for idx, (label_text, var) in enumerate(self.config_params.items()):
            tk.Label(root, text=label_text.replace('_', ' ').title()).grid(row=idx, column=0)
            tk.Entry(root, textvariable=var).grid(row=idx, column=1)

        # Add trace callbacks to update number_of_blocks_slice
        self.config_params["number_blocks_to_add"].trace_add("write", self.update_number_of_blocks_slice)
        self.config_params["slice_factor"].trace_add("write", self.update_number_of_blocks_slice)

        # Run Blockchain button
        self.run_button = tk.Button(root, text="Run Blockchain", command=self.run_blockchain)
        self.run_button.grid(row=len(self.config_params), column=0, columnspan=2)
        self.run_button.focus_set()

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=len(self.config_params) + 1, column=0, columnspan=2)

    def update_number_of_blocks_slice(self, *args):
        try:
            number_of_blocks_to_add = self.config_params["number_blocks_to_add"].get()
            slice_factor = self.config_params["slice_factor"].get()
            number_of_blocks_slice = int(number_of_blocks_to_add / slice_factor)
            self.config_params["number_of_blocks_slice"].set(number_of_blocks_slice)
        except (tk.TclError, ZeroDivisionError):
            self.config_params["number_of_blocks_slice"].set(0)

    def run_blockchain(self, event=None):
        # Recalculate number_of_blocks_slice before running the blockchain
        self.update_number_of_blocks_slice()

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
        number_of_blocks_slice = self.config_params["number_of_blocks_slice"].get()

        # Log the collected values
        logger.info(f"Initial Bit Difficulty: {initial_bit_difficulty}")
        logger.info(f"Target Block Mining Time: {target_block_mining_time}")
        logger.info(f"Adjustment Block Interval: {adjustment_block_interval}")
        logger.info(f"Clamp Factor: {clamp_factor}")
        logger.info(f"Smallest Bit Difficulty: {smallest_bit_difficulty}")
        logger.info(f"Number of Blocks to Add: {number_blocks_to_add}")
        logger.info(f"Slice Factor: {slice_factor}")
        logger.info(f"Number of Blocks Slice: {number_of_blocks_slice}")

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
            clamp_factor=clamp_factor,
            smallest_bit_difficulty=smallest_bit_difficulty,
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
