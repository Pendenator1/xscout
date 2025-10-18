# XScout Quick Start Guide

Quick reference to get your multi-platform lead finder running.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment

Your `.env` file is already set up with:
- Twitter API credentials
- CallMeBot WhatsApp settings
- Keywords
- Portfolio URL

## 📱 Run Individual Platforms

### Twitter (Continuous)
```bash
python xscout.py
```
Runs continuously, checks every 5 minutes.

### TikTok (Single Run)
```bash
python tiktok_scout.py
```
Searches TikTok once, sends notifications.

### Facebook (Single Run - Requires Login)
```bash
python facebook_scout.py
```
First time: Browser opens, log in manually
Next times: Uses saved session

### All Platforms (Single Run)
```bash
python unified_scout.py
```
Runs Twitter → TikTok → Facebook in sequence.

## ☁️ Deploy to Cloud (FREE)

### GitHub Actions - Twitter Only

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

**Note:** TikTok and Facebook require browser automation and work best locally.

## 🔧 Local Automation (Windows)

### Option 1: Task Scheduler

1. Open **Task Scheduler**
2. **Create Basic Task**
3. Name: "XScout Unified"
4. Trigger: **Daily** at startup
5. Repeat: **Every 1 hour**
6. Action: **Start a program**
7. Program: `python`
8. Arguments: `C:\Users\hp\Desktop\XScout\unified_scout.py`
9. Start in: `C:\Users\hp\Desktop\XScout`

### Option 2: Batch File

Create `run_hourly.bat`:
```batch
@echo off
:loop
python C:\Users\hp\Desktop\XScout\unified_scout.py
timeout /t 3600
goto loop
```

Run this file, it loops every hour.

## 📊 Recommended Schedule

| Platform | Frequency | Method |
|----------|-----------|--------|
| **Twitter** | Every 10 min | GitHub Actions (cloud) |
| **TikTok** | Every 30-60 min | Local automation |
| **Facebook** | Every 1-2 hours | Local automation |
| **All (Unified)** | Every 1 hour | Local automation |

## 🔍 What Happens When You Run

### Twitter (xscout.py)
1. ✅ Validates API credentials
2. 🔍 Searches last hour of tweets
3. 📱 Sends WhatsApp notifications
4. 💬 Auto-replies (if credentials fixed)
5. 😴 Waits 5 minutes
6. 🔄 Repeats

### TikTok (tiktok_scout.py)
1. 🌐 Opens browser (headless)
2. 🔍 Searches 2 keyword queries
3. 📹 Extracts video info
4. 📱 Sends WhatsApp notifications
5. ✅ Completes

### Facebook (facebook_scout.py)
1. 🌐 Opens browser
2. 🔐 Loads saved session OR prompts login
3. 🔍 Searches posts for keywords
4. 📱 Sends WhatsApp notifications
5. 💾 Saves session
6. ✅ Completes

### Unified (unified_scout.py)
Runs all three in sequence.

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

### "playwright not found"
```bash
pip install playwright
playwright install chromium
```

### "No tweets found"
- Check Twitter API credentials
- Verify keywords are realistic
- Check rate limits

### "Facebook session expired"
- Delete `facebook_session.json`
- Run script again to re-login

### "WhatsApp notifications not working"
- Verify CallMeBot setup
- Check phone number format: `+233542855399`
- Test API key at callmebot.com

## 📚 Full Documentation

- **Complete Setup:** `PLATFORM_SETUP_GUIDE.md`
- **GitHub Actions:** `GITHUB_ACTIONS_SETUP.md`
- **TikTok/FB Details:** `TIKTOK_FACEBOOK_EXPANSION.md`

## 🎓 Next Steps

1. ✅ Test each platform individually
2. ✅ Verify notifications work
3. ✅ Adjust keywords based on results
4. ✅ Set up automation (cloud or local)
5. ✅ Monitor and respond to leads
6. ✅ Track conversion rates

Good luck! 🚀
