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
        Generate a personalized reply based on the tweet content
        """
        if not self.enabled:
            return None
        
        try:
            prompt = f"""You are a professional web developer responding to a potential client.

Their tweet: "{tweet_text}"
Their username: @{author_username}
Your portfolio: {portfolio_url}

Write a short, personalized reply (max 280 characters) that:
1. References something specific from their tweet
2. Briefly mentions your relevant skills
3. Includes the portfolio link naturally
4. Sounds professional but friendly
5. Invites them to discuss further

Reply:"""

            response = self.model.generate_content(prompt)
            reply = response.text.strip()
            
            if len(reply) > 280:
                reply = reply[:277] + "..."
            
            return reply
        except Exception as e:
            print(f"[X] AI reply generation error: {e}")
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
