#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a test_blockchain and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
import time
import unittest

from block import Block
from blockchain import Blockchain


class TestConsensus(unittest.TestCase):

    def test_consensus_longer_local_chain(self):
        blockchain = Blockchain(difficulty=4)
        blockchain.add_block(Block(1, time.time(), "Block 1 Data"))
        blockchain.add_block(Block(2, time.time(), "Block 2 Data"))
        node = Blockchain(difficulty=4)
        node.add_block(Block(1, time.time(), "Block 1 Data"))
        blockchain.nodes.append(node)
        self.assertTrue(blockchain.consensus())

    def test_consensus_shorter_local_chain(self):
        blockchain = Blockchain(difficulty=4)
        blockchain.add_block(Block(1, time.time(), "Block 1 Data"))
        node = Blockchain(difficulty=4)
        node.add_block(Block(1, time.time(), "Block 1 Data"))
        node.add_block(Block(2, time.time(), "Block 2 Data"))
        blockchain.nodes.append(node)
        self.assertFalse(blockchain.consensus())

    def test_consensus_empty_nodes_list(self):
        blockchain = Blockchain(difficulty=4)
        self.assertFalse(blockchain.consensus())

    def test_consensus_single_node(self):
        blockchain = Blockchain(difficulty=4)
        blockchain.add_block(Block(1, time.time(), "Block 1 Data"))
        node = Blockchain(difficulty=4)
        blockchain.nodes.append(node)
        self.assertTrue(blockchain.consensus())


if __name__ == '__main__':
    unittest.main()
