# Twitter Lead Finder Setup Guide

Complete guide to setting up Twitter lead finding with XScout.

## Table of Contents
- [Installation](#installation)
- [Twitter Setup](#twitter-setup)
- [Running the Bot](#running-the-bot)
- [Troubleshooting](#troubleshooting)

---

## Installation

### 1. Install Python Dependencies

```bash
cd C:\Users\hp\Desktop\XScout
pip install -r requirements.txt
```

---

## Twitter Setup

Already configured! Your Twitter bot is working with:
- ✅ Twitter API credentials
- ✅ WhatsApp notifications via CallMeBot
- ✅ Auto-reply functionality

**To run Twitter:**
```bash
python xscout.py
```

---

## Running the Bot

### Run Twitter Scout

```bash
python xscout.py
```

This runs continuously and checks every 5 minutes.

### Run Single Search

```bash
python unified_scout.py
```

This runs a single Twitter search.

### Run on Schedule (Local)

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every 1 hour)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\Users\hp\Desktop\XScout\unified_scout.py`

**Or use batch file:**

Create `run_all_scouts.bat`:
```batch
@echo off
cd C:\Users\hp\Desktop\XScout
python unified_scout.py
pause
```

---

## GitHub Actions (Cloud Deployment)

For running in the cloud, see:
- **Twitter:** Already configured in `.github/workflows/xscout.yml`

---

## Troubleshooting

### General Issues

**Problem:** "Module not found"
```bash
pip install -r requirements.txt
```

**Problem:** "WhatsApp notifications not working"
- Check `CALLMEBOT_PHONE` and `CALLMEBOT_APIKEY` in `.env`
- Verify CallMeBot is set up correctly

---

## Security & Privacy

⚠️ **Important:**

1. **Keep `.env` private** (already in .gitignore)
2. **Respect ToS** of Twitter
3. **Be ethical** in your outreach

---

## Recommended Schedule

- **Twitter:** Every 10 minutes (via GitHub Actions)

---

## Next Steps

1. ✅ Test Twitter individually
2. ✅ Verify WhatsApp notifications work
3. ✅ Set up scheduled runs
4. ✅ Monitor results and adjust keywords
5. ✅ Respond to leads professionally

---

## Need Help?

Check the logs for detailed error messages:
- Twitter errors usually indicate API issues

Good luck finding leads! 🚀
