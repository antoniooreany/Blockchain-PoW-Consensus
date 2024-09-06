# #   Copyright (c) 2024, Anton Gorshkov
# #   All rights reserved.
# #
# #   This code is for a test_merkle_tree_get_proof and its unit tests.
# #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
#
# import unittest
# from merkle_tree import MerkleTree
#
# class TestMerkleTreeGetProof(unittest.TestCase):
#     def test_even_index_leaf(self):
#         leaves = [1, 2, 3, 4]
#         tree = MerkleTree(leaves)
#         proof = tree.get_proof(2)
#         self.assertEqual(proof, [1, 3])
#
#     def test_odd_index_leaf(self):
#         leaves = [1, 2, 3, 4]
#         tree = MerkleTree(leaves)
#         proof = tree.get_proof(3)
#         self.assertEqual(proof, [2, 1])
#
#     def test_single_child_leaf(self):
#         leaves = [1, 2]
#         tree = MerkleTree(leaves)
#         proof = tree.get_proof(2)
#         self.assertEqual(proof, [1])
#
#     def test_non_existent_leaf(self):
#         leaves = [1, 2, 3, 4]
#         tree = MerkleTree(leaves)
#         proof = tree.get_proof(5)
#         self.assertIsNone(proof)
#
#     def test_empty_tree(self):
#         leaves = []
#         tree = MerkleTree(leaves)
#         proof = tree.get_proof(1)
#         self.assertIsNone(proof)
#
# if __name__ == '__main__':
#     unittest.main()

import unittest
from merkle_tree import MerkleTree

class TestMerkleTreeGetProof(unittest.TestCase):

    def test_get_proof_existing_leaf(self):
        leaves = [1, 2, 3, 4]
        tree = MerkleTree(leaves)
        proof = tree.get_proof(2) # todo why unexpectedly None???
        self.assertIsNotNone(proof)
        self.assertEqual(len(proof), 2)  # expected proof length for leaf at index 1

    def test_get_proof_non_existing_leaf(self):
        leaves = [1, 2, 3, 4]
        tree = MerkleTree(leaves)
        proof = tree.get_proof(5)
        self.assertIsNone(proof)

    def test_get_proof_empty_tree(self):
        leaves = []
        tree = MerkleTree(leaves)
        proof = tree.get_proof(1)
        self.assertIsNone(proof)

    def test_get_proof_single_leaf_tree(self):
        leaves = [1]
        tree = MerkleTree(leaves)
        proof = tree.get_proof(1)
        self.assertEqual(proof, [])  # expected proof length for single leaf tree

    def test_get_proof_multiple_leaves_tree(self):
        leaves = [1, 2, 3, 4, 5, 6, 7, 8]
        tree = MerkleTree(leaves)
        proof = tree.get_proof(4)
        self.assertIsNotNone(proof) # todo why unexpectedly None???
        self.assertEqual(len(proof), 3)  # expected proof length for leaf at index 3

if __name__ == '__main__':
    unittest.main()

