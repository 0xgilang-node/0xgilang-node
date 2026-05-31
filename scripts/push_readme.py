#!/usr/bin/env python3
"""
Push updated README to GitHub profile repo
Uses GitHub REST API instead of git push
"""
import base64
import datetime
import os
import urllib.request
import urllib.error
import json

# Config
USERNAME = "0xgilang-node"
TOKEN = "REDACTED"
REPO = USERNAME  # Profile repo = username
BRANCH = "main"
README_PATH = "README.md"

# Read README content
with open("/tmp/test-profile-repo/README.md", "r") as f:
    content = f.read()

# Update timestamp
tz = datetime.timezone(datetime.timedelta(hours=7))  # WIB
now = datetime.datetime.now(tz)
date_str = now.strftime("%d %b %Y %H:%M %Z")
content = content.replace("UPDATED_AT", date_str)

# Get current README SHA
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

# Get current file SHA
print("📡 Fetching current README SHA...")
result = api("GET", f"/repos/{USERNAME}/{REPO}/contents/{README_PATH}?ref={BRANCH}")
if "error" in result:
    print(f"❌ Error fetching: {result['error']}")
    exit(1)

sha = result.get("sha")
print(f"✅ Current SHA: {sha[:8]}...")

# Encode content
encoded = base64.b64encode(content.encode()).decode()

# Push update
print("📤 Pushing update...")
commit_msg = f"chore: auto-update portfolio README {date_str} [skip ci]"
update_data = {
    "message": commit_msg,
    "content": encoded,
    "sha": sha,
    "branch": BRANCH
}

result = api("PUT", f"/repos/{USERNAME}/{REPO}/contents/{README_PATH}", update_data)
if "error" in result:
    print(f"❌ Push failed: {result['error']}")
    exit(1)

print(f"✅ Pushed successfully!")
print(f"🔗 https://github.com/{USERNAME}/{REPO}")
print(f"📅 Timestamp: {date_str}")