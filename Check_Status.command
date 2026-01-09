#!/bin/bash
#
# Stock Screener - Status Checker
# Double-click to check if screener is running and view recent activity
#

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         STOCK SCREENER STATUS                             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if screener is running
PIDS=$(pgrep -f "stock_screener_ultra.py")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PROCESS STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -z "$PIDS" ]; then
    echo "❌ Screener is NOT running"
    echo ""
    echo "To start: Double-click 'Start_Screener.command'"
else
    echo "✅ Screener is RUNNING"
    echo ""
    echo "Process details:"
    ps aux | grep "stock_screener_ultra.py" | grep -v grep
    echo ""
    echo "PID(s): $PIDS"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "RECENT ACTIVITY (Last 20 log lines)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "stock_screener.log" ]; then
    tail -20 stock_screener.log
else
    echo "⚠️  No log file found (stock_screener.log)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CANDIDATES FOUND (Recent)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "stock_screener.log" ]; then
    CANDIDATES=$(grep "✓" stock_screener.log | tail -10)
    if [ -z "$CANDIDATES" ]; then
        echo "ℹ️  No candidates found yet"
    else
        echo "$CANDIDATES"
    fi
else
    echo "⚠️  No log file found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CONFIGURATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "config.yaml" ]; then
    echo "Email alerts: $(grep 'receiver_email:' config.yaml | cut -d'"' -f2)"
    echo "Scan interval: $(grep 'scan_interval:' config.yaml | awk '{print $2}') seconds ($(echo "$(grep 'scan_interval:' config.yaml | awk '{print $2}') / 3600" | bc) hours)"
    echo "Min daily change: $(grep 'min_daily_change:' config.yaml | awk '{print $2}')%"
    echo "Min volume: $(grep 'min_volume:' config.yaml | awk '{print $2}') shares"
else
    echo "⚠️  config.yaml not found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter to close this window..."
