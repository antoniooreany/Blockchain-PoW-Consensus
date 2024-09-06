# #   Copyright (c) 2024, Anton Gorshkov
# #   All rights reserved.
# #
# #   This code is for a test_merkle_tree and its unit tests.
# #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
#
# import unittest
# from merkle_tree import MerkleTree
#
# class TestMerkleTreeBuildTree(unittest.TestCase):
#     def test_single_leaf_node(self):
#         leaves = ['leaf1']
#         tree = MerkleTree(leaves)
#         root = tree.build_tree()
#         self.assertEqual(root, 'leaf1')
#
#     def test_multiple_leaf_nodes_even(self):
#         leaves = ['leaf1', 'leaf2', 'leaf3', 'leaf4']
#         tree = MerkleTree(leaves)
#         root = tree.build_tree()
#         self.assertEqual(root, 'leaf1leaf2leaf3leaf4')
#
#     def test_multiple_leaf_nodes_odd(self):
#         leaves = ['leaf1', 'leaf2', 'leaf3']
#         tree = MerkleTree(leaves)
#         root = tree.build_tree()
#         self.assertEqual(root, 'leaf1leaf2leaf3')
#
#     def test_empty_leaf_nodes(self):
#         leaves = []
#         tree = MerkleTree(leaves)
#         with self.assertRaises(IndexError):
#             tree.build_tree()
#
#     def test_duplicate_leaf_nodes(self):
#         leaves = ['leaf1', 'leaf1', 'leaf2']
#         tree = MerkleTree(leaves)
#         root = tree.build_tree()
#         self.assertEqual(root, 'leaf1leaf1leaf2')
#
# if __name__ == '__main__':
#     unittest.main()

import unittest
from merkle_tree import MerkleTree

class TestBuildTree(unittest.TestCase):
    def test_even_leaves(self):
        leaves = ['a', 'b', 'c', 'd']
        merkle_tree = MerkleTree(leaves)
        tree = merkle_tree.build_tree()
        self.assertEqual(len(tree), 3)  # 2 levels + 1 root
        self.assertEqual(len(tree[0]), 2)  # 2 pairs at level 1
        self.assertEqual(len(tree[1]), 1)  # 1 pair at level 2
        self.assertEqual(len(tree[2]), 1)  # 1 root

    # def test_odd_leaves(self):
    #     leaves = ['a', 'b', 'c', 'd', 'e']
    #     merkle_tree = MerkleTree(leaves)
    #     tree = merkle_tree.build_tree()
    #     self.assertEqual(len(tree), 3)  # 2 levels + 1 root

    # def test_odd_leaves(self):
    #     leaves = ['a', 'b', 'c', 'd', 'e']
    #     merkle_tree = MerkleTree(leaves)
    #     tree = merkle_tree.build_tree()
    #     print(tree)  # Add this line
    #     self.assertEqual(len(tree), 3)  # 2 levels + 1 root
    #     self.assertEqual(len(tree[0]), 2)  # 2 pairs at level 1
    #     self.assertEqual(len(tree[1]), 2)  # 2 pairs at level 2 (one is a duplicate)
    #     self.assertEqual(len(tree[2]), 1)  # 1 root


    # def test_odd_leaves(self):
    #     leaves = ['a', 'b', 'c', 'd', 'e']
    #     merkle_tree = MerkleTree(leaves)
    #     tree = merkle_tree.build_tree()
    #     print(tree)  # Add this line
    #     self.assertEqual(len(tree), 4)  # 3 levels + 1 root
    #     self.assertEqual(len(tree[0]), 2)  # 2 pairs at level 1
    #     self.assertEqual(len(tree[1]), 2)  # 2 pairs at level 2 (one is a duplicate)
    #     self.assertEqual(len(tree[2]), 1)  # 1 pair at level 3
    #     self.assertEqual(len(tree[3]), 1)  # 1 root


    def test_odd_leaves(self):
        leaves = ['a', 'b', 'c', 'd', 'e']
        merkle_tree = MerkleTree(leaves)
        tree = merkle_tree.build_tree()
        print(tree)  # Add this line
        self.assertEqual(len(tree), 4)  # 3 levels + 1 root
        self.assertEqual(len(tree[0]), 3)  # 3 pairs at level 1 (one is a duplicate)
        self.assertEqual(len(tree[1]), 2)  # 2 pairs at level 2 (one is a duplicate)
        self.assertEqual(len(tree[2]), 1)  # 1 pair at level 3
        self.assertEqual(len(tree[3]), 1)  # 1 root

    def test_single_leaf(self):
        leaves = ['a']
        merkle_tree = MerkleTree(leaves)
        tree = merkle_tree.build_tree()
        self.assertEqual(len(tree), 1)  # 1 root
        self.assertEqual(len(tree[0]), 1)  # 1 root

    def test_no_leaves(self):
        leaves = []
        merkle_tree = MerkleTree(leaves)
        tree = merkle_tree.build_tree()
        self.assertEqual(len(tree), 1)  # 1 root
        self.assertEqual(len(tree[0]), 1)  # 1 None root

if __name__ == '__main__':
    unittest.main()
