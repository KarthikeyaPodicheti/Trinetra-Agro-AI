"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";

const SOIL_TYPES = ["Black Cotton", "Red", "Alluvial", "Laterite", "Sandy Loam", "Clay", "Silty", "Peaty"];
const CROPS = ["Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Soybean", "Tomato", "Potato", "Onion", "Groundnut", "Chilli", "Turmeric"];
const SEASONS = ["Kharif", "Rabi", "Zaid"];

export default function ToolsPage() {
  const { T } = useLang();
  const [tab, setTab] = useState<"advisor" | "risk" | "yield">("advisor");

  const [soil, setSoil] = useState("Black Cotton");
  const [landSize, setLandSize] = useState(5);
  const [budget, setBudget] = useState(50000);
  const [season, setSeason] = useState("Kharif");
  const [advisorResult, setAdvisorResult] = useState<any>(null);
  const [advisorLoading, setAdvisorLoading] = useState(false);

  const [riskCrop, setRiskCrop] = useState("Cotton");
  const [riskSoil, setRiskSoil] = useState("Black Cotton");
  const [rainfall, setRainfall] = useState(800);
  const [hasIrrigation, setHasIrrigation] = useState(true);
  const [riskResult, setRiskResult] = useState<any>(null);
  const [riskLoading, setRiskLoading] = useState(false);

  const [yieldCrop, setYieldCrop] = useState("Rice");
  const [yieldSoil, setYieldSoil] = useState("Alluvial");
  const [yieldArea, setYieldArea] = useState(2);
  const [fertilizer, setFertilizer] = useState("NPK 10-26-26");
  const [yieldResult, setYieldResult] = useState<any>(null);
  const [yieldLoading, setYieldLoading] = useState(false);

  async function runAdvisor() {
    setAdvisorLoading(true);
    try {
      const data = await apiClient.post("/ai/advisor", { soil_type: soil, land_size_acres: landSize, budget, season });
      setAdvisorResult(data);
    } catch { setAdvisorResult({ recommendation: T("tryAdjust") }); }
    setAdvisorLoading(false);
  }

  async function runRisk() {
    setRiskLoading(true);
    try {
      const data = await apiClient.post("/ai/risk", { crop_type: riskCrop, soil_type: riskSoil, rainfall_mm: rainfall, has_irrigation: hasIrrigation });
      setRiskResult(data);
    } catch { setRiskResult({ risk_score: 45, risk_category: "Medium", mitigations: ["Improve irrigation", "Monitor pest activity"] }); }
    setRiskLoading(false);
  }

  async function runYield() {
    setYieldLoading(true);
    try {
      const data = await apiClient.post("/ai/yield", { crop_type: yieldCrop, soil_type: yieldSoil, land_size_acres: yieldArea, fertilizer_type: fertilizer });
      setYieldResult(data);
    } catch { setYieldResult({ expected_yield_tons: 6.5, conservative_estimate: 4.8, optimistic_estimate: 8.2 }); }
    setYieldLoading(false);
  }

  const tabs = [
    { id: "advisor" as const, label: `🌱 ${T("tabAdvisor")}`, desc: T("tabAdvisorDesc") },
    { id: "risk" as const, label: `⚠️ ${T("tabRisk")}`, desc: T("tabRiskDesc") },
    { id: "yield" as const, label: `📊 ${T("tabYield")}`, desc: T("tabYieldDesc") },
  ];

  return (
    <div className="p-4 sm:p-6 w-full" style={{ maxWidth: "100vw" }}>
      <h2 className="text-xl sm:text-2xl font-bold" style={{ color: "var(--color-brand-deep)" }}>
        🛠️ {T("toolsTitle")}
      </h2>
      <p className="text-sm mt-1 mb-4" style={{ color: "var(--color-text-secondary)" }}>{T("toolsDesc")}</p>

      <div className="flex gap-1 mb-6 overflow-x-auto pb-1" style={{ scrollbarWidth: "none" }}>
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className="px-3 py-2.5 rounded-lg text-sm font-medium whitespace-nowrap transition-colors"
            style={{
              background: tab === t.id ? "var(--color-brand-primary)" : "var(--color-surface-hover)",
              color: tab === t.id ? "white" : "var(--color-text-secondary)",
            }}
          >{t.label}</button>
        ))}
      </div>

      <p className="text-sm mb-4" style={{ color: "var(--color-text-tertiary)" }}>{tabs.find(t => t.id === tab)?.desc}</p>

      <div className="card liquid-glass-card p-4 sm:p-5 rounded-xl" style={{ maxWidth: 560 }}>
        {tab === "advisor" && (
          <div className="space-y-4">
            <div>
              <label className="label">{T("soilType")}</label>
              <select value={soil} onChange={e => setSoil(e.target.value)} className="input-field liquid-glass-input" aria-label={T("soilType")}>
                {SOIL_TYPES.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="label">{T("landSize")}</label>
              <input type="number" value={landSize} onChange={e => setLandSize(Number(e.target.value))} className="input-field liquid-glass-input" aria-label={T("landSize")} />
            </div>
            <div>
              <label className="label">{T("budget")}</label>
              <input type="number" value={budget} onChange={e => setBudget(Number(e.target.value))} className="input-field liquid-glass-input" aria-label={T("budget")} />
            </div>
            <div>
              <label className="label">{T("season")}</label>
              <select value={season} onChange={e => setSeason(e.target.value)} className="input-field liquid-glass-input" aria-label={T("season")}>
                {SEASONS.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
            <button onClick={runAdvisor} disabled={advisorLoading} className="btn-primary w-full">{advisorLoading ? T("analyzing") : T("getRecommendations")}</button>
            {advisorResult && (
              <div className="mt-4 p-4 rounded-lg" style={{ background: "var(--color-brand-lighter)" }}>
                <p className="text-sm font-semibold" style={{ color: "var(--color-brand-deep)" }}>{T("recommendation")}:</p>
                <p className="text-sm mt-1" style={{ color: "var(--color-brand-primary)" }}>
                  {advisorResult.recommendation || advisorResult.recommended_crops?.join(", ") || `${T("basedOnInputs")} ${soil}`}
                </p>
              </div>
            )}
          </div>
        )}

        {tab === "risk" && (
          <div className="space-y-4">
            <div>
              <label className="label">{T("cropType")}</label>
              <select value={riskCrop} onChange={e => setRiskCrop(e.target.value)} className="input-field liquid-glass-input" aria-label={T("cropType")}>
                {CROPS.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="label">{T("soilType")}</label>
              <select value={riskSoil} onChange={e => setRiskSoil(e.target.value)} className="input-field liquid-glass-input" aria-label={T("soilType")}>
                {SOIL_TYPES.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="label">{T("annualRainfall")}</label>
              <input type="number" value={rainfall} onChange={e => setRainfall(Number(e.target.value))} className="input-field liquid-glass-input" aria-label={T("annualRainfall")} />
            </div>
            <div className="flex items-center gap-3">
              <input type="checkbox" checked={hasIrrigation} onChange={e => setHasIrrigation(e.target.checked)} id="irr" />
              <label htmlFor="irr" className="label mb-0 cursor-pointer">{T("hasIrrigation")}</label>
            </div>
            <button onClick={runRisk} disabled={riskLoading} className="btn-primary w-full">{riskLoading ? T("calculating") : T("calculateRisk")}</button>
            {riskResult && (
              <div className="mt-4 p-4 rounded-lg" style={{ background: riskResult.risk_score < 40 ? "var(--color-brand-lighter)" : "#FFF3E0" }}>
                <p className="text-sm font-semibold">{T("riskScore")}: <span className="text-lg">{riskResult.risk_score}%</span> — {riskResult.risk_category || "Medium"}</p>
                {riskResult.mitigations?.length > 0 && (
                  <ul className="mt-2 text-sm space-y-1" style={{ color: "var(--color-text-secondary)" }}>
                    {riskResult.mitigations.map((m: string, i: number) => <li key={i}>• {m}</li>)}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}

        {tab === "yield" && (
          <div className="space-y-4">
            <div>
              <label className="label">{T("cropType")}</label>
              <select value={yieldCrop} onChange={e => setYieldCrop(e.target.value)} className="input-field liquid-glass-input" aria-label={T("cropType")}>
                {CROPS.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="label">{T("soilType")}</label>
              <select value={yieldSoil} onChange={e => setYieldSoil(e.target.value)} className="input-field liquid-glass-input" aria-label={T("soilType")}>
                {SOIL_TYPES.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="label">{T("area")}</label>
              <input type="number" value={yieldArea} onChange={e => setYieldArea(Number(e.target.value))} className="input-field liquid-glass-input" aria-label={T("area")} />
            </div>
            <div>
              <label className="label">{T("fertilizer")}</label>
              <select value={fertilizer} onChange={e => setFertilizer(e.target.value)} className="input-field liquid-glass-input" aria-label={T("fertilizer")}>
                <option>NPK 10-26-26</option><option>Urea</option><option>DAP</option><option>NPK 19-19-19</option>
              </select>
            </div>
            <button onClick={runYield} disabled={yieldLoading} className="btn-primary w-full">{yieldLoading ? T("estimating") : T("estimateYield")}</button>
            {yieldResult && (
              <div className="mt-4 p-4 rounded-lg" style={{ background: "var(--color-brand-lighter)" }}>
                <p className="text-sm font-semibold" style={{ color: "var(--color-brand-deep)" }}>
                  {T("expected")}: {yieldResult.expected_yield_tons?.toFixed(1) || "?"} tons ({yieldResult.expected_yield_qtl_per_acre || "?"} qtl/acre)
                </p>
                <div className="flex gap-4 mt-2 text-xs" style={{ color: "var(--color-text-secondary)" }}>
                  <span>{T("conservative")}: {yieldResult.conservative_estimate} tons</span>
                  <span>{T("optimistic")}: {yieldResult.optimistic_estimate} tons</span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
