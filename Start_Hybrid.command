#!/bin/bash
#
# Start HYBRID Autonomous Screener
# Weekly summaries + Urgent immediate alerts for time-sensitive opportunities
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       HYBRID MODE - Best of Both Worlds                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if already running
if pgrep -f "stock_screener_hybrid.py" > /dev/null; then
    echo "⚠️  Hybrid screener is already running"
    echo ""
    read -p "Stop and restart? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🛑 Stopping existing instance..."
        pkill -f "stock_screener_hybrid.py"
        sleep 3
    else
        echo "❌ Cancelled"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "HYBRID MODE = TWO-TIER NOTIFICATIONS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚡ TIER 1: URGENT ALERTS (Immediate Email)"
echo "   • Score 85+ / 100"
echo "   • Daily change 8%+"
echo "   • Volume 3x average"
echo "   • Major catalyst (FDA, partnership, etc.)"
echo "   • Max 2 per day"
echo "   ➜ Catches RGTI-like limited window opportunities!"
echo ""
echo "📊 TIER 2: WEEKLY SUMMARY (Sunday 8 PM)"
echo "   • Normal opportunities"
echo "   • Top 10 from entire week"
echo "   • System adjustments"
echo "   • Auto-discovery/pruning results"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📧 EXPECTED EMAILS:"
echo ""
echo "• Urgent: 1-3 per week (time-sensitive)"
echo "• Summary: 1 per week (Sunday)"
echo "• Total: 2-4 emails per week"
echo ""
echo "⏰ TIME INVESTMENT:"
echo ""
echo "• Per urgent: 10 min research + decision"
echo "• Per summary: 15 min review top 10"
echo "• Total: ~30-60 min per week"
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
if [ ! -f "config_autonomous_hybrid.yaml" ]; then
    echo "❌ Error: config_autonomous_hybrid.yaml not found!"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Environment ready"
echo ""

read -p "Start HYBRID mode? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    read -p "Press Enter to exit..."
    exit 0
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 LAUNCHING HYBRID MODE..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ AUTO-TUNES thresholds (weekly)"
echo "✅ AUTO-DISCOVERS new tickers (weekly)"
echo "✅ AUTO-PRUNES dead tickers (weekly)"
echo "✅ URGENT ALERTS for exceptional opportunities"
echo "✅ WEEKLY SUMMARIES for normal opportunities"
echo ""
echo "⚡ You'll receive URGENT emails for limited-window opportunities"
echo "📊 You'll receive WEEKLY emails every Sunday"
echo ""
echo "🛑 To stop: Close this window or press Ctrl+C"
echo ""
echo "💤 Minimize this window and forget about it!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sleep 3

# Run hybrid screener
python stock_screener_hybrid.py --config config_autonomous_hybrid.yaml

# If it exits
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛑 Hybrid mode stopped"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter to close..."
