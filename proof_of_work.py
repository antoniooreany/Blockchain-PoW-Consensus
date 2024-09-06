#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a proof_of_work and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

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
