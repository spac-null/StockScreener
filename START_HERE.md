# 🎯 START HERE - Simple Guide

## 📂 Step 1: Open Finder

Press `Cmd+Space` and type **"Finder"**, then press Enter.

Navigate to:
```
/Users/stargatesgx/code/StockScreener
```

**💡 Pro Tip:** Drag this folder to Finder sidebar for quick access!

---

## 🚀 Step 2: Start the Screener

Find this file in Finder:
```
Start_Screener.command
```

**Double-click it!**

---

## ✨ What Happens Next

A Terminal window opens showing:

```
╔═══════════════════════════════════════════════════════════╗
║         HIGH-POTENTIAL STOCK SCREENER v1.0                ║
║         eToro EU Edition - ULTRA OPTIMIZED                ║
╚═══════════════════════════════════════════════════════════╝

📍 Location: /Users/stargatesgx/code/StockScreener
🚀 Starting in 3 seconds...

🔧 Activating Python virtual environment...
✅ Environment ready

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 STOCK SCREENER STARTING...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Scans every 4 hours
📧 Email alerts: musabanana@protonmail.com
💡 Press Ctrl+C to stop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cycle #1 starting...
Phase 1: Scanning news for 31 tickers...
📰 LCID: 5 news items, catalyst=true
Phase 2: Fetching price data for 1 ticker...
✓ LCID: $2.45 (+5.2%) - Score: 82.5

📧 Email sent to musabanana@protonmail.com
```

**Keep this Terminal window open!** (You can minimize it)

---

## 📧 Step 3: Check Your Email

Alerts arrive at: **musabanana@protonmail.com**

When you receive an email:
1. Read the catalyst details
2. Research the stock on eToro
3. Decide: Trade or pass
4. If trading: **Set stop-loss immediately!**

---

## 🛑 Step 4: Stop the Screener

### Method A: Keyboard
1. Click on the Terminal window
2. Press `Ctrl+C`
3. Done!

### Method B: Double-Click
1. Find in Finder: `Stop_Screener.command`
2. Double-click it
3. Done!

---

## 📊 Check Status Anytime

Double-click: `Check_Status.command`

Shows:
- ✅ Is it running?
- 📜 Recent activity
- 🎯 Candidates found
- ⚙️ Current settings

---

## 🎮 Three Magic Scripts

| Script | What It Does | When to Use |
|--------|--------------|-------------|
| 🚀 **Start_Screener.command** | Starts screener in Terminal | Daily, when you want to monitor |
| 🛑 **Stop_Screener.command** | Stops all screeners | End of day, or troubleshooting |
| 📊 **Check_Status.command** | Shows status & logs | Anytime to check if working |

---

## 💡 Daily Workflow

**Morning:**
1. Double-click `Start_Screener.command`
2. Minimize Terminal window (don't close!)
3. Go about your day

**Throughout Day:**
- Check email for alerts
- Research opportunities on eToro

**Evening:**
- Press `Ctrl+C` in Terminal
- Or double-click `Stop_Screener.command`

---

## 🔧 Advanced Settings

Want to change how it works?

1. Open `config.yaml` in a text editor
2. Change values:
   ```yaml
   min_daily_change: 3.0    # Lower = more alerts
   min_volume: 500000       # Lower = more stocks
   scan_interval: 14400     # Seconds (4 hours)
   ```
3. Save file
4. Restart screener

---

## ❓ Troubleshooting

### "Permission denied"
Open Terminal and run:
```bash
cd /Users/stargatesgx/code/StockScreener
chmod +x *.command
```

### No alerts for 24+ hours?
- This is **normal** if market is quiet
- Double-click `Check_Status.command` to verify it's running
- Try lowering `min_daily_change` to `1.0` in config.yaml

### Terminal window closed by accident?
- Screener stops
- Just double-click `Start_Screener.command` again

---

## 🎓 Understanding the Output

**Phase 1 (News Scan):**
```
Phase 1: Scanning news for 31 tickers...
```
Checks each stock for recent news (~7 minutes)

**Phase 2 (Price Check):**
```
Phase 2: Fetching price data for 3 tickers...
```
Only checks stocks with news (~3 minutes)

**Results:**
```
✓ LCID: $2.45 (+5.2%) - Score: 82.5
📧 Email sent
```
Found a candidate and notified you!

---

## 🔐 Important Security Notes

- **Don't share** `config.yaml` (has your API keys)
- **Keep Terminal window secure** (shows API activity)
- **Use app password** for email (not main password)

---

## 📚 More Information

For detailed guides, check these files:
- **HOW_TO_USE.md** - Complete instructions
- **RUNNING_NOW.md** - Quick reference
- **DEPLOYMENT_SUMMARY.md** - Technical details
- **README.md** - Full documentation

---

## 🚀 You're Ready!

1. **Open Finder**
2. **Go to:** `/Users/stargatesgx/code/StockScreener`
3. **Double-click:** `Start_Screener.command`
4. **Done!** Screener is running

---

## ⚠️ Critical Reminders

- **NOT financial advice**
- **High-risk investments** - possible total loss
- **Always use stop-losses** (10% suggested)
- **Only invest disposable income**
- **Do your own research** before trading

---

**Happy (and safe) trading! 🚀📈🛡️**

---

*Email alerts: musabanana@protonmail.com*
*Scans: Every 4 hours*
*Tickers: 31 eToro EU stocks*
