"use client";

import { useState } from "react";
import { apiClient } from "@/lib/api";

const FEATURES = [
  "AI Advisor",
  "Disease Scanner",
  "Market Intelligence",
  "Risk Monitor",
  "Yield Prediction",
  "Profit Calculator",
  "Voice AI",
];

export default function FeedbackPage() {
  const [feature, setFeature] = useState(FEATURES[0]);
  const [rating, setRating] = useState(4);
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!comment.trim()) {
      setError("Please add a comment before submitting.");
      return;
    }
    setError("");
    try {
      await apiClient.post("/feedback", { feature, rating, comment });
      setSubmitted(true);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to submit feedback");
    }
  }

  if (submitted) {
    return (
      <div className="p-6 max-w-2xl">
        <h2 className="text-2xl font-bold text-gray-800">💬 Send Feedback</h2>
        <p className="text-gray-500 mt-1">Help us improve Trinetra Agro AI for farmers everywhere.</p>
        <div className="mt-6 bg-green-50 border border-green-200 rounded-xl p-6 text-center">
          <p className="text-lg mb-2">✅</p>
          <p className="font-semibold text-green-800">Thank you! Your feedback helps us improve Trinetra.</p>
        </div>
        <button
          onClick={() => {
            setSubmitted(false);
            setComment("");
            setRating(4);
            setFeature(FEATURES[0]);
          }}
          className="mt-4 px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition"
        >
          Submit another
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-2xl">
      <h2 className="text-2xl font-bold text-gray-800">💬 Send Feedback</h2>
      <p className="text-gray-500 mt-1">Help us improve Trinetra Agro AI for farmers everywhere.</p>

      <form onSubmit={handleSubmit} className="mt-6 bg-white rounded-xl border border-green-100 p-6 shadow-sm space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">Which feature are you reviewing?</label>
          <select
            value={feature}
            onChange={(e) => setFeature(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            {FEATURES.map((f) => <option key={f} value={f}>{f}</option>)}
          </select>
        </div>

        <div>
          <p className="text-sm font-medium text-gray-600 mb-2">How was your experience?</p>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((n) => (
              <button
                key={n}
                type="button"
                onClick={() => setRating(n)}
                className={`w-10 h-10 rounded-lg text-sm font-bold transition ${
                  n <= rating
                    ? "bg-green-100 text-green-700 border border-green-300"
                    : "bg-gray-50 text-gray-400 border border-gray-200 hover:bg-gray-100"
                }`}
              >
                {n}
              </button>
            ))}
          </div>
          <p className="text-xs text-gray-400 mt-1">1 = Poor, 5 = Excellent</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">Your thoughts</label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="What worked well? What can we improve?"
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
          />
        </div>

        {error && <p className="text-red-600 text-sm">⚠️ {error}</p>}

        <button
          type="submit"
          className="w-full py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 transition"
        >
          Submit Feedback
        </button>
      </form>
    </div>
  );
}
