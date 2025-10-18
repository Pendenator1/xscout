"""
Facebook Scout - Cloud Version for GitHub Actions
Handles automated login using credentials from environment variables
"""
import os
import asyncio
import requests
from dotenv import load_dotenv
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

load_dotenv(override=True)

class FacebookScoutCloud:
    def __init__(self):
        self.callmebot_phone = os.getenv('CALLMEBOT_PHONE')
        self.callmebot_apikey = os.getenv('CALLMEBOT_APIKEY')
        self.portfolio_url = os.getenv('PORTFOLIO_URL', '')
        self.keywords = os.getenv('KEYWORDS', '').split(',')
        
        # Facebook credentials for automated login
        self.fb_email = os.getenv('FACEBOOK_EMAIL')
        self.fb_password = os.getenv('FACEBOOK_PASSWORD')
        
        self.session_file = 'facebook_session.json'
        
        # Use all keywords from .env as search queries
        self.search_queries = [kw.strip() for kw in self.keywords if kw.strip()]
        
        print(f"[*] Loaded {len(self.search_queries)} search queries from keywords")
    
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
    
    async def login_to_facebook(self, page):
        """Automated Facebook login"""
        print("[*] Attempting Facebook login...")
        
        if not self.fb_email or not self.fb_password:
            print("[X] Facebook credentials not found in environment variables")
            print("[!] Set FACEBOOK_EMAIL and FACEBOOK_PASSWORD secrets in GitHub")
            return False
        
        try:
            # Go to Facebook
            await page.goto('https://www.facebook.com', timeout=30000)
            await asyncio.sleep(2)
            
            # Fill email
            try:
                await page.fill('input[name="email"]', self.fb_email, timeout=5000)
                print("[+] Email filled")
            except:
                print("[X] Could not find email field")
                return False
            
            # Fill password
            try:
                await page.fill('input[name="pass"]', self.fb_password, timeout=5000)
                print("[+] Password filled")
            except:
                print("[X] Could not find password field")
                return False
            
            # Click login button
            try:
                await page.click('button[name="login"]', timeout=5000)
                print("[+] Login button clicked")
            except:
                print("[X] Could not find login button")
                return False
            
            # Wait for navigation
            await asyncio.sleep(5)
            
            # Check if login was successful
            try:
                await page.wait_for_selector('[aria-label="Account"]', timeout=10000)
                print("[+] Successfully logged in!")
                
                # Save session
                cookies = await page.context.cookies()
                import json
                with open(self.session_file, 'w') as f:
                    json.dump(cookies, f)
                print("[+] Session saved")
                
                return True
            except:
                print("[X] Login may have failed or 2FA required")
                return False
        
        except Exception as e:
            print(f"[X] Error during login: {e}")
            return False
    
    async def search_facebook_marketplace(self):
        """Search Facebook with automated login"""
        print(f"\n[*] Facebook Scout Cloud Started")
        
        # Check if running in GitHub Actions
        is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,  # Always headless in cloud
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-setuid-sandbox'
                    ]
                )
                
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                
                # Try to load saved session
                session_loaded = False
                try:
                    if os.path.exists(self.session_file):
                        import json
                        with open(self.session_file, 'r') as f:
                            cookies = json.load(f)
                            await context.add_cookies(cookies)
                        print("[+] Loaded saved Facebook session")
                        session_loaded = True
                except Exception as e:
                    print(f"[!] Could not load session: {e}")
                
                page = await context.new_page()
                
                # Check if we're logged in
                await page.goto('https://www.facebook.com', timeout=30000)
                await asyncio.sleep(3)
                
                is_logged_in = False
                try:
                    await page.wait_for_selector('[aria-label="Account"]', timeout=5000)
                    is_logged_in = True
                    print("[+] Already logged in (session valid)")
                except:
                    print("[!] Not logged in, attempting automated login...")
                    is_logged_in = await self.login_to_facebook(page)
                
                if not is_logged_in:
                    print("[X] Could not log in to Facebook")
                    print("[!] This is common in cloud environments due to:")
                    print("    - 2FA requirements")
                    print("    - IP/device verification")
                    print("    - Captchas")
                    print("\n[!] Recommendation: Run Facebook scout locally or use Facebook Graph API")
                    await browser.close()
                    return
                
                # Search for all keywords
                for idx, query in enumerate(self.search_queries, 1):
                    print(f"\n[*] Query {idx}/{len(self.search_queries)}: Searching for: {query}")
                    
                    search_url = f"https://www.facebook.com/search/posts/?q={query.replace(' ', '%20')}"
                    
                    try:
                        await page.goto(search_url, timeout=30000)
                        await asyncio.sleep(5)
                        
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
                                
                                self.send_whatsapp_notification(post, "Facebook")
                        else:
                            print(f"[i] No posts found for: {query}")
                    
                    except Exception as e:
                        print(f"[X] Error searching Facebook: {e}")
                    
                    # Delay between searches (longer delays to avoid rate limits)
                    if idx < len(self.search_queries):
                        delay = 4 if idx < 5 else 6
                        print(f"[*] Waiting {delay}s before next search...")
                        await asyncio.sleep(delay)
                
                await browser.close()
                
        except Exception as e:
            print(f"[X] Error in Facebook search: {e}")
    
    async def extract_facebook_posts(self, page):
        """Extract posts from Facebook search results"""
        posts = []
        
        try:
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
                        print(f"[+] Found {len(post_elements)} post elements")
                        
                        for post_elem in post_elements[:5]:
                            try:
                                post_info = {
                                    'author': 'Unknown',
                                    'content': '',
                                    'url': ''
                                }
                                
                                # Extract author
                                author_selectors = [
                                    'a[role="link"] strong',
                                    'h4 a',
                                    'a[class*="actor"]'
                                ]
                                
                                for auth_sel in author_selectors:
                                    try:
                                        author_elem = await post_elem.query_selector(auth_sel)
                                        if author_elem:
                                            post_info['author'] = (await author_elem.inner_text()).strip()
                                            break
                                    except:
                                        continue
                                
                                # Extract content
                                content_selectors = [
                                    'div[data-ad-preview="message"]',
                                    'div[data-ad-comet-preview="message"]',
                                    'div[dir="auto"]'
                                ]
                                
                                for cont_sel in content_selectors:
                                    try:
                                        content_elem = await post_elem.query_selector(cont_sel)
                                        if content_elem:
                                            text = await content_elem.inner_text()
                                            if text and len(text) > 20:
                                                post_info['content'] = text.strip()
                                                break
                                    except:
                                        continue
                                
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
                                    content_lower = post_info['content'].lower()
                                    if any(kw.strip().lower() in content_lower for kw in self.keywords):
                                        posts.append(post_info)
                            
                            except:
                                continue
                        
                        break
                
                except PlaywrightTimeout:
                    continue
        
        except Exception as e:
            print(f"[X] Error extracting posts: {e}")
        
        return posts
    
    async def run_search(self):
        """Run Facebook search"""
        print(f"\n[*] Facebook Scout Cloud Started at {datetime.now()}")
        await self.search_facebook_marketplace()
        print(f"\n[*] Facebook Scout Cloud Completed at {datetime.now()}")

async def main():
    scout = FacebookScoutCloud()
    await scout.run_search()

if __name__ == "__main__":
    asyncio.run(main())
