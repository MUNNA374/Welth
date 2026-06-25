"use client";

import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  ArrowRight 
} from 'lucide-react';
import apiClient from '@/lib/api';

interface Message {
  sender: 'USER' | 'AI';
  text: string;
  actions?: string[];
}

export default function AIChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    { 
      sender: 'AI', 
      text: "Hello! I am Welth AI, your premium personal financial assistant. Ask me questions about budget limits, portfolio allocations, or custom savings recommendations." 
    }
  ]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (textToSend: string) => {
    if (!textToSend.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { sender: 'USER', text: textToSend }]);
    setQuery('');
    setLoading(true);

    try {
      const response = await apiClient.post('/ai/chat', { query: textToSend });
      const advice = response.data;
      
      setMessages(prev => [...prev, { 
        sender: 'AI', 
        text: advice.advice,
        actions: advice.recommended_actions 
      }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { 
        sender: 'AI', 
        text: "I encountered an error querying my model. Please verify your internet connection or try again." 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleActionClick = (action: string) => {
    handleSend(action);
  };

  return (
    <div className="h-[calc(100vh-180px)] md:h-[calc(100vh-140px)] flex flex-col gap-6">
      {/* HEADER */}
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 bg-gradient-to-tr from-emerald-400 to-indigo-500 rounded-xl flex items-center justify-center text-white">
          <Bot size={22} />
        </div>
        <div>
          <h1 className="text-2xl font-extrabold text-white">Welth AI Advisor</h1>
          <p className="text-slate-400 text-xs">Conversational intelligence for budget modeling and savings optimization.</p>
        </div>
      </div>

      {/* CHAT CONTAINER */}
      <div className="flex-1 glass-card rounded-3xl flex flex-col justify-between overflow-hidden relative border border-slate-800/80">
        {/* Glow */}
        <div className="absolute top-10 right-10 w-[200px] h-[200px] bg-emerald-500/5 rounded-full blur-[80px] pointer-events-none" />

        {/* MESSAGES VIEW */}
        <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-6">
          {messages.map((msg, index) => {
            const isAI = msg.sender === 'AI';
            return (
              <div key={index} className={`flex gap-4 max-w-[80%] ${isAI ? 'self-start' : 'self-end flex-row-reverse'}`}>
                {/* ICON */}
                <div className={`h-8 w-8 rounded-lg flex items-center justify-center shrink-0 ${isAI ? 'bg-gradient-to-tr from-emerald-500/10 to-indigo-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-900 text-slate-300 border border-slate-800'}`}>
                  {isAI ? <Bot size={16} /> : <User size={16} />}
                </div>

                <div className="flex flex-col gap-3">
                  {/* MESSAGE TEXT */}
                  <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${isAI ? 'bg-slate-900/50 text-slate-200 border border-slate-900' : 'bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-medium'}`}>
                    {msg.text}
                  </div>

                  {/* ACTION RECOMMENDATIONS */}
                  {isAI && msg.actions && msg.actions.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-1">
                      {msg.actions.map((act, aIdx) => (
                        <button
                          key={aIdx}
                          onClick={() => handleActionClick(act)}
                          className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800/80 text-[10px] font-bold text-slate-300 border border-slate-800 rounded-xl transition-all duration-300 active:scale-95"
                        >
                          <span>{act}</span>
                          <ArrowRight size={10} className="text-emerald-400" />
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          
          {loading && (
            <div className="flex gap-4 self-start max-w-[80%]">
              <div className="h-8 w-8 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-emerald-400">
                <Bot size={16} className="animate-pulse" />
              </div>
              <div className="px-4 py-3 bg-slate-900/30 text-slate-500 text-xs border border-slate-900 rounded-2xl flex items-center gap-2">
                <span className="h-1.5 w-1.5 bg-slate-500 rounded-full animate-bounce" />
                <span className="h-1.5 w-1.5 bg-slate-500 rounded-full animate-bounce delay-100" />
                <span className="h-1.5 w-1.5 bg-slate-500 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* INPUT FORM */}
        <div className="p-4 border-t border-slate-900 bg-slate-950/40">
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSend(query); }} 
            className="flex gap-3 bg-slate-900 border border-slate-800 rounded-2xl p-2 focus-within:border-emerald-500/50 transition-colors"
          >
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask AI e.g. Suggest stock investments matching moderate risk..."
              className="flex-1 bg-transparent px-4 py-2.5 text-sm text-slate-100 focus:outline-none placeholder:text-slate-500"
            />
            <button
              type="submit"
              disabled={loading}
              className="h-10 w-10 bg-gradient-to-r from-emerald-500 to-teal-500 hover:brightness-110 text-slate-950 font-bold rounded-xl flex items-center justify-center transition-all duration-300 active:scale-95 disabled:opacity-50 shrink-0"
            >
              <Send size={16} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
