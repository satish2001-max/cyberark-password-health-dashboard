"""
Password health analysis logic.
"""
import datetime
from config import OVERDUE_DAYS, WARNING_DAYS


def analyze_account(account):
    """
    Analyze a single account and return its health status and details.
    """
    mgmt = account.get("secretManagement", {})
    status = mgmt.get("status", "unknown").lower()
    last_modified_ts = mgmt.get("lastModifiedTime", None)
    auto_mgmt_enabled = mgmt.get("automaticManagementEnabled", False)

    now = datetime.datetime.now()
    last_changed = None
    days_since_change = None

    if last_modified_ts:
        last_changed = datetime.datetime.fromtimestamp(last_modified_ts)
        days_since_change = (now - last_changed).days

    # Determine health label
    if not auto_mgmt_enabled:
        health = "unmanaged"
        health_label = "⚪ Unmanaged"
    elif status == "failure":
        health = "error"
        health_label = "🔴 CPM Error"
    elif days_since_change is not None and days_since_change >= OVERDUE_DAYS:
        health = "overdue"
        health_label = f"🔴 Overdue ({days_since_change}d)"
    elif days_since_change is not None and days_since_change >= WARNING_DAYS:
        health = "warning"
        health_label = f"🟡 Warning ({days_since_change}d)"
    elif status == "success":
        health = "healthy"
        health_label = "🟢 Healthy"
    else:
        health = "unknown"
        health_label = "⚪ Unknown"

    return {
        "id": account.get("id", ""),
        "username": account.get("userName", ""),
        "address": account.get("address", ""),
        "safe": account.get("safeName", ""),
        "platform": account.get("platformId", ""),
        "cpm_status": status,
        "auto_managed": auto_mgmt_enabled,
        "last_changed": last_changed.strftime("%Y-%m-%d %H:%M") if last_changed else "Never",
        "days_since_change": days_since_change if days_since_change is not None else "N/A",
        "health": health,
        "health_label": health_label,
    }


def analyze_all(accounts):
    """Analyze all accounts and return results + summary stats."""
    results = [analyze_account(a) for a in accounts]

    summary = {
        "total": len(results),
        "healthy": sum(1 for r in results if r["health"] == "healthy"),
        "warning": sum(1 for r in results if r["health"] == "warning"),
        "overdue": sum(1 for r in results if r["health"] == "overdue"),
        "error": sum(1 for r in results if r["health"] == "error"),
        "unmanaged": sum(1 for r in results if r["health"] == "unmanaged"),
        "unknown": sum(1 for r in results if r["health"] == "unknown"),
    }

    # Sort: errors and overdue first
    priority = {"error": 0, "overdue": 1, "warning": 2, "unknown": 3, "unmanaged": 4, "healthy": 5}
    results.sort(key=lambda x: priority.get(x["health"], 99))

    return results, summary
