import socket
import ssl
import subprocess
import requests
import os

# ─────────────────────────────────────────────────────────────────────────────
# CODE WEAKNESSES: Network and HTTP module
# ─────────────────────────────────────────────────────────────────────────────

# CWE-918: SSRF - fetches any user-supplied URL including internal services
def proxy_request(url):
    response = requests.get(url, timeout=10)
    return response.text

# CWE-918: SSRF to AWS metadata service
def get_aws_credentials():
    r = requests.get("http://169.254.169.254/latest/meta-data/iam/security-credentials/")
    return r.text

# CWE-295: SSL verification disabled globally
def download_file(url, dest):
    r = requests.get(url, verify=False, stream=True)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

# CWE-295: Raw socket with no certificate check
def connect_tls(host, port):
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    sock = socket.create_connection((host, port))
    return ctx.wrap_socket(sock)

# CWE-78: Command injection via hostname parameter
def ping_host(hostname):
    result = subprocess.check_output("ping -c 1 " + hostname, shell=True)
    return result.decode()

# CWE-78: DNS lookup with shell injection
def resolve_host(hostname):
    output = os.popen("nslookup " + hostname).read()
    return output

# CWE-400: No timeout on external request - DoS risk
def fetch_external_resource(url):
    return requests.get(url).content

# CWE-319: Sensitive data sent over HTTP not HTTPS
def send_credentials(username, password):
    requests.post(
        "http://internal-auth.company.com/verify",
        json={"user": username, "pass": password}
    )
