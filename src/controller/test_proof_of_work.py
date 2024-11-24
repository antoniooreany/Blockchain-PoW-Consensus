#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import unittest
from unittest.mock import MagicMock, patch
from src.controller.proof_of_work import ProofOfWork
from src.model.block import Block

class TestProofOfWork(unittest.TestCase):
    def test_find_nonce_none_block(self):
        proof_of_work = ProofOfWork()
        with self.assertRaises(ValueError):
            proof_of_work.find_nonce(None, 1.0)

    @patch('src.utils.logging_utils.log_mined_block')
    def test_find_nonce_valid_nonce(self, mock_log_mined_block):
        # block = Block(index=1, timestamp=123, data='data', previous_hash='prev_hash')
        block = MagicMock()
        proof_of_work = ProofOfWork()
        proof_of_work.find_nonce(block, 1.0)
        self.assertIsNotNone(block.hash)
        mock_log_mined_block.assert_called_once_with(block)

    @patch('src.utils.hash_utils.calculate_block_hash')
    def test_find_nonce_increment_nonce(self, mock_calculate_block_hash):
        # block = Block(index=1, timestamp=123, data='data', previous_hash='prev_hash')
        block = MagicMock()
        mock_calculate_block_hash.side_effect = ['invalid_hash', 'valid_hash']
        proof_of_work = ProofOfWork()
        proof_of_work.find_nonce(block, 1.0)
        self.assertEqual(block.nonce, 2)
        mock_calculate_block_hash.assert_called_twice()

if __name__ == '__main__':
    unittest.main()