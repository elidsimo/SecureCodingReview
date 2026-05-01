# Secure Coding Review — Findings Report
**Project:** vulnerable_app.py  
**Reviewer:** EL-IDRYSY Mohamed  
**Date:** 2026-05-01  
**Tool used:** Bandit 1.9.4  

---

## Summary
7 vulnerabilities were identified and fixed in the 
Python application.

| # | Vulnerability | Severity | Status |
|---|--------------|----------|--------|
| 1 | Hard-coded Credentials | HIGH | ✅ Fixed |
| 2 | SQL Injection | HIGH | ✅ Fixed |
| 3 | Weak Hashing (MD5) | HIGH | ✅ Fixed |
| 4 | Command Injection | HIGH | ✅ Fixed |
| 5 | Path Traversal | MEDIUM | ✅ Fixed |
| 6 | Insecure Deserialization | HIGH | ✅ Fixed |
| 7 | Sensitive Data in Logs | MEDIUM | ✅ Fixed |

---

## Detailed Findings

### VULN-01: Hard-coded Credentials
- **Location:** Lines 14-16
- **Risk:** Credentials exposed in source code
- **Fix:** Use environment variables with os.environ.get()

### VULN-02: SQL Injection
- **Location:** Line 41
- **Risk:** Attacker can bypass authentication
- **Fix:** Use parameterized queries with ?

### VULN-03: Weak Hashing (MD5)
- **Location:** Line 51
- **Risk:** MD5 is broken, passwords easily cracked
- **Fix:** Use SHA-256 with random salt (secrets)

### VULN-04: Command Injection
- **Location:** Line 57
- **Risk:** Attacker can execute shell commands
- **Fix:** Use shell=False, validate input with whitelist

### VULN-05: Path Traversal
- **Location:** Line 65
- **Risk:** Attacker can read /etc/passwd or any file
- **Fix:** Use os.path.realpath() to validate path

### VULN-06: Insecure Deserialization
- **Location:** Line 75
- **Risk:** pickle allows remote code execution
- **Fix:** Replace pickle with json.loads()

### VULN-07: Sensitive Data in Logs
- **Location:** Line 83
- **Risk:** Passwords printed in plain text to console
- **Fix:** Log only username, never the password

---

## Tools Used
- **Bandit 1.9.4** — Static analysis
- **Manual Review** — Code inspection

## Conclusion
All 7 vulnerabilities have been identified and 
remediated. The secure version follows OWASP 
secure coding best practices.
