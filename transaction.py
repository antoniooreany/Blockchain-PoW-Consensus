#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a transaction and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com

class Transaction:
    def __init__(self, sender, recipient, amount, signature=''):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def sign(self, private_key):
        # Placeholder for signing logic
        pass

    def verify_signature(self, public_key):
        # Placeholder for signature verification
        pass
