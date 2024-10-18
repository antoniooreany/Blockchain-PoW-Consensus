#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a block and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


import hashlib


class Block:
    def __init__(
            self,
            index: int,
            timestamp: float,
            data: str,
            previous_hash: str = '',
    ) -> None:
        self.index: int = index
        self.timestamp: float = timestamp
        self.data: str = data
        self.previous_hash: str = previous_hash
        self.nonce: int = 0
        self.hash: str = self.calculate_hash()

    def calculate_hash(self) -> str:
        sha: hashlib.sha256 = hashlib.sha256()
        sha.update(
            (str(self.index) +
             str(self.timestamp) +
             str(self.data) +
             str(self.previous_hash) +
             str(self.nonce))
            .encode('utf-8'))
        return sha.hexdigest()
