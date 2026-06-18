"use client";

import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";

const CROP_LOCATIONS: Record<string, { lat: number; lon: number; name: string }> = {
  maharashtra: { lat: 19.07, lon: 72.87, name: "Maharashtra (Mumbai)" },
  andhra: { lat: 15.82, lon: 78.03, name: "Andhra Pradesh (Kurnool)" },
  karnataka: { lat: 12.97, lon: 77.59, name: "Karnataka (Bangalore)" },
  telangana: { lat: 17.38, lon: 78.48, name: "Telangana (Hyderabad)" },
  tamil: { lat: 11.01, lon: 76.97, name: "Tamil Nadu (Coimbatore)" },
  punjab: { lat: 30.73, lon: 76.78, name: "Punjab (Chandigarh)" },
  up: { lat: 26.84, lon: 80.94, name: "Uttar Pradesh (Lucknow)" },
  gujarat: { lat: 23.02, lon: 72.57, name: "Gujarat (Ahmedabad)" },
  mp: { lat: 23.25, lon: 77.41, name: "Madhya Pradesh (Bhopal)" },
};

interface HourlyData { time: string; temp_c: number; rain_mm: number; wind_kmh: number; }
interface Advisory { can_spray: boolean; reason: string; next_rain?: string; next_safe_window?: string; }

export default function WeatherPage() {
  const { T } = useLang();
  const [locKey, setLocKey] = useState("maharashtra");
  const [loading, setLoading] = useState(false);
  const [forecast, setForecast] = useState<HourlyData[]>([]);
  const [advisory, setAdvisory] = useState<Advisory | null>(null);
  const [error, setError] = useState("");

  const loc = CROP_LOCATIONS[locKey];

  async function fetchWeather() {
    setLoading(true);
    setError("");
    try {
      const [advData, fcData] = await Promise.all([
        apiClient.get<Advisory>(`/weather/spray-advisory?lat=${loc.lat}&lon=${loc.lon}`),
        apiClient.get<{hours: HourlyData[]}>(`/weather/forecast?lat=${loc.lat}&lon=${loc.lon}`),
      ]);
      setAdvisory(advData);
      setForecast(fcData.hours || []);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Weather data unavailable");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchWeather(); }, [locKey]);

  const next24 = forecast.slice(0, 24);

  return (
    <div className="p-4 sm:p-6 w-full" style={{ maxWidth: "100vw" }}>
      <h2 className="text-xl sm:text-2xl font-bold" style={{ color: "var(--color-brand-deep)" }}>☁️ Weather & Spray Advisor</h2>
      <p className="text-sm mt-1 mb-4" style={{ color: "var(--color-text-secondary)" }}>Know exactly when to spray pesticides — avoid wasting chemicals</p>

      <div className="flex gap-2 mb-6 overflow-x-auto pb-1" style={{ scrollbarWidth: "none" }}>
        {Object.entries(CROP_LOCATIONS).map(([key, val]) => (
          <button key={key} onClick={() => setLocKey(key)}
            className="px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors"
            style={{
              background: key === locKey ? "var(--color-brand-primary)" : "var(--color-surface-hover)",
              color: key === locKey ? "white" : "var(--color-text-secondary)",
            }}
          >{val.name.split("(")[0].trim()}</button>
        ))}
      </div>

      {/* Spray Advisory Hero */}
      {advisory && (
        <div className="rounded-2xl p-6 mb-6 text-center" style={{
          background: advisory.can_spray ? "linear-gradient(135deg, #1B5E20, #2E7D32)" : "linear-gradient(135deg, #C62828, #E53935)",
          color: "white",
        }}>
          <div className="text-5xl mb-3">{advisory.can_spray ? "✅" : "❌"}</div>
          <h3 className="text-xl font-bold mb-1">{advisory.can_spray ? "Safe to Spray Today" : "Do Not Spray Now"}</h3>
          <p className="text-sm opacity-90">{advisory.reason}</p>
          {advisory.next_rain && <p className="text-xs mt-2 opacity-75">Next rain: {advisory.next_rain}</p>}
          {advisory.next_safe_window && !advisory.can_spray && (
            <p className="text-xs mt-1 opacity-75">Next safe window: {advisory.next_safe_window}</p>
          )}
        </div>
      )}

      {loading && <div className="skeleton h-48 rounded-2xl mb-6" />}

      {error && <div className="mb-4 p-4 rounded-xl text-sm" style={{ background: "#FFEBEE", color: "#C62828" }}>{error}</div>}

      {/* 24-hour breakdown */}
      {next24.length > 0 && (
        <div className="card liquid-glass-card rounded-xl p-4 overflow-x-auto">
          <h3 className="text-sm font-semibold mb-3" style={{ color: "var(--color-brand-deep)" }}>📊 24-Hour Forecast for {loc.name}</h3>
          <table className="w-full text-xs min-w-[500px]">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--color-border-light)" }}>
                <th className="text-left py-2 font-medium">Time</th>
                <th className="text-right py-2 font-medium">Temp</th>
                <th className="text-right py-2 font-medium">Rain</th>
                <th className="text-right py-2 font-medium">Wind</th>
                <th className="text-center py-2 font-medium">Spray?</th>
              </tr>
            </thead>
            <tbody>
              {next24.map((h, i) => {
                const safe = h.rain_mm < 0.5 && h.wind_kmh <= 15 && h.temp_c <= 35;
                return (
                  <tr key={i} className="border-b" style={{ borderColor: "var(--color-border-light)" }}>
                    <td className="py-2">{h.time?.slice(11, 16) || `+${i}h`}</td>
                    <td className="py-2 text-right">{h.temp_c.toFixed(1)}°C</td>
                    <td className="py-2 text-right">{h.rain_mm > 0 ? `${h.rain_mm.toFixed(1)}mm` : "—"}</td>
                    <td className="py-2 text-right">{h.wind_kmh.toFixed(0)} km/h</td>
                    <td className="py-2 text-center">{safe ? "✅" : "❌"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Rules reference */}
      <div className="mt-4 card liquid-glass-card rounded-xl p-4">
        <h3 className="text-sm font-semibold mb-2" style={{ color: "var(--color-brand-deep)" }}>ℹ️ Spray Rules</h3>
        <ul className="text-xs space-y-1" style={{ color: "var(--color-text-secondary)" }}>
          <li>❌ Rain expected within 6 hours — spray washes off</li>
          <li>❌ Wind above 15 km/h — chemicals drift away from target</li>
          <li>❌ Temperature above 35°C — chemicals evaporate too fast</li>
          <li>✅ All clear — safe to spray, check table above for best hour</li>
        </ul>
      </div>
    </div>
  );
}
