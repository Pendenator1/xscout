"""
AI Helper for XScout - Uses Google Gemini (Free)
Features: Lead Scoring, Reply Generation, Keyword Expansion
"""
import google.generativeai as genai
import os
import json
from typing import Dict, List, Optional

class AIHelper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.enabled = bool(api_key and api_key != 'your_gemini_api_key_here')
        
        if self.enabled:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                print("[+] AI Features enabled with Google Gemini")
            except Exception as e:
                print(f"[X] Failed to initialize AI: {e}")
                self.enabled = False
        else:
            print("[i] AI Features disabled (no API key)")
    
    def score_lead(self, tweet_text: str, author_username: str) -> Dict:
        """
        Score a tweet as a potential lead (0-10)
        Returns: {score: int, reason: str, is_quality: bool}
        """
        if not self.enabled:
            return {"score": 5, "reason": "AI disabled", "is_quality": True}
        
        try:
            prompt = f"""Analyze this tweet to determine if it's a quality lead for a web developer/designer.

Tweet: "{tweet_text}"
Author: @{author_username}

CRITICAL: If the author is a developer/designer offering services, score 0! We want CLIENTS, not competitors.

Red flags (score 0-2):
- "I help", "I build", "I offer", "hire me", "I'm a developer"
- Portfolio links, service advertisements
- Other developers promoting themselves

Rate from 0-10 where:
- 10: CLIENT with clear intent, budget indicators, or urgency
- 7-9: CLIENT with project details or specific requirements
- 4-6: Possible CLIENT but vague or uncertain
- 1-3: Poor lead, might be spam or irrelevant
- 0: NOT A CLIENT (developer/competitor, spam, or irrelevant)

Respond ONLY in this JSON format:
{{"score": <number>, "reason": "<brief explanation>"}}"""

            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            
            score = int(result.get('score', 5))
            reason = result.get('reason', 'No reason provided')
            
            return {
                "score": score,
                "reason": reason,
                "is_quality": score >= int(os.getenv('AI_MIN_LEAD_SCORE', '7'))
            }
        except Exception as e:
            print(f"[X] AI scoring error: {e}")
            return {"score": 5, "reason": f"Error: {e}", "is_quality": True}
    
    def generate_reply(self, tweet_text: str, author_username: str, portfolio_url: str) -> Optional[str]:
        """
        Generate a personalized DM based on the client's business and needs
        """
        if not self.enabled:
            return None
        
        try:
            prompt = f"""You are a professional web developer reaching out to a potential client.

Their tweet: "{tweet_text}"
Their username: @{author_username}

Write a SHORT, friendly reply (max 200 characters) that:
1. References their specific need from the tweet
2. Mentions 1-2 key benefits a website would bring to their business type
3. Include: {portfolio_url}
4. End with "DM me if interested"

Keep it brief, friendly, and focused on THEIR benefit, not your skills.

Reply:"""

            response = self.model.generate_content(prompt)
            reply = response.text.strip()
            
            # Remove any quotes that might be added
            reply = reply.strip('"').strip("'")
            
            if len(reply) > 280:
                reply = reply[:277] + "..."
            
            return reply
        except Exception as e:
            print(f"[X] AI reply generation error: {e}")
            return None
    
    def generate_dm(self, tweet_text: str, author_username: str, portfolio_url: str) -> Optional[str]:
        """
        Generate a short, personalized DM for direct messaging
        """
        if not self.enabled:
            return None
        
        try:
            prompt = f"""You are a professional web developer reaching out to a potential client.

Their tweet: "{tweet_text}"
Their username: @{author_username}

Write a SHORT, personalized message (150-200 characters max):

1. Quick friendly greeting
2. Reference their specific need from tweet
3. Mention 2 KEY BENEFITS a website brings to their business type
4. Add: {portfolio_url}
5. Simple CTA: "Let me know if you'd like to discuss!"

CRITICAL: Keep it BRIEF, CASUAL, and FRIENDLY. Like texting a friend, not writing a business proposal.
Don't be pushy or salesy. Just helpful.

Message:"""

            response = self.model.generate_content(prompt)
            dm = response.text.strip()
            
            # Remove any quotes
            dm = dm.strip('"').strip("'")
            
            return dm
        except Exception as e:
            print(f"[X] AI DM generation error: {e}")
            return None
    
    def expand_keywords(self, base_keywords: List[str], count: int = 10) -> List[str]:
        """
        Generate additional relevant keywords based on existing ones
        """
        if not self.enabled:
            return []
        
        try:
            keywords_str = ', '.join(base_keywords[:5])
            prompt = f"""Given these search keywords for finding web development clients:
{keywords_str}

Generate {count} more creative, relevant variations that potential clients might use when looking for web developers. Focus on:
- Different phrasings
- Various project types (e-commerce, portfolio, business sites, etc.)
- Urgency indicators
- Budget-related phrases

Respond with ONLY a comma-separated list of keywords, no numbering or extra text."""

            response = self.model.generate_content(prompt)
            new_keywords = [k.strip() for k in response.text.strip().split(',')]
            
            return [k for k in new_keywords if k and len(k) < 100][:count]
        except Exception as e:
            print(f"[X] AI keyword expansion error: {e}")
            return []
