# Multi-Platform Setup Guide

Complete guide to setting up Twitter, TikTok, and Facebook lead finding.

## Table of Contents
- [Installation](#installation)
- [Twitter Setup](#twitter-setup)
- [TikTok Setup](#tiktok-setup)
- [Facebook Setup](#facebook-setup)
- [Running the Bots](#running-the-bots)
- [Troubleshooting](#troubleshooting)

---

## Installation

### 1. Install Python Dependencies

```bash
cd C:\Users\hp\Desktop\XScout
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

Playwright needs to download browser binaries:

```bash
playwright install chromium
```

This downloads Chromium browser (~300MB) for web scraping.

---

## Twitter Setup

Already configured! Your Twitter bot is working with:
- ✅ Twitter API credentials
- ✅ WhatsApp notifications via CallMeBot
- ✅ Auto-reply functionality

**To run Twitter only:**
```bash
python xscout.py
```

---

## TikTok Setup

### How It Works
- Searches TikTok for your keywords
- Scrapes video information (no API needed)
- Sends WhatsApp notifications for matches

### Configuration

Your keywords from `.env` are automatically used:
```
KEYWORDS=need a website,looking for web developer,hire web developer,...
```

### Run TikTok Scout

```bash
python tiktok_scout.py
```

### What to Expect

1. **First Run:** Browser opens, searches TikTok
2. **Headless Mode:** Runs in background (no visible browser)
3. **Results:** Finds videos matching your keywords
4. **Notifications:** WhatsApp alerts for each match

### Limitations

- TikTok may show login prompts occasionally
- Search results limited by TikTok (no API access)
- Rate limiting: Don't run too frequently (every 30+ minutes recommended)

### TikTok Best Practices

✅ **DO:**
- Run every 30-60 minutes
- Use 2-3 search queries at a time
- Monitor for TikTok changes (selectors may update)

❌ **DON'T:**
- Run every few minutes (will trigger rate limits)
- Use too many search queries in one run
- Leave browser open for hours

---

## Facebook Setup

### How It Works
- Searches Facebook posts for your keywords
- **Requires:** Manual login (first time)
- Saves session for future runs
- Sends WhatsApp notifications

### First-Time Setup

1. **Run the script:**
   ```bash
   python facebook_scout.py
   ```

2. **Browser opens** - you'll see:
   ```
   [!] NOT LOGGED IN TO FACEBOOK
   [!] Please log in manually in the browser window
   [!] After logging in, the bot will continue automatically
   ```

3. **Log in manually** in the browser window:
   - Enter your email/phone
   - Enter your password
   - Complete any 2FA if enabled
   - Wait for homepage to load

4. **Session saved automatically:**
   ```
   [+] Successfully logged in!
   [+] Session saved for future use
   ```

5. **Bot continues** searching automatically

### Subsequent Runs

After first login:
- Session is loaded from `facebook_session.json`
- No manual login needed (unless session expires)
- Runs automatically

### Facebook Groups (Optional)

To monitor specific groups, add to `.env`:

```
FACEBOOK_GROUPS=123456789,987654321
```

### What Facebook Scout Searches

- Public posts matching your keywords
- Marketplace requests (if available in your region)
- Posts from groups you're a member of

### Run Facebook Scout

```bash
python facebook_scout.py
```

### Limitations

- **Requires login:** Cannot search Facebook without authentication
- **Session expires:** May need to re-login every 7-30 days
- **Limited search:** Facebook removed public keyword search for non-ads
- **Rate limits:** Don't run too frequently

### Facebook Best Practices

✅ **DO:**
- Join relevant freelancer/business groups manually
- Run every 1-2 hours
- Keep session file secure (don't commit to git)
- Use specific search terms

❌ **DON'T:**
- Share your session file
- Run every few minutes
- Search too broadly
- Violate Facebook's Terms of Service

---

## Running the Bots

### Run Individual Platforms

**Twitter only:**
```bash
python xscout.py
```

**TikTok only:**
```bash
python tiktok_scout.py
```

**Facebook only:**
```bash
python facebook_scout.py
```

### Run All Platforms Together

```bash
python unified_scout.py
```

This runs Twitter → TikTok → Facebook in sequence.

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
- **TikTok/Facebook:** Requires persistent sessions (harder to run in cloud)

**Note:** TikTok and Facebook work best running locally due to login requirements.

---

## Troubleshooting

### TikTok Issues

**Problem:** "No videos found"
- **Solution:** TikTok changed their HTML structure. Selectors need updating.

**Problem:** "Timeout loading page"
- **Solution:** Increase timeout, check internet connection.

**Problem:** "Rate limit exceeded"
- **Solution:** Reduce search frequency, use fewer keywords.

### Facebook Issues

**Problem:** "Session expired"
- **Solution:** Delete `facebook_session.json` and run script again to re-login.

**Problem:** "No posts found"
- **Solution:** Facebook search is limited. Try joining specific groups and searching within them.

**Problem:** "Login timeout"
- **Solution:** Log in faster, or increase wait time in script.

### General Issues

**Problem:** "playwright not found"
```bash
pip install playwright
playwright install chromium
```

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

1. **Never commit** `facebook_session.json` to Git
2. **Keep `.env` private** (already in .gitignore)
3. **Don't share** your session files
4. **Respect ToS** of each platform
5. **Be ethical** in your outreach

---

## Platform Comparison

| Platform | API Access | Login Required | Best For |
|----------|-----------|----------------|----------|
| **Twitter** | ✅ Yes | No (API Key) | Real-time leads, easy setup |
| **TikTok** | ❌ No | No | Video-based leads, younger audience |
| **Facebook** | ⚠️ Limited | Yes | Groups, marketplace, B2B leads |

---

## Recommended Schedule

- **Twitter:** Every 10 minutes (via GitHub Actions)
- **TikTok:** Every 30-60 minutes (local)
- **Facebook:** Every 1-2 hours (local)
- **Unified:** Every 1 hour (local)

---

## Next Steps

1. ✅ Test each platform individually
2. ✅ Verify WhatsApp notifications work
3. ✅ Set up scheduled runs
4. ✅ Monitor results and adjust keywords
5. ✅ Join relevant Facebook groups
6. ✅ Respond to leads professionally

---

## Need Help?

Check the logs for detailed error messages:
- Twitter errors usually indicate API issues
- TikTok errors often mean selector changes
- Facebook errors typically relate to sessions/login

Good luck finding leads! 🚀
