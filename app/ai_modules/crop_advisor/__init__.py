"""
Trinetra Agro AI - Personalized Farming Advisor Module
Uses Recommendation System with Collaborative Filtering and ML
"""

import random
from datetime import datetime
from typing import Dict, List, Any


class CropAdvisor:
    """
    AI-Powered Personalized Farming Advisor
    Uses collaborative filtering and content-based recommendations
    """
    
    # Crop database with detailed information
    CROP_DATABASE = {
        'rice': {
            'name': 'Rice (Paddy)',
            'season': 'Kharif',
            'duration': '120-150 days',
            'soil_types': ['alluvial', 'clay', 'loamy'],
            'water_requirement': 'High (150-200 cm)',
            'temperature': '20-35°C',
            'rainfall': '100-150 cm',
            'npk_ratio': '100:50:50',
            'expected_yield': '3-6 tons/ha',
            'profit_range': '30000-80000',
            'diseases': ['Blast', 'Bacterial Leaf Blight', 'Brown Spot'],
            'varieties': ['Basmati', 'Ponni', 'IR64', 'Sona Masuri'],
            'markets': ['rice mills', 'wholesale markets', 'export']
        },
        'wheat': {
            'name': 'Wheat',
            'season': 'Rabi',
            'duration': '120-150 days',
            'soil_types': ['alluvial', 'loamy', 'clay'],
            'water_requirement': 'Medium (40-60 cm)',
            'temperature': '15-25°C',
            'rainfall': '50-75 cm',
            'npk_ratio': '120:60:40',
            'expected_yield': '3-5 tons/ha',
            'profit_range': '25000-60000',
            'diseases': ['Rust', 'Powdery Mildew', 'Loose Smut'],
            'varieties': ['HD 2967', 'PBW 550', 'WHD 943'],
            'markets': ['mandis', 'flour mills', 'government procurement']
        },
        'cotton': {
            'name': 'Cotton',
            'season': 'Kharif',
            'duration': '150-180 days',
            'soil_types': ['black cotton', 'clayey', 'loamy'],
            'water_requirement': 'Medium (60-80 cm)',
            'temperature': '25-35°C',
            'rainfall': '60-100 cm',
            'npk_ratio': '100:50:50',
            'expected_yield': '1.5-3 tons/ha',
            'profit_range': '40000-100000',
            'diseases': ['Boll Rot', 'Wilt', 'Leaf Curl Virus'],
            'varieties': ['Bt Cotton', 'Desi Cotton', 'MCU 5'],
            'markets': ['textile mills', 'ginning factories', 'export']
        },
        'tomato': {
            'name': 'Tomato',
            'season': 'Rabi/Kharif',
            'duration': '90-120 days',
            'soil_types': ['loamy', 'sandy loam'],
            'water_requirement': 'Medium (60-80 cm)',
            'temperature': '20-30°C',
            'rainfall': '60-100 cm',
            'npk_ratio': '100:60:80',
            'expected_yield': '40-60 tons/ha',
            'profit_range': '50000-150000',
            'diseases': ['Late Blight', 'Early Blight', 'Leaf Curl'],
            'varieties': ['Pusa Ruby', 'Roma', 'Sankranthi'],
            'markets': ['wholesale markets', 'processing industry', 'local']
        },
        'potato': {
            'name': 'Potato',
            'season': 'Rabi',
            'duration': '90-120 days',
            'soil_types': ['sandy loam', 'loamy'],
            'water_requirement': 'Medium (50-70 cm)',
            'temperature': '15-25°C',
            'rainfall': '50-70 cm',
            'npk_ratio': '100:60:80',
            'expected_yield': '20-30 tons/ha',
            'profit_range': '40000-120000',
            'diseases': ['Late Blight', 'Early Blight', 'Bacterial Wilt'],
            'varieties': ['Kufri Jyoti', 'Kufri Badshah', 'Kufri Pukhraj'],
            'markets': ['wholesale markets', 'chip manufacturers', 'cold storage']
        },
        'onion': {
            'name': 'Onion',
            'season': 'Rabi/Kharif',
            'duration': '90-120 days',
            'soil_types': ['sandy loam', 'loamy'],
            'water_requirement': 'Medium (50-70 cm)',
            'temperature': '15-30°C',
            'rainfall': '50-70 cm',
            'npk_ratio': '100:50:50',
            'expected_yield': '20-30 tons/ha',
            'profit_range': '30000-100000',
            'diseases': ['Purple Blotch', 'Stemphylium Blight'],
            'varieties': ['Nashik Red', 'Pusa Red', 'Arka Kalyan'],
            'markets': ['wholesale markets', 'export', 'processing']
        },
        'maize': {
            'name': 'Maize (Corn)',
            'season': 'Kharif/Rabi',
            'duration': '90-120 days',
            'soil_types': ['loamy', 'sandy loam'],
            'water_requirement': 'Medium (50-80 cm)',
            'temperature': '20-30°C',
            'rainfall': '50-100 cm',
            'npk_ratio': '120:60:40',
            'expected_yield': '6-10 tons/ha',
            'profit_range': '30000-80000',
            'diseases': ['Northern Leaf Blight', 'Stalk Rot'],
            'varieties': ['HQPM 1', 'PMH 1', 'Bio 9688'],
            'markets': ['animal feed industry', 'starch industry', 'wholesale']
        },
        'sugarcane': {
            'name': 'Sugarcane',
            'season': 'Spring/Kharif',
            'duration': '300-360 days',
            'soil_types': ['alluvial', 'loamy', 'black cotton'],
            'water_requirement': 'High (150-200 cm)',
            'temperature': '20-35°C',
            'rainfall': '100-150 cm',
            'npk_ratio': '250:60:60',
            'expected_yield': '60-80 tons/ha',
            'profit_range': '80000-200000',
            'diseases': ['Red Rot', 'Smut', 'Wilt'],
            'varieties': ['Co 86032', 'Co 0238', 'Co V 8450'],
            'markets': ['sugar mills', 'jaggery', 'cogeneration']
        },
        'soybean': {
            'name': 'Soybean',
            'season': 'Kharif',
            'duration': '90-120 days',
            'soil_types': ['sandy loam', 'loamy'],
            'water_requirement': 'Medium (45-60 cm)',
            'temperature': '20-30°C',
            'rainfall': '60-90 cm',
            'npk_ratio': '20:60:20',
            'expected_yield': '2-3 tons/ha',
            'profit_range': '25000-70000',
            'diseases': ['Yellow Mosaic Virus', 'Rust'],
            'varieties': ['JS 95-60', 'PK 472', 'MAUS 158'],
            'markets': ['oil industry', 'export', 'animal feed']
        },
        'groundnut': {
            'name': 'Groundnut (Peanut)',
            'season': 'Kharif/Rabi',
            'duration': '120-150 days',
            'soil_types': ['sandy loam', 'loamy'],
            'water_requirement': 'Medium (50-70 cm)',
            'temperature': '25-30°C',
            'rainfall': '50-70 cm',
            'npk_ratio': '20:60:40',
            'expected_yield': '2-3 tons/ha',
            'profit_range': '30000-80000',
            'diseases': ['Tikka', 'Leaf Spot', 'Rust'],
            'varieties': ['JL 24', 'TAG 24', 'K 134'],
            'markets': ['oil mills', 'confectionery', 'export']
        }
    }
    
    # Regional recommendations
    REGIONAL_CROPS = {
        'andhra_pradesh': ['rice', 'cotton', 'sugarcane', 'tomato', 'groundnut'],
        'telangana': ['rice', 'cotton', 'sugarcane', 'maize', 'soybean'],
        'maharashtra': ['cotton', 'sugarcane', 'tomato', 'onion', 'wheat'],
        'karnataka': ['rice', 'sugarcane', 'cotton', 'maize', 'groundnut'],
        'tamil_nadu': ['rice', 'cotton', 'sugarcane', 'groundnut', 'tomato'],
        'gujarat': ['cotton', 'groundnut', 'wheat', 'tomato', 'onion'],
        'punjab': ['wheat', 'rice', 'cotton', 'maize', 'potato'],
        'haryana': ['wheat', 'rice', 'cotton', 'mustard', 'potato'],
        'uttar_pradesh': ['wheat', 'rice', 'sugarcane', 'potato', 'onion'],
        'west_bengal': ['rice', 'potato', 'mustard', 'jute', 'vegetables']
    }
    
    def __init__(self):
        """Initialize the Crop Advisor"""
        self.farmer_profiles = {}
        self.recommendation_history = []
    
    def create_farmer_profile(self, farmer_id: str, profile_data: dict) -> dict:
        """
        Create farmer profile for personalized recommendations
        
        Args:
            farmer_id: Unique farmer identifier
            profile_data: Dictionary with farmer details
            
        Returns:
            Created profile
        """
        profile = {
            'farmer_id': farmer_id,
            'name': profile_data.get('name', ''),
            'land_size': float(profile_data.get('land_size', 1)),  # acres
            'soil_type': profile_data.get('soil_type', 'unknown').lower(),
            'budget': float(profile_data.get('budget', 50000)),
            'location': profile_data.get('location', 'unknown').lower(),
            'climate': profile_data.get('climate', 'tropical'),
            'irrigation_available': profile_data.get('irrigation_available', True),
            'crop_history': profile_data.get('crop_history', []),
            'experience_years': int(profile_data.get('experience_years', 5)),
            'risk_preference': profile_data.get('risk_preference', 'medium'),  # low, medium, high
            'created_at': datetime.now().isoformat()
        }
        
        self.farmer_profiles[farmer_id] = profile
        return profile
    
    def get_recommendations(self, farmer_id: str = None, profile: dict = None) -> dict:
        """
        Get personalized crop recommendations
        
        Args:
            farmer_id: Farmer ID (if profile exists)
            profile: Or provide profile directly
            
        Returns:
            Recommendations dictionary
        """
        # Get profile
        if farmer_id and farmer_id in self.farmer_profiles:
            profile = self.farmer_profiles[farmer_id]
        elif profile is None:
            return {'error': 'No profile provided'}
        
        # Content-based filtering
        content_recs = self._content_based_recommendations(profile)
        
        # Collaborative filtering (similar farmers)
        collab_recs = self._collaborative_recommendations(profile)
        
        # Combine recommendations
        combined = self._combine_recommendations(content_recs, collab_recs)
        
        # Generate seasonal plan
        seasonal_plan = self._generate_seasonal_plan(profile, combined)
        
        # Store recommendation
        self.recommendation_history.append({
            'farmer_id': farmer_id,
            'recommendations': combined,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'success': True,
            'farmer_profile': profile,
            'primary_recommendations': combined['primary'],
            'secondary_recommendations': combined['secondary'],
            'seasonal_plan': seasonal_plan,
            'risk_assessment': self._assess_farming_risk(profile, combined),
            'expected_returns': self._estimate_returns(profile, combined)
        }
    
    def _content_based_recommendations(self, profile: dict) -> list:
        """Content-based filtering using farmer profile"""
        recommendations = []
        
        soil_type = profile.get('soil_type', 'unknown')
        land_size = profile.get('land_size', 1)
        budget = profile.get('budget', 50000)
        location = profile.get('location', 'unknown')
        
        for crop_id, crop_info in self.CROP_DATABASE.items():
            score = 0
            
            # Soil compatibility
            if soil_type in crop_info['soil_types']:
                score += 40
            elif 'loamy' in crop_info['soil_types'] and soil_type in ['alluvial', 'clay']:
                score += 20
            
            # Budget compatibility
            profit_min = int(crop_info['profit_range'].split('-')[0])
            if budget >= profit_min:
                score += 30
            
            # Land size suitability
            if land_size >= 2:
                score += 15
            
            # Location/regional suitability
            if location in self.REGIONAL_CROPS:
                if crop_id in self.REGIONAL_CROPS[location]:
                    score += 15
            
            recommendations.append({
                'crop': crop_id,
                'score': score,
                'reasons': self._get_recommendation_reasons(crop_id, profile)
            })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations
    
    def _collaborative_recommendations(self, profile: dict) -> list:
        """Find similar farmers and recommend what worked for them"""
        # This is a simplified version
        # In production, this would use actual clustering
        
        # Get regional crops
        location = profile.get('location', 'unknown')
        
        if location in self.REGIONAL_CROPS:
            regional = self.REGIONAL_CROPS[location]
            return [
                {'crop': crop, 'score': 70 + random.randint(0, 20)}
                for crop in regional[:3]
            ]
        
        # Default popular crops
        popular = ['rice', 'wheat', 'cotton', 'tomato']
        return [
            {'crop': crop, 'score': 60}
            for crop in popular
        ]
    
    def _combine_recommendations(self, content: list, collab: list) -> dict:
        """Combine content-based and collaborative recommendations"""
        # Create score dictionary
        combined_scores = {}
        
        for rec in content:
            combined_scores[rec['crop']] = {
                'score': rec['score'] * 0.6,
                'reasons': rec.get('reasons', [])
            }
        
        for rec in collab:
            crop = rec['crop']
            if crop in combined_scores:
                combined_scores[crop]['score'] += rec['score'] * 0.4
            else:
                combined_scores[crop] = {
                    'score': rec['score'] * 0.4,
                    'reasons': []
                }
        
        # Sort and separate
        sorted_crops = sorted(combined_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        return {
            'primary': [self._get_crop_details(item[0]) for item in sorted_crops[:3]],
            'secondary': [self._get_crop_details(item[0]) for item in sorted_crops[3:6]]
        }
    
    def _get_crop_details(self, crop_id: str) -> dict:
        """Get full crop details"""
        if crop_id in self.CROP_DATABASE:
            return {**self.CROP_DATABASE[crop_id], 'crop_id': crop_id}
        return {'crop_id': crop_id, 'name': crop_id.title()}
    
    def _get_recommendation_reasons(self, crop_id: str, profile: dict) -> list:
        """Explain why a crop is recommended"""
        reasons = []
        crop = self.CROP_DATABASE.get(crop_id, {})
        
        soil = profile.get('soil_type', '')
        if soil in crop.get('soil_types', []):
            reasons.append(f"Suitable for {soil} soil")
        
        if profile.get('irrigation_available'):
            if crop.get('water_requirement', '').startswith('High'):
                reasons.append("Good irrigation available")
        
        profit = crop.get('profit_range', '')
        if profit:
            reasons.append(f"Profit potential: ₹{profit}")
        
        return reasons
    
    def _generate_seasonal_plan(self, profile: dict, recommendations: dict) -> dict:
        """Generate personalized seasonal farming plan"""
        current_month = datetime.now().month
        
        # Determine season
        if current_month in [6, 7, 8, 9]:
            season = 'Kharif'
        elif current_month in [10, 11, 12, 1, 2, 3]:
            season = 'Rabi'
        else:
            season = 'Zaid'
        
        primary_crops = [r['crop_id'] for r in recommendations['primary'][:2]]
        
        plan = {
            'current_season': season,
            'months': {
                'month_1': {
                    'name': 'Soil Preparation',
                    'activities': [
                        'Soil testing and analysis',
                        'Land preparation and plowing',
                        'Apply organic manure',
                        'Create beds and furrows'
                    ]
                },
                'month_2': {
                    'name': 'Sowing/Planting',
                    'activities': [
                        f'Select quality seeds for {", ".join(primary_crops)}',
                        'Seed treatment with fungicides',
                        'Sowing at optimal depth',
                        'Initial irrigation'
                    ]
                },
                'month_3': {
                    'name': 'Crop Growth',
                    'activities': [
                        'Regular irrigation schedule',
                        'First fertilizer application',
                        'Weed control',
                        'Pest monitoring'
                    ]
                },
                'month_4': {
                    'name': 'Vegetative Growth',
                    'activities': [
                        'Second fertilizer application',
                        'Pest and disease management',
                        'Intercultural operations',
                        'Water management'
                    ]
                },
                'month_5': {
                    'name': 'Harvesting',
                    'activities': [
                        'Monitor crop maturity',
                        'Harvest at right stage',
                        'Post-harvest handling',
                        'Market preparation'
                    ]
                }
            }
        }
        
        return plan
    
    def _assess_farming_risk(self, profile: dict, recommendations: dict) -> dict:
        """Assess farming risk based on profile and recommendations"""
        risk_factors = []
        risk_score = 0
        
        # Land size risk
        if profile.get('land_size', 0) < 2:
            risk_factors.append('Small land size limits economy of scale')
            risk_score += 20
        
        # Budget risk
        if profile.get('budget', 0) < 30000:
            risk_factors.append('Limited budget may restrict optimal inputs')
            risk_score += 25
        
        # Experience risk
        if profile.get('experience_years', 5) < 3:
            risk_factors.append('Limited experience - start with easier crops')
            risk_score += 15
        
        # Crop-specific risks
        for crop in recommendations.get('primary', [])[:2]:
            if crop.get('diseases'):
                risk_score += 10
                risk_factors.append(f"{crop['name']} has common disease risks")
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_level': 'Low' if risk_score < 30 else 'Medium' if risk_score < 60 else 'High',
            'factors': risk_factors,
            'mitigation': self._get_risk_mitigation(risk_factors)
        }
    
    def _get_risk_mitigation(self, factors: list) -> list:
        """Get risk mitigation strategies"""
        mitigation = []
        
        if any('budget' in f.lower() for f in factors):
            mitigation.append('Start with low-investment crops like vegetables')
            mitigation.append('Look for government subsidies and schemes')
        
        if any('experience' in f.lower() for f in factors):
            mitigation.append('Consult local agricultural extension')
            mitigation.append('Start small and scale up gradually')
        
        if any('disease' in f.lower() for f in factors):
            mitigation.append('Use disease-resistant varieties')
            mitigation.append('Follow IPM practices')
        
        return mitigation
    
    def _estimate_returns(self, profile: dict, recommendations: dict) -> dict:
        """Estimate expected returns"""
        land = profile.get('land_size', 1)
        
        returns = {
            'conservative': 0,
            'moderate': 0,
            'optimistic': 0
        }
        
        for crop_rec in recommendations.get('primary', [])[:2]:
            crop = self.CROP_DATABASE.get(crop_rec['crop_id'], {})
            profit_range = crop.get('profit_range', '0-0').split('-')
            
            if len(profit_range) == 2:
                min_profit = int(profit_range[0])
                max_profit = int(profit_range[1])
                
                returns['conservative'] += min_profit * land * 0.7
                returns['moderate'] += (min_profit + max_profit) / 2 * land * 0.8
                returns['optimistic'] += max_profit * land
        
        return {
            'conservative': round(returns['conservative']),
            'moderate': round(returns['moderate']),
            'optimistic': round(returns['optimistic']),
            'per_acre': {
                'conservative': round(returns['conservative'] / land) if land > 0 else 0,
                'moderate': round(returns['moderate'] / land) if land > 0 else 0,
                'optimistic': round(returns['optimistic'] / land) if land > 0 else 0
            }
        }


# Factory function
def create_crop_advisor() -> CropAdvisor:
    """Create and return a crop advisor instance"""
    return CropAdvisor()


if __name__ == "__main__":
    advisor = create_crop_advisor()
    print("Crop Advisor initialized successfully!")
    
    # Test with sample profile
    profile = {
        'name': 'Rama Rao',
        'land_size': 5,
        'soil_type': 'clay',
        'budget': 75000,
        'location': 'andhra_pradesh',
        'irrigation_available': True,
        'experience_years': 10
    }
    
    result = advisor.get_recommendations(profile=profile)
    print(f"\nRecommendations for {profile['name']}:")
    for crop in result['primary_recommendations'][:2]:
        print(f"  - {crop['name']}: ₹{crop['profit_range']}")
