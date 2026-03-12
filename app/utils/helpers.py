"""
Helper functions and utilities for Trinetra Agro AI
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"trinetra_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def validate_farmer_profile(profile: Dict[str, Any]) -> bool:
    """
    Validate farmer profile data
    
    Args:
        profile: Farmer profile dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['land_size', 'soil_type']
    
    for field in required_fields:
        if field not in profile or profile[field] is None:
            return False
    
    # Validate land size
    if not isinstance(profile['land_size'], (int, float)) or profile['land_size'] <= 0:
        return False
    
    # Validate soil type
    valid_soil_types = ['red_soil', 'black_cotton', 'alluvial', 'sandy', 'clay']
    if profile['soil_type'].lower().replace(' ', '_') not in valid_soil_types:
        return False
    
    return True


def get_current_season() -> str:
    """
    Get current agricultural season
    
    Returns:
        Current season name
    """
    month = datetime.now().month
    
    if month in [6, 7, 8, 9, 10]:
        return "Kharif"
    elif month in [11, 12, 1, 2, 3]:
        return "Rabi"
    else:
        return "Zaid"


def calculate_crop_suitability(soil_type: str, season: str, budget: float) -> List[Dict]:
    """
    Calculate crop suitability based on parameters
    
    Args:
        soil_type: Type of soil
        season: Current season
        budget: Available budget
        
    Returns:
        List of suitable crops with scores
    """
    from .config import SOIL_TYPES, CROP_CALENDAR
    
    suitable_crops = []
    
    # Sample crop database
    crops_db = {
        'rice': {
            'investment_per_acre': 25000,
            'profit_potential': 0.8,
            'suitable_soils': ['alluvial', 'clay'],
            'seasons': ['kharif', 'rabi']
        },
        'cotton': {
            'investment_per_acre': 35000,
            'profit_potential': 0.9,
            'suitable_soils': ['black_cotton', 'red_soil'],
            'seasons': ['kharif']
        },
        'wheat': {
            'investment_per_acre': 20000,
            'profit_potential': 0.7,
            'suitable_soils': ['alluvial', 'black_cotton'],
            'seasons': ['rabi']
        },
        'maize': {
            'investment_per_acre': 18000,
            'profit_potential': 0.75,
            'suitable_soils': ['alluvial', 'red_soil', 'sandy'],
            'seasons': ['kharif', 'rabi', 'zaid']
        }
    }
    
    soil_normalized = soil_type.lower().replace(' ', '_')
    season_normalized = season.lower()
    
    for crop_name, crop_data in crops_db.items():
        score = 0
        
        # Soil suitability
        if soil_normalized in crop_data['suitable_soils']:
            score += 40
        
        # Season suitability
        if season_normalized in crop_data['seasons']:
            score += 30
        
        # Budget feasibility
        if budget >= crop_data['investment_per_acre']:
            score += 20
        elif budget >= crop_data['investment_per_acre'] * 0.7:
            score += 10
        
        # Profit potential
        score += crop_data['profit_potential'] * 10
        
        if score > 50:  # Minimum threshold
            suitable_crops.append({
                'crop': crop_name.title(),
                'score': round(score, 1),
                'investment_needed': crop_data['investment_per_acre'],
                'profit_potential': f"{crop_data['profit_potential']*100:.0f}%"
            })
    
    # Sort by score
    suitable_crops.sort(key=lambda x: x['score'], reverse=True)
    return suitable_crops[:5]  # Top 5 recommendations


def process_weather_data(location: str) -> Dict[str, Any]:
    """
    Process weather data for agricultural insights
    
    Args:
        location: Location for weather data
        
    Returns:
        Processed weather information
    """
    # Simulated weather data (replace with actual API call)
    weather_data = {
        'temperature': np.random.randint(25, 35),
        'humidity': np.random.randint(60, 85),
        'rainfall_forecast': np.random.choice(['No rain', 'Light rain', 'Moderate rain', 'Heavy rain']),
        'wind_speed': np.random.randint(5, 15),
        'uv_index': np.random.randint(6, 10)
    }
    
    # Agricultural insights
    insights = []
    
    if weather_data['temperature'] > 32:
        insights.append("High temperature - ensure adequate irrigation")
    
    if weather_data['humidity'] > 80:
        insights.append("High humidity - monitor for fungal diseases")
    
    if weather_data['rainfall_forecast'] in ['Moderate rain', 'Heavy rain']:
        insights.append("Rain expected - adjust irrigation schedule")
    
    weather_data['agricultural_insights'] = insights
    return weather_data


def format_market_prediction(crop: str, days: int = 7) -> Dict[str, Any]:
    """
    Format market prediction data
    
    Args:
        crop: Crop name
        days: Prediction period
        
    Returns:
        Formatted market prediction
    """
    # Simulated market data
    current_price = np.random.randint(2000, 5000)
    trend = np.random.choice(['bullish', 'bearish', 'stable'])
    
    # Generate price predictions
    dates = [datetime.now() + timedelta(days=i) for i in range(1, days + 1)]
    
    if trend == 'bullish':
        price_change = np.random.normal(50, 20, days)
    elif trend == 'bearish':
        price_change = np.random.normal(-30, 15, days)
    else:
        price_change = np.random.normal(0, 10, days)
    
    predictions = []
    price = current_price
    
    for i, date in enumerate(dates):
        price += price_change[i]
        predictions.append({
            'date': date.strftime('%Y-%m-%d'),
            'predicted_price': round(price),
            'confidence': round(np.random.uniform(0.7, 0.95), 2)
        })
    
    return {
        'crop': crop,
        'current_price': current_price,
        'trend': trend,
        'predictions': predictions,
        'recommendation': get_market_recommendation(trend, current_price)
    }


def get_market_recommendation(trend: str, current_price: float) -> str:
    """
    Get market-based recommendation
    
    Args:
        trend: Market trend
        current_price: Current market price
        
    Returns:
        Recommendation string
    """
    recommendations = {
        'bullish': f"📈 Prices trending upward. Consider holding for better rates. Current price ₹{current_price:.0f} may increase.",
        'bearish': f"📉 Prices declining. Consider selling soon if urgent. Current price ₹{current_price:.0f} may decrease further.",
        'stable': f"📊 Prices stable. Good time to sell at current rate of ₹{current_price:.0f}."
    }
    
    return recommendations.get(trend, "Monitor market closely for best selling opportunity.")


def calculate_fertilizer_recommendation(soil_type: str, crop: str, land_size: float) -> Dict[str, Any]:
    """
    Calculate fertilizer recommendations
    
    Args:
        soil_type: Type of soil
        crop: Crop being grown
        land_size: Size of land in acres
        
    Returns:
        Fertilizer recommendation
    """
    # Simplified fertilizer recommendations
    fertilizer_db = {
        'rice': {'N': 120, 'P': 60, 'K': 40},  # kg per hectare
        'cotton': {'N': 150, 'P': 75, 'K': 50},
        'wheat': {'N': 100, 'P': 50, 'K': 30},
        'maize': {'N': 130, 'P': 65, 'K': 45}
    }
    
    crop_lower = crop.lower()
    if crop_lower not in fertilizer_db:
        crop_lower = 'rice'  # Default
    
    base_npk = fertilizer_db[crop_lower]
    
    # Convert acres to hectares (1 acre = 0.4047 hectares)
    hectares = land_size * 0.4047
    
    # Calculate total fertilizer needed
    total_fertilizer = {
        'nitrogen': base_npk['N'] * hectares,
        'phosphorus': base_npk['P'] * hectares,
        'potassium': base_npk['K'] * hectares
    }
    
    # Commercial fertilizer recommendations
    urea_needed = total_fertilizer['nitrogen'] / 0.46  # Urea is 46% nitrogen
    dap_needed = total_fertilizer['phosphorus'] / 0.46  # DAP is 46% phosphorus
    mop_needed = total_fertilizer['potassium'] / 0.60   # MOP is 60% potassium
    
    return {
        'crop': crop,
        'land_size_hectares': round(hectares, 2),
        'npk_requirements': total_fertilizer,
        'commercial_fertilizers': {
            'urea_kg': round(urea_needed),
            'dap_kg': round(dap_needed),
            'mop_kg': round(mop_needed)
        },
        'application_schedule': [
            "Apply 50% nitrogen at planting",
            "Apply phosphorus and potassium at planting", 
            "Apply remaining nitrogen at flowering stage"
        ],
        'estimated_cost': round((urea_needed * 6) + (dap_needed * 25) + (mop_needed * 17))  # Approximate costs
    }


def generate_irrigation_schedule(crop: str, weather_forecast: Dict, soil_type: str) -> List[Dict]:
    """
    Generate irrigation schedule
    
    Args:
        crop: Crop name
        weather_forecast: Weather forecast data
        soil_type: Soil type
        
    Returns:
        Irrigation schedule
    """
    # Base water requirements (liters per day per plant)
    water_requirements = {
        'rice': 20,
        'cotton': 15,
        'wheat': 10,
        'maize': 12,
        'tomato': 8,
        'onion': 6
    }
    
    base_requirement = water_requirements.get(crop.lower(), 10)
    
    # Soil water retention factor
    soil_factors = {
        'sandy': 0.7,      # Requires more frequent watering
        'clay': 1.3,       # Retains water longer
        'alluvial': 1.0,   # Balanced
        'red_soil': 0.9,   # Slightly less retention
        'black_cotton': 1.2  # Good retention
    }
    
    soil_factor = soil_factors.get(soil_type.lower().replace(' ', '_'), 1.0)
    adjusted_requirement = base_requirement * soil_factor
    
    # Generate 7-day schedule
    schedule = []
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        
        # Adjust for weather (simplified)
        if 'rain' in weather_forecast.get('rainfall_forecast', '').lower():
            water_needed = adjusted_requirement * 0.5  # Reduce if rain expected
            recommendation = "Light irrigation - rain expected"
        else:
            water_needed = adjusted_requirement
            recommendation = "Normal irrigation"
        
        schedule.append({
            'date': date.strftime('%Y-%m-%d'),
            'water_needed_liters_per_plant': round(water_needed),
            'irrigation_time': 'Early morning (6-8 AM)',
            'recommendation': recommendation
        })
    
    return schedule


def save_farmer_feedback(feedback_data: Dict[str, Any]) -> bool:
    """
    Save farmer feedback
    
    Args:
        feedback_data: Feedback information
        
    Returns:
        Success status
    """
    try:
        feedback_dir = Path(__file__).parent.parent.parent / "data" / "feedback"
        feedback_dir.mkdir(parents=True, exist_ok=True)
        
        feedback_file = feedback_dir / f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2, default=str)
        
        logging.info(f"Feedback saved: {feedback_file}")
        return True
        
    except Exception as e:
        logging.error(f"Error saving feedback: {e}")
        return False


def text_to_telugu(text: str) -> str:
    """
    Simple text translation to Telugu (placeholder)
    
    Args:
        text: English text
        
    Returns:
        Telugu text
    """
    # This is a placeholder. In a real implementation,
    # you would use a proper translation API or model
    simple_translations = {
        'hello': 'హలో',
        'farmer': 'రైతు',
        'crop': 'పంట',
        'water': 'నీరు',
        'soil': 'మట్టి',
        'weather': 'వాతావరణం',
        'disease': 'వ్యాధి',
        'price': 'ధర'
    }
    
    words = text.lower().split()
    translated_words = [simple_translations.get(word, word) for word in words]
    return ' '.join(translated_words)


def validate_image_upload(file_path: str) -> bool:
    """
    Validate uploaded image for disease detection
    
    Args:
        file_path: Path to uploaded image
        
    Returns:
        True if valid image
    """
    try:
        from PIL import Image
        
        # Check file exists
        if not os.path.exists(file_path):
            return False
        
        # Check file size (max 10MB)
        if os.path.getsize(file_path) > 10 * 1024 * 1024:
            return False
        
        # Try to open as image
        with Image.open(file_path) as img:
            # Check image dimensions
            if img.width < 100 or img.height < 100:
                return False
            
            # Check format
            if img.format not in ['JPEG', 'PNG', 'JPG']:
                return False
        
        return True
        
    except Exception as e:
        logging.error(f"Image validation error: {e}")
        return False


def format_response_for_language(response: str, language: str) -> str:
    """
    Format response based on selected language
    
    Args:
        response: Original response
        language: Target language
        
    Returns:
        Formatted response
    """
    if language == "Telugu (తెలుగు)":
        # Add Telugu formatting/translation
        return f"🔱 {text_to_telugu(response)}"
    elif language == "Hindi (हिंदी)":
        # Hindi formatting (placeholder)
        return f"🔱 {response}"
    else:
        # English (default)
        return f"🔱 {response}"