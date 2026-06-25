"use client";

import React, { useEffect, useState } from 'react';
import { 
  PieChart, 
  Plus, 
  Sparkles, 
  TrendingUp, 
  DollarSign 
} from 'lucide-react';
import apiClient from '@/lib/api';

export default function BudgetsPage() {
  const [budgets, setBudgets] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  // Form fields
  const [category, setCategory] = useState('FOOD');
  const [amount, setAmount] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const fetchBudgetData = async () => {
    try {
      const [bRes, aRes, tRes] = await Promise.all([
        apiClient.get('/budgets/'),
        apiClient.get('/budgets/alerts'),
        apiClient.get('/transactions/')
      ]);
      setBudgets(bRes.data);
      setAlerts(aRes.data.alerts || []);
      setTransactions(tRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBudgetData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || !startDate || !endDate) return;

    try {
      await apiClient.post('/budgets/', {
        category,
        amount: parseFloat(amount),
        startDate: new Date(startDate).toISOString(),
        endDate: new Date(endDate).toISOString(),
        period: 'MONTHLY'
      });
      setAmount('');
      setStartDate('');
      setEndDate('');
      setShowAddForm(false);
      fetchBudgetData();
    } catch (err) {
      console.error(err);
    }
  };

  // Helper: calculate total spent per category
  const getCategorySpending = (cat: string) => {
    return transactions
      .filter(tx => tx.category === cat && tx.type === 'OUTFLOW')
      .reduce((sum, tx) => sum + tx.amount, 0);
  };

  if (loading) {
    return (
      <div className="flex flex-col gap-6 animate-pulse">
        <div className="h-10 w-48 bg-slate-800 rounded-xl" />
        <div className="h-96 bg-slate-800 rounded-3xl" />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-8 pb-10">
      {/* HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Budgets</h1>
          <p className="text-slate-400">Manage and optimize limits for your core spending groups.</p>
        </div>
        <button 
          onClick={() => setShowAddForm(true)}
          className="flex items-center justify-center gap-2 px-5 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold rounded-xl hover:brightness-110 active:scale-95 transition-all duration-300 w-full sm:w-auto"
        >
          <Plus size={18} />
          <span>New Budget Limit</span>
        </button>
      </div>

      {/* CREATE BUDGET FORM */}
      {showAddForm && (
        <form onSubmit={handleCreate} className="glass-card p-6 rounded-3xl flex flex-col gap-5">
          <div className="flex items-center justify-between">
            <span className="font-bold text-white text-lg">Define Category Limit</span>
            <button type="button" onClick={() => setShowAddForm(false)} className="text-slate-500 hover:text-slate-300 text-sm">Cancel</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Category</label>
              <select 
                value={category} 
                onChange={(e) => setCategory(e.target.value)}
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 focus:outline-none"
              >
                <option value="FOOD">Food</option>
                <option value="RENT">Rent</option>
                <option value="UTILITIES">Utilities</option>
                <option value="INVESTMENT">Investment</option>
                <option value="TRAVEL">Travel</option>
                <option value="ENTERTAINMENT">Entertainment</option>
                <option value="OTHER">Other</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Budget Amount ($)</label>
              <input 
                type="number" 
                required 
                value={amount} 
                onChange={(e) => setAmount(e.target.value)} 
                placeholder="500.00"
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-emerald-500/50"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Start Date</label>
              <input 
                type="date" 
                required 
                value={startDate} 
                onChange={(e) => setStartDate(e.target.value)} 
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-emerald-500/50"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider">End Date</label>
              <input 
                type="date" 
                required 
                value={endDate} 
                onChange={(e) => setEndDate(e.target.value)} 
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-emerald-500/50"
              />
            </div>
          </div>
          <button 
            type="submit" 
            className="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold rounded-xl self-start active:scale-95 transition-all duration-300 w-full sm:w-auto flex items-center justify-center"
          >
            Create Limit
          </button>
        </form>
      )}

      {/* BUDGET SLABS GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {budgets.map((b) => {
          const spent = getCategorySpending(b.category);
          const pct = Math.min((spent / b.amount) * 100, 100);
          const isWarning = pct >= 85;
          const isExceeded = pct >= 100;

          return (
            <div key={b.id} className="glass-card p-6 rounded-3xl flex flex-col gap-4 relative overflow-hidden">
              <div className="flex items-center justify-between">
                <span className="font-extrabold text-white uppercase tracking-wider text-sm">{b.category}</span>
                <span className="text-xs text-slate-400">
                  ${spent.toFixed(2)} / <strong className="text-slate-100">${b.amount.toFixed(2)}</strong>
                </span>
              </div>

              {/* Progress bar wrapper */}
              <div className="h-3 w-full bg-slate-900 rounded-full overflow-hidden">
                <div 
                  className={`h-full rounded-full transition-all duration-500 ${
                    isExceeded 
                      ? 'bg-rose-500 shadow-lg shadow-rose-500/20' 
                      : isWarning 
                        ? 'bg-amber-400 shadow-lg shadow-amber-400/20' 
                        : 'bg-gradient-to-r from-emerald-400 to-emerald-500 shadow-lg shadow-emerald-500/20'
                  }`}
                  style={{ width: `${pct}%` }}
                />
              </div>

              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">
                  Active {new Date(b.startDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - {new Date(b.endDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </span>
                <span className={`font-bold ${isExceeded ? 'text-rose-400' : isWarning ? 'text-amber-400' : 'text-emerald-400'}`}>
                  {pct.toFixed(0)}% Used
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* AI RECOMMENDATION BOX */}
      <div className="glass-card p-6 sm:p-8 rounded-3xl border border-emerald-500/10 flex flex-col md:flex-row gap-6 items-start">
        <div className="h-12 w-12 rounded-2xl bg-emerald-500/10 flex items-center justify-center text-emerald-400 font-bold text-xl shrink-0">💡</div>
        <div className="flex flex-col gap-2">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles size={18} className="text-emerald-400" />
            <span>AI Budget Advice</span>
          </h3>
          <p className="text-slate-400 text-sm leading-relaxed">
            Your dining out expenses (category Food) are growing 12.5% week-over-week. We recommend redirecting $120.00 from your entertainment budget into stocks to capitalize on S&P 500 growth indices.
          </p>
        </div>
      </div>
    </div>
  );
}
