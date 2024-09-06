#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a test_merkle_tree and its unit tests.
from unittest import TestCase


#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# from merkle_tree import MerkleTree
#
# class TestMerkleTree(TestCase):
#     def test_verify_proof(self):
#         # Setup
#         leaves = ['a', 'b', 'c', 'd']
#         merkle_tree = MerkleTree(leaves)
#
#         # Build Tree
#         merkle_tree.build_tree()
#
#         # Get Proof
#         leaf = 'a'
#         proof = merkle_tree.get_proof(leaf)
#
#         # Verify Proof
#         is_valid = merkle_tree.verify_proof(leaf, proof)
#
#         # Assertions
#         self.assertTrue(is_valid)
#         self.assertEqual(merkle_tree.get_root(), merkle_tree.get_root())

from unittest import TestCase
from merkle_tree import MerkleTree

class TestMerkleTree(TestCase):
    def test_verify_proof(self):
        # Setup
        leaves = ['a', 'b', 'c', 'd']
        merkle_tree = MerkleTree(leaves)

        # Build Tree
        merkle_tree.build_tree()

        # Get Proof
        leaf = 'a'
        proof = merkle_tree.get_proof(leaf)

        # Verify Proof
        is_valid = merkle_tree.verify_proof(leaf, proof)

        # Assertions
        self.assertTrue(is_valid)
        self.assertEqual(merkle_tree.get_root(), merkle_tree.get_root())
