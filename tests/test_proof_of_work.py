#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#   This code is for a pow and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import unittest
from unittest.mock import patch

from src.model.block import Block
from src.controller.proof_of_work import ProofOfWork


class TestProofOfWork(unittest.TestCase):

    @patch('src.utils.logging_utils.log_mined_block')
    def test_Block_with_valid_nonce_has_valid_proof(self):
        pass  # todo: implement test

    @patch('src.utils.hash_utils.calculate_block_hash')
    def test_Block_with_invalid_nonce_has_invalid_proof(self):
        pass  # todo: implement test

    @patch('src.utils.logging_utils.log_mined_block')
    def test_Block_with_none_raises_value_error(self):
        proof_of_work = ProofOfWork()
        with self.assertRaises(ValueError):
            proof_of_work.find_nonce(block=None, bit_difficulty=4)

    @patch('src.utils.logging_utils.log_mined_block')
    def test_Bit_adjustment_factor_clamped_within_range(self):
        pow = ProofOfWork()
        self.assertEqual(pow.clamp_bit_adjustment_factor(5, 3), 3)
        self.assertEqual(pow.clamp_bit_adjustment_factor(-5, 3), -3)
        self.assertEqual(pow.clamp_bit_adjustment_factor(2, 3), 2)
        self.assertEqual(pow.clamp_bit_adjustment_factor(-2, 3), -2)

    @patch('src.utils.logging_utils.log_mined_block')
    def test_Bit_adjustment_factor_raises_value_error_for_none(self):
        pow = ProofOfWork()
        with self.assertRaises(ValueError):
            pow.clamp_bit_adjustment_factor(None, 3)
        with self.assertRaises(ValueError):
            pow.clamp_bit_adjustment_factor(2, None)

    @patch('src.utils.logging_utils.log_mined_block')
    def test_Bit_adjustment_factor_raises_type_error_for_non_numbers(self):
        pow = ProofOfWork()
        with self.assertRaises(TypeError):
            pow.clamp_bit_adjustment_factor("invalid", 3)
        with self.assertRaises(TypeError):
            pow.clamp_bit_adjustment_factor(2, "invalid")

    @patch('src.utils.logging_utils.log_mined_block')
    def test_Bit_adjustment_factor_raises_value_error_for_negative_clamp_factor(self):
        pow = ProofOfWork()
        with self.assertRaises(ValueError):
            pow.clamp_bit_adjustment_factor(2, -3)


if __name__ == "__main__":
    unittest.main()
