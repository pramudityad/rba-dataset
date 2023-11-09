import hashlib

def generate_sha512_hash(input_string):
    sha512_hash = hashlib.sha512()
    sha512_hash.update(input_string.encode('utf-8'))
    return sha512_hash.hexdigest()

if __name__ == '__main__':
    input_string = input("Enter the string to generate SHA-512 hash for: ")
    sha512_hash = generate_sha512_hash(input_string)
    print(f'SHA-512 Hash: {sha512_hash}')