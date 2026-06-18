"use client";
import { useState } from "react";

export default function AdvisorPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  return (
    <div className="p-4 md:p-6 max-w-3xl">
      <h2 className="text-xl md:text-2xl font-bold mb-4" style={{ color: "var(--color-brand-deep)" }}>AI Crop Advisor</h2>
      <div className="liquid-glass-card p-4 md:p-6 rounded-2xl">
        <p className="text-sm mb-4" style={{ color: "var(--color-text-secondary)" }}>Get personalized crop recommendations based on your soil type, budget, and season.</p>
        <div className="space-y-3">
          <select className="input-field liquid-glass-input w-full"><option>Black Cotton Soil</option><option>Red Soil</option><option>Alluvial Soil</option><option>Loamy Soil</option><option>Sandy Soil</option></select>
          <input type="number" placeholder="Land size (acres)" className="input-field liquid-glass-input w-full" />
          <input type="number" placeholder="Budget (rupees)" className="input-field liquid-glass-input w-full" />
          <select className="input-field liquid-glass-input w-full"><option>Kharif (Jun-Oct)</option><option>Rabi (Nov-Mar)</option><option>Zaid (Apr-Jun)</option></select>
          <button onClick={async () => { setLoading(true); try { const r = await fetch("/api/advisor"); setResult(await r.json()); } finally { setLoading(false); } }} className="liquid-glass-btn w-full">{loading ? "Analyzing..." : "Get Recommendations"}</button>
        </div>
        {result && <div className="mt-4 p-4 rounded-xl liquid-glass-card"><p className="font-semibold">Recommendations:</p><pre className="text-sm mt-2 whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre></div>}
      </div>
    </div>
  );
}
