"use client";

import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { useLang } from "@/lib/language";

function getCurrentSeason() {
  const month = new Date().getMonth();
  if (month >= 5 && month <= 9) return "kharif";
  if (month >= 10 || month <= 1) return "rabi";
  return "zaid";
}

const SEASON_INFO = {
  kharif: {
    crops: ["Rice", "Cotton", "Maize", "Soybean", "Groundnut"],
    tasks: ["Prepare nursery beds", "Check monsoon forecast", "Apply basal fertilizer", "Ensure drainage channels are clear"],
    color: "#2E7D32",
  },
  rabi: {
    crops: ["Wheat", "Mustard", "Chickpea", "Potato", "Peas"],
    tasks: ["Prepare land after kharif harvest", "Plan irrigation schedule", "Seed treatment before sowing", "Apply FYM/compost"],
    color: "#1565C0",
  },
  zaid: {
    crops: ["Watermelon", "Cucumber", "Moong", "Sunflower", "Vegetables"],
    tasks: ["Ensure water availability", "Use mulching to conserve moisture", "Plan short-duration crops", "Monitor for summer pests"],
    color: "#E65100",
  },
};

export default function DashboardPage() {
  const router = useRouter();
  const { T, lang } = useLang();
  const [weather, setWeather] = useState<{ temp: number; desc: string } | null>(null);

  const season = getCurrentSeason();
  const info = SEASON_INFO[season];
  const dateStr = new Date().toLocaleDateString(lang === "Telugu" ? "te-IN" : lang === "Hindi" ? "hi-IN" : "en-IN", {
    weekday: "long", year: "numeric", month: "long", day: "numeric",
  });
  const seasonLabel = { kharif: { English: "Kharif", Hindi: "खरीफ", Telugu: "ఖరీఫ్" }, rabi: { English: "Rabi", Hindi: "रबी", Telugu: "రబీ" }, zaid: { English: "Zaid", Hindi: "जायद", Telugu: "జైద్" } };

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (pos) => {
        try {
          const { latitude, longitude } = pos.coords;
          const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`);
          const data = await r.json();
          const cw = data.current_weather;
          const codes: Record<number, string> = { 0: "☀️ Clear", 1: "🌤️ Mostly Clear", 2: "⛅ Partly Cloudy", 3: "☁️ Overcast", 45: "🌫️ Fog", 51: "🌦️ Drizzle", 61: "🌧️ Rain", 63: "🌧️ Moderate Rain", 65: "🌧️ Heavy Rain", 80: "🌦️ Showers", 95: "⛈️ Storm" };
          setWeather({ temp: Math.round(cw.temperature), desc: codes[cw.weathercode] || "🌤️" });
        } catch { /* silent */ }
      }, () => {});
    }
  }, []);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Hero */}
      <div className="liquidGlass-wrapper mb-6" style={{ borderRadius: "1.25rem", padding: 0, cursor: "default", background: "linear-gradient(135deg, #166534, #15803d, #22c55e)" }}>
        <div className="liquidGlass-effect" style={{ background: "rgba(255,255,255,0.1)" }} />
        <div className="liquidGlass-tint" />
        <div className="liquidGlass-shine" />
        <div className="liquidGlass-text" style={{ padding: "1.5rem", color: "white", position: "relative", zIndex: 3 }}>
          <div className="flex justify-between items-start flex-wrap gap-4">
            <div>
              <h2 style={{ fontSize: "1.75rem", fontWeight: 700 }}>📊 {T("farmDashboard")}</h2>
              <p style={{ marginTop: "0.25rem", opacity: 0.8, fontSize: "0.875rem" }}>{dateStr}</p>
              <p style={{ marginTop: "0.5rem", opacity: 0.9 }}>
                🌾 {lang === "Telugu" ? "సీజన్" : lang === "Hindi" ? "मौसम" : "Season"}: <strong>{seasonLabel[season][lang]}</strong>
              </p>
            </div>
            {weather && (
              <div style={{ textAlign: "right" }}>
                <p style={{ fontSize: "1.5rem", fontWeight: 700 }}>{weather.temp}°C</p>
                <p style={{ opacity: 0.85, fontSize: "0.875rem" }}>{weather.desc}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {[
          { label: `🔬 ${T("scanDisease")}`, path: "/disease-scanner" },
          { label: `📈 ${T("marketPrices")}`, path: "/market" },
          { label: `💬 ${T("aiChatbot")}`, path: "/chatbot" },
        ].map((btn) => (
          <div key={btn.path} className="liquidGlass-wrapper" style={{ cursor: "pointer" }}>
            <div className="liquidGlass-effect" />
            <div className="liquidGlass-tint" />
            <div className="liquidGlass-shine" />
            <button onClick={() => router.push(btn.path)} className="liquidGlass-text"
              style={{ width: "100%", padding: "0.875rem", fontSize: "0.875rem", fontWeight: 600, textAlign: "center", color: "#1A6B2C", background: "transparent", border: "none", cursor: "pointer", fontFamily: "inherit" }}>
              {btn.label}
            </button>
          </div>
        ))}
      </div>

      {/* Season Crops + Tasks */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="liquidGlass-wrapper" style={{ cursor: "default" }}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "1.25rem" }}>
            <h3 style={{ fontSize: "0.9375rem", fontWeight: 600, color: info.color, marginBottom: "0.75rem" }}>
              🌾 {lang === "Telugu" ? `${seasonLabel[season][lang]} పంటలు` : lang === "Hindi" ? `${seasonLabel[season][lang]} फसलें` : `${seasonLabel[season][lang]} Season Crops`}
            </h3>
            <div className="flex flex-wrap gap-2">
              {info.crops.map((crop) => (
                <span key={crop} style={{ background: "rgba(34,197,94,0.1)", color: "#166534", padding: "0.375rem 0.75rem", borderRadius: "9999px", fontSize: "0.8125rem", fontWeight: 500 }}>{crop}</span>
              ))}
            </div>
          </div>
        </div>

        <div className="liquidGlass-wrapper" style={{ cursor: "default" }}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "1.25rem" }}>
            <h3 style={{ fontSize: "0.9375rem", fontWeight: 600, color: "rgba(0,0,0,0.7)", marginBottom: "0.75rem" }}>
              ✅ {lang === "Telugu" ? "ఈ సీజన్ పనులు" : lang === "Hindi" ? "इस मौसम के कार्य" : "Seasonal Tasks"}
            </h3>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {info.tasks.map((task, i) => (
                <li key={i} style={{ padding: "0.375rem 0", fontSize: "0.8125rem", color: "rgba(0,0,0,0.65)", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <span style={{ color: "#22c55e" }}>○</span> {task}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Weather Advisory + Ask AI */}
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div className="liquidGlass-wrapper" style={{ cursor: "default" }}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "1.25rem" }}>
            <h3 style={{ fontSize: "0.9375rem", fontWeight: 600, color: "rgba(0,0,0,0.7)", marginBottom: "0.75rem" }}>
              🌤️ {lang === "Telugu" ? "వాతావరణ సలహా" : lang === "Hindi" ? "मौसम सलाह" : "Weather Advisory"}
            </h3>
            {weather ? (
              <div style={{ padding: "0.75rem", background: "rgba(34,197,94,0.08)", borderRadius: "0.75rem", fontSize: "0.8125rem", color: "#166534" }}>
                {weather.temp > 35
                  ? (lang === "Telugu" ? "⚠️ అధిక ఉష్ణోగ్రత — ఉదయం/సాయంత్రం నీరు పెట్టండి, మల్చింగ్ వాడండి" : lang === "Hindi" ? "⚠️ अधिक तापमान — सुबह/शाम सिंचाई करें, मल्चिंग करें" : "⚠️ High temp — irrigate morning/evening, use mulching")
                  : weather.temp < 10
                  ? (lang === "Telugu" ? "❄️ చల్లని వాతావరణం — పంటలను కప్పండి, మంచు నుండి రక్షించండి" : lang === "Hindi" ? "❄️ ठंड — फसलों को ढकें, पाले से बचाएं" : "❄️ Cold — cover crops, protect from frost")
                  : (lang === "Telugu" ? "✅ వ్యవసాయానికి అనుకూల వాతావరణం. పంట పనులు కొనసాగించండి." : lang === "Hindi" ? "✅ खेती के लिए अनुकूल मौसम। फसल कार्य जारी रखें।" : "✅ Favorable weather. Continue farm operations normally.")}
              </div>
            ) : (
              <p style={{ fontSize: "0.8125rem", color: "rgba(0,0,0,0.4)" }}>
                {lang === "Telugu" ? "లొకేషన్ అనుమతి ఇవ్వండి" : lang === "Hindi" ? "लोकेशन अनुमति दें" : "Allow location for weather advisory"}
              </p>
            )}
          </div>
        </div>

        <div className="liquidGlass-wrapper" style={{ cursor: "pointer" }} onClick={() => router.push("/chatbot")}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "1.25rem" }}>
            <h3 style={{ fontSize: "0.9375rem", fontWeight: 600, color: "rgba(0,0,0,0.7)", marginBottom: "0.75rem" }}>
              🤖 {lang === "Telugu" ? "AI ని అడగండి" : lang === "Hindi" ? "AI से पूछें" : "Ask AI Anything"}
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {(lang === "Telugu"
                ? ["నా పంటకు ఏ ఎరువు వాడాలి?", "ధర ఎప్పుడు పెరుగుతుంది?", "వ్యాధి నివారణ ఎలా?"]
                : lang === "Hindi"
                ? ["मेरी फसल को कौन सा खाद दें?", "भाव कब बढ़ेगा?", "बीमारी कैसे रोकें?"]
                : ["What fertilizer for my crop?", "When will prices rise?", "How to prevent disease?"]
              ).map((q) => (
                <div key={q} style={{ padding: "0.5rem 0.75rem", background: "rgba(34,197,94,0.08)", borderRadius: "0.5rem", fontSize: "0.8125rem", color: "#166534" }}>
                  💬 {q}
                </div>
              ))}
            </div>
            <p style={{ marginTop: "0.75rem", fontSize: "0.75rem", color: "rgba(0,0,0,0.4)" }}>
              {lang === "Telugu" ? "క్లిక్ చేసి చాట్ చేయండి →" : lang === "Hindi" ? "क्लिक करके चैट करें →" : "Click to chat →"}
            </p>
          </div>
        </div>
      </div>

      {/* Tip */}
      <div className="liquidGlass-wrapper" style={{ cursor: "default" }}>
        <div className="liquidGlass-effect" />
        <div className="liquidGlass-tint" />
        <div className="liquidGlass-shine" />
        <div className="liquidGlass-text" style={{ padding: "1rem", fontSize: "0.875rem", color: "#1565C0" }}>
          💡 <strong>{T("farmingTip")}</strong> {info.tasks[Math.floor(Math.random() * info.tasks.length)]}
        </div>
      </div>
    </div>
  );
}
