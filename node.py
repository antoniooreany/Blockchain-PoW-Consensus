#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a node and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

class Node:
    def __init__(self, address, blockchain):
        self.address = address
        self.blockchain = blockchain

    def broadcast_transaction(self, transaction):
        # todo Implement the transaction broadcasting logic here
        for node in self.blockchain.nodes:
            node.receive_transaction(transaction)
        return True



    def broadcast_block(self, block):
        # todo Placeholder for broadcasting block
        for node in self.blockchain.nodes:
            node.receive_block(block)
        return True


    def receive_transaction(self, transaction):
        # todo Placeholder for receiving transaction here
        if transaction.is_valid():
            self.blockchain.block.add_transaction(transaction)
        return True


    def receive_block(self, block):
        # todo Placeholder for receiving block
        if block.is_valid():
            self.blockchain.add_block(block)
        return True

