# 🔐 CyberArk Password Health Dashboard

A Python automation tool that audits all privileged accounts in CyberArk PAM, analyzes password health, and generates a clean HTML dashboard report.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![CyberArk](https://img.shields.io/badge/CyberArk-PAM-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 What It Does

- Connects to your CyberArk PVWA via REST API
- Fetches all privileged accounts (with pagination support)
- Analyzes each account's CPM status and days since last password change
- Categorizes accounts as: **Healthy**, **Warning**, **Overdue**, **CPM Error**, or **Unmanaged**
- Generates a dark-themed HTML dashboard report
- Optionally sends the report via **Email** and/or **Slack**

---

## 📁 Project Structure

```
cyberark-password-health-dashboard/
├── main.py                  # Entry point
├── cyberark_api.py          # PVWA REST API wrapper
├── health_checker.py        # Password health analysis logic
├── report_generator.py      # HTML report generator
├── notifier.py              # Email & Slack notifications
├── config.py                # Configuration (URL, thresholds, SMTP, Slack)
├── requirements.txt
├── output/
│   └── password_health_report.html   # Generated report
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/satish2001-max/cyberark-password-health-dashboard.git
cd cyberark-password-health-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure settings
Edit `config.py`:
```python
PVWA_URL = "https://your-pvwa.example.com"
AUTH_TYPE = "CyberArk"   # or "LDAP"
VERIFY_SSL = True        # Set False only for dev/test

OVERDUE_DAYS = 90
WARNING_DAYS = 60
```

---

## 🚀 Usage

### Basic run (all accounts)
```bash
python main.py --username admin
```

### Filter by safe
```bash
python main.py --username admin --safe "Windows-Servers"
```

### Skip notifications
```bash
python main.py --username admin --no-notify
```

### Pass password directly (not recommended for production)
```bash
python main.py --username admin --password "YourPassword"
```

---

## 📊 Health Status Legend

| Status | Meaning |
|--------|---------|
| 🟢 Healthy | CPM managed, changed within warning threshold |
| 🟡 Warning | Not changed in 60+ days |
| 🔴 Overdue | Not changed in 90+ days |
| 🔴 CPM Error | CPM failed to manage this account |
| ⚪ Unmanaged | Automatic management is disabled |
| ⚪ Unknown | Status could not be determined |

---

## 📧 Email & Slack Setup

In `config.py`, fill in your SMTP and/or Slack settings:

```python
# Email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "you@gmail.com"
SMTP_PASSWORD = "your_app_password"
EMAIL_FROM = "you@gmail.com"
EMAIL_TO = ["security@company.com"]

# Slack
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

---

## 🕒 Schedule with Cron (Linux)

Run daily at 8am:
```bash
0 8 * * * cd /opt/dashboard && python main.py --username svc_api --no-notify >> logs/dashboard.log 2>&1
```

---

## 🔒 Security Notes

- Never hardcode passwords — use environment variables or a secrets manager
- Enable SSL verification (`VERIFY_SSL = True`) in production
- Use a dedicated CyberArk service account with read-only safe permissions
- Rotate the API service account password regularly

---

## 📜 License

MIT License — free to use and modify.
