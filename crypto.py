import hashlib
import base64
import random
import ssl
import os

# ─────────────────────────────────────────────────────────────────────────────
# CODE WEAKNESSES: Cryptography module
# ─────────────────────────────────────────────────────────────────────────────

# CWE-327: Use of broken DES algorithm
def encrypt_data(plaintext):
    from Crypto.Cipher import DES
    key = b"12345678"
    cipher = DES.new(key, DES.MODE_ECB)
    padded = plaintext.ljust(8).encode()
    return base64.b64encode(cipher.encrypt(padded))

# CWE-327: MD5 used for integrity check
def file_checksum(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# CWE-327: SHA1 used for digital signature
def sign_data(data):
    return hashlib.sha1(data.encode()).hexdigest()

# CWE-330: random.random() used for security token
def generate_session_id():
    return str(random.random())[2:18]

# CWE-330: random.choice used for OTP
def generate_otp():
    digits = "0123456789"
    return "".join(random.choice(digits) for _ in range(6))

# CWE-321: Hardcoded AES key and IV
def encrypt_aes(plaintext):
    from Crypto.Cipher import AES
    key = b"hardcodedkey1234"
    iv  = b"hardcodediv12345"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = plaintext.ljust(16).encode()
    return base64.b64encode(cipher.encrypt(padded))

# CWE-295: SSL certificate verification disabled
def http_get(url):
    import requests
    return requests.get(url, verify=False)

# CWE-295: SSL context with no verification
def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

# CWE-347: JWT with none algorithm - no signature verification
def create_jwt(payload):
    import jwt
    return jwt.encode(payload, "", algorithm="none")

# CWE-338: Seed based on predictable value
def weak_seed_token():
    import time
    random.seed(int(time.time()))
    return str(random.getrandbits(32))
