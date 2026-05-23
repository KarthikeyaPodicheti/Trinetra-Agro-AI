"use client";

import { useRouter } from "next/navigation";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";

const marketData = [
  { day: "D-6", Wheat: 2100, Rice: 2800 },
  { day: "D-5", Wheat: 2120, Rice: 2790 },
  { day: "D-4", Wheat: 2150, Rice: 2820 },
  { day: "D-2", Wheat: 2140, Rice: 2850 },
  { day: "D-1", Wheat: 2180, Rice: 2880 },
  { day: "Today", Wheat: 2200, Rice: 2860 },
];

const resourceData = [
  { day: "D-6", Water: 60, Soil: 80 },
  { day: "D-5", Water: 65, Soil: 80 },
  { day: "D-4", Water: 70, Soil: 79 },
  { day: "D-3", Water: 68, Soil: 81 },
  { day: "D-2", Water: 55, Soil: 82 },
  { day: "D-1", Water: 60, Soil: 82 },
  { day: "Today", Water: 62, Soil: 83 },
];

const tips = [
  "Check soil moisture before irrigating — overwatering reduces yield.",
  "Rotate crops each season to maintain soil health and reduce pests.",
  "Use drip irrigation to save 30-50% water compared to flood method.",
  "Monitor market prices weekly for best selling window.",
  "Apply mulch to reduce water evaporation by 25-30%.",
];

export default function DashboardPage() {
  const router = useRouter();
  const randomTip = tips[Math.floor(Math.random() * tips.length)];

  return (
    <div className="p-6 max-w-6xl">
      <h2 className="text-2xl font-bold text-gray-800">📊 Farm Intelligence Dashboard</h2>
      <p className="text-gray-500 mt-1">Welcome to your centralized farm management command center.</p>

      {/* Quick Actions */}
      <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: "🌱  Crop Advice", path: "/advisor" },
          { label: "🔬  Scan Disease", path: "/disease-scanner" },
          { label: "📈  Market Prices", path: "/market" },
          { label: "💬  AI Chatbot", path: "/chatbot" },
        ].map((btn) => (
          <button
            key={btn.path}
            onClick={() => router.push(btn.path)}
            className="bg-white border border-green-100 rounded-xl p-3.5 text-sm font-semibold text-green-700 shadow-sm hover:shadow-md hover:bg-green-50 transition text-center cursor-pointer"
          >
            {btn.label}
          </button>
        ))}
      </div>

      {/* KPI Cards */}
      <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "System Status", value: "Online", sub: "All systems nominal", color: "text-green-600" },
          { label: "Active Crops", value: "4", sub: "Monitored", color: "text-gray-800" },
          { label: "AI Analyses", value: "127", sub: "Total run", color: "text-gray-800" },
          { label: "Market Alerts", value: "3", sub: "Active", color: "text-red-600" },
        ].map((kpi) => (
          <div key={kpi.label} className="bg-white rounded-xl border border-green-100 p-4 shadow-sm">
            <p className="text-sm text-gray-500">{kpi.label}</p>
            <p className={`text-lg font-bold mt-1 ${kpi.color}`}>{kpi.value}</p>
            <p className="text-xs text-gray-400 mt-1">{kpi.sub}</p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="mt-6 grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-green-100 p-4 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">🌾 Simulated Market Trends (Last 7 Days)</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={marketData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E8F5E9" />
              <XAxis dataKey="day" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Line type="monotone" dataKey="Wheat" stroke="#2E7D32" strokeWidth={2} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="Rice" stroke="#81C784" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl border border-green-100 p-4 shadow-sm">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">💧 Resource Usage (Estimated)</h3>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={resourceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E8F5E9" />
              <XAxis dataKey="day" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} domain={[0, 100]} />
              <Tooltip />
              <Area type="monotone" dataKey="Water" stroke="#2E7D32" fill="#C8E6C9" fillOpacity={0.6} />
              <Area type="monotone" dataKey="Soil" stroke="#81C784" fill="#E8F5E9" fillOpacity={0.8} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tip */}
      <div className="mt-6 bg-blue-50 border border-blue-100 rounded-xl p-4 text-sm text-blue-800">
        💡 <strong>Today&apos;s Farming Tip:</strong> {randomTip}
      </div>
    </div>
  );
}
