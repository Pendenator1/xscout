"""
Facebook Scout - Find leads from Facebook groups and pages
Uses web scraping with Playwright
IMPORTANT: Must join relevant groups manually first
"""
import os
import asyncio
import requests
from dotenv import load_dotenv
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

load_dotenv(override=True)

class FacebookScout:
    def __init__(self):
        self.callmebot_phone = os.getenv('CALLMEBOT_PHONE')
        self.callmebot_apikey = os.getenv('CALLMEBOT_APIKEY')
        self.portfolio_url = os.getenv('PORTFOLIO_URL', '')
        self.keywords = os.getenv('KEYWORDS', '').split(',')
        
        # Facebook groups to monitor (you need to join these first)
        # Format: {'name': 'Group Name', 'id': 'group_id_or_url'}
        self.fb_groups = os.getenv('FACEBOOK_GROUPS', '').split(',')
        
        # Session file to persist login
        self.session_file = 'facebook_session.json'
        
        # Search queries
        self.search_queries = [
            'need a website',
            'looking for web developer',
            'hire developer',
            'need developer'
        ]
    
    def send_whatsapp_notification(self, post_info, platform="Facebook"):
        if not self.callmebot_phone or not self.callmebot_apikey:
            print("WhatsApp not configured. Skipping notification.")
            return
        
        message = f"[!] New {platform} Lead Found!\n\n"
        message += f"Author: {post_info['author']}\n"
        message += f"Post: {post_info['content'][:150]}...\n\n"
        message += f"View: {post_info['url']}"
        
        try:
            url = "https://api.callmebot.com/whatsapp.php"
            params = {
                'phone': self.callmebot_phone,
                'text': message,
                'apikey': self.callmebot_apikey
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                print(f"[+] WhatsApp notification sent for post by {post_info['author']}")
            else:
                print(f"[X] Failed to send WhatsApp notification: {response.text}")
        except Exception as e:
            print(f"[X] Error sending WhatsApp notification: {e}")
    
    async def check_if_logged_in(self, page):
        """Check if we're logged into Facebook"""
        try:
            # Check for common elements that appear when logged in
            await page.wait_for_selector('[aria-label="Account"]', timeout=3000)
            return True
        except:
            return False
    
    async def search_facebook_marketplace(self):
        """Search Facebook Marketplace for service requests"""
        print(f"\n[*] Searching Facebook Marketplace")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=False,  # Must be False to handle login
                    args=['--disable-blink-features=AutomationControlled']
                )
                
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                
                # Load saved session if exists
                try:
                    if os.path.exists(self.session_file):
                        import json
                        with open(self.session_file, 'r') as f:
                            cookies = json.load(f)
                            await context.add_cookies(cookies)
                        print("[+] Loaded saved Facebook session")
                except:
                    pass
                
                page = await context.new_page()
                
                # Go to Facebook
                await page.goto('https://www.facebook.com', timeout=30000)
                await asyncio.sleep(3)
                
                # Check if logged in
                is_logged_in = await self.check_if_logged_in(page)
                
                if not is_logged_in:
                    print("\n" + "="*60)
                    print("[!] NOT LOGGED IN TO FACEBOOK")
                    print("[!] Please log in manually in the browser window")
                    print("[!] After logging in, the bot will continue automatically")
                    print("[!] Your session will be saved for future runs")
                    print("="*60 + "\n")
                    
                    # Wait for user to log in (check every 5 seconds for 5 minutes)
                    for i in range(60):
                        await asyncio.sleep(5)
                        is_logged_in = await self.check_if_logged_in(page)
                        if is_logged_in:
                            print("[+] Successfully logged in!")
                            # Save session
                            cookies = await context.cookies()
                            import json
                            with open(self.session_file, 'w') as f:
                                json.dump(cookies, f)
                            print("[+] Session saved for future use")
                            break
                    
                    if not is_logged_in:
                        print("[X] Login timeout. Please run the script again.")
                        await browser.close()
                        return
                
                print("[+] Logged into Facebook")
                
                # Search for keywords
                for query in self.search_queries[:2]:  # Limit searches
                    print(f"\n[*] Searching for: {query}")
                    
                    search_url = f"https://www.facebook.com/search/posts/?q={query.replace(' ', '%20')}"
                    
                    try:
                        await page.goto(search_url, timeout=30000)
                        await asyncio.sleep(5)  # Wait for results to load
                        
                        # Scroll to load more posts
                        for _ in range(3):
                            await page.evaluate('window.scrollBy(0, 800)')
                            await asyncio.sleep(2)
                        
                        # Find posts
                        posts = await self.extract_facebook_posts(page)
                        
                        if posts:
                            print(f"[+] Found {len(posts)} posts")
                            for idx, post in enumerate(posts):
                                print(f"\n[>] Facebook Post #{idx + 1}:")
                                print(f"    Author: {post['author']}")
                                print(f"    Content: {post['content'][:100]}...")
                                print(f"    URL: {post['url']}")
                                
                                # Send notification
                                self.send_whatsapp_notification(post, "Facebook")
                        else:
                            print(f"[i] No posts found for: {query}")
                    
                    except Exception as e:
                        print(f"[X] Error searching Facebook: {e}")
                    
                    await asyncio.sleep(3)  # Delay between searches
                
                await browser.close()
                
        except Exception as e:
            print(f"[X] Error in Facebook search: {e}")
    
    async def extract_facebook_posts(self, page):
        """Extract posts from Facebook search results"""
        posts = []
        
        try:
            # Facebook uses dynamic selectors, these are common patterns
            post_selectors = [
                '[role="article"]',
                'div[data-pagelet*="FeedUnit"]',
                'div[class*="userContentWrapper"]'
            ]
            
            for selector in post_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    post_elements = await page.query_selector_all(selector)
                    
                    if post_elements:
                        print(f"[+] Found {len(post_elements)} post elements using: {selector}")
                        
                        for post_elem in post_elements[:5]:  # Limit to 5 posts
                            try:
                                post_info = {
                                    'author': 'Unknown',
                                    'content': '',
                                    'url': ''
                                }
                                
                                # Extract author name
                                try:
                                    author_selectors = [
                                        'a[role="link"] strong',
                                        'h4 a',
                                        'a[class*="actor"]'
                                    ]
                                    
                                    for auth_sel in author_selectors:
                                        author_elem = await post_elem.query_selector(auth_sel)
                                        if author_elem:
                                            post_info['author'] = (await author_elem.inner_text()).strip()
                                            break
                                except:
                                    pass
                                
                                # Extract content
                                try:
                                    content_selectors = [
                                        'div[data-ad-preview="message"]',
                                        'div[data-ad-comet-preview="message"]',
                                        'div[dir="auto"]'
                                    ]
                                    
                                    for cont_sel in content_selectors:
                                        content_elem = await post_elem.query_selector(cont_sel)
                                        if content_elem:
                                            text = await content_elem.inner_text()
                                            if text and len(text) > 20:  # Meaningful content
                                                post_info['content'] = text.strip()
                                                break
                                except:
                                    pass
                                
                                # Extract URL
                                try:
                                    link_elem = await post_elem.query_selector('a[href*="/posts/"], a[href*="/permalink/"]')
                                    if link_elem:
                                        href = await link_elem.get_attribute('href')
                                        if href:
                                            if href.startswith('http'):
                                                post_info['url'] = href.split('?')[0]
                                            else:
                                                post_info['url'] = f"https://www.facebook.com{href.split('?')[0]}"
                                except:
                                    post_info['url'] = 'https://www.facebook.com'
                                
                                # Only add if we have meaningful content
                                if post_info['content'] and len(post_info['content']) > 20:
                                    # Check if content matches any keywords
                                    content_lower = post_info['content'].lower()
                                    if any(kw.strip().lower() in content_lower for kw in self.keywords):
                                        posts.append(post_info)
                            
                            except Exception as e:
                                continue
                        
                        break  # Found posts, stop trying other selectors
                
                except PlaywrightTimeout:
                    continue
        
        except Exception as e:
            print(f"[X] Error extracting posts: {e}")
        
        return posts
    
    async def run_search(self):
        """Run Facebook search"""
        print(f"\n[*] Facebook Scout Started at {datetime.now()}")
        await self.search_facebook_marketplace()
        print(f"\n[*] Facebook Scout Completed at {datetime.now()}")

async def main():
    scout = FacebookScout()
    await scout.run_search()

if __name__ == "__main__":
    asyncio.run(main())
