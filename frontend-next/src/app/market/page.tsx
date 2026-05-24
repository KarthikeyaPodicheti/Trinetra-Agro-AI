"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";
import type { MarketResponse } from "@/lib/types";
import { FormSkeleton } from "@/components/skeleton";

const CROPS = ["rice", "wheat", "cotton", "tomato", "potato", "onion", "maize", "sugarcane", "soybean", "groundnut"];

export default function MarketPage() {
  const { T } = useLang();
  const [crop, setCrop] = useState("Rice");
  const [days, setDays] = useState(14);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<MarketResponse | null>(null);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const r = await apiClient.post<MarketResponse>("/ai/market", {
        crop: crop.toLowerCase(),
        days,
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

  const recColors: Record<string, string> = {
    Buy: "text-green-600 bg-green-50 border-green-200",
    Sell: "text-red-600 bg-red-50 border-red-200",
    Hold: "text-orange-600 bg-orange-50 border-orange-200",
    Monitor: "text-blue-600 bg-blue-50 border-blue-200",
  };

  if (loading && !result) {
    return (
      <div className="p-6 max-w-4xl">
        <h2 className="text-2xl font-bold text-gray-800">📈 {T("marketTitle")}</h2>
        <p className="text-gray-500 mt-1">{T("marketSubtitle")}</p>
        <div className="mt-6"><FormSkeleton /></div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl">
      <h2 className="text-2xl font-bold text-gray-800">📈 {T("marketTitle")}</h2>
      <p className="text-gray-500 mt-1">{T("marketSubtitle")}</p>

      <form onSubmit={handleSubmit} className="mt-6 bg-white rounded-xl border border-green-100 p-6 shadow-sm space-y-5 liquid-glass-card">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">{T("selectCrop")}</label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              {CROPS.map((c) => <option key={c} value={c.charAt(0).toUpperCase() + c.slice(1)}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">{T("forecastDays")}</label>
            <input
              type="range"
              min={7}
              max={30}
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="w-full accent-green-600"
            />
            <p className="text-xs text-gray-400 mt-1">{days} days</p>
          </div>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
        >
          {loading ? "..." : `📊  ${T("getPrediction")}`}
        </button>
      </form>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">{error}</div>
      )}

      {loading && (
        <div className="mt-6 space-y-4">
          <div className="animate-pulse bg-white rounded-xl border border-gray-100 p-4 shadow-sm h-12" />
          <div className="grid grid-cols-3 gap-4">
            <div className="animate-pulse bg-white rounded-xl border border-gray-100 p-4 shadow-sm h-20" />
            <div className="animate-pulse bg-white rounded-xl border border-gray-100 p-4 shadow-sm h-20" />
            <div className="animate-pulse bg-white rounded-xl border border-gray-100 p-4 shadow-sm h-20" />
          </div>
          <div className="animate-pulse bg-white rounded-xl border border-gray-100 p-4 shadow-sm h-72" />
        </div>
      )}

      {result && (
        <div className="mt-6 space-y-4">
          {/* Recommendation */}
          <div className={`rounded-xl border p-4 text-sm font-medium ${recColors[result.recommendation.action] || recColors.Monitor}`}>
            <strong>{result.recommendation.action}</strong> — {result.recommendation.message}
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-white rounded-xl border border-green-100 p-4 shadow-sm text-center liquid-glass-card">
              <p className="text-xs text-gray-500">Current Price</p>
              <p className="text-lg font-bold text-gray-800 mt-1">₹{result.current_price.toLocaleString()}/q</p>
            </div>
            <div className="bg-white rounded-xl border border-green-100 p-4 shadow-sm text-center liquid-glass-card">
              <p className="text-xs text-gray-500">Avg Expected ({days}d)</p>
              {(() => {
                const preds = result.predictions.prices;
                const avg = preds.reduce((a, b) => a + b, 0) / preds.length;
                const delta = avg - result.current_price;
                return (
                  <>
                    <p className="text-lg font-bold text-gray-800 mt-1">₹{avg.toFixed(0)}</p>
                    <p className={`text-xs ${delta >= 0 ? "text-green-500" : "text-red-500"}`}>
                      {delta >= 0 ? "+" : ""}{delta.toFixed(0)}
                    </p>
                  </>
                );
              })()}
            </div>
            <div className="bg-white rounded-xl border border-green-100 p-4 shadow-sm text-center liquid-glass-card">
              <p className="text-xs text-gray-500">Overall Trend</p>
              <p className="text-lg font-bold text-gray-800 mt-1 capitalize">{result.trend}</p>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-white rounded-xl border border-green-100 p-4 shadow-sm liquid-glass-card">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">📉 Price Forecast — {crop}</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={result.predictions.dates.map((d, i) => ({
                  date: d,
                  Price: result.predictions.prices[i],
                  "7-day MA": result.predictions.moving_avg[i],
                }))}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#E8F5E9" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="Price" stroke="#2E7D32" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="7-day MA" stroke="#81C784" strokeWidth={2} strokeDasharray="5 5" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Market Tips */}
          {result.market_tips && result.market_tips.length > 0 && (
            <div className="bg-white rounded-xl border border-green-100 p-4 shadow-sm liquid-glass-card">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">💡 Market Tips</h3>
              <ul className="space-y-1 text-sm text-gray-600 list-disc list-inside">
                {result.market_tips.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
