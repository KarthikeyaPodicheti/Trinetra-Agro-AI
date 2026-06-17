// Auth
export interface UserCreate {
  email: string;
  password: string;
  full_name?: string;
  phone?: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserResponse {
  id: string;
  email: string;
  full_name?: string;
  phone?: string;
  is_active: boolean;
  created_at: string;
}

// AI Features
export interface AdvisorRequest {
  soil_type: string;
  land_acres: number;
  budget: number;
  season: string;
}

export interface CropRecommendation {
  name: string;
  score: number;
  season: string;
  duration: string;
  water_requirement: string;
  profit_range: string;
  diseases?: string[];
}

export interface AdvisorResponse {
  success: boolean;
  primary_recommendations: CropRecommendation[];
  expected_returns: {
    conservative: number;
    moderate: number;
    optimistic: number;
  };
  error?: string;
}

export interface MarketRequest {
  crop: string;
  days: number;
  location?: string;
}

export interface MarketResponse {
  success: boolean;
  current_price: number;
  predictions: {
    dates: string[];
    prices: number[];
    moving_avg: number[];
  };
  trend: string;
  recommendation: {
    action: string;
    message: string;
  };
  market_tips?: string[];
  error?: string;
}

export interface DiseaseResponse {
  success: boolean;
  disease: string;
  confidence: number;
  severity?: string;
  recommendation?: string;
  prevention_tips?: string[] | string;
  note?: string;
  error?: string;
}

export interface ChatRequest {
  message: string;
  session_id: string;
}

export interface ChatResponse {
  reply: string;
  session_id: string;
}

export interface FeedbackRequest {
  feature: string;
  rating: number;
  comment: string;
}

export interface ApiError {
  detail: string;
}
