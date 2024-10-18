#   Copyright (c) 2024, Anton Gorshkov
#   All rights reserved.
#
#   This code is for a helpers.py and its unit tests.
#   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com


# helpers.py
def clamp(log_adjustment_factor: float, clamp_factor: float) -> float:
    if log_adjustment_factor > clamp_factor:
        log_adjustment_factor = clamp_factor
    elif log_adjustment_factor < -clamp_factor:
        log_adjustment_factor = -clamp_factor
    return log_adjustment_factor


def collect_filtered_bit_difficulties(blockchain, adjustment_interval):
    filtered_bit_difficulties = []
    for i, difficulty in enumerate(blockchain.bit_difficulties):
        if (i + 1) % adjustment_interval != 0:
            filtered_bit_difficulties.append(difficulty)
    return filtered_bit_difficulties