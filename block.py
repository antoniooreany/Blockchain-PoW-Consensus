#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import time

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.merkle_root) + str(self.previous_hash) + str(self.nonce)).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

    def calculate_merkle_root(self):
        # Placeholder for Merkle root calculation
        return "merkle_root"

    def validate_transactions(self):
        # Placeholder for transaction validation
        return True