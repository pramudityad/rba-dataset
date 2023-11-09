import hashlib

def generate_sha512_hash(input_string):
    sha512_hash = hashlib.sha512()
    sha512_hash.update(input_string.encode('utf-8'))
    return sha512_hash.hexdigest()

def verify_sha512_hash(input_string, stored_hash):
    generated_hash = generate_sha512_hash(input_string)
    return generated_hash == stored_hash

if __name__ == '__main__':
    input_string = input("Enter the string: ")
    stored_hash = input("Enter the SHA-512 hash to verify against: ")

    if verify_sha512_hash(input_string, stored_hash):
        print("Hashes match. The input string is valid.")
    else:
        print("Hashes do not match. The input string is invalid.")