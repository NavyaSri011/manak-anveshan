# pyrefly: ignore [missing-import]
import os
# pyrefly: ignore [missing-import]
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

class LLMService:

    @staticmethod
    def is_configured() -> bool:
        return bool(settings.LLM_API_KEY and settings.LLM_API_KEY.strip() != "")

    @staticmethod
    async def generate_explanation(prompt: str) -> str:
        if not LLMService.is_configured():
            return "Rule-based deterministic engine output (LLM Provider set to DEMO mode)."
        
        try:
            if settings.LLM_PROVIDER == "openai":
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"},
                        json={
                            "model": settings.LLM_MODEL,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.2
                        },
                        timeout=10.0
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["choices"][0]["message"]["content"]
            elif settings.LLM_PROVIDER in ["gemini", "google"]:
                async with httpx.AsyncClient() as client:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.LLM_MODEL}:generateContent?key={settings.LLM_API_KEY}"
                    resp = await client.post(
                        url,
                        json={"contents": [{"parts": [{"text": prompt}]}]},
                        timeout=10.0
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[LLM Service Error] {str(e)}")
            
        return "Deterministic recommendation supported by structured Gazette & BIS scope records."
