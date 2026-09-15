import argparse
import csv
import os
from pathlib import Path

ENDPOINT = "https://graph.microsoft.com/v1.0/me?$select=displayName,jobTitle"

def safe_cell(value):
    text = str(value or "")
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text

def main():
    parser = argparse.ArgumentParser(description="Read-only delegated Graph profile export")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(f"GET {ENDPOINT}; delegated User.Read; output/profile.csv")
        return
    import msal
    import requests
    client_id = os.environ.get("GRAPH_CLIENT_ID", "")
    tenant = os.environ.get("GRAPH_TENANT_ID", "")
    if not client_id or not tenant or "REPLACE" in client_id or "REPLACE" in tenant:
        raise SystemExit("Set local GRAPH_CLIENT_ID and GRAPH_TENANT_ID")
    import uuid
    try:
        uuid.UUID(client_id)
        uuid.UUID(tenant)
    except ValueError:
        raise SystemExit("Client and tenant IDs must be UUIDs")
    client = msal.PublicClientApplication(client_id, authority=f"https://login.microsoftonline.com/{tenant}")
    flow = client.initiate_device_flow(scopes=["User.Read"])
    if "user_code" not in flow:
        raise SystemExit("Could not initiate device login")
    print(flow["message"])
    result = client.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise SystemExit("Authentication failed; check app settings and consent")
    response = requests.get(ENDPOINT, headers={"Authorization": "Bearer " + result["access_token"]}, timeout=30)
    if response.status_code != 200:
        raise SystemExit(f"Graph returned HTTP {response.status_code}; retry later if throttled")
    profile = response.json()
    path = Path("output/profile.csv")
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["displayName", "jobTitle"])
        writer.writerow([safe_cell(profile.get("displayName")), safe_cell(profile.get("jobTitle"))])
    print("Wrote local profile report; it is excluded from Git")

if __name__ == "__main__":
    main()
