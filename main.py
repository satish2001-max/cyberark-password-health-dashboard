"""
CyberArk Password Health Dashboard
Entry point — run this script to generate the report.

Usage:
    python main.py --username admin --password YourPassword
    python main.py --username admin --password YourPassword --safe "Windows-Servers"
"""
import argparse
import getpass
import sys
from cyberark_api import logon, logoff, get_accounts
from health_checker import analyze_all
from report_generator import generate_html_report
from notifier import send_email, send_slack_alert
from config import AUTH_TYPE


def parse_args():
    parser = argparse.ArgumentParser(description="CyberArk Password Health Dashboard")
    parser.add_argument("--username", required=True, help="PVWA username")
    parser.add_argument("--password", help="PVWA password (will prompt if not provided)")
    parser.add_argument("--safe", help="Filter by safe name (optional)")
    parser.add_argument("--search", help="Search keyword (optional)")
    parser.add_argument("--no-notify", action="store_true", help="Skip email/Slack notifications")
    return parser.parse_args()


def main():
    args = parse_args()
    password = args.password or getpass.getpass("Enter PVWA password: ")

    token = None
    try:
        print(f"🔐 Authenticating to PVWA as '{args.username}'...")
        token = logon(args.username, password, AUTH_TYPE)
        print("✅ Authenticated successfully.")

        print("📋 Fetching accounts...")
        accounts = get_accounts(token, safe_name=args.safe, search=args.search)
        print(f"   Found {len(accounts)} accounts.")

        print("🔍 Analyzing password health...")
        results, summary = analyze_all(accounts)

        print("\n📊 Summary:")
        print(f"   Total     : {summary['total']}")
        print(f"   Healthy   : {summary['healthy']}")
        print(f"   Warning   : {summary['warning']}")
        print(f"   Overdue   : {summary['overdue']}")
        print(f"   CPM Error : {summary['error']}")
        print(f"   Unmanaged : {summary['unmanaged']}")

        print("\n📄 Generating HTML report...")
        report_path = generate_html_report(results, summary)

        if not args.no_notify:
            send_email(report_path, summary)
            send_slack_alert(summary)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        if token:
            logoff(token)
            print("👋 Logged off.")


if __name__ == "__main__":
    main()
