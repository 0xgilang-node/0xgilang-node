#!/usr/bin/env python3
"""
GitHub Actions scheduled update — pushes updated timestamp to profile README
Run via GitHub Actions cron: every day at 23:00 UTC = 06:00 WIB
"""
import base64
import datetime
import os
import urllib.request
import urllib.error
import json

USERNAME = os.environ.get("GITHUB_ACTOR", "0xgilang-node")
TOKEN = os.environ.get("GH_PAT")
REPO = USERNAME
BRANCH = "main"
README_PATH = "README.md"

def api(method, path, data=None):
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Portfolio-Auto-Update"
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(), "status": e.code}

# Get current README
result = api("GET", f"/repos/{USERNAME}/{REPO}/contents/{README_PATH}?ref={BRANCH}")
if "error" in result:
    print(f"❌ Error: {result['error']}")
    exit(1)

sha = result["sha"]
content = base64.b64decode(result["content"]).decode()

# Update timestamp
tz = datetime.timezone(datetime.timedelta(hours=7))
now = datetime.datetime.now(tz)
date_str = now.strftime("%d %b %Y %H:%M %Z")

new_content = content.replace(
    "UPDATED_AT",
    f"{date_str} [auto]"
)

# Push
update_data = {
    "message": f"chore: auto-update portfolio README {date_str} [skip ci]",
    "content": base64.b64encode(new_content.encode()).decode(),
    "sha": sha,
    "branch": BRANCH
}

result = api("PUT", f"/repos/{USERNAME}/{REPO}/contents/{README_PATH}", update_data)
if "error" in result:
    print(f"❌ Push failed: {result['error']}")
    exit(1)

print(f"✅ Updated: {date_str}")