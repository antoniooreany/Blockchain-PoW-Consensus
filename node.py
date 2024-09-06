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
        # Placeholder for receiving transaction
        pass

    def receive_block(self, block):
        # Placeholder for receiving block
        pass

    def validate_and_add_block(self, block):
        # Placeholder for block validation and addition
        pass
