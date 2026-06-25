"use client";

import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-emerald-500/30">
      {/* HEADER */}
      <header className="px-6 py-5 max-w-7xl mx-auto w-full flex items-center justify-between border-b border-slate-900/80 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 bg-gradient-to-tr from-emerald-400 to-indigo-500 rounded-xl flex items-center justify-center">
            <span className="font-extrabold text-white text-lg">W</span>
          </div>
          <span className="text-xl font-bold tracking-tight text-white">Welth</span>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/login" className="px-4 py-2 text-slate-400 hover:text-slate-200 transition-colors font-medium">
            Log in
          </Link>
          <Link href="/register" className="px-5 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 hover:brightness-110 active:scale-95 transition-all duration-300 font-bold rounded-xl shadow-lg shadow-emerald-500/10">
            Sign up
          </Link>
        </div>
      </header>

      {/* HERO SECTION */}
      <main className="flex-1 flex flex-col items-center justify-center max-w-5xl mx-auto px-6 py-20 text-center gap-8 relative overflow-hidden">
        {/* Glow Effects */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[120px] pointer-events-none -z-10" />
        <div className="absolute top-1/3 left-1/3 w-[300px] h-[300px] bg-indigo-500/10 rounded-full blur-[100px] pointer-events-none -z-10" />

        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-slate-800 bg-slate-900/50 backdrop-blur-sm text-xs font-semibold text-emerald-400 tracking-wide">
          ✨ Introducing Welth AI 1.0
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight leading-none text-white max-w-4xl">
          Master Your Money with <span className="gradient-text">AI Intelligence</span>
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Welth is the premium, enterprise-grade personal finance suite that automatically categorizes transactions, forecasts spending patterns, and drafts custom financial advice.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 items-center justify-center mt-4">
          <Link href="/register" className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-emerald-400 via-teal-400 to-indigo-500 text-slate-950 font-extrabold rounded-2xl shadow-xl shadow-emerald-500/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300">
            Start Free Trial
          </Link>
          <Link href="/login" className="w-full sm:w-auto px-8 py-4 bg-slate-900/80 hover:bg-slate-900 border border-slate-800 text-slate-200 font-bold rounded-2xl transition-all duration-300">
            Contact Sales
          </Link>
        </div>

        {/* FEATURES GRID */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-24">
          <div className="glass-card p-8 rounded-3xl text-left hover:border-slate-700/60 transition-all duration-300">
            <div className="h-12 w-12 rounded-2xl bg-emerald-500/10 flex items-center justify-center text-emerald-400 mb-6 font-bold text-xl">🤖</div>
            <h3 className="text-xl font-bold text-white mb-3">AI Transactions Parser</h3>
            <p className="text-slate-400 leading-relaxed">
              Upload receipt images or connect feeds. Gemini AI parses items, merchant names, tax breakdowns, and categorizes automatically.
            </p>
          </div>
          <div className="glass-card p-8 rounded-3xl text-left hover:border-slate-700/60 transition-all duration-300">
            <div className="h-12 w-12 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-6 font-bold text-xl">📈</div>
            <h3 className="text-xl font-bold text-white mb-3">XGBoost Predictions</h3>
            <p className="text-slate-400 leading-relaxed">
              Our integrated Machine Learning engine monitors rolling averages and lag data to predict overspending before it occurs.
            </p>
          </div>
          <div className="glass-card p-8 rounded-3xl text-left hover:border-slate-700/60 transition-all duration-300">
            <div className="h-12 w-12 rounded-2xl bg-teal-500/10 flex items-center justify-center text-teal-400 mb-6 font-bold text-xl">🔒</div>
            <h3 className="text-xl font-bold text-white mb-3">Enterprise Grade Security</h3>
            <p className="text-slate-400 leading-relaxed">
              Equipped with double-submit cookie CSRF validation, rate limiting sliding windows, and bcrypt password encryptions.
            </p>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="border-t border-slate-900 py-8 px-6 text-center text-slate-500 text-sm">
        <p>&copy; {new Date().getFullYear()} Welth Inc. All rights reserved.</p>
      </footer>
    </div>
  );
}
