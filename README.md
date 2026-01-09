# 🚀 High-Potential Stock Screener

A Python-based stock screening tool designed to identify high-potential low-priced stocks (<$5) available on eToro EU, focusing on catalyst-driven momentum opportunities similar to RGTI's 1000% gains.

## ⚠️ DISCLAIMER

**THIS IS NOT FINANCIAL ADVICE.** This tool is for educational and informational purposes only. Penny stocks are extremely high-risk investments with potential for total loss. Always conduct your own research and consult with a licensed financial advisor before making investment decisions.

## 🎯 Features

- **Regional Filter**: Pre-configured with eToro EU-available tickers
- **Smart Screening**: Filters by price ($0.10-$5), daily change (>5%), volume (>1M)
- **Catalyst Detection**: Analyzes recent news (24h) for positive catalysts
- **Sector Focus**: Targets biotech, renewables, EV, crypto, AI, quantum computing
- **Intelligent Notifications**: Only alerts on top 3-5 opportunities to avoid spam
- **24/7 Operation**: Runs continuously with 4-hour scan cycles
- **Email Alerts**: Automatic email notifications with detailed analysis
- **Risk Management**: Includes stop-loss suggestions and eToro trading steps
- **Comprehensive Logging**: Full audit trail of all screening activity

## 📋 Prerequisites

- Python 3.8 or higher
- Polygon.io API key (free tier available at https://polygon.io)
- Email account for notifications (Gmail recommended)
- eToro account (for trading the identified stocks)

## 🔧 Installation

### 1. Clone or Download

```bash
cd /Users/stargatesgx/code/StockScreener
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Edit `config.yaml` and update the following:

```yaml
api:
  polygon_api_key: "YOUR_ACTUAL_API_KEY"

email:
  sender_email: "your_email@gmail.com"
  sender_password: "your_app_password"
  receiver_email: "your_email@gmail.com"
```

#### Getting a Polygon API Key:
1. Go to https://polygon.io
2. Sign up for a free account
3. Navigate to Dashboard → API Keys
4. Copy your API key

#### Gmail App Password (Recommended):
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account → Security → 2-Step Verification → App Passwords
3. Generate an app password for "Mail"
4. Use this 16-character password in config.yaml

**Alternative Email Providers:**
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- Update `smtp_server` and `smtp_port` in config.yaml accordingly

## 🎮 Usage

### Basic Usage

Run the screener:

```bash
python stock_screener.py
```

The script will:
- Load configuration from `config.yaml`
- Initialize connection to Polygon API
- Start screening every 4 hours (configurable)
- Send notifications when high-potential stocks are found
- Log all activity to `stock_screener.log`

### Running in Background (Linux/Mac)

```bash
nohup python stock_screener.py > output.log 2>&1 &
```

### Running in Background (Windows)

```batch
pythonw stock_screener.py
```

### Stopping the Screener

Press `Ctrl+C` in the terminal, or:

```bash
# Find the process
ps aux | grep stock_screener

# Kill the process
kill <PID>
```

## ⚙️ Configuration

### Key Settings in `config.yaml`:

```yaml
screening:
  min_price: 0.1              # Minimum stock price
  max_price: 5.0              # Maximum stock price
  min_daily_change: 5.0       # Minimum % daily increase
  min_volume: 1000000         # Minimum trading volume
  max_notifications: 5        # Top N stocks per cycle
  scan_interval: 14400        # Seconds between scans (4 hours)
```

### eToro Ticker Whitelist

The `etoro_available` list contains tickers confirmed available in eToro EU. Update this list based on your region:

```yaml
etoro_available:
  - BCAB   # BioCorRx Inc
  - OPTT   # Ocean Power Technologies
  - PLUG   # Plug Power
  - SNDL   # Sundial Growers
  # Add more as needed
```

**How to verify eToro availability:**
1. Open eToro app/website
2. Search for the ticker
3. If tradeable in your region, add to the list

### Target Sectors

Customize which sectors to focus on:

```yaml
target_sectors:
  - biotech
  - quantum
  - AI
  - renewable
  # Add your preferences
```

## 📊 Example Output

### Console Output:

```
════════════════════════════════════════════════════════════
🚀 STOCK ALERT: 3 HIGH-POTENTIAL OPPORTUNITIES
════════════════════════════════════════════════════════════
Scan Time: 2024-01-15 14:30:00

⚠️ NOT FINANCIAL ADVICE. High-risk stocks. Possible total loss.

1. OPTT - $1.85
   Daily Change: +12.3%
   Volume: 2,450,000
   Score: 78.5/100
   Catalysts:
   • Ocean Power Technologies Announces Major Partnership Deal
   • Company Receives DOE Grant for Wave Energy Project

2. BCAB - $0.87
   Daily Change: +8.7%
   Volume: 1,850,000
   Score: 65.2/100
   Catalysts:
   • BioCorRx Completes Phase 2 Clinical Trial with Positive Results

3. PLUG - $3.42
   Daily Change: +7.1%
   Volume: 5,200,000
   Score: 61.8/100
   Catalysts:
   • Plug Power Secures $500M Contract for Hydrogen Fuel Cells

════════════════════════════════════════════════════════════
```

### Email Notification:

Detailed email with:
- Stock ticker and price
- Daily change percentage
- Trading volume
- Opportunity score
- News catalysts
- Risk management tips
- Step-by-step eToro trading guide

## 📈 Understanding the Scoring System

The screener calculates an opportunity score (0-100) based on:

- **Daily Change** (up to 40 points): Higher % gains = higher score
- **Volume** (up to 20 points): More volume = more liquidity
- **Catalysts** (30 points): Positive news detected
- **Sector Match** (10 points): Matches target sectors

Stocks are ranked by score, and only top N are notified.

## 🛡️ Risk Management Features

### Built-in Protections:

1. **Stop-Loss Suggestions**: Default 10% (configurable)
2. **Position Sizing Reminders**: Only risk what you can lose
3. **Disclaimer on Every Alert**: Reinforces high-risk nature
4. **Spam Prevention**: Max 3-5 notifications per cycle

### Recommended Trading Strategy:

```
1. Start small: 1-2% of portfolio per position
2. Set stop-loss immediately: 10-15% below entry
3. Take partial profits: Scale out at 20%, 50%, 100% gains
4. Never average down on losers
5. Cut losses quickly, let winners run
```

## 🔍 How It Works

### Screening Process:

1. **Fetch Data**: Retrieves price, volume, change from Polygon
2. **Apply Filters**: Price, volume, daily change thresholds
3. **Analyze News**: Scans last 24h for positive catalysts
4. **Check Sectors**: Matches against target sectors
5. **Calculate Score**: Ranks opportunities
6. **Notify**: Sends top candidates via email/console

### News Catalyst Detection:

Positive keywords:
- approval, breakthrough, partnership, deal, contract
- revenue growth, acquisition, clinical trial success
- FDA approval, patent, innovation, milestone

Negative keywords (filtered out):
- lawsuit, investigation, bankruptcy, decline
- downgrade, failed, rejected, warning

## 🐛 Troubleshooting

### Common Issues:

**1. "No module named 'polygon'"**
```bash
pip install polygon-api-client
```

**2. "Invalid API key"**
- Verify your Polygon API key in config.yaml
- Check if free tier has usage limits

**3. "Authentication failed" (Email)**
- Gmail: Use App Password, not regular password
- Enable "Less secure app access" or use App Passwords

**4. "No candidates found"**
- Market conditions may not meet criteria
- Try lowering `min_daily_change` to 3%
- Expand `etoro_available` ticker list

**5. Rate Limiting**
- Free Polygon tier: 5 requests/minute
- Script includes 0.12s delay between tickers
- Upgrade to paid plan for higher limits

## 📁 File Structure

```
StockScreener/
├── stock_screener.py      # Main application
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── stock_screener.log    # Generated log file
```

## 🚀 Future Enhancements

### Potential Additions:

1. **GUI Version** (Tkinter/PyQt)
   - Real-time dashboard
   - Manual search capability
   - Chart visualization

2. **Web App** (Flask/Django)
   - Browser-based interface
   - Multi-user support
   - Historical tracking

3. **Advanced Features**
   - Technical indicators (RSI, MACD)
   - Social media sentiment (Twitter/Reddit)
   - Portfolio tracking
   - Backtesting engine

4. **Dynamic eToro Integration**
   - Web scraping for real-time availability
   - Automatic ticker discovery

## 📚 Additional Resources

### Learning Materials:
- [Polygon.io Documentation](https://polygon.io/docs)
- [Catalyst-Driven Trading Strategies](https://www.investopedia.com/catalyst-investing)
- [Penny Stock Risk Management](https://www.sec.gov/investor/pubs/microcapstock.htm)

### Tools:
- [eToro Platform](https://www.etoro.com)
- [Finviz Screener](https://finviz.com/screener.ashx)
- [TradingView Charts](https://www.tradingview.com)

## 📝 License

This project is for educational purposes only. Use at your own risk.

## 🤝 Contributing

To add more eToro-available tickers:
1. Verify ticker availability in your eToro account
2. Add to `etoro_available` list in config.yaml
3. Test with a manual run

## 💬 Support

For issues or questions:
1. Check `stock_screener.log` for errors
2. Review this README's troubleshooting section
3. Verify API keys and configuration

---

**Remember**: Penny stocks are speculative investments. Never invest more than you can afford to lose completely. This tool identifies potential opportunities but does not guarantee profits. Always do your own research (DYOR) and consider consulting a financial advisor.

**Happy (and safe) trading! 📈🛡️**
