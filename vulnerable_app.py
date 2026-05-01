"""
vulnerable_app.py
-----------------
A deliberately insecure Python application for security review purposes.
Contains multiple common security vulnerabilities for educational demonstration.
"""
import sqlite3
import os
import hashlib
import pickle
import subprocess

# VULNERABILITY 1: Hard-coded credentials
SECRET_KEY  = "admin123"
DB_PASSWORD = "root:password123"
API_KEY     = "sk-abc123supersecretapikey"


def get_db_connection():
    """Returns a SQLite connection."""
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    return conn



# VULNERABILITY 2: SQL Injection
def login(username, password):
    """Authenticate a user — SQL injection possible."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # BAD: user input concatenated directly into SQL query
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user is not None


# VULNERABILITY 3: Weak hashing (MD5 with no salt)
def hash_password(password):
    """Hash a password — uses weak MD5 algorithm without salt."""
    return hashlib.md5(password.encode()).hexdigest()   # BAD: MD5 is broken

# VULNERABILITY 4: Command Injection
def ping_host(hostname):
    """Ping a host — shell=True opens command injection."""
    # BAD: hostname is never validated; attacker can inject shell commands
    result = subprocess.run("ping -c 1 " + hostname, shell=True, capture_output=True, text=True)
    return result.stdout


# VULNERABILITY 5: Path Traversal
def read_file(filename):
    """Read a file from the uploads directory — path traversal possible."""
    # BAD: no sanitisation → attacker can pass "../../etc/passwd"
    filepath = "/var/www/uploads/" + filename
    with open(filepath, "r") as f:
        return f.read()


# VULNERABILITY 6: Insecure Deserialization

def load_user_session(session_data):
    """Load user session from serialized data — arbitrary code execution risk."""
    # BAD: pickle.loads on untrusted data allows remote code execution
    return pickle.loads(session_data)


# VULNERABILITY 7: Sensitive data printed to console / logs
def create_user(username, password):
    """Create a new user account."""
    conn = get_db_connection()
    hashed = hash_password(password)
    print(f"[DEBUG] Creating user: {username} with password: {password}")   # BAD: plaintext password in logs
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_user("alice", "mypassword")
    result = login("alice", "mypassword")
    print("Login result:", result)
    print(ping_host("127.0.0.1"))
