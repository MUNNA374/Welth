"use client";

import React, { useEffect, useState } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Newspaper, 
  Briefcase, 
  DollarSign 
} from 'lucide-react';
import apiClient from '@/lib/api';

export default function InvestmentsPage() {
  const [investments, setInvestments] = useState<any[]>([]);
  const [marketData, setMarketData] = useState<any>(null);
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInvestments() {
      try {
        const [invRes, mktRes, newsRes] = await Promise.all([
          apiClient.get('/investments/'),
          apiClient.get('/investments/market-data'),
          apiClient.get('/investments/news')
        ]);
        setInvestments(invRes.data);
        setMarketData(mktRes.data);
        setNews(newsRes.data.news || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchInvestments();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col gap-6 animate-pulse">
        <div className="h-10 w-48 bg-slate-800 rounded-xl" />
        <div className="h-96 bg-slate-800 rounded-3xl" />
      </div>
    );
  }

  // Calculate portfolio totals
  const totalValue = investments.reduce((sum, inv) => sum + (inv.shares * inv.currentPrice), 0);
  const totalCost = investments.reduce((sum, inv) => sum + (inv.shares * inv.buyPrice), 0);
  const gainLoss = totalValue - totalCost;
  const gainPct = totalCost > 0 ? (gainLoss / totalCost) * 100 : 0;

  return (
    <div className="flex flex-col gap-8 pb-10">
      {/* HEADER */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Investments</h1>
          <p className="text-slate-400">Track portfolio performance and read live financial news feeds.</p>
        </div>
      </div>

      {/* INVESTMENT PERFORMANCE GRID */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6 rounded-3xl relative overflow-hidden flex flex-col gap-2">
          <span className="text-slate-400 text-sm font-medium">Portfolio Value</span>
          <span className="text-3xl font-bold text-white">${totalValue.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
          <span className="text-slate-500 text-xs">Based on current market prices</span>
        </div>

        <div className="glass-card p-6 rounded-3xl relative overflow-hidden flex flex-col gap-2">
          <span className="text-slate-400 text-sm font-medium">Invested Principal</span>
          <span className="text-3xl font-bold text-white">${totalCost.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
          <span className="text-slate-500 text-xs">Total cost basis</span>
        </div>

        <div className="glass-card p-6 rounded-3xl relative overflow-hidden flex flex-col gap-2">
          <span className="text-slate-400 text-sm font-medium">Total Returns</span>
          <span className={`text-3xl font-bold ${gainLoss >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {gainLoss >= 0 ? '+' : ''}${gainLoss.toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </span>
          <span className={`text-xs font-semibold flex items-center gap-1 ${gainLoss >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {gainLoss >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
            {gainLoss >= 0 ? '+' : ''}{gainPct.toFixed(2)}%
          </span>
        </div>
      </div>

      {/* PORTFOLIO ASSETS TABLE & LIVE WATCHLIST */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* ASSET LIST */}
        <div className="glass-card rounded-3xl overflow-hidden lg:col-span-2">
          <div className="p-6 border-b border-slate-900 font-bold text-white text-lg flex items-center gap-2">
            <Briefcase size={18} className="text-emerald-400" />
            <span>Holdings</span>
          </div>
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-900 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                <th className="px-6 py-4">Asset</th>
                <th className="px-6 py-4">Shares</th>
                <th className="px-6 py-4">Avg Buy</th>
                <th className="px-6 py-4">Current</th>
                <th className="px-6 py-4 text-right">Value</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-900 text-sm">
              {investments.map((inv) => {
                const value = inv.shares * inv.currentPrice;
                const gain = value - (inv.shares * inv.buyPrice);
                return (
                  <tr key={inv.id} className="hover:bg-slate-900/20 transition-colors">
                    <td className="px-6 py-4">
                      <div>
                        <span className="font-extrabold text-white block">{inv.symbol}</span>
                        <span className="text-slate-500 text-xs">{inv.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-300 font-medium">{inv.shares}</td>
                    <td className="px-6 py-4 text-slate-400">${inv.buyPrice.toFixed(2)}</td>
                    <td className="px-6 py-4 text-slate-300">${inv.currentPrice.toFixed(2)}</td>
                    <td className="px-6 py-4 text-right">
                      <span className="font-bold text-white block">${value.toFixed(2)}</span>
                      <span className={`text-[10px] font-bold ${gain >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {gain >= 0 ? '+' : ''}{((gain / (inv.shares * inv.buyPrice)) * 100).toFixed(2)}%
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* WATCHLIST */}
        <div className="glass-card p-6 rounded-3xl flex flex-col gap-4">
          <span className="font-bold text-white text-lg">Market Watchlist</span>
          {marketData && (
            <div className="flex flex-col gap-4">
              {/* STOCKS */}
              <div className="flex flex-col gap-2">
                <span className="text-slate-500 font-bold text-[10px] uppercase tracking-wider">Stocks</span>
                {Object.entries(marketData.stocks || {}).map(([sym, item]: any) => (
                  <div key={sym} className="flex justify-between items-center text-xs p-2.5 bg-slate-900/40 border border-slate-900 rounded-xl">
                    <span className="font-bold text-white">{sym}</span>
                    <div className="text-right">
                      <span className="font-bold text-slate-200 block">${item.price.toFixed(2)}</span>
                      <span className={`text-[10px] font-bold ${item.change >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {item.change >= 0 ? '+' : ''}{item.change.toFixed(2)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              {/* CRYPTO */}
              <div className="flex flex-col gap-2">
                <span className="text-slate-500 font-bold text-[10px] uppercase tracking-wider">Crypto</span>
                {Object.entries(marketData.crypto || {}).map(([sym, item]: any) => (
                  <div key={sym} className="flex justify-between items-center text-xs p-2.5 bg-slate-900/40 border border-slate-900 rounded-xl">
                    <span className="font-bold text-white">{sym}</span>
                    <div className="text-right">
                      <span className="font-bold text-slate-200 block">${item.price.toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
                      <span className={`text-[10px] font-bold ${item.change >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {item.change >= 0 ? '+' : ''}{item.change.toFixed(2)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* MARKET NEWS */}
      <div className="glass-card p-6 rounded-3xl">
        <div className="flex items-center gap-2 font-bold text-white text-lg mb-6 border-b border-slate-900 pb-4">
          <Newspaper size={18} className="text-emerald-400" />
          <span>Financial News</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {news.map((item, idx) => (
            <div key={idx} className="p-4 bg-slate-900/20 border border-slate-900 hover:border-slate-800 rounded-2xl flex flex-col gap-2 transition-all duration-300">
              <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wider">{item.source}</span>
              <a href={item.url} target="_blank" rel="noreferrer" className="font-bold text-white hover:text-emerald-400 transition-colors text-sm">
                {item.title}
              </a>
              <p className="text-slate-400 text-xs leading-relaxed">{item.summary}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
