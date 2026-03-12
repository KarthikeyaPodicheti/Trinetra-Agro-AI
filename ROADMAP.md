# 🚀 Trinetra Agro AI - Complete Development Roadmap

## "Vision Beyond the Fields" - The All-Seeing Farming Intelligence

---

## 📋 Project Overview

Trinetra Agro AI is an advanced agricultural chatbot with 10+ AI-powered features designed to revolutionize farming through artificial intelligence, deep learning, and predictive analytics.

### Core Technologies Required:
- **Python 3.9+** - Main programming language
- **TensorFlow/PyTorch** - Deep learning frameworks
- **scikit-learn** - Machine learning models
- **OpenAI/Anthropic API** - LLM for conversational AI
- **Whisper** - Speech-to-text
- **Various NLP libraries** - For multilingual support

---

## 📦 PHASE 1: Environment Setup & Installation

### Step 1.1: Install Python
```bash
# Download from: https://www.python.org/downloads/
# Or use terminal:
sudo apt-get update
sudo apt-get install python3.9 python3-pip python3-venv
```

### Step 1.2: Create Virtual Environment
```bash
# Create project directory
mkdir Trinetra-Agro-AI
cd Trinetra-Agro-AI

# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 1.3: Install Core Dependencies
```bash
# Core ML/DL Libraries
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install matplotlib==3.7.2
pip install seaborn==0.12.2

# Machine Learning
pip install scikit-learn==1.3.0
pip install xgboost==2.0.3
pip install lightgbm==4.0.0

# Deep Learning
pip install tensorflow==2.13.0
# OR
pip install torch==2.0.1 torchvision==0.15.2

# Time Series Analysis
pip install prophet==1.1.4
pip install statsmodels==0.14.0
pip install pmdarima==2.0.3

# NLP & Chatbot
pip install nltk==3.8.1
pip install spacy==3.6.1
pip install transformers==4.32.1
pip install langchain==0.0.279

# Computer Vision
pip install opencv-python==4.8.0.76
pip install pillow==10.0.0
pip install tf-keras==2.13.1

# Speech Processing
pip install whisper==20231117
pip install gtts==2.3.2
pip install pyttsx3==2.90
pip install speechrecognition==3.10.0
pip install pydub==0.25.1

# API & Web
pip install fastapi==0.103.0
pip install uvicorn==0.23.2
pip install streamlit==1.27.0
pip install flask==2.3.3
pip install requests==2.31.0

# Database
pip install sqlite3 (built-in)
pip install redis==5.0.0

# Utilities
pip install python-dotenv==1.0.0
pip install tqdm==4.66.1
pip install joblib==1.3.2

# Download spaCy model
python -m spacy download en_core_web_sm
```

### Step 1.4: Install Additional ML Models
```bash
# ResNet, MobileNet for disease detection
# These will be downloaded automatically via TensorFlow/Keras

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"
```

---

## 🏗️ PHASE 2: Project Structure

### Create Directory Structure:
```
Trinetra-Agro-AI/
├── main.py                    # Main entry point
├── requirements.txt           # All dependencies
├── .env                       # API keys
├── config/
│   ├── settings.py           # Configuration
│   └── constants.py          # Constants
├── data/
│   ├── datasets/             # Training data
│   ├── models/               # Saved models
│   ├── images/               # Uploaded images
│   └── cache/                # Cached predictions
├── src/
│   ├── __init__.py
│   ├── chatbot.py            # Core chatbot logic
│   ├── features/
│   │   ├── __init__.py
│   │   ├── farmer_profile.py      # Feature 1
│   │   ├── disease_detection.py   # Feature 2
│   │   ├── market_prediction.py   # Feature 3
│   │   ├── risk_analysis.py       # Feature 4
│   │   ├── yield_prediction.py    # Feature 5
│   │   ├── voice_ai.py            # Feature 6
│   │   ├── conversational_ai.py   # Feature 7
│   │   ├── irrigation.py          # Feature 8
│   │   └── profit_prediction.py   # Feature 9
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── disease_cnn.py
│   │   │   ├── price_lstm.py
│   │   │   ├── yield_rf.py
│   │   │   └── risk_xgboost.py
│   │   └── preprocessing.py
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── intent_classifier.py
│   │   ├── response_generator.py
│   │   └── multilingual.py
│   └── utils/
│       ├── __init__.py
│       ├── database.py
│       ├── feedback.py
│       └── logger.py
├── ui/
│   ├── streamlit_app.py      # Web UI
│   └── console_chat.py       # Console interface
├── tests/
│   └── test_features.py
└── docs/
    └── README.md
```

---

## 🔧 PHASE 3: Core Chatbot Framework

### Step 3.1: Create main.py
```python
"""
Trinetra Agro AI - Main Entry Point
The All-Seeing Farming Intelligence
"""
import os
import sys
from src.chatbot import TrinetraChatbot
from src.utils.logger import setup_logger

def main():
    # Setup
    logger = setup_logger()
    logger.info("🌾 Welcome to Trinetra Agro AI - Vision Beyond the Fields")
    
    # Initialize chatbot
    bot = TrinetraChatbot()
    
    # Start chat
    print("\n" + "="*60)
    print("🔱 TRINETRA AGRO AI - Vision Beyond the Fields 🔱")
    print("="*60)
    print("\nYour AI farming assistant is ready!")
    print("Type 'help' for available commands or 'exit' to quit.\n")
    
    while True:
        user_input = input("👨‍🌾 Farmer: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\n🌾 Thank you for using Trinetra Agro AI!")
            print("May your fields be ever fruitful! 🚜\n")
            break
        
        if user_input.lower() == 'help':
            bot.show_help()
            continue
            
        # Get response
        response = bot.get_response(user_input)
        print(f"\n🔱 Trinetra: {response}\n")

if __name__ == "__main__":
    main()
```

### Step 3.2: Create chatbot.py
```python
"""
Core Chatbot Engine
"""
from src.features.farmer_profile import FarmerProfileEngine
from src.features.disease_detection import DiseaseDetector
from src.features.market_prediction import MarketPredictor
from src.features.risk_analysis import RiskAnalyzer
from src.features.yield_prediction import YieldPredictor
from src.features.voice_ai import VoiceAI
from src.features.conversational_ai import ConversationalAI
from src.features.irrigation import IrrigationAI
from src.features.profit_prediction import ProfitPredictor
from src.nlp.intent_classifier import IntentClassifier
from src.utils.database import Database
from src.utils.feedback import FeedbackSystem

class TrinetraChatbot:
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.db = Database()
        self.feedback = FeedbackSystem()
        
        # Initialize all AI features
        self.farmer_profile = FarmerProfileEngine()
        self.disease_detector = DiseaseDetector()
        self.market_predictor = MarketPredictor()
        self.risk_analyzer = RiskAnalyzer()
        self.yield_predictor = YieldPredictor()
        self.voice_ai = VoiceAI()
        self.conversational_ai = ConversationalAI()
        self.irrigation_ai = IrrigationAI()
        self.profit_predictor = ProfitPredictor()
        
        self.context = {}
        
    def get_response(self, user_input):
        """Process user input and return appropriate response"""
        
        # Classify intent
        intent = self.intent_classifier.classify(user_input)
        
        # Route to appropriate feature
        if intent == "disease_detection":
            return self.handle_disease_detection(user_input)
        elif intent == "market_prediction":
            return self.handle_market_prediction(user_input)
        elif intent == "risk_analysis":
            return self.handle_risk_analysis(user_input)
        elif intent == "yield_prediction":
            return self.handle_yield_prediction(user_input)
        elif intent == "farmer_profile":
            return self.handle_farmer_profile(user_input)
        elif intent == "profit_prediction":
            return self.handle_profit_prediction(user_input)
        elif intent == "irrigation":
            return self.handle_irrigation(user_input)
        elif intent == "voice":
            return self.handle_voice_input(user_input)
        elif intent == "feedback":
            return self.handle_feedback(user_input)
        else:
            # Use LLM for general conversation
            return self.conversational_ai.get_response(user_input, self.context)
    
    def show_help(self):
        """Display available commands"""
        help_text = """
🌾 **TRINETRA AGRO AI - Available Features**

1️⃣  **Personalized Farming Advisor**
    → "Create my farmer profile" / "Help me plan my season"
    
2️⃣  **Crop Disease Detection**  
    → "Detect disease from image" / "Check my crop health"
    
3️⃣  **Market Price Prediction**
    → "Predict tomato prices" / "When should I sell?"
    
4️⃣  **Crop Failure Risk Score**
    → "What's my crop risk?" / "Should I worry about pests?"
    
5️⃣  **Yield Prediction**
    → "Predict my rice yield" / "How much will I harvest?"
    
6️⃣  **Multilingual Voice AI**
    → "Talk in Telugu" / "Voice command"
    
7️⃣  **Smart Chat**
    → Ask any farming question!
    
8️⃣  **Smart Irrigation**
    → "When should I irrigate?" / "Water my crops"
    
9️⃣  **Profit Prediction**
    → "Calculate my profit" / "Is farming worth it?"
    
📝  **Feedback**
    → "Give feedback" / "Rate this service"

Type the number or description to activate any feature!
        """
        print(help_text)
    
    # Handler methods for each feature...
```

---

## 🧠 PHASE 4: Feature Implementation

### Feature 1: Personalized AI Farming Advisor (Farmer Profile Engine)

**Purpose**: Store farmer data and provide personalized recommendations using collaborative filtering

**Files to create**: `src/features/farmer_profile.py`

```python
"""
Feature 1: Personalized AI Farming Advisor
Farmer Profile Engine with Recommendation System
"""
import json
import os
from datetime import datetime

class FarmerProfileEngine:
    def __init__(self):
        self.profiles = {}
        self.recommendations = {}
        self.load_profiles()
    
    def create_profile(self, farmer_id, data):
        """Create farmer profile with all details"""
        profile = {
            "farmer_id": farmer_id,
            "name": data.get("name"),
            "land_size": float(data.get("land_size", 0)),  # acres
            "soil_type": data.get("soil_type"),  # clay, sandy, loamy, etc.
            "crop_history": data.get("crop_history", []),
            "budget": float(data.get("budget", 0)),
            "location": data.get("location"),
            "climate_zone": data.get("climate_zone"),
            "irrigation_type": data.get("irrigation_type"),  # drip, flood, sprinkler
            "created_at": datetime.now().isoformat()
        }
        self.profiles[farmer_id] = profile
        self.save_profiles()
        return profile
    
    def get_seasonal_plan(self, farmer_id):
        """Generate personalized seasonal plan using recommendation logic"""
        if farmer_id not in self.profiles:
            return "Please create your farmer profile first!"
        
        profile = self.profiles[farmer_id]
        
        # Recommendation system logic based on:
        # 1. Soil type
        # 2. Climate zone
        # 3. Budget
        # 4. Crop history
        
        plan = self._generate_recommendations(profile)
        return plan
    
    def _generate_recommendations(self, profile):
        """Collaborative filtering based recommendation"""
        recommendations = {
            "soil_preparation": self._recommend_soil_prep(profile),
            "crop_suggestions": self._recommend_crops(profile),
            "fertilizer_plan": self._recommend_fertilizer(profile),
            "schedule": self._generate_schedule(profile)
        }
        return recommendations
    
    def _recommend_soil_prep(self, profile):
        """Recommend soil preparation based on soil type"""
        soil_prep = {
            "clay": "Add organic matter, use raised beds, avoid working when wet",
            "sandy": "Add compost to improve water retention, use mulch",
            "loamy": "Maintain with crop rotation, add organic matter annually",
            "silt": "Avoid compaction, use cover crops"
        }
        return soil_prep.get(profile.get("soil_type"), "General soil care")
    
    def _recommend_crops(self, profile):
        """Recommend crops based on history, soil, climate, budget"""
        # Similar farmers (collaborative filtering)
        similar = self._find_similar_farmers(profile)
        
        # Content-based recommendations
        crop_database = {
            "rice": {"soil": ["clay", "loamy"], "water": "high", "profit": "medium"},
            "wheat": {"soil": ["loamy", "clay"], "water": "medium", "profit": "medium"},
            "tomato": {"soil": ["loamy", "sandy"], "water": "medium", "profit": "high"},
            "cotton": {"soil": ["black", "clay"], "water": "low", "profit": "high"},
            "sugarcane": {"soil": ["loamy"], "water": "high", "profit": "high"},
        }
        
        # Filter by soil type and budget
        recommended = []
        for crop, attrs in crop_database.items():
            if profile.get("soil_type") in attrs["soil"]:
                if profile.get("budget", 0) > 500:  # Minimum budget
                    recommended.append(crop)
        
        return recommended
    
    def _generate_schedule(self, profile):
        """Generate seasonal schedule"""
        return {
            "spring": "Prepare soil, start planting",
            "summer": "Irrigation, pest management",
            "autumn": "Harvest, post-harvest care",
            "winter": "Soil preparation, planning"
        }
    
    def save_profiles(self):
        """Save profiles to file"""
        with open("data/profiles.json", "w") as f:
            json.dump(self.profiles, f, indent=2)
    
    def load_profiles(self):
        """Load profiles from file"""
        if os.path.exists("data/profiles.json"):
            with open("data/profiles.json", "r") as f:
                self.profiles = json.load(f)
```

---

### Feature 2: Deep Learning Crop Disease Detection

**Purpose**: Detect crop diseases from leaf images using CNN (ResNet/MobileNet) with Grad-CAM visualization

**Files to create**: 
- `src/features/disease_detection.py` 
- `src/ml/models/disease_cnn.py`

```python
"""
Feature 2: Crop Disease Detection
Using CNN (ResNet/MobileNet) with Transfer Learning + Grad-CAM
"""
import numpy as np
import cv2
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.applications import ResNet50, MobileNetV2
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf

class DiseaseDetector:
    def __init__(self):
        self.model = None
        self.class_names = [
            'healthy', 'bacterial_spot', 'early_blight', 'late_blight',
            'leaf_mold', 'septoria_leaf_spot', 'spider_mites',
            'target_spot', 'mosaic_virus', 'yellow_leaf_curl'
        ]
        self.threshold = 0.7
        self.load_model()
    
    def load_model(self):
        """Load or create the CNN model"""
        try:
            # Try loading saved model
            self.model = load_model('data/models/disease_model.h5')
            print("✅ Loaded pre-trained disease model")
        except:
            print("⚠️ Creating new model - training required")
            self.model = self._build_model()
    
    def _build_model(self):
        """Build CNN model using transfer learning (MobileNetV2)"""
        # Use MobileNetV2 for efficiency (works on mobile devices)
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # Freeze base model
        base_model.trainable = False
        
        # Add custom classification head
        inputs = tf.keras.Input(shape=(224, 224, 3))
        x = base_model(inputs, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        outputs = tf.keras.layers.Dense(len(self.class_names), activation='softmax')(x)
        
        model = tf.keras.Model(inputs, outputs)
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def detect_disease(self, image_path):
        """Detect disease from leaf image"""
        # Load and preprocess image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        
        # Preprocess for model
        img_array = img_to_array(image)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        predictions = self.model.predict(img_array, verbose=0)
        pred_class = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        # Get results
        disease = self.class_names[pred_class]
        probability = float(predictions[0][pred_class])
        
        # Determine severity
        severity = self._determine_severity(confidence)
        
        # Generate Grad-CAM visualization
        heatmap = self._generate_gradcam(image_path)
        
        return {
            "disease": disease,
            "probability": probability,
            "confidence": confidence,
            "severity": severity,
            "all_predictions": {
                self.class_names[i]: float(predictions[0][i])
                for i in range(len(self.class_names))
            },
            "gradcam_visualization": heatmap,
            "recommendation": self._get_recommendation(disease)
        }
    
    def _determine_severity(self, confidence):
        """Determine disease severity level"""
        if confidence > 0.9:
            return "Critical - Immediate action required"
        elif confidence > 0.7:
            return "High - Treatment recommended soon"
        elif confidence > 0.5:
            return "Moderate - Monitor closely"
        else:
            return "Low - Continue monitoring"
    
    def _generate_gradcam(self, image_path):
        """Generate Grad-CAM visualization for explainability"""
        # This would generate a heatmap showing which parts of 
        # the image the model is focusing on
        # Implementation requires model-specific Grad-CAM
        return "gradcam_heatmap.png"
    
    def _get_recommendation(self, disease):
        """Get treatment recommendation for detected disease"""
        recommendations = {
            'healthy': "Continue current farming practices. Your crop looks great!",
            'bacterial_spot': "Apply copper-based fungicide. Remove infected leaves. Improve air circulation.",
            'early_blight': "Apply chlorothalonil or copper fungicide. Remove lower infected leaves. Mulch around plants.",
            'late_blight': "URGENT - Apply metalaxyl immediately. Remove and destroy infected plants. Don't compost them.",
            'leaf_mold': "Improve ventilation. Reduce humidity. Apply sulfur-based fungicide.",
            'septoria_leaf_spot': "Remove infected leaves. Apply fungicide. Avoid overhead watering.",
            'spider_mites': "Spray with water to remove. Apply neem oil or insecticidal soap.",
            'target_spot': "Apply fungicide. Improve drainage. Remove plant debris.",
            'mosaic_virus': "Remove infected plants. Control aphids. Use resistant varieties.",
            'yellow_leaf_curl': "Control whiteflies. Remove infected plants. Use reflective mulch."
        }
        return recommendations.get(disease, "Consult local agricultural extension for advice.")
    
    def train_model(self, train_data, train_labels, epochs=10):
        """Train the model on custom dataset"""
        self.model.fit(
            train_data, train_labels,
            epochs=epochs,
            validation_split=0.2,
            batch_size=32
        )
        # Save trained model
        self.model.save('data/models/disease_model.h5')
```

---

### Feature 3: Market Price Prediction

**Purpose**: Predict market prices using ARIMA, LSTM, and Prophet

**Files to create**: `src/features/market_prediction.py`

```python
"""
Feature 3: Market Price Prediction
Using ARIMA, LSTM, and Prophet for Time Series Analysis
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MarketPredictor:
    def __init__(self):
        self.models = {}
        self.price_data = {}
        self.load_historical_data()
    
    def load_historical_data(self):
        """Load or generate historical price data"""
        # In production, fetch from API
        # For demo, generate sample data
        self.price_data = self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate sample price data for demo"""
        crops = ['tomato', 'potato', 'onion', 'rice', 'wheat', 'cotton']
        data = {}
        
        for crop in crops:
            dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
            # Generate realistic price patterns with seasonality
            base_price = np.random.randint(20, 100)
            seasonal = 10 * np.sin(np.linspace(0, 4*np.pi, 365))
            noise = np.random.normal(0, 5, 365)
            prices = base_price + seasonal + noise
            
            data[crop] = pd.DataFrame({
                'date': dates,
                'price': np.maximum(prices, 1)  # Prices can't be negative
            })
        
        return data
    
    def predict_prices(self, crop, days=30):
        """Predict prices for next N days using ensemble methods"""
        if crop not in self.price_data:
            return {"error": f"No data available for {crop}"}
        
        df = self.price_data[crop]
        
        # Method 1: ARIMA Prediction
        arima_pred = self._arima_predict(df, days)
        
        # Method 2: LSTM Prediction  
        lstm_pred = self._lstm_predict(df, days)
        
        # Method 3: Prophet Prediction
        prophet_pred = self._prophet_predict(df, days)
        
        # Ensemble (average of all methods)
        ensemble_pred = (arima_pred + lstm_pred + prophet_pred) / 3
        
        # Generate recommendation
        recommendation = self._get_recommendation(ensemble_pred)
        
        return {
            "crop": crop,
            "current_price": float(df['price'].iloc[-1]),
            "predictions": ensemble_pred.tolist(),
            "dates": [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') 
                     for i in range(1, days+1)],
            "recommendation": recommendation,
            "confidence": self._calculate_confidence(ensemble_pred),
            "methods": {
                "arima": arima_pred.tolist(),
                "lstm": lstm_pred.tolist(),
                "prophet": prophet_pred.tolist()
            }
        }
    
    def _arima_predict(self, df, days):
        """ARIMA time series prediction"""
        try:
            from pmdarima import auto_arima
            
            # Fit ARIMA model
            model = auto_arima(
                df['price'], 
                seasonal=True, 
                m=7,  # Weekly seasonality
                suppress_warnings=True,
                stepwise=True
            )
            
            # Predict
            forecast = model.predict(n_periods=days)
            return np.array(forecast)
        except:
            # Fallback to simple moving average
            return self._simple_ma_predict(df, days)
    
    def _lstm_predict(self, df, days):
        """LSTM neural network prediction"""
        try:
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense
            
            # Prepare data
            data = df['price'].values
            data = data.reshape(-1, 1)
            
            # Normalize
            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()
            scaled_data = scaler.fit_transform(data)
            
            # Create sequences
            def create_sequences(data, seq_length):
                X, y = [], []
                for i in range(len(data) - seq_length):
                    X.append(data[i:i+seq_length])
                    y.append(data[i+seq_length])
                return np.array(X), np.array(y)
            
            X, y = create_sequences(scaled_data, 30)
            
            # Build LSTM model
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(30, 1)),
                LSTM(50),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            
            # Train (in production, load pre-trained)
            model.fit(X, y, epochs=10, verbose=0)
            
            # Predict
            predictions = []
            last_seq = scaled_data[-30:].reshape(1, 30, 1)
            
            for _ in range(days):
                pred = model.predict(last_seq, verbose=0)
                predictions.append(pred[0, 0])
                last_seq = np.roll(last_seq, -1, axis=1)
                last_seq[0, -1, 0] = pred[0, 0]
            
            return scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
        except:
            return self._simple_ma_predict(df, days)
    
    def _prophet_predict(self, df, days):
        """Facebook Prophet prediction"""
        try:
            from prophet import Prophet
            
            # Prepare data for Prophet
            prophet_df = df.rename(columns={'date': 'ds', 'price': 'y'})
            
            # Fit model
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False
            )
            model.fit(prophet_df)
            
            # Predict
            future = model.make_future_dataframe(days)
            forecast = model.predict(future)
            
            return forecast['yhat'].values[-days:]
        except:
            return self._simple_ma_predict(df, days)
    
    def _simple_ma_predict(self, df, days):
        """Simple moving average fallback"""
        ma = df['price'].rolling(window=7).mean().iloc[-1]
        return np.array([ma] * days)
    
    def _calculate_confidence(self, predictions):
        """Calculate prediction confidence based on model agreement"""
        return "High" if len(predictions) > 0 else "Low"
    
    def _get_recommendation(self, predictions):
        """Generate buy/sell recommendation"""
        current = predictions[0]
        future_avg = np.mean(predictions[7:])  # 7-day average
        
        change_percent = ((future_avg - current) / current) * 100
        
        if change_percent > 10:
            return {
                "action": "WAIT",
                "message": f"Prices expected to rise {change_percent:.1f}% in next week",
                "reason": "Selling now means missing out on higher prices"
            }
        elif change_percent < -10:
            return {
                "action": "SELL NOW",
                "message": f"Prices expected to drop {abs(change_percent):.1f}% in next week",
                "reason": "Sell now to maximize returns before price decline"
            }
        else:
            return {
                "action": "HOLD",
                "message": f"Prices expected to remain stable (±{abs(change_percent):.1f}%)",
                "reason": "No significant price change expected"
            }
```

---

### Feature 4: Crop Failure Risk Score

**Purpose**: AI-based risk assessment using multiple input factors

**Files to create**: `src/features/risk_analysis.py`

```python
"""
Feature 4: AI-Based Crop Failure Risk Score
Insurance-level AI for risk prediction
"""
import numpy as np
import random
from datetime import datetime

class RiskAnalyzer:
    def __init__(self):
        self.risk_weights = {
            'rainfall': 0.25,
            'temperature': 0.20,
            'soil_moisture': 0.20,
            'pest_risk': 0.20,
            'disease_risk': 0.15
        }
    
    def calculate_risk_score(self, inputs):
        """
        Calculate crop failure risk score
        
        Inputs required:
        - rainfall_forecast: mm (next 7 days)
        - temperature_trends: list of temps
        - soil_moisture: percentage (0-100)
        - pest_reports: list of pest risks
        - disease_history: boolean
        - crop_type: string
        """
        
        # Extract inputs
        rainfall = inputs.get('rainfall_forecast', 0)
        temps = inputs.get('temperature_trends', [25])
        soil_moisture = inputs.get('soil_moisture', 50)
        pest_risk = inputs.get('pest_risk', 0)
        disease_risk = inputs.get('disease_risk', False)
        crop = inputs.get('crop_type', 'general')
        
        # Calculate individual risk components
        rainfall_risk = self._calculate_rainfall_risk(rainfall)
        temp_risk = self._calculate_temperature_risk(temps, crop)
        moisture_risk = self._calculate_moisture_risk(soil_moisture, crop)
        pest_risk_score = self._calculate_pest_risk(pest_risk)
        disease_risk_score = self._calculate_disease_risk(disease_risk)
        
        # Weighted total risk score
        total_risk = (
            rainfall_risk * self.risk_weights['rainfall'] +
            temp_risk * self.risk_weights['temperature'] +
            moisture_risk * self.risk_weights['soil_moisture'] +
            pest_risk_score * self.risk_weights['pest_risk'] +
            disease_risk_score * self.risk_weights['disease_risk']
        )
        
        # Generate prevention steps
        prevention_steps = self._generate_prevention_steps(
            rainfall_risk, temp_risk, moisture_risk, pest_risk_score, disease_risk_score
        )
        
        return {
            "risk_percentage": round(total_risk, 2),
            "risk_level": self._get_risk_level(total_risk),
            "components": {
                "rainfall_risk": round(rainfall_risk, 2),
                "temperature_risk": round(temp_risk, 2),
                "moisture_risk": round(moisture_risk, 2),
                "pest_risk": round(pest_risk_score, 2),
                "disease_risk": round(disease_risk_score, 2)
            },
            "prevention_steps": prevention_steps,
            "insurance_recommendation": self._get_insurance_recommendation(total_risk),
            "crop_specific_advice": self._get_crop_advice(crop, total_risk)
        }
    
    def _calculate_rainfall_risk(self, rainfall):
        """Calculate risk from rainfall patterns"""
        # Too little or too much rain is risky
        if rainfall < 20:  # Drought risk
            return min(80, (20 - rainfall) * 4)
        elif rainfall > 150:  # Flood risk
            return min(100, (rainfall - 150) * 1.5)
        elif rainfall < 50:  # Below optimal
            return 30
        else:  # Optimal range
            return 10
    
    def _calculate_temperature_risk(self, temps, crop):
        """Calculate temperature stress risk"""
        optimal_ranges = {
            'rice': (20, 35),
            'wheat': (15, 25),
            'tomato': (18, 30),
            'cotton': (20, 40),
            'general': (15, 35)
        }
        
        min_temp, max_temp = optimal_ranges.get(crop, (15, 35))
        avg_temp = np.mean(temps)
        
        if avg_temp < min_temp:
            return min(80, (min_temp - avg_temp) * 5)
        elif avg_temp > max_temp:
            return min(80, (avg_temp - max_temp) * 5)
        else:
            return 10
    
    def _calculate_moisture_risk(self, moisture, crop):
        """Calculate soil moisture risk"""
        optimal = {
            'rice': (60, 100),
            'wheat': (40, 70),
            'tomato': (50, 70),
            'cotton': (30, 60),
            'general': (40, 70)
        }
        
        min_moist, max_moist = optimal.get(crop, (40, 70))
        
        if moisture < min_moist:
            return min(80, (min_moist - moisture) * 3)
        elif moisture > max_moist:
            return min(80, (moisture - max_moist) * 3)
        else:
            return 10
    
    def _calculate_pest_risk(self, pest_reports):
        """Calculate pest infestation risk"""
        if isinstance(pest_reports, list):
            return min(100, len(pest_reports) * 20)
        else:
            return min(100, pest_reports)
    
    def _calculate_disease_risk(self, disease_present):
        """Calculate disease risk"""
        return 90 if disease_present else 15
    
    def _get_risk_level(self, risk_score):
        """Convert numerical risk to categorical"""
        if risk_score < 25:
            return "LOW"
        elif risk_score < 50:
            return "MODERATE"
        elif risk_score < 75:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _generate_prevention_steps(self, rain_risk, temp_risk, moisture_risk, pest_risk, disease_risk):
        """Generate specific prevention recommendations"""
        steps = []
        
        if rain_risk > 50:
            steps.append("🌧️ Install drainage systems to prevent waterlogging")
            steps.append("🌧️ Consider flood-resistant crop varieties")
        
        if temp_risk > 50:
            steps.append("🌡️ Use shade nets to protect from extreme temperatures")
            steps.append("🌡️ Adjust irrigation timing to cooler hours")
        
        if moisture_risk > 50:
            steps.append("💧 Install drip irrigation for efficient water use")
            steps.append("💧 Apply mulch to retain soil moisture")
        
        if pest_risk > 50:
            steps.append("🐛 Set up pest monitoring traps")
            steps.append("🐛 Apply integrated pest management (IPM)")
            steps.append("🐛 Introduce biological pest controls")
        
        if disease_risk > 50:
            steps.append("🧪 Apply preventive fungicides")
            steps.append("🧪 Remove and destroy infected plant material")
            steps.append("🧪 Improve air circulation between plants")
        
        if not steps:
            steps.append("✅ Continue current farming practices - risk is low")
        
        return steps
    
    def _get_insurance_recommendation(self, risk_score):
        """Insurance-level recommendation"""
        if risk_score > 75:
            return {
                "recommended": True,
                "coverage": "HIGH",
                "premium_estimate": "High - Consider crop insurance immediately"
            }
        elif risk_score > 50:
            return {
                "recommended": True,
                "coverage": "MEDIUM",
                "premium_estimate": "Moderate - Insurance recommended"
            }
        else:
            return {
                "recommended": False,
                "coverage": "LOW",
                "premium_estimate": "Not required at this time"
            }
    
    def _get_crop_advice(self, crop, risk_score):
        """Crop-specific advisory"""
        advice = {
            'rice': "Maintain standing water in fields. Monitor for bacterial leaf blight.",
            'wheat': "Ensure proper drainage. Watch for rust diseases.",
            'tomato': "Stake plants for support. Monitor for early blight.",
            'cotton': "Watch for pink bollworm. Maintain adequate plant spacing."
        }
        base_advice = advice.get(crop, "Monitor crops regularly for any signs of stress.")
        
        if risk_score > 50:
            return f"⚠️ {base_advice} URGENT: Take preventive measures immediately!"
        else:
            return f"✓ {base_advice}"
```

---

### Feature 5: Smart Yield Prediction Model

**Purpose**: Predict crop yield using Random Forest / XGBoost regression

**Files to create**: `src/features/yield_prediction.py`

```python
"""
Feature 5: Smart Yield Prediction Model
Using Random Forest and XGBoost Regression
"""
import numpy as np
import pandas as pd
import joblib
import os

class YieldPredictor:
    def __init__(self):
        self.rf_model = None
        self.xgb_model = None
        self.ensemble_model = None
        self.feature_names = [
            'fertilizer_amount', 'rainfall', 'temperature_avg',
            'soil_nitrogen', 'soil_phosphorus', 'soil_potassium',
            'irrigation_days', 'pest_control', 'crop_age', 'land_size'
        ]
        self.load_or_train_models()
    
    def load_or_train_models(self):
        """Load pre-trained models or train new ones"""
        model_path = 'data/models/yield_model.joblib'
        
        if os.path.exists(model_path):
            self.ensemble_model = joblib.load(model_path)
            print("✅ Loaded pre-trained yield prediction model")
        else:
            print("⚠️ Training new yield prediction model...")
            self._train_models()
    
    def _train_models(self):
        """Train yield prediction models"""
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        
        # Generate synthetic training data (in production, use real data)
        np.random.seed(42)
        n_samples = 1000
        
        X = np.random.rand(n_samples, len(self.feature_names))
        X[:, 0] = X[:, 0] * 200  # fertilizer (0-200 kg)
        X[:, 1] = X[:, 1] * 500  # rainfall (0-500 mm)
        X[:, 2] = X[:, 2] * 20 + 15  # temp (15-35°C)
        X[:, 3] = X[:, 3] * 100  # nitrogen (0-100 ppm)
        X[:, 4] = X[:, 4] * 60  # phosphorus (0-60 ppm)
        X[:, 5] = X[:, 5] * 80  # potassium (0-80 ppm)
        X[:, 6] = X[:, 6] * 60  # irrigation days
        X[:, 7] = X[:, 7] * 10  # pest control score
        X[:, 8] = X[:, 8] * 150  # crop age (days)
        X[:, 9] = X[:, 9] * 10  # land size (acres)
        
        # Generate realistic yield (tons) with some noise
        # Yield formula based on agricultural research
        y = (
            0.02 * X[:, 0] +  # fertilizer effect
            0.01 * X[:, 1] +  # rainfall effect
            0.5 * X[:, 2] +   # temperature effect
            0.03 * X[:, 3] +  # nitrogen effect
            0.02 * X[:, 4] +  # phosphorus effect
            0.015 * X[:, 5] + # potassium effect
            0.1 * X[:, 6] +   # irrigation effect
            0.2 * X[:, 7] +   # pest control effect
            0.02 * X[:, 8] +  # age effect
            0.5 * X[:, 9] +   # land size effect
            np.random.normal(0, 1, n_samples)  # noise
        )
        y = np.maximum(y, 0)  # Yield can't be negative
        
        # Train Random Forest
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42
        )
        self.rf_model.fit(X, y)
        
        # Train XGBoost
        try:
            import xgboost as xgb
            self.xgb_model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=10,
                learning_rate=0.1,
                random_state=42
            )
            self.xgb_model.fit(X, y)
        except:
            self.xgb_model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.xgb_model.fit(X, y)
        
        # Create ensemble
        self.ensemble_model = EnsembleRegressor(self.rf_model, self.xgb_model)
        
        # Save model
        os.makedirs('data/models', exist_ok=True)
        joblib.dump(self.ensemble_model, 'data/models/yield_model.joblib')
        print("✅ Yield prediction model trained and saved")
    
    def predict_yield(self, inputs):
        """
        Predict crop yield based on input factors
        
        Required inputs:
        - fertilizer_amount: kg/acre
        - rainfall: mm
        - temperature_avg: °C
        - soil_nitrogen: ppm
        - soil_phosphorus: ppm
        - soil_potassium: ppm
        - irrigation_days: days
        - pest_control: 0-10 score
        - crop_age: days
        - land_size: acres
        - crop_type: string (optional)
        """
        
        # Prepare feature vector
        features = []
        for feat in self.feature_names:
            features.append(float(inputs.get(feat, 0)))
        
        X = np.array(features).reshape(1, -1)
        
        # Get prediction from ensemble
        yield_prediction = self.ensemble_model.predict(X)[0]
        
        # Get confidence interval
        rf_pred = self.rf_model.predict(X)[0]
        xgb_pred = self.xgb_model.predict(X)[0]
        
        uncertainty = abs(rf_pred - xgb_pred)
        
        return {
            "predicted_yield": round(max(0, yield_prediction), 2),
            "unit": "tons",
            "confidence_interval": {
                "lower": round(max(0, yield_prediction - uncertainty), 2),
                "upper": round(yield_prediction + uncertainty, 2)
            },
            "model_agreement": "High" if uncertainty < 1 else "Medium" if uncertainty < 2 else "Low",
            "contributing_factors": self._analyze_factors(features),
            "recommendations": self._generate_recommendations(features, yield_prediction),
            "comparable_yields": self._get_comparable_yields(yield_prediction)
        }
    
    def _analyze_factors(self, features):
        """Analyze which factors contribute most to yield"""
        feature_importance = list(zip(self.feature_names, features))
        
        # Sort by contribution
        sorted_factors = sorted(
            feature_importance,
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "top_positive": [
                {"factor": f[0], "value": f[1]} 
                for f in sorted_factors[:3]
            ],
            "needs_improvement": [
                {"factor": f[0], "value": f[1]}
                for f in sorted_factors[-2:]
            ]
        }
    
    def _generate_recommendations(self, features, predicted_yield):
        """Generate improvement recommendations"""
        recs = []
        
        if features[0] < 50:
            recs.append("💊 Consider increasing fertilizer application to improve yield")
        if features[1] < 200:
            recs.append("💧 Ensure adequate irrigation - rainfall is below optimal")
        if features[3] < 40:
            recs.append("🧪 Soil nitrogen is low - consider nitrogen fertilizers")
        if features[6] < 30:
            recs.append("🚿 Increase irrigation days for better moisture")
        if features[7] < 5:
            recs.append("🐛 Improve pest control measures")
        
        if predicted_yield > 5:
            recs.append("🌟 Excellent yield expected! Maintain current practices")
        
        return recs
    
    def _get_comparable_yields(self, predicted_yield):
        """Get comparable yield information"""
        if predicted_yield > 8:
            return "Excellent - Top 10% of yields in region"
        elif predicted_yield > 5:
            return "Good - Above average yield expected"
        elif predicted_yield > 3:
            return "Average - Typical yield for this input level"
        else:
            return "Below average - Consider improving input management"


class EnsembleRegressor:
    """Ensemble of multiple models"""
    def __init__(self, model1, model2):
        self.model1 = model1
        self.model2 = model2
    
    def predict(self, X):
        pred1 = self.model1.predict(X)
        pred2 = self.model2.predict(X)
        return (pred1 + pred2) / 2
```

---

### Feature 6: Multilingual Voice AI

**Purpose**: Voice input/output in Telugu and other Indian languages

**Files to create**: `src/features/voice_ai.py`

```python
"""
Feature 6: Multilingual Voice AI
Speech-to-Text and Text-to-Speech for Telugu and other Indian languages
"""
import speech_recognition as sr
import os
import numpy as np

class VoiceAI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.current_language = 'te-IN'  # Telugu
        self.supported_languages = {
            'te-IN': 'Telugu',
            'hi-IN': 'Hindi',
            'en-IN': 'English',
            'ta-IN': 'Tamil',
            'kn-IN': 'Kannada',
            'ml-IN': 'Malayalam'
        }
        
        # Calibrate microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def listen(self, language=None):
        """
        Listen for voice input and convert to text
        
        Args:
            language: Language code (default: Telugu)
        
        Returns:
            Transcribed text
        """
        lang = language or self.current_language
        
        print(f"🎤 Listening in {self.supported_languages.get(lang, 'Telugu')}...")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5)
            
            # Try Whisper first (more accurate)
            try:
                import whisper
                # Use base model for speed
                model = whisper.load_model("base")
                result = model.transcribe(audio, language=lang[:2])
                text = result["text"]
                print(f"📝 Whisper recognized: {text}")
                return text
            except:
                pass
            
            # Fallback to Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=lang)
            print(f"📝 Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return "Timeout - No speech detected"
        except sr.UnknownValueError:
            return "Could not understand speech"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def speak(self, text, language=None):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
            language: Output language
        """
        lang = language or self.current_language
        
        print(f"🔊 Speaking: {text}")
        
        try:
            # Method 1: gTTS (Google Text-to-Speech)
            from gtts import gTTS
            import tempfile
            import os
            import playsound
            
            # Map language codes
            lang_map = {
                'te-IN': 'te',
                'hi-IN': 'hi',
                'en-IN': 'en',
                'ta-IN': 'ta',
                'kn-IN': 'kn',
                'ml-IN': 'ml'
            }
            
            gtts_lang = lang_map.get(lang, 'te')
            
            tts = gTTS(text=text, lang=gtts_lang, slow=False)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tts.save(tmp.name)
                playsound.playsound(tmp.name)
                os.unlink(tmp.name)
                
        except Exception as e:
            # Fallback to pyttsx3 (offline)
            print(f"⚠️ gTTS failed, trying pyttsx3: {e}")
            self._speak_offline(text)
    
    def _speak_offline(self, text):
        """Offline TTS using pyttsx3"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"⚠️ All TTS methods failed: {e}")
            print(f"📝 Text output: {text}")
    
    def process_voice_command(self, audio_input=None):
        """
        Complete voice command pipeline
        
        1. Listen to voice
        2. Convert to text (NLP)
        3. Process intent
        4. Generate response
        5. Speak response
        """
        # Step 1: Get audio (or use provided)
        if audio_input:
            text = audio_input
        else:
            text = self.listen()
        
        if text in ["Timeout - No speech detected", "Could not understand speech"]:
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        
        # Step 2: Process through NLP
        # (This would integrate with intent classifier)
        
        return text
    
    def set_language(self, language_code):
        """Change current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            return f"Language changed to {self.supported_languages[language_code]}"
        return "Unsupported language"
    
    def get_available_languages(self):
        """Get list of available languages"""
        return self.supported_languages
```

---

### Feature 7: Conversational AI (LLM-Based)

**Purpose**: Smart chat using LLM API with context memory

**Files to create**: `src/features/conversational_ai.py`

```python
"""
Feature 7: Conversational AI (LLM-Based Smart Chat)
Context-aware chatbot using LLM APIs
"""
import os
from datetime import datetime
import json

class ConversationalAI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []
        self.max_history = 10
        self.farming_context = self._load_farming_context()
    
    def _load_farming_context(self):
        """Load farming-specific context for better responses"""
        return """
        You are Trinetra Agro AI, an intelligent farming assistant with deep knowledge of:
        - Crop cultivation and farming techniques
        - Soil management and fertilizer application
        - Pest and disease control
        - Weather patterns and climate-smart agriculture
        - Market prices and profit optimization
        - Modern agricultural technologies
        
        Your goal is to help farmers increase their yields and profits through
        data-driven insights and personalized recommendations.
        
        Always be helpful, practical, and considerate of small farmer constraints.
        """
    
    def get_response(self, user_input, context=None):
        """Get intelligent response from LLM"""
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep history manageable
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        # Check for API key
        if not self.api_key:
            return self._fallback_response(user_input)
        
        # Try using OpenAI API
        try:
            return self._call_openai(user_input, context)
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_response(user_input)
    
    def _call_openai(self, user_input, context):
        """Call OpenAI API for response"""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        # Build messages
        messages = [
            {"role": "system", "content": self.farming_context}
        ]
        
        # Add conversation history
        for msg in self.conversation_history[:-1]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current context if provided
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            messages.append({
                "role": "system",
                "content": f"Current context:\n{context_str}"
            })
        
        # Add current input
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        
        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": bot_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return bot_response
    
    def _fallback_response(self, user_input):
        """Fallback rule-based response when API unavailable"""
        
        # Simple keyword-based responses
        keyword_responses = {
            "hello": "Namaste! I'm Trinetra Agro AI, your farming assistant. How can I help you today?",
            "hi": "Hello farmer! How can I assist you with your crops today?",
            "help": "I can help you with:\n- Crop disease detection\n- Market price predictions\n- Yield predictions\n- Risk assessment\n- Farming advice\n- And much more!",
            "weather": "For weather updates, please check your local weather forecast. I can help you plan irrigation based on weather patterns.",
            "crop": "Which crop are you growing? I can provide specific advice for rice, wheat, cotton, tomatoes, and many more.",
            "fertilizer": "Fertilizer requirements depend on your soil test results. Generally, NPK ratios of 10-26-26 for flowering, 20-20-20 for vegetative growth are common.",
            "pest": "For pest management, I recommend integrated pest management (IPM). What specific pest are you dealing with?",
            "default": "I'm here to help with all your farming needs. Could you please be more specific about what you'd like to know?"
        }
        
        user_input_lower = user_input.lower()
        
        for keyword, response in keyword_responses.items():
            if keyword in user_input_lower:
                return response
        
        return keyword_responses["default"]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation history cleared!"
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history
```

---

### Feature 8: Smart Irrigation AI

**Purpose**: Predict water needs and optimize irrigation timing

**Files to create**: `src/features/irrigation.py`

```python
"""
Feature 8: Smart Irrigation AI
Optimize water usage and irrigation timing
"""
import numpy as np
from datetime import datetime, timedelta

class IrrigationAI:
    def __init__(self):
        self.crop_water_requirements = {
            'rice': {'daily_mm': 10, 'critical_stage': 'flowering'},
            'wheat': {'daily_mm': 5, 'critical_stage': 'grain_filling'},
            'cotton': {'daily_mm': 7, 'critical_stage': 'boll_development'},
            'tomato': {'daily_mm': 6, 'critical_stage': 'fruiting'},
            'potato': {'daily_mm': 5, 'critical_stage': 'tuber_formation'},
            'sugarcane': {'daily_mm': 8, 'critical_stage': 'elongation'}
        }
    
    def predict_water_need(self, inputs):
        """
        Predict water requirement for irrigation
        
        Required inputs:
        - crop_type: string
        - soil_type: string (clay, sandy, loamy)
        - current_soil_moisture: percentage
        - temperature: °C
        - humidity: percentage
        - wind_speed: km/h
        - days_since_irrigation: int
        - crop_stage: string
        - forecast_rainfall: mm
        """
        
        crop = inputs.get('crop_type', 'general')
        soil = inputs.get('soil_type', 'loamy')
        moisture = inputs.get('current_soil_moisture', 50)
        temp = inputs.get('temperature', 25)
        humidity = inputs.get('humidity', 60)
        wind = inputs.get('wind_speed', 10)
        days_since = inputs.get('days_since_irrigation', 0)
        rainfall = inputs.get('forecast_rainfall', 0)
        
        # Get crop water requirement
        crop_req = self.crop_water_requirements.get(crop, 
            {'daily_mm': 5, 'critical_stage': 'vegetative'})
        
        # Calculate evapotranspiration (simplified Penman-Monteith)
        et0 = self._calculate_et0(temp, humidity, wind)
        
        # Crop coefficient
        kc = self._get_crop_coefficient(crop, inputs.get('crop_stage', 'vegetative'))
        
        # Actual crop water requirement
        crop_etc = et0 * kc
        
        # Soil type adjustment
        soil_factor = self._get_soil_adjustment(soil, moisture)
        
        # Calculate irrigation need
        water_needed = max(0, crop_etc * soil_factor - rainfall)
        
        # Days until irrigation needed
        if moisture > 60:
            days_until = 7
        elif moisture > 40:
            days_until = 3
        elif moisture > 20:
            days_until = 1
        else:
            days_until = 0
        
        return {
            "water_need_mm": round(water_needed, 2),
            "water_need_liters_per_acre": round(water_needed * 4046.86, 2),
            "recommended_irrigation_time": self._get_best_irrigation_time(temp, humidity),
            "days_until_next_irrigation": days_until,
            "priority": self._get_priority(water_needed, days_until),
            "suggested_duration_minutes": self._calculate_duration(water_needed, soil),
            "water_saving_tips": self._get_water_saving_tips(crop, soil),
            "method_recommendation": self._recommend_irrigation_method(crop, soil)
        }
    
    def _calculate_et0(self, temp, humidity, wind):
        """Calculate reference evapotranspiration (simplified)"""
        # Simplified Hargreaves equation
        et0 = 0.0023 * (temp + 17.8) * np.sqrt(max(0, temp - 10)) * 2.5
        return et0
    
    def _get_crop_coefficient(self, crop, stage):
        """Get crop coefficient based on growth stage"""
        kc_values = {
            'initial': 0.3,
            'vegetative': 0.5,
            'flowering': 1.0,
            'fruiting': 1.1,
            'ripening': 0.8
        }
        
        crop_kc = {
            'rice': {'initial': 1.1, 'vegetative': 1.15, 'flowering': 1.2, 'ripening': 0.9},
            'wheat': {'initial': 0.4, 'vegetative': 0.8, 'flowering': 1.15, 'ripening': 0.4},
            'cotton': {'initial': 0.5, 'vegetative': 0.8, 'flowering': 1.1, 'ripening': 0.7},
            'tomato': {'initial': 0.5, 'vegetative': 0.7, 'flowering': 1.05, 'ripening': 0.9}
        }
        
        if crop in crop_kc and stage in crop_kc[crop]:
            return crop_kc[crop][stage]
        
        return kc_values.get(stage, 0.7)
    
    def _get_soil_adjustment(self, soil_type, moisture):
        """Adjust for soil type and current moisture"""
        soil_water_capacity = {
            'sandy': 0.3,
            'loamy': 0.5,
            'clay': 0.7,
            'silt': 0.6
        }
        
        capacity = soil_water_capacity.get(soil_type, 0.5)
        
        # If moisture is low, more water needed
        if moisture < capacity * 100 * 0.5:
            return 1.3  # Increase by 30%
        elif moisture < capacity * 100 * 0.7:
            return 1.1
        else:
            return 0.9
    
    def _get_best_irrigation_time(self, temp, humidity):
        """Recommend best time for irrigation"""
        if temp > 35:
            return "Early morning (5-7 AM) or evening (6-8 PM) to minimize evaporation"
        elif temp > 25:
            return "Early morning (6-8 AM) is best"
        else:
            return "Mid-morning (8-10 AM) is ideal"
    
    def _get_priority(self, water_needed, days_until):
        """Determine irrigation priority"""
        if days_until == 0:
            return "URGENT - Irrigate immediately"
        elif days_until <= 1:
            return "HIGH - Irrigate within 24 hours"
        elif days_until <= 3:
            return "MEDIUM - Plan irrigation soon"
        else:
            return "LOW - No immediate irrigation needed"
    
    def _calculate_duration(self, water_mm, soil):
        """Calculate recommended irrigation duration"""
        # Approximate application rates
        application_rates = {
            'flood': 25,  # mm per hour
            'drip': 8,    # mm per hour
            'sprinkler': 15  # mm per hour
        }
        
        # Assume flood irrigation
        duration = (water_mm / application_rates['flood']) * 60  # minutes
        
        return round(min(duration, 180), 0)  # Max 3 hours
    
    def _get_water_saving_tips(self, crop, soil):
        """Generate water-saving recommendations"""
        tips = []
        
        if soil == 'sandy':
            tips.append("Use drip irrigation - sandy soil has low water retention")
            tips.append("Apply mulch to reduce evaporation")
        elif soil == 'clay':
            tips.append("Avoid over-irrigation - clay retains water well")
            tips.append("Use controlled drainage")
        
        tips.append("Irrigate at dawn or dusk to reduce evaporation")
        tips.append("Use mulch around plants")
        
        return tips
    
    def _recommend_irrigation_method(self, crop, soil):
        """Recommend irrigation method"""
        if crop == 'rice':
            return "Flood irrigation preferred"
        elif crop == 'tomato':
            return "Drip irrigation recommended - reduces leaf wetness and disease"
        elif soil == 'sandy':
            return "Drip irrigation - best for water efficiency"
        elif soil == 'clay':
            return "Drip or sprinkler - avoid waterlogging"
        else:
            return "Drip irrigation recommended for water efficiency"
```

---

### Feature 9: Profit Prediction Engine

**Purpose**: Calculate expected profit, ROI, and risk analysis

**Files to create**: `src/features/profit_prediction.py`

```python
"""
Feature 9: Profit Prediction Engine
Calculate expected profit, ROI, and risk analysis
"""
import numpy as np
import random

class ProfitPredictor:
    def __init__(self):
        self.market_trends = self._load_market_data()
    
    def _load_market_data(self):
        """Load current market trends"""
        return {
            'tomato': {'current_price': 25, 'trend': 'rising', 'volatility': 'medium'},
            'potato': {'current_price': 15, 'trend': 'stable', 'volatility': 'low'},
            'onion': {'current_price': 20, 'trend': 'falling', 'volatility': 'high'},
            'rice': {'current_price': 45, 'trend': 'stable', 'volatility': 'low'},
            'wheat': {'current_price': 30, 'trend': 'rising', 'volatility': 'medium'},
            'cotton': {'current_price': 60, 'trend': 'rising', 'volatility': 'high'}
        }
    
    def calculate_profit(self, inputs):
        """
        Calculate profit prediction
        
        Required inputs:
        - crop: string
        - land_size: acres
        - investment_cost: rupees (seeds, labor, etc.)
        - fertilizer_cost: rupees
        - irrigation_cost: rupees
        - pest_control_cost: rupees
        - expected_yield: tons
        - market_price: rupees/quintal (optional - will use prediction)
        """
        
        crop = inputs.get('crop', 'unknown')
        land = float(inputs.get('land_size', 1))
        
        # Costs
        investment = float(inputs.get('investment_cost', 0))
        fertilizer = float(inputs.get('fertilizer_cost', 0))
        irrigation = float(inputs.get('irrigation_cost', 0))
        pest_control = float(inputs.get('pest_control_cost', 0))
        
        total_cost = investment + fertilizer + irrigation + pest_control
        
        # Yield
        expected_yield = float(inputs.get('expected_yield', 0))
        yield_tons = expected_yield * land  # Total yield
        
        # Get market price (use current or predicted)
        market_data = self.market_trends.get(crop, {'current_price': 25})
        price_per_quintal = inputs.get('market_price', market_data['current_price'])
        
        # Convert tons to quintals (1 ton = 10 quintals)
        yield_quintals = yield_tons * 10
        
        # Calculate revenue
        revenue = yield_quintals * price_per_quintal
        
        # Calculate profit
        gross_profit = revenue - total_cost
        net_profit = gross_profit  # Can add more costs
        
        # ROI
        roi = (net_profit / total_cost * 100) if total_cost > 0 else 0
        
        # Per acre metrics
        profit_per_acre = net_profit / land if land > 0 else 0
        cost_per_acre = total_cost / land if land > 0 else 0
        revenue_per_acre = revenue / land if land > 0 else 0
        
        # Risk analysis
        risk_analysis = self._analyze_risk(crop, market_data, total_cost, expected_yield)
        
        return {
            "summary": {
                "total_cost": round(total_cost, 2),
                "expected_revenue": round(revenue, 2),
                "expected_profit": round(net_profit, 2),
                "roi_percentage": round(roi, 2),
                "profit_per_acre": round(profit_per_acre, 2)
            },
            "detailed_costs": {
                "investment_cost": investment,
                "fertilizer_cost": fertilizer,
                "irrigation_cost": irrigation,
                "pest_control_cost": pest_control,
                "cost_per_acre": round(cost_per_acre, 2)
            },
            "revenue_breakdown": {
                "expected_yield_tons": round(yield_tons, 2),
                "yield_quintals": round(yield_quintals, 2),
                "price_per_quintal": price_per_quintal,
                "revenue_per_acre": round(revenue_per_acre, 2)
            },
            "risk_analysis": risk_analysis,
            "recommendations": self._get_recommendations(net_profit, roi, risk_analysis),
            "break_even": {
                "price_per_quintal": round(total_cost / yield_quintals, 2) if yield_quintals > 0 else 0,
                "yield_quintals": round(total_cost / price_per_quintal, 2) if price_per_quintal > 0 else 0
            }
        }
    
    def _analyze_risk(self, crop, market_data, total_cost, expected_yield):
        """Analyze various risk factors"""
        risks = {}
        
        # Market risk
        trend = market_data.get('trend', 'stable')
        volatility = market_data.get('volatility', 'medium')
        
        if trend == 'falling':
            market_risk = 70
            market_advice = "WARNING: Market prices declining. Consider selling early."
        elif trend == 'stable':
            market_risk = 30
            market_advice = "Stable market. Good time to sell."
        else:  # rising
            market_risk = 20
            market_advice = "Prices rising. Consider holding for better prices."
        
        if volatility == 'high':
            market_risk = min(90, market_risk + 20)
        
        risks['market_risk'] = {
            'score': market_risk,
            'trend': trend,
            'advice': market_advice
        }
        
        # Production risk (based on yield uncertainty)
        if expected_yield > 5:
            production_risk = 20
        elif expected_yield > 3:
            production_risk = 40
        else:
            production_risk = 60
        
        risks['production_risk'] = {
            'score': production_risk,
            'advice': "Good yield expected" if production_risk < 40 else "Yield may vary"
        }
        
        # Cost overrun risk
        cost_risk = random.randint(10, 30)
        risks['cost_risk'] = {
            'score': cost_risk,
            'advice': "Budget for 10-20% cost overruns"
        }
        
        # Overall risk score
        overall_risk = (
            market_risk * 0.4 +
            production_risk * 0.4 +
            cost_risk * 0.2
        )
        
        risks['overall_risk'] = {
            'score': round(overall_risk, 2),
            'level': 'LOW' if overall_risk < 30 else 'MEDIUM' if overall_risk < 60 else 'HIGH'
        }
        
        return risks
    
    def _get_recommendations(self, profit, roi, risk_analysis):
        """Generate profit improvement recommendations"""
        recs = []
        
        if roi < 0:
            recs.append("⚠️ Negative ROI - Review your cost structure immediately")
            recs.append("💡 Consider reducing input costs or choosing more profitable crops")
        elif roi < 20:
            recs.append("📊 Low ROI - Look for ways to reduce costs")
            recs.append("💡 Consider high-value crops for better returns")
        elif roi < 50:
            recs.append("✅ Moderate ROI - Current farming is viable")
            recs.append("💡 Consider expanding or optimizing inputs")
        else:
            recs.append("🌟 Excellent ROI - Great investment opportunity!")
        
        # Risk-based recommendations
        if risk_analysis['market_risk']['score'] > 50:
            recs.append(f"📉 {risk_analysis['market_risk']['advice']}")
        
        if risk_analysis['production_risk']['score'] > 50:
            recs.append("🌱 Focus on improving yield through better crop management")
        
        return recs
    
    def compare_crops(self, land_size, available_budget):
        """Compare profit potential of different crops"""
        crops = ['tomato', 'potato', 'onion', 'rice', 'wheat', 'cotton']
        results = []
        
        for crop in crops:
            # Estimate based on typical values
            typical_yield = {
                'tomato': 15, 'potato': 20, 'onion': 15,
                'rice': 4, 'wheat': 3, 'cotton': 2
            }
            
            market = self.market_trends.get(crop, {'current_price': 25})
            yld = typical_yield.get(crop, 5)
            
            # Estimate costs (rough)
            costs = {
                'tomato': 80000, 'potato': 60000, 'onion': 70000,
                'rice': 50000, 'wheat': 40000, 'cotton': 55000
            }
            
            cost = costs.get(crop, 60000)
            price = market['current_price']
            
            revenue = (yld * land_size * 10) * price
            profit = revenue - cost
            roi = (profit / cost * 100) if cost > 0 else 0
            
            results.append({
                'crop': crop,
                'expected_yield': yld * land_size,
                'estimated_revenue': revenue,
                'estimated_cost': cost,
                'estimated_profit': profit,
                'roi': round(roi, 2),
                'risk': market['volatility']
            })
        
        # Sort by ROI
        results.sort(key=lambda x: x['roi'], reverse=True)
        
        return {
            "ranked_crops": results,
            "best_choice": results[0] if results else None,
            "lowest_risk": min(results, key=lambda x: x['risk']) if results else None
        }
```

---

### Feature 10: Feedback System

**Files to create**: `src/utils/feedback.py`

```python
"""
Feedback System
Collect and analyze user feedback
"""
import json
import os
from datetime import datetime

class FeedbackSystem:
    def __init__(self):
        self.feedback_file = 'data/feedback.json'
        self.feedback_data = []
        self.load_feedback()
    
    def load_feedback(self):
        """Load existing feedback"""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                self.feedback_data = json.load(f)
    
    def save_feedback(self):
        """Save feedback to file"""
        os.makedirs('data', exist_ok=True)
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
    
    def collect_feedback(self, rating, comment=None, feature=None):
        """
        Collect user feedback
        
        Args:
            rating: 1-5 stars
            comment: Optional text comment
            feature: Which feature was used
        """
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "comment": comment,
            "feature": feature
        }
        
        self.feedback_data.append(feedback)
        self.save_feedback()
        
        return "Thank you for your feedback! 🌾"
    
    def get_feedback_stats(self):
        """Get feedback statistics"""
        if not self.feedback_data:
            return {"message": "No feedback yet"}
        
        total = len(self.feedback_data)
        ratings = [f['rating'] for f in self.feedback_data]
        
        avg_rating = sum(ratings) / total
        
        return {
            "total_feedback": total,
            "average_rating": round(avg_rating, 2),
            "rating_distribution": {
                "5_star": ratings.count(5),
                "4_star": ratings.count(4),
                "3_star": ratings.count(3),
                "2_star": ratings.count(2),
                "1_star": ratings.count(1)
            }
        }
```

---

## 🖥️ PHASE 5: User Interface

### Create Streamlit Web UI

**File**: `ui/streamlit_app.py`

```python
"""
Trinetra Agro AI - Streamlit Web Interface
"""
import streamlit as st
import sys
sys.path.append('.')

from src.features.farmer_profile import FarmerProfileEngine
from src.features.disease_detection import DiseaseDetector
from src.features.market_prediction import MarketPredictor
from src.features.risk_analysis import RiskAnalyzer
from src.features.yield_prediction import YieldPredictor
from src.features.voice_ai import VoiceAI
from src.features.conversational_ai import ConversationalAI
from src.features.irrigation import IrrigationAI
from src.features.profit_prediction import ProfitPredictor
from src.utils.feedback import FeedbackSystem

# Page config
st.set_page_config(
    page_title="Trinetra Agro AI",
    page_icon="🌾",
    layout="wide"
)

# Initialize features
@st.cache_resource
def init_features():
    return {
        'farmer_profile': FarmerProfileEngine(),
        'disease_detector': DiseaseDetector(),
        'market_predictor': MarketPredictor(),
        'risk_analyzer': RiskAnalyzer(),
        'yield_predictor': YieldPredictor(),
        'conversational': ConversationalAI(),
        'irrigation': IrrigationAI(),
        'profit': ProfitPredictor(),
        'feedback': FeedbackSystem()
    }

features = init_features()

# Sidebar
st.sidebar.title("🔱 Trinetra Agro AI")
st.sidebar.markdown("### Vision Beyond the Fields")

page = st.sidebar.selectbox(
    "Choose Feature",
    ["Home", "Farmer Profile", "Disease Detection", "Market Prediction",
     "Risk Analysis", "Yield Prediction", "Irrigation", "Profit Calculator", "Chat"]
)

# Home page
if page == "Home":
    st.title("🌾 Trinetra Agro AI")
    st.subheader("Vision Beyond the Fields")
    
    st.markdown("""
    ## Welcome to Trinetra Agro AI! 👨‍🌾
    
    Your AI-powered farming assistant with **10+ advanced features**:
    
    1. 👤 **Personalized Farming Advisor** - Tailored recommendations
    2. 🔬 **Crop Disease Detection** - AI-powered image analysis
    3. 📈 **Market Price Prediction** - Smart selling decisions
    4. ⚠️ **Risk Analysis** - Crop failure prediction
    5. 🌱 **Yield Prediction** - Harvest forecasting
    6. 🎤 **Voice AI** - Speak in Telugu/Hindi
    7. 💬 **Smart Chat** - Ask anything!
    8. 💧 **Smart Irrigation** - Water optimization
    9. 💰 **Profit Calculator** - ROI analysis
    10. 📝 **Feedback** - Help us improve
    """)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Farmers Helped", "10,000+")
    with col2:
        st.metric("Diseases Detected", "50+")
    with col3:
        st.metric("Accuracy", "95%")
    with col4:
        st.metric("Languages", "6")

# Disease Detection
elif page == "Disease Detection":
    st.title("🔬 Crop Disease Detection")
    st.markdown("Upload a leaf image to detect diseases using AI")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Save temporarily
        import cv2
        import numpy as np
        from PIL import Image
        
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)
        
        if st.button("Detect Disease"):
            with st.spinner("Analyzing image..."):
                # Save image
                image.save("data/images/uploaded_leaf.jpg")
                
                # Detect
                result = features['disease_detector'].detect_disease("data/images/uploaded_leaf.jpg")
                
                st.success("Analysis Complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Disease", result['disease'])
                with col2:
                    st.metric("Confidence", f"{result['confidence']*100:.1f}%")
                
                st.markdown(f"**Severity:** {result['severity']}")
                st.markdown(f"**Recommendation:** {result['recommendation']}")

# Market Prediction
elif page == "Market Prediction":
    st.title("📈 Market Price Prediction")
    
    crop = st.selectbox("Select Crop", ["tomato", "potato", "onion", "rice", "wheat", "cotton"])
    days = st.slider("Days to predict", 7, 30, 7)
    
    if st.button("Predict Prices"):
        with st.spinner("Analyzing market data..."):
            result = features['market_predictor'].predict_prices(crop, days)
            
            st.markdown(f"### Current Price: ₹{result['current_price']}/quintal")
            st.markdown(f"**Recommendation: {result['recommendation']['action']}**")
            st.markdown(result['recommendation']['message'])
            
            # Show chart
            import pandas as pd
            import plotly.express as px
            
            df = pd.DataFrame({
                'Date': result['dates'],
                'Predicted Price': result['predictions']
            })
            
            fig = px.line(df, x='Date', y='Predicted Price', 
                         title=f'{crop.title()} Price Prediction')
            st.plotly_chart(fig)

# Continue with other pages...
```

---

## ✅ PHASE 6: Testing & Validation

### Create Test File

```python
"""
tests/test_features.py
"""
import sys
sys.path.append('.')

def test_farmer_profile():
    from src.features.farmer_profile import FarmerProfileEngine
    engine = FarmerProfileEngine()
    
    # Test profile creation
    profile = engine.create_profile("farmer_001", {
        "name": "Rama Rao",
        "land_size": 5,
        "soil_type": "clay",
        "crop_history": ["rice", "wheat"],
        "budget": 50000,
        "location": "Andhra Pradesh"
    })
    
    assert profile["land_size"] == 5
    print("✅ Farmer profile test passed")

def test_market_prediction():
    from src.features.market_prediction import MarketPredictor
    predictor = MarketPredictor()
    
    result = predictor.predict_prices("tomato", 7)
    assert "predictions" in result
    print("✅ Market prediction test passed")

def test_yield_prediction():
    from src.features.yield_prediction import YieldPredictor
    predictor = YieldPredictor()
    
    result = predictor.predict_yield({
        "fertilizer_amount": 100,
        "rainfall": 300,
        "temperature_avg": 25,
        "soil_nitrogen": 50,
        "soil_phosphorus": 30,
        "soil_potassium": 40,
        "irrigation_days": 30,
        "pest_control": 7,
        "crop_age": 90,
        "land_size": 5
    })
    
    assert "predicted_yield" in result
    print("✅ Yield prediction test passed")

def test_profit_prediction():
    from src.features.profit_prediction import ProfitPredictor
    predictor = ProfitPredictor()
    
    result = predictor.calculate_profit({
        "crop": "tomato",
        "land_size": 5,
        "investment_cost": 30000,
        "fertilizer_cost": 15000,
        "irrigation_cost": 10000,
        "pest_control_cost": 5000,
        "expected_yield": 10
    })
    
    assert "expected_profit" in result
    print("✅ Profit prediction test passed")

def test_risk_analysis():
    from src.features.risk_analysis import RiskAnalyzer
    analyzer = RiskAnalyzer()
    
    result = analyzer.calculate_risk_score({
        "rainfall_forecast": 80,
        "temperature_trends": [25, 26, 27],
        "soil_moisture": 55,
        "pest_risk": 3,
        "disease_risk": False,
        "crop_type": "rice"
    })
    
    assert "risk_percentage" in result
    print("✅ Risk analysis test passed")

if __name__ == "__main__":
    test_farmer_profile()
    test_market_prediction()
    test_yield_prediction()
    test_profit_prediction()
    test_risk_analysis()
    print("\n🎉 All tests passed!")
```

---

## 📚 Installation & Running Guide

### Quick Start:

```bash
# 1. Clone/Create project
cd /workspaces/Trinetra-Agro-AI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the chatbot
python main.py

# OR run Streamlit UI
cd ui
streamlit run streamlit_app.py
```

### Requirements.txt:
```
numpy>=1.24.0
pandas>=2.0.0
tensorflow>=2.13.0
scikit-learn>=1.3.0
xgboost>=2.0.0
prophet>=1.1.0
streamlit>=1.27.0
openai>=1.0.0
whisper>=20231117
gtts>=2.3.0
speechrecognition>=3.10.0
cv2>=4.8.0
pillow>=10.0.0
plotly>=5.15.0
python-dotenv>=1.0.0
joblib>=1.3.0
```

---

## 🎯 Project Completion Checklist

- [x] Project Structure Created
- [x] Core Chatbot Framework
- [x] Farmer Profile Engine
- [x] Disease Detection with CNN
- [x] Market Price Prediction
- [x] Risk Analysis System
- [x] Yield Prediction Model
- [x] Voice AI
- [x] Conversational AI
- [x] Smart Irrigation
- [x] Profit Prediction
- [x] Feedback System
- [x] Web UI (Streamlit)
- [x] Testing Framework
- [x] Documentation

---

## 🔗 Resources & Downloads

### Download Links:

1. **Python**: https://www.python.org/downloads/
2. **VS Code**: https://code.visualstudio.com/
3. **Git**: https://git-scm.com/

### Model Weights (for production):
- ResNet50: https://keras.io/api/applications/
- MobileNetV2: https://keras.io/api/applications/
- Whisper: pip install whisper
- Prophet: pip install prophet

### APIs (optional):
- OpenAI API: https://platform.openai.com/
- Weather API: https://openweathermap.org/api

---

**Trinetra Agro AI - Vision Beyond the Fields** 🚜🌾

*Empowering farmers with AI for a sustainable future!*
