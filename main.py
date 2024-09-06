#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a main.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import time
from blockchain import Block, Blockchain

if __name__ == "__main__":
    blockchain = Blockchain(difficulty=4)

    blockchain.add_block(Block(1, time.time(), "Block 1 Data"))
    blockchain.add_block(Block(2, time.time(), "Block 2 Data"))

    print("Blockchain valid?", blockchain.is_chain_valid())

    for block in blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Nonce: {block.nonce}")
