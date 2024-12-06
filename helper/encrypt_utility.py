import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load the .env file (if using dotenv)
load_dotenv()

class SimpleEncryptor:
    def __init__(self):
        # Load the encryption key from the environment variable
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            raise ValueError("Encryption key not found in environment variable.")
        self.fernet = Fernet(self.key)

    def encrypt(self, plaintext):
        """
        Encrypt plaintext string and return encrypted bytes.
        """
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        """
        Decrypt ciphertext bytes and return plaintext string.
        """
        return self.fernet.decrypt(ciphertext.encode()).decode()
