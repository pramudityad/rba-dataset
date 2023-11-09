# Define a secret key for encryption
secret_key = 0x5A7B9C4D3E2F1865  # You can change this key to any 64-bit value

def custom_encrypt(data, key):
    encrypted_data = ''
    for char in data:
        encrypted_char = ord(char) ^ (key & 0xFF)
        encrypted_data += chr(encrypted_char)
        key = (key >> 1) | ((key & 1) << 63)  # Rotate the key right by one bit
    return encrypted_data

def custom_decrypt(data, key):
    decrypted_data = ''
    for char in data:
        decrypted_char = ord(char) ^ (key & 0xFF)
        decrypted_data += chr(decrypted_char)
        key = (key >> 1) | ((key & 1) << 63)  # Rotate the key right by one bit
    return decrypted_data

# Sample user IDs
user_id_1 = -4324475583306591935
user_id_2 = -3284137479262433373

# Convert user IDs to strings
user_id_str_1 = str(user_id_1)
user_id_str_2 = str(user_id_2)

# Generate tokens
token_1 = custom_encrypt(user_id_str_1, secret_key)
token_2 = custom_encrypt(user_id_str_2, secret_key)

print(f"User ID 1: {user_id_1}")
print(f"Token 1: {token_1}")

print(f"User ID 2: {user_id_2}")
print(f"Token 2: {token_2}")

# Decode tokens back to user IDs
decoded_user_id_str_1 = custom_decrypt(token_1, secret_key)
decoded_user_id_str_2 = custom_decrypt(token_2, secret_key)

decoded_user_id_1 = int(decoded_user_id_str_1)
decoded_user_id_2 = int(decoded_user_id_str_2)

print(f"Decoded User ID 1: {decoded_user_id_1}")
print(f"Decoded User ID 2: {decoded_user_id_2}")
