# 🤖 AI Features for XScout

XScout now includes **FREE AI-powered features** using Google Gemini to help you find better leads and engage more effectively!

## 🎯 Features

### 1. **AI Lead Filtering** 🔍
- Automatically scores each tweet from 0-10 based on quality
- Filters out spam, bots, and low-quality leads
- Only notifies you about high-quality opportunities (score ≥ 7)
- Saves time by focusing on the best prospects

**Example:**
```
[AI] Score: 9/10 - Strong lead with specific budget and timeline mentioned
[+] Quality lead detected!
```

### 2. **AI Reply Generation** ✍️
- Creates personalized responses for each lead
- References specific details from their tweet
- More natural and engaging than templates
- Increases response rates

**Example:**
Instead of generic template:
> "Hi! I'm a web developer. Check out my portfolio..."

AI generates:
> "I'd love to help with your e-commerce project! I've built several Shopify sites with custom features. Check out my work: [portfolio] Let's discuss your requirements!"

### 3. **AI Keyword Expansion** 🔎
- Coming soon: Auto-generate new search keywords
- Discovers phrases you might have missed
- Adapts to trends and client language

## 🚀 Setup (Free!)

### Step 1: Get Google Gemini API Key (100% FREE)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your key

**Free Limits:**
- ✅ 15 requests/minute
- ✅ 1 million tokens/day  
- ✅ No credit card required

### Step 2: Configure XScout

Add to your `.env` file:

```env
# AI Features
GEMINI_API_KEY=your_api_key_here
ENABLE_AI_FEATURES=true
AI_MIN_LEAD_SCORE=7
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### `.env` Settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `GEMINI_API_KEY` | Required | Your Google Gemini API key |
| `ENABLE_AI_FEATURES` | `false` | Turn AI features on/off |
| `AI_MIN_LEAD_SCORE` | `7` | Minimum score (0-10) to process a lead |

### Lead Score Guide:

- **9-10**: Excellent lead - Clear intent, budget, urgency
- **7-8**: Good lead - Specific requirements, serious inquiry
- **5-6**: Possible lead - Vague but might be real
- **3-4**: Low quality - Generic or unclear
- **0-2**: Poor lead - Spam, bots, or irrelevant

**Tip:** Lower `AI_MIN_LEAD_SCORE` to get more leads, raise it for higher quality only.

## 📊 Usage

Once configured, AI features work automatically:

```bash
python xscout.py
```

You'll see AI in action:

```
[*] Searching for 13 keywords:
    1. 'need a website'
    2. 'looking for web developer'
    ...

[>] Found tweet by @potential_client:
   "Looking for a React developer to build a SaaS dashboard..."
   https://twitter.com/potential_client/status/...

[*] AI analyzing lead quality...
[AI] Score: 9/10 - Clear project requirements with specific tech stack mentioned
[+] Quality lead detected!

[*] Generating AI reply for @potential_client...
[+] AI generated personalized reply

[+] Auto-replied to @potential_client
[+] WhatsApp notification sent
```

## 🔧 Troubleshooting

### "AI Features disabled"
- Check that `ENABLE_AI_FEATURES=true` in `.env`
- Verify your `GEMINI_API_KEY` is correct
- Make sure you ran `pip install -r requirements.txt`

### "AI scoring error"
- Check your internet connection
- Verify API key hasn't expired
- Check you haven't exceeded free tier limits (rare)

### API Rate Limits
Free tier: 15 requests/minute is plenty for XScout's usage pattern. Each tweet uses 1-2 requests (scoring + reply).

## 💡 Tips

1. **Start with default settings**: `AI_MIN_LEAD_SCORE=7` is a good balance
2. **Review AI scores**: Watch the logs to understand how AI rates different tweets
3. **Adjust threshold**: If too few leads, lower to `6`. If too many spam, raise to `8`
4. **AI replies are optional**: You can use AI for filtering only by setting `AUTO_REPLY=false`

## 🆚 With vs Without AI

### Without AI:
- Gets all matching tweets (including spam)
- Generic template replies
- Manual filtering needed
- Lower conversion rates

### With AI:
- Only quality leads
- Personalized responses
- Automatic filtering
- Higher conversion rates
- More efficient use of time

## 📈 Next Steps

- Monitor your AI lead scores for a few days
- Adjust `AI_MIN_LEAD_SCORE` based on results
- Watch your response rates improve
- Focus your time on quality conversations

## 🔐 Privacy & Security

- Your API key stays in `.env` (never committed to git)
- Tweets are only sent to Gemini for analysis
- No data is stored by the AI
- You control what gets processed

---

**Questions?** Check the main README.md or raise an issue!
