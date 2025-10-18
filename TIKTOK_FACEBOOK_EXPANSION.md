# Expanding to TikTok and Facebook

This guide explains how to add TikTok and Facebook lead finding to XScout.

## TikTok Integration

### Option 1: TikTok Research API (Official - Requires Application)

**Requirements:**
- Apply for TikTok Research API access at: https://developers.tiktok.com/
- Academic or research institution affiliation may be required
- Approval process can take weeks

**Features:**
- Search videos and comments
- Filter by keywords
- Official and reliable

### Option 2: Unofficial TikTok API (TikTokApi Python Library)

**Pros:**
- No API key required
- Can search videos by keywords
- Can read comments

**Cons:**
- Against TikTok ToS
- May break if TikTok changes their website
- Risk of IP ban

**Installation:**
```bash
pip install TikTokApi playwright
playwright install
```

**Example Code:**
```python
from TikTokApi import TikTokApi
import asyncio

async def search_tiktok_leads():
    async with TikTokApi() as api:
        # Search for videos with keywords
        videos = await api.search.videos('need a website', count=10)
        
        for video in videos:
            print(f"Video: {video.desc}")
            print(f"Author: @{video.author.username}")
            print(f"URL: https://tiktok.com/@{video.author.username}/video/{video.id}")
            
            # Get comments
            comments = await video.comments(count=20)
            for comment in comments:
                if 'need' in comment.text.lower() or 'looking for' in comment.text.lower():
                    print(f"  Comment by @{comment.user.username}: {comment.text}")

asyncio.run(search_tiktok_leads())
```

### Option 3: Web Scraping (Most Reliable Free Option)

Use Playwright or Selenium to scrape TikTok search results:

```python
from playwright.async_api import async_playwright

async def scrape_tiktok():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Search for keywords
        await page.goto('https://www.tiktok.com/search?q=need%20a%20website')
        await page.wait_for_selector('[data-e2e="search-video-item"]')
        
        # Extract video information
        videos = await page.query_selector_all('[data-e2e="search-video-item"]')
        
        for video in videos:
            # Extract details and send notifications
            pass
        
        await browser.close()
```

## Facebook Integration

### Option 1: Facebook Graph API (Official)

**Requirements:**
- Facebook Developer account: https://developers.facebook.com/
- Create an app
- Get access token
- Limited to public posts and pages you manage

**Limitations:**
- Cannot search all public posts by keyword (this feature was removed)
- Can only search within:
  - Pages you manage
  - Public groups you're a member of
  - Your own timeline

**Installation:**
```bash
pip install facebook-sdk
```

**Example Code:**
```python
import facebook

graph = facebook.GraphAPI(access_token='YOUR_ACCESS_TOKEN')

# Search within a specific page
posts = graph.get_connections('PAGE_ID', 'feed', q='need a website')

for post in posts['data']:
    print(f"Post: {post.get('message', '')}")
    print(f"Link: https://facebook.com/{post['id']}")
```

### Option 2: Facebook Groups (Manual Search)

Since Facebook removed keyword search for public posts, the best approach is:

1. **Join relevant Facebook groups:**
   - Web development marketplace groups
   - Freelancer groups
   - Business groups

2. **Use Facebook's group search:**
   - Search within groups for keywords like "need website", "looking for developer"

3. **Browser Extension Approach:**
   - Use Puppeteer/Playwright to automate searches within groups you're a member of
   - Extract posts matching your keywords

**Example with Playwright:**
```python
from playwright.sync_api import sync_playwright

def search_facebook_groups():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # Load saved session (you need to login once manually)
        page = context.new_page()
        page.goto('https://www.facebook.com/groups/YOUR_GROUP_ID')
        
        # Search within the group
        page.fill('input[placeholder="Search this group"]', 'need a website')
        page.press('input[placeholder="Search this group"]', 'Enter')
        page.wait_for_load_state('networkidle')
        
        # Extract posts
        # ...
        
        browser.close()
```

## Recommended Approach

### For TikTok:
1. Start with **web scraping using Playwright**
2. Monitor TikTok search pages for your keywords
3. Extract video descriptions and comments
4. Send WhatsApp notifications for matches

### For Facebook:
1. **Join relevant groups** manually
2. Use **Facebook's native search** within groups
3. Optionally: Use **browser automation** to monitor group posts
4. **Important:** Respect Facebook's ToS to avoid account bans

## Complete Multi-Platform Bot Structure

```
xscout/
├── xscout.py              # Twitter bot (current)
├── tiktok_scout.py        # TikTok lead finder
├── facebook_scout.py      # Facebook lead finder
├── unified_scout.py       # Runs all bots
└── requirements.txt       # Updated with new dependencies
```

## Next Steps

1. **Choose your approach** for each platform
2. **Test locally** before deploying
3. **Be aware of rate limits** and ToS
4. **Consider using proxies** if scraping at scale
5. **Monitor for changes** in platform structures

## Legal & Ethical Considerations

⚠️ **Important:**
- Respect each platform's Terms of Service
- Don't spam or send unsolicited messages
- Be transparent in your outreach
- Consider GDPR/data privacy laws
- Use automation responsibly

## Need Help?

If you want to implement TikTok or Facebook lead finding:
1. Choose your preferred approach
2. Let me know which platform to start with
3. I'll create the complete implementation
