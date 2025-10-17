import tweepy
import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class XScout:
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
        
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret,
            wait_on_rate_limit=True
        )
        
        self.seen_tweets = set()
        
        self.validate_credentials()
    
    def validate_credentials(self):
        print("\n[*] Validating API credentials...")
        
        missing_creds = []
        if not self.bearer_token:
            missing_creds.append("TWITTER_BEARER_TOKEN")
        if not self.api_key:
            missing_creds.append("TWITTER_API_KEY")
        if not self.api_secret:
            missing_creds.append("TWITTER_API_SECRET")
        if not self.access_token:
            missing_creds.append("TWITTER_ACCESS_TOKEN")
        if not self.access_secret:
            missing_creds.append("TWITTER_ACCESS_SECRET")
        
        if missing_creds:
            print(f"[!] Warning: Missing credentials: {', '.join(missing_creds)}")
            print("    The bot may not function correctly without these.")
        else:
            print("[+] All Twitter credentials are present")
        
        if self.auto_reply:
            print("[+] Auto-reply is ENABLED")
            if not self.portfolio_url:
                print("[!] Warning: AUTO_REPLY is enabled but PORTFOLIO_URL is not set")
            else:
                print(f"    Portfolio URL: {self.portfolio_url}")
            
            try:
                me = self.client.get_me()
                print(f"[+] Authenticated as: @{me.data.username}")
                print("    Note: Auto-reply requires 'Read and Write' permissions in your Twitter app settings")
            except tweepy.errors.Unauthorized:
                print("[X] Authentication failed: 401 Unauthorized")
                print("    Your credentials are invalid or your app lacks proper permissions")
                print("    To fix this:")
                print("    1. Go to https://developer.twitter.com/en/portal/dashboard")
                print("    2. Select your app > Settings > User authentication settings")
                print("    3. Ensure OAuth 1.0a is enabled with 'Read and Write' permissions")
                print("    4. Regenerate your Access Token & Secret")
                print("    5. Update your .env file with the new tokens")
            except Exception as e:
                print(f"[!] Could not verify authentication: {e}")
        else:
            print("[i] Auto-reply is DISABLED")
        
        if self.callmebot_phone and self.callmebot_apikey:
            print(f"[+] WhatsApp notifications enabled for {self.callmebot_phone}")
        else:
            print("[i] WhatsApp notifications not configured")
        
        print()
    
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
    
    def send_auto_reply(self, tweet_id, username):
        if not self.auto_reply:
            print(f"[i] Auto-reply disabled. Skipping reply to @{username}")
            return
        
        if not self.portfolio_url:
            print(f"[!] Portfolio URL not configured. Skipping reply to @{username}")
            return
        
        reply_text = f"Hi! I'm a web developer specializing in frontend and fullstack development. Check out my portfolio: {self.portfolio_url}\n\nI'd love to discuss your project!"
        
        try:
            self.client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet_id
            )
            print(f"[+] Auto-replied to @{username}")
        except tweepy.errors.Unauthorized as e:
            print(f"[X] Error sending auto-reply: 401 Unauthorized")
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
        print(f"[*] Searching for keywords: {', '.join(self.keywords)}")
        
        query = ' OR '.join([f'"{keyword.strip()}"' for keyword in self.keywords])
        query += ' -is:retweet lang:en'
        
        try:
            from datetime import timedelta
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=10,
                start_time=start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                tweet_fields=['created_at', 'author_id', 'public_metrics'],
                expansions=['author_id'],
                user_fields=['username', 'name']
            )
            
            if not tweets.data:
                print("No new tweets found.")
                return
            
            users = {user.id: user for user in tweets.includes.get('users', [])}
            
            for tweet in tweets.data:
                if tweet.id in self.seen_tweets:
                    continue
                
                self.seen_tweets.add(tweet.id)
                
                author = users.get(tweet.author_id)
                username = author.username if author else 'unknown'
                tweet_url = f"https://twitter.com/{username}/status/{tweet.id}"
                
                print(f"\n[>] Found tweet by @{username}:")
                print(f"   {tweet.text[:100]}...")
                print(f"   {tweet_url}")
                
                self.send_whatsapp_notification(tweet.text, tweet_url, username)
                self.send_auto_reply(tweet.id, username)
        
        except tweepy.errors.TweepyException as e:
            print(f"[X] Twitter API Error: {e}")
        except Exception as e:
            print(f"[X] Error: {e}")
    
    def run(self, interval=60):
        print("[*] XScout Bot Started!")
        print(f"[*] Checking every {interval} seconds...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[{timestamp}] Running search...")
                self.search_tweets()
                print(f"[-] Sleeping for {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n[*] XScout Bot stopped.")

if __name__ == "__main__":
    bot = XScout()
    bot.run(interval=300)
