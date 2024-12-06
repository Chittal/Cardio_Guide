from cryptography.fernet import Fernet

# Generate a key and print it (store this securely, e.g., in .env file)
print(Fernet.generate_key().decode())