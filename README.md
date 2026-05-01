# 🔐 Secure Coding Review — CodeAlpha Internship Task 3

A Python security code review project that identifies and remediates common vulnerabilities using **Bandit**, a static analysis tool for Python.

---

## 📁 Project Structure

```
CodeAlpha_SecureCodingReview/
├── vulnerable_app.py     ← Intentionally insecure Python app (for audit)
├── secure_app.py         ← Fully remediated secure version
├── bandit_report.txt     ← Raw output from Bandit static analyzer
├── findings_report.md    ← Detailed vulnerability report with fixes
└── README.md             ← This file
```

---

## 🛠 Tool Used

**Bandit** — Python Static Application Security Testing (SAST)

```bash
pip install bandit
bandit vulnerable_app.py
```

---

## 🚨 Vulnerabilities Found (7 Total)

| Severity | Count | Examples |
|----------|-------|---------|
| 🔴 High   | 2     | Command Injection, Weak MD5 Hashing |
| 🟠 Medium | 2     | SQL Injection, Insecure Deserialization |
| 🟡 Low    | 3     | Hard-coded Credentials, Path Traversal, Log Exposure |

---

## 🔍 Key Findings

### 1. Command Injection
```python
# ❌ Vulnerable
subprocess.run("ping -c 1 " + hostname, shell=True)

# ✅ Fixed
subprocess.run(["ping", "-c", "1", hostname], shell=False)
```

### 2. SQL Injection
```python
# ❌ Vulnerable
query = "SELECT * FROM users WHERE username = '" + username + "'"

# ✅ Fixed
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### 3. Weak Hashing
```python
# ❌ Vulnerable
hashlib.md5(password.encode()).hexdigest()

# ✅ Fixed
hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations=260_000)
```

### 4. Insecure Deserialization
```python
# ❌ Vulnerable
pickle.loads(session_data)

# ✅ Fixed
json.loads(session_data)
```

### 5. Hard-coded Credentials
```python
# ❌ Vulnerable
SECRET_KEY = "admin123"

# ✅ Fixed
SECRET_KEY = os.environ.get("SECRET_KEY")
```

---

## 📖 Full Report

See [`findings_report.md`](./findings_report.md) for the complete analysis with CWE references and detailed remediation steps.

---

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Bandit Docs](https://bandit.readthedocs.io/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

## 👤 Author

**elidsimo** — CodeAlpha Cybersecurity Intern
