"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";
import type { AdvisorResponse, CropRecommendation } from "@/lib/types";
import { FormSkeleton, ResultsSkeleton } from "@/components/skeleton";

const SOIL_TYPES = ["loamy", "black cotton", "alluvial", "sandy", "clay", "red soil"];
const SEASONS = ["kharif", "rabi", "zaid"];

export default function AdvisorPage() {
  const [soilType, setSoilType] = useState(SOIL_TYPES[0]);
  const [acres, setAcres] = useState(5);
  const [season, setSeason] = useState(SEASONS[0]);
  const [budget, setBudget] = useState(50000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AdvisorResponse | null>(null);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const r = await apiClient.post<AdvisorResponse>("/ai/advisor", {
        soil_type: soilType,
        land_acres: acres,
        budget,
        season,
      });
      if (r.success) {
        setResult(r);
      } else {
        setError(r.error || "Analysis failed");
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  if (loading && !result) {
    return (
      <div className="p-6 max-w-4xl">
        <h2 className="text-2xl font-bold text-gray-800">🌱 AI Farming Advisor</h2>
        <p className="text-gray-500 mt-1">Get personalized crop recommendations based on your specific farm conditions.</p>
        <div className="mt-6"><FormSkeleton /></div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl">
      <h2 className="text-2xl font-bold text-gray-800">🌱 AI Farming Advisor</h2>
      <p className="text-gray-500 mt-1">Get personalized crop recommendations based on your specific farm conditions.</p>

      <form onSubmit={handleSubmit} className="mt-6 bg-white rounded-xl border border-green-100 p-6 shadow-sm space-y-5">
        <h3 className="font-semibold text-gray-700">Farm Parameters</h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Soil Type</label>
            <select
              value={soilType}
              onChange={(e) => setSoilType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              {SOIL_TYPES.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Land Size (acres)</label>
            <input
              type="number"
              min={0.5}
              max={500}
              step={0.5}
              value={acres}
              onChange={(e) => setAcres(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Season</label>
            <select
              value={season}
              onChange={(e) => setSeason(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              {SEASONS.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">Budget (₹)</label>
          <input
            type="number"
            min={5000}
            max={10000000}
            step={5000}
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
        >
          {loading ? "AI analyzing your farm data..." : "🌱  Get Crop Recommendations"}
        </button>
      </form>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">{error}</div>
      )}

      {loading && <ResultsSkeleton />}

      {result && (
        <div className="mt-6 space-y-4">
          <div className="bg-green-50 border border-green-200 rounded-xl p-4 text-green-800 text-sm font-medium">
            ✅ Top recommendations for {season.charAt(0).toUpperCase() + season.slice(1)} season
          </div>

          {result.primary_recommendations.map((crop: CropRecommendation, i: number) => (
            <div key={crop.name} className="bg-white rounded-xl border border-green-100 p-5 shadow-sm">
              <details open={i === 0}>
                <summary className="font-semibold text-gray-800 cursor-pointer">
                  {i + 1}. {crop.name} — Match Score: {(crop.score * 100).toFixed(0)}%
                </summary>
                <div className="mt-3 space-y-1 text-sm text-gray-600 ml-4">
                  <p><strong>Season:</strong> {crop.season}</p>
                  <p><strong>Duration:</strong> {crop.duration}</p>
                  <p><strong>Water Req:</strong> {crop.water_requirement}</p>
                  <p><strong>Profit Range:</strong> ₹{crop.profit_range}</p>
                  {crop.diseases && crop.diseases.length > 0 && (
                    <p><strong>Watch for:</strong> {crop.diseases.join(", ")}</p>
                  )}
                </div>
              </details>
            </div>
          ))}

          <div className="bg-white rounded-xl border border-green-100 p-5 shadow-sm">
            <h3 className="font-semibold text-gray-700 mb-3">💰 Expected ROI</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gray-50 rounded-lg p-3 text-center">
                <p className="text-xs text-gray-500">Conservative</p>
                <p className="text-lg font-bold text-gray-800">₹{result.expected_returns.conservative.toLocaleString()}</p>
              </div>
              <div className="bg-green-50 rounded-lg p-3 text-center border border-green-100">
                <p className="text-xs text-gray-500">Moderate</p>
                <p className="text-lg font-bold text-green-700">₹{result.expected_returns.moderate.toLocaleString()}</p>
                <p className="text-xs text-green-500">Expected</p>
              </div>
              <div className="bg-gray-50 rounded-lg p-3 text-center">
                <p className="text-xs text-gray-500">Optimistic</p>
                <p className="text-lg font-bold text-gray-800">₹{result.expected_returns.optimistic.toLocaleString()}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
