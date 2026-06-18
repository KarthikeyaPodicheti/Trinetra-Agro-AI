"use client";

import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";

const CROPS = ["Tomato", "Onion", "Potato", "Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Soybean", "Groundnut", "Banana", "Turmeric", "Chilli", "Ginger", "Garlic"];
const STATES = ["Andhra Pradesh", "Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Uttar Pradesh", "Gujarat", "Madhya Pradesh", "Rajasthan", "Punjab"];

interface MandiPrice { mandi: string; crop: string; price_per_quintal: number; state: string; district: string; date: string; }

export default function MarketPage() {
  const { T } = useLang();
  const [crop, setCrop] = useState("Tomato");
  const [state, setState] = useState("Maharashtra");
  const [district, setDistrict] = useState("");
  const [loading, setLoading] = useState(false);
  const [prices, setPrices] = useState<MandiPrice[]>([]);
  const [trend, setTrend] = useState("");
  const [recommendation, setRecommendation] = useState<any>(null);
  const [error, setError] = useState("");
  const [totalRecords, setTotalRecords] = useState(0);
  const [cachedAt, setCachedAt] = useState("");

  async function fetchPrices() {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams({ crop, limit: "30" });
      if (state) params.set("state", state);
      if (district) params.set("district", district);
      const data = await apiClient.get<any>(`/mandi/prices?${params.toString()}`);
      if (data.success) {
        setPrices(data.prices || []);
        setTrend(data.trend || "stable");
        setRecommendation(data.recommendation);
        setTotalRecords(data.total_records || 0);
        setCachedAt(new Date().toLocaleTimeString());
      } else {
        setError(data.error || "No data available for this crop and location.");
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Mandi data unavailable right now. Try again.");
    } finally {
      setLoading(false);
    }
  }

  const recColors: Record<string, string> = {
    sell_now: "bg-red-50 border-red-200 text-red-700",
    hold: "bg-green-50 border-green-200 text-green-700",
    monitor: "bg-blue-50 border-blue-200 text-blue-700",
    no_data: "bg-gray-50 border-gray-200 text-gray-600",
  };

  const recLabels: Record<string, string> = { sell_now: "📉 Sell Now", hold: "📈 Hold / Wait", monitor: "📊 Monitor", no_data: "ℹ️ No Data" };

  const chartData = prices.slice(0, 14).reverse().map((p, i) => ({
    date: p.date?.slice(5) || `Day ${i + 1}`,
    price: p.price_per_quintal,
    mandi: p.mandi,
  }));

  return (
    <div className="p-4 sm:p-6 w-full" style={{ maxWidth: "100vw" }}>
      <h2 className="text-xl sm:text-2xl font-bold" style={{ color: "var(--color-brand-deep)" }}>📈 Mandi Prices</h2>
      <p className="text-sm mt-1" style={{ color: "var(--color-text-secondary)" }}>Real-time crop prices from Government of India mandis</p>

      <form onSubmit={(e) => { e.preventDefault(); fetchPrices(); }} className="mt-6 card liquid-glass-card rounded-xl p-4 sm:p-5 space-y-4" style={{ maxWidth: 600 }}>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="label">{T("selectCrop")}</label>
            <select value={crop} onChange={e => setCrop(e.target.value)} className="input-field liquid-glass-input" aria-label="Crop">
              {CROPS.map(c => <option key={c}>{c}</option>)}
            </select>
          </div>
          <div>
            <label className="label">{T("state") || "State"}</label>
            <select value={state} onChange={e => setState(e.target.value)} className="input-field liquid-glass-input" aria-label="State">
              <option value="">All States</option>
              {STATES.map(s => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="label">{T("district") || "District"} <span className="text-xs font-normal" style={{ color: "var(--color-text-tertiary)" }}>(optional)</span></label>
            <input type="text" value={district} onChange={e => setDistrict(e.target.value)} placeholder="e.g. Kurnool" className="input-field liquid-glass-input" />
          </div>
        </div>
        <button type="submit" disabled={loading} className="btn-primary w-full">
          {loading ? "Fetching real-time mandi data..." : "🔍 Get Live Prices"}
        </button>
        {cachedAt && !loading && <p className="text-xs text-center" style={{ color: "var(--color-text-tertiary)" }}>Last updated: {cachedAt} (cached for 30 min)</p>}
      </form>

      {error && <div className="mt-4 p-4 rounded-xl text-sm" style={{ background: "#FFEBEE", color: "#C62828" }}>{error}</div>}

      {loading && (
        <div className="mt-6 space-y-4">
          <div className="skeleton h-12 rounded-xl" />
          <div className="grid grid-cols-3 gap-4">
            <div className="skeleton h-20 rounded-xl" />
            <div className="skeleton h-20 rounded-xl" />
            <div className="skeleton h-20 rounded-xl" />
          </div>
          <div className="skeleton h-64 rounded-xl" />
        </div>
      )}

      {prices.length > 0 && (
        <div className="mt-6 space-y-4" style={{ maxWidth: "100vw" }}>
          {/* Recommendation */}
          {recommendation && (
            <div className={`rounded-xl border p-4 text-sm font-medium ${recColors[recommendation.action] || recColors.monitor}`}>
              {recLabels[recommendation.action] || recommendation.action} — {recommendation.message}
            </div>
          )}

          {/* KPI Cards */}
          <div className="grid grid-cols-3 gap-3">
            <div className="card liquid-glass-card rounded-xl p-3 text-center">
              <p className="text-xs" style={{ color: "var(--color-text-tertiary)" }}>Current Price</p>
              <p className="text-lg font-bold mt-1" style={{ color: "var(--color-brand-deep)" }}>
                ₹{prices[0]?.price_per_quintal?.toLocaleString()}/q
              </p>
            </div>
            <div className="card liquid-glass-card rounded-xl p-3 text-center">
              <p className="text-xs" style={{ color: "var(--color-text-tertiary)" }}>7-Day Avg</p>
              <p className="text-lg font-bold mt-1" style={{ color: "var(--color-brand-deep)" }}>
                ₹{Math.round(prices.slice(0, 7).reduce((a, p) => a + p.price_per_quintal, 0) / Math.min(prices.length, 7)).toLocaleString()}/q
              </p>
            </div>
            <div className="card liquid-glass-card rounded-xl p-3 text-center">
              <p className="text-xs" style={{ color: "var(--color-text-tertiary)" }}>Trend</p>
              <p className="text-lg font-bold mt-1 capitalize" style={{ color: trend === "rising" ? "#2E7D32" : trend === "falling" ? "#C62828" : "#1565C0" }}>
                {trend === "rising" ? "↑" : trend === "falling" ? "↓" : "→"} {trend}
              </p>
            </div>
          </div>

          {/* Chart */}
          <div className="card liquid-glass-card rounded-xl p-4">
            <h3 className="text-sm font-semibold mb-3" style={{ color: "var(--color-brand-deep)" }}>📉 Price Trend — {crop} in {state || "All India"}</h3>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8F5E9" />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip content={({ active, payload }) => {
                  if (active && payload?.[0]) {
                    return <div className="bg-white p-2 rounded-lg shadow text-sm border"><p>₹{payload[0].payload.price}/quintal</p><p className="text-xs text-gray-500">{payload[0].payload.mandi}</p></div>;
                  }
                  return null;
                }} />
                <Legend />
                <Line type="monotone" dataKey="price" name="₹/Quintal" stroke="#2E7D32" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Price Table */}
          <div className="card liquid-glass-card rounded-xl p-4 overflow-x-auto">
            <h3 className="text-sm font-semibold mb-3" style={{ color: "var(--color-brand-deep)" }}>📋 Recent Mandi Prices ({prices.length} records of {totalRecords})</h3>
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b" style={{ borderColor: "var(--color-border-light)" }}>
                  <th className="text-left py-2 font-medium" style={{ color: "var(--color-text-secondary)" }}>Mandi</th>
                  <th className="text-right py-2 font-medium" style={{ color: "var(--color-text-secondary)" }}>₹/Quintal</th>
                  <th className="text-right py-2 font-medium" style={{ color: "var(--color-text-secondary)" }}>Date</th>
                </tr>
              </thead>
              <tbody>
                {prices.slice(0, 10).map((p, i) => (
                  <tr key={i} className="border-b" style={{ borderColor: "var(--color-border-light)" }}>
                    <td className="py-2">{p.mandi}</td>
                    <td className="py-2 text-right font-semibold">₹{p.price_per_quintal.toLocaleString()}</td>
                    <td className="py-2 text-right" style={{ color: "var(--color-text-tertiary)" }}>{p.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {!loading && prices.length === 0 && !error && (
        <div className="mt-6 p-8 text-center card liquid-glass-card rounded-xl">
          <p className="text-3xl mb-2">📈</p>
          <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>Select a crop and state above, then click <strong>Get Live Prices</strong> to fetch real mandi data from the Government of India.</p>
          <p className="text-xs mt-2" style={{ color: "var(--color-text-tertiary)" }}>First query may take 15-20 seconds. Repeat queries are cached for 30 minutes.</p>
        </div>
      )}
    </div>
  );
}
