"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { register } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const ok = await register(email, password, fullName, phone);
    setLoading(false);
    if (ok) {
      await new Promise(r => setTimeout(r, 300));
      window.location.href = "/";
    } else setError("Registration failed — email may already exist");
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

      <div className="reg-page">
        <div className="glass-card">
          <div className="glass-card__effect"></div>
          <div className="glass-card__tint"></div>
          <div className="glass-card__shine"></div>
          <div className="glass-card__content">
            <div className="text-center mb-6">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-green-600 to-emerald-400 flex items-center justify-center text-3xl mx-auto mb-4 shadow-lg shadow-green-500/30">🔱</div>
              <h1 className="glass-title">Trinetra Agro AI</h1>
              <p className="glass-subtitle">Create your account</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="glass-label">Full Name</label>
                <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Your name" className="glass-input" />
              </div>
              <div>
                <label className="glass-label">Email</label>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required className="glass-input" />
              </div>
              <div>
                <label className="glass-label">Phone (for OTP login)</label>
                <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+919876543210" className="glass-input" />
              </div>
              <div>
                <label className="glass-label">Password</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={8} className="glass-input" />
              </div>
              {error && <p className="text-red-400 text-sm text-center">{error}</p>}
              <button type="submit" disabled={loading} className="glass-btn">{loading ? "Creating account..." : "Create Account"}</button>
            </form>

            <p className="text-center text-sm text-white/70 mt-6">
              Already have an account?{" "}
              <Link href="/login" className="text-green-300 font-medium hover:underline">Sign In</Link>
            </p>
          </div>
        </div>
      </div>

      <style jsx global>{`
        .reg-page {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1rem;
          background: url("/bg.jpg") center bottom;
          background-size: 120% 200%;
          animation: regBgMove 30s ease-in-out infinite alternate;
        }
        @keyframes regBgMove {
          from { background-position: center bottom; }
          to { background-position: center top; }
        }
        .glass-card {
          position: relative;
          display: flex;
          width: 100%;
          max-width: 24rem;
          overflow: hidden;
          border-radius: 1.8rem;
          box-shadow: 0 6px 6px rgba(0,0,0,0.2), 0 0 20px rgba(0,0,0,0.1);
          transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 2.2);
        }
        .glass-card:hover { transform: scale(1.01); }
        .glass-card__effect {
          position: absolute; z-index: 0; inset: 0;
          backdrop-filter: blur(3px);
          filter: url(#glass-distortion);
          overflow: hidden; isolation: isolate;
        }
        .glass-card__tint {
          position: absolute; inset: 0; z-index: 1;
          background: rgba(255,255,255,0.25);
        }
        .glass-card__shine {
          position: absolute; inset: 0; z-index: 2;
          box-shadow: inset 2px 2px 1px 0 rgba(255,255,255,0.5), inset -1px -1px 1px 1px rgba(255,255,255,0.5);
        }
        .glass-card__content {
          position: relative; z-index: 3; width: 100%; padding: 2rem;
        }
        .glass-title {
          font-size: 1.5rem; font-weight: 700; color: #166534;
          text-shadow: 0 2px 8px rgba(255,255,255,0.4), 0 0 20px rgba(22,101,52,0.3);
        }
        .glass-subtitle {
          font-size: 0.875rem; margin-top: 0.25rem; color: #15803d;
          text-shadow: 0 1px 6px rgba(255,255,255,0.3);
        }
        .glass-label {
          display: block; font-size: 0.875rem; font-weight: 500; color: white; margin-bottom: 0.25rem;
        }
        .glass-input {
          width: 100%; padding: 0.5rem 1rem; border-radius: 0.8rem;
          background: rgba(255,255,255,0.3); backdrop-filter: blur(2px);
          border: 1px solid rgba(255,255,255,0.4);
          box-shadow: inset 2px 2px 1px rgba(255,255,255,0.5), inset -1px -1px 1px rgba(255,255,255,0.5);
          color: #fff; outline: none; transition: all 0.2s;
        }
        .glass-input::placeholder { color: rgba(255,255,255,0.5); }
        .glass-input:focus {
          background: rgba(255,255,255,0.4);
          box-shadow: inset 2px 2px 1px rgba(255,255,255,0.6), inset -1px -1px 1px rgba(255,255,255,0.6), 0 0 0 3px rgba(34,197,94,0.2);
        }
        .glass-btn {
          display: flex; align-items: center; justify-content: center;
          width: 100%; padding: 0.75rem 1.5rem; border-radius: 3rem;
          font-weight: 600; color: white; background: rgba(255,255,255,0.2);
          backdrop-filter: blur(3px); border: none; cursor: pointer;
          box-shadow: 0 6px 6px rgba(0,0,0,0.2), 0 0 20px rgba(0,0,0,0.1);
          transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 2.2); overflow: hidden;
        }
        .glass-btn:hover:not(:disabled) { padding: 0.9rem 1.8rem; background: rgba(255,255,255,0.3); }
        .glass-btn:active:not(:disabled) { transform: scale(0.98); }
        .glass-btn:disabled { opacity: 0.5; cursor: not-allowed; }
      `}</style>
    </>
  );
}
