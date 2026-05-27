# Cortex POC — Vulnerable Python App

> WARNING: Deliberate vulnerabilities for security demo purposes only.

## Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Vulnerable + risky packages |
| `src/auth.py` | SQL injection, weak hashing, hardcoded creds |
| `src/api.py` | Command injection, path traversal, SSRF, XXE |
| `src/crypto.py` | Weak crypto, broken algorithms, disabled SSL |
| `src/storage.py` | Zip slip, path traversal, sensitive data logging |
| `src/network.py` | SSRF, SSL bypass, command injection |
| `src/config.py` | Hardcoded secrets, insecure session config |
| `src/main.py` | Flask app wiring all findings together |
| `tests/test_auth.py` | Secrets in tests, SQL injection in test code |
