import hashlib
import sqlite3
import pickle
import random
import os

# ─────────────────────────────────────────────────────────────────────────────
# CODE WEAKNESSES: Authentication module
# ─────────────────────────────────────────────────────────────────────────────

# CWE-89: SQL Injection - user input concatenated directly into query
def get_user(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

# CWE-89: SQL Injection via format string
def get_user_by_email(email):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = '%s'" % email
    cursor.execute(query)
    return cursor.fetchone()

# CWE-916: Weak password hashing - MD5 with no salt
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# CWE-916: SHA1 also weak for passwords
def hash_password_v2(password):
    return hashlib.sha1(password.encode()).hexdigest()

# CWE-798: Hardcoded backdoor credentials
def check_admin(username, password):
    if username == "admin" and password == "admin123":
        return True
    if username == "backdoor" and password == "Sup3rS3cr3tBackd00r":
        return True
    return False

# CWE-502: Insecure deserialization via pickle
def restore_session(session_bytes):
    return pickle.loads(session_bytes)

# CWE-311: Passwords written to plaintext file
def save_credentials(username, password):
    with open("/var/app/credentials.txt", "a") as f:
        f.write(username + ":" + password + "\n")

# CWE-330: Weak non-cryptographic random for security token
def generate_reset_token():
    return str(random.randint(100000, 999999))

# CWE-321: Hardcoded cryptographic keys and secrets
SECRET_KEY  = "hardcoded-secret-key-abc123"
JWT_SECRET  = "jwt-do-not-share-xyz789"
AWS_KEY     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET  = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "P@ssw0rd-Lab2024"
