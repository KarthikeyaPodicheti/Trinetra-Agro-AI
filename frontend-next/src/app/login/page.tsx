"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login, sendOtp, verifyOtp } from "@/lib/auth";

type AuthMode = "password" | "otp";

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<AuthMode>("password");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handlePasswordLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const ok = await login(email, password);
    setLoading(false);
    if (ok) {
      router.push("/");
    } else {
      setError("Invalid email or password");
    }
  }

  const [consoleOtp, setConsoleOtp] = useState("");

  async function handleSendOtp(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const otpCode = await sendOtp(phone);
    setLoading(false);
    if (otpCode !== null) {
      setConsoleOtp(otpCode);
      setOtpSent(true);
    } else {
      setError("Phone not registered. Please register first.");
    }
  }

  async function handleVerifyOtp(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const ok = await verifyOtp(phone, otp);
    setLoading(false);
    if (ok) {
      router.push("/");
    } else {
      setError("Invalid or expired OTP");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-white px-4">
      <div className="w-full max-w-sm bg-white rounded-2xl shadow-lg border border-green-100 p-8">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-green-700">🔱 Trinetra Agro AI</h1>
          <p className="text-sm text-green-500 mt-1">Vision Beyond the Fields</p>
        </div>

        {/* Tab toggle */}
        <div className="flex mb-6 bg-gray-100 rounded-lg p-1">
          <button
            onClick={() => { setMode("password"); setError(""); setOtpSent(false); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition ${
              mode === "password" ? "bg-white shadow-sm text-green-700" : "text-gray-500"
            }`}
          >
            Password
          </button>
          <button
            onClick={() => { setMode("otp"); setError(""); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition ${
              mode === "otp" ? "bg-white shadow-sm text-green-700" : "text-gray-500"
            }`}
          >
            Phone OTP
          </button>
        </div>

        {mode === "password" ? (
          <form onSubmit={handlePasswordLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="demo@farm.com"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            {error && <p className="text-red-600 text-sm text-center">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
            >
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>
        ) : (
          <div className="space-y-4">
            {!otpSent ? (
              <form onSubmit={handleSendOtp} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="+919876543210"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
                {error && <p className="text-red-600 text-sm text-center">{error}</p>}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
                >
                  {loading ? "Sending OTP..." : "Send OTP"}
                </button>
              </form>
            ) : (
              <form onSubmit={handleVerifyOtp} className="space-y-4">
                <p className="text-sm text-gray-500 text-center">OTP sent to {phone}</p>
                {consoleOtp && (
                  <p className="text-xs text-amber-600 text-center bg-amber-50 border border-amber-200 rounded-lg p-2">
                    Dev mode — OTP: <strong>{consoleOtp}</strong>
                  </p>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Enter OTP</label>
                  <input
                    type="text"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    placeholder="123456"
                    required
                    maxLength={6}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-center text-lg tracking-widest"
                  />
                </div>
                {error && <p className="text-red-600 text-sm text-center">{error}</p>}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-2.5 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-lg text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
                >
                  {loading ? "Verifying..." : "Verify & Sign In"}
                </button>
                <button
                  type="button"
                  onClick={() => { setOtpSent(false); setOtp(""); setError(""); }}
                  className="w-full text-sm text-gray-500 hover:text-gray-700"
                >
                  Change phone number
                </button>
              </form>
            )}
          </div>
        )}

        <p className="text-center text-sm text-gray-500 mt-6">
          Don&apos;t have an account?{" "}
          <Link href="/register" className="text-green-600 font-medium hover:underline">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}
