# 🚀 Quick AI Setup (2 Minutes)

## ✅ Your Status
- ✅ AI code integrated
- ✅ Dependencies installed
- ✅ Configuration ready

## 🎯 What You Have Now

### 1. **Smart Lead Filtering**
- AI scores each tweet 0-10
- Only processes quality leads (score ≥ 7)
- Filters out spam automatically

### 2. **Personalized Replies**
- AI reads the tweet and creates custom responses
- References specific details from their message
- Much better than generic templates

### 3. **All Features FREE**
- Using Google Gemini free tier
- 15 requests/minute
- 1 million tokens/day
- No credit card needed

## 🔑 Already Configured

Your `.env` file already has:
```env
GEMINI_API_KEY=your_gemini_api_key_here
ENABLE_AI_FEATURES=true
AI_MIN_LEAD_SCORE=7
```

**Note:** Replace `your_gemini_api_key_here` with your actual API key from https://makersuite.google.com/app/apikey

## 🎮 How to Use

Just run your bot normally:

```bash
# Continuous monitoring
python xscout.py

# Single run (for GitHub Actions)
python xscout_single_run.py
```

## 📊 What You'll See

```
[*] Searching for 13 keywords:
    1. 'need a website'
    2. 'looking for web developer'
    ...

[>] Found tweet by @john_doe:
   "Need a React developer ASAP for my SaaS project..."
   https://twitter.com/john_doe/status/...

[*] AI analyzing lead quality...
[AI] Score: 9/10 - Clear urgency, specific tech stack, likely has budget
[+] Quality lead detected!

[*] Generating AI reply for @john_doe...
[+] AI generated personalized reply
[+] Auto-replied to @john_doe
[+] WhatsApp notification sent
```

## ⚙️ Settings You Can Adjust

In `.env`:

| Setting | What It Does | Recommended |
|---------|--------------|-------------|
| `AI_MIN_LEAD_SCORE` | Minimum score to process | Start with 7 |
| `ENABLE_AI_FEATURES` | Turn AI on/off | `true` |
| `AUTO_REPLY` | Enable AI replies | `true` |

**Tip:** If you're getting too many notifications, increase `AI_MIN_LEAD_SCORE` to `8`. If too few, lower it to `6`.

## 🔍 How AI Scores Leads

- **10/10**: "Need React dev, $5k budget, start Monday"
- **9/10**: "Looking for full-stack developer for e-commerce site"
- **7/10**: "Anyone know a good web developer?"
- **5/10**: "Thinking about getting a website"
- **2/10**: "Websites are cool" (not a real lead)

## 💡 Pro Tips

1. **Watch the scores** for a few hours to understand AI's judgment
2. **Adjust threshold** based on how many leads you want
3. **AI replies are contextual** - they reference the person's tweet
4. **All automatic** - just let it run!

## 🆘 Troubleshooting

**Not seeing "[+] AI Features enabled"?**
- Your API key might be invalid
- Check GEMINI_API_KEY in .env
- Get a new one: https://makersuite.google.com/app/apikey

**Getting too many/few leads?**
- Adjust AI_MIN_LEAD_SCORE in .env
- Higher number = fewer, better leads
- Lower number = more leads, some noise

**AI replies not working?**
- Check AUTO_REPLY=true in .env
- Verify PORTFOLIO_URL is set
- Make sure Twitter has Read+Write permissions

## 📈 Next Steps

1. Run the bot: `python xscout.py`
2. Watch the AI in action
3. Adjust settings as needed
4. Enjoy better leads!

---

**Full documentation:** See `AI_FEATURES.md` for complete details.
