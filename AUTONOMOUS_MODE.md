# 🤖 Autonomous Mode - "Set and Forget"

## 🎯 What Is Autonomous Mode?

**The Ultimate "Hands-Off" Stock Screening System**

Instead of:
- ❌ Daily alerts flooding your inbox
- ❌ Manual threshold adjustments
- ❌ Manually adding new tickers
- ❌ Constant monitoring

You get:
- ✅ **ONE weekly email** with top opportunities
- ✅ **Self-tuning** thresholds (adapts to market conditions)
- ✅ **Auto-discovery** of new tickers
- ✅ **Auto-pruning** of dead tickers
- ✅ **Self-healing** (auto-restarts on errors)

**Result:** Set it up once, check email once per week. Done.

---

## 🚀 Quick Start

1. **Open Finder:** `/Users/stargatesgx/code/StockScreener`
2. **Double-click:** `Start_Autonomous.command`
3. **Confirm:** Click "Yes" to start
4. **Minimize Terminal** (keep open, don't close!)
5. **Forget about it** for a week

**Next action:** Check email Sunday evening for weekly summary.

---

## 📊 How It Works

### **Daily Operations** (Automatic):

**Every 4 Hours:**
1. Scans all tickers with current thresholds
2. Finds candidates matching criteria
3. Logs results (no email)
4. Continues silently

**Every Hour:**
- Health check (is it still running?)
- Auto-restarts if crashed
- Logs performance metrics

---

### **Weekly Operations** (Automatic):

**Every Sunday at 8 PM:**

#### **1. Performance Analysis**
```
Past week data:
• 42 scans completed
• 18 candidates found
• Average score: 72/100
• Alerts per day: 2.6
```

#### **2. Threshold Auto-Tuning**

**If too few alerts (<1/day):**
```
Current: 3% change, 500K volume
Action: Loosen to 2.5% change, 400K volume
Reason: Not finding enough opportunities
```

**If too many alerts (>6/day):**
```
Current: 2% change, 300K volume
Action: Tighten to 2.5% change, 400K volume
Reason: Too much noise, need higher quality
```

**If just right (2-4/day):**
```
Action: No changes
Status: Optimal alert rate maintained
```

#### **3. Ticker Discovery**

Searches Polygon for new opportunities:
```
Criteria:
• Price: $0.50-$3.00
• Volume: >500K
• Not currently monitored
• Active trading

Discovered this week:
• ABCD ($1.85, 1.2M vol)
• EFGH ($2.40, 800K vol)

Added to watchlist → Will monitor going forward
```

#### **4. Dead Ticker Pruning**

Removes underperformers:
```
Tickers with no alerts for 30+ days:
• OLDTICK (90 days silent)
• DEADSTOCK (45 days silent)

Action: Removed from watchlist
Result: More focused monitoring
```

#### **5. Weekly Summary Email**

Sends comprehensive report:
```
Subject: 📊 Weekly Stock Screener Summary - 18 Opportunities

Top 10 Opportunities:
1. IONQ - $12.50 (Score: 88/100)
   Catalyst: Quantum breakthrough announced
   Date: 2026-01-08

2. CRSP - $45.80 (Score: 82/100)
   Catalyst: FDA fast-track designation
   Date: 2026-01-09

[... continues ...]

System Adjustments:
• Threshold tuned: 3% → 2.5% (too few alerts)
• Added tickers: ABCD, EFGH
• Removed tickers: OLDTICK, DEADSTOCK

Next Summary: 2026-01-19
```

---

## ⚙️ Configuration

### **config_autonomous.yaml:**

```yaml
# Email Settings
email:
  summary_mode: true       # Weekly summaries only
  summary_day: "Sunday"    # Day for weekly email
  summary_hour: 20         # 8 PM

# Initial Thresholds (will auto-adjust)
screening:
  min_daily_change: 2.0    # Starting point
  min_volume: 400000       # Starting point

# Autonomous Features
autonomous:
  enabled: true

  # Auto-discovery
  discover_new_tickers: true
  discovery_interval_days: 7
  max_tickers: 100         # Cap total

  # Auto-tuning
  auto_tune_thresholds: true
  tune_interval_days: 7
  target_alerts_per_day: 3  # Optimize for this

  # Auto-pruning
  prune_dead_tickers: true
  prune_after_days: 30

  # Self-healing
  auto_restart: true
  max_consecutive_errors: 5
```

---

## 📧 Weekly Email Format

### **Subject:**
```
📊 Weekly Stock Screener Summary - 18 Opportunities
```

### **Body:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 PERFORMANCE SUMMARY (Last 7 Days):

• Candidates Found: 18
• Average Score: 72.4/100
• Scans Completed: 42
• System Status: ✅ Healthy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 TOP 10 OPPORTUNITIES:

1. IONQ - $12.50
   Score: 88.5/100
   Change: +8.2%
   Volume: 5,200,000
   Date: 2026-01-08
   Catalyst: Quantum computing breakthrough announced

2. CRSP - $45.80
   Score: 82.3/100
   Change: +6.5%
   Volume: 2,100,000
   Date: 2026-01-09
   Catalyst: FDA grants fast-track designation

[... 8 more ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 SYSTEM ADJUSTMENTS:

• Alert rate was low (1.2/day) - loosened thresholds
  min_daily_change: 3.0% → 2.5%
  min_volume: 500K → 400K

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 NEW TICKERS DISCOVERED:

ABCD, EFGH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 ACTIONS TO TAKE:

1. Review top 10 opportunities above
2. Research any promising tickers on eToro
3. System is auto-optimizing - no manual adjustments needed
4. Next summary: Sunday, 2026-01-19

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  NOT FINANCIAL ADVICE. Do your own research.

🤖 Autonomous Stock Screener - Running since 2026-01-03
```

---

## 🎯 Benefits vs Other Modes

| Feature | Manual Mode | Conservative | Optimal | Autonomous |
|---------|-------------|--------------|---------|------------|
| **Alerts** | Daily | 2-4/week | 10-20/week | 1/week (summary) |
| **Inbox Noise** | High | Medium | High | Very Low |
| **Tuning** | Manual | Manual | Manual | **Automatic** |
| **Ticker Discovery** | Manual | Manual | Manual | **Automatic** |
| **Maintenance** | Weekly | Weekly | Weekly | **None** |
| **Best For** | Active trading | Part-time | Active research | **Set & forget** |

---

## 📊 Performance Tracking

### **Stored in:** `performance_history.json`

```json
{
  "start_date": "2026-01-03T10:00:00",
  "candidates_found": [
    {
      "ticker": "IONQ",
      "price": 12.50,
      "score": 88.5,
      "timestamp": "2026-01-08T14:30:00"
    },
    ...
  ],
  "config_changes": [
    {
      "timestamp": "2026-01-07T20:00:00",
      "reason": "Alert rate: 1.2/day",
      "changes": {
        "min_daily_change": "3.0 → 2.5"
      }
    }
  ],
  "ticker_discoveries": [
    {
      "timestamp": "2026-01-07T20:15:00",
      "discovered": ["ABCD", "EFGH"]
    }
  ]
}
```

---

## 🔧 Customization

### **Change Weekly Email Day:**
```yaml
# config_autonomous.yaml
email:
  summary_day: "Friday"    # Instead of Sunday
  summary_hour: 18         # 6 PM instead of 8 PM
```

### **Adjust Target Alert Rate:**
```yaml
autonomous:
  target_alerts_per_day: 5  # More aggressive (default: 3)
```

### **Discovery Frequency:**
```yaml
autonomous:
  discovery_interval_days: 14  # Every 2 weeks (default: 7)
```

### **Pruning Threshold:**
```yaml
autonomous:
  prune_after_days: 60     # Keep longer (default: 30)
```

---

## 🛠️ Troubleshooting

### **Not Receiving Weekly Emails?**

**Check:**
1. Is it Sunday evening?
2. Check `autonomous_screener.log` for errors
3. Verify email config in `config_autonomous.yaml`
4. Look for "Weekly summary sent" in logs

**Test manually:**
```bash
# Check if running
ps aux | grep autonomous

# View recent logs
tail -50 autonomous_screener.log

# Check performance file
cat performance_history.json
```

### **Too Many/Few Opportunities?**

**System auto-adjusts, but you can override:**

Edit `config_autonomous.yaml`:
```yaml
autonomous:
  target_alerts_per_day: 5   # More (default: 3)
  # or
  target_alerts_per_day: 1   # Less
```

Restart screener for changes to take effect.

### **Want to See What It's Doing?**

**View live logs:**
```bash
tail -f autonomous_screener.log
```

**Check performance data:**
```bash
cat performance_history.json | jq .
```

---

## 🎓 Best Practices

### **1. Initial Setup (Week 1):**
- Start with default settings
- Let system run for full week
- Review first weekly summary
- Decide if target alert rate needs adjustment

### **2. Ongoing (Weeks 2+):**
- Check weekly email Sunday evening
- Research top 5 opportunities
- Trade 1-2 if promising
- Otherwise: Ignore until next week

### **3. Monthly Review:**
- Check `performance_history.json`
- See which tickers alert most often
- Review system adjustments
- Optionally adjust target alert rate

### **4. Quarterly Maintenance:**
- Update Polygon API key if needed
- Verify email still working
- Review discovered tickers
- Check log file size

---

## 💡 Example Workflow

### **Sunday Evening:**

**8:05 PM - Email Arrives:**
```
📊 Weekly Summary - 23 Opportunities Found
```

**8:10 PM - Quick Review (10 minutes):**
- Scan top 10 list
- Note: IONQ (score 88) + CRSP (score 82)
- Google "IONQ quantum breakthrough"
- Google "CRSP FDA fast track"

**8:20 PM - Decision:**
- IONQ looks promising
- Add to eToro watchlist
- Set price alert at $12.00
- Will buy if dips

**8:25 PM - Done!**
- Close email
- Forget about it until next Sunday

---

## 🚨 Important Notes

### **What Autonomous Mode Does:**
✅ Automatically tunes thresholds
✅ Discovers new tickers
✅ Prunes dead tickers
✅ Sends weekly summaries
✅ Self-heals on errors

### **What It Does NOT Do:**
❌ Trade for you
❌ Guarantee profits
❌ Replace your research
❌ Make investment decisions

**You still need to:**
- Research opportunities
- Decide what to trade
- Set stop-losses
- Manage positions

Autonomous mode just **filters the noise** and presents you with **weekly curated opportunities**.

---

## 📋 Comparison: Before vs After

### **Before Autonomous Mode:**
```
Monday: 5 alerts
Tuesday: 3 alerts
Wednesday: 7 alerts
Thursday: 2 alerts
Friday: 4 alerts
Saturday: 0 alerts
Sunday: 6 alerts

Total: 27 alerts to review
Time spent: 2-3 hours/week
Quality: Mixed
```

### **After Autonomous Mode:**
```
Sunday: 1 email with top 10 from week

Total: 10 curated opportunities
Time spent: 15 minutes/week
Quality: Top-scored only
```

**Result:** 85% less time, better quality.

---

## 🎯 Summary

**Autonomous Mode is perfect if you want:**
- 💤 Set it and forget it
- 📧 ONE weekly email (not daily noise)
- 🤖 System that manages itself
- 🎯 Curated opportunities (not spam)
- ⏰ 15 minutes/week (not hours)

**Not perfect if you:**
- Need daily alerts
- Like manual tuning
- Want to see every opportunity
- Prefer active day-trading

---

## 🚀 Ready to Go Autonomous?

**Simple steps:**
1. Double-click: `Start_Autonomous.command`
2. Minimize Terminal (keep open)
3. Check email Sunday evening
4. Repeat weekly

**That's it!** 🎉

System will self-manage:
- ✅ Tune thresholds
- ✅ Discover tickers
- ✅ Prune deadweight
- ✅ Send summaries
- ✅ Heal on errors

**You just:** Review weekly email + Trade good opportunities.

---

**Welcome to truly passive stock screening!** 🤖📈

---

*For questions or issues, check `autonomous_screener.log`*
