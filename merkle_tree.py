# # # # #   Copyright (c) 2024, Anton Gorshkov
# # # # #   All rights reserved.
# # # # #
# # # # #   This code is for a merkle_tree and its unit tests.
# # # # #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
# # # #
# # # # class MerkleTree:
# # # #     def __init__(self, leaves):
# # # #         self.leaves = leaves
# # # #         self.nodes = []
# # # #
# # # #     def build_tree(self, leaves=None):
# # # #         # Implement the Merkle tree building logic here
# # # #         if leaves is None:
# # # #             leaves = self.leaves
# # # #         if not self.leaves:
# # # #             return None
# # # #         for leaf in self.leaves:
# # # #             self.nodes.append(leaf)
# # # #         while len(self.nodes) > 1:
# # # #             new_nodes = []
# # # #             for i in range(0, len(self.nodes), 2):
# # # #                 node = self.nodes[i]
# # # #                 if i + 1 < len(self.nodes):
# # # #                     node += self.nodes[i + 1]
# # # #                 new_nodes.append(node)
# # # #             self.nodes = new_nodes
# # # #         return self.nodes[0]
# # # #
# # # #
# # # #     def get_proof(self, leaf):
# # # #         # todo unit tests are failing
# # # #         # Implement the proof calculation logic here
# # # #         if not hasattr(self, 'nodes'):
# # # #             raise ValueError("Merkle tree is not built yet")
# # # #         try:
# # # #             self.build_tree()
# # # #             if self.nodes is None:
# # # #                 return None
# # # #             for i in range(len(self.nodes)):
# # # #                 if self.nodes[i] == leaf:
# # # #                     proof = []
# # # #                     while i > 0:
# # # #                         sibling = self.nodes[i - 1] if i % 2 == 1 else self.nodes[i + 1]
# # # #                         proof.append(sibling)
# # # #                         i = (i - 1) // 2
# # # #                         print(f"Sibling for {leaf} is {sibling} at index {i}")
# # # #                         print(f"Leaf is {leaf} at index {i}")
# # # #                         print(f"Nodes are {self.nodes}")
# # # #                     return proof
# # # #         except Exception as e:
# # # #             print(f"Error getting proof for leaf index {leaf}: {str(e)}")
# # # #             return None
# # # #
# # # #
# # # #     def get_root(self):
# # # #         # Implement the Merkle root calculation logic here
# # # #         self.build_tree()
# # # #         return self.nodes[0]
# # # #
# # # #     def verify_proof(self, leaf, proof):
# # # #         # todo Implement the proof verification logic here
# # # #         if not hasattr(self, 'nodes'):
# # # #             raise ValueError("Merkle tree is not built yet")
# # # #         if not proof:
# # # #             return False
# # # #         try:
# # # #             computed_root = leaf
# # # #             for sibling in proof:
# # # #                 computed_root += sibling
# # # #             return computed_root == self.get_root()
# # # #         except Exception as e:
# # # #             print(f"Error verifying proof for leaf index {leaf}: {str(e)}")
# # # #             return False
# # # #
# # #
# # # import hashlib
# # #
# # #
# # # class MerkleTree:
# # #     def __init__(self, leaves):
# # #         self.leaves = leaves
# # #         self.nodes = []  # Initialize nodes as an empty list
# # #         self.root = self.build_tree()
# # #
# # #     # def build_tree(self):
# # #     #     self.nodes = self.leaves[:]
# # #     #     while len(self.nodes) > 1:
# # #     #         temp_nodes = []
# # #     #         for i in range(0, len(self.nodes), 2):
# # #     #             left = self.nodes[i]
# # #     #             right = self.nodes[i + 1] if i + 1 < len(self.nodes) else left
# # #     #             temp_nodes.append(self.hash_pair(left, right))
# # #     #         self.nodes = temp_nodes
# # #     #     return self.nodes[0] if self.nodes else None
# # #
# # #     def build_tree(self):
# # #         self.nodes = self.leaves[:]
# # #         tree = []
# # #         while len(self.nodes) > 1:
# # #             level = []
# # #             temp_nodes = []
# # #             for i in range(0, len(self.nodes), 2):
# # #                 left = self.nodes[i]
# # #                 right = self.nodes[i + 1] if i + 1 < len(self.nodes) else left
# # #                 level.append((left, right))
# # #                 temp_nodes.append(self.hash_pair(left, right))
# # #             tree.append(level)
# # #             self.nodes = temp_nodes
# # #         tree.append([self.nodes[0] if self.nodes else None])
# # #         return tree
# # #
# # #     def hash_pair(self, left, right):
# # #         sha = hashlib.sha256()
# # #         sha.update((left + right).encode('utf-8'))
# # #         return sha.hexdigest()
# # #
# # #     def get_root(self):
# # #         return self.root
# # #
# # #     def get_proof(self, leaf):
# # #         index = self.leaves.index(leaf)
# # #         proof = []
# # #         nodes = self.leaves[:]
# # #         while len(nodes) > 1:
# # #             temp_nodes = []
# # #             for i in range(0, len(nodes), 2):
# # #                 left = nodes[i]
# # #                 right = nodes[i + 1] if i + 1 < len(nodes) else left
# # #                 if i == index or i + 1 == index:
# # #                     proof.append(right if i == index else left)
# # #                 temp_nodes.append(self.hash_pair(left, right))
# # #             nodes = temp_nodes
# # #             index //= 2
# # #         return proof
# # #
# # #     def verify_proof(self, leaf, proof):
# # #         print(f"Verofying proof for leaf: {leaf} with proof: {proof}")
# # #         current_hash = leaf
# # #         for sibling in proof:
# # #             current_hash = self.hash_pair(current_hash, sibling)
# # #         is_valid = current_hash == self.root
# # #         print(f"Returning {is_valid}")
# # #         return is_valid
# # #
# # #     def update_tree(self, new_leaf):
# # #         # todo Placeholder for updating tree
# # #         pass
# #
# # import hashlib
# #
# # class MerkleTree:
# #     def __init__(self, leaves):
# #         self.leaves = leaves
# #         self.nodes = []  # Initialize nodes as an empty list
# #         self.root = self.build_tree()
# #
# #     def build_tree(self):
# #         self.nodes = self.leaves[:]
# #         while len(self.nodes) > 1:
# #             temp_nodes = []
# #             for i in range(0, len(self.nodes), 2):
# #                 left = self.nodes[i]
# #                 right = self.nodes[i + 1] if i + 1 < len(self.nodes) else left
# #                 temp_nodes.append(self.hash_pair(left, right))
# #             self.nodes = temp_nodes
# #         return self.nodes[0] if self.nodes else None
# #
# #     def hash_pair(self, left, right):
# #         sha = hashlib.sha256()
# #         sha.update((left + right).encode('utf-8'))
# #         return sha.hexdigest()
# #
# #     def get_root(self):
# #         return self.root
# #
# #     def get_proof(self, leaf):
# #         index = self.leaves.index(leaf)
# #         proof = []
# #         nodes = self.leaves[:]
# #         while len(nodes) > 1:
# #             temp_nodes = []
# #             for i in range(0, len(nodes), 2):
# #                 left = nodes[i]
# #                 right = nodes[i + 1] if i + 1 < len(nodes) else left
# #                 if i == index or i + 1 == index:
# #                     proof.append(right if i == index else left)
# #                 temp_nodes.append(self.hash_pair(left, right))
# #             nodes = temp_nodes
# #             index //= 2
# #         return proof
# #
# #     def verify_proof(self, leaf, proof):
# #         current_hash = hashlib.sha256(leaf.encode('utf-8')).hexdigest()
# #         for sibling in proof:
# #             if current_hash < sibling:
# #                 current_hash = self.hash_pair(current_hash, sibling)
# #             else:
# #                 current_hash = self.hash_pair(sibling, current_hash)
# #         return current_hash == self.root
# #
# #     def update_tree(self, new_leaf):
# #         # Placeholder for updating tree
# #         pass
#
#
# import hashlib
#
# class MerkleTree:
#     def __init__(self, leaves):
#         self.leaves = leaves
#         self.nodes = []  # Initialize nodes as an empty list
#         self.root = self.build_tree()
#
#     def build_tree(self):
#         self.nodes = self.leaves[:]
#         while len(self.nodes) > 1:
#             temp_nodes = []
#             for i in range(0, len(self.nodes), 2):
#                 left = self.nodes[i]
#                 right = self.nodes[i + 1] if i + 1 < len(self.nodes) else left
#                 temp_nodes.append(self.hash_pair(left, right))
#             self.nodes = temp_nodes
#         return self.nodes[0] if self.nodes else None
#
#     def hash_pair(self, left, right):
#         sha = hashlib.sha256()
#         sha.update((left + right).encode('utf-8'))
#         return sha.hexdigest()
#
#     def get_root(self):
#         return self.root
#
#     def get_proof(self, leaf):
#         index = self.leaves.index(leaf)
#         proof = []
#         nodes = self.leaves[:]
#         while len(nodes) > 1:
#             temp_nodes = []
#             for i in range(0, len(nodes), 2):
#                 left = nodes[i]
#                 right = nodes[i + 1] if i + 1 < len(nodes) else left
#                 if i == index or i + 1 == index:
#                     proof.append(right if i == index else left)
#                 temp_nodes.append(self.hash_pair(left, right))
#             nodes = temp_nodes
#             index //= 2
#         return proof
#
#     def verify_proof(self, leaf, proof):
#         current_hash = hashlib.sha256(leaf.encode('utf-8')).hexdigest()
#         for sibling in proof:
#             if current_hash < sibling:
#                 current_hash = self.hash_pair(current_hash, sibling)
#             else:
#                 current_hash = self.hash_pair(sibling, current_hash)
#         return current_hash == self.root
#
#     def update_tree(self, new_leaf):
#         # Placeholder for updating tree
#         pass

import hashlib

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = leaves
        self.nodes = []  # Initialize nodes as an empty list
        self.root = self.build_tree()

    def build_tree(self):
        self.nodes = self.leaves[:]
        while len(self.nodes) > 1:
            temp_nodes = []
            for i in range(0, len(self.nodes), 2):
                left = self.nodes[i]
                right = self.nodes[i + 1] if i + 1 < len(self.nodes) else left
                temp_nodes.append(self.hash_pair(left, right))
            self.nodes = temp_nodes
        return self.nodes[0] if self.nodes else None

    def hash_pair(self, left, right):
        sha = hashlib.sha256()
        sha.update((left + right).encode('utf-8'))
        return sha.hexdigest()

    def get_root(self):
        return self.root

    def get_proof(self, leaf):
        index = self.leaves.index(leaf)
        proof = []
        nodes = self.leaves[:]
        while len(nodes) > 1:
            temp_nodes = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else left
                if i == index or i + 1 == index:
                    proof.append(right if i == index else left)
                temp_nodes.append(self.hash_pair(left, right))
            nodes = temp_nodes
            index //= 2
        return proof

    # def verify_proof(self, leaf, proof):
    #     current_hash = hashlib.sha256(leaf.encode('utf-8')).hexdigest()
    #     for sibling in proof:
    #         if current_hash < sibling:
    #             current_hash = self.hash_pair(current_hash, sibling)
    #         else:
    #             current_hash = self.hash_pair(sibling, current_hash)
    #     return current_hash == self.root


    # def verify_proof(self, leaf, proof):
    #     root = leaf
    #     for sibling in proof:
    #         if hash(root + sibling) != hash(sibling + root):
    #             return False
    #         root = hash(root + sibling)
    #     return root == self.root

    def verify_proof(self, leaf, proof):
        # todo implemented incorrectly
        current_hash = hashlib.sha256(leaf.encode('utf-8')).hexdigest()
        for sibling in proof:
            if current_hash < sibling:
                current_hash = self.hash_pair(current_hash, sibling)
            else:
                current_hash = self.hash_pair(sibling, current_hash)
        return current_hash == self.root

    def update_tree(self, new_leaf):
        self.leaves.append(new_leaf)
        self.root = self.build_tree()

    def get_leaf(self, index):
        return self.leaves[index] if index < len(self.leaves) else None

    def get_all_leaves(self):
        return self.leaves
