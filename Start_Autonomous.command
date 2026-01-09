#!/bin/bash
#
# Start Autonomous Stock Screener - "Set and Forget" Mode
# Self-adapts, discovers tickers, sends weekly summaries
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       AUTONOMOUS MODE - 'SET AND FORGET'                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if already running
if pgrep -f "stock_screener_autonomous.py" > /dev/null; then
    echo "⚠️  Autonomous screener is already running"
    echo ""
    read -p "Stop and restart? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🛑 Stopping existing instance..."
        pkill -f "stock_screener_autonomous.py"
        sleep 3
    else
        echo "❌ Cancelled"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "AUTONOMOUS MODE FEATURES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ AUTO-TUNES thresholds based on performance"
echo "   • Too many alerts → tightens filters"
echo "   • Too few alerts → loosens filters"
echo "   • Target: 2-4 quality alerts per day"
echo ""
echo "✅ AUTO-DISCOVERS new tickers weekly"
echo "   • Scans Polygon for new opportunities"
echo "   • Adds promising low-priced stocks"
echo "   • Caps at 100 total tickers"
echo ""
echo "✅ AUTO-PRUNES dead tickers"
echo "   • Removes stocks with no alerts for 30+ days"
echo "   • Keeps recently discovered for evaluation"
echo "   • Maintains optimal watchlist"
echo ""
echo "✅ WEEKLY EMAIL SUMMARIES"
echo "   • Top 10 opportunities from the week"
echo "   • Performance metrics"
echo "   • System adjustments made"
echo "   • No daily noise!"
echo ""
echo "✅ SELF-HEALING"
echo "   • Auto-restarts on errors"
echo "   • Health checks every hour"
echo "   • Performance tracking"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⏰ WHAT TO EXPECT:"
echo ""
echo "📧 ONE email per week (Sunday 8 PM)"
echo "📊 Contains all opportunities from that week"
echo "🤖 System manages itself automatically"
echo "💤 You can ignore for weeks/months"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Activate virtual environment
echo "🔧 Activating Python environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error: Could not activate virtual environment"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check config
if [ ! -f "config_autonomous.yaml" ]; then
    echo "❌ Error: config_autonomous.yaml not found!"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Environment ready"
echo ""

read -p "Start autonomous mode? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    read -p "Press Enter to exit..."
    exit 0
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 LAUNCHING AUTONOMOUS MODE..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "System is now running autonomously."
echo ""
echo "📧 You'll receive weekly summary emails"
echo "📊 Check autonomous_screener.log for details"
echo "🛑 To stop: Close this window or press Ctrl+C"
echo ""
echo "💤 You can now minimize this and forget about it!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sleep 3

# Run autonomous screener
python stock_screener_autonomous.py --config config_autonomous.yaml

# If it exits
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛑 Autonomous mode stopped"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter to close..."
