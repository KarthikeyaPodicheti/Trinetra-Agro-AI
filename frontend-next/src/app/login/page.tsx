"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login, sendOtp, verifyOtp } from "@/lib/auth";
import "./login.css";

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
  const [consoleOtp, setConsoleOtp] = useState("");

  async function handlePasswordLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const ok = await login(email, password);
    setLoading(false);
    if (ok) {
      // Force-clear any stale non-Secure cookies before setting new ones
      document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + window.location.hostname;
      document.cookie = "refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + window.location.hostname;
      await new Promise(r => setTimeout(r, 200));
      window.location.href = "/";
    } else setError("Invalid email or password");
  }

  async function handleSendOtp(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const otpCode = await sendOtp(phone);
    setLoading(false);
    if (otpCode !== null) { setConsoleOtp(otpCode); setOtpSent(true); }
    else setError("Phone not registered. Please register first.");
  }

  async function handleVerifyOtp(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const ok = await verifyOtp(phone, otp);
    setLoading(false);
    if (ok) window.location.href = "/";
    else setError("Invalid or expired OTP");
  }

  return (
    <>
      <svg style={{ display: "none" }}>
        <filter id="glass-distortion" x="0%" y="0%" width="100%" height="100%" filterUnits="objectBoundingBox">
          <feTurbulence type="fractalNoise" baseFrequency="0.01 0.01" numOctaves="1" seed="5" result="turbulence" />
          <feComponentTransfer in="turbulence" result="mapped">
            <feFuncR type="gamma" amplitude="1" exponent="10" offset="0.5" />
            <feFuncG type="gamma" amplitude="0" exponent="1" offset="0" />
            <feFuncB type="gamma" amplitude="0" exponent="1" offset="0.5" />
          </feComponentTransfer>
          <feGaussianBlur in="turbulence" stdDeviation="3" result="softMap" />
          <feSpecularLighting in="softMap" surfaceScale="5" specularConstant="1" specularExponent="100" lightingColor="white" result="specLight">
            <fePointLight x="-200" y="-200" z="300" />
          </feSpecularLighting>
          <feComposite in="specLight" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="litImage" />
          <feDisplacementMap in="SourceGraphic" in2="softMap" scale="150" xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </svg>

      <div className="login-page">
        <div className="login-card">
          <div className="login-card__effect"></div>
          <div className="login-card__tint"></div>
          <div className="login-card__shine"></div>
          <div className="login-card__content">
            <div className="text-center mb-6">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-green-600 to-emerald-400 flex items-center justify-center text-3xl mx-auto mb-4 shadow-lg shadow-green-500/30" style={{ fontSize: "2rem", lineHeight: 1 }}>
                🔱
              </div>
              <h1 className="login-title">Trinetra Agro AI</h1>
              <p className="login-subtitle">Vision Beyond the Fields</p>
            </div>

            {/* Mode Toggle */}
            <div className="login-toggle">
              <button
                type="button"
                onClick={() => { setMode("password"); setError(""); setOtpSent(false); }}
                className={`login-toggle__btn ${mode === "password" ? "login-toggle__btn--active" : ""}`}
              >Password</button>
              <button
                type="button"
                onClick={() => { setMode("otp"); setError(""); }}
                className={`login-toggle__btn ${mode === "otp" ? "login-toggle__btn--active" : ""}`}
              >Phone OTP</button>
            </div>

            {mode === "password" ? (
              <form onSubmit={handlePasswordLogin} className="space-y-4">
                <div>
                  <label className="login-label">Email</label>
                  <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="demo@farm.com" required className="login-input" />
                </div>
                <div>
                  <label className="login-label">Password</label>
                  <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required className="login-input" />
                </div>
                {error && <p className="text-red-400 text-sm text-center">{error}</p>}
                <button type="submit" disabled={loading} className="login-btn">{loading ? "Signing in..." : "Sign In"}</button>
              </form>
            ) : (
              <div className="space-y-4">
                {!otpSent ? (
                  <form onSubmit={handleSendOtp} className="space-y-4">
                    <div>
                      <label className="login-label">Phone Number</label>
                      <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+919876543210" required className="login-input" />
                    </div>
                    {error && <p className="text-red-400 text-sm text-center">{error}</p>}
                    <button type="submit" disabled={loading} className="login-btn">{loading ? "Sending OTP..." : "Send OTP"}</button>
                  </form>
                ) : (
                  <form onSubmit={handleVerifyOtp} className="space-y-4">
                    <p className="text-sm text-white/80 text-center">OTP sent to {phone}</p>
                    {consoleOtp && (
                      <p className="text-xs text-amber-200 text-center bg-amber-900/30 border border-amber-500/30 rounded-lg p-2">
                        Dev mode — OTP: <strong>{consoleOtp}</strong>
                      </p>
                    )}
                    <div>
                      <label className="login-label">Enter OTP</label>
                      <input type="text" value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="123456" required maxLength={6} className="login-input text-center text-lg tracking-[0.2em]" />
                    </div>
                    {error && <p className="text-red-400 text-sm text-center">{error}</p>}
                    <button type="submit" disabled={loading} className="login-btn">{loading ? "Verifying..." : "Verify & Sign In"}</button>
                    <button type="button" onClick={() => { setOtpSent(false); setOtp(""); setError(""); }} className="w-full text-sm text-white/60 hover:text-white transition-colors">Change phone number</button>
                  </form>
                )}
              </div>
            )}

            <p className="text-center text-sm text-white/70 mt-6">
              Don&apos;t have an account?{" "}
              <Link href="/register" className="text-green-300 font-medium hover:underline">Register</Link>
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
