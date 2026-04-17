"""
Trinetra Agro AI - Core Chatbot Module
The main intelligence engine for agricultural conversations
"""

import random
import datetime
from typing import Dict, List, Any
import sys
from pathlib import Path

# Make sure sibling packages are importable
sys.path.append(str(Path(__file__).parent.parent))

# --- AI module imports (lazy-safe) ---
try:
    from ai_modules.disease_detection import DiseaseDetector
except Exception:
    DiseaseDetector = None

try:
    from ai_modules.market_prediction import MarketPredictor
except Exception:
    MarketPredictor = None

try:
    from ai_modules.crop_advisor import CropAdvisor
except Exception:
    CropAdvisor = None

try:
    from ai_modules.risk_assessment import assess_risk
except Exception:
    assess_risk = None

try:
    from ai_modules.yield_prediction import predict_yield
except Exception:
    predict_yield = None

try:
    from ai_modules.irrigation_ai import irrigation_plan
except Exception:
    irrigation_plan = None

try:
    from ai_modules.profit_predictor import predict_profit
except Exception:
    predict_profit = None

# OpenRouter LLM (optional)
try:
    from utils.openrouter_client import OpenRouterClient
except ImportError:
    try:
        sys.path.append(str(Path(__file__).parent.parent / 'utils'))
        from openrouter_client import OpenRouterClient
    except ImportError:
        OpenRouterClient = None


class TrinetraBot:
    """Core chatbot – routes intents to the real AI modules."""

    def __init__(self, language: str = "English", farmer_profile: Dict = None):
        self.language = language
        self.farmer_profile = farmer_profile or {}
        self.conversation_history: list = []
        self.context: dict = {}

        # Initialise AI modules (cheap — all run on CPU / numpy)
        self.disease_detector = DiseaseDetector() if DiseaseDetector else None
        self.market_predictor = MarketPredictor() if MarketPredictor else None
        self.crop_advisor = CropAdvisor() if CropAdvisor else None

        # OpenRouter LLM (optional enrichment)
        self.openrouter_client = None
        if OpenRouterClient:
            try:
                self.openrouter_client = OpenRouterClient()
                if not self.openrouter_client.api_key:
                    self.openrouter_client = None
            except Exception:
                self.openrouter_client = None

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------
    def get_response(self, user_input: str) -> str:
        self.conversation_history.append({'user': user_input, 'timestamp': self._ts()})
        intent = self._analyze_intent(user_input)
        response = self._generate_response(intent, user_input)
        # Translate to selected language
        response = self._translate(response)
        self.conversation_history.append({'bot': response, 'timestamp': self._ts()})
        return response

    # ------------------------------------------------------------------
    # Intent classification (keyword-based)
    # ------------------------------------------------------------------
    def _analyze_intent(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ['disease', 'pest', 'fungus', 'infection', 'leaf', 'spot', 'blight', 'wilt', 'rot']):
            return 'disease_inquiry'
        if any(w in t for w in ['price', 'market', 'sell', 'cost', 'rate', 'mandi']):
            return 'market_inquiry'
        if any(w in t for w in ['crop', 'plant', 'sow', 'harvest', 'variety', 'seed', 'recommend']):
            return 'crop_advice'
        if any(w in t for w in ['water', 'irrigation', 'rain', 'drought', 'moisture']):
            return 'irrigation_advice'
        if any(w in t for w in ['fertilizer', 'manure', 'nutrient', 'nitrogen', 'phosphorus', 'npk']):
            return 'fertilizer_advice'
        if any(w in t for w in ['risk', 'danger', 'loss', 'insurance']):
            return 'risk_inquiry'
        if any(w in t for w in ['yield', 'production', 'output', 'how much']):
            return 'yield_inquiry'
        if any(w in t for w in ['profit', 'income', 'earning', 'return', 'revenue']):
            return 'profit_inquiry'
        if any(w in t for w in ['hello', 'hi', 'namaste', 'good morning', 'good evening', 'help']):
            return 'greeting'
        return 'general'

    # ------------------------------------------------------------------
    # Response generation
    # ------------------------------------------------------------------
    def _generate_response(self, intent: str, user_input: str) -> str:
        if self._is_meta_ai_question(user_input):
            return self._domain_guardrail_response()

        if intent == 'general' and not self._is_agriculture_related(user_input):
            return self._domain_guardrail_response()

        # Try LLM first
        if self.openrouter_client:
            try:
                msgs = self._prepare_conversation_for_llm(user_input)
                llm = self.openrouter_client.chat_completion(msgs, self.farmer_profile)
                if llm and llm.strip():
                    return self._personalise(llm, intent)
            except Exception:
                pass

        # --- Fallback: route to rule-based modules ---
        return self._rule_based(intent, user_input)

    def _rule_based(self, intent, user_input):
        if intent == 'disease_inquiry':
            return self._disease_response(user_input)
        if intent == 'market_inquiry':
            return self._market_response(user_input)
        if intent == 'crop_advice':
            return self._crop_response()
        if intent == 'irrigation_advice':
            return self._irrigation_response(user_input)
        if intent == 'fertilizer_advice':
            return self._fertilizer_response()
        if intent == 'risk_inquiry':
            return self._risk_response(user_input)
        if intent == 'yield_inquiry':
            return self._yield_response(user_input)
        if intent == 'profit_inquiry':
            return self._profit_response(user_input)
        if intent == 'greeting':
            return self._greeting()
        return self._general_response()

    # --- intent handlers ---
    def _greeting(self):
        if self.language.startswith("Telugu"):
            return "🙏 నమస్కారం! నేను త్రినేత్ర, మీ AI వ్యవసాయ సలహాదారుని. మీకు ఎలా సహాయం చేయాలి?"
        return ("🙏 Namaste! I'm **Trinetra**, your AI farming advisor.\n\n"
                "I can help with:\n"
                "• 🔬 Disease detection\n• 📈 Market prices\n• 🌾 Crop advice\n"
                "• 💧 Irrigation\n• ⚠️ Risk assessment\n• 🌾 Yield prediction\n"
                "• 💰 Profit estimation\n\nWhat would you like to know?")

    def _disease_response(self, user_input):
        return ("🔬 I can identify crop diseases! Upload a leaf image in the **Disease Detection** tab "
                "for AI-powered analysis.\n\nMeanwhile, describe the symptoms and I'll try to help:\n"
                "• Leaf spots or discoloration?\n• Wilting or yellowing?\n• Any unusual growth?")

    def _market_response(self, user_input):
        if not self.market_predictor:
            return "📈 Market prediction module is loading... Please try the Market Prediction tab."
        crop = self._extract_crop(user_input)
        if crop:
            res = self.market_predictor.predict_prices(crop, 14)
            if res.get('success'):
                rec = res['recommendation']
                return (f"📈 **{crop.title()} Market Prediction** (14 days)\n\n"
                        f"• Current price: **₹{res['current_price']:,.0f}/quintal**\n"
                        f"• Trend: **{res['trend'].title()}**\n"
                        f"• Confidence: {res['confidence']}\n"
                        f"• Recommendation: **{rec['action']}** — {rec['message']}\n\n"
                        f"💡 {res['market_tips'][0] if res['market_tips'] else ''}")
        return "📈 Which crop's market price would you like to know? (rice, wheat, cotton, tomato, etc.)"

    def _crop_response(self):
        if not self.crop_advisor:
            return "🌾 Crop advisor loading... Use the Farming Advisor tab."
        profile = {
            'soil_type': self.farmer_profile.get('soil_type', 'loamy'),
            'land_size': self.farmer_profile.get('land_size', 5),
            'budget': self.farmer_profile.get('budget', 50000),
            'location': self.farmer_profile.get('location', ''),
            'irrigation_available': True,
        }
        recs = self.crop_advisor.get_recommendations(profile=profile)
        if recs.get('success'):
            primary = recs.get('primary_recommendations', [])[:3]
            names = ', '.join(c.get('name', c.get('crop_id', '')).title() for c in primary)
            return (f"🌾 **Crop Recommendations** for your profile:\n\n"
                    f"**Top picks:** {names}\n\n"
                    f"Check the **Farming Advisor** tab for full seasonal plans!")
        return "🌾 I can recommend crops! Tell me your soil type, land size, and budget."

    def _irrigation_response(self, user_input):
        if irrigation_plan is None:
            return "💧 Irrigation module loading..."
        crop = self._extract_crop(user_input) or 'rice'
        acres = self.farmer_profile.get('land_size', 5)
        res = irrigation_plan(crop, acres)
        if res.get('success'):
            w = res['water_needs']
            s = res['schedule']
            return (f"💧 **Irrigation Plan — {res['crop']}** ({acres} acres)\n\n"
                    f"• Daily need: **{w['daily_litres']:,.0f} litres** ({w['daily_mm']} mm)\n"
                    f"• Weekly: **{w['weekly_litres']:,.0f} litres**\n"
                    f"• Method: {res['recommended_method']}\n"
                    f"• Schedule: {s['frequency']} — {s['best_time']}\n\n"
                    f"💡 {res['tips'][0]}")
        return "💧 Which crop needs irrigation advice?"

    def _fertilizer_response(self):
        return ("🧪 **Fertilizer Guide:**\n\n"
                "| Crop | NPK Ratio | Per Acre |\n|---|---|---|\n"
                "| Rice | 100:50:50 | 200 kg |\n"
                "| Wheat | 120:60:40 | 180 kg |\n"
                "| Cotton | 100:50:50 | 250 kg |\n"
                "| Tomato | 100:60:80 | 220 kg |\n\n"
                "Always do a soil test before applying! 🌱")

    def _risk_response(self, user_input):
        if assess_risk is None:
            return "⚠️ Risk module loading..."
        crop = self._extract_crop(user_input) or 'rice'
        res = assess_risk(
            crop,
            soil_type=self.farmer_profile.get('soil_type', ''),
            land_size=self.farmer_profile.get('land_size', 5),
            budget=self.farmer_profile.get('budget', 50000),
        )
        return (f"⚠️ **Risk Assessment — {res['crop']}**\n\n"
                f"• Risk Score: **{res['risk_score']}/100** ({res['risk_level']})\n"
                f"• Factors: {'; '.join(res['factors'][:3]) if res['factors'] else 'None significant'}\n\n"
                f"**Mitigations:** " + "; ".join(res['mitigations'][:3]))

    def _yield_response(self, user_input):
        if predict_yield is None:
            return "🌾 Yield prediction module loading..."
        crop = self._extract_crop(user_input) or 'rice'
        acres = self.farmer_profile.get('land_size', 5)
        res = predict_yield(crop, acres, self.farmer_profile.get('soil_type', ''))
        if res.get('success'):
            e = res['estimates']
            return (f"🌾 **Yield Estimate — {res['crop']}** ({acres} acres)\n\n"
                    f"• Conservative: **{e['conservative']:.1f} {res['unit']}**\n"
                    f"• Moderate: **{e['moderate']:.1f} {res['unit']}**\n"
                    f"• Optimistic: **{e['optimistic']:.1f} {res['unit']}**\n\n"
                    f"📝 {res['notes'][0]}")
        return res.get('error', 'Could not predict yield.')

    def _profit_response(self, user_input):
        if predict_profit is None:
            return "💰 Profit module loading..."
        crop = self._extract_crop(user_input) or 'rice'
        acres = self.farmer_profile.get('land_size', 5)
        res = predict_profit(crop, acres, soil_type=self.farmer_profile.get('soil_type', ''))
        if res.get('success'):
            p = res['profit']
            return (f"💰 **Profit Estimate — {res['crop']}** ({acres} acres)\n\n"
                    f"• Input cost: ₹{res['input_costs']['total']:,.0f}\n"
                    f"• Profit (moderate): **₹{p['moderate']:,.0f}**\n"
                    f"• ROI: {res['roi_percent']['moderate']}%\n\n"
                    f"📝 {res['recommendation']}")
        return res.get('error', 'Could not predict profit.')

    def _general_response(self):
        return ("I'm Trinetra 🔱 — your AI farming advisor!\n\n"
                "Ask me about **crops, diseases, markets, irrigation, yield, risk, or profit** "
                "and I'll provide intelligent guidance.")

    def _domain_guardrail_response(self):
        if self.language.startswith("Telugu"):
            return ("నేను వ్యవసాయం మరియు పంటల విషయాలకే సహాయం చేస్తాను. 🌾\n\n"
                    "దయచేసి పంటలు, వ్యాధులు, మార్కెట్ ధరలు, నీటిపారుదల, దిగుబడి లేదా లాభాలపై ప్రశ్న అడగండి.")
        if self.language.startswith("Hindi"):
            return ("मैं केवल खेती और कृषि से जुड़े सवालों में मदद करता हूं। 🌾\n\n"
                    "कृपया फसल, रोग, मंडी भाव, सिंचाई, उपज या मुनाफे से जुड़ा सवाल पूछें।")
        return ("I can only help with farming and agriculture-related questions. 🌾\n\n"
                "Please ask about crops, plant diseases, market prices, irrigation, yield, risk, or profit.")

    # --- helpers ---
    _CROP_KEYWORDS = [
        'rice', 'wheat', 'cotton', 'tomato', 'potato', 'onion', 'maize',
        'corn', 'sugarcane', 'soybean', 'groundnut', 'mustard',
    ]

    _AGRI_KEYWORDS = [
        'agri', 'agriculture', 'farming', 'farm', 'crop', 'soil', 'seed', 'sow', 'harvest',
        'disease', 'pest', 'fungus', 'blight', 'wilt', 'irrigation', 'water', 'rain',
        'fertilizer', 'manure', 'npk', 'market', 'mandi', 'price', 'yield', 'profit',
        'livestock', 'dairy', 'tractor', 'drip', 'sprinkler', 'weather',
    ]

    _META_AI_KEYWORDS = [
        'what model', 'which model', 'who made you', 'who created you', 'are you gpt',
        'openai', 'llm', 'architecture', 'model are you', 'what ai are you',
    ]

    def _extract_crop(self, text):
        t = text.lower()
        for c in self._CROP_KEYWORDS:
            if c in t:
                return c
        return None

    def _is_agriculture_related(self, text: str) -> bool:
        t = (text or '').lower()
        return any(k in t for k in self._AGRI_KEYWORDS)

    def _is_meta_ai_question(self, text: str) -> bool:
        t = (text or '').lower()
        return any(k in t for k in self._META_AI_KEYWORDS)

    def _personalise(self, resp, intent):
        if 'name' in self.farmer_profile:
            resp = resp.replace("farmer", f"{self.farmer_profile['name']} ji", 1)
        season = self._get_current_season()
        if intent in ('crop_advice', 'irrigation_advice'):
            resp += f"\n\n🗓️ *Current {season} season recommendations*"
        return resp

    def _translate(self, text: str) -> str:
        """Translate text to the selected language (no-op for English)."""
        if not self.language or self.language.startswith("English"):
            return text
        try:
            from utils.translator import translate
            return translate(text, self.language)
        except Exception:
            return text

    @staticmethod
    def _get_current_season():
        m = datetime.datetime.now().month
        if m in (6, 7, 8, 9, 10):
            return 'Kharif'
        elif m in (11, 12, 1, 2, 3):
            return 'Rabi'
        return 'Zaid'

    @staticmethod
    def _ts():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _prepare_conversation_for_llm(self, current_input):
        msgs = []
        for e in self.conversation_history[-6:]:
            if 'user' in e:
                msgs.append({"role": "user", "content": e['user']})
            elif 'bot' in e:
                msgs.append({"role": "assistant", "content": e['bot']})
        msgs.append({"role": "user", "content": current_input})
        return msgs

    def update_farmer_profile(self, updates: Dict):
        if updates:
            self.farmer_profile.update(updates)

    def get_api_status(self) -> Dict[str, Any]:
        connected = self.openrouter_client is not None and getattr(self.openrouter_client, 'api_key', None) is not None
        return {
            'openrouter_connected': connected,
            'openrouter_tested': False,
            'fallback_mode': not connected,
        }

    def get_conversation_summary(self) -> Dict:
        return {
            'total_messages': len(self.conversation_history),
            'farmer_profile': self.farmer_profile,
            'language': self.language,
        }
