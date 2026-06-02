# CyberArk PVWA connection settings
PVWA_URL = "https://pvwa.example.com"  # Replace with your PVWA URL
AUTH_TYPE = "CyberArk"                 # Options: CyberArk, LDAP, RADIUS
VERIFY_SSL = False                     # Set True in production

# Password health thresholds (days)
OVERDUE_DAYS = 90       # Flag as overdue if not changed in this many days
WARNING_DAYS = 60       # Flag as warning if not changed in this many days

# Report settings
REPORT_OUTPUT_DIR = "output"
REPORT_FILENAME = "password_health_report.html"

# Optional: Email settings (leave empty to skip)
SMTP_SERVER = ""
SMTP_PORT = 587
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
EMAIL_FROM = ""
EMAIL_TO = []           # List of recipient emails
EMAIL_SUBJECT = "CyberArk Password Health Report"

# Optional: Slack webhook (leave empty to skip)
SLACK_WEBHOOK_URL = ""
