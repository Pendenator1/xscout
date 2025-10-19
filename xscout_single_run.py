"""
XScout Single Run - For GitHub Actions
Runs once per execution (GitHub Actions will schedule it)
"""
import tweepy
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from ai_helper import AIHelper

load_dotenv(override=True)

class XScoutSingleRun:
    def __init__(self):
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        
        self.callmebot_phone = os.getenv('CALLMEBOT_PHONE')
        self.callmebot_apikey = os.getenv('CALLMEBOT_APIKEY')
        
        self.auto_reply = os.getenv('AUTO_REPLY', 'true').lower() == 'true'
        self.portfolio_url = os.getenv('PORTFOLIO_URL', '')
        
        self.keywords = os.getenv('KEYWORDS', '').split(',')
        
        self.ai_enabled = os.getenv('ENABLE_AI_FEATURES', 'false').lower() == 'true'
        self.ai_helper = AIHelper(os.getenv('GEMINI_API_KEY', '')) if self.ai_enabled else None
        self.min_lead_score = int(os.getenv('AI_MIN_LEAD_SCORE', '7'))
        
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret,
            wait_on_rate_limit=True
        )
    
    def send_whatsapp_notification(self, tweet_text, tweet_url, author):
        if not self.callmebot_phone or not self.callmebot_apikey:
            print("WhatsApp not configured. Skipping notification.")
            return
        
        message = f"[!] New Lead Found!\n\n"
        message += f"Author: @{author}\n"
        message += f"Tweet: {tweet_text[:200]}...\n\n"
        message += f"View: {tweet_url}"
        
        try:
            url = "https://api.callmebot.com/whatsapp.php"
            params = {
                'phone': self.callmebot_phone,
                'text': message,
                'apikey': self.callmebot_apikey
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                print(f"[+] WhatsApp notification sent for tweet by @{author}")
            else:
                print(f"[X] Failed to send WhatsApp notification: {response.text}")
        except Exception as e:
            print(f"[X] Error sending WhatsApp notification: {e}")
    
    def send_auto_reply(self, tweet_id, username, tweet_text=''):
        print(f"[*] send_auto_reply called for @{username}")
        print(f"    AUTO_REPLY={self.auto_reply}")
        print(f"    PORTFOLIO_URL={self.portfolio_url}")
        print(f"    AI_ENABLED={self.ai_enabled}")
        
        if not self.auto_reply:
            print(f"[i] Auto-reply disabled. Skipping reply to @{username}")
            return
        
        if not self.portfolio_url:
            print(f"[!] Portfolio URL not configured. Skipping reply to @{username}")
            return
        
        reply_text = None
        if self.ai_enabled and self.ai_helper and self.ai_helper.enabled and tweet_text:
            print(f"[*] Generating AI reply for @{username}...")
            try:
                reply_text = self.ai_helper.generate_reply(tweet_text, username, self.portfolio_url)
                if reply_text:
                    print(f"[+] AI generated personalized reply: {reply_text[:50]}...")
                else:
                    print(f"[!] AI returned empty reply")
            except Exception as e:
                print(f"[X] AI reply generation failed: {e}")
        
        if not reply_text:
            reply_text = f"Hi! I'm a web developer specializing in frontend and fullstack development. Check out my portfolio: {self.portfolio_url}\n\nI'd love to discuss your project!"
            print(f"[*] Using template reply")
        
        print(f"[*] Attempting to post reply to tweet {tweet_id}...")
        try:
            response = self.client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet_id
            )
            print(f"[+] ✅ Auto-replied to @{username} - Tweet ID: {response.data['id']}")
        except tweepy.errors.Unauthorized as e:
            print(f"[X] ❌ Error sending auto-reply: 401 Unauthorized")
            print(f"    This typically means:")
            print(f"    1. Your Twitter API credentials are invalid or expired")
            print(f"    2. Your app lacks 'Read and Write' permissions")
            print(f"    3. Access tokens need to be regenerated with proper permissions")
            print(f"    Details: {e}")
        except tweepy.errors.Forbidden as e:
            print(f"[X] Error sending auto-reply: 403 Forbidden - {e}")
            print(f"    Your app may not have permission to post tweets")
        except tweepy.errors.TweepyException as e:
            print(f"[X] Twitter API Error sending auto-reply: {e}")
        except Exception as e:
            print(f"[X] Unexpected error sending auto-reply: {e}")
    
    def search_tweets(self):
        print(f"[*] Searching for {len(self.keywords)} keywords:")
        for i, keyword in enumerate(self.keywords, 1):
            print(f"    {i}. '{keyword.strip()}'")
        
        query = ' OR '.join([f'"{keyword.strip()}"' for keyword in self.keywords])
        query += ' -is:retweet lang:en'
        query += ' -"I help" -"I build" -"I offer" -"hire me" -"portfolio" -"check out my"'
        print(f"[*] Search query: {query[:200]}...")
        
        try:
            # Search tweets from the last 15 minutes
            end_time = datetime.now()
            start_time = end_time - timedelta(minutes=15)
            
            print(f"[*] Querying Twitter API...")
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=10,
                start_time=start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                tweet_fields=['created_at', 'author_id', 'public_metrics'],
                expansions=['author_id'],
                user_fields=['username', 'name']
            )
            print(f"[+] Twitter API query completed")
            
            if not tweets.data:
                print("[i] No new tweets found in the last 15 minutes.")
                return
            
            users = {user.id: user for user in tweets.includes.get('users', [])}
            
            for tweet in tweets.data:
                author = users.get(tweet.author_id)
                username = author.username if author else 'unknown'
                tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"
                
                print(f"\n[>] Found tweet by @{username}:")
                print(f"    {tweet.text[:100]}...")
                print(f"    {tweet_url}")
                
                if self.ai_enabled and self.ai_helper and self.ai_helper.enabled:
                    print(f"[*] AI analyzing lead quality...")
                    lead_score = self.ai_helper.score_lead(tweet.text, username)
                    print(f"[AI] Score: {lead_score['score']}/10 - {lead_score['reason']}")
                    
                    if not lead_score['is_quality']:
                        print(f"[i] Skipping low-quality lead (score: {lead_score['score']} < {self.min_lead_score})")
                        continue
                    else:
                        print(f"[+] Quality lead detected!")
                
                self.send_whatsapp_notification(tweet.text, tweet_url, username)
                self.send_auto_reply(tweet.id, username, tweet.text)
        
        except tweepy.errors.TweepyException as e:
            print(f"[X] Twitter API Error: {e}")
        except Exception as e:
            print(f"[X] Error: {e}")

if __name__ == "__main__":
    print(f"[*] XScout Single Run Started at {datetime.now()}")
    bot = XScoutSingleRun()
    bot.search_tweets()
    print(f"[*] XScout Single Run Completed at {datetime.now()}")
