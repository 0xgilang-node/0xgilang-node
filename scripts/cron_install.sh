#!/bin/bash
# ============================================================
# CRON INSTALL — Setup daily auto-update
# Run: bash cron_install.sh
# ============================================================

SCRIPT_DIR="$HOME/portfolio-automation/scripts/update_stats.sh"
CRON_JOB="0 6 * * * /bin/bash $SCRIPT_DIR >> /var/log/portfolio-update.log 2>&1"

echo "⏰ Installing cron job..."

# Check if already installed
if crontab -l 2>/dev/null | grep -q "portfolio-update"; then
    echo "ℹ️ Cron job already installed. Skipping."
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job installed!"
fi

echo ""
echo "📋 Current crontab:"
crontab -l 2>/dev/null | grep portfolio || echo "  (none)"
echo ""
echo "🕐 Running daily at 06:00 Asia/Jakarta"
echo "📄 Logs: /var/log/portfolio-update.log"
echo ""
echo "✅ Setup complete!"
echo ""
echo "Commands useful:"
echo "  crontab -e          → edit cron"
echo "  crontab -l          → list cron"
echo "  bash $SCRIPT_DIR   → run now"