from flask import Flask, request, jsonify, redirect
from src.auth import get_user, hash_password, restore_session, check_admin
from src.api import read_file, fetch_url, debug_info, search_products
from src.storage import download_file, extract_archive, log_transaction
from src.crypto import encrypt_data, generate_session_id, http_get

app = Flask(__name__)

# CWE-16: Debug mode on in production
app.debug = True

# CWE-614: Insecure session cookie config
app.config["SECRET_KEY"]            = "hardcoded-key-abc123"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = False

@app.route("/login", methods=["POST"])
def login():
    data    = request.json
    user    = get_user(data.get("username"))
    pw_hash = hash_password(data.get("password"))
    return jsonify({"user": str(user), "hash": pw_hash})

@app.route("/file")
def get_file():
    # CWE-22: Path traversal via query param
    filename = request.args.get("name", "")
    return read_file(filename)

@app.route("/fetch")
def fetch():
    # CWE-918: SSRF
    url = request.args.get("url", "")
    return fetch_url(url)

@app.route("/session/restore", methods=["POST"])
def session_restore():
    # CWE-502: Insecure deserialization
    return jsonify(str(restore_session(request.data)))

@app.route("/search")
def search():
    # CWE-89: SQL injection
    keyword  = request.args.get("q", "")
    category = request.args.get("cat", "")
    return jsonify(search_products(keyword, category))

@app.route("/redirect")
def do_redirect():
    # CWE-601: Open redirect
    return redirect(request.args.get("next", "/"))

@app.route("/debug")
def debug():
    # CWE-215: Exposes all env vars
    return jsonify(debug_info())

@app.route("/upload/extract", methods=["POST"])
def upload_extract():
    # CWE-22: Zip slip
    f = request.files.get("archive")
    f.save("/tmp/upload.tar.gz")
    extract_archive("/tmp/upload.tar.gz", "/var/app/uploads/")
    return jsonify({"status": "extracted"})

@app.route("/pay", methods=["POST"])
def pay():
    data = request.json
    # CWE-312: Credit card logged in plaintext
    log_transaction(data["user"], data["card"], data["amount"])
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
