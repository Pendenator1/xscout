# XScout - Twitter Lead Monitoring Bot

A Python bot that monitors X (Twitter) in real-time for specific keywords and sends instant notifications via Telegram.

## 🚀 Features

- Real-time tweet monitoring for custom keywords
- Instant WhatsApp notifications via Twilio
- Filters out retweets and non-English tweets
- Rate limit handling
- Easy configuration via environment variables

## 📋 Prerequisites

- Python 3.8 or higher
- X (Twitter) Developer Account with API access
- Twilio Account (for WhatsApp notifications)

## 🔧 Setup Instructions

### 1. Get X Developer Access

1. Go to [developer.x.com/en/portal/dashboard](https://developer.x.com/en/portal/dashboard)
2. Apply for a Developer Account
3. Create a Project and an App
4. Under "Keys and Tokens", copy:
   - Bearer Token
   - API Key
   - API Secret
   - Access Token & Secret

### 2. Set Up WhatsApp with Twilio

**See the detailed guide: [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)**

Quick steps:
1. Create free account at [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Get your Account SID and Auth Token from the console
3. Join WhatsApp Sandbox by sending join code to Twilio number
4. Configure your phone number in `.env`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   TWITTER_BEARER_TOKEN=your_actual_token
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
   WHATSAPP_TO=whatsapp:+1234567890
   KEYWORDS=need a website,looking for developer,hire developer
   ```

### 5. Run the Bot

```bash
python xscout.py
```

## 🎯 Customizing Keywords

Edit the `KEYWORDS` in your `.env` file:

```
KEYWORDS=need a website,looking for web developer,hire freelancer,need SEO expert
```

Separate multiple keywords with commas.

## ⚙️ Configuration

- **Interval**: Change the search interval by modifying the `interval` parameter in `xscout.py`:
  ```python
  bot.run(interval=60)  # Check every 60 seconds
  ```

- **Max Results**: Adjust the number of tweets fetched per search:
  ```python
  max_results=10  # In the search_tweets() method
  ```

## 🛡️ Important Notes

- X API Free tier has rate limits (50 requests per 15 minutes for search)
- The bot filters out retweets automatically
- Only English tweets are included by default
- Duplicate tweets are tracked and ignored

## 📝 License

MIT License - feel free to modify and use for your projects!

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## ⚠️ Disclaimer

Use responsibly and comply with X's Developer Agreement and Policy.
