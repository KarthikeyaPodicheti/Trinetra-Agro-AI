"use client";

export default function YieldPage() {
  return (
    <div className="p-4 md:p-6 max-w-3xl">
      <h2 className="text-xl md:text-2xl font-bold mb-4" style={{ color: "var(--color-brand-deep)" }}>Yield Prediction</h2>
      <div className="liquid-glass-card p-4 md:p-6 rounded-2xl">
        <p className="text-sm mb-4" style={{ color: "var(--color-text-secondary)" }}>Estimate crop yield based on fertilizer, rainfall, soil nutrients, and crop type.</p>
        <div className="space-y-3">
          <select className="input-field liquid-glass-input w-full"><option>Rice</option><option>Wheat</option><option>Maize</option><option>Sugarcane</option></select>
          <input type="number" placeholder="Fertilizer used (kg/acre)" className="input-field liquid-glass-input w-full" />
          <input type="number" placeholder="Rainfall (mm)" className="input-field liquid-glass-input w-full" />
          <select className="input-field liquid-glass-input w-full"><option>Loamy</option><option>Clay</option><option>Sandy</option><option>Alluvial</option></select>
          <button className="liquid-glass-btn w-full">Predict Yield</button>
        </div>
      </div>
    </div>
  );
}
