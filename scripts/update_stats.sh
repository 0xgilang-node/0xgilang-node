#!/bin/bash
# ============================================================
# UPDATE STATS — Auto-run daily via cron
# Fetches latest GitHub stats & pushes to profile repo
# ============================================================
set -e

# Load config
source ~/.portfolio_env

DATE=$(TZ="Asia/Jakarta" date "+%d %b %Y %H:%M %Z")
PROFILE_REPO="/tmp/profile-readme"

echo "📊 Updating portfolio for @$GITHUB_USERNAME at $DATE"

# Clone profile repo
if [ -d "$PROFILE_REPO/.git" ]; then
    cd "$PROFILE_REPO"
    git pull --force origin $PORTFOLIO_BRANCH 2>/dev/null
else
    rm -rf "$PROFILE_REPO"
    git clone --depth=1 https://"$GITHUB_TOKEN"@github.com/"$GITHUB_USERNAME"/"$GITHUB_USERNAME".git "$PROFILE_REPO"
    cd "$PROFILE_REPO"
fi

# Update timestamp
sed -i "s/\*Last update:.*/\*Last update: $DATE/" README.md 2>/dev/null || true

# Commit & push
git config user.name "$GITHUB_NAME"
git config user.email "$GITHUB_EMAIL"
git add -A
git commit -m "chore: auto-update stats $DATE [skip ci]" || {
    echo "ℹ️ No changes to commit"
    exit 0
}
git push -f origin $PORTFOLIO_BRANCH

echo "✅ Portfolio updated & pushed!"