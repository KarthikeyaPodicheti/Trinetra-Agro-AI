"""
Configuration settings for Trinetra Agro AI
"""

import os
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class"""
    
    # Application settings
    APP_NAME = "Trinetra Agro AI"
    VERSION = "1.0.0"
    DEBUG = True
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    
    # AI Model settings
    DISEASE_MODEL_PATH = MODELS_DIR / "disease_detection" / "model.h5"
    MARKET_MODEL_PATH = MODELS_DIR / "market_prediction" / "lstm_model.pkl"
    
    # API Keys (Set these in environment variables)
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'openai/gpt-4-turbo-preview')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/trinetra.db')
    MARKET_DATA_API_KEY = os.getenv('MARKET_DATA_API_KEY', '')
    
    # Language settings
    SUPPORTED_LANGUAGES = ['English', 'Telugu (తెలుగు)', 'Hindi (हिंदी)']
    DEFAULT_LANGUAGE = 'English'
    
    # Model parameters
    IMAGE_SIZE = (224, 224)
    CROP_CLASSES = [
        'Apple', 'Blueberry', 'Cherry', 'Corn', 'Grape', 'Orange', 'Peach',
        'Pepper', 'Potato', 'Rice', 'Soybean', 'Squash', 'Strawberry', 'Tomato'
    ]
    
    # Market prediction settings
    PREDICTION_DAYS = 30
    CONFIDENCE_THRESHOLD = 0.7
    
    # Voice AI settings
    SPEECH_RECOGNITION_LANGUAGE = {
        'English': 'en-US',
        'Telugu (తెలుగు)': 'te-IN',
        'Hindi (हिंदी)': 'hi-IN'
    }
    
    # Farming seasons
    SEASONS = {
        'Kharif': {'months': [6, 7, 8, 9, 10], 'crops': ['rice', 'cotton', 'sugarcane', 'maize']},
        'Rabi': {'months': [11, 12, 1, 2, 3], 'crops': ['wheat', 'barley', 'gram', 'mustard']},
        'Zaid': {'months': [4, 5], 'crops': ['watermelon', 'muskmelon', 'cucumber', 'fodder']}
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///test_trinetra.db'


def load_config(environment: str = 'development') -> Config:
    """
    Load configuration based on environment
    
    Args:
        environment: Configuration environment
        
    Returns:
        Configuration object
    """
    configurations = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return configurations.get(environment, DevelopmentConfig)()


def get_api_endpoints() -> Dict[str, str]:
    """
    Get external API endpoints
    
    Returns:
        API endpoints dictionary
    """
    return {
        'weather': 'https://api.openweathermap.org/data/2.5/weather',
        'market_data': 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070',
        'soil_data': 'https://api.soilhealth.dac.gov.in/api/soildata',
        'crop_calendar': 'https://farmer.gov.in/cropstaticsapi.aspx'
    }


# Agricultural knowledge constants
SOIL_TYPES = {
    'red_soil': {
        'characteristics': ['well_drained', 'iron_rich'],
        'crops': ['peanuts', 'cotton', 'wheat'],
        'ph_range': (5.5, 8.0)
    },
    'black_cotton': {
        'characteristics': ['high_clay', 'moisture_retention'],
        'crops': ['cotton', 'sugarcane', 'wheat'],
        'ph_range': (7.2, 8.5)
    },
    'alluvial': {
        'characteristics': ['fertile', 'well_drained'],
        'crops': ['rice', 'wheat', 'maize'],
        'ph_range': (6.0, 8.0)
    },
    'sandy': {
        'characteristics': ['well_drained', 'low_retention'],
        'crops': ['millets', 'groundnut', 'pulses'],
        'ph_range': (5.5, 7.0)
    },
    'clay': {
        'characteristics': ['high_retention', 'poor_drainage'],
        'crops': ['rice', 'wheat'],
        'ph_range': (6.5, 7.8)
    }
}

CROP_CALENDAR = {
    'rice': {
        'kharif': {'sowing': 'June-July', 'harvesting': 'October-November'},
        'rabi': {'sowing': 'November-December', 'harvesting': 'March-April'}
    },
    'cotton': {
        'kharif': {'sowing': 'May-June', 'harvesting': 'October-January'}
    },
    'wheat': {
        'rabi': {'sowing': 'October-December', 'harvesting': 'March-May'}
    },
    'maize': {
        'kharif': {'sowing': 'June-July', 'harvesting': 'September-October'},
        'rabi': {'sowing': 'October-November', 'harvesting': 'February-March'},
        'zaid': {'sowing': 'February-March', 'harvesting': 'May-June'}
    }
}
