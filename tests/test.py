# import hashlib
#
# # Input data
# index = 1
# timestamp = 1732396702.8675945
# data = "Block 1 Data"
# previous_hash = "29be884b41c3c7d0412a48d18ae8902d0452f139341a94ec9c8d7b24927cda8a"
# nonce = 3229483838
#
# # Combine the input data into a single string
# input_string = f"{index}{timestamp}{data}{previous_hash}{nonce}"
#
# # Encode the input string using UTF-8
# encoded_input = input_string.encode('utf-8')
#
# # Compute the SHA-256 hash
# hash_object = hashlib.sha256()
# hash_object.update(encoded_input)
# computed_hash = hash_object.hexdigest()
#
# # Print the computed hash
# print(computed_hash)


import hashlib

# Input data
index = 95
timestamp = 1732397439.4279182
data = "Block 95 Data"
previous_hash = "00099c2a13eeb8e4f467687c270de581a805823067056e778324ffef5e759fc0"
nonce = 930958724

# Combine the input data into a single string
input_string = f"{index}{timestamp}{data}{previous_hash}{nonce}"

# Encode the input string using UTF-8
encoded_input = input_string.encode('utf-8')

# Compute the SHA-256 hash
hash_object = hashlib.sha256()
hash_object.update(encoded_input)
computed_hash = hash_object.hexdigest()

# Print the computed hash
print(computed_hash)
