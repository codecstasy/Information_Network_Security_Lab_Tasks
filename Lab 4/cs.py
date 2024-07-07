import os
import time
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Constants for file paths
AES_KEY_FILE = "aes_key.json"
RSA_KEY_FILE = "rsa_key.json"
RSA_PUBLIC_KEY_FILE = "rsa_public_key.pem"
RSA_PRIVATE_KEY_FILE = "rsa_private_key.pem"

# Function to generate and save AES keys
def generate_aes_keys():
    aes_keys = {
        "128": get_random_bytes(16),
        "256": get_random_bytes(32)
    }
    with open(AES_KEY_FILE, 'w') as f:
        json.dump({k: v.hex() for k, v in aes_keys.items()}, f)
    print("AES keys generated and saved.")

# Function to load AES keys
def load_aes_keys():
    with open(AES_KEY_FILE, 'r') as f:
        aes_keys = json.load(f)
    return {k: bytes.fromhex(v) for k, v in aes_keys.items()}

# Function to generate and save RSA keys
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(RSA_PRIVATE_KEY_FILE, 'wb') as f:
        f.write(private_key)
    with open(RSA_PUBLIC_KEY_FILE, 'wb') as f:
        f.write(public_key)
    print("RSA keys generated and saved.")

# Function to load RSA keys
def load_rsa_keys():
    with open(RSA_PRIVATE_KEY_FILE, 'rb') as f:
        private_key = RSA.import_key(f.read())
    with open(RSA_PUBLIC_KEY_FILE, 'rb') as f:
        public_key = RSA.import_key(f.read())
    return private_key, public_key

# AES encryption
def aes_encrypt(mode, key_length, input_text, output_file):
    keys = load_aes_keys()
    key = keys[str(key_length)]
    data = input_text.encode()

    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(data.ljust(16 * ((len(data) + 15) // 16)))
    elif mode == "CFB":
        cipher = AES.new(key, AES.MODE_CFB)
        ciphertext = cipher.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(ciphertext)
    print(f"Encrypted text written to {output_file}.")

# AES decryption
def aes_decrypt(mode, key_length, input_file):
    keys = load_aes_keys()
    key = keys[str(key_length)]

    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    if mode == "ECB":
        cipher = AES.new(key, AES.MODE_ECB)
        data = cipher.decrypt(ciphertext)
    elif mode == "CFB":
        cipher = AES.new(key, AES.MODE_CFB)
        data = cipher.decrypt(ciphertext)

    print(f"Decrypted text: {data.strip().decode()}")

# RSA encryption
def rsa_encrypt(input_text, output_file):
    private_key, public_key = load_rsa_keys()
    data = input_text.encode()

    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(ciphertext)
    print(f"Encrypted text written to {output_file}.")

# RSA decryption
def rsa_decrypt(input_file):
    private_key, public_key = load_rsa_keys()

    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    cipher = PKCS1_OAEP.new(private_key)
    data = cipher.decrypt(ciphertext)

    print(f"Decrypted text: {data.decode()}")

# RSA signing
def rsa_sign(input_text, signature_file):
    private_key, public_key = load_rsa_keys()
    data = input_text.encode()

    h = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(h)

    with open(signature_file, 'wb') as f:
        f.write(signature)
    print(f"Signature written to {signature_file}.")

# RSA signature verification
def rsa_verify(input_text, signature_file):
    private_key, public_key = load_rsa_keys()
    data = input_text.encode()

    with open(signature_file, 'rb') as f:
        signature = f.read()

    h = SHA256.new(data)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        print("RSA signature verification successful.")
    except (ValueError, TypeError):
        print("RSA signature verification failed.")

# SHA-256 hashing
def sha256_hash(input_text):
    data = input_text.encode()
    h = SHA256.new(data).hexdigest()
    print(f"SHA-256 hash: {h}")

# Function to measure and report execution time
def measure_execution_time(func, *args):
    start_time = time.time()
    func(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")

# Command line interface
def main():
    while True:
        print("Choose an option:")
        print("1. Generate AES keys")
        print("2. Generate RSA keys")
        print("3. AES encryption")
        print("4. AES decryption")
        print("5. RSA encryption")
        print("6. RSA decryption")
        print("7. RSA signing")
        print("8. RSA signature verification")
        print("9. SHA-256 hashing")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            generate_aes_keys()
        elif choice == "2":
            generate_rsa_keys()
        elif choice == "3":
            mode = input("Enter AES mode (ECB/CFB): ")
            key_length = int(input("Enter AES key length (128/256): "))
            input_text = input("Enter text to encrypt: ")
            output_file = input("Enter output file name: ")
            measure_execution_time(aes_encrypt, mode, key_length, input_text, output_file)
        elif choice == "4":
            mode = input("Enter AES mode (ECB/CFB): ")
            key_length = int(input("Enter AES key length (128/256): "))
            input_file = input("Enter input file name: ")
            measure_execution_time(aes_decrypt, mode, key_length, input_file)
        elif choice == "5":
            input_text = input("Enter text to encrypt: ")
            output_file = input("Enter output file name: ")
            measure_execution_time(rsa_encrypt, input_text, output_file)
        elif choice == "6":
            input_file = input("Enter input file name: ")
            measure_execution_time(rsa_decrypt, input_file)
        elif choice == "7":
            input_text = input("Enter text to sign: ")
            signature_file = input("Enter signature file name: ")
            measure_execution_time(rsa_sign, input_text, signature_file)
        elif choice == "8":
            input_text = input("Enter text to verify: ")
            signature_file = input("Enter signature file name: ")
            measure_execution_time(rsa_verify, input_text, signature_file)
        elif choice == "9":
            input_text = input("Enter text to hash: ")
            measure_execution_time(sha256_hash, input_text)
        elif choice == "10":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
