import os

# ─────────────────────────────────────────────────────────────────────────────
# CODE WEAKNESSES: Hardcoded secrets and insecure configuration
# ─────────────────────────────────────────────────────────────────────────────

# CWE-798: Hardcoded AWS credentials
AWS_ACCESS_KEY_ID     = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION            = "eu-central-1"

# CWE-798: Hardcoded database password
DB_HOST     = "10.10.10.50"
DB_PORT     = 5432
DB_NAME     = "appdb"
DB_USER     = "dbadmin"
DB_PASSWORD = "P@ssw0rd-Lab2024"
DATABASE_URL = "postgresql://dbadmin:P@ssw0rd-Lab2024@10.10.10.50:5432/appdb"

# CWE-798: Hardcoded JWT and session secrets
SECRET_KEY    = "flask-secret-key-hardcoded-abc123"
JWT_SECRET    = "jwt-signing-secret-xyz789"
SESSION_KEY   = "session-encryption-key-000"

# CWE-798: Third party API keys committed to source
STRIPE_KEY    = "sk_live_FAKE_4eC39HqLyjWDarjtT1zdp7dc"
SENDGRID_KEY  = "SG.FAKE_KEY.3d4Kd9bKjHJH9Jb9"
GITHUB_TOKEN  = "ghp_FAKE1234567890abcdefghijklmnopqrstuvwx"
SLACK_TOKEN   = "xoxb-FAKE-123456789-abcdefghijklmnop"

# CWE-16: Debug mode enabled in production config
DEBUG         = True
TESTING       = False
LOG_LEVEL     = "DEBUG"

# CWE-614: Session cookie missing secure flag
SESSION_COOKIE_SECURE   = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = None
