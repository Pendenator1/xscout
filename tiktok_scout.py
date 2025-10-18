"""
TikTok Scout - Find leads from TikTok videos and comments
Uses web scraping with Playwright
"""
import os
import asyncio
import requests
from dotenv import load_dotenv
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

load_dotenv(override=True)

class TikTokScout:
    def __init__(self):
        self.callmebot_phone = os.getenv('CALLMEBOT_PHONE')
        self.callmebot_apikey = os.getenv('CALLMEBOT_APIKEY')
        self.auto_comment = os.getenv('AUTO_REPLY', 'true').lower() == 'true'
        self.portfolio_url = os.getenv('PORTFOLIO_URL', '')
        self.keywords = os.getenv('KEYWORDS', '').split(',')
        
        # TikTok search queries
        self.search_queries = [
            'need a website',
            'looking for web developer',
            'hire web developer',
            'need web designer'
        ]
    
    def send_whatsapp_notification(self, video_info, platform="TikTok"):
        if not self.callmebot_phone or not self.callmebot_apikey:
            print("WhatsApp not configured. Skipping notification.")
            return
        
        message = f"[!] New {platform} Lead Found!\n\n"
        message += f"Author: @{video_info['author']}\n"
        message += f"Description: {video_info['description'][:150]}...\n"
        message += f"Likes: {video_info.get('likes', 'N/A')}\n"
        message += f"Views: {video_info.get('views', 'N/A')}\n\n"
        message += f"View: {video_info['url']}"
        
        try:
            url = "https://api.callmebot.com/whatsapp.php"
            params = {
                'phone': self.callmebot_phone,
                'text': message,
                'apikey': self.callmebot_apikey
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                print(f"[+] WhatsApp notification sent for video by @{video_info['author']}")
            else:
                print(f"[X] Failed to send WhatsApp notification: {response.text}")
        except Exception as e:
            print(f"[X] Error sending WhatsApp notification: {e}")
    
    async def search_tiktok_videos(self, query):
        """Search TikTok for videos matching keywords"""
        print(f"[*] Searching TikTok for: {query}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = await context.new_page()
                
                # Build search URL
                search_url = f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}"
                print(f"[*] Navigating to: {search_url}")
                
                try:
                    await page.goto(search_url, timeout=30000)
                    await asyncio.sleep(3)  # Wait for content to load
                    
                    # Try to find video containers
                    # TikTok uses dynamic selectors, these are common patterns
                    video_selectors = [
                        '[data-e2e="search-video-item"]',
                        'div[class*="video-feed-item"]',
                        'div[data-e2e="search-card-item"]'
                    ]
                    
                    videos_found = []
                    
                    for selector in video_selectors:
                        try:
                            await page.wait_for_selector(selector, timeout=5000)
                            videos = await page.query_selector_all(selector)
                            
                            if videos:
                                print(f"[+] Found {len(videos)} videos using selector: {selector}")
                                
                                for idx, video in enumerate(videos[:5]):  # Limit to first 5
                                    try:
                                        # Extract video information
                                        video_info = await self.extract_video_info(video, page)
                                        
                                        if video_info:
                                            videos_found.append(video_info)
                                            print(f"\n[>] TikTok Video #{idx + 1}:")
                                            print(f"    Author: @{video_info['author']}")
                                            print(f"    Description: {video_info['description'][:100]}...")
                                            print(f"    URL: {video_info['url']}")
                                            
                                            # Send notification
                                            self.send_whatsapp_notification(video_info, "TikTok")
                                    
                                    except Exception as e:
                                        print(f"[!] Error extracting video info: {e}")
                                        continue
                                
                                break  # Found videos, no need to try other selectors
                        
                        except PlaywrightTimeout:
                            continue
                    
                    if not videos_found:
                        print(f"[i] No videos found for query: {query}")
                
                except PlaywrightTimeout:
                    print(f"[!] Timeout loading TikTok search page")
                except Exception as e:
                    print(f"[X] Error during search: {e}")
                
                finally:
                    await browser.close()
                    
        except Exception as e:
            print(f"[X] Error in TikTok search: {e}")
    
    async def extract_video_info(self, video_element, page):
        """Extract information from a video element"""
        try:
            video_info = {
                'author': 'Unknown',
                'description': '',
                'url': '',
                'likes': 'N/A',
                'views': 'N/A'
            }
            
            # Try to extract author
            author_selectors = [
                '[data-e2e="search-card-user-unique-id"]',
                'a[class*="author"]',
                '[class*="username"]'
            ]
            
            for selector in author_selectors:
                try:
                    author_elem = await video_element.query_selector(selector)
                    if author_elem:
                        video_info['author'] = (await author_elem.inner_text()).strip('@').strip()
                        break
                except:
                    continue
            
            # Try to extract description
            desc_selectors = [
                '[data-e2e="search-card-desc"]',
                'div[class*="video-desc"]',
                '[class*="description"]'
            ]
            
            for selector in desc_selectors:
                try:
                    desc_elem = await video_element.query_selector(selector)
                    if desc_elem:
                        video_info['description'] = (await desc_elem.inner_text()).strip()
                        break
                except:
                    continue
            
            # Try to extract video URL
            try:
                link_elem = await video_element.query_selector('a')
                if link_elem:
                    href = await link_elem.get_attribute('href')
                    if href:
                        if href.startswith('http'):
                            video_info['url'] = href
                        else:
                            video_info['url'] = f"https://www.tiktok.com{href}"
            except:
                pass
            
            # Only return if we have at least author or description
            if video_info['author'] != 'Unknown' or video_info['description']:
                return video_info
            
            return None
            
        except Exception as e:
            print(f"[!] Error extracting video info: {e}")
            return None
    
    async def run_search(self):
        """Run search for all queries"""
        print(f"\n[*] TikTok Scout Started at {datetime.now()}")
        print(f"[*] Searching {len(self.search_queries)} queries")
        
        for query in self.search_queries[:2]:  # Limit to first 2 queries to avoid rate limits
            await self.search_tiktok_videos(query)
            await asyncio.sleep(2)  # Delay between searches
        
        print(f"\n[*] TikTok Scout Completed at {datetime.now()}")

async def main():
    scout = TikTokScout()
    await scout.run_search()

if __name__ == "__main__":
    asyncio.run(main())
