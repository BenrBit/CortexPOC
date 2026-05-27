import os
import subprocess
import tarfile
import sqlite3

# ─────────────────────────────────────────────────────────────────────────────
# CODE WEAKNESSES: File storage and database module
# ─────────────────────────────────────────────────────────────────────────────

# CWE-22: Path traversal in file download
def download_file(filename):
    base = "/var/app/files/"
    filepath = base + filename
    with open(filepath, "rb") as f:
        return f.read()

# CWE-22: Zip slip - tar extraction without member path check
def extract_archive(archive_path, dest):
    with tarfile.open(archive_path) as tar:
        tar.extractall(path=dest)

# CWE-78: Command injection in file processing
def process_image(filename):
    cmd = "convert " + filename + " -resize 100x100 thumb_" + filename
    subprocess.call(cmd, shell=True)

# CWE-89: SQL injection in file metadata query
def get_file_metadata(file_id):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM files WHERE id = " + file_id)
    return cur.fetchone()

# CWE-732: File created with overly permissive mode
def save_upload(filename, data):
    path = "/var/app/uploads/" + filename
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o777)

# CWE-73: External control of file name
def load_template(template_name):
    template_dir = "/var/app/templates/"
    with open(template_dir + template_name) as f:
        return f.read()

# CWE-400: No limit on file size - potential DoS
def read_user_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

# CWE-312: Sensitive data written to log in plaintext
def log_transaction(user, card_number, amount):
    with open("/var/log/transactions.log", "a") as f:
        f.write("user=" + user + " card=" + card_number + " amount=" + str(amount) + "\n")
