"use client";

import { useState, useRef, useEffect } from "react";
import { apiClient } from "@/lib/api";
import { useLang } from "@/lib/language";
import type { ChatResponse } from "@/lib/types";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function BotMessage({ content }: { content: string }) {
  const lines = content
    .split("\n")
    .map((l) => l.replace(/^#{1,3}\s+/, "").trim())
    .filter((l) => l.length > 0);
  return (
    <ul className="space-y-1 list-none p-0 m-0">
      {lines.map((line, i) => {
        const isBullet = /^[\-•*]\s+/.test(line);
        const text = line.replace(/^[\-•*]\s+/, "").trim();
        const parts = text.split(/\*\*(.*?)\*\*/g);
        return (
          <li key={i} className={isBullet ? "flex gap-1.5" : ""}>
            {isBullet && <span className="text-green-500 shrink-0">•</span>}
            <span>{parts.map((p, j) => j % 2 === 1 ? <strong key={j}>{p}</strong> : p)}</span>
          </li>
        );
      })}
    </ul>
  );
}

export function FloatingChat() {
  const { lang, T } = useLang();
  const [open, setOpen] = useState(false);
  const [hovered, setHovered] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: T("chatWelcome") },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open) bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;
    const userMsg: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const r = await apiClient.post<ChatResponse>("/chat/send", {
        message: userMsg.content,
        session_id: "widget",
        language: lang,
      });
      setMessages((prev) => [...prev, { role: "assistant", content: r.reply }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Connection error." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* Floating trigger button */}
      <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-1">
        {hovered && !open && (
          <div className="bg-green-600 text-white text-xs font-medium px-3 py-1.5 rounded-xl shadow-lg whitespace-nowrap">
            👋 Hello! How can I help?
          </div>
        )}
        <button
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
          onClick={() => setOpen((v) => !v)}
          aria-label="Open AI Chatbot"
          className="w-14 h-14 rounded-full bg-gradient-to-br from-green-500 to-green-600 text-2xl flex items-center justify-center shadow-lg transition-transform hover:scale-110"
          style={{ animation: open ? "none" : "chatPulse 2s infinite" }}
        >
          {open ? "✕" : hovered ? "🧑" : "🧑‍🌾"}
        </button>
      </div>

      {/* Chat window */}
      {open && (
        <div
          className="fixed bottom-24 right-6 z-50 w-80 flex flex-col rounded-2xl shadow-2xl overflow-hidden"
          style={{ height: "460px", background: "white", border: "1px solid #d1fae5" }}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-gradient-to-r from-green-600 to-green-500 text-white">
            <div className="flex items-center gap-2 text-sm font-semibold">
              <span>🧑‍🌾</span> AI Farming Assistant
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={async () => {
                  try { await apiClient.post("/chat/clear?session_id=widget"); } catch {}
                  setMessages([{ role: "assistant", content: "Chat cleared! How can I help you? 🌾" }]);
                }}
                className="text-white/80 hover:text-white text-xs"
                title="Clear chat"
              >🗑️</button>
              <button onClick={() => setOpen(false)} className="text-white/80 hover:text-white text-lg leading-none">✕</button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-3 space-y-3 bg-gray-50">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[85%] rounded-2xl px-3 py-2 text-xs leading-relaxed ${
                    msg.role === "user"
                      ? "bg-green-600 text-white rounded-br-sm"
                      : "bg-white border border-green-100 shadow-sm text-gray-800 rounded-bl-sm"
                  }`}
                >
                  {msg.role === "user" ? msg.content : <BotMessage content={msg.content} />}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white border border-green-100 shadow-sm rounded-2xl rounded-bl-sm px-3 py-2 text-xs text-gray-400">
                  <span className="animate-pulse">Thinking...</span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSend} className="flex gap-2 p-3 border-t border-gray-100 bg-white">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={T("chatPlaceholder")}
              disabled={loading}
              className="flex-1 px-3 py-2 border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-green-400 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="px-3 py-2 bg-green-600 text-white rounded-xl text-xs font-semibold hover:bg-green-700 disabled:opacity-50 transition"
            >
              {T("send")}
            </button>
          </form>
        </div>
      )}
    </>
  );
}
