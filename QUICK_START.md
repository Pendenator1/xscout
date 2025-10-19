# XScout Quick Start Guide

Quick reference to get your Twitter lead finder running.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Your `.env` file is already set up with:
- Twitter API credentials
- CallMeBot WhatsApp settings
- Keywords
- Portfolio URL

## 📱 Run XScout

### Twitter (Continuous)
```bash
python xscout.py
```
Runs continuously, checks every 5 minutes.

### Single Run
```bash
python xscout.py --single-run
```
Runs Twitter search once (searches last 15 minutes).

## ☁️ Deploy to Cloud (FREE)

### GitHub Actions - Automated Twitter Monitoring

1. Go to: https://github.com/Pendenator1/xscout/settings/secrets/actions
2. Add these secrets:
   - `TWITTER_BEARER_TOKEN`
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`
   - `CALLMEBOT_PHONE`
   - `CALLMEBOT_APIKEY`
   - `AUTO_REPLY`
   - `PORTFOLIO_URL`
   - `KEYWORDS`

3. Go to: https://github.com/Pendenator1/xscout/actions
4. Enable workflows
5. Done! Runs every 10 minutes automatically

## 🔧 Local Automation (Windows)

### Option 1: Task Scheduler

1. Open **Task Scheduler**
2. **Create Basic Task**
3. Name: "XScout"
4. Trigger: **Daily** at startup
5. Repeat: **Every 1 hour**
6. Action: **Start a program**
7. Program: `python`
8. Arguments: `C:\Users\hp\Desktop\XScout\xscout.py --single-run`
9. Start in: `C:\Users\hp\Desktop\XScout`

### Option 2: Batch File

Create `run_hourly.bat`:
```batch
@echo off
:loop
python C:\Users\hp\Desktop\XScout\xscout.py --single-run
timeout /t 3600
goto loop
```

Run this file, it loops every hour.

## 📊 Recommended Schedule

| Platform | Frequency | Method |
|----------|-----------|--------|
| **Twitter** | Every 10 min | GitHub Actions (cloud) |

## 🔍 What Happens When You Run

### Twitter (xscout.py)
1. ✅ Validates API credentials
2. 🔍 Searches last hour of tweets
3. 📱 Sends WhatsApp notifications
4. 💬 Auto-replies (if enabled)
5. 😴 Waits 5 minutes
6. 🔄 Repeats

## 🎯 Expected Results

### First Day
- 5-20 notifications (depending on keywords)
- Mix of relevant and semi-relevant leads
- Some false positives

### After Keyword Tuning
- More targeted leads
- Better quality prospects
- Fewer false positives

## ⚙️ Customize Keywords

Edit `.env`:
```
KEYWORDS=need a website,looking for web developer,hire developer,website developer needed
```

**Tips:**
- Use specific phrases
- Include variations
- Test individually
- Monitor results

## 🆘 Common Issues

### "No tweets found"
- Check Twitter API credentials
- Verify keywords are realistic
- Check rate limits

### "WhatsApp notifications not working"
- Verify CallMeBot setup
- Check phone number format: `+233542855399`
- Test API key at callmebot.com

## 📚 Full Documentation

- **Complete Setup:** `PLATFORM_SETUP_GUIDE.md`
- **GitHub Actions:** `GITHUB_ACTIONS_SETUP.md`

## 🎓 Next Steps

1. ✅ Test Twitter individually
2. ✅ Verify notifications work
3. ✅ Adjust keywords based on results
4. ✅ Set up automation (cloud or local)
5. ✅ Monitor and respond to leads
6. ✅ Track conversion rates

Good luck! 🚀
