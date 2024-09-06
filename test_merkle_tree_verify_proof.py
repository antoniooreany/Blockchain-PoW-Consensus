# # # #   Copyright (c) 2024, Anton Gorshkov
# # # #   All rights reserved.
# # # #
# # # #   This code is for a test_merkle_tree_verify_proof and its unit tests.
# # # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# # #
# # # import unittest
# # # from merkle_tree import MerkleTree
# # #
# # # class TestVerifyProof(unittest.TestCase):
# # #     def setUp(self, leaves):
# # #         self.merkle_tree = MerkleTree(leaves)
# # #
# # #     def test_empty_proof(self):
# # #         self.assertFalse(self.merkle_tree.verify_proof("leaf", []))
# # #
# # #     def test_invalid_proof(self):
# # #         self.merkle_tree.build_tree(["leaf1", "leaf2"])
# # #         self.assertFalse(self.merkle_tree.verify_proof("leaf1", ["invalid_sibling"]))
# # #
# # #     def test_valid_proof(self):
# # #         self.merkle_tree.build_tree(["leaf1", "leaf2"])
# # #         proof = self.merkle_tree.get_proof("leaf1")
# # #         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
# # #
# # #     def test_single_sibling_proof(self):
# # #         self.merkle_tree.build_tree(["leaf1", "leaf2"])
# # #         proof = self.merkle_tree.get_proof("leaf1")
# # #         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
# # #
# # #     def test_multiple_siblings_proof(self):
# # #         self.merkle_tree.build_tree(["leaf1", "leaf2", "leaf3", "leaf4"])
# # #         proof = self.merkle_tree.get_proof("leaf1")
# # #         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
# # #
# # #     def test_edge_case_empty_leaf(self):
# # #         self.merkle_tree.build_tree([""])
# # #         proof = self.merkle_tree.get_proof("")
# # #         self.assertTrue(self.merkle_tree.verify_proof("", proof))
# # #
# # # if __name__ == "__main__":
# # #     unittest.main()
# #
# # import unittest
# # from merkle_tree import MerkleTree
# #
# # class TestMerkleTreeVerifyProof(unittest.TestCase):
# #     def setUp(self):
# #         self.merkle_tree = MerkleTree([])
# #
# #     def test_empty_proof(self):
# #         leaves = []
# #         tree = MerkleTree(leaves)
# #         with self.assertRaises(IndexError):
# #             tree.build_tree()
# #         # self.assertFalse(self.merkle_tree.verify_proof("leaf", []))
# #
# #     def test_invalid_proof(self):
# #         self.merkle_tree.build_tree(["leaf1", "leaf2"])
# #         self.assertFalse(self.merkle_tree.verify_proof("leaf1", ["invalid_sibling"]))
# #
# #     def test_valid_proof(self):
# #         self.merkle_tree.build_tree(["leaf1", "leaf2"])
# #         proof = self.merkle_tree.get_proof("leaf1")
# #         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
# #
# #     def test_single_sibling_proof(self):
# #         self.merkle_tree.build_tree(["leaf1", "leaf2"])
# #         proof = self.merkle_tree.get_proof("leaf1")
# #         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
# #
# #     def test_multiple_siblings_proof(self):
# #         self.merkle_tree.build_tree(["leaf1", "leaf2", "leaf3", "leaf4"])
# #         proof = self.merkle_tree.get_proof("leaf1")
# #         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
# #
# #     def test_edge_case_empty_leaf(self):
# #         self.merkle_tree.build_tree([])
# #         self.assertFalse(self.merkle_tree.verify_proof("leaf", []))
# #
# # if __name__ == '__main__':
# #     unittest.main()
#
# import unittest
# from merkle_tree import MerkleTree
#
# class TestMerkleTreeVerifyProof(unittest.TestCase):
#     def setUp(self):
#         self.merkle_tree = MerkleTree([])
#         self.merkle_tree.build_tree([])
#
#     def test_empty_proof(self):
#         leaves = []
#         tree = MerkleTree(leaves)
#         with self.assertRaises(IndexError):
#             tree.build_tree()
#
#     def test_invalid_proof(self):
#         self.merkle_tree.build_tree(["leaf1", "leaf2"])
#         self.assertFalse(self.merkle_tree.verify_proof("leaf1", ["invalid_sibling"]))
#
#     def test_valid_proof(self):
#         self.merkle_tree.build_tree(["leaf1", "leaf2"])
#         proof = self.merkle_tree.get_proof("leaf1")
#         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
#
#     def test_single_sibling_proof(self):
#         self.merkle_tree.build_tree(["leaf1", "leaf2"])
#         proof = self.merkle_tree.get_proof("leaf1")
#         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
#
#     def test_multiple_siblings_proof(self):
#         self.merkle_tree.build_tree(["leaf1", "leaf2", "leaf3", "leaf4"])
#         proof = self.merkle_tree.get_proof("leaf1")
#         self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))
#
#     def test_edge_case_empty_leaf(self):
#         self.merkle_tree.build_tree(["leaf1", "leaf2"])
#         proof = self.merkle_tree.get_proof("")
#         # rest of the test method
#         self.merkle_tree.build_tree([""])
#         proof = self.merkle_tree.get_proof("")
#         self.assertTrue(self.merkle_tree.verify_proof("", proof))
#
# if __name__ == "__main__":
#     unittest.main()
#

import unittest
from merkle_tree import MerkleTree

class TestVerifyProof(unittest.TestCase):
    def setUp(self):
        self.merkle_tree = MerkleTree(["leaf1", "leaf2", "leaf3", "leaf4"])

    def test_valid_proof(self):
        proof = self.merkle_tree.get_proof("leaf1")
        self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))

    def test_invalid_proof(self):
        proof = ["invalid_sibling"]
        self.assertFalse(self.merkle_tree.verify_proof("leaf1", proof))

    def test_empty_proof(self):
        self.assertFalse(self.merkle_tree.verify_proof("leaf1", []))

    def test_single_sibling_proof(self):
        self.merkle_tree = MerkleTree(["leaf1", "leaf2"])
        proof = self.merkle_tree.get_proof("leaf1")
        self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))

    def test_multiple_siblings_proof(self):
        proof = self.merkle_tree.get_proof("leaf1")
        self.assertTrue(self.merkle_tree.verify_proof("leaf1", proof))

    def test_non_existent_leaf(self):
        self.assertFalse(self.merkle_tree.verify_proof("non_existent_leaf", []))

if __name__ == "__main__":
    unittest.main()
