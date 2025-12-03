from cryptography.fernet import Fernet
import hashlib
import base64
import secrets
import string

def derive_key(master_password: str) -> bytes:
    sha = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(sha)

def encrypt(master_password: str, plaintext: str) -> str:
    key = derive_key(master_password)
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()

def decrypt(master_password: str, ciphertext: str) -> str:
    key = derive_key(master_password)
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()

def generate_password(length=16) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

