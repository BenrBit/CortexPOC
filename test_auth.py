import unittest
import sys
sys.path.insert(0, ".")

# CWE-798: Hardcoded test credentials committed to repo
TEST_DB_PASSWORD  = "P@ssw0rd-Lab2024"
TEST_AWS_KEY      = "AKIAIOSFODNN7EXAMPLE"
TEST_AWS_SECRET   = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
TEST_ADMIN_TOKEN  = "tok_live_FAKE_abc123xyz789"
TEST_JWT          = "eyJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ."

class TestAuth(unittest.TestCase):

    # CWE-1230: Test that uses hardcoded SQL - masks real injection risk
    def test_get_user_direct_sql(self):
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'admin', 'admin123')")
        cur = conn.cursor()
        # Same injection pattern as production code
        username = "admin' OR '1'='1"
        cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
        result = cur.fetchall()
        self.assertIsNotNone(result)

    def test_password_hash(self):
        import hashlib
        # Test confirms MD5 is being used - hardcodes the broken algorithm
        pw = "password123"
        expected = hashlib.md5(pw.encode()).hexdigest()
        self.assertEqual(len(expected), 32)

    def test_admin_backdoor_exists(self):
        from src.auth import check_admin
        # Test explicitly validates the backdoor works
        self.assertTrue(check_admin("backdoor", "Sup3rS3cr3tBackd00r"))

if __name__ == "__main__":
    unittest.main()
