#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a test_block and its unit tests.
import hashlib
from unittest import TestCase

from src.block import Block


#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
class Test(TestCase):
    # def test_block(self):
    #     self.fail()
    def block_initialization(self=None):
        block = Block(1, 1634070400.0, "Test Data", "0")
        self.assertEqual(block.index, 1)
        self.assertEqual(block.timestamp, 1634070400.0)
        self.assertEqual(block.data, "Test Data")
        self.assertEqual(block.previous_hash, "0")
        self.assertEqual(block.nonce, 0)
        self.assertIsNotNone(block.hash)

    def calculate_hash(self=None):
        block = Block(1, 1634070400.0, "Test Data", "0")
        expected_hash = hashlib.sha256(
            (str(block.index) +
             str(block.timestamp) +
             str(block.data) +
             str(block.previous_hash) +
             str(block.nonce)).encode('utf-8')).hexdigest()
        self.assertEqual(block.calculate_hash(), expected_hash)

    def mine_block(self=None):
        block = Block(1, 1634070400.0, "Test Data", "0")
        block.mine(4)
        self.assertTrue(int(block.hash, 16) < (2 ** (256 - 4)) - 1)

    def mine_block_with_high_difficulty(self=None):
        block = Block(1, 1634070400.0, "Test Data", "0")
        block.mine(20)
        self.assertTrue(int(block.hash, 16) < (2 ** (256 - 20)) - 1)

    def mine_block_with_low_difficulty(self=None):
        block = Block(1, 1634070400.0, "Test Data", "0")
        block.mine(1)
        self.assertTrue(int(block.hash, 16) < (2 ** (256 - 1)) - 1)

    def mine_block_edge_case_max_nonce(self=None):
        block = Block(1, 1634070400.0, "Test Data", "0")
        block.nonce = 2 ** 256 - 1
        block.mine(4)
        self.assertTrue(int(block.hash, 16) < (2 ** (256 - 4)) - 1)

    def mine_block_edge_case_zero_nonce(self=None):
        block = Block(1, 1634070400.0, "Test Data", "0")
        block.nonce = 0
        block.mine(4)
        self.assertTrue(int(block.hash, 16) < (2 ** (256 - 4)) - 1)
