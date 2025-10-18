# Deploy XScout Using GitHub Actions (100% FREE)

GitHub Actions allows you to run your bot automatically on a schedule at no cost.

## Setup Instructions

### 1. Push Code to GitHub

Your code is already on GitHub at: https://github.com/Pendenator1/xscout.git

### 2. Add Secrets to GitHub Repository

1. Go to your repository: https://github.com/Pendenator1/xscout
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of these:

| Secret Name | Value |
|-------------|-------|
| `TWITTER_BEARER_TOKEN` | Your Twitter bearer token |
| `TWITTER_API_KEY` | Your Twitter API key |
| `TWITTER_API_SECRET` | Your Twitter API secret |
| `TWITTER_ACCESS_TOKEN` | Your Twitter access token |
| `TWITTER_ACCESS_SECRET` | Your Twitter access secret |
| `CALLMEBOT_PHONE` | +233542855399 |
| `CALLMEBOT_APIKEY` | 6019929 |
| `AUTO_REPLY` | true |
| `PORTFOLIO_URL` | https://ecstasy-geospatial.vercel.app/projects |
| `KEYWORDS` | need a website,looking for web developer,hire web developer,need web designer,looking for frontend developer,hire frontend developer,need fullstack developer,looking for fullstack developer,website developer needed,web designer needed,need someone to build a website,looking for website designer,hire website developer |

### 3. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Enable workflows if prompted
3. The bot will run automatically every 10 minutes

### 4. Manual Trigger (Optional)

You can manually trigger the workflow:
1. Go to **Actions** tab
2. Select **XScout Bot** workflow
3. Click **Run workflow**

## How It Works

- Runs every 10 minutes automatically
- Searches for tweets from the last 15 minutes
- Sends WhatsApp notifications for new leads
- Auto-replies to tweets (if enabled)
- Completely free (GitHub provides 2,000 minutes/month for private repos, unlimited for public)

## Customize Schedule

Edit `.github/workflows/xscout.yml` to change the schedule:

```yaml
schedule:
  - cron: '*/10 * * * *'  # Every 10 minutes
  # - cron: '*/5 * * * *'  # Every 5 minutes
  # - cron: '0 * * * *'    # Every hour
```

## View Logs

1. Go to **Actions** tab
2. Click on any workflow run
3. Click **run-bot** to see logs

## Advantages

- ✅ 100% Free
- ✅ No server management
- ✅ Reliable (GitHub infrastructure)
- ✅ Easy to monitor (built-in logs)
- ✅ Automatically restarts on failure
- ✅ No credit card required

## Limitations

- Runs on a schedule (not continuous)
- Maximum 2,000 minutes/month on private repos (plenty for this use case)
- Each run is isolated (no persistent state between runs)
