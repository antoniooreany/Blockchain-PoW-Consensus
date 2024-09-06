#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a transaction_pool and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

class TransactionPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def remove_transaction(self, transaction):
        self.transactions.remove(transaction)

    def get_transactions(self):
        return self.transactions

    def clear_transactions(self):
        self.transactions = []
