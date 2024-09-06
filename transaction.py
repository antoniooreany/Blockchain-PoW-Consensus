#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a transaction and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
import hashlib


class Transaction:
    def __init__(self, from_address, to_address, amount, fee, nonce, type, signature=''):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.fee = fee
        self.nonce = nonce
        self.type = type
        self.signature = signature

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.from_address) + str(self.to_address) + str(self.amount) + str(self.fee) + str(self.nonce) + str(self.type)).encode('utf-8'))
        return sha.hexdigest()

    def sign_transaction(self, signing_key):
        # Placeholder for signing logic
        pass

    def is_valid(self):
        # Placeholder for transaction validation
        return True

    def serialize(self):
        # Placeholder for serialization logic
        pass

    def deserialize(self, data):
        # Placeholder for deserialization logic
        pass
