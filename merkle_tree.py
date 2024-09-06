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
        if not self.leaves:
            return None
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


    def get_proof(self, leaf):
        # todo unit tests are failing
        # Implement the proof calculation logic here
        try:
            self.build_tree()
            if self.nodes is None:
                return None
            for i in range(len(self.nodes)):
                if self.nodes[i] == leaf:
                    proof = []
                    while i > 0:
                        sibling = self.nodes[i - 1] if i % 2 == 1 else self.nodes[i + 1]
                        proof.append(sibling)
                        i = (i - 1) // 2
                        print(f"Sibling for {leaf} is {sibling} at index {i}")
                        print(f"Leaf is {leaf} at index {i}")
                        print(f"Nodes are {self.nodes}")
                    return proof
        except Exception as e:
            print(f"Error getting proof for leaf index {leaf}: {str(e)}")
            return None


    def get_root(self):
        # Implement the Merkle root calculation logic here
        self.build_tree()
        return self.nodes[0]

    def verify_proof(self, leaf, proof):
        # Placeholder for verifying proof
        # todo Implement the proof verification logic here
        if not proof:
            return False
        try:
            computed_root = leaf
            for sibling in proof:
                computed_root += sibling
            return computed_root == self.get_root()
        except Exception as e:
            print(f"Error verifying proof for leaf index {leaf}: {str(e)}")
            return False

