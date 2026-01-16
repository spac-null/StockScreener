# Quick Context - Enhanced Stock Screener

## Project
**Name:** Enhanced Stock Screener
**Purpose:** Multi-source stock screening with 6 FREE APIs
**Status:** ✅ Production Ready

## Tech Stack
**Backend:** Python 3.14
**Data:** yfinance, Alpha Vantage, NewsAPI, SEC Edgar, Reddit (optional), Polygon (optional)
**Architecture:** Multi-source scoring, cache + rate limiting, rich terminal UI

## Critical Rules
1. **All APIs are FREE** - No paid services
2. **Graceful degradation** - Works with 2+ sources
3. **Cache-first** - Respect API rate limits (Alpha Vantage: 25/day)

## File Locations
- **Main:** `stock_screener_free_enhanced.py`
- **Config:** `config_free_enhanced.yaml`
- **Launcher:** `Start_Enhanced.command` (double-click)
- **Logs:** `enhanced_screener.log`
- **Cache:** `.cache/` directory

## Key Commands
```bash
# Run
python stock_screener_free_enhanced.py

# Or double-click
Start_Enhanced.command

# Test
python tests/test_infrastructure.py

# Clear cache
rm -rf .cache/
```

## Next Priorities
1. Optional: Add Reddit API keys
2. Optional: Tune weights based on results
3. Monitor: Check logs after 24h run

## Remember
> "Multi-source = cross-validation. Cache = respect limits. Rich UI = user satisfaction."

---

**READ FIRST AFTER CONTEXT WIPE:** `START_HERE.md`
**THEN READ:** `.claude/CONTINUATION_GUIDE.md`
