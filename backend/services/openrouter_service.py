"""OpenRouter LLM client using backend config."""

from typing import Dict, List, Optional

import requests

from backend.core.config import get_settings

settings = get_settings()

AGRICULTURE_PROMPT = """You are TRINETRA AGRO AI - "Vision Beyond the Fields", an advanced agricultural intelligence assistant.

You help farmers with: crop diseases, market prices, irrigation, yield prediction, risk assessment, profit analysis, crop recommendations, fertilizer advice, weather-based farming, and sustainable practices.

Rules:
- Give practical, actionable advice farmers can implement
- Use simple language, avoid complex jargon
- Include cost estimates when recommending inputs
- Mention safety precautions for chemicals
- Support English, Telugu, and Hindi
- Be encouraging and supportive
"""


class OpenRouterService:
    def __init__(self):
        self.api_key = self._normalize(settings.openrouter_api_key)
        self.model = settings.openrouter_model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    @staticmethod
    def _normalize(key: str) -> Optional[str]:
        if not key or not key.strip():
            return None
        k = key.strip().lower()
        if any(m in k for m in ["your_openrouter_api_key_here", "your-actual", "replace_with", "changeme"]):
            return None
        return key.strip()

    @property
    def is_available(self) -> bool:
        return self.api_key is not None

    def chat(self, messages: List[Dict], farmer_context: Optional[Dict] = None, language: str = "English") -> str:
        if not self.api_key:
            return self._fallback(messages[-1]["content"] if messages else "")

        system = AGRICULTURE_PROMPT
        if language != "English":
            system += f"\n\nIMPORTANT: Respond ONLY in {language}. Use {language} script."
        if farmer_context:
            ctx = ", ".join(f"{k}: {v}" for k, v in farmer_context.items() if v)
            system += f"\n\nFarmer context: {ctx}"

        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}] + messages,
            "temperature": 0.7,
            "max_tokens": 500,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/KarthikeyaPodicheti/Trinetra-Agro-AI",
            "X-Title": "Trinetra Agro AI",
        }

        try:
            resp = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception:
            pass
        return self._fallback(messages[-1]["content"] if messages else "")

    def _fallback(self, user_input: str) -> str:
        inp = user_input.lower()
        if any(w in inp for w in ["hello", "hi", "namaste"]):
            return ("Namaste! I'm Trinetra, your AI farming advisor. "
                    "I'm currently in offline mode but can help with basic farming guidance. "
                    "Try asking about crops, diseases, markets, irrigation, or profit.")
        if any(w in inp for w in ["disease", "pest", "spot", "leaf"]):
            return ("For disease identification, upload a leaf image in the Disease Detection tab. "
                    "Meanwhile, describe the symptoms and I'll try to help.")
        if any(w in inp for w in ["price", "market", "sell"]):
            return ("For market prices, check the Market Prediction tab. "
                    "You can also visit your local mandi for real-time rates.")
        return ("I'm Trinetra, your AI farming advisor. I can help with crops, diseases, "
                "markets, irrigation, yield, risk, and profit. What would you like to know?")
