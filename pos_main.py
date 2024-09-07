#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a pos_main and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import time
import random

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f'Transaction({self.sender} -> {self.receiver}, {self.amount})'


class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.previous_hash}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return f'Block(Index: {self.index}, Transactions: {self.transactions}, Hash: {self.hash})'


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.stakers = {}
        self.transactions = []

    def create_genesis_block(self):
        return Block(0, [], "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def stake(self, node, amount):
        if node not in self.stakers:
            self.stakers[node] = amount
        else:
            self.stakers[node] += amount

    def select_validator(self):
        total_stake = sum(self.stakers.values())
        weighted_nodes = [(node, stake / total_stake) for node, stake in self.stakers.items()]
        chosen = random.choices(
            [node for node, _ in weighted_nodes],
            weights=[weight for _, weight in weighted_nodes],
            k=1
        )[0]
        return chosen

    def validate_and_add_block(self):
        if not self.transactions:
            print("No transactions to validate.")
            return

        validator = self.select_validator()
        print(f"Validator {validator} selected to create the block.")

        new_block = Block(
            index=len(self.chain),
            transactions=self.transactions,
            previous_hash=self.get_last_block().hash
        )

        self.add_block(new_block)
        self.transactions = []

        print(f"Block {new_block.index} has been added by {validator}.")


class Node:
    def __init__(self, name, blockchain):
        self.name = name
        self.blockchain = blockchain

    def stake_coins(self, amount):
        self.blockchain.stake(self.name, amount)

    def create_transaction(self, receiver, amount):
        transaction = Transaction(self.name, receiver, amount)
        self.blockchain.add_transaction(transaction)


# Example Usage
if __name__ == "__main__":
    # Initialize the blockchain
    my_blockchain = Blockchain()

    # Create nodes
    node1 = Node("Node1", my_blockchain)
    node2 = Node("Node2", my_blockchain)

    # Nodes stake coins
    node1.stake_coins(10)
    node2.stake_coins(20)

    # Create transactions
    node1.create_transaction("Node2", 5)
    node2.create_transaction("Node1", 3)

    # Validate and add block to the blockchain
    my_blockchain.validate_and_add_block()

    # Print the current state of the blockchain
    for block in my_blockchain.chain:
        print(block)

