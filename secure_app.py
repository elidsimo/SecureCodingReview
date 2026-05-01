"""
secure_app.py
-------------
Secure refactored version of vulnerable_app.py.
All vulnerabilities identified in the code review have been remediated.
"""

import sqlite3
import os
import hashlib
import hmac
import secrets
import subprocess
import re
import logging

# FIX 1: No hard-coded credentials — use environment variables
SECRET_KEY  = os.environ.get("SECRET_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
API_KEY     = os.environ.get("API_KEY")

if not SECRET_KEY:
    raise EnvironmentError("SECRET_KEY environment variable is not set.")

# Secure logging — never log sensitive data
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_db_connection():
    """Returns a SQLite connection."""
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            salt     TEXT
        )
    """)
    conn.commit()
    return conn


# FIX 2: Parameterized queries prevent SQL Injection
def login(username: str, password: str) -> bool:
    """Authenticate a user safely using parameterized queries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # GOOD: parameterized query — user input is never concatenated
    cursor.execute("SELECT password, salt FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False

    stored_hash, salt = row
    candidate_hash = hash_password(password, salt)
    # GOOD: constant-time comparison prevents timing attacks
    return hmac.compare_digest(stored_hash, candidate_hash)


# FIX 3: Strong hashing — bcrypt-style using SHA-256 + unique salt
def hash_password(password: str, salt: str = None):
    """Hash a password with SHA-256 and a random salt."""
    if salt is None:
        salt = secrets.token_hex(32)          
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations=260_000                   
    ).hex()
    return hashed, salt


# FIX 4: No shell=True — validated input prevents Command Injection
VALID_HOSTNAME = re.compile(r"^[a-zA-Z0-9.\-]{1,253}$")

def ping_host(hostname: str) -> str:
    """Ping a host safely — input validated, shell=False."""
    if not VALID_HOSTNAME.match(hostname):
        raise ValueError(f"Invalid hostname: {hostname}")
    # GOOD: list form + shell=False — no shell injection possible
    result = subprocess.run(["ping", "-c", "1", hostname], shell=False, capture_output=True, text=True, timeout=5)
    return result.stdout


# FIX 5: Path sanitisation prevents Path Traversal
UPLOAD_DIR = "/var/www/uploads"

def read_file(filename: str) -> str:
    """Read a file safely — path traversal prevented."""
    # GOOD: resolve the real path and verify it stays inside UPLOAD_DIR
    safe_path = os.path.realpath(os.path.join(UPLOAD_DIR, filename))
    if not safe_path.startswith(os.path.realpath(UPLOAD_DIR) + os.sep):
        raise PermissionError("Access denied: path traversal detected.")
    with open(safe_path, "r") as f:
        return f.read()


# FIX 6: Replace pickle with JSON — safe deserialization
import json

def load_user_session(session_data: str) -> dict:
    """Load user session from JSON — no arbitrary code execution."""
    # GOOD: json.loads only parses data, never executes code
    return json.loads(session_data)


# FIX 7: Never log plaintext passwords #
def create_user(username: str, password: str) -> None:
    """Create a new user account securely."""
    conn = get_db_connection()
    hashed, salt = hash_password(password)
    logger.info("Creating user: %s", username)   
    try:
        conn.execute(
            "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
            (username, hashed, salt)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        logger.warning("User %s already exists.", username)
    finally:
        conn.close()


# Simple demo entry point #
if __name__ == "__main__":
    create_user("alice", "mypassword")
    result = login("alice", "mypassword")
    print("Login result:", result)
    print(ping_host("127.0.0.1"))
