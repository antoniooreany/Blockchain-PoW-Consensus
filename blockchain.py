#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import hashlib
import time

from block import Block


class Blockchain:
    def __init__(self, difficulty):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

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


class ProofOfWork:
    @staticmethod
    def find_nonce(block, difficulty):
        target = '0' * difficulty
        while block.hash[:difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.nonce

    @staticmethod
    def validate_proof(block, difficulty):
        target = '0' * difficulty
        return block.hash[:difficulty] == target
