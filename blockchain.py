#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import time

from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self, difficulty):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.nodes = []

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def adjust_difficulty(self):
        # todo Placeholder for difficulty adjustment logic

        pass

    def add_node(self, node):
        self.nodes.append(node)

    def consensus(self):
        # Replace the longest chain with the new one
        if not self.nodes:
            # todo Handle the case where the nodes list is empty
            return False
        if len(self.chain) > len(self.nodes[0].chain):
            self.nodes[0].chain = self.chain
            return True
        return False

    # def mine_pending_transactions(self, miner_address):
    #     # Placeholder for mining pending transactions
    #     reward_transaction = Transaction(
    #         "network", miner_address, 100
    #     )
    #     # Create a new block with the pending transactions and mine it
    #     new_block = Block(
    #         len(self.chain),
    #         time.time(),
    #         self.pending_transactions
    #     )
    #     new_block.mine_block(self.difficulty)
    #     self.pending_transactions = [reward_transaction]
