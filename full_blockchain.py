#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a full_blockchain.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import hashlib
import time


class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str = '') -> None:
        """
        Initialize a Block object.

        Args:
            index (int): The index of the block in the blockchain.
            timestamp (float): The timestamp of the block.
            data (str): The data stored in the block.
            previous_hash (str, optional): The hash of the previous block. Defaults to ''.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Initialize nonce before calculating hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the block based on its properties.

        The hash is calculated using the SHA-256 algorithm.

        Args:
            index (int): The index of the block in the blockchain.
            timestamp (float): The timestamp of the block.
            data (str): The data stored in the block.
            previous_hash (str): The hash of the previous block.
            nonce (int): The nonce used to mine the block.

        Returns:
            str: The hash of the block in hexadecimal representation.
        """
        sha = hashlib.sha256()
        sha.update(
            (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)).encode(
                'utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Mine a block with a given difficulty.

        The block is mined by incrementing the nonce until the hash of the block
        starts with 'difficulty' zeros.

        Args:
            difficulty (int): The difficulty of the block to mine.

        Returns:
            None
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")


class Blockchain:
    def __init__(self, difficulty: int) -> None:
        """
        Initialize a Blockchain object.

        Args:
            difficulty (int): The difficulty of the blockchain.

        Returns:
            None
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    @staticmethod
    def create_genesis_block() -> Block:
        """
        Create the genesis block (index 0) of the blockchain.

        The genesis block is a special block that is the first block in the
        blockchain. It is created with a timestamp of the current time,
        data of "Genesis Block", and a previous hash of "0".

        Returns:
            Block: The genesis block.
        """
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        """
        Get the latest block in the blockchain.

        This function returns the last block that was added to the blockchain.

        Returns:
            Block: The latest block in the blockchain.
        """
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        """
        Add a new block to the blockchain after mining it.

        Args:
            new_block (Block): The new block to be added.

        Returns:
            None
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

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block: Block = self.chain[i]
            previous_block: Block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


class ProofOfWork:
    @staticmethod
    def find_nonce(block: Block, difficulty: int) -> int:
        """
        Finds a nonce for a given block such that the block's hash
        starts with 'difficulty' zeros.

        Args:
            block (Block): The block to find a nonce for.
            difficulty (int): The number of zeros that the block's hash
                should start with.

        Returns:
            int: The nonce that results in the block's hash starting
                with 'difficulty' zeros.
        """
        target = '0' * difficulty
        while block.hash[:difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.nonce

    @staticmethod
    def validate_proof(block: Block, difficulty: int) -> bool:
        """
        Checks if a given block's hash starts with 'difficulty' zeros.

        Args:
            block (Block): The block to validate.
            difficulty (int): The number of zeros that the block's hash
                should start with.

        Returns:
            bool: True if the block's hash starts with 'difficulty' zeros,
                False otherwise.
        """
        target = '0' * difficulty
        return block.hash[:difficulty] == target


if __name__ == "__main__":
    blockchain = Blockchain(difficulty=4)

    for i in range(10):
        blockchain.add_block(Block(i, time.time(), f"Block {i} Data"))
        print("Blockchain valid?", blockchain.is_chain_valid())

    for block in blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Nonce: {block.nonce}")