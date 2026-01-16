# 🚀 Enhanced Stock Screener v2.0
## Higher ROI, Better Protection

A sophisticated Python-based stock screening system designed to identify high-potential catalyst-driven opportunities in eToro EU, with enhanced risk management and quality filtering for superior risk-adjusted returns.

### ✨ **NEW v2.0 Features**
- 🛡️ **Enhanced Risk Management**: 2% max position sizing, automatic stop-losses, scale-out take profits
- 📊 **Fundamental Analysis**: Revenue growth, debt/equity ratios, market cap filters
- 📈 **Technical Indicators**: RSI, volume surge detection for optimal timing
- 📋 **Performance Tracking**: Complete trade history with win rates and P&L analytics
- 🎯 **Quality Filters**: Weed out weak companies before they reach your alerts
- 🔍 **Multi-Factor Scoring**: Combines momentum, fundamentals, and technicals (100-point scale)

### 🎯 **Strategy Evolution**
- **v1.0**: Basic catalyst momentum (high risk, high reward)
- **v2.0**: Quality-filtered momentum (higher ROI potential, better protection)

## ⚠️ DISCLAIMER

**THIS IS NOT FINANCIAL ADVICE.** This tool is for educational and informational purposes only. Penny stocks are extremely high-risk investments with potential for total loss. Always conduct your own research and consult with a licensed financial advisor before making investment decisions.

## 🎯 Enhanced Features v2.0

### Core Screening Engine
- **Regional Filter**: Pre-configured with eToro EU-available tickers (60+ stocks)
- **Multi-Factor Scoring**: 100-point system combining momentum, fundamentals, technicals
- **Quality Filters**: Revenue growth >10%, debt/equity <2.0, market cap >$50M
- **Technical Analysis**: RSI, volume surge patterns, trend confirmation
- **Catalyst Detection**: Enhanced news analysis with 48h lookback

### Risk Management System
- **Position Sizing**: Max 2% of portfolio per trade
- **Stop Losses**: Automatic 10% stop-loss with 5% trailing stops
- **Take Profits**: Scale out at 20%, 50%, 100% gains
- **Sector Limits**: Max 10% portfolio exposure per sector
- **Portfolio Protection**: Max 20% drawdown limits

### Performance & Analytics
- **Trade Tracking**: Complete P&L history with win rates
- **Sector Analysis**: Performance breakdown by sector/catalyst type
- **Risk Metrics**: Sharpe ratio, max drawdown, holding periods
- **Continuous Learning**: Adapts based on historical performance

### Operational Features
- **Intelligent Notifications**: Quality-filtered alerts (2-5/week vs 10-20 spam)
- **24/7 Operation**: Runs continuously with 3-hour scan cycles
- **Email Alerts**: Enhanced notifications with risk management plans
- **Comprehensive Logging**: Full audit trail with performance metrics

## 📋 Prerequisites

- Python 3.8 or higher
- **Polygon.io API key** (free tier: https://polygon.io) - For stock data & news
- **Alpha Vantage API key** (free tier: https://alphavantage.co) - For fundamentals
- **News API key** (optional, free tier: https://newsapi.org) - For enhanced news analysis
- Email account for notifications (Gmail/recommended)
- eToro account for trading the identified opportunities

## 🔒 Security & API Keys

### ⚠️ IMPORTANT: API Key Security
This project has been updated to use environment variables for security. **NEVER commit API keys to git!**

#### 1. Create .env file:
```bash
cp .env.example .env  # Or create manually
```

#### 2. Add your API keys to .env:
```bash
# Required
POLYGON_API_KEY=your_polygon_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
NEWS_API_KEY=your_news_api_key_here
EMAIL_PASSWORD=your_email_password_here
```

#### 3. The system automatically loads these securely.

### 🛡️ Security Features
- API keys stored in environment variables (not in code)
- .env file excluded from git (.gitignore protected)
- No hardcoded secrets in any scripts
- All sensitive data uses ${VAR_NAME} substitution

## 🌐 Dynamic eToro Stock Discovery

### ⚠️ **IMPORTANT WARNING**
Dynamic scraping of eToro's screener may violate their terms of service. Use at your own risk and consider the ethical implications.

### How Dynamic Scraping Works (2024-2026 Trending Sectors)
1. **Sector-Focused**: Targets high-potential trending sectors instead of scraping everything
2. **Anti-Detection**: Random delays, user-agent rotation, gentle scrolling
3. **Quality First**: Applies fundamental filters (market cap, revenue growth, debt ratios)
4. **Trending Priority**: Focuses on AI, quantum, biotech, clean energy, semiconductors
5. **Fallback Safety**: Uses your configured stock list if scraping fails

### Setup Dynamic Scraping
```yaml
# In config.yaml
etoro_dynamic_scraping:
  enabled: true  # ⚠️  Set to true to enable
  filters:
    sectors: ['quantum', 'ai', 'biotech']  # Specify sectors or leave empty for all
    min_price: 0.10
    max_price: 50.00
    min_market_cap: 50000000
```

### Requirements for Dynamic Scraping
```bash
pip install selenium webdriver-manager
# Also need ChromeDriver or equivalent
```

### 🎯 Trending Sectors Targeted (2024-2026)

**🚀 HIGH PRIORITY (Breakthrough Potential):**
- **AI & Quantum Computing**: Neural networks, machine learning, quantum advantage
- **Biotech & Gene Therapy**: CRISPR, RNA therapeutics, clinical breakthroughs
- **Clean Energy**: Hydrogen, advanced batteries, carbon capture

**📈 MEDIUM PRIORITY (Government Backed):**
- **Semiconductors**: Chip manufacturing, advanced materials, supply chain
- **Infrastructure**: 5G, broadband, satellite communications
- **Cybersecurity**: Digital security, blockchain, encryption

**Benefits:**
- ✅ **Future-Focused**: Targets sectors with 5-10x growth potential
- ✅ **Government Support**: Many backed by infrastructure bills/defense spending
- ✅ **Innovation Driven**: Early access to breakthrough technologies
- ✅ **Always Current**: Gets latest eToro offerings in trending sectors

### Risks
- ❌ **Terms Violation**: May breach eToro's terms
- ❌ **Detection**: Could trigger anti-bot measures
- ❌ **Rate Limits**: eToro may block scraping attempts
- ❌ **Legal Risk**: Web scraping restrictions vary by jurisdiction

## 🛡️ Risk Management System

### Position Sizing Rules
- **Max per trade**: 2% of total portfolio
- **Max per sector**: 10% of total portfolio
- **Max portfolio drawdown**: 20% before system pause

### Automated Risk Controls
- **Stop Loss**: 10% below entry price (automatic)
- **Trailing Stop**: 5% trailing stop after 20% profit
- **Take Profit Scaling**: 1/3 position at +20%, 1/3 at +50%, 1/3 at +100%

### Quality Filters
- **Revenue Growth**: Minimum 10% YoY growth
- **Debt/Equity**: Maximum 2.0 ratio
- **Market Cap**: Minimum $50M
- **Technical**: RSI oversold (<30) preferred for entries

### Example Risk-Managed Trade
```
Stock: IONQ @ $2.50
Portfolio: $10,000
Position Size: $200 (2%)
Stop Loss: $2.25 (10% below)
Take Profits: $200 @ $3.00 (20%), $200 @ $3.75 (50%), $200 @ $5.00 (100%)
```

## 🚀 Quick Start - Ultimate Screener

### Single Powerful Script (Recommended)
```bash
cd /Users/stargatesgx/code/StockScreener
python3 ultimate_screener.py
```
This is the **ULTIMATE STOCK SCREENER v4.0** - a single, self-contained script that combines ALL features: risk management, multi-source data, performance tracking, technical analysis, and API efficiency.

### Option 2: Manual Installation

#### 1. Clone or Download
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
