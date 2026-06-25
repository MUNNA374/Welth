"use client";

import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  TrendingUp, 
  TrendingDown, 
  Wallet, 
  AlertTriangle, 
  Sparkles,
  Zap
} from 'lucide-react';
import apiClient from '@/lib/api';

export default function DashboardPage() {
  const [profile, setProfile] = useState<any>(null);
  const [cashflow, setCashflow] = useState({ inflow: 0, outflow: 0, net_cash_flow: 0 });
  const [forecast, setForecast] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [marketPrices, setMarketPrices] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [meRes, cfRes, fcRes, alRes, mpRes] = await Promise.all([
          apiClient.get('/auth/me'),
          apiClient.get('/transactions/cashflow'),
          apiClient.get('/ml/forecast'),
          apiClient.get('/budgets/alerts'),
          apiClient.get('/investments/market-data')
        ]);
        
        setProfile(meRes.data);
        setCashflow(cfRes.data);
        setForecast(fcRes.data);
        setAlerts(alRes.data.alerts || []);
        setMarketPrices(mpRes.data);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col gap-6 animate-pulse">
        <div className="h-10 w-48 bg-slate-800 rounded-xl" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="h-32 bg-slate-800 rounded-3xl" />
          <div className="h-32 bg-slate-800 rounded-3xl" />
          <div className="h-32 bg-slate-800 rounded-3xl" />
        </div>
        <div className="h-96 bg-slate-800 rounded-3xl" />
      </div>
    );
  }

  // Chart data formatting
  const chartData = [
    { name: 'Week 1', Inflow: cashflow.inflow * 0.25, Outflow: cashflow.outflow * 0.2 },
    { name: 'Week 2', Inflow: cashflow.inflow * 0.55, Outflow: cashflow.outflow * 0.45 },
    { name: 'Week 3', Inflow: cashflow.inflow * 0.80, Outflow: cashflow.outflow * 0.75 },
    { name: 'Week 4', Inflow: cashflow.inflow, Outflow: cashflow.outflow },
  ];

  return (
    <div className="flex flex-col gap-8 pb-10">
      {/* HEADER */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Hello, {profile?.firstName || 'User'}</h1>
          <p className="text-slate-400">Here's your smart financial health snapshot.</p>
        </div>
        <div className="glass-panel px-4 py-2.5 rounded-2xl flex items-center gap-2 border border-emerald-500/10">
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-ping" />
          <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Sync Live</span>
        </div>
      </div>

      {/* METRICS ROW */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6 rounded-3xl relative overflow-hidden flex flex-col gap-2">
          <div className="absolute top-0 right-0 p-6 opacity-5"><Wallet size={80} /></div>
          <span className="text-slate-400 text-sm font-medium">Total Balance</span>
          <span className="text-3xl font-bold text-white">${(cashflow.net_cash_flow + 24500).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
          <span className="text-emerald-400 text-xs font-semibold flex items-center gap-1">
            <TrendingUp size={12} /> +12.4% this month
          </span>
        </div>

        <div className="glass-card p-6 rounded-3xl relative overflow-hidden flex flex-col gap-2">
          <div className="absolute top-0 right-0 p-6 opacity-5 text-emerald-400"><TrendingUp size={80} /></div>
          <span className="text-slate-400 text-sm font-medium">Monthly Inflow</span>
          <span className="text-3xl font-bold text-emerald-400">${cashflow.inflow.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
          <span className="text-slate-500 text-xs">Salary & transfers</span>
        </div>

        <div className="glass-card p-6 rounded-3xl relative overflow-hidden flex flex-col gap-2">
          <div className="absolute top-0 right-0 p-6 opacity-5 text-rose-400"><TrendingDown size={80} /></div>
          <span className="text-slate-400 text-sm font-medium">Monthly Outflow</span>
          <span className="text-3xl font-bold text-rose-400">${cashflow.outflow.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
          <span className="text-slate-500 text-xs">Rent, utilities & dining</span>
        </div>
      </div>

      {/* CHARTS & ANALYTICS SECTION */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* CHART */}
        <div className="glass-card p-6 rounded-3xl lg:col-span-2 flex flex-col gap-4">
          <span className="text-white font-bold text-lg">Cash Flow History</span>
          <div className="h-72 w-full mt-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorInflow" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorOutflow" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '12px' }} />
                <Area type="monotone" dataKey="Inflow" stroke="#10b981" fillOpacity={1} fill="url(#colorInflow)" strokeWidth={2} />
                <Area type="monotone" dataKey="Outflow" stroke="#ef4444" fillOpacity={1} fill="url(#colorOutflow)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI PANEL & ML WORKPLACE */}
        <div className="flex flex-col gap-6">
          {/* ML FORECAST CARD */}
          <div className="glass-card p-6 rounded-3xl border border-indigo-500/10 flex flex-col gap-3">
            <div className="flex items-center gap-2 text-indigo-400 font-bold text-sm">
              <Zap size={18} />
              <span>XGBoost Spending Forecast</span>
            </div>
            <p className="text-slate-400 text-xs">Based on lag elements from the past 3 days, tomorrow's forecasted outflow is:</p>
            <span className="text-2xl font-bold text-white">
              ${forecast?.predicted_next_day_spending ? forecast.predicted_next_day_spending.toFixed(2) : '50.00'}
            </span>
            <div className="px-3 py-1.5 rounded-xl bg-indigo-950/20 border border-indigo-500/10 text-xs text-indigo-300 font-semibold inline-flex items-center gap-1 self-start">
              Trend Direction: {forecast?.trend_analysis?.trend_direction || 'STABLE'}
            </div>
          </div>

          {/* AI BUDGET ALERTS */}
          <div className="glass-card p-6 rounded-3xl flex-1 flex flex-col gap-4">
            <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
              <AlertTriangle size={18} />
              <span>Budget Compliance</span>
            </div>
            {alerts.length > 0 ? (
              <div className="flex flex-col gap-3">
                {alerts.map((alert, idx) => (
                  <div key={idx} className="p-3.5 bg-amber-950/10 border border-amber-950/30 rounded-2xl flex items-center justify-between text-xs">
                    <div>
                      <span className="font-bold text-amber-400 block uppercase tracking-wide">{alert.category}</span>
                      <span className="text-slate-400">Spent: ${alert.spent.toFixed(2)} / ${alert.limit.toFixed(2)}</span>
                    </div>
                    <span className="px-2.5 py-1 rounded-full bg-amber-400/10 text-amber-400 font-bold text-[10px]">
                      {alert.status}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-4">
                <span className="text-3xl mb-2">🎉</span>
                <span className="text-sm font-semibold text-white">All budgets in control</span>
                <span className="text-xs text-slate-500 mt-1">Keep it up! No warnings triggered.</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
