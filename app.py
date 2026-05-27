from flask import Flask, request, jsonify, redirect
import sqlite3
import subprocess
import os
import pickle
import hashlib
import yaml

app = Flask(__name__)

# Hardcoded secret key - CWE-798
app.secret_key = "hardcoded-flask-secret-abc123"

# CWE-89: SQL Injection
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return jsonify(cur.fetchall())

# CWE-78: Command Injection
@app.route("/run")
def run_cmd():
    cmd = request.args.get("cmd", "")
    output = subprocess.check_output(cmd, shell=True)
    return output

# CWE-22: Path Traversal
@app.route("/file")
def read_file():
    filename = request.args.get("name", "")
    with open("/var/app/" + filename, "r") as f:
        return f.read()

# CWE-502: Insecure Deserialization
@app.route("/session", methods=["POST"])
def restore():
    return str(pickle.loads(request.data))

# CWE-918: SSRF
@app.route("/fetch")
def fetch():
    import requests
    url = request.args.get("url", "")
    return requests.get(url).text

# CWE-601: Open Redirect
@app.route("/redirect")
def open_redirect():
    return redirect(request.args.get("next", "/"))

# CWE-916: Weak password hashing
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    pw_hash = hashlib.md5(data["password"].encode()).hexdigest()
    return jsonify({"hash": pw_hash})

# CWE-502: YAML unsafe load
@app.route("/config", methods=["POST"])
def load_config():
    return jsonify(yaml.load(request.data))

# CWE-215: Debug endpoint
@app.route("/debug")
def debug():
    return jsonify(dict(os.environ))

# CWE-798: Hardcoded credentials
DB_PASSWORD = "P@ssw0rd-Lab2024"
AWS_KEY     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET  = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
JWT_SECRET  = "jwt-secret-xyz789"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
