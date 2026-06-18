"use client";

import { createContext, useContext, useState, ReactNode } from "react";

export type Lang = "English" | "Hindi" | "Telugu";

const t = {
  // Sidebar / Nav
  dashboard: { English: "Dashboard", Hindi: "डैशबोर्ड", Telugu: "డాష్‌బోర్డ్" },
  aiAdvisor: { English: "AI Advisor", Hindi: "AI सलाहकार", Telugu: "AI సలహాదారు" },
  diseaseScanner: { English: "Disease Scanner", Hindi: "रोग स्कैनर", Telugu: "వ్యాధి స్కానర్" },
  marketIntelligence: { English: "Market Intelligence", Hindi: "बाज़ार जानकारी", Telugu: "మార్కెట్ ఇంటెలిజెన్స్" },
  aiChatbot: { English: "AI Chatbot", Hindi: "AI चैटबॉट", Telugu: "AI చాట్‌బాట్" },
  feedback: { English: "Feedback", Hindi: "प्रतिक्रिया", Telugu: "ఫీడ్‌బ్యాక్" },
  logout: { English: "Logout", Hindi: "लॉग आउट", Telugu: "లాగ్ అవుట్" },
  // Dashboard
  farmDashboard: { English: "Farm Intelligence Dashboard", Hindi: "कृषि इंटेलिजेंस डैशबोर्ड", Telugu: "వ్యవసాయ ఇంటెలిజెన్స్ డాష్‌బోర్డ్" },
  welcomeMsg: { English: "Welcome to your centralized farm management command center.", Hindi: "आपके केंद्रीकृत कृषि प्रबंधन कमांड सेंटर में आपका स्वागत है।", Telugu: "మీ కేంద్రీకృత వ్యవసాయ నిర్వహణ కమాండ్ సెంటర్‌కు స్వాగతం." },
  cropAdvice: { English: "Crop Advice", Hindi: "फसल सलाह", Telugu: "పంట సలహా" },
  scanDisease: { English: "Scan Disease", Hindi: "रोग स्कैन", Telugu: "వ్యాధి స్కాన్" },
  marketPrices: { English: "Market Prices", Hindi: "बाज़ार भाव", Telugu: "మార్కెట్ ధరలు" },
  weather: { English: "Weather", Hindi: "मौसम", Telugu: "వాతావరణం" },
  systemStatus: { English: "System Status", Hindi: "सिस्टम स्थिति", Telugu: "సిస్టమ్ స్థితి" },
  online: { English: "Online", Hindi: "ऑनलाइन", Telugu: "ఆన్‌లైన్" },
  allNominal: { English: "All systems nominal", Hindi: "सभी सिस्टम सामान्य", Telugu: "అన్ని సిస్టమ్‌లు సాధారణం" },
  activeCrops: { English: "Active Crops", Hindi: "सक्रिय फसलें", Telugu: "యాక్టివ్ పంటలు" },
  monitored: { English: "Monitored", Hindi: "निगरानी में", Telugu: "పర్యవేక్షించబడుతోంది" },
  aiAnalyses: { English: "AI Analyses", Hindi: "AI विश्लेषण", Telugu: "AI విశ్లేషణలు" },
  totalRun: { English: "Total run", Hindi: "कुल चलाए", Telugu: "మొత్తం రన్" },
  marketAlerts: { English: "Market Alerts", Hindi: "बाज़ार अलर्ट", Telugu: "మార్కెట్ అలర్ట్‌లు" },
  active: { English: "Active", Hindi: "सक्रिय", Telugu: "యాక్టివ్" },
  marketTrends: { English: "Market Trends (Last 7 Days)", Hindi: "बाज़ार रुझान (पिछले 7 दिन)", Telugu: "మార్కెట్ ట్రెండ్‌లు (గత 7 రోజులు)" },
  resourceUsage: { English: "Resource Usage", Hindi: "संसाधन उपयोग", Telugu: "వనరుల వినియోగం" },
  farmingTip: { English: "Today's Farming Tip:", Hindi: "आज की खेती टिप:", Telugu: "నేటి వ్యవసాయ చిట్కా:" },
  // Chatbot
  chatTitle: { English: "AI Farming Chatbot", Hindi: "AI कृषि चैटबॉट", Telugu: "AI వ్యవసాయ చాట్‌బాట్" },
  chatSubtitle: { English: "Ask any farming question and get an instant AI-powered answer.", Hindi: "कोई भी खेती का सवाल पूछें और तुरंत AI उत्तर पाएं।", Telugu: "ఏదైనా వ్యవసాయ ప్రశ్న అడగండి మరియు తక్షణ AI సమాధానం పొందండి." },
  chatPlaceholder: { English: "Ask about crops, soil, weather, market tips...", Hindi: "फसल, मिट्टी, मौसम, बाज़ार टिप्स के बारे में पूछें...", Telugu: "పంటలు, నేల, వాతావరణం, మార్కెట్ చిట్కాల గురించి అడగండి..." },
  send: { English: "Send", Hindi: "भेजें", Telugu: "పంపు" },
  chatWelcome: { English: "Hello! I'm your AI farming assistant. Ask me anything about crops, soil, market prices, or farming techniques! 🌾", Hindi: "नमस्ते! मैं आपका AI कृषि सहायक हूँ। फसलों, मिट्टी, बाज़ार भाव या खेती तकनीकों के बारे में कुछ भी पूछें! 🌾", Telugu: "నమస్కారం! నేను మీ AI వ్యవసాయ సహాయకుడిని. పంటలు, నేల, మార్కెట్ ధరలు లేదా వ్యవసాయ పద్ధతుల గురించి ఏదైనా అడగండి! 🌾" },
  // Advisor
  advisorTitle: { English: "AI Farming Advisor", Hindi: "AI कृषि सलाहकार", Telugu: "AI వ్యవసాయ సలహాదారు" },
  advisorSubtitle: { English: "Get personalized crop recommendations based on your specific farm conditions.", Hindi: "अपनी खेत की स्थिति के अनुसार व्यक्तिगत फसल सिफारिशें प्राप्त करें।", Telugu: "మీ నిర్దిష్ట పొలం పరిస్థితుల ఆధారంగా వ్యక్తిగత పంట సిఫార్సులు పొందండి." },
  farmParams: { English: "Farm Parameters", Hindi: "खेत पैरामीटर", Telugu: "పొలం పారామీటర్లు" },
  soilType: { English: "Soil Type", Hindi: "मिट्टी का प्रकार", Telugu: "నేల రకం" },
  landSize: { English: "Land Size (acres)", Hindi: "भूमि का आकार (एकड़)", Telugu: "భూమి పరిమాణం (ఎకరాలు)" },
  season: { English: "Season", Hindi: "मौसम", Telugu: "సీజన్" },
  budget: { English: "Budget (₹)", Hindi: "बजट (₹)", Telugu: "బడ్జెట్ (₹)" },
  getRecommendations: { English: "Get Crop Recommendations", Hindi: "फसल सिफारिशें प्राप्त करें", Telugu: "పంట సిఫార్సులు పొందండి" },
  analyzing: { English: "AI analyzing your farm data...", Hindi: "AI आपके खेत का विश्लेषण कर रहा है...", Telugu: "AI మీ పొలం డేటాను విశ్లేషిస్తోంది..." },
  // Disease Scanner
  diseaseScannerTitle: { English: "AI Disease Scanner", Hindi: "AI रोग स्कैनर", Telugu: "AI వ్యాధి స్కానర్" },
  diseaseScannerSubtitle: { English: "Upload a leaf image for AI-powered disease detection and treatment recommendations.", Hindi: "AI-संचालित रोग पहचान और उपचार सिफारिशों के लिए पत्ती की छवि अपलोड करें।", Telugu: "AI-ఆధారిత వ్యాధి గుర్తింపు మరియు చికిత్స సిఫార్సుల కోసం ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి." },
  uploadImage: { English: "Upload Image", Hindi: "छवि अपलोड करें", Telugu: "చిత్రాన్ని అప్‌లోడ్ చేయండి" },
  cropType: { English: "Crop Type", Hindi: "फसल का प्रकार", Telugu: "పంట రకం" },
  analyzeDisease: { English: "Analyze for Disease", Hindi: "रोग के लिए विश्लेषण करें", Telugu: "వ్యాధి కోసం విశ్లేషించండి" },
  aiDiagnosis: { English: "AI Diagnosis", Hindi: "AI निदान", Telugu: "AI రోగ నిర్ధారణ" },
  uploadPrompt: { English: "Upload an image of a leaf on the left to see the AI diagnosis here.", Hindi: "AI निदान देखने के लिए बाईं ओर पत्ती की छवि अपलोड करें।", Telugu: "AI రోగ నిర్ధారణ చూడటానికి ఎడమ వైపు ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి." },
  clickUpload: { English: "Click to upload leaf/crop image", Hindi: "पत्ती/फसल छवि अपलोड करने के लिए क्लिक करें", Telugu: "ఆకు/పంట చిత్రాన్ని అప్‌లోడ్ చేయడానికి క్లిక్ చేయండి" },
  // Market
  marketTitle: { English: "Market Intelligence", Hindi: "बाज़ार जानकारी", Telugu: "మార్కెట్ ఇంటెలిజెన్స్" },
  marketSubtitle: { English: "AI-powered crop price predictions and market analysis.", Hindi: "AI-संचालित फसल मूल्य भविष्यवाणी और बाज़ार विश्लेषण।", Telugu: "AI-ఆధారిత పంట ధర అంచనాలు మరియు మార్కెట్ విశ్లేషణ." },
  selectCrop: { English: "Select Crop", Hindi: "फसल चुनें", Telugu: "పంట ఎంచుకోండి" },
  forecastDays: { English: "Forecast Days", Hindi: "पूर्वानुमान दिन", Telugu: "అంచనా రోజులు" },
  getPrediction: { English: "Get Price Prediction", Hindi: "मूल्य भविष्यवाणी प्राप्त करें", Telugu: "ధర అంచనా పొందండి" },
  // Feedback
  feedbackTitle: { English: "Feedback", Hindi: "प्रतिक्रिया", Telugu: "ఫీడ్‌బ్యాక్" },
  feedbackSubtitle: { English: "Help us improve Trinetra Agro AI with your feedback.", Hindi: "अपनी प्रतिक्रिया से त्रिनेत्र एग्रो AI को बेहतर बनाने में मदद करें।", Telugu: "మీ ఫీడ్‌బ్యాక్‌తో త్రినేత్ర అగ్రో AIని మెరుగుపరచడంలో సహాయపడండి." },
  selectFeature: { English: "Feature", Hindi: "सुविधा", Telugu: "ఫీచర్" },
  rating: { English: "Rating", Hindi: "रेटिंग", Telugu: "రేటింగ్" },
  comment: { English: "Comment", Hindi: "टिप्पणी", Telugu: "వ్యాఖ్య" },
  submit: { English: "Submit", Hindi: "जमा करें", Telugu: "సమర్పించు" },
  // Language
  language: { English: "Language", Hindi: "भाषा", Telugu: "భాష" },
  // New sidebar labels
  farmTools: { English: "Farm Tools", Hindi: "कृषि उपकरण", Telugu: "వ్యవసాయ సాధనాలు" },
  farmAssistant: { English: "Farm Assistant", Hindi: "कृषि सहायक", Telugu: "వ్యవసాయ సహాయకుడు" },
  farmProfile: { English: "Farm Profile", Hindi: "कृषि प्रोफ़ाइल", Telugu: "వ్యవసాయ ప్రొఫైల్" },
  // Tools page
  toolsTitle: { English: "Farm Tools", Hindi: "कृषि उपकरण", Telugu: "వ్యవసాయ సాధనాలు" },
  toolsDesc: { English: "Calculators and decision tools for your farm", Hindi: "आपके खेत के लिए कैलकुलेटर और निर्णय उपकरण", Telugu: "మీ పొలం కోసం కాలిక్యులేటర్లు మరియు నిర్ణయ సాధనాలు" },
  tabAdvisor: { English: "Crop Advisor", Hindi: "फसल सलाहकार", Telugu: "పంట సలహాదారు" },
  tabRisk: { English: "Risk Calculator", Hindi: "जोखिम कैलकुलेटर", Telugu: "రిస్క్ కాలిక్యులేటర్" },
  tabYield: { English: "Yield Estimator", Hindi: "उपज अनुमानक", Telugu: "దిగుబడి అంచనాదారు" },
  tabAdvisorDesc: { English: "Find the best crops for your soil and budget", Hindi: "अपनी मिट्टी और बजट के लिए सर्वोत्तम फसलें खोजें", Telugu: "మీ నేల మరియు బడ్జెట్ కోసం ఉత్తమ పంటలను కనుగొనండి" },
  tabRiskDesc: { English: "Estimate crop failure risk factors", Hindi: "फसल विफलता जोखिम कारकों का अनुमान लगाएं", Telugu: "పంట వైఫల్య రిస్క్ కారకాలను అంచనా వేయండి" },
  tabYieldDesc: { English: "Estimate expected harvest output", Hindi: "अपेक्षित फसल उत्पादन का अनुमान लगाएं", Telugu: "ఊహించిన పంట దిగుబడిని అంచనా వేయండి" },
  analyzing2: { English: "Analyzing...", Hindi: "विश्लेषण हो रहा है...", Telugu: "విశ్లేషిస్తోంది..." },
  calculateRisk: { English: "Calculate Risk", Hindi: "जोखिम की गणना करें", Telugu: "రిస్క్ లెక్కించండి" },
  calculating: { English: "Calculating...", Hindi: "गणना हो रही है...", Telugu: "లెక్కిస్తోంది..." },
  estimateYield: { English: "Estimate Yield", Hindi: "उपज का अनुमान लगाएं", Telugu: "దిగుబడి అంచనా వేయండి" },
  estimating: { English: "Estimating...", Hindi: "अनुमान लग रहा है...", Telugu: "అంచనా వేస్తోంది..." },
  annualRainfall: { English: "Annual Rainfall (mm)", Hindi: "वार्षिक वर्षा (मिमी)", Telugu: "వార్షిక వర్షపాతం (మిమీ)" },
  hasIrrigation: { English: "Has Irrigation", Hindi: "सिंचाई उपलब्ध", Telugu: "నీటి పారుదల ఉంది" },
  area: { English: "Area (acres)", Hindi: "क्षेत्र (एकड़)", Telugu: "విస్తీర్ణం (ఎకరాలు)" },
  fertilizer: { English: "Fertilizer", Hindi: "उर्वरक", Telugu: "ఎరువు" },
  expected: { English: "Expected", Hindi: "अनुमानित", Telugu: "అంచనా" },
  conservative: { English: "Conservative", Hindi: "न्यूनतम", Telugu: "కనిష్ట" },
  optimistic: { English: "Optimistic", Hindi: "अधिकतम", Telugu: "గరిష్ట" },
  recommendation: { English: "Recommendation", Hindi: "सिफारिश", Telugu: "సిఫార్సు" },
  riskScore: { English: "Risk Score", Hindi: "जोखिम स्कोर", Telugu: "రిస్క్ స్కోర్" },
  tryAdjust: { English: "Try adjusting your inputs and running again.", Hindi: "अपने इनपुट समायोजित करके पुनः प्रयास करें।", Telugu: "మీ ఇన్‌పుట్‌లను సర్దుబాటు చేసి మళ్లీ ప్రయత్నించండి." },
  basedOnInputs: { English: "Based on your inputs, consider crops suited for", Hindi: "आपके इनपुट के अनुसार, इन फसलों पर विचार करें:", Telugu: "మీ ఇన్‌పుట్‌ల ఆధారంగా, ఈ పంటలను పరిగణించండి:" },
  // Profile page
  profileTitle: { English: "Farm Profile", Hindi: "कृषि प्रोफ़ाइल", Telugu: "వ్యవసాయ ప్రొఫైల్" },
  profileSubtitle: { English: "Manage your farm details, land, and crop preferences.", Hindi: "अपने खेत का विवरण, भूमि और फसल प्राथमिकताएं प्रबंधित करें।", Telugu: "మీ పొలం వివరాలు, భూమి మరియు పంట ప్రాధాన్యతలను నిర్వహించండి." },
  saveProfile: { English: "Save Profile", Hindi: "प्रोफ़ाइल सहेजें", Telugu: "ప్రొఫైల్ సేవ్ చేయండి" },
  saving: { English: "Saving...", Hindi: "सहेज रहे हैं...", Telugu: "సేవ్ చేస్తోంది..." },
  state: { English: "State", Hindi: "राज्य", Telugu: "రాష్ట్రం" },
  district: { English: "District", Hindi: "जिला", Telugu: "జిల్లా" },
  profileSaved: { English: "Profile saved!", Hindi: "प्रोफ़ाइल सहेज ली गई!", Telugu: "ప్రొఫైల్ సేవ్ చేయబడింది!" },
  // Crop Calendar
  cropCalendar: { English: "Crop Calendar", Hindi: "फसल कैलेंडर", Telugu: "పంట క్యాలెండర్" },
  cropCalendarDesc: { English: "Week-by-week guide from sowing to harvest with irrigation, fertilizer, and pest advice.", Hindi: "बुवाई से कटाई तक सप्ताह-दर-सप्ताह मार्गदर्शिका — सिंचाई, उर्वरक और कीट सलाह के साथ।", Telugu: "నాట్ల నుండి పంట వరకు వారం-వారం గైడ్ — నీటిపారుదల, ఎరువు మరియు చీడ సలహాతో." },
  sowingDate: { English: "Sowing Date", Hindi: "बुवाई तिथि", Telugu: "నాట్ల తేదీ" },
  generateCalendar: { English: "Generate Calendar", Hindi: "कैलेंडर बनाएं", Telugu: "క్యాలెండర్ రూపొందించండి" },
  expectedHarvest: { English: "Expected Harvest", Hindi: "अपेक्षित फसल", Telugu: "అంచనా పంట" },
  totalWeeks: { English: "Total Weeks", Hindi: "कुल सप्ताह", Telugu: "మొత్తం వారాలు" },
  week: { English: "Week", Hindi: "सप्ताह", Telugu: "వారం" },
  irrigation: { English: "Irrigation", Hindi: "सिंचाई", Telugu: "నీటిపారుదల" },
  pestManagement: { English: "Pest Management", Hindi: "कीट प्रबंधन", Telugu: "చీడ నిర్వహణ" },
  tip: { English: "Tip", Hindi: "सुझाव", Telugu: "చిట్కా" },
  crop: { English: "Crop", Hindi: "फसल", Telugu: "పంట" },
  loading: { English: "Loading...", Hindi: "लोड हो रहा है...", Telugu: "లోడ్ అవుతోంది..." },
} as const;

export type TKey = keyof typeof t;

interface LangContextType {
  lang: Lang;
  setLang: (l: Lang) => void;
  T: (key: TKey) => string;
}

const LangContext = createContext<LangContextType>({
  lang: "English",
  setLang: () => {},
  T: (key) => t[key]["English"],
});

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Lang>("English");
  const T = (key: TKey) => t[key][lang] || t[key]["English"];
  return (
    <LangContext.Provider value={{ lang, setLang, T }}>
      {children}
    </LangContext.Provider>
  );
}

export function useLang() {
  return useContext(LangContext);
}
