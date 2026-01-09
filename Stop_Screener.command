#!/bin/bash
#
# Stock Screener - Stop Script
# Double-click to stop any running screener instances
#

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         STOP STOCK SCREENER                               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Find all running screener processes
PIDS=$(pgrep -f "stock_screener_ultra.py")

if [ -z "$PIDS" ]; then
    echo "✅ No screener processes found running"
    echo ""
else
    echo "🔍 Found running screener(s):"
    echo ""
    ps aux | grep "stock_screener_ultra.py" | grep -v grep
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    for PID in $PIDS; do
        echo "🛑 Stopping process $PID..."
        kill $PID

        # Wait a moment
        sleep 1

        # Check if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo "⚠️  Process $PID still running, forcing..."
            kill -9 $PID
        fi
    done

    echo ""
    echo "✅ All screener processes stopped"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter to close this window..."
