"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";

const CROPS = ["Cotton", "Rice", "Wheat", "Maize", "Soybean", "Groundnut", "Sugarcane"];

const STAGE_ICONS: Record<string, string> = {
  "Sowing": "🌱",
  "Germination": "🌿",
  "Germination & Crown Root": "🌿",
  "Seedling": "🌿",
  "Seedling Growth": "🌿",
  "Seedling / Knee-high": "🌿",
  "Seedling & Nodulation": "🌿",
  "Transplanting": "🌿",
  "Nursery / Transplanting": "🌿",
  "Tillering": "🌾",
  "Maximum Tillering": "🌾",
  "Vegetative Growth": "🌾",
  "Jointing": "🌾",
  "Pegging": "🥜",
  "Grand Growth": "🌾",
  "Square Formation": "🌸",
  "Booting & Heading": "🌸",
  "Flowering": "🌸",
  "Flowering & Grain Filling": "🌸",
  "Flowering / Grain Filling": "🌸",
  "Tasseling": "🌸",
  "Silking & Grain Fill": "🌸",
  "Boll Development": "🫘",
  "Pod Development": "🫘",
  "Panicle Initiation": "🌾",
  "Boll Opening": "🫘",
  "Dough Stage": "🌽",
  "Maturity / Ripening": "🌾",
  "Maturity & Harvest": "🌾",
  "Ripening & Harvest": "🌾",
  "Harvest": "🎉",
};

interface TimelineEntry {
  week_number: number;
  stage: string;
  date_range: { start: string; end: string };
  irrigation: string;
  fertilizer: string;
  pest_management: string;
  tip: string;
}

interface CalendarData {
  crop: string;
  sowing_date: string;
  expected_harvest: string;
  total_weeks: number;
  timeline: TimelineEntry[];
}

export default function CropCalendarPage() {
  const { T } = useLang();
  const [crop, setCrop] = useState("Cotton");
  const [sowingDate, setSowingDate] = useState("");
  const [data, setData] = useState<CalendarData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expandedWeek, setExpandedWeek] = useState<number | null>(null);

  async function generate() {
    setLoading(true);
    setError("");
    setData(null);
    try {
      const query = sowingDate ? `?crop=${encodeURIComponent(crop)}&sowing_date=${sowingDate}` : `?crop=${encodeURIComponent(crop)}`;
      const res: any = await apiClient.get(`/calendar/generate${query}`);
      if (res && res.timeline) {
        setData(res as CalendarData);
      } else if (res && res.error) {
        setError(res.error);
      } else {
        setError("No data returned from server. Try a different crop.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to load calendar. Check your connection.");
    }
    setLoading(false);
  }

  const toggleWeek = (n: number) => setExpandedWeek(expandedWeek === n ? null : n);

  return (
    <div className="p-4 sm:p-6 max-w-5xl" style={{ maxWidth: "100vw" }}>
      <h2 className="text-xl sm:text-2xl font-bold text-[var(--color-brand-deep)] mb-1">
        📅 {T("cropCalendar")}
      </h2>
      <p className="text-sm text-[var(--color-text-tertiary)] mb-4">
        {T("cropCalendarDesc")}
      </p>

      {/* Form Card */}
      <div className="liquidGlass-wrapper liquidGlass-card rounded-xl mb-5" style={{ cursor: "default" }}>
        <div className="liquidGlass-effect" />
        <div className="liquidGlass-tint" />
        <div className="liquidGlass-shine" />
        <div className="liquidGlass-text p-4 sm:p-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1">{T("selectCrop")}</label>
            <select value={crop} onChange={(e) => setCrop(e.target.value)} className="liquid-glass-input w-full" aria-label={T("selectCrop")}>
              {CROPS.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">{T("sowingDate")}</label>
            <input type="date" value={sowingDate} onChange={(e) => setSowingDate(e.target.value)} className="liquid-glass-input w-full" aria-label={T("sowingDate")} />
          </div>
          <div className="flex items-end">
            <button onClick={generate} disabled={loading} className="liquid-glass-btn w-full" style={{ minHeight: 44 }}>
              {loading ? T("loading") : T("generateCalendar")}
            </button>
          </div>
        </div>
      </div>

      {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

      {/* Harvest Summary Banner */}
      {data && (
        <div className="bg-gradient-to-r from-green-600 to-emerald-500 rounded-xl p-3 sm:p-4 text-white mb-4">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-sm">
            <div><span className="opacity-70">{T("crop")}:</span> <strong>{data.crop}</strong></div>
            <div><span className="opacity-70">{T("sowingDate")}:</span> <strong>{data.sowing_date}</strong></div>
            <div><span className="opacity-70">{T("expectedHarvest")}:</span> <strong>{data.expected_harvest}</strong></div>
            <div><span className="opacity-70">{T("totalWeeks")}:</span> <strong>{data.total_weeks}</strong></div>
          </div>
        </div>
      )}

      {/* Timeline */}
      {data && (
        <div className="space-y-2">
          {data.timeline.map((entry, _i) => {
            const isOpen = expandedWeek === entry.week_number;
            const icon = STAGE_ICONS[entry.stage] || "📋";
            return (
              <div
                key={entry.week_number}
                className="liquidGlass-wrapper liquidGlass-card rounded-xl transition-all"
                style={{ cursor: "pointer" }}
                onClick={() => toggleWeek(entry.week_number)}
              >
                <div className="liquidGlass-effect" />
                <div className="liquidGlass-tint" />
                <div className="liquidGlass-shine" />
                <div className="liquidGlass-text p-3 sm:p-4">
                  <div className="flex items-center gap-3" style={{ minHeight: 44 }}>
                    <span className="text-2xl">{icon}</span>
                    <div className="flex-1">
                      <p className="font-semibold text-sm sm:text-base">
                        {T("week")} {entry.week_number}: {entry.stage}
                      </p>
                      <p className="text-xs opacity-60">
                        {entry.date_range.start} → {entry.date_range.end}
                      </p>
                    </div>
                    <span className="text-lg transition-transform" style={{ transform: isOpen ? "rotate(180deg)" : "rotate(0deg)" }}>
                      ▼
                    </span>
                  </div>

                  {isOpen && (
                    <div className="mt-3 pt-3 border-t border-white/30 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                      <div>
                        <p className="font-medium mb-0.5">💧 {T("irrigation")}</p>
                        <p className="opacity-70">{entry.irrigation}</p>
                      </div>
                      <div>
                        <p className="font-medium mb-0.5">🧪 {T("fertilizer")}</p>
                        <p className="opacity-70">{entry.fertilizer}</p>
                      </div>
                      <div>
                        <p className="font-medium mb-0.5">🐛 {T("pestManagement")}</p>
                        <p className="opacity-70">{entry.pest_management}</p>
                      </div>
                      <div>
                        <p className="font-medium mb-0.5">💡 {T("tip")}</p>
                        <p className="opacity-70">{entry.tip}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
