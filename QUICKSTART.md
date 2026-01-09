# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed polygon-api-client-1.12.5 pandas-2.1.4 requests-2.31.0 pyyaml-6.0.1 python-dotenv-1.0.0
```

## Step 2: Get Your Polygon API Key

1. Visit: https://polygon.io/dashboard/signup
2. Sign up for FREE account
3. Navigate to: Dashboard → API Keys
4. Copy your key (looks like: `abcdefgh12345678`)

## Step 3: Configure Your Settings

Edit `config.yaml`:

```yaml
api:
  polygon_api_key: "paste_your_key_here"

email:
  sender_email: "youremail@gmail.com"
  sender_password: "your_16_char_app_password"
  receiver_email: "youremail@gmail.com"
```

### Gmail App Password Setup:

1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Search for "App Passwords"
4. Generate password for "Mail"
5. Copy the 16-character password

## Step 4: Test Run

```bash
python stock_screener.py
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║         HIGH-POTENTIAL STOCK SCREENER v1.0                ║
║         eToro EU Edition - Low-Priced Catalyst Stocks     ║
╚═══════════════════════════════════════════════════════════╝

2024-01-15 10:00:00 - INFO - Stock Screener initialized successfully
2024-01-15 10:00:00 - INFO - Starting continuous screening (every 4.0 hours)
```

## Example Successful Output

```
════════════════════════════════════════════════════════════════════════════════
Starting stock screening cycle...
2024-01-15 10:05:23 - INFO - Loaded 45 eToro-available tickers
✓ OPTT: $1.85 (+12.3%) - Score: 78.5
✓ BCAB: $0.87 (+8.7%) - Score: 65.2
✓ PLUG: $3.42 (+7.1%) - Score: 61.8
Found 3 candidates, notifying top 3

════════════════════════════════════════════════════════════
🚀 STOCK ALERT: 3 HIGH-POTENTIAL OPPORTUNITIES
════════════════════════════════════════════════════════════
Scan Time: 2024-01-15 10:05:45

⚠️ NOT FINANCIAL ADVICE. High-risk stocks. Possible total loss. Always do your own research.

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

2024-01-15 10:05:50 - INFO - Email notification sent to youremail@gmail.com
2024-01-15 10:05:50 - INFO - Next scan at: 2024-01-15 14:05:50
2024-01-15 10:05:50 - INFO - Sleeping for 4.0 hours...
```

## Example Email Notification

**Subject:** 🚀 Stock Alert: 3 High-Potential Stocks Found

**Body:**
```
🚀 HIGH-POTENTIAL STOCK ALERT 🚀
Scan Time: 2024-01-15 10:05:45

⚠️ NOT FINANCIAL ADVICE. High-risk stocks. Possible total loss. Always do your own research.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP OPPORTUNITIES:

1. OPTT - $1.85
   📈 Daily Change: +12.3%
   📊 Volume: 2,450,000 shares
   🎯 Opportunity Score: 78.5/100
   📰 Recent News: 5 articles

   CATALYSTS:
   • Ocean Power Technologies Announces Major Partnership Deal
   • Company Receives DOE Grant for Wave Energy Project

   🛡️ RISK MANAGEMENT:
   • Suggested Stop-Loss: 10%
   • Position Size: Risk only what you can afford to lose

   📱 HOW TO TRADE ON eTORO:
   1. Search for "OPTT" in eToro app
   2. Review company info and charts
   3. Set price alert for monitoring
   4. If buying, use stop-loss orders
   5. Consider taking profits at 20-50% gains

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Additional stocks...]

IMPORTANT REMINDERS:
• Penny stocks are extremely volatile
• Past performance doesn't guarantee future results
• News catalysts can reverse quickly
• Only invest money you can afford to lose completely
• Set stop-losses to protect capital
• Consider scaling out profits gradually

This is NOT financial advice. Always do your own research.
```

## Testing Without Waiting 4 Hours

Modify `config.yaml` temporarily:

```yaml
screening:
  scan_interval: 300  # 5 minutes instead of 14400 (4 hours)
  min_daily_change: 2.0  # Lower threshold to see more results
```

## Common First-Time Issues

### Issue 1: "No candidates found"

**Cause**: Market conditions or criteria too strict

**Solution**:
```yaml
screening:
  min_daily_change: 2.0  # Lower from 5.0
  min_volume: 500000     # Lower from 1000000
```

### Issue 2: "Authentication failed" (Email)

**Cause**: Regular password instead of App Password

**Solution**:
- Use Gmail App Password (16 chars, no spaces)
- Or disable email: `email: enabled: false`

### Issue 3: "Rate limit exceeded" (Polygon)

**Cause**: Free tier = 5 requests/minute

**Solution**: Already handled by script (0.12s delay)
- With 45 tickers = ~5.4 seconds per cycle
- Well under rate limit

### Issue 4: No logs appearing

**Cause**: Logging disabled or permission issue

**Solution**:
```yaml
logging:
  enabled: true
  log_level: "INFO"
```

## Understanding the Logs

```
stock_screener.log content:

2024-01-15 10:00:00 - INFO - Stock Screener initialized successfully
2024-01-15 10:00:00 - INFO - Loaded 45 eToro-available tickers
2024-01-15 10:00:05 - DEBUG - No snapshot data for KULR
2024-01-15 10:00:06 - INFO - ✓ OPTT: $1.85 (+12.3%) - Score: 78.5
2024-01-15 10:00:50 - INFO - Email notification sent
```

- **INFO**: Normal operations
- **DEBUG**: Detailed info (useful for troubleshooting)
- **ERROR**: Problems that need attention

## Customizing for Your Strategy

### Focus on Specific Sectors

```yaml
target_sectors:
  - quantum       # For RGTI-like opportunities
  - AI
  - biotech
```

### Add More Tickers

Check eToro availability, then add to config:

```yaml
etoro_available:
  - BCAB
  - OPTT
  - XYZW  # Your new ticker
```

### Adjust Risk Tolerance

```yaml
screening:
  min_price: 0.5      # Avoid ultra-penny stocks
  max_price: 3.0      # Stay well under $5
  min_volume: 2000000 # Higher liquidity
```

## Running 24/7

### On Mac/Linux:

```bash
# Start in background
nohup python stock_screener.py > output.log 2>&1 &

# Check if running
ps aux | grep stock_screener

# View logs in real-time
tail -f stock_screener.log

# Stop
kill $(pgrep -f stock_screener.py)
```

### On Windows:

```batch
# Start (no console window)
pythonw stock_screener.py

# Stop (Task Manager)
Ctrl+Shift+Esc → Find python.exe → End Task
```

### Using Screen (Linux/Mac):

```bash
# Start screen session
screen -S stock_screener

# Run script
python stock_screener.py

# Detach: Ctrl+A, then D

# Reattach later
screen -r stock_screener
```

## Performance Tips

### Reduce API Calls

```yaml
etoro_available:
  # Only keep tickers you're interested in
  - OPTT
  - BCAB
  - PLUG
  # Remove others to speed up scans
```

### Increase Scan Interval (Save API Quota)

```yaml
screening:
  scan_interval: 21600  # 6 hours instead of 4
```

### Monitor API Usage

Free Polygon tier:
- **Limit**: 5 calls/minute, 100,000/month
- **Usage**: 45 tickers × 2 calls = 90 calls/cycle
- **Cycles/day**: 6 (every 4 hours)
- **Monthly**: ~90 × 6 × 30 = 16,200 calls ✅ Well under limit

## Next Steps

1. ✅ **Run for 24 hours** - See how many alerts you get
2. ✅ **Tune parameters** - Adjust based on results
3. ✅ **Paper trade** - Test strategy without real money
4. ✅ **Set eToro alerts** - For the tickers that appear frequently
5. ✅ **Review log** - Learn what works and what doesn't

## Advanced: Adding Custom Indicators

Want to add RSI, MACD, or other technical indicators?

1. Install TA-Lib: `pip install TA-Lib`
2. Modify `screen_stocks()` function
3. Add technical criteria to scoring

Example:
```python
import talib

# In screen_stocks() method:
rsi = talib.RSI(price_history, timeperiod=14)
if rsi[-1] < 30:  # Oversold
    score += 10
```

## Support & Resources

- **Polygon Docs**: https://polygon.io/docs/stocks
- **Python Docs**: https://docs.python.org/3/
- **eToro Help**: https://www.etoro.com/customer-service/

---

**You're all set! The screener is now running 24/7, hunting for the next RGTI-like opportunity. Good luck! 🚀📈**

**Remember: High-risk = High-reward = Possible total loss. Trade responsibly!**
