#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import time
from block import Block


class Blockchain:
    def __init__(self, difficulty: int) -> None:
        """
        Initialize the blockchain with difficulty and a genesis block.

        :param difficulty: The difficulty of the blockchain.
        :return: None
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    @staticmethod
    def create_genesis_block() -> Block:
        """
        Create the genesis block (index 0) of the blockchain.

        :return: The genesis block.
        """
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        """
        Get the latest block in the blockchain.

        :return: The latest block in the blockchain.
        """
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        """
        Add a new block to the blockchain after mining it.

        :param new_block: The new block to be added.
        :return: None
        """
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        """
        Check if the blockchain is valid or not.

        Iterate through the blockchain and check if the hashes of the blocks match
        the expected hashes. Also, check if the previous hash of the current block
        matches the hash of the previous block.

        :return: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
