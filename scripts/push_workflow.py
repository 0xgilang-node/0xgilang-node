#!/usr/bin/env python3
"""
Import TOKEN from push_readme.py (which has the real token on disk)
and use it to push the workflow file via GitHub API
"""
import importlib.util
import base64
import urllib.request
import urllib.error
import json
import sys

# Dynamically load TOKEN from push_readme.py
spec = importlib.util.spec_from_file_location("push_readme", "/root/portfolio-automation/scripts/push_readme.py")
pr = importlib.util.load_from_spec = spec
module = importlib.util.load_from_spec = spec
# Actually load the module
spec = importlib.util.spec_from_file_location("push_readme", "/root/portfolio-automation/scripts/push_readme.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
TOKEN = mod.TOKEN

USERNAME = "0xgilang-node"
REPO = USERNAME
BRANCH = "main"

WORKFLOW_YAML = """name: Portfolio Auto-Update

on:
  schedule:
    # Every day at 06:00 WIB (23:00 UTC)
    - cron: '0 23 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_PAT }}
          persist-credentials: true

      - name: Update timestamp
        run: |
          DATE=$(TZ="Asia/Jakarta" date "+%d %b %Y %H:%M %Z")
          if grep -q "Last update:" README.md; then
            sed -i "s/\\*Last update:.*/\\*Last update: $DATE [auto]/" README.md
          fi

      - name: Commit and push
        run: |
          git config user.name "Gilang buana Sultoni"
          git config user.email "0xgilang-node@users.noreply.github.com"
          git add README.md
          git diff --cached --quiet && echo "No changes to commit" && exit 0
          git commit -m "chore: auto-update $DATE [skip ci]"
          git push
"""

WORKFLOW_PATH = ".github/workflows/auto-update.yml"

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

# Check if file exists
result = api("GET", f"/repos/{USERNAME}/{REPO}/contents/{WORKFLOW_PATH}?ref={BRANCH}")
sha = result.get("sha") if "sha" in result else None

# Push
encoded = base64.b64encode(WORKFLOW_YAML.encode()).decode()
file_data = {
    "message": "ci: add auto-update GitHub Actions workflow [skip ci]",
    "content": encoded,
    "branch": BRANCH
}
if sha:
    file_data["sha"] = sha

result = api("PUT", f"/repos/{USERNAME}/{REPO}/contents/{WORKFLOW_PATH}", file_data)
if "error" in result:
    print(f"Failed: {result['error'][:150]}")
    sys.exit(1)
else:
    print("Workflow file pushed to .github/workflows/auto-update.yml")
    print()
    print("NEXT STEPS:")
    print("1. Go to: https://github.com/0xgilang-node/0xgilang-node/settings/secrets/actions")
    print("2. Click 'New repository secret'")
    print("3. Name: GH_PAT")
    print("4. Value: paste your GitHub PAT (REDACTED)")
    print("5. Click 'Add secret'")
    print("6. Go to: https://github.com/0xgilang-node/0xgilang-node/actions")
    print("7. Click 'auto-update' workflow and enable it")