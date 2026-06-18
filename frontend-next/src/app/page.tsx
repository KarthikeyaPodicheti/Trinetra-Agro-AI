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

const SEASON_INFO: Record<string, { crops: string[]; tasks: string[]; color: string; defaultCrop: string }> = {
  kharif: { crops: ["Rice", "Cotton", "Maize", "Soybean", "Groundnut"], tasks: ["Prepare nursery beds", "Check monsoon forecast", "Apply basal fertilizer", "Ensure drainage channels are clear"], color: "#2E7D32", defaultCrop: "Cotton" },
  rabi: { crops: ["Wheat", "Mustard", "Chickpea", "Potato", "Peas"], tasks: ["Prepare land after kharif harvest", "Plan irrigation schedule", "Seed treatment before sowing", "Apply FYM/compost"], color: "#1565C0", defaultCrop: "Wheat" },
  zaid: { crops: ["Watermelon", "Cucumber", "Moong", "Sunflower", "Vegetables"], tasks: ["Ensure water availability", "Use mulching to conserve moisture", "Plan short-duration crops", "Monitor for summer pests"], color: "#E65100", defaultCrop: "Moong" },
};

export default function DashboardPage() {
  const router = useRouter();
  const { T, lang } = useLang();
  const [weather, setWeather] = useState<{ temp: number; desc: string } | null>(null);
  const [price, setPrice] = useState<{ crop: string; price: number; trend: string } | null>(null);
  const [stage, setStage] = useState<{ crop: string; stage: string; tip: string } | null>(null);
  const [schemes, setSchemes] = useState<{ count: number; top: string[] } | null>(null);

  const season = getCurrentSeason();
  const info = SEASON_INFO[season];
  const dateStr = new Date().toLocaleDateString(lang === "Telugu" ? "te-IN" : lang === "Hindi" ? "hi-IN" : "en-IN", { weekday: "long", year: "numeric", month: "long", day: "numeric" });
  const seasonLabel: Record<string, Record<string, string>> = { kharif: { English: "Kharif", Hindi: "खरीफ", Telugu: "ఖరీఫ్" }, rabi: { English: "Rabi", Hindi: "रबी", Telugu: "రబీ" }, zaid: { English: "Zaid", Hindi: "जायद", Telugu: "జైద్" } };

  useEffect(() => {
    const API = process.env.NEXT_PUBLIC_API_URL || "https://shirts-flexible-michelle-classes.trycloudflare.com";

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (pos) => {
        try {
          const { latitude, longitude } = pos.coords;
          const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`);
          const data = await r.json();
          const cw = data.current_weather;
          const codes: Record<number, string> = { 0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌦️", 61: "🌧️", 63: "🌧️", 65: "🌧️", 80: "🌦️", 95: "⛈️" };
          setWeather({ temp: Math.round(cw.temperature), desc: codes[cw.weathercode] || "🌤️" });
        } catch { /* offline */ }
      }, () => {});
    }

    fetch(`${API}/mandi/prices?crop=${info.defaultCrop}`)
      .then(r => r.json())
      .then(d => { if (d.current_price) setPrice({ crop: d.crop || info.defaultCrop, price: d.current_price, trend: d.trend || "stable" }); })
      .catch(() => {});

    fetch(`${API}/calendar/generate?crop=${info.defaultCrop}`)
      .then(r => r.json())
      .then(d => {
        if (d.timeline) {
          const today = new Date().toISOString().slice(0, 10);
          const current = d.timeline.find((s: any) => s.date_range.start <= today && s.date_range.end >= today);
          if (current) setStage({ crop: d.crop, stage: current.stage, tip: current.tip });
        }
      })
      .catch(() => {});

    fetch(`${API}/schemes/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: "Maharashtra", land_size_acres: 2, crop_type: info.defaultCrop }),
    })
      .then(r => r.json())
      .then(d => { if (d.eligible_count) setSchemes({ count: d.eligible_count, top: (d.eligible || []).slice(0, 3).map((s: any) => s.name) }); })
      .catch(() => {});
  }, []);

  const trendEmoji: Record<string, string> = { rising: "📈", falling: "📉", stable: "📊" };

  return (
    <div className="p-4 sm:p-6 w-full" style={{ maxWidth: "100vw" }}>

      {/* ==================== HERO ==================== */}
      <div className="liquidGlass-wrapper mb-4 sm:mb-5" style={{ borderRadius: "1rem", padding: 0, cursor: "default", background: `linear-gradient(135deg, ${info.color}, ${info.color}dd, #166534)` }}>
        <div className="liquidGlass-effect" style={{ background: "rgba(255,255,255,0.08)" }} />
        <div className="liquidGlass-tint" />
        <div className="liquidGlass-shine" />
        <div className="liquidGlass-text" style={{ padding: "clamp(1rem, 4vw, 1.5rem)", color: "white", position: "relative", zIndex: 3 }}>
          <div className="flex justify-between items-start flex-wrap gap-3">
            <div>
              <h2 style={{ fontSize: "clamp(1.25rem, 5vw, 1.75rem)", fontWeight: 700, lineHeight: 1.2 }}>📊 {T("farmDashboard")}</h2>
              <p style={{ marginTop: "0.25rem", opacity: 0.8, fontSize: "clamp(0.75rem, 2.8vw, 0.875rem)" }}>{dateStr}</p>
              <p style={{ marginTop: "0.375rem", opacity: 0.9, fontSize: "clamp(0.75rem, 2.8vw, 0.875rem)" }}>
                🌾 {lang === "Telugu" ? "సీజన్" : lang === "Hindi" ? "मौसम" : "Season"}: <strong>{seasonLabel[season][lang]}</strong>
              </p>
            </div>
            {weather && (
              <div style={{ textAlign: "right" }}>
                <p style={{ fontSize: "clamp(1.125rem, 4.5vw, 1.5rem)", fontWeight: 700, lineHeight: 1 }}>{weather.temp}°C</p>
                <p style={{ opacity: 0.85, fontSize: "clamp(0.75rem, 2.8vw, 0.875rem)" }}>{weather.desc}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ==================== GOVT SCHEMES BOX — standalone, prominent ==================== */}
      <div className="liquidGlass-wrapper mb-5 sm:mb-6" style={{ cursor: "pointer" }} onClick={() => router.push("/schemes")}>
        <div className="liquidGlass-effect" />
        <div className="liquidGlass-tint" />
        <div className="liquidGlass-shine" />
        <div className="liquidGlass-text" style={{ padding: "clamp(0.875rem, 3vw, 1.125rem)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", flexWrap: "wrap" }}>
            <span style={{ fontSize: "1.75rem", background: "linear-gradient(135deg, #F59E0B, #D97706)", color: "white", borderRadius: "0.75rem", padding: "0.5rem 0.625rem", lineHeight: 1 }}>🏛️</span>
            <div style={{ flex: 1, minWidth: 0 }}>
              <p style={{ fontSize: "clamp(0.875rem, 3vw, 1rem)", fontWeight: 700, color: "#1A1C19" }}>
                {lang === "Telugu" ? "🏛️ మీరు ప్రభుత్వ పథకాలకు అర్హులా?" : lang === "Hindi" ? "🏛️ क्या आप सरकारी योजनाओं के लिए पात्र हैं?" : "🏛️ Are you eligible for Govt Schemes?"}
              </p>
              <p style={{ fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", color: "rgba(0,0,0,0.5)", marginTop: "0.25rem" }}>
                {lang === "Telugu" ? "PM-KISAN, PMFBY, Kisan Credit Card వంటి 8 పథకాలకు మీ అర్హతను ఒకే క్లిక్‌లో తనిఖీ చేయండి." : lang === "Hindi" ? "PM-KISAN, PMFBY, किसान क्रेडिट कार्ड जैसी 8 योजनाओं के लिए एक क्लिक में अपनी पात्रता जांचें।" : "Check your eligibility for 8 schemes including PM-KISAN, PMFBY, Kisan Credit Card in one click."}
              </p>
            </div>
            <button onClick={(e) => { e.stopPropagation(); router.push("/schemes"); }}
              style={{ background: "linear-gradient(135deg, #F59E0B, #D97706)", color: "white", border: "none", borderRadius: "0.75rem", padding: "clamp(0.5rem, 2vw, 0.625rem) clamp(1rem, 3vw, 1.25rem)", fontSize: "clamp(0.75rem, 2.6vw, 0.875rem)", fontWeight: 600, cursor: "pointer", whiteSpace: "nowrap" }}>
              {lang === "Telugu" ? "తనిఖీ చేయండి →" : lang === "Hindi" ? "जांचें →" : "Check Now →"}
            </button>
          </div>

          {schemes && (
            <div style={{ marginTop: "0.75rem", paddingTop: "0.75rem", borderTop: "1px solid rgba(0,0,0,0.06)", display: "flex", flexWrap: "wrap", gap: "0.5rem", alignItems: "center" }}>
              <span style={{ background: "#22c55e", color: "white", padding: "0.2rem 0.5rem", borderRadius: "999px", fontSize: "clamp(0.625rem, 2vw, 0.6875rem)", fontWeight: 600 }}>
                ✅ {schemes.count}/8 {lang === "Telugu" ? "అర్హత" : lang === "Hindi" ? "पात्र" : "eligible"}
              </span>
              {schemes.top.map((name) => (
                <span key={name} style={{ background: "rgba(34,197,94,0.1)", color: "#166534", padding: "0.2rem 0.625rem", borderRadius: "999px", fontSize: "clamp(0.625rem, 2vw, 0.6875rem)", fontWeight: 500 }}>
                  {name}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ==================== QUICK ACTIONS ==================== */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3 mb-5 sm:mb-6">
        {[
          { label: `🔬 ${T("scanDisease")}`, path: "/disease-scanner" },
          { label: `📈 ${T("marketPrices")}`, path: "/market" },
          { label: `💬 ${T("aiChatbot")}`, path: "/chatbot" },
          { label: `📅 ${T("cropCalendar")}`, path: "/calendar" },
        ].map((btn) => (
          <div key={btn.path} className="liquidGlass-wrapper" style={{ cursor: "pointer" }}>
            <div className="liquidGlass-effect" />
            <div className="liquidGlass-tint" />
            <div className="liquidGlass-shine" />
            <button onClick={() => router.push(btn.path)} className="liquidGlass-text"
              style={{ width: "100%", minHeight: "44px", padding: "clamp(0.625rem, 2vw, 0.875rem)", fontSize: "clamp(0.75rem, 2.8vw, 0.875rem)", fontWeight: 600, textAlign: "center", color: "#1A6B2C", background: "transparent", border: "none", cursor: "pointer", fontFamily: "inherit" }}>
              {btn.label}
            </button>
          </div>
        ))}
      </div>

      {/* ==================== LIVE DATA CARDS ==================== */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3 mb-5 sm:mb-6">
        <div className="liquidGlass-wrapper" style={{ cursor: "pointer" }} onClick={() => router.push("/market")}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "clamp(0.75rem, 2.5vw, 1rem)", display: "flex", alignItems: "center", gap: "0.75rem", minHeight: "56px" }}>
            <span style={{ fontSize: "1.5rem" }}>💰</span>
            <div>
              <p style={{ fontSize: "clamp(0.6875rem, 2.2vw, 0.75rem)", fontWeight: 500, color: "rgba(0,0,0,0.5)" }}>
                {lang === "Telugu" ? "నేటి ధర" : lang === "Hindi" ? "आज का भाव" : "Today's Price"}
              </p>
              {price ? (
                <p style={{ fontSize: "clamp(0.9375rem, 3vw, 1.0625rem)", fontWeight: 700, color: "#1A6B2C" }}>
                  {price.crop} — ₹{price.price}/qtl {trendEmoji[price.trend] || ""}
                </p>
              ) : (
                <p style={{ fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", color: "rgba(0,0,0,0.35)" }}>
                  {lang === "Telugu" ? "మండి ధరలు చూడండి →" : lang === "Hindi" ? "मंडी भाव देखें →" : "Tap for live prices →"}
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="liquidGlass-wrapper" style={{ cursor: "pointer" }} onClick={() => router.push("/calendar")}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "clamp(0.75rem, 2.5vw, 1rem)", display: "flex", alignItems: "center", gap: "0.75rem", minHeight: "56px" }}>
            <span style={{ fontSize: "1.5rem" }}>📅</span>
            <div>
              <p style={{ fontSize: "clamp(0.6875rem, 2.2vw, 0.75rem)", fontWeight: 500, color: "rgba(0,0,0,0.5)" }}>
                {lang === "Telugu" ? "ఈ రోజు దశ" : lang === "Hindi" ? "आज की अवस्था" : "Today's Stage"}
              </p>
              {stage ? (
                <>
                  <p style={{ fontSize: "clamp(0.8125rem, 2.8vw, 0.9375rem)", fontWeight: 600, color: "#1A6B2C" }}>{stage.crop}: {stage.stage}</p>
                  <p style={{ fontSize: "clamp(0.6875rem, 2.2vw, 0.75rem)", color: "rgba(0,0,0,0.45)", marginTop: "0.125rem" }}>{stage.tip}</p>
                </>
              ) : (
                <p style={{ fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", color: "rgba(0,0,0,0.35)" }}>
                  {lang === "Telugu" ? "పంట క్యాలెండర్ చూడండి →" : lang === "Hindi" ? "फसल कैलेंडर देखें →" : "Tap for crop calendar →"}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ==================== SEASON CROPS + TASKS ==================== */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 mb-5 sm:mb-6">
        <div className="liquidGlass-wrapper" style={{ cursor: "default" }}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "clamp(1rem, 3vw, 1.25rem)" }}>
            <h3 style={{ fontSize: "clamp(0.875rem, 3vw, 0.9375rem)", fontWeight: 600, color: info.color, marginBottom: "0.75rem" }}>
              🌾 {lang === "Telugu" ? `${seasonLabel[season][lang]} పంటలు` : lang === "Hindi" ? `${seasonLabel[season][lang]} फसलें` : `${seasonLabel[season][lang]} Season Crops`}
            </h3>
            <div className="flex flex-wrap gap-1.5 sm:gap-2">
              {info.crops.map((crop) => (
                <span key={crop} style={{ background: "rgba(34,197,94,0.1)", color: "#166534", padding: "clamp(0.25rem, 1vw, 0.375rem) clamp(0.5rem, 2vw, 0.75rem)", borderRadius: "9999px", fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", fontWeight: 500, lineHeight: 1.4 }}>{crop}</span>
              ))}
            </div>
          </div>
        </div>

        <div className="liquidGlass-wrapper" style={{ cursor: "default" }}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "clamp(1rem, 3vw, 1.25rem)" }}>
            <h3 style={{ fontSize: "clamp(0.875rem, 3vw, 0.9375rem)", fontWeight: 600, color: "rgba(0,0,0,0.7)", marginBottom: "0.75rem" }}>
              ✅ {lang === "Telugu" ? "ఈ సీజన్ పనులు" : lang === "Hindi" ? "इस मौसम के कार्य" : "Seasonal Tasks"}
            </h3>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {info.tasks.map((task, i) => (
                <li key={i} style={{ padding: "0.4375rem 0", fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", color: "rgba(0,0,0,0.65)", display: "flex", alignItems: "center", gap: "0.5rem", lineHeight: 1.4, minHeight: "44px" }}>
                  <span style={{ color: "#22c55e", flexShrink: 0 }}>○</span> <span>{task}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* ==================== WEATHER + ASK AI ==================== */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 mb-5 sm:mb-6">
        <div className="liquidGlass-wrapper" style={{ cursor: "default" }}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "clamp(1rem, 3vw, 1.25rem)" }}>
            <h3 style={{ fontSize: "clamp(0.875rem, 3vw, 0.9375rem)", fontWeight: 600, color: "rgba(0,0,0,0.7)", marginBottom: "0.75rem" }}>
              🌤️ {lang === "Telugu" ? "వాతావరణ సలహా" : lang === "Hindi" ? "मौसम सलाह" : "Weather Advisory"}
            </h3>
            {weather ? (
              <div style={{ padding: "clamp(0.625rem, 2vw, 0.75rem)", background: "rgba(34,197,94,0.08)", borderRadius: "0.75rem", fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", color: "#166534", lineHeight: 1.5 }}>
                {weather.temp > 35
                  ? (lang === "Telugu" ? "⚠️ అధిక ఉష్ణోగ్రత — ఉదయం/సాయంత్రం నీరు పెట్టండి, మల్చింగ్ వాడండి" : lang === "Hindi" ? "⚠️ अधिक तापमान — सुबह/शाम सिंचाई करें, मल्चिंग करें" : "⚠️ High temp — irrigate morning/evening, use mulching")
                  : weather.temp < 10
                  ? (lang === "Telugu" ? "❄️ చల్లని వాతావరణం — పంటలను కప్పండి, మంచు నుండి రక్షించండి" : lang === "Hindi" ? "❄️ ठंड — फसलों को ढकें, पाले से बचाएं" : "❄️ Cold — cover crops, protect from frost")
                  : (lang === "Telugu" ? "✅ వ్యవసాయానికి అనుకూల వాతావరణం. పంట పనులు కొనసాగించండి." : lang === "Hindi" ? "✅ खेती के लिए अनुकूल मौसम। फसल कार्य जारी रखें।" : "✅ Favorable weather. Continue farm operations normally.")}
              </div>
            ) : (
              <p style={{ fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", color: "rgba(0,0,0,0.4)" }}>📍 Allow location for live weather advisory</p>
            )}
          </div>
        </div>

        <div className="liquidGlass-wrapper" style={{ cursor: "pointer" }} onClick={() => router.push("/chatbot")}>
          <div className="liquidGlass-effect" />
          <div className="liquidGlass-tint" />
          <div className="liquidGlass-shine" />
          <div className="liquidGlass-text" style={{ padding: "clamp(1rem, 3vw, 1.25rem)" }}>
            <h3 style={{ fontSize: "clamp(0.875rem, 3vw, 0.9375rem)", fontWeight: 600, color: "rgba(0,0,0,0.7)", marginBottom: "0.75rem" }}>
              🤖 {lang === "Telugu" ? "AI ని అడగండి" : lang === "Hindi" ? "AI से पूछें" : "Ask AI Anything"}
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {(lang === "Telugu"
                ? ["నా పంటకు ఏ ఎరువు వాడాలి?", "ధర ఎప్పుడు పెరుగుతుంది?", "వ్యాధి నివారణ ఎలా?"]
                : lang === "Hindi"
                ? ["मेरी फसल को कौन सा खाद दें?", "भाव कब बढ़ेगा?", "बीमारी कैसे रोकें?"]
                : ["What fertilizer for my crop?", "When will prices rise?", "How to prevent disease?"]
              ).map((q) => (
                <div key={q} style={{ padding: "clamp(0.4375rem, 1.5vw, 0.5rem) clamp(0.625rem, 2vw, 0.75rem)", background: "rgba(34,197,94,0.08)", borderRadius: "0.5rem", fontSize: "clamp(0.75rem, 2.6vw, 0.8125rem)", color: "#166534", minHeight: "44px", display: "flex", alignItems: "center" }}>
                  💬 {q}
                </div>
              ))}
            </div>
            <p style={{ marginTop: "0.75rem", fontSize: "clamp(0.6875rem, 2.4vw, 0.75rem)", color: "rgba(0,0,0,0.4)" }}>
              {lang === "Telugu" ? "క్లిక్ చేసి చాట్ చేయండి →" : lang === "Hindi" ? "क्लिक करके चैट करें →" : "Click to chat →"}
            </p>
          </div>
        </div>
      </div>

      {/* ==================== DAILY TIP ==================== */}
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
