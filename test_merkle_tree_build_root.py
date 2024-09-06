#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a test_merkle_tree and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import unittest
from merkle_tree import MerkleTree

class TestMerkleTreeBuildTree(unittest.TestCase):
    def test_single_leaf_node(self):
        leaves = ['leaf1']
        tree = MerkleTree(leaves)
        root = tree.build_tree()
        self.assertEqual(root, 'leaf1')

    def test_multiple_leaf_nodes_even(self):
        leaves = ['leaf1', 'leaf2', 'leaf3', 'leaf4']
        tree = MerkleTree(leaves)
        root = tree.build_tree()
        self.assertEqual(root, 'leaf1leaf2leaf3leaf4')

    def test_multiple_leaf_nodes_odd(self):
        leaves = ['leaf1', 'leaf2', 'leaf3']
        tree = MerkleTree(leaves)
        root = tree.build_tree()
        self.assertEqual(root, 'leaf1leaf2leaf3')

    def test_empty_leaf_nodes(self):
        leaves = []
        tree = MerkleTree(leaves)
        with self.assertRaises(IndexError):
            tree.build_tree()

    def test_duplicate_leaf_nodes(self):
        leaves = ['leaf1', 'leaf1', 'leaf2']
        tree = MerkleTree(leaves)
        root = tree.build_tree()
        self.assertEqual(root, 'leaf1leaf1leaf2')

if __name__ == '__main__':
    unittest.main()
