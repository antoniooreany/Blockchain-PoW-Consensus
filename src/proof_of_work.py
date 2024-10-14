#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

from block import Block


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
