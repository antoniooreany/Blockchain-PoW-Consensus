#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a merkle_tree and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = leaves
        self.nodes = []

    def build_tree(self):
        # Implement the Merkle tree building logic here
        for leaf in self.leaves:
            self.nodes.append(leaf)
        while len(self.nodes) > 1:
            new_nodes = []
            for i in range(0, len(self.nodes), 2):
                node = self.nodes[i]
                if i + 1 < len(self.nodes):
                    node += self.nodes[i + 1]
                new_nodes.append(node)
            self.nodes = new_nodes
        return self.nodes[0]


    def get_root(self):
        # todo Placeholder for getting Merkle root
        # Implement the Merkle root calculation logic here
        return "merkle_root"

    def get_proof(self, leaf):
        # Placeholder for getting proof
        pass

    def verify_proof(self, leaf, proof):
        # Placeholder for verifying proof
        pass
