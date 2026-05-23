"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Menu, X } from "lucide-react";
import { getUser, logout } from "@/lib/auth";
import type { UserResponse } from "@/lib/types";

const NAV_ITEMS = [
  { label: "📊  Dashboard", path: "/" },
  { label: "🌱  AI Advisor", path: "/advisor" },
  { label: "🔬  Disease Scanner", path: "/disease-scanner" },
  { label: "📈  Market Intelligence", path: "/market" },
  { label: "💬  AI Chatbot", path: "/chatbot" },
  { label: "📝  Feedback", path: "/feedback" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<UserResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const isAuthPage = pathname === "/login" || pathname === "/register";

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
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-white">
        <p className="text-green-600 font-medium">Loading...</p>
      </div>
    );
  }

  if (isAuthPage) {
    return <>{children}</>;
  }

  const sidebarContent = (
    <>
      <div className="px-5 py-6 border-b border-green-100">
        <h1 className="text-lg font-bold text-green-700">🔱 Trinetra Agro AI</h1>
        <p className="text-xs text-green-500 mt-0.5">Vision Beyond the Fields</p>
      </div>
      <div className="px-5 py-3 border-b border-green-100 text-sm text-gray-700 truncate">
        👨‍🌾 {user?.full_name || user?.email || "Farmer"}
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const isActive =
            pathname === item.path ||
            (item.path !== "/" && pathname.startsWith(item.path));
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full text-left px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-green-100 text-green-800"
                  : "text-gray-600 hover:bg-green-50 hover:text-green-700"
              }`}
            >
              {item.label}
            </button>
          );
        })}
      </nav>
      <div className="px-3 pb-4">
        <button
          onClick={handleLogout}
          className="w-full text-left px-3 py-2.5 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
        >
          🚪  Logout
        </button>
      </div>
    </>
  );

  return (
    <div className="flex min-h-screen">
      {/* Desktop sidebar */}
      <aside className="hidden md:flex md:flex-col md:w-64 bg-gradient-to-b from-[#FAFFFE] to-[#E8F5E9] border-r border-green-100 shrink-0">
        {sidebarContent}
      </aside>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/30 z-40 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-gradient-to-b from-[#FAFFFE] to-[#E8F5E9] border-r border-green-100 shadow-xl transform transition-transform duration-200 md:hidden ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex justify-end p-3">
          <button onClick={() => setSidebarOpen(false)} className="p-1 text-gray-500 hover:text-gray-700">
            <X size={20} />
          </button>
        </div>
        {sidebarContent}
      </aside>

      {/* Main area */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Mobile top bar */}
        <header className="md:hidden flex items-center justify-between px-4 py-3 border-b border-green-100 bg-white/80 backdrop-blur-sm">
          <button onClick={() => setSidebarOpen(true)} className="p-1 text-gray-600">
            <Menu size={22} />
          </button>
          <span className="text-sm font-bold text-green-700">🔱 Trinetra Agro AI</span>
          <span className="text-xs text-gray-500 truncate max-w-[100px]">
            {user?.full_name || user?.email || ""}
          </span>
        </header>

        <main className="flex-1 bg-gradient-to-br from-green-50 to-white overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
