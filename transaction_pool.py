#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a transaction_pool and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

import queue

class TransactionPool:
    def __init__(self):
        self.pending_transactions = []
        self.transaction_queue = queue.PriorityQueue()

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        self.transaction_queue.put(transaction)

    def get_pending_transactions(self):
        return self.pending_transactions

    def clear_transactions(self):
        self.pending_transactions = []
        while not self.transaction_queue.empty():
            self.transaction_queue.get()

    def prioritize_transactions(self):
        # Placeholder for prioritization logic
        pass

    def remove_conflicting_transactions(self, block):
        # Placeholder for removing conflicting transactions
        pass
