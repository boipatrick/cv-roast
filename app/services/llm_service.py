import openai
## import anthropic
from typing import Dict, Any
from ..config import get_settings

settings = get_settings()

class LLMService:
    def __init__(self):
        self.settings = settings
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        ##if settings.ANTHROPIC_API_KEY:
            ##self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def generate_roast(self, cv_text: str, roast_level: str, focus_areas: list = None) -> Dict[str, Any]:
        """Generate a roast based on CV content"""
        prompt = self._build_roast_prompt(cv_text, roast_level, focus_areas)
        
        if self.settings.PREFERRED_LLM == "openai" and self.settings.OPENAI_API_KEY:
            return await self._roast_with_openai(prompt)
        elif self.settings.PREFERRED_LLM == "anthropic" and self.settings.ANTHROPIC_API_KEY:
            return await self._roast_with_anthropic(prompt)
        else:
            # Fallback roast if no API keys
            return await self._fallback_roast(cv_text, roast_level)
    
    def _build_roast_prompt(self, cv_text: str, roast_level: str, focus_areas: list = None) -> str:
        """Build the roasting prompt"""
        focus_text = ""
        if focus_areas:
            focus_text = f"Focus especially on: {', '.join(focus_areas)}."
        
        roast_styles = {
            "gentle": "Be constructive but point out obvious issues with humor.",
            "savage": "Be brutally honest and sarcastic. Don't hold back, but keep it professional.",
            "brutal": "Absolutely destroy this CV. Be merciless but creative in your criticism.",
            "constructive": "Provide harsh but helpful feedback with specific improvement suggestions."
        }
        
        style_instruction = roast_styles.get(roast_level, roast_styles["savage"])
        
        return f"""
You are a brutal CV critic. Your job is to roast this CV mercilessly while being insightful.

ROASTING STYLE: {style_instruction}
{focus_text}

CV CONTENT:
{cv_text}

Roast this CV focusing on:
- Poor formatting and presentation
- Weak or clichéd language
- Lack of quantifiable achievements
- Irrelevant information
- Grammar and spelling mistakes
- Skills that don't match the role
- Experience gaps or inconsistencies

Provide a roast score from 1-10 (10 being most brutal) and categorize your roast.

Format your response as JSON:
{{
    "roast": "Your brutal roast here...",
    "score": 8.5,
    "categories": ["formatting", "experience", "skills"],
    "model": "gpt-4"
}}
"""
    
    async def _roast_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Generate roast using OpenAI"""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=1000
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            result["model"] = "gpt-4"
            return result
        except Exception :
            return await self._fallback_roast("", "savage")
    
    async def _roast_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Generate roast using Anthropic Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            result = json.loads(response.content[0].text)
            result["model"] = "claude-3-sonnet"
            return result
        except Exception :
            return await self._fallback_roast("", "savage")
    
    async def _fallback_roast(self, cv_text: str, roast_level: str) -> Dict[str, Any]:
        """Fallback roast when APIs are unavailable"""
        roasts = {
            "gentle": "This CV has potential but needs some work. Consider adding more specific achievements and improving the formatting.",
            "savage": "This CV looks like it was written during a coffee break. Generic buzzwords, zero personality, and I've seen grocery lists with more structure.",
            "brutal": "This CV is a masterclass in mediocrity. It's so bland, it makes plain toast look exciting. Did you use a template from 2003?",
            "constructive": "This CV needs significant improvement in structure, content specificity, and professional presentation."
        }
        
        return {
            "roast": roasts.get(roast_level, roasts["savage"]),
            "score": 7.0,
            "categories": ["general", "formatting"],
            "model": "fallback"
        }