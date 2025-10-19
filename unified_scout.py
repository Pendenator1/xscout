"""
Unified Scout - Twitter Lead Finder
"""
from datetime import datetime
from xscout import XScout

class UnifiedScout:
    def __init__(self):
        self.twitter_scout = XScout()
    
    def run_all_platforms(self):
        """Run Twitter scout"""
        print("="*60)
        print("[*] XScout Started")
        print(f"[*] Timestamp: {datetime.now()}")
        print("="*60)
        
        # Run Twitter
        print("\n--- TWITTER SEARCH ---")
        try:
            self.twitter_scout.search_tweets()
        except Exception as e:
            print(f"[X] Twitter error: {e}")
        
        print("\n" + "="*60)
        print("[*] XScout Completed")
        print(f"[*] Timestamp: {datetime.now()}")
        print("="*60)

def main():
    scout = UnifiedScout()
    scout.run_all_platforms()

if __name__ == "__main__":
    main()
