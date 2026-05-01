# 🔐 Secure Coding Review

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
bandit -r vulnerable_app.py -f txt -o bandit_report.txt
```

---

## 🚨 Vulnerabilities Found (7 Total)

| Severity | Count | Examples |
|----------|-------|---------|
| 🔴 High   | 2     | Command Injection, Weak MD5 Hashing |
| 🟠 Medium | 2     | SQL Injection, Insecure Deserialization |
| 🟡 Low    | 3     | Hard-coded Credentials, Path Traversal, Log Exposure |



## 📖 Full Report

See [`findings_report.md`](./findings_report.md) for the complete analysis with CWE references and detailed remediation steps.

---

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Bandit Docs](https://bandit.readthedocs.io/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

## 👤 Author

**EL-IDRYSY Mohamed** — CodeAlpha Cybersecurity Intern
