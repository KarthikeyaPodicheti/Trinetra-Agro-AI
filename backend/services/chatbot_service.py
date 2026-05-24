"""Chatbot service — intent routing + OpenRouter LLM."""

from typing import Any, Dict, List, Optional

from backend.services.openrouter_service import OpenRouterService

_AGRI_KEYWORDS = [
    'agri', 'farm', 'crop', 'soil', 'seed', 'sow', 'harvest', 'disease',
    'pest', 'fungus', 'blight', 'wilt', 'irrigation', 'water', 'rain',
    'fertilizer', 'manure', 'npk', 'market', 'mandi', 'price', 'yield',
    'profit', 'livestock', 'dairy', 'tractor', 'drip', 'sprinkler', 'weather',
    'hi', 'hello', 'namaste', 'help', 'suggest', 'advice', 'recommend',
]

_META_KEYWORDS = ['what model', 'who made you', 'are you gpt', 'openai', 'llm', 'what ai']


class ChatbotService:
    def __init__(self):
        self.llm = OpenRouterService()
        self.history: Dict[str, List[Dict]] = {}

    def _is_agriculture(self, text: str) -> bool:
        return any(k in text.lower() for k in _AGRI_KEYWORDS)

    def _is_meta(self, text: str) -> bool:
        return any(k in text.lower() for k in _META_KEYWORDS)

    async def chat(self, message: str, session_id: str = "default",
                   farmer_context: Optional[Dict] = None, language: str = "English") -> str:
        if session_id not in self.history:
            self.history[session_id] = []

        self.history[session_id].append({"role": "user", "content": message})
        recent = self.history[session_id][-6:]

        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.llm.chat, recent, farmer_context, language)

        self.history[session_id].append({"role": "assistant", "content": response})
        return response

    def clear_history(self, session_id: str = "default") -> None:
        self.history.pop(session_id, None)

    def get_history(self, session_id: str = "default") -> List[Dict]:
        return self.history.get(session_id, [])


_chatbot_instance: Optional[ChatbotService] = None


def get_chatbot() -> ChatbotService:
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = ChatbotService()
    return _chatbot_instance
