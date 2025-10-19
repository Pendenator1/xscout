"""
Test script to demonstrate AI urgency detection and DM generation
"""
import os
import sys
from dotenv import load_dotenv
from ai_helper import AIHelper

# Fix Windows CMD encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# Initialize AI
ai = AIHelper(os.getenv('GEMINI_API_KEY', ''))

if not ai.enabled:
    print("[X] AI not enabled. Check your GEMINI_API_KEY in .env")
    exit(1)

print("="*60)
print("XScout AI Features Test")
print("="*60)

# Test tweets with different urgency levels
test_tweets = [
    {
        "text": "URGENT! Need a website developer ASAP for my new restaurant. Budget ready, need to launch this week!",
        "username": "restaurant_owner"
    },
    {
        "text": "Looking for a web developer to build an e-commerce site. Project starts next month.",
        "username": "ecommerce_startup"
    },
    {
        "text": "Thinking about getting a website for my consulting business eventually. Any recommendations?",
        "username": "consultant_john"
    }
]

portfolio_url = os.getenv('PORTFOLIO_URL', 'https://your-portfolio.com')

for i, tweet in enumerate(test_tweets, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}: @{tweet['username']}")
    print(f"{'='*60}")
    print(f"Tweet: \"{tweet['text'][:100]}...\"")
    print()
    
    # Test lead scoring with urgency detection
    print("[*] AI analyzing lead quality and urgency...")
    lead_score = ai.score_lead(tweet['text'], tweet['username'])
    
    urgency_emoji = {"high": "🔥", "medium": "⚡", "low": "📌"}
    emoji = urgency_emoji.get(lead_score.get('urgency', 'medium').lower(), "⚡")
    
    print(f"[AI] Score: {lead_score['score']}/10 | Urgency: {emoji} {lead_score.get('urgency', 'medium').upper()}")
    print(f"[AI] {lead_score['reason']}")
    print(f"[AI] Quality Lead: {'✅ YES' if lead_score['is_quality'] else '❌ NO'}")
    
    # Test DM generation
    print()
    print("[*] Generating personalized DM...")
    dm = ai.generate_dm(tweet['text'], tweet['username'], portfolio_url)
    
    if dm:
        print(f"[+] AI Generated DM:")
        print(f"    \"{dm}\"")
    else:
        print("[X] Failed to generate DM")
    
    print()

print("="*60)
print("Test Complete!")
print("="*60)
print("\n[i] These features are now active in your bot:")
print("    - 🔥 HIGH urgency leads are flagged in WhatsApp")
print("    - ❤️ Tweets are auto-liked before replying")
print("    - 💬 DMs are personalized to each business type")
