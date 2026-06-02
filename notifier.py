"""
Optional email and Slack notifications for the dashboard.
"""
import smtplib
import json
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import (SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD,
                    EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, SLACK_WEBHOOK_URL)


def send_email(report_path, summary):
    """Send the HTML report as an email attachment."""
    if not SMTP_SERVER or not EMAIL_TO:
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    msg["Subject"] = EMAIL_SUBJECT

    body = f"""CyberArk Password Health Report Summary:

Total Accounts : {summary['total']}
Healthy        : {summary['healthy']}
Warning        : {summary['warning']}
Overdue        : {summary['overdue']}
CPM Errors     : {summary['error']}
Unmanaged      : {summary['unmanaged']}

Please see the attached HTML report for full details.
"""
    msg.attach(MIMEText(body, "plain"))

    with open(report_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename=password_health_report.html")
        msg.attach(attachment)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print("✅ Email sent successfully.")


def send_slack_alert(summary):
    """Send a summary notification to a Slack channel."""
    if not SLACK_WEBHOOK_URL:
        return

    message = {
        "text": f"*CyberArk Password Health Report*\n"
                f"🟢 Healthy: {summary['healthy']}  |  "
                f"🟡 Warning: {summary['warning']}  |  "
                f"🔴 Overdue: {summary['overdue']}  |  "
                f"❌ CPM Errors: {summary['error']}  |  "
                f"⚪ Unmanaged: {summary['unmanaged']}\n"
                f"Total: {summary['total']} accounts audited."
    }

    data = json.dumps(message).encode("utf-8")
    req = urllib.request.Request(SLACK_WEBHOOK_URL, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)
    print("✅ Slack notification sent.")
