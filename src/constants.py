#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a constants.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


# constants.py
HASH_BIT_LENGTH = 256  # The length of the hash in bits
NONCE_BIT_LENGTH = 32  # The length of the nonce in bits

INITIAL_BIT_DIFFICULTY = 16  # todo use bit_difficulty, better even linear_difficulty
ADJUSTMENT_INTERVAL = 10
TARGET_BLOCK_TIME = 0.1
NUMBER_BLOCKS_TO_ADD = 100

CLAMP_FACTOR = 2  # todo 2 bits; bin: 0b10, hex: 0x2, dec: 2: max adjustment factor
SMALLEST_BIT_DIFFICULTY = 4  # todo 4 bits; bin: 0b0000, hex: 0x0, dec: 0: smallest bit difficulty
