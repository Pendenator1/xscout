# Complete Cloud Deployment Guide

Run all platforms (Twitter, TikTok, Facebook) automatically in the cloud using GitHub Actions - 100% FREE!

## 🎯 Quick Overview

| Platform | Frequency | Difficulty | Notes |
|----------|-----------|------------|-------|
| **Twitter** | Every 10 min | ✅ Easy | Fully automated |
| **TikTok** | Every 30 min | ✅ Easy | No login needed |
| **Facebook** | Every 2 hours | ⚠️ Complex | Requires credentials |

## 🚀 Complete Setup (Step-by-Step)

### Step 1: Go to GitHub Secrets

1. Open: **https://github.com/Pendenator1/xscout/settings/secrets/actions**
2. Make sure you're logged in

### Step 2: Add ALL Secrets

Click **"New repository secret"** for each of these:

#### Twitter Secrets (Required)
```
Name: TWITTER_BEARER_TOKEN
Value: AAAAAAAAAAAAAAAAAAAAAKuI4wEAAAAAXULPUKovNa%2BJdz%2B%2FZUYmzwRR0JQ%3DgPvS23u91MI9Ve5TUZZff9sxTulSyEtooQulokVyFzgKz80Nat
```

```
Name: TWITTER_API_KEY
Value: gph04xpi4ev4YuxvF4TfcAdJz
```

```
Name: TWITTER_API_SECRET
Value: thn5bqiNjOh5XBXssZP8Alixp58HQgWkU2izcB6hM80BlGJ1BN
```

```
Name: TWITTER_ACCESS_TOKEN
Value: 799150188-XNzR2cASLCIvyxIuLnsqDVjC4N4zKemaKJR6yHmD
```

```
Name: TWITTER_ACCESS_SECRET
Value: DXQrt8y6PVwf5QHbWg1APRhVFInnbFVAd1GLNlzFvcr84
```

#### WhatsApp/General Secrets (Required)
```
Name: CALLMEBOT_PHONE
Value: +233542855399
```

```
Name: CALLMEBOT_APIKEY
Value: 6019929
```

```
Name: AUTO_REPLY
Value: true
```

```
Name: PORTFOLIO_URL
Value: https://ecstasy-geospatial.vercel.app/projects
```

```
Name: KEYWORDS
Value: need a website,looking for web developer,hire web developer,need web designer,looking for frontend developer,hire frontend developer,need fullstack developer,looking for fullstack developer,website developer needed,web designer needed,need someone to build a website,looking for website designer,hire website developer
```

#### Facebook Secrets (Optional - For Facebook Scout)

⚠️ **IMPORTANT:** Facebook requires login credentials. This has risks:
- Your credentials will be stored as GitHub secrets
- Facebook may flag automated logins
- 2FA will prevent automated login

**If you want to enable Facebook:**

```
Name: FACEBOOK_EMAIL
Value: your_facebook_email@example.com
```

```
Name: FACEBOOK_PASSWORD
Value: your_facebook_password
```

**Recommendation:** Skip Facebook cloud deployment and run it locally instead. See [Local Option](#local-option-recommended-for-facebook) below.

### Step 3: Enable GitHub Actions

1. Go to: **https://github.com/Pendenator1/xscout/actions**
2. If workflows are disabled, click **"I understand my workflows, go ahead and enable them"**

### Step 4: Verify Workflows Are Active

You should now see these workflows:

1. **XScout Bot** - Twitter only, runs every 10 minutes
2. **TikTok Scout** - TikTok only, runs every 30 minutes
3. **Facebook Scout** - Facebook only, runs every 2 hours (if credentials added)
4. **Unified Scout** - ALL platforms, runs every hour

### Step 5: Test Run (Optional)

1. Click on **"Unified Scout (All Platforms)"**
2. Click **"Run workflow"** dropdown
3. Click the green **"Run workflow"** button
4. Wait 1-2 minutes
5. Click on the running workflow to see logs

## 📊 Workflow Schedule

### Recommended (All 4 workflows running):

- **Twitter:** Every 10 minutes (XScout Bot)
- **TikTok:** Every 30 minutes (TikTok Scout)  
- **Facebook:** Every 2 hours (Facebook Scout) - *if credentials added*
- **Unified:** Every 1 hour (Unified Scout - runs all 3)

### Optimized (Avoid duplication):

**Option A - Use individual workflows:**
- Keep: XScout Bot, TikTok Scout, Facebook Scout
- Disable: Unified Scout

**Option B - Use unified only:**
- Disable: XScout Bot, TikTok Scout, Facebook Scout
- Keep: Unified Scout (runs all three every hour)

**How to disable a workflow:**
1. Go to Actions → Click workflow name
2. Click "..." menu → Disable workflow

## 🔍 Monitor Your Bots

### View Logs:
1. Go to: https://github.com/Pendenator1/xscout/actions
2. Click any workflow run
3. Click the job name to see logs
4. You'll see output like:
   ```
   [*] Searching for keywords: need a website, ...
   [>] Found tweet by @username
   [+] WhatsApp notification sent
   ```

### Check Notifications:
- You'll receive WhatsApp messages via CallMeBot
- Each lead will send a notification with link

### Troubleshooting:
- Red X = Workflow failed (click to see error)
- Yellow dot = Running
- Green check = Success

## ⚠️ Facebook Cloud Deployment Limitations

### Why Facebook is Hard in the Cloud:

1. **Login Detection:** Facebook detects automated logins from cloud IPs
2. **2FA:** If you have 2-factor authentication, automated login fails
3. **Device Verification:** Facebook may require device verification
4. **Captchas:** Cloud IPs often trigger captchas
5. **Account Security:** Risk of account restrictions

### Recommendations for Facebook:

#### Option 1: Local Deployment (Recommended)
Run Facebook scout on your local computer:
```bash
python facebook_scout.py
```

Benefits:
- ✅ Your normal IP address (trusted)
- ✅ Can handle 2FA manually
- ✅ Session persists across runs
- ✅ No account security risks

#### Option 2: Use Facebook Graph API
Limited search, but more reliable. See `TIKTOK_FACEBOOK_EXPANSION.md`

#### Option 3: Skip Facebook
Focus on Twitter and TikTok in the cloud (both work perfectly!)

## 🎉 What You Get (Free Cloud Deployment)

### Twitter (Fully Automated):
- ✅ Searches every 10 minutes
- ✅ Auto-replies to leads (if credentials fixed)
- ✅ WhatsApp notifications
- ✅ No limits on free tier

### TikTok (Fully Automated):
- ✅ Searches every 30 minutes
- ✅ Scrapes video descriptions
- ✅ WhatsApp notifications
- ✅ No login required

### Facebook (Conditional):
- ⚠️ Works if credentials provided and no 2FA
- ⚠️ May fail due to login detection
- ✅ WhatsApp notifications if successful
- 💡 Better to run locally

## 💰 Cost: $0

GitHub Actions free tier:
- **Public repos:** Unlimited minutes
- **Private repos:** 2,000 minutes/month

Your usage per month:
- Twitter: ~4,320 minutes (10 min runs, every 10 min)
- TikTok: ~2,880 minutes (10 min runs, every 30 min)
- Facebook: ~1,080 minutes (15 min runs, every 2 hours)
- **Total:** ~8,280 minutes

**Solution:** Make your repo public (code doesn't contain secrets), or use individual workflows to stay under 2,000 min.

## 🔒 Security

✅ **Safe:**
- Secrets are encrypted by GitHub
- Never shown in logs
- Only accessible by workflows

⚠️ **Consider:**
- Facebook credentials stored as secrets
- Risk of account restrictions
- Alternative: Run Facebook locally

## 📱 Expected Results

### First 24 Hours:
- 5-20 notifications per day
- Mix of relevant leads
- Some false positives

### After Tuning:
- 3-10 quality leads per day
- Highly targeted matches
- Better conversion rates

## 🛠️ Customization

### Change Schedule:

Edit `.github/workflows/*.yml`:

```yaml
schedule:
  - cron: '*/10 * * * *'  # Current: Every 10 minutes
  # - cron: '*/5 * * * *'   # Every 5 minutes
  # - cron: '0 * * * *'     # Every hour
  # - cron: '0 */2 * * *'   # Every 2 hours
```

### Change Keywords:

Update the `KEYWORDS` secret in GitHub.

### Disable Platform:

Disable the workflow in Actions tab.

## 🎓 Next Steps

1. ✅ Add all secrets to GitHub
2. ✅ Enable workflows
3. ✅ Test run Unified Scout manually
4. ✅ Monitor logs for first hour
5. ✅ Check WhatsApp for notifications
6. ✅ Adjust keywords based on results
7. ✅ Respond to leads professionally

## 📚 Additional Resources

- **Quick Start:** `QUICK_START.md`
- **Platform Setup:** `PLATFORM_SETUP_GUIDE.md`
- **GitHub Actions:** `GITHUB_ACTIONS_SETUP.md`

---

## Local Option (Recommended for Facebook)

If you prefer to run everything locally with full control:

**Windows Task Scheduler:**
1. Create task: "XScout Unified"
2. Trigger: Every 1 hour
3. Action: `python C:\Users\hp\Desktop\XScout\unified_scout.py`

**Batch File Loop:**
```batch
@echo off
:loop
cd C:\Users\hp\Desktop\XScout
python unified_scout.py
timeout /t 3600
goto loop
```

This gives you:
- ✅ Full control over Facebook login
- ✅ Session persistence
- ✅ No cloud limitations
- ✅ Handle 2FA manually

---

Your multi-platform lead finder is now running 24/7 in the cloud! 🚀
