"use client";

import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";

interface FarmerProfile {
  soil_type?: string;
  land_size_acres?: number;
  budget_inr?: number;
  location?: string;
  crops?: string[];
  irrigation_type?: string;
  experience_years?: number;
}

const SOIL_TYPES = ["Black", "Red", "Alluvial", "Laterite", "Sandy", "Clay", "Loamy"];
const IRRIGATION_TYPES = ["Drip", "Sprinkler", "Flood", "Canal", "Rainfed", "Borewell"];

export default function ProfilePage() {
  const { T } = useLang();
  const [profile, setProfile] = useState<FarmerProfile>({});
  const [cropInput, setCropInput] = useState("");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get<FarmerProfile | null>("/profile").then((data) => {
      if (data) {
        setProfile(data);
        setCropInput((data.crops || []).join(", "));
      }
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  async function handleSave() {
    setSaving(true);
    setSaved(false);
    const crops = cropInput.split(",").map(c => c.trim()).filter(Boolean);
    await apiClient.post("/profile", { ...profile, crops });
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  }

  if (loading) return <div className="p-6"><p>Loading...</p></div>;

  return (
    <div className="p-6 max-w-3xl">
      <h2 className="text-2xl font-bold text-gray-800">🧑‍🌾 Farm Profile</h2>
      <p className="text-gray-500 mt-1 mb-6">Tell us about your farm — this helps the AI chatbot give personalized advice.</p>

      <div className="bg-white rounded-xl border border-green-100 p-6 shadow-sm space-y-5">
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Location / District</label>
            <input
              type="text"
              value={profile.location || ""}
              onChange={(e) => setProfile({ ...profile, location: e.target.value })}
              placeholder="e.g. Guntur, Andhra Pradesh"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Land Size (acres)</label>
            <input
              type="number"
              value={profile.land_size_acres || ""}
              onChange={(e) => setProfile({ ...profile, land_size_acres: parseFloat(e.target.value) || undefined })}
              placeholder="e.g. 5"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">Crops (comma separated)</label>
          <input
            type="text"
            value={cropInput}
            onChange={(e) => setCropInput(e.target.value)}
            placeholder="e.g. Rice, Cotton, Tomato"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Soil Type</label>
            <select
              value={profile.soil_type || ""}
              onChange={(e) => setProfile({ ...profile, soil_type: e.target.value || undefined })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="">Select...</option>
              {SOIL_TYPES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Irrigation Type</label>
            <select
              value={profile.irrigation_type || ""}
              onChange={(e) => setProfile({ ...profile, irrigation_type: e.target.value || undefined })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="">Select...</option>
              {IRRIGATION_TYPES.map(i => <option key={i} value={i}>{i}</option>)}
            </select>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Budget (₹)</label>
            <input
              type="number"
              value={profile.budget_inr || ""}
              onChange={(e) => setProfile({ ...profile, budget_inr: parseFloat(e.target.value) || undefined })}
              placeholder="e.g. 50000"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Experience (years)</label>
            <input
              type="number"
              value={profile.experience_years || ""}
              onChange={(e) => setProfile({ ...profile, experience_years: parseInt(e.target.value) || undefined })}
              placeholder="e.g. 10"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
        </div>

        <button
          onClick={handleSave}
          disabled={saving}
          className="w-full py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
        >
          {saving ? "Saving..." : "💾 Save Profile"}
        </button>

        {saved && (
          <p className="text-green-600 text-sm text-center font-medium">✅ Profile saved! The chatbot will now use your farm context.</p>
        )}
      </div>
    </div>
  );
}
