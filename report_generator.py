"""
HTML report generator for Password Health Dashboard.
"""
import os
import datetime
from config import REPORT_OUTPUT_DIR, REPORT_FILENAME, OVERDUE_DAYS, WARNING_DAYS


def generate_html_report(results, summary):
    """Generate a full HTML report and save to output directory."""
    os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(REPORT_OUTPUT_DIR, REPORT_FILENAME)
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = ""
    for r in results:
        color_class = {
            "healthy": "healthy",
            "warning": "warning",
            "overdue": "overdue",
            "error": "error",
            "unmanaged": "unmanaged",
            "unknown": "unknown",
        }.get(r["health"], "unknown")

        rows += f"""
        <tr class="{color_class}">
            <td>{r['username']}</td>
            <td>{r['address']}</td>
            <td>{r['safe']}</td>
            <td>{r['platform']}</td>
            <td>{r['last_changed']}</td>
            <td>{r['days_since_change']}</td>
            <td>{r['health_label']}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CyberArk Password Health Dashboard</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f1117; color: #e0e0e0; }}
    header {{ background: #1a1d27; padding: 24px 40px; border-bottom: 2px solid #00b4d8; }}
    header h1 {{ font-size: 24px; color: #00b4d8; }}
    header p {{ color: #888; font-size: 13px; margin-top: 4px; }}
    .container {{ padding: 32px 40px; }}

    .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin-bottom: 32px; }}
    .stat-card {{ background: #1a1d27; border-radius: 10px; padding: 20px; text-align: center; border: 1px solid #2a2d3a; }}
    .stat-card .number {{ font-size: 36px; font-weight: bold; }}
    .stat-card .label {{ font-size: 12px; color: #888; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }}
    .stat-card.total .number {{ color: #00b4d8; }}
    .stat-card.healthy .number {{ color: #4caf50; }}
    .stat-card.warning .number {{ color: #ff9800; }}
    .stat-card.overdue .number {{ color: #f44336; }}
    .stat-card.error .number {{ color: #e91e63; }}
    .stat-card.unmanaged .number {{ color: #9e9e9e; }}

    .section-title {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #ccc; border-left: 3px solid #00b4d8; padding-left: 12px; }}
    .thresholds {{ background: #1a1d27; border-radius: 8px; padding: 16px 20px; margin-bottom: 24px; font-size: 13px; color: #aaa; border: 1px solid #2a2d3a; }}
    .thresholds span {{ margin-right: 24px; }}

    .table-wrapper {{ overflow-x: auto; border-radius: 10px; border: 1px solid #2a2d3a; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    thead {{ background: #1a1d27; }}
    thead th {{ padding: 12px 16px; text-align: left; color: #00b4d8; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }}
    tbody tr {{ border-bottom: 1px solid #1e2130; transition: background 0.15s; }}
    tbody tr:hover {{ background: #1e2130; }}
    tbody td {{ padding: 11px 16px; }}

    tr.healthy td:last-child {{ color: #4caf50; font-weight: 600; }}
    tr.warning td:last-child {{ color: #ff9800; font-weight: 600; }}
    tr.overdue td:last-child {{ color: #f44336; font-weight: 600; }}
    tr.error td:last-child {{ color: #e91e63; font-weight: 600; }}
    tr.unmanaged td:last-child {{ color: #9e9e9e; font-weight: 600; }}
    tr.unknown td:last-child {{ color: #777; font-weight: 600; }}

    footer {{ text-align: center; padding: 24px; color: #444; font-size: 12px; }}
  </style>
</head>
<body>
  <header>
    <h1>🔐 CyberArk Password Health Dashboard</h1>
    <p>Generated: {generated_at} &nbsp;|&nbsp; Thresholds: Warning ≥{WARNING_DAYS} days &nbsp;|&nbsp; Overdue ≥{OVERDUE_DAYS} days</p>
  </header>

  <div class="container">
    <div class="summary-grid">
      <div class="stat-card total"><div class="number">{summary['total']}</div><div class="label">Total Accounts</div></div>
      <div class="stat-card healthy"><div class="number">{summary['healthy']}</div><div class="label">Healthy</div></div>
      <div class="stat-card warning"><div class="number">{summary['warning']}</div><div class="label">Warning</div></div>
      <div class="stat-card overdue"><div class="number">{summary['overdue']}</div><div class="label">Overdue</div></div>
      <div class="stat-card error"><div class="number">{summary['error']}</div><div class="label">CPM Errors</div></div>
      <div class="stat-card unmanaged"><div class="number">{summary['unmanaged']}</div><div class="label">Unmanaged</div></div>
    </div>

    <div class="section-title">Account Details</div>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>Address</th>
            <th>Safe</th>
            <th>Platform</th>
            <th>Last Changed</th>
            <th>Days Since Change</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
  </div>

  <footer>CyberArk Password Health Dashboard &mdash; For internal security use only</footer>
</body>
</html>"""

    with open(filepath, "w") as f:
        f.write(html)

    print(f"✅ Report saved to: {filepath}")
    return filepath
