"""
CyberArk REST API wrapper for Password Health Dashboard.
"""
import requests
import urllib3
from config import PVWA_URL, VERIFY_SSL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }


def logon(username, password, auth_type="CyberArk"):
    """Authenticate and return session token."""
    url = f"{PVWA_URL}/PasswordVault/API/auth/{auth_type}/Logon"
    payload = {"username": username, "password": password, "concurrentSession": True}
    response = requests.post(url, json=payload, verify=VERIFY_SSL)
    response.raise_for_status()
    return response.text.strip('"')


def logoff(token):
    """Terminate the session."""
    url = f"{PVWA_URL}/PasswordVault/API/auth/Logoff"
    requests.post(url, headers=get_headers(token), verify=VERIFY_SSL)


def get_all_safes(token):
    """Return list of all safes."""
    url = f"{PVWA_URL}/PasswordVault/API/Safes"
    safes = []
    params = {"limit": 100, "offset": 0}

    while True:
        response = requests.get(url, headers=get_headers(token), params=params, verify=VERIFY_SSL)
        response.raise_for_status()
        data = response.json()
        batch = data.get("value", [])
        safes.extend(batch)
        if len(batch) < 100:
            break
        params["offset"] += 100

    return safes


def get_accounts(token, safe_name=None, search=None):
    """Return all accounts, optionally filtered by safe or keyword."""
    url = f"{PVWA_URL}/PasswordVault/API/Accounts"
    accounts = []
    params = {"limit": 100, "offset": 0}

    if safe_name:
        params["filter"] = f"safeName eq {safe_name}"
    if search:
        params["search"] = search

    while True:
        response = requests.get(url, headers=get_headers(token), params=params, verify=VERIFY_SSL)
        response.raise_for_status()
        data = response.json()
        batch = data.get("value", [])
        accounts.extend(batch)
        if len(batch) < 100:
            break
        params["offset"] += 100

    return accounts
