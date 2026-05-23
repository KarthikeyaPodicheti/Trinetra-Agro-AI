"use client";

import { useState, useRef } from "react";
import { apiClient } from "@/lib/api";
import type { DiseaseResponse } from "@/lib/types";

const CROPS = ["Rice", "Tomato", "Cotton", "Potato", "Wheat"];

export default function DiseaseScannerPage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [cropType, setCropType] = useState(CROPS[0]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DiseaseResponse | null>(null);
  const [error, setError] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (f) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResult(null);
      setError("");
    }
  }

  async function handleAnalyze() {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("image", file);
      const r = await apiClient.upload<DiseaseResponse>(`/ai/disease?crop_type=${encodeURIComponent(cropType.toLowerCase())}`, formData);
      if (r.success) {
        setResult(r);
      } else {
        setError(r.error || "Analysis failed");
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 max-w-5xl">
      <h2 className="text-2xl font-bold text-gray-800">🔬 AI Disease Scanner</h2>
      <p className="text-gray-500 mt-1">Upload a leaf image for AI-powered disease detection and treatment recommendations.</p>

      <div className="mt-6 grid md:grid-cols-2 gap-6">
        {/* Left — Upload */}
        <div className="bg-white rounded-xl border border-green-100 p-5 shadow-sm space-y-4">
          <h3 className="font-semibold text-gray-700">1. Upload Image</h3>
          <div
            onClick={() => fileRef.current?.click()}
            className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:border-green-400 transition"
          >
            {preview ? (
              <img src={preview} alt="Leaf preview" className="max-h-48 mx-auto rounded-lg" />
            ) : (
              <div className="text-gray-400">
                <p className="text-3xl mb-2">📷</p>
                <p className="text-sm">Click to upload leaf/crop image</p>
                <p className="text-xs mt-1">JPG, JPEG, or PNG</p>
              </div>
            )}
            <input
              ref={fileRef}
              type="file"
              accept="image/jpeg,image/png"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
          {file && (
            <p className="text-xs text-gray-500 truncate">{file.name} ({(file.size / 1024).toFixed(1)} KB)</p>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">Crop Type</label>
            <select
              value={cropType}
              onChange={(e) => setCropType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              {CROPS.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="w-full py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
          >
            {loading ? "AI analyzing your crop image..." : "🔍  Analyze for Disease"}
          </button>
        </div>

        {/* Right — Diagnosis */}
        <div className="bg-white rounded-xl border border-green-100 p-5 shadow-sm">
          <h3 className="font-semibold text-gray-700 mb-3">2. AI Diagnosis</h3>

          {!file && (
            <p className="text-gray-400 text-sm">👈 Upload an image of a leaf on the left to see the AI diagnosis here.</p>
          )}

          {file && !loading && !result && !error && (
            <p className="text-gray-400 text-sm">👆 Click &quot;Analyze for Disease&quot; to start the scan.</p>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">{error}</div>
          )}

          {loading && (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
            </div>
          )}

          {result && (
            <div className="space-y-4">
              {result.disease.toLowerCase() === "healthy" ? (
                <div className="bg-green-50 border border-green-200 rounded-xl p-4 text-green-800 text-sm font-medium">
                  ✅ <strong>Healthy</strong> — Confidence: {(result.confidence * 100).toFixed(1)}%
                </div>
              ) : (
                <>
                  <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-800 text-sm">
                    ⚠️ <strong>Disease: {result.disease}</strong>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-gray-50 rounded-lg p-3 text-center">
                      <p className="text-xs text-gray-500">Confidence</p>
                      <p className="text-lg font-bold text-gray-800">{(result.confidence * 100).toFixed(1)}%</p>
                    </div>
                    <div className="bg-gray-50 rounded-lg p-3 text-center">
                      <p className="text-xs text-gray-500">Severity</p>
                      <p className="text-lg font-bold text-gray-800 capitalize">{result.severity || "Unknown"}</p>
                    </div>
                  </div>
                  {result.recommendation && (
                    <div>
                      <h4 className="font-semibold text-sm text-gray-700">💡 Treatment</h4>
                      <p className="text-sm text-gray-600 mt-1">{result.recommendation}</p>
                    </div>
                  )}
                  {result.prevention_tips && (
                    <div>
                      <h4 className="font-semibold text-sm text-gray-700">🛡️ Prevention</h4>
                      <ul className="space-y-1 text-sm text-gray-600 list-disc list-inside mt-1">
                        {(Array.isArray(result.prevention_tips)
                          ? result.prevention_tips
                          : [result.prevention_tips]
                        ).map((tip, i) => (
                          <li key={i}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {result.note && (
                    <div className="bg-blue-50 border border-blue-200 rounded-xl p-3 text-sm text-blue-700">{result.note}</div>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
