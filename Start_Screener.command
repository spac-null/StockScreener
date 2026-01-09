#!/bin/bash
#
# Stock Screener - Launch Script
# Double-click this file from Finder to start the screener in Terminal
#

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Display banner
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         HIGH-POTENTIAL STOCK SCREENER v1.0                ║"
echo "║         eToro EU Edition - ULTRA OPTIMIZED                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Location: $SCRIPT_DIR"
echo "🚀 Starting in 3 seconds..."
echo ""
sleep 3

# Activate virtual environment
echo "🔧 Activating Python virtual environment..."
source venv/bin/activate

# Check if activation succeeded
if [ $? -ne 0 ]; then
    echo "❌ Error: Could not activate virtual environment"
    echo "   Run 'python3 -m venv venv' first"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if config exists
if [ ! -f "config.yaml" ]; then
    echo "❌ Error: config.yaml not found!"
    echo "   Please configure your API keys and settings"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Environment ready"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 STOCK SCREENER STARTING..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Scans every 4 hours"
echo "📧 Email alerts: $(grep 'receiver_email:' config.yaml | cut -d'"' -f2)"
echo "💡 Press Ctrl+C to stop"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the screener
python stock_screener_ultra.py

# If screener exits, wait before closing terminal
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛑 Screener stopped"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press Enter to close this window..."
