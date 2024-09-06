#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a test_broadcast_transaction and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import unittest
from node import Node  # assuming the Node class is defined in node.py

class TestBroadcastTransaction(unittest.TestCase):
    def setUp(self):
        self.node1 = MockNode()
        self.node2 = MockNode()
        self.node3 = MockNode()
        self.blockchain = MockBlockchain([self.node1, self.node2, self.node3])

    def test_broadcast_transaction_to_multiple_nodes(self):
        transaction = "test_transaction"
        self.node1.blockchain = self.blockchain
        self.assertTrue(self.node1.broadcast_transaction(transaction))
        self.assertEqual(self.node1.receive_transaction_call_count, 1)
        self.assertEqual(self.node2.receive_transaction_call_count, 1)
        self.assertEqual(self.node3.receive_transaction_call_count, 1)

    def test_broadcast_transaction_to_single_node(self):
        transaction = "test_transaction"
        self.blockchain.nodes = [self.node1]
        self.node1.blockchain = self.blockchain
        self.assertTrue(self.node1.broadcast_transaction(transaction))
        self.assertEqual(self.node1.receive_transaction_call_count, 1)

    def test_broadcast_transaction_to_no_nodes(self):
        transaction = "test_transaction"
        self.blockchain.nodes = []
        self.node1.blockchain = self.blockchain
        self.assertTrue(self.node1.broadcast_transaction(transaction))

    def test_broadcast_transaction_with_none_transaction(self):
        self.node1.blockchain = self.blockchain
        self.assertTrue(self.node1.broadcast_transaction(None))

    def test_broadcast_transaction_with_non_node_object(self):
        self.blockchain.nodes = ["not_a_node"]
        self.node1.blockchain = self.blockchain
        with self.assertRaises(AttributeError):
            self.node1.broadcast_transaction("test_transaction")

class MockBlockchain:
    def __init__(self, nodes):
        self.nodes = nodes

class MockNode:
    def __init__(self):
        self.blockchain = None
        self.receive_transaction_call_count = 0

    def receive_transaction(self, transaction):
        self.receive_transaction_call_count += 1

    def broadcast_transaction(self, transaction):
        for node in self.blockchain.nodes:
            node.receive_transaction(transaction)
        return True


if __name__ == '__main__':
    unittest.main()
