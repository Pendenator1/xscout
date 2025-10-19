# Complete Cloud Deployment Guide

Run Twitter lead finding automatically in the cloud using GitHub Actions - 100% FREE!

## 🎯 Quick Overview

| Platform | Frequency | Difficulty | Notes |
|----------|-----------|------------|-------|
| **Twitter** | Every 10 min | ✅ Easy | Fully automated |

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

### Step 3: Enable GitHub Actions

1. Go to: **https://github.com/Pendenator1/xscout/actions**
2. If workflows are disabled, click **"I understand my workflows, go ahead and enable them"**

### Step 4: Verify Workflows Are Active

You should now see the workflow:

**XScout Bot** - Twitter, runs every 10 minutes

### Step 5: Test Run (Optional)

1. Click on **"XScout Bot"**
2. Click **"Run workflow"** dropdown
3. Click the green **"Run workflow"** button
4. Wait 1-2 minutes
5. Click on the running workflow to see logs

## 📊 Workflow Schedule

**Recommended:**
- **Twitter:** Every 10 minutes (XScout Bot)

## 🔍 Monitor Your Bot

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

## 🎉 What You Get (Free Cloud Deployment)

### Twitter (Fully Automated):
- ✅ Searches every 10 minutes
- ✅ Auto-replies to leads (if enabled)
- ✅ WhatsApp notifications
- ✅ No limits on free tier

## 💰 Cost: $0

GitHub Actions free tier:
- **Public repos:** Unlimited minutes
- **Private repos:** 2,000 minutes/month

Your usage per month:
- Twitter: ~4,320 minutes (10 min runs, every 10 min)

**Solution:** Make your repo public (code doesn't contain secrets), or optimize workflow frequency.

## 🔒 Security

✅ **Safe:**
- Secrets are encrypted by GitHub
- Never shown in logs
- Only accessible by workflows

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

Edit `.github/workflows/xscout.yml`:

```yaml
schedule:
  - cron: '*/10 * * * *'  # Current: Every 10 minutes
  # - cron: '*/5 * * * *'   # Every 5 minutes
  # - cron: '0 * * * *'     # Every hour
  # - cron: '0 */2 * * *'   # Every 2 hours
```

### Change Keywords:

Update the `KEYWORDS` secret in GitHub.

## 🎓 Next Steps

1. ✅ Add all secrets to GitHub
2. ✅ Enable workflows
3. ✅ Test run XScout Bot manually
4. ✅ Monitor logs for first hour
5. ✅ Check WhatsApp for notifications
6. ✅ Adjust keywords based on results
7. ✅ Respond to leads professionally

## 📚 Additional Resources

- **Quick Start:** `QUICK_START.md`
- **Platform Setup:** `PLATFORM_SETUP_GUIDE.md`
- **GitHub Actions:** `GITHUB_ACTIONS_SETUP.md`

---

## Local Option

If you prefer to run everything locally with full control:

**Windows Task Scheduler:**
1. Create task: "XScout"
2. Trigger: Every 1 hour
3. Action: `python C:\Users\hp\Desktop\XScout\xscout.py --single-run`

**Batch File Loop:**
```batch
@echo off
:loop
cd C:\Users\hp\Desktop\XScout
python xscout.py --single-run
timeout /t 3600
goto loop
```

This gives you:
- ✅ Full control
- ✅ No cloud limitations

---

Your Twitter lead finder is now running 24/7 in the cloud! 🚀
