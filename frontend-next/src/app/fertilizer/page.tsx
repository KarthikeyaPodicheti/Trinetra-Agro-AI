"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";

const CROPS = ["Cotton", "Rice", "Wheat", "Maize", "Soybean", "Groundnut", "Sugarcane"];

const SOIL_TYPES = ["Alluvial", "Black Cotton", "Loamy", "Sandy Loam", "Clay", "Red Soil"];

const TARGET_YIELDS = ["Moderate", "Good", "Maximum"];

interface FertilizerResult {
  crop: string;
  soil: string;
  N: number; P: number; K: number;
  urea: number;
  dap: number;
  mop: number;
  cost: number;
  schedule: { stage: string; urea: number; dap: number; mop: number; note: string }[];
  tip: string;
  subsidy: string;
}

export default function FertilizerPage() {
  const { T, lang } = useLang();
  const [crop, setCrop] = useState("Cotton");
  const [soil, setSoil] = useState("Black Cotton");
  const [yieldLevel, setYieldLevel] = useState("Moderate");
  const [result, setResult] = useState<FertilizerResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function calculate() {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const q = `?crop=${encodeURIComponent(crop)}&soil=${encodeURIComponent(soil)}&target_yield=${encodeURIComponent(yieldLevel)}`;
      const res: any = await apiClient.get(`/fertilizer/calculate${q}`);
      if (res && res.N !== undefined) {
        setResult(res as FertilizerResult);
      } else {
        setError("No data returned. Try different inputs.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to calculate. Check your connection.");
    }
    setLoading(false);
  }

  return (
    <div className="p-4 sm:p-6 w-full" style={{ maxWidth: "100vw" }}>
      <h2 className="text-xl sm:text-2xl font-bold text-[var(--color-brand-deep)] mb-1">🧪 Fertilizer Calculator</h2>
      <p className="text-sm text-[var(--color-text-tertiary)] mb-4">
        {lang === "Telugu" ? "ICAR సిఫార్సుల ఆధారంగా మీ పంటకు ఖచ్చితమైన NPK ఎరువు మోతాదును పొందండి." : lang === "Hindi" ? "ICAR की सिफारिशों के आधार पर अपनी फसल के लिए सटीक NPK उर्वरक खुराक प्राप्त करें।" : "Get exact NPK fertilizer dosage for your crop based on ICAR recommendations."}
      </p>

      {/* Form */}
      <div className="liquidGlass-wrapper liquidGlass-card rounded-xl mb-5" style={{ cursor: "default" }}>
        <div className="liquidGlass-effect" />
        <div className="liquidGlass-tint" />
        <div className="liquidGlass-shine" />
        <div className="liquidGlass-text p-4 sm:p-5 grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1">{lang === "Telugu" ? "పంట" : lang === "Hindi" ? "फसल" : "Crop"}</label>
            <select value={crop} onChange={(e) => setCrop(e.target.value)} className="liquid-glass-input w-full" aria-label="Crop">
              {CROPS.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">{lang === "Telugu" ? "నేల రకం" : lang === "Hindi" ? "मिट्टी का प्रकार" : "Soil Type"}</label>
            <select value={soil} onChange={(e) => setSoil(e.target.value)} className="liquid-glass-input w-full" aria-label="Soil Type">
              {SOIL_TYPES.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">{lang === "Telugu" ? "లక్ష్య దిగుబడి" : lang === "Hindi" ? "लक्ष्य उपज" : "Target Yield"}</label>
            <select value={yieldLevel} onChange={(e) => setYieldLevel(e.target.value)} className="liquid-glass-input w-full" aria-label="Target Yield">
              {TARGET_YIELDS.map((y) => <option key={y} value={y}>{y}</option>)}
            </select>
          </div>
          <div className="flex items-end">
            <button onClick={calculate} disabled={loading} className="liquid-glass-btn w-full" style={{ minHeight: 44 }}>
              {loading ? (lang === "Telugu" ? "లెక్కిస్తోంది..." : lang === "Hindi" ? "गणना हो रही है..." : "Calculating...") : (lang === "Telugu" ? "లెక్కించండి" : lang === "Hindi" ? "गणना करें" : "Calculate")}
            </button>
          </div>
        </div>
      </div>

      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

      {/* Results */}
      {result && (
        <>
          {/* NPK Summary */}
          <div className="liquidGlass-wrapper liquidGlass-card rounded-xl mb-4" style={{ cursor: "default" }}>
            <div className="liquidGlass-effect" />
            <div className="liquidGlass-tint" />
            <div className="liquidGlass-shine" />
            <div className="liquidGlass-text p-4 sm:p-5">
              <h3 className="font-semibold mb-3 text-lg text-[var(--color-brand-deep)]">
                {lang === "Telugu" ? "📊 NPK సారాంశం" : lang === "Hindi" ? "📊 NPK सारांश" : "📊 NPK Summary"}
              </h3>
              <div className="grid grid-cols-3 gap-3 text-center mb-4">
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-xs opacity-60">{lang === "Telugu" ? "నత్రజని (N)" : lang === "Hindi" ? "नाइट्रोजन (N)" : "Nitrogen (N)"}</p>
                  <p className="text-2xl font-bold text-blue-700">{result.N}</p>
                  <p className="text-xs opacity-50">kg/acre</p>
                </div>
                <div className="bg-amber-50 rounded-lg p-3">
                  <p className="text-xs opacity-60">{lang === "Telugu" ? "ఫాస్ఫరస్ (P)" : lang === "Hindi" ? "फास्फोरस (P)" : "Phosphorus (P)"}</p>
                  <p className="text-2xl font-bold text-amber-700">{result.P}</p>
                  <p className="text-xs opacity-50">kg/acre</p>
                </div>
                <div className="bg-green-50 rounded-lg p-3">
                  <p className="text-xs opacity-60">{lang === "Telugu" ? "పొటాషియం (K)" : lang === "Hindi" ? "पोटाशियम (K)" : "Potassium (K)"}</p>
                  <p className="text-2xl font-bold text-green-700">{result.K}</p>
                  <p className="text-xs opacity-50">kg/acre</p>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-3">
                <div className="bg-gray-50 rounded-lg p-2 text-center">
                  <p className="text-xs opacity-60">Urea</p>
                  <p className="font-bold text-sm">{result.urea} kg</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-2 text-center">
                  <p className="text-xs opacity-60">DAP</p>
                  <p className="font-bold text-sm">{result.dap} kg</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-2 text-center">
                  <p className="text-xs opacity-60">MOP</p>
                  <p className="font-bold text-sm">{result.mop} kg</p>
                </div>
                <div className="bg-emerald-50 rounded-lg p-2 text-center">
                  <p className="text-xs opacity-60">{lang === "Telugu" ? "ఖర్చు" : lang === "Hindi" ? "लागत" : "Cost"}</p>
                  <p className="font-bold text-sm text-emerald-700">₹{result.cost}</p>
                </div>
              </div>

              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-sm text-amber-800">
                💰 {result.subsidy}
              </div>
            </div>
          </div>

          {/* Stage-wise Schedule */}
          <div className="liquidGlass-wrapper liquidGlass-card rounded-xl mb-4" style={{ cursor: "default" }}>
            <div className="liquidGlass-effect" />
            <div className="liquidGlass-tint" />
            <div className="liquidGlass-shine" />
            <div className="liquidGlass-text p-4 sm:p-5">
              <h3 className="font-semibold mb-3 text-lg text-[var(--color-brand-deep)]">
                {lang === "Telugu" ? "📅 దశల వారీ షెడ్యూల్" : lang === "Hindi" ? "📅 चरण-वार अनुसूची" : "📅 Stage-wise Schedule"}
              </h3>
              <div className="overflow-x-auto" style={{ maxWidth: "100%" }}>
                <table style={{ width: "100%", fontSize: "clamp(0.75rem, 2.6vw, 0.875rem)", borderCollapse: "collapse" }}>
                  <thead>
                    <tr style={{ borderBottom: "2px solid rgba(0,0,0,0.1)" }}>
                      <th style={{ padding: "0.5rem", textAlign: "left", fontWeight: 600 }}>
                        {lang === "Telugu" ? "దశ" : lang === "Hindi" ? "चरण" : "Stage"}
                      </th>
                      <th style={{ padding: "0.5rem", textAlign: "right", fontWeight: 600 }}>Urea (kg)</th>
                      <th style={{ padding: "0.5rem", textAlign: "right", fontWeight: 600 }}>DAP (kg)</th>
                      <th style={{ padding: "0.5rem", textAlign: "right", fontWeight: 600 }}>MOP (kg)</th>
                      <th style={{ padding: "0.5rem", textAlign: "left", fontWeight: 600 }}>
                        {lang === "Telugu" ? "గమనిక" : lang === "Hindi" ? "नोट" : "Note"}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.schedule.map((s, i) => (
                      <tr key={i} style={{ borderBottom: "1px solid rgba(0,0,0,0.06)" }}>
                        <td style={{ padding: "0.5rem", fontWeight: 500 }}>{s.stage}</td>
                        <td style={{ padding: "0.5rem", textAlign: "right" }}>{s.urea}</td>
                        <td style={{ padding: "0.5rem", textAlign: "right" }}>{s.dap}</td>
                        <td style={{ padding: "0.5rem", textAlign: "right" }}>{s.mop}</td>
                        <td style={{ padding: "0.5rem", color: "rgba(0,0,0,0.6)", fontSize: "0.8125rem" }}>{s.note}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Tip */}
          <div className="liquidGlass-wrapper liquidGlass-card rounded-xl" style={{ cursor: "default" }}>
            <div className="liquidGlass-effect" />
            <div className="liquidGlass-tint" />
            <div className="liquidGlass-shine" />
            <div className="liquidGlass-text p-4" style={{ fontSize: "0.875rem", color: "#1565C0" }}>
              💡 {result.tip}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
