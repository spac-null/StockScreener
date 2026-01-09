#!/bin/bash
#
# Switch to OPTIMAL Configuration
# Designed to catch RGTI-like opportunities early
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         SWITCH TO OPTIMAL CONFIGURATION                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if screener is running
if pgrep -f "stock_screener_ultra.py" > /dev/null; then
    echo "⚠️  Screener is currently running"
    echo ""
    read -p "Stop it and switch config? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🛑 Stopping screener..."
        pkill -f "stock_screener_ultra.py"
        sleep 2
    else
        echo "❌ Cancelled. Stop screener manually first."
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Backup current config
if [ -f "config.yaml" ]; then
    echo "💾 Backing up current config to config_backup.yaml..."
    cp config.yaml config_backup.yaml
fi

# Switch to optimal
if [ -f "config_optimal.yaml" ]; then
    echo "🔄 Switching to OPTIMAL configuration..."
    cp config_optimal.yaml config.yaml
    echo "✅ Configuration switched!"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "OPTIMAL CONFIG FEATURES:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✓ Two-tier alert system (High Conviction + Watchlist)"
    echo "✓ 60+ stocks monitored (vs 31)"
    echo "✓ 3-hour scans (vs 4 hours) = 33% more frequent"
    echo "✓ Lower thresholds = catch accumulation phase"
    echo "✓ 72-hour news window = catch developing stories"
    echo "✓ 50+ sector keywords = broader coverage"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "WHAT TO EXPECT:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📧 Tier 1 Alerts: 2-3 per day (high conviction)"
    echo "👀 Tier 2 Alerts: 1-2 per day (watchlist/early signals)"
    echo "📊 Total: 10-20 alerts per week (vs 2-4 with current)"
    echo ""
    echo "💡 TIP: Review Tier 2 alerts weekly to build watchlist"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    read -p "Start screener now with OPTIMAL config? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🚀 Starting screener with OPTIMAL configuration..."
        echo ""
        sleep 2
        ./Start_Screener.command
    else
        echo ""
        echo "✅ Config switched. Start manually when ready:"
        echo "   Double-click: Start_Screener.command"
        echo ""
        read -p "Press Enter to exit..."
    fi
else
    echo "❌ Error: config_optimal.yaml not found!"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi
