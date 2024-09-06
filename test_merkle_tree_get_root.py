#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a test_merkle_tree_get_root and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import unittest
from merkle_tree import MerkleTree

class TestMerkleTreeGetRoot(unittest.TestCase):
    def test_single_leaf_node(self):
        leaves = ['leaf1']
        tree = MerkleTree(leaves)
        root = tree.get_root()
        self.assertEqual(root, 'leaf1')

    def test_multiple_leaf_nodes_even(self):
        leaves = ['leaf1', 'leaf2', 'leaf3', 'leaf4']
        tree = MerkleTree(leaves)
        root = tree.get_root()
        self.assertEqual(root, 'leaf1leaf2leaf3leaf4')

    def test_multiple_leaf_nodes_odd(self):
        leaves = ['leaf1', 'leaf2', 'leaf3', 'leaf4', 'leaf5']
        tree = MerkleTree(leaves)
        root = tree.get_root()
        self.assertEqual(root, 'leaf1leaf2leaf3leaf4leaf5')

    def test_empty_leaf_nodes(self):
        leaves = []
        tree = MerkleTree(leaves)
        with self.assertRaises(IndexError):
            tree.get_root()

if __name__ == '__main__':
    unittest.main()
