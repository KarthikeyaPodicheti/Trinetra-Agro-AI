"use client";

import { FloatingChat } from "@/components/FloatingChat";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Menu, X } from "lucide-react";
import { getUser, logout } from "@/lib/auth";
import { useLang, Lang } from "@/lib/language";
import type { UserResponse } from "@/lib/types";

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<UserResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const isAuthPage = pathname === "/login" || pathname === "/register";
  const { lang, setLang, T } = useLang();

  const NAV = [
    { label: `📊  ${T("dashboard")}`, path: "/" },
    { label: `🛠️  ${T("farmTools")}`, path: "/tools" },
    { label: `🔬  ${T("diseaseScanner")}`, path: "/disease-scanner" },
    { label: `📈  ${T("marketIntelligence")}`, path: "/market" },
    { label: `🤖  ${T("farmAssistant")}`, path: "/chatbot" },
    { label: `🧑‍🌾  ${T("farmProfile")}`, path: "/profile" },
    { label: `📝  ${T("feedback")}`, path: "/feedback" },
  ];

  useEffect(() => {
    if (!isAuthPage) {
      getUser().then((u) => {
        setUser(u);
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, [isAuthPage]);

  useEffect(() => {
    setSidebarOpen(false);
  }, [pathname]);

  async function handleLogout() {
    logout();
    router.push("/login");
  }

  function navigate(path: string) {
    router.push(path);
    setSidebarOpen(false);
  }

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center"><p className="text-[var(--color-brand-primary)] font-medium">Loading...</p></div>;
  }

  if (isAuthPage) {
    return <div>{children}</div>;
  }

  const sidebarContent = (
    <>
      <div className="px-5 py-6 border-b" style={{ borderColor: "var(--color-border-light)" }}>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-brand-primary)] to-[var(--color-brand-accent)] flex items-center justify-center text-xl shrink-0">{'\uD83D\uDD31'}</div>
          <div>
            <h1 className="text-base font-bold" style={{ color: "var(--color-brand-deep)" }}>Trinetra Agro AI</h1>
            <p className="text-[10px]" style={{ color: "var(--color-brand-primary)" }}>Vision Beyond the Fields</p>
          </div>
        </div>
      </div>
      <div className="px-5 py-3 border-b text-sm truncate" style={{ color: "var(--color-text-secondary)", borderColor: "var(--color-border-light)" }}>
        {'\u{1F468}\u200D\u{1F33E}'} {user?.full_name || user?.email || "Farmer"}
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV.map((item) => {
          const isActive = pathname === item.path || (item.path !== "/" && pathname.startsWith(item.path));
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full text-left px-3 py-3 rounded-lg text-sm font-medium transition-colors ${
                isActive ? "text-[var(--color-brand-deep)]" : "text-gray-600"
              }`}
              style={{ background: isActive ? "var(--color-brand-lighter)" : "transparent" }}
              onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.background = "var(--color-surface-hover)"; }}
              onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.background = "transparent"; }}
            >
              {item.label}
            </button>
          );
        })}
      </nav>
      <div className="px-3 pb-4 space-y-2">
        <div className="px-3 py-2">
          <p className="text-xs font-medium text-gray-500 mb-2">{T("language")}</p>
          <div className="flex gap-1">
            {(["English", "Hindi", "Telugu"] as Lang[]).map((l) => (
              <button key={l} onClick={() => setLang(l)}
                className={`flex-1 text-sm py-2.5 rounded-md font-medium transition-colors ${lang === l ? "bg-green-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}
              >{l === "English" ? "EN" : l === "Hindi" ? "हि" : "తె"}</button>
            ))}
          </div>
        </div>
        <button onClick={handleLogout} className="w-full text-left px-3 py-3 rounded-lg text-sm font-medium" style={{ color: "var(--color-error)" }}>
          {'\u{1F6AA}'}  {T("logout")}
        </button>
      </div>
    </>
  );

  return (
    <div className="app-shell relative" style={{ display: "flex", minHeight: "100vh", maxWidth: "100vw", overflow: "hidden" }}>
      {/* Desktop sidebar — flex child, visible only on md+ */}
      <aside className="hidden md:flex md:flex-col md:w-64 shrink-0 liquid-glass-sidebar"
        style={{ borderRight: "1px solid var(--color-border-light)" }}>
        {sidebarContent}
      </aside>

      {/* Mobile sidebar overlay — positioned absolutely, never in flex flow */}
      {sidebarOpen && (
        <>
          <div className="fixed inset-0 bg-black/30 z-40" onClick={() => setSidebarOpen(false)} />
          <aside className="fixed inset-y-0 left-0 z-50 w-[85vw] max-w-[320px] shadow-xl liquid-glass-sidebar"
            style={{ borderRight: "1px solid var(--color-border-light)" }}>
            <div className="flex justify-end p-3">
              <button onClick={() => setSidebarOpen(false)} className="p-1 text-gray-500 hover:text-gray-700"><X size={20} /></button>
            </div>
            {sidebarContent}
          </aside>
        </>
      )}

      {/* Main area — takes remaining space */}
      <div className="flex-1 flex flex-col min-h-screen" style={{ background: "transparent", minWidth: 0, maxWidth: "100%" }}>
        <header className="md:hidden flex items-center justify-between px-4 py-3 border-b liquid-glass-header" style={{ borderColor: "var(--color-border-light)" }}>
          <button onClick={() => setSidebarOpen(true)} className="p-1 text-gray-600"><Menu size={22} /></button>
          <span className="text-sm font-bold" style={{ color: "var(--color-brand-primary)" }}>Trinetra Agro AI</span>
          <span className="text-xs text-gray-500 truncate max-w-[100px]">{user?.full_name || user?.email || ""}</span>
        </header>
        <main className="flex-1 overflow-y-auto glass-bg" style={{ maxWidth: "100vw", overflowX: "hidden" }}>
          {children}
        </main>
      </div>
      {/* Floating chatbot widget — hidden on /chatbot page */}
      {pathname !== "/chatbot" && !isAuthPage && <FloatingChat />}
    </div>
  );
}
