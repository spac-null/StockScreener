# 🎮 How to Use - Double-Click Scripts

## 📂 Open in Finder

Navigate to:
```
/Users/stargatesgx/code/StockScreener
```

You'll see 3 special scripts:
- `Start_Screener.command` 🚀
- `Stop_Screener.command` 🛑
- `Check_Status.command` 📊

---

## 🚀 Start Screener

### Method 1: Double-Click (Recommended)
1. Open Finder
2. Navigate to `/Users/stargatesgx/code/StockScreener`
3. **Double-click** `Start_Screener.command`
4. Terminal window opens showing live output
5. Screener runs continuously - you'll see:
   - Phase 1: Scanning news
   - Phase 2: Checking prices
   - Candidates found (if any)
   - Email notifications sent

### Method 2: From Terminal
```bash
cd /Users/stargatesgx/code/StockScreener
./Start_Screener.command
```

### What You'll See:
```
╔═══════════════════════════════════════════════════════════╗
║         HIGH-POTENTIAL STOCK SCREENER v1.0                ║
║         eToro EU Edition - ULTRA OPTIMIZED                ║
╚═══════════════════════════════════════════════════════════╝

🔧 Activating Python virtual environment...
✅ Environment ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 STOCK SCREENER STARTING...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Scans every 4 hours
📧 Email alerts: musabanana@protonmail.com
💡 Press Ctrl+C to stop
```

### To Stop:
- Press `Ctrl+C` in the Terminal window
- Or double-click `Stop_Screener.command`

---

## 🛑 Stop Screener

### Method 1: Ctrl+C
If screener is running in visible Terminal:
1. Click on the Terminal window
2. Press `Ctrl+C`
3. Screener stops gracefully

### Method 2: Double-Click Stop Script
If screener is running anywhere (background or foreground):
1. Double-click `Stop_Screener.command`
2. Shows all running screener processes
3. Stops them automatically
4. Confirms when done

### What You'll See:
```
╔═══════════════════════════════════════════════════════════╗
║         STOP STOCK SCREENER                               ║
╚═══════════════════════════════════════════════════════════╝

🔍 Found running screener(s):
[Process details]

🛑 Stopping process 12345...
✅ All screener processes stopped
```

---

## 📊 Check Status

### How to Use:
1. Double-click `Check_Status.command`
2. Terminal opens showing:
   - Is screener running? (✅ or ❌)
   - Recent log activity
   - Candidates found
   - Current configuration

### What You'll See:
```
╔═══════════════════════════════════════════════════════════╗
║         STOCK SCREENER STATUS                             ║
╚═══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROCESS STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Screener is RUNNING
PID: 12345

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECENT ACTIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Last 20 log lines...]
```

---

## 🎯 Typical Workflow

### Daily Use:
1. **Morning:** Double-click `Start_Screener.command`
2. **Let it run:** Keep Terminal window open (can minimize)
3. **Check email:** Alerts arrive automatically
4. **Evening:** Press `Ctrl+C` or use `Stop_Screener.command`

### 24/7 Operation:
1. Start the screener
2. Minimize Terminal window (don't close!)
3. Screener runs continuously
4. Email alerts arrive every ~4 hours if candidates found
5. Check status anytime with `Check_Status.command`

### Troubleshooting:
1. Double-click `Check_Status.command`
2. See if it's running
3. Review recent logs
4. Check configuration
5. Stop and restart if needed

---

## 💡 Tips

### Keep Terminal Open:
- **Don't close** the Terminal window - screener stops!
- **Minimize** is OK - screener continues
- Can hide with `Cmd+H`

### Multiple Instances:
- Script prevents running multiple instances
- Use `Stop_Screener.command` to clean up
- Then start fresh

### View Live Output:
- Terminal shows real-time activity
- See each ticker being checked
- See API calls, rate limiting
- See candidates as they're found

### Background Operation:
If you want to close Terminal but keep screener running:
```bash
cd /Users/stargatesgx/code/StockScreener
source venv/bin/activate
nohup python stock_screener_ultra.py > screener_output.log 2>&1 &
```
*But the .command script is easier for most users!*

---

## 📧 Email Notifications

**Currently configured:**
- Receiver: `musabanana@protonmail.com`
- Sender: `crypto@jaschablume.nl`
- Server: `send.one.com:587`

**When you receive an email:**
1. Open and read catalyst details
2. Research the ticker on eToro
3. Decide: Trade or pass
4. If trading: Set stop-loss immediately!

---

## ⚙️ Configuration

**To change settings:**
1. Close screener (if running)
2. Edit `config.yaml` in text editor
3. Modify values:
   ```yaml
   min_daily_change: 3.0    # Lower = more alerts
   min_volume: 500000       # Lower = more stocks
   scan_interval: 14400     # Seconds between scans
   ```
4. Save file
5. Restart screener with `Start_Screener.command`

---

## 🚨 Common Issues

### "Permission denied"
```bash
cd /Users/stargatesgx/code/StockScreener
chmod +x *.command
```

### "Virtual environment not found"
```bash
cd /Users/stargatesgx/code/StockScreener
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Config file not found"
Make sure `config.yaml` exists in the same folder as the scripts.

### No alerts for days
- Normal if market is quiet
- Try lowering `min_daily_change` to `1.0`
- Check logs with `Check_Status.command`

---

## 📁 File Organization

```
StockScreener/
├── Start_Screener.command    ← Double-click to START
├── Stop_Screener.command      ← Double-click to STOP
├── Check_Status.command       ← Double-click to CHECK
├── stock_screener_ultra.py    (Main script)
├── config.yaml                (Your settings)
├── stock_screener.log         (Detailed logs)
├── venv/                      (Python environment)
└── [Other files...]
```

---

## 🎓 Understanding Output

### Phase 1 (News Scan):
```
Phase 1: Scanning news for 31 tickers...
📰 LCID: 5 news items, catalyst=true
```
- Checking each ticker for recent news
- Identifies stocks with catalysts
- ~7 minutes

### Phase 2 (Price Check):
```
Phase 2: Fetching price data for 3 tickers...
✓ LCID: $2.45 (+5.2%) - Score: 82.5
```
- Only checks stocks that have news
- Validates price, volume, change
- ~3 minutes

### Results:
```
Scan complete: 1 candidates found
📧 Email sent to musabanana@protonmail.com
```

---

## 🔐 Security Notes

- **Never share** `config.yaml` (contains API keys)
- **Never commit** `config.yaml` to git
- **API keys** are in plain text - keep file secure
- **Email password** is in plain text - use app password

---

## 🚀 Quick Start Summary

1. **Start:** Double-click `Start_Screener.command`
2. **Monitor:** Keep Terminal open, check email
3. **Check:** Double-click `Check_Status.command` anytime
4. **Stop:** Press `Ctrl+C` or double-click `Stop_Screener.command`

**That's it!** 🎉

---

## 📞 Need Help?

Check these files:
- `RUNNING_NOW.md` - Quick reference
- `DEPLOYMENT_SUMMARY.md` - Full details
- `README.md` - Complete documentation
- `stock_screener.log` - What's happening

---

**Happy screening! 🚀📈**

*Remember: This is NOT financial advice. High risk investments. Always use stop-losses.*
