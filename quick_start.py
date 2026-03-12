#!/usr/bin/env python3
"""
Trinetra Agro AI - Quick Start Script
Run this script to quickly test the basic functionality
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_path = Path(__file__).parent / "app"
sys.path.insert(0, str(app_path))

def main():
    """Quick start demonstration"""
    
    print("🔱" * 20)
    print("🔱 TRINETRA AGRO AI - QUICK START 🔱")
    print("🔱 Vision Beyond the Fields 🔱")
    print("🔱" * 20)
    print()
    
    try:
        # Test basic imports
        print("📦 Testing imports...")
        from chatbot.core_bot import TrinetraBot
        from utils.helpers import validate_farmer_profile, calculate_crop_suitability
        from utils.config import load_config
        print("✅ All imports successful!")
        print()
        
        # Create sample farmer profile
        print("👨‍🌾 Creating sample farmer profile...")
        farmer_profile = {
            'name': 'Ramesh Kumar',
            'land_size': 5.0,
            'soil_type': 'Black Cotton',
            'budget': 50000,
            'location': 'Hyderabad'
        }
        
        # Validate profile
        if validate_farmer_profile(farmer_profile):
            print("✅ Farmer profile validation successful!")
        else:
            print("❌ Farmer profile validation failed!")
            return
        
        print(f"📋 Farmer: {farmer_profile['name']}")
        print(f"📐 Land Size: {farmer_profile['land_size']} acres")
        print(f"🏞️ Soil Type: {farmer_profile['soil_type']}")
        print(f"💰 Budget: ₹{farmer_profile['budget']:,}")
        print()
        
        # Initialize chatbot
        print("🤖 Initializing Trinetra AI chatbot...")
        bot = TrinetraBot(
            language="English",
            farmer_profile=farmer_profile
        )
        print("✅ Chatbot initialized successfully!")
        print()
        
        # Test basic conversation
        print("💬 Testing conversation capabilities...")
        test_messages = [
            "Hello, I need farming advice",
            "What crops should I plant this season?",
            "I see some spots on my tomato leaves",
            "What are the current rice prices?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n🧑‍🌾 User {i}: {message}")
            response = bot.get_response(message)
            print(f"🔱 Trinetra: {response[:200]}{'...' if len(response) > 200 else ''}")
        
        print("\n" + "="*60)
        print("✅ BASIC FUNCTIONALITY TEST COMPLETE!")
        print("="*60)
        
        # Test crop recommendations
        print("\n🌾 Testing crop recommendation system...")
        recommendations = calculate_crop_suitability(
            soil_type=farmer_profile['soil_type'],
            season="Kharif",
            budget=farmer_profile['budget']
        )
        
        print("\n📊 TOP CROP RECOMMENDATIONS:")
        for i, crop in enumerate(recommendations[:3], 1):
            print(f"{i}. {crop['crop']} - Score: {crop['score']}/100")
            print(f"   💰 Investment: ₹{crop['investment_needed']:,}")
            print(f"   📈 Profit Potential: {crop['profit_potential']}")
        
        print("\n" + "="*60)
        print("🎉 QUICK START DEMO COMPLETE!")
        print("="*60)
        print()
        
        # Next steps
        print("🚀 NEXT STEPS:")
        print("1. Run the full application:")
        print("   ./start_trinetra.sh")
        print("   OR")
        print("   streamlit run app/main.py")
        print()
        print("2. Open your browser and go to:")
        print("   http://localhost:8501")
        print()
        print("3. Start chatting with Trinetra AI!")
        print()
        print("📚 For detailed development guide, see:")
        print("   📄 ROADMAP.md - Complete development roadmap")
        print("   📄 README.md - Project documentation")
        print()
        print("🔱 Happy Farming with AI! 🔱")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 SOLUTION:")
        print("1. Make sure you've installed all dependencies:")
        print("   pip install -r requirements.txt")
        print()
        print("2. Or run the setup script:")
        print("   chmod +x setup.sh && ./setup.sh")
        print()
        return False
        
    except Exception as e:
        print(f"❌ Error during quick start: {e}")
        print("\n🔧 Please check your setup and try again.")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)