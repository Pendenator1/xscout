"""
Unified Scout - Run all platforms (Twitter, TikTok, Facebook)
"""
import asyncio
from datetime import datetime
from xscout import XScout
from tiktok_scout import TikTokScout
from facebook_scout import FacebookScout

class UnifiedScout:
    def __init__(self):
        self.twitter_scout = XScout()
        self.tiktok_scout = TikTokScout()
        self.facebook_scout = FacebookScout()
    
    async def run_all_platforms(self):
        """Run all platform scouts"""
        print("="*60)
        print("[*] Unified Scout Started")
        print(f"[*] Timestamp: {datetime.now()}")
        print("="*60)
        
        # Run Twitter (synchronous)
        print("\n--- TWITTER SEARCH ---")
        try:
            self.twitter_scout.search_tweets()
        except Exception as e:
            print(f"[X] Twitter error: {e}")
        
        # Run TikTok (async)
        print("\n--- TIKTOK SEARCH ---")
        try:
            await self.tiktok_scout.run_search()
        except Exception as e:
            print(f"[X] TikTok error: {e}")
        
        # Run Facebook (async)
        print("\n--- FACEBOOK SEARCH ---")
        try:
            await self.facebook_scout.run_search()
        except Exception as e:
            print(f"[X] Facebook error: {e}")
        
        print("\n" + "="*60)
        print("[*] Unified Scout Completed")
        print(f"[*] Timestamp: {datetime.now()}")
        print("="*60)

async def main():
    scout = UnifiedScout()
    await scout.run_all_platforms()

if __name__ == "__main__":
    asyncio.run(main())
