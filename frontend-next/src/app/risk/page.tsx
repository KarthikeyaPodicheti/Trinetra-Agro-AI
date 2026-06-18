"use client";
import { useState } from "react";

export default function RiskPage() {
  return (
    <div className="p-4 md:p-6 max-w-3xl">
      <h2 className="text-xl md:text-2xl font-bold mb-4" style={{ color: "var(--color-brand-deep)" }}>Risk Assessment</h2>
      <div className="liquid-glass-card p-4 md:p-6 rounded-2xl">
        <p className="text-sm mb-4" style={{ color: "var(--color-text-secondary)" }}>Evaluate crop failure risk based on weather, disease, market, water, and budget factors.</p>
        <div className="space-y-3">
          <select className="input-field liquid-glass-input w-full"><option>Cotton</option><option>Rice</option><option>Wheat</option><option>Sugarcane</option></select>
          <select className="input-field liquid-glass-input w-full"><option>Medium rainfall (600-1200mm)</option><option>Low rainfall (&lt;600mm)</option><option>High rainfall (&gt;1200mm)</option></select>
          <select className="input-field liquid-glass-input w-full"><option>Moderate humidity (40-70%)</option><option>Low humidity</option><option>High humidity</option></select>
          <button className="liquid-glass-btn w-full">Calculate Risk Score</button>
        </div>
      </div>
    </div>
  );
}
