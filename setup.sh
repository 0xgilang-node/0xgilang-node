#!/bin/bash
# ============================================================
# PORTFOLIO SETUP — Auto-install buat 0xgilang-node
# Run once: bash setup.sh
# ============================================================
set -e

echo "🚀 Portfolio Automation Setup"
echo "=============================="

# 1. Prompt for GitHub token
echo ""
echo "📌 Paste your GitHub PAT (ghp_xxx...):"
read -r GITHUB_TOKEN

if [[ ! "$GITHUB_TOKEN" =~ ^ghp_ ]]; then
    echo "❌ Token harus mulai dengan 'ghp_'"
    exit 1
fi

# 2. Save token ke .env (gitignored)
cat > ~/.portfolio_env << EOF
export GITHUB_USERNAME="0xgilang-node"
export GITHUB_TOKEN="$GITHUB_TOKEN"
export GITHUB_EMAIL="0xgilang-node@users.noreply.github.com"
export GITHUB_NAME="Gilang buana sultoni"
export PORTFOLIO_BRANCH="main"
export TIMEZONE="Asia/Jakarta"
export ACCENT_COLOR="#0db7ed"
EOF

echo "✅ Token saved ke ~/.portfolio_env"

# 3. Clone/fetch current profile repo
PROFILE_REPO_DIR="/tmp/profile-readme"
if [ -d "$PROFILE_REPO_DIR" ]; then
    cd "$PROFILE_REPO_DIR"
    git pull --force origin main
else
    git clone https://"$GITHUB_TOKEN"@github.com/"0xgilang-node"/0xgilang-node.git "$PROFILE_REPO_DIR"
fi

# 4. Copy README template
cp ~/portfolio-automation/templates/README.md "$PROFILE_REPO_DIR/README.md"
echo "✅ README template copied"

# 5. Commit & push
cd "$PROFILE_REPO_DIR"
git add README.md
git config user.name "Gilang buana sultoni"
git config user.email "0xgilang-node@users.noreply.github.com"
git commit -m "chore: initial dynamic portfolio README [skip ci]"
git push -f origin main

echo ""
echo "✅ Profile README pushed!"
echo ""
echo "📋 Next steps:"
echo "   1. Buka https://github.com/0xgilang-node/0xgilang-node"
echo "   2. Cek README sudah keliatan di profil lu"
echo "   3. Setup cron: bash ~/portfolio-automation/scripts/cron_install.sh"
echo ""
echo "⏰ Script auto-update akan jalan setiap hari jam 06:00 WIB"