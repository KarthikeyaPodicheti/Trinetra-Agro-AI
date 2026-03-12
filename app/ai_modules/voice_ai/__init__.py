"""
Trinetra Agro AI - Multilingual Voice AI Module
Speech-to-Text and Text-to-Speech for Telugu and other Indian languages
"""

import os
import time
from typing import Optional, Dict

# Try importing speech recognition libraries
try:
    import speech_recognition as sr
    SPEECH_RECOG_AVAILABLE = True
except ImportError:
    SPEECH_RECOG_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


class VoiceAI:
    """
    Multilingual Voice AI for Farmers
    Supports Speech-to-Text and Text-to-Speech in Telugu, Hindi, English
    """
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'en': {'name': 'English', 'code': 'en', 'tts_code': 'en'},
        'te': {'name': 'Telugu (తెలుగు)', 'code': 'te-IN', 'tts_code': 'te'},
        'hi': {'name': 'Hindi (हिंदी)', 'code': 'hi-IN', 'tts_code': 'hi'},
        'ta': {'name': 'Tamil (தமிழ்)', 'code': 'ta-IN', 'tts_code': 'ta'},
        'kn': {'name': 'Kannada (ಕನ್ನಡ)', 'code': 'kn-IN', 'tts_code': 'kn'},
        'ml': {'name': 'Malayalam (മലയാളം)', 'code': 'ml-IN', 'tts_code': 'ml'},
        'bn': {'name': 'Bengal (বাংলা)', 'code': 'bn-IN', 'tts_code': 'bn'},
        'mr': {'name': 'Marathi (मराठी)', 'code': 'mr-IN', 'tts_code': 'mr'}
    }
    
    # Common farming phrases in Telugu
    TELUGU_PHRASES = {
        'greeting': ['నమస్కారం', 'హలో', 'శుభాకాంశలు'],
        'disease': [' వ్యాధి', ' ఆకు', ' మచ్చ', ' ఎలుగుబంటి'],
        'crop': [' పంట', ' విత్తనం', ' కూర్చు'],
        'price': [' ధర', ' వాణిజ్యం', ' అమ్ముట'],
        'help': [' సహాయం', ' బుద్ధి', ' చెప్పు']
    }
    
    def __init__(self):
        """Initialize Voice AI"""
        self.recognizer = None
        self.microphone = None
        self.current_language = 'te'  # Default to Telugu
        self.is_listening = False
        
        if SPEECH_RECOG_AVAILABLE:
            self._init_speech_recognition()
    
    def _init_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("✅ Speech recognition initialized")
        except Exception as e:
            print(f"⚠️ Speech recognition init error: {e}")
            self.recognizer = None
            self.microphone = None
    
    def set_language(self, language_code: str) -> Dict:
        """
        Set the current language for voice interaction
        
        Args:
            language_code: Language code (en, te, hi, etc.)
            
        Returns:
            Status dictionary
        """
        if language_code in self.SUPPORTED_LANGUAGES:
            self.current_language = language_code
            return {
                'success': True,
                'message': f"Language changed to {self.SUPPORTED_LANGUAGES[language_code]['name']}"
            }
        return {
            'success': False,
            'error': f"Language {language_code} not supported"
        }
    
    def listen(self, timeout: int = 5) -> Dict:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: Maximum seconds to wait for speech
            
        Returns:
            Dictionary with transcribed text
        """
        if not SPEECH_RECOG_AVAILABLE or not self.recognizer:
            return {
                'success': False,
                'error': 'Speech recognition not available',
                'text': None
            }
        
        lang_code = self.SUPPORTED_LANGUAGES.get(self.current_language, 
                                                   self.SUPPORTED_LANGUAGES['te'])['code']
        
        try:
            with self.microphone as source:
                print(f"🎤 Listening in {self.SUPPORTED_LANGUAGES[self.current_language]['name']}...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # Try Google Speech Recognition
            try:
                text = self.recognizer.recognize_google(audio, language=lang_code)
                print(f"📝 Recognized: {text}")
                return {
                    'success': True,
                    'text': text,
                    'language': self.current_language
                }
            except sr.UnknownValueError:
                return {
                    'success': False,
                    'error': 'Could not understand speech',
                    'text': None
                }
            except sr.RequestError as e:
                return {
                    'success': False,
                    'error': f'Speech recognition service error: {e}',
                    'text': None
                }
                
        except sr.WaitTimeoutError:
            return {
                'success': False,
                'error': 'No speech detected (timeout)',
                'text': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': None
            }
    
    def speak(self, text: str, save_file: str = None) -> Dict:
        """
        Convert text to speech and play
        
        Args:
            text: Text to speak
            save_file: Optional file path to save audio
            
        Returns:
            Status dictionary
        """
        if not GTTS_AVAILABLE:
            return self._speak_fallback(text)
        
        lang_code = self.SUPPORTED_LANGUAGES.get(self.current_language, 
                                                   self.SUPPORTED_LANGUAGES['te'])['tts_code']
        
        try:
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            if save_file:
                tts.save(save_file)
                return {'success': True, 'file': save_file}
            
            # Play audio (requires additional library or file playback)
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tts.save(tmp.name)
                
                # Try to play
                try:
                    import playsound
                    playsound.playsound(tmp.name)
                    os.unlink(tmp.name)
                    return {'success': True}
                except ImportError:
                    # Save to temp location if playsound not available
                    return {
                        'success': True, 
                        'message': f'Audio generated but playback not available. Saved to {tmp.name}',
                        'temp_file': tmp.name
                    }
                    
        except Exception as e:
            return self._speak_fallback(text)
    
    def _speak_fallback(self, text: str) -> Dict:
        """Fallback TTS using pyttsx3"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
            return {'success': True, 'method': 'pyttsx3'}
        except:
            return {
                'success': False,
                'message': f'🔊 {text}',  # Return as text display
                'error': 'No TTS available'
            }
    
    def speak_agricultural_terms(self, term: str) -> Dict:
        """
        Speak agricultural terms in local language
        
        Args:
            term: Agricultural term to speak
            
        Returns:
            Status dictionary
        """
        translations = {
            'disease': {
                'te': 'व्याधि (vīrōdha)',
                'en': 'Disease'
            },
            'fertilizer': {
                'te': 'పత్తం (pattaina)',
                'en': 'Fertilizer'
            },
            'pesticide': {
                'te': 'క్రిమిసాధకం (krimināśaka)',
                'en': 'Pesticide'
            },
            'irrigation': {
                'te': ' నీటిపారుసల (nītipārusala)',
                'en': 'Irrigation'
            },
            'harvest': {
                'te': 'కోత (kōta)',
                'en': 'Harvest'
            }
        }
        
        term_lower = term.lower()
        if term_lower in translations:
            text = translations[term_lower].get(self.current_language, translations[term_lower]['en'])
            return self.speak(text)
        
        return self.speak(term)
    
    def get_available_languages(self) -> Dict:
        """Get list of available languages"""
        return {
            'supported': self.SUPPORTED_LANGUAGES,
            'current': self.current_language
        }
    
    def continuous_listen(self, duration: int = 10) -> Dict:
        """
        Listen for multiple phrases
        
        Args:
            duration: Maximum duration in seconds
            
        Returns:
            List of recognized phrases
        """
        phrases = []
        start_time = time.time()
        
        print(f"🎤 Continuous listening for {duration} seconds...")
        
        while time.time() - start_time < duration:
            result = self.listen(timeout=3)
            
            if result['success'] and result['text']:
                phrases.append(result['text'])
                print(f"  ✓: {result['text']}")
        
        return {
            'success': True,
            'phrases': phrases,
            'count': len(phrases)
        }
    
    def voice_command_example(self) -> str:
        """Example voice command flow"""
        return """
        🎤 Voice Command Example:
        
        1. Set Language: "Set language to Telugu"
        2. Ask Question: "Tell me about tomato diseases"
        3. Get Response: System speaks answer
        
        Commands:
        - "Detect disease" → Opens disease detection
        - "Market price" → Shows market prices
        - "Crop advice" → Gives crop recommendations
        """
    
    def process_voice_query(self) -> Dict:
        """
        Complete voice query processing pipeline
        
        1. Listen to voice
        2. Convert to text
        3. Process query
        4. Generate and speak response
        """
        # Step 1: Listen
        listen_result = self.listen(timeout=5)
        
        if not listen_result['success']:
            return {
                'step': 'listen',
                'success': False,
                'error': listen_result['error']
            }
        
        # Step 2: Return transcribed text for NLP processing
        return {
            'step': 'transcribe',
            'success': True,
            'text': listen_result['text'],
            'language': self.current_language
        }


class TeluguNLP:
    """
    Simple Telugu NLP for agricultural terms
    """
    
    # Telugu agricultural vocabulary
    VOCABULARY = {
        'paddy': ' వరి',
        'rice': ' వరి',
        'cotton': ' పత్తి',
        'sugarcane': ' చెరుకు',
        'tomato': ' tomato (টমాటो)',
        'potato': ' ఉల్లిపాయ',
        'onion': ' ఉల్లిపాయ',
        'wheat': ' గోధుమ',
        'disease': ' వ్యాధి',
        'pest': ' బ్రాహ్మణ',
        'fertilizer': 'త్రావు',
        'water': ' నీరు',
        'rain': ' వర్షం',
        'soil': ' నేల',
        'field': ' పొలం',
        'farmer': ' telugu farmer'
    }
    
    # Common farming questions in Telugu
    QUESTION_PATTERNS = [
        'naa pelli kosam emi undi',
        'crop chese vaasthundam',
        'disease vachhindi',
        'price enti',
        'fertilizer emi use cheyali'
    ]
    
    def __init__(self):
        """Initialize Telugu NLP"""
        self.language = 'te'
    
    def detect_intent(self, text: str) -> str:
        """Detect intent from Telugu text"""
        text_lower = text.lower()
        
        if 'disease' in text_lower or 'infection' in text_lower:
            return 'disease_detection'
        elif 'price' in text_lower or 'market' in text_lower:
            return 'market_prediction'
        elif 'crop' in text_lower or 'plant' in text_lower:
            return 'crop_advice'
        elif 'water' in text_lower or 'irrigation' in text_lower:
            return 'irrigation'
        else:
            return 'general'
    
    def translate_key_terms(self, text: str) -> str:
        """Translate common terms to Telugu"""
        for eng, tel in self.VOCABULARY.items():
            text = text.replace(eng, tel)
        return text


# Factory functions
def create_voice_ai() -> VoiceAI:
    """Create and return Voice AI instance"""
    return VoiceAI()


def create_telugu_nlp() -> TeluguNLP:
    """Create and return Telugu NLP instance"""
    return TeluguNLP()


if __name__ == "__main__":
    voice = create_voice_ai()
    print("Voice AI initialized!")
    print(f"Supported languages: {list(voice.SUPPORTED_LANGUAGES.keys())}")
    
    # Set to Telugu
    voice.set_language('te')
    print(f"Current language: {voice.current_language}")
