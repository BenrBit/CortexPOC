import subprocess
import os
import yaml
import xml.etree.ElementTree as ET
import sqlite3
import requests
import tempfile

# ─────────────────────────────────────────────────────────────────────────────
# CODE WEAKNESSES: API handlers
# ─────────────────────────────────────────────────────────────────────────────

# CWE-78: Command injection - user input passed directly to shell
def run_report(report_name):
    cmd = "python3 reports/" + report_name + ".py"
    return subprocess.check_output(cmd, shell=True)

# CWE-78: Command injection via os.system
def convert_file(filename, fmt):
    os.system("convert uploads/" + filename + " output." + fmt)

# CWE-22: Path traversal - no sanitization on file path
def read_file(filename):
    base = "/var/app/uploads/"
    with open(base + filename, "r") as f:
        return f.read()

# CWE-22: Path traversal in file write
def write_report(name, content):
    path = "/var/reports/" + name
    with open(path, "w") as f:
        f.write(content)

# CWE-611: XXE - XML parsed with external entities enabled
def parse_config(xml_string):
    from lxml import etree
    parser = etree.XMLParser(resolve_entities=True)
    return etree.fromstring(xml_string.encode(), parser)

# CWE-502: Unsafe YAML deserialization
def load_config(yaml_string):
    return yaml.load(yaml_string)

# CWE-918: SSRF - user controlled URL fetched server side
def fetch_url(url):
    return requests.get(url, timeout=5).text

# CWE-918: SSRF to internal metadata service
def get_instance_metadata():
    return requests.get("http://169.254.169.254/latest/meta-data/").text

# CWE-377: Predictable temp file - race condition risk
def process_upload(data, user_ip):
    tmp_path = "/tmp/upload_" + user_ip
    with open(tmp_path, "wb") as f:
        f.write(data)
    return tmp_path

# CWE-601: Open redirect - no URL validation
def redirect_after_login(next_url):
    from flask import redirect
    return redirect(next_url)

# CWE-215: Debug endpoint exposes environment variables
def debug_info():
    return {
        "env": dict(os.environ),
        "cwd": os.getcwd(),
        "user": os.getenv("USER")
    }

# CWE-89: SQL injection in search
def search_products(keyword, category):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    query = "SELECT * FROM products WHERE name LIKE '%" + keyword + "%' AND category='" + category + "'"
    cur.execute(query)
    return cur.fetchall()
