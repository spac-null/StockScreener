#!/bin/bash
#
# Switch to CONSERVATIVE Configuration (Original)
# High-quality alerts only, less noise
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         SWITCH TO CONSERVATIVE CONFIGURATION              ║"
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

# Check if backup exists
if [ -f "config_backup.yaml" ]; then
    echo "💾 Restoring from backup..."
    cp config_backup.yaml config.yaml
    echo "✅ Configuration restored!"
else
    echo "⚠️  No backup found. Using default conservative settings..."
    # Create conservative config on the fly
    cat > config.yaml << 'EOF'
# Conservative Stock Screener Configuration
# High-quality alerts only, less noise

api:
  polygon_api_key: "Y2Qew5cni67EIpHHQshd7Pj6Rl1DFZd6"

email:
  enabled: true
  smtp_server: "send.one.com"
  smtp_port: 587
  sender_email: "crypto@jaschablume.nl"
  sender_password: "CrYpt0W1zz"
  receiver_email: "musabanana@protonmail.com"

screening:
  min_price: 0.1
  max_price: 5.0
  min_daily_change: 3.0
  min_volume: 500000
  max_notifications: 5
  scan_interval: 14400

  target_sectors:
    - biotech
    - renewable
    - solar
    - wind
    - electric vehicle
    - EV
    - crypto
    - blockchain
    - AI
    - artificial intelligence
    - quantum
    - gene therapy
    - clinical trial

  news_lookback_hours: 24

etoro_available:
  - ACB
  - BCAB
  - BLNK
  - BNGO
  - CAN
  - CENN
  - CGC
  - CLNE
  - CLSK
  - CLOV
  - CRON
  - FCEL
  - FUBO
  - GEVO
  - GSAT
  - ICLN
  - LCID
  - LOGC
  - MARA
  - NNDM
  - OCGN
  - OPTT
  - PLTR
  - PLUG
  - RIOT
  - SNDL
  - SOFI
  - TLRY
  - TOON
  - ZOMDF
  - OPTT

logging:
  enabled: true
  log_file: "stock_screener.log"
  log_level: "INFO"

risk_management:
  stop_loss_percentage: 10
  disclaimer: "⚠️ NOT FINANCIAL ADVICE. High-risk stocks. Possible total loss. Always do your own research."
EOF
    echo "✅ Conservative config created!"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CONSERVATIVE CONFIG FEATURES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✓ Single-tier alerts (high quality only)"
echo "✓ 31 stocks monitored"
echo "✓ 4-hour scans = less frequent"
echo "✓ 3% daily change threshold = obvious movers"
echo "✓ 24-hour news window = fresh catalysts only"
echo "✓ Less noise, higher conviction"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "WHAT TO EXPECT:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📧 Alerts: 2-4 per week"
echo "📊 Quality: High (obvious opportunities)"
echo "⏰ Best for: Part-time traders, busy schedules"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Start screener now with CONSERVATIVE config? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting screener with CONSERVATIVE configuration..."
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
