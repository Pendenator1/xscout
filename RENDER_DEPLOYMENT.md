# Deploy XScout to Render

## Prerequisites
- GitHub account
- Render account (sign up at https://render.com)
- Your Twitter API credentials
- CallMeBot API key

## Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
cd c:\Users\hp\Desktop\XScout
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/xscout.git
git push -u origin main
```

### 2. Deploy on Render

1. Go to https://render.com and sign in
2. Click **"New +"** → **"Background Worker"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** `xscout-bot`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python xscout.py`
   - **Plan:** Select **Free**

### 3. Add Environment Variables

In Render dashboard, go to **Environment** and add these variables:

| Key | Value |
|-----|-------|
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

### 4. Deploy

Click **"Create Background Worker"** and Render will:
- Build your application
- Install dependencies
- Start the bot

### 5. Monitor

- View logs in Render dashboard
- Bot will run 24/7 in the cloud
- Free tier includes 750 hours/month (more than enough)

## Notes

- **Free Tier Limitations:** Service may sleep after 15 minutes of inactivity (won't affect background workers)
- **Logs:** Check Render logs to see tweets found and notifications sent
- **Restart:** Can manually restart from Render dashboard if needed

## Troubleshooting

- If bot stops, check Render logs for errors
- Verify all environment variables are set correctly
- Check Twitter API rate limits in logs
