"""
OpenRouter API Client for Trinetra Agro AI
Handles communication with OpenRouter LLM API
"""

import os
import requests
import json
from typing import Dict, List, Optional
from pathlib import Path
import logging

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class OpenRouterClient:
    """
    Client for OpenRouter API integration
    Provides access to various LLM models through OpenRouter
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize OpenRouter client
        
        Args:
            api_key: OpenRouter API key
            model: Model to use (default: openai/gpt-4-turbo-preview)
        """
        self.api_key = self._normalize_api_key(api_key or os.getenv('OPENROUTER_API_KEY'))
        self.model = model or os.getenv('OPENROUTER_MODEL', 'openai/gpt-4-turbo-preview')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            logging.warning("No OpenRouter API key provided. Chat will use fallback responses.")
            self.api_key = None
        
        self.headers = {
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/KarthikeyaPodicheti/Trinetra-Agro-AI",
            "X-Title": "Trinetra Agro AI"
        }
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Agricultural system prompt
        self.system_prompt = self._get_agricultural_system_prompt()

    @staticmethod
    def _normalize_api_key(api_key: Optional[str]) -> Optional[str]:
        if not api_key:
            return None
        key = api_key.strip()
        if not key:
            return None
        lowered = key.lower()
        placeholder_markers = [
            "your_openrouter_api_key_here",
            "your-actual-api-key-here",
            "replace_with",
            "changeme",
        ]
        if any(marker in lowered for marker in placeholder_markers):
            return None
        return key
    
    def _get_agricultural_system_prompt(self) -> str:
        """
        Generate comprehensive agricultural AI system prompt
        
        Returns:
            System prompt for agricultural AI assistant
        """
        return """You are TRINETRA AGRO AI - "Vision Beyond the Fields" 🔱, an advanced agricultural intelligence assistant with expertise across all aspects of modern farming.

CORE IDENTITY:
- You are an AI farming advisor with deep knowledge of agriculture, crop science, soil management, weather patterns, market trends, and sustainable farming practices
- Your name "Trinetra" means "third eye" - you see beyond what normal farming methods can detect
- You provide practical, actionable advice tailored to individual farmer profiles and local conditions
- You support farmers in English, Telugu (తెలుగు), and Hindi (हिंदी)

EXPERTISE AREAS:
🔬 DISEASE DETECTION & PLANT HEALTH:
- Identify crop diseases, pests, and nutrient deficiencies from descriptions or symptoms
- Provide treatment recommendations with organic and chemical options
- Suggest preventive measures and integrated pest management strategies
- Knowledge of diseases affecting rice, wheat, cotton, maize, vegetables, fruits, and cash crops

📈 MARKET INTELLIGENCE & PRICING:
- Analyze market trends and price patterns for agricultural commodities
- Provide buy/sell recommendations based on seasonal patterns
- Understand government policies, MSP (Minimum Support Price), and subsidy schemes
- Knowledge of local mandis, agricultural markets, and export opportunities

🌾 CROP ADVISORY & PLANNING:
- Recommend suitable crops based on soil type, climate, water availability, and budget
- Provide seasonal agricultural calendars and crop rotation advice
- Suggest high-yield varieties and modern cultivation techniques
- Knowledge of Kharif, Rabi, and Zaid seasons across different regions

💧 IRRIGATION & WATER MANAGEMENT:
- Optimize irrigation schedules based on crop requirements and weather forecasts
- Recommend water conservation techniques and efficient irrigation methods
- Calculate water requirements for different crops and growth stages
- Suggest drought management and water stress mitigation strategies

🧪 SOIL HEALTH & FERTILIZATION:
- Analyze soil types (black cotton, red soil, alluvial, sandy, clay) and their characteristics
- Calculate fertilizer requirements (NPK) based on soil tests and crop needs
- Recommend organic amendments, bio-fertilizers, and sustainable soil management
- Provide guidance on soil pH management and micronutrient deficiencies

🌤️ WEATHER-BASED FARMING:
- Integrate weather forecasts with farming decisions
- Provide climate-smart agriculture recommendations
- Suggest adaptation strategies for changing weather patterns
- Calculate crop failure risk and insurance recommendations

💰 ECONOMIC ANALYSIS & PROFITABILITY:
- Calculate cost of cultivation and expected returns for different crops
- Provide ROI analysis and profit maximization strategies
- Suggest value addition opportunities and farm diversification
- Knowledge of agricultural credit, loans, and financial planning

🏭 MODERN FARMING TECHNOLOGIES:
- Recommend precision agriculture tools and techniques
- Suggest appropriate farm machinery for different scale operations
- Knowledge of IoT sensors, drones, and digital farming solutions
- Promote sustainable and organic farming practices

RESPONSE GUIDELINES:
- Always provide practical, actionable advice that farmers can implement
- Consider local conditions, farmer's resources, and economic constraints
- Use simple language that farmers can understand, avoiding complex technical jargon
- Include cost estimates when recommending inputs or practices
- Mention safety precautions when discussing chemicals or equipment
- Provide alternative solutions for resource-constrained farmers
- Include seasonal timing for recommendations
- Reference local agricultural departments and extension services when appropriate

SAFETY & ETHICS:
- Always prioritize farmer safety and environmental sustainability
- Recommend IPM (Integrated Pest Management) over excessive chemical use
- Promote soil health and long-term farm sustainability
- Respect traditional farming knowledge while introducing modern techniques
- Avoid recommendations that could harm environment or human health

COMMUNICATION STYLE:
- Be friendly, encouraging, and supportive
- Use emojis appropriately to make responses engaging
- Show empathy for farming challenges and celebrate successes
- Provide hope and confidence to farmers facing difficulties
- Use cultural context and local examples when possible

MULTILINGUAL SUPPORT:
- Respond in the language the farmer is most comfortable with
- Use local terminology for crops, practices, and measurements
- Understand regional farming practices and adapt advice accordingly

## remember 
-

Remember: You are here to empower farmers with knowledge and technology to improve their livelihoods while protecting the environment for future generations. Your goal is to make farming more profitable, sustainable, and less risky."""

    def chat_completion(self, messages: List[Dict], farmer_profile: Dict = None) -> str:
        """
        Get chat completion from OpenRouter API
        
        Args:
            messages: List of message dictionaries
            farmer_profile: Farmer's profile for personalized responses
            
        Returns:
            AI response string
        """
        if not self.api_key:
            return self._fallback_response(messages[-1]['content'] if messages else "")
        
        try:
            # Add farmer context to system prompt if available
            contextualized_prompt = self.system_prompt
            if farmer_profile:
                context = self._build_farmer_context(farmer_profile)
                contextualized_prompt += f"\n\nFARMER CONTEXT:\n{context}"
            
            # Prepare messages with system prompt
            api_messages = [{"role": "system", "content": contextualized_prompt}]
            api_messages.extend(messages)
            
            payload = {
                "model": self.model,
                "messages": api_messages,
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                logging.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return self._fallback_response(messages[-1]['content'] if messages else "")
                
        except requests.exceptions.RequestException as e:
            logging.error(f"OpenRouter API request error: {e}")
            return self._fallback_response(messages[-1]['content'] if messages else "")
        except Exception as e:
            logging.error(f"OpenRouter API unexpected error: {e}")
            return self._fallback_response(messages[-1]['content'] if messages else "")
    
    def _build_farmer_context(self, farmer_profile: Dict) -> str:
        """
        Build farmer context for personalized responses
        
        Args:
            farmer_profile: Farmer's profile data
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        if farmer_profile.get('name'):
            context_parts.append(f"Farmer Name: {farmer_profile['name']}")
        
        if farmer_profile.get('location'):
            context_parts.append(f"Location: {farmer_profile['location']}")
            
        if farmer_profile.get('land_size'):
            context_parts.append(f"Farm Size: {farmer_profile['land_size']} acres")
            
        if farmer_profile.get('soil_type'):
            context_parts.append(f"Soil Type: {farmer_profile['soil_type']}")
            
        if farmer_profile.get('budget'):
            context_parts.append(f"Budget: ₹{farmer_profile['budget']:,}")
            
        if farmer_profile.get('crops'):
            context_parts.append(f"Current Crops: {', '.join(farmer_profile['crops'])}")
            
        if farmer_profile.get('experience'):
            context_parts.append(f"Farming Experience: {farmer_profile['experience']} years")
        
        return "\n".join(context_parts) if context_parts else "General farmer inquiry"
    
    def _fallback_response(self, user_input: str) -> str:
        """
        Provide fallback response when API is unavailable
        
        Args:
            user_input: User's message
            
        Returns:
            Fallback response
        """
        fallback_responses = {
            'greeting': "🙏 Namaste! I'm Trinetra, your AI farming advisor. While I'm currently in offline mode, I'm here to help with basic farming guidance. For advanced AI features, please add your OpenRouter API key to the .env file.",
            'crop_advice': "🌾 For crop recommendations, I suggest consulting with your local agricultural extension officer. Generally, consider your soil type, climate, water availability, and market demand when selecting crops.",
            'disease': "🔬 For disease identification, please consult a plant pathologist or visit your nearest Krishi Vigyan Kendra. Early detection and proper treatment are crucial for crop health.",
            'market': "📈 For current market prices, check with your local mandi or agricultural department. Consider seasonal demand and storage costs when planning sales.",
            'general': "🔱 I'm your agricultural AI assistant. While my advanced AI features require an API connection, I recommend consulting local agricultural experts, extension services, or Krishi Vigyan Kendras for immediate farming guidance."
        }
        
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['hello', 'hi', 'namaste', 'good']):
            return fallback_responses['greeting']
        elif any(word in input_lower for word in ['crop', 'plant', 'sow', 'variety']):
            return fallback_responses['crop_advice']
        elif any(word in input_lower for word in ['disease', 'pest', 'spot', 'leaf']):
            return fallback_responses['disease']
        elif any(word in input_lower for word in ['price', 'market', 'sell', 'rate']):
            return fallback_responses['market']
        else:
            return fallback_responses['general']
    
    def test_connection(self) -> bool:
        """
        Test OpenRouter API connection
        
        Returns:
            True if connection successful, False otherwise
        """
        if not self.api_key:
            return False
            
        try:
            test_message = [{"role": "user", "content": "Hello, are you working?"}]
            response = self.chat_completion(test_message)
            return len(response) > 0
        except:
            return False
