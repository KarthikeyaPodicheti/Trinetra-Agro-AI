"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";

const STATES = ["Andhra Pradesh", "Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Uttar Pradesh", "Gujarat", "Madhya Pradesh", "Rajasthan", "Punjab"];
const CROPS = ["", "Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Soybean", "Groundnut", "Tomato", "Onion", "Potato", "Turmeric", "Chilli", "Banana"];

interface SchemeData { name: string; full_name: string; benefit: string; description: string; eligibility_reason: string; apply_url: string; documents: string[]; helpline: string; }

export default function SchemesPage() {
  const { T } = useLang();
  const [state, setState] = useState("Maharashtra");
  const [landSize, setLandSize] = useState(2);
  const [cropType, setCropType] = useState("Cotton");
  const [income, setIncome] = useState("");
  const [loading, setLoading] = useState(false);
  const [schemes, setSchemes] = useState<SchemeData[]>([]);
  const [total, setTotal] = useState(0);
  const [showAll, setShowAll] = useState(false);
  const [error, setError] = useState("");

  async function handleCheck() {
    setLoading(true);
    setError("");
    try {
      const body: any = { state, land_size_acres: landSize, crop_type: cropType };
      if (income) body.annual_income = parseFloat(income);
      const data = await apiClient.post<any>("/schemes/check", body);
      setSchemes(data.eligible || []);
      setTotal(data.total_schemes || 8);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Could not check eligibility");
    } finally {
      setLoading(false);
    }
  }

  const displayed = showAll ? schemes : schemes;

  return (
    <div className="p-4 sm:p-6 w-full" style={{ maxWidth: "100vw" }}>
      <h2 className="text-xl sm:text-2xl font-bold" style={{ color: "var(--color-brand-deep)" }}>🏛️ Government Schemes</h2>
      <p className="text-sm mt-1 mb-4" style={{ color: "var(--color-text-secondary)" }}>Check which central government farm schemes you qualify for</p>

      <form onSubmit={(e) => { e.preventDefault(); handleCheck(); }} className="card liquid-glass-card rounded-xl p-4 sm:p-5 space-y-4 mb-6" style={{ maxWidth: 560 }}>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="label">{T("state") || "State"}</label>
            <select value={state} onChange={e => setState(e.target.value)} className="input-field liquid-glass-input" aria-label="State">
              {STATES.map(s => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="label">{T("landSize")}</label>
            <input type="number" value={landSize} onChange={e => setLandSize(Number(e.target.value) || 0.5)} min={0.5} step={0.5} className="input-field liquid-glass-input" aria-label="Land size" />
          </div>
          <div>
            <label className="label">{T("cropType")}</label>
            <select value={cropType} onChange={e => setCropType(e.target.value)} className="input-field liquid-glass-input" aria-label="Crop">
              {CROPS.map(c => <option key={c} value={c}>{c || "Any / Mixed"}</option>)}
            </select>
          </div>
          <div>
            <label className="label">Annual Income (₹) <span className="text-xs font-normal" style={{ color: "var(--color-text-tertiary)" }}>(optional)</span></label>
            <input type="number" value={income} onChange={e => setIncome(e.target.value)} placeholder="e.g. 50000" className="input-field liquid-glass-input" />
          </div>
        </div>
        <button type="submit" disabled={loading} className="btn-primary w-full">
          {loading ? "Checking eligibility..." : "🔍 Check My Eligibility"}
        </button>
      </form>

      {error && <div className="mb-4 p-4 rounded-xl text-sm" style={{ background: "#FFEBEE", color: "#C62828" }}>{error}</div>}

      {loading && <div className="skeleton h-32 rounded-xl mb-4" />}

      {schemes.length > 0 && (
        <>
          <p className="text-sm mb-4" style={{ color: "var(--color-text-secondary)" }}>
            <strong style={{ color: "var(--color-brand-deep)" }}>{schemes.length} of {total}</strong> schemes you qualify for.
            {schemes.length === 0 && <span> Try adjusting your land size or crop.</span>}
          </p>
          <div className="grid gap-4" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(min(100%, 340px), 1fr))" }}>
            {displayed.map((s, i) => (
              <div key={i} className="card liquid-glass-card rounded-xl p-4 flex flex-col">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-bold text-sm" style={{ color: "var(--color-brand-deep)" }}>{s.full_name}</h3>
                  <span className="text-xs px-2 py-0.5 rounded-full font-medium" style={{ background: "var(--color-brand-lighter)", color: "var(--color-brand-primary)", whiteSpace: "nowrap" }}>✅ Eligible</span>
                </div>
                <p className="text-xs mb-3" style={{ color: "var(--color-text-secondary)" }}>{s.description}</p>
                <div className="p-3 rounded-lg mb-3" style={{ background: "var(--color-brand-lighter)" }}>
                  <p className="text-xs font-semibold mb-1" style={{ color: "var(--color-brand-deep)" }}>💰 What You Get</p>
                  <p className="text-xs" style={{ color: "var(--color-brand-primary)" }}>{s.benefit}</p>
                </div>
                <div className="mb-3">
                  <p className="text-xs font-semibold mb-1" style={{ color: "var(--color-text-secondary)" }}>📋 Documents Needed</p>
                  <ul className="text-xs space-y-0.5" style={{ color: "var(--color-text-tertiary)" }}>
                    {s.documents.map((d, j) => <li key={j}>• {d}</li>)}
                  </ul>
                </div>
                <p className="text-xs mb-3" style={{ color: "var(--color-text-tertiary)" }}>
                  📞 Helpline: {s.helpline}
                </p>
                <p className="text-xs mb-3 italic" style={{ color: "var(--color-brand-primary)" }}>✓ {s.eligibility_reason}</p>
                <div className="mt-auto">
                  <a href={s.apply_url} target="_blank" rel="noopener noreferrer"
                    className="block w-full text-center py-2.5 rounded-lg text-sm font-semibold transition-colors"
                    style={{ background: "var(--color-brand-primary)", color: "white" }}>
                    Apply Now →
                  </a>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {!loading && schemes.length === 0 && !error && (
        <div className="card liquid-glass-card rounded-xl p-8 text-center">
          <p className="text-3xl mb-2">🏛️</p>
          <p className="text-sm" style={{ color: "var(--color-text-secondary)" }}>Fill in your farm details above and click <strong>Check My Eligibility</strong>.</p>
          <p className="text-xs mt-2" style={{ color: "var(--color-text-tertiary)" }}>8 central government schemes checked against your profile. No personal data is stored.</p>
        </div>
      )}
    </div>
  );
}
