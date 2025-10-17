# WhatsApp API Setup Guide

This guide will walk you through setting up WhatsApp notifications for XScout using Twilio.

## 📱 Option 1: Twilio WhatsApp API (Recommended - Easiest)

### Step 1: Create a Twilio Account

1. Go to [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your email and phone number
4. You'll get **$15 in free credits** (enough for thousands of messages)

### Step 2: Get Your API Credentials

1. After logging in, go to your [Twilio Console](https://console.twilio.com/)
2. You'll see your dashboard with:
   - **Account SID** (looks like: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - **Auth Token** (click to reveal)
3. Copy both values - you'll need them for your `.env` file

### Step 3: Set Up WhatsApp Sandbox

Since you're testing, you'll use Twilio's WhatsApp Sandbox:

1. In Twilio Console, go to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. You'll see a page with:
   - A WhatsApp number (usually `+1 415 523 8886`)
   - A join code (like `join <word>-<word>`)

3. **Activate your WhatsApp:**
   - Open WhatsApp on your phone
   - Send the join code to the Twilio number
   - Example: Send `join abc-def` to `+1 415 523 8886`
   - You'll get a confirmation message

### Step 4: Configure Your .env File

Open your `.env` file and add:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+1234567890
```

**Replace:**
- `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your Account SID
- `your_auth_token_here` with your Auth Token
- `+1234567890` with YOUR phone number (including country code)

**Important:** 
- Keep the `whatsapp:` prefix
- Use international format: `whatsapp:+1234567890` (not `+1 (234) 567-890`)
- For US numbers: `whatsapp:+1234567890`
- For UK numbers: `whatsapp:+44234567890`
- For India: `whatsapp:+91234567890`

### Step 5: Test Your Setup

Run the bot:
```bash
python xscout.py
```

You should receive WhatsApp messages when leads are found!

---

## 📱 Option 2: WhatsApp Cloud API (Free, More Complex)

If you want unlimited free messages, you can use Meta's WhatsApp Cloud API:

### Step 1: Create a Meta Developer Account

1. Go to [developers.facebook.com](https://developers.facebook.com/)
2. Create an account or log in
3. Click **My Apps** → **Create App**
4. Select **Business** type

### Step 2: Set Up WhatsApp Business

1. In your app dashboard, click **Add Products**
2. Find **WhatsApp** and click **Set Up**
3. Under **API Setup**, you'll see:
   - **Temporary access token** (valid for 24 hours)
   - **Phone number ID**
   - **WhatsApp Business Account ID**

### Step 3: Get Permanent Access Token

1. Go to **WhatsApp** → **Getting Started**
2. Click **Generate Token**
3. Select permissions: `whatsapp_business_messaging`
4. Copy the permanent token

### Step 4: Add Your Phone Number

1. In WhatsApp settings, click **Add Recipient Phone Number**
2. Enter your phone number with country code
3. Verify it with the code sent to WhatsApp

### Step 5: Modify the Bot (Advanced)

You'll need to update `xscout.py` to use WhatsApp Cloud API instead of Twilio:

```python
def send_whatsapp_notification(self, tweet_text, tweet_url, author):
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    to_number = os.getenv('WHATSAPP_TO')
    
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    
    message = f"🚨 New Lead Found!\n\nAuthor: @{author}\nTweet: {tweet_text[:200]}...\n\nView: {tweet_url}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'messaging_product': 'whatsapp',
        'to': to_number,
        'type': 'text',
        'text': {'body': message}
    }
    
    response = requests.post(url, headers=headers, json=payload)
```

---

## 🆚 Comparison: Twilio vs WhatsApp Cloud API

| Feature | Twilio | WhatsApp Cloud API |
|---------|--------|-------------------|
| Setup Difficulty | ⭐ Easy | ⭐⭐⭐ Complex |
| Free Credits | $15 (~4,500 messages) | Unlimited (first 1,000/month free) |
| Approval Required | No (sandbox) | Yes (for production) |
| Message Cost | $0.0079 per message | Free (1,000/month), then $0.005 |
| Best For | Quick testing | Production apps |

## 💡 Recommendation

**Start with Twilio** - It's much easier and the $15 credit will last a long time for personal use. Once you're ready for production and need more volume, switch to WhatsApp Cloud API.

---

## 🔧 Troubleshooting

### "Not a valid WhatsApp user"
- Make sure you joined the Twilio sandbox by sending the join code
- Verify your phone number format includes country code

### "Authentication failed"
- Double-check your Account SID and Auth Token
- Make sure there are no extra spaces in your `.env` file

### "From number not found"
- Use the exact WhatsApp number from Twilio (usually `+1 415 523 8886`)
- Keep the `whatsapp:` prefix

### Messages not arriving
- Check your phone has an active internet connection
- Verify you completed the sandbox join process
- Check Twilio console logs for error details

---

## 🎓 Next Steps

Once your bot is working:
1. For production use, apply for Twilio WhatsApp approval
2. Get your own WhatsApp Business number
3. Or switch to WhatsApp Cloud API for unlimited free messages

For questions, check [Twilio's WhatsApp Docs](https://www.twilio.com/docs/whatsapp)
