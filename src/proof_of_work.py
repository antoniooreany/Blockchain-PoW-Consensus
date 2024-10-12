#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


from block import Block


# todo redundant class, move methods to Block class
class ProofOfWork:
    @staticmethod
    def find_nonce(block: Block, bit_difficulty: int) -> int:
        """
        Finds a nonce for a given block such that the block's hash
        is less than the target value based on the difficulty.

        Args:
            block (Block): The block to find a nonce for.
            bit_difficulty (int): The number of leading zero bits required in the hash.

        Returns:
            int: The nonce that results in the block's hash meeting the difficulty requirement.
        """
        target_value = (2 ** (256 - bit_difficulty)) - 1
        while int(block.hash, 16) >= target_value:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.nonce

    @staticmethod
    def validate_proof(block: Block, bit_difficulty: int) -> bool:
        """
        Checks if a given block's hash is less than the target value based on the difficulty.

        Args:
            block (Block): The block to validate.
            bit_difficulty (int): The number of leading zero bits required in the hash.

        Returns:
            bool: True if the block's hash meets the difficulty requirement, False otherwise.
        """
        target_value = (2 ** (256 - bit_difficulty)) - 1
        return int(block.hash, 16) < target_value
