"use client";

import { useState, useRef, useEffect } from "react";
import { apiClient } from "@/lib/api";
import type { ChatResponse } from "@/lib/types";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatbotPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm your AI farming assistant. Ask me anything about crops, soil, market prices, or farming techniques! 🌾",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

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
        session_id: "main",
      });
      setMessages((prev) => [...prev, { role: "assistant", content: r.reply }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Connection error. Make sure the backend is running." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function handleClear() {
    try {
      await apiClient.post("/chat/clear?session_id=main");
    } catch {
      // best effort
    }
    setMessages([
      { role: "assistant", content: "Chat cleared! How can I help you? 🌾" },
    ]);
  }

  return (
    <div className="p-6 max-w-3xl flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">💬 AI Farming Chatbot</h2>
          <p className="text-gray-500 text-sm mt-1">Ask any farming question and get an instant AI-powered answer.</p>
        </div>
        {messages.length > 1 && (
          <button
            onClick={handleClear}
            className="text-sm px-3 py-1.5 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 transition"
          >
            🗑️ Clear Chat
          </button>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2 mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
                msg.role === "user"
                  ? "bg-green-600 text-white rounded-br-md"
                  : "bg-white border border-green-100 shadow-sm rounded-bl-md"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-green-100 shadow-sm rounded-2xl rounded-bl-md px-4 py-3 text-sm text-gray-500">
              <span className="animate-pulse">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about crops, soil, weather, market tips..."
          disabled={loading}
          className="flex-1 px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="px-5 py-3 bg-gradient-to-r from-green-600 to-green-500 text-white font-semibold rounded-xl text-sm hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
        >
          Send
        </button>
      </form>
    </div>
  );
}
