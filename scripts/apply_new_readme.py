#!/usr/bin/env python3
"""Push new Web3-optimized README to profile repo"""
import base64, datetime, urllib.request, urllib.error, json, importlib.util

# Load token from push_readme.py
spec = importlib.util.spec_from_file_location("push_readme", "/root/portfolio-automation/scripts/push_readme.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
TOKEN=mod.TOKEN

USERNAME = "0xgilang-node"
REPO = USERNAME
BRANCH = "main"

# Read new README
with open("/tmp/new_readme.md", "r") as f:
    content = f.read()

# Update timestamp
tz = datetime.timezone(datetime.timedelta(hours=7))
now = datetime.datetime.now(tz)
date_str = now.strftime("%d %b %Y %H:%M %Z")
content = content.replace("UPDATED_AT", date_str)

def api(method, path, data=None):
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Portfolio-Update"
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

# Get current SHA
print("📡 Fetching current README SHA...")
result = api("GET", f"/repos/{USERNAME}/{REPO}/contents/README.md?ref={BRANCH}")
if "error" in result:
    print(f"❌ Error: {result['error']}")
    exit(1)

sha = result["sha"]
print(f"✅ SHA: {sha[:8]}...")

# Push
encoded = base64.b64encode(content.encode()).decode()
update_data = {
    "message": f"feat: new Web3-optimized portfolio README {date_str}",
    "content": encoded,
    "sha": sha,
    "branch": BRANCH
}

result = api("PUT", f"/repos/{USERNAME}/{REPO}/contents/README.md", update_data)
if "error" in result:
    print(f"❌ Push failed: {result['error']}")
    exit(1)

print(f"✅ README pushed successfully!")
print(f"🔗 https://github.com/{USERNAME}/{USERNAME}")
print(f"📅 Timestamp: {date_str}")