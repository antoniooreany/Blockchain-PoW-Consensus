#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a test_broadcast_block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import unittest
from unittest.mock import Mock

from node import Node
from blockchain import Blockchain

class TestBroadcastBlock(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain(difficulty=3)
        self.node = Node("address", self.blockchain)

    # def test_broadcast_block_multiple_nodes(self, mock_receive_block):
    #     # node1 = Node("node1", self.blockchain)
    #     # node2 = Node("node2", self.blockchain)
    #     # self.blockchain.nodes = [node1, node2]
    #     # block = "test_block"
    #     # self.assertTrue(self.node.broadcast_block(block))
    #     # self.assertEqual(node1.receive_block.call_count, 1)
    #     # self.assertEqual(node2.receive_block.call_count, 1)
    #
    #     node1 = Node("node1", self.blockchain)
    #     node2 = Node("node2", self.blockchain)
    #     self.blockchain.nodes = [node1, node2]
    #     block = "test_block"
    #     self.assertTrue(self.node.broadcast_block(block))
    #     mock_receive_block.assert_called_once_with(block)

    def test_broadcast_block_no_nodes(self):
        self.blockchain.nodes = []
        block = "test_block"
        self.assertTrue(self.node.broadcast_block(block))

    # def test_broadcast_block_invalid_block_input(self):
    #     self.blockchain.nodes = [Node("node1", self.blockchain)]
    #     block = None
    #     with self.assertRaises(AttributeError):
    #         self.node.broadcast_block(block)

    # def test_broadcast_block_invalid_node_input(self):
    #     self.blockchain.nodes = [None]
    #     block = "test_block"
    #     with self.assertRaises(AttributeError):
    #         self.node.broadcast_block(block)

    # def test_broadcast_block_multiple_nodes(self):
    #     node1 = Node("node1", self.blockchain)
    #     node2 = Node("node2", self.blockchain)
    #     self.blockchain.nodes = [node1, node2]
    #     block = "test_block"
    #     mock_receive_block = unittest.mock.Mock()
    #     node1.receive_block = mock_receive_block
    #     node2.receive_block = mock_receive_block
    #     self.assertTrue(self.node.broadcast_block(block))
    #     mock_receive_block.assert_called_once_with(block)

    # def test_broadcast_block_multiple_nodes(self):
    #     node1 = Node("node1", self.blockchain)
    #     node2 = Node("node2", self.blockchain)
    #     self.blockchain.nodes = [node1, node2]
    #     block = "test_block"
    #     mock_receive_block = Mock()
    #     node1.receive_block = mock_receive_block
    #     node2.receive_block = mock_receive_block
    #     self.assertTrue(self.node.broadcast_block(block))
    #     mock_receive_block.assert_called_once_with(block)

    def test_broadcast_block_multiple_nodes(self):
        node1 = Node("node1", self.blockchain)
        node2 = Node("node2", self.blockchain)
        self.blockchain.nodes = [node1, node2]
        block = "test_block"
        mock_receive_block = Mock()
        node1.receive_block = mock_receive_block
        node2.receive_block = mock_receive_block
        self.assertTrue(self.node.broadcast_block(block))
        self.assertEqual(mock_receive_block.call_count, 2)  # Expect it to be called twice
        mock_receive_block.assert_any_call(block)  # Check that it was called with the block

if __name__ == '__main__':
    unittest.main()
