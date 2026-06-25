"use client";

import React, { useEffect, useState } from 'react';
import { 
  ArrowUpRight, 
  ArrowDownLeft, 
  Plus, 
  Camera, 
  Search,
  CheckCircle,
  AlertOctagon
} from 'lucide-react';
import apiClient from '@/lib/api';

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showScanner, setShowScanner] = useState(false);
  
  // Form fields
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('FOOD');
  const [type, setType] = useState('OUTFLOW');
  const [accountId, setAccountId] = useState('');

  // Scanner status
  const [scanStatus, setScanStatus] = useState('');
  const [uploading, setUploading] = useState(false);

  // Fetch transactions and default account ID
  const fetchTxs = async () => {
    try {
      const res = await apiClient.get('/transactions/');
      setTransactions(res.data);
      
      // Grab first bank/credit account to default to
      const accRes = await apiClient.get('/investments/market-data'); // Just checking data
      // Alternatively find user checking account from transactions or default
      if (res.data.length > 0) {
        setAccountId(res.data[0].accountId);
      } else {
        setAccountId("seed-checking-id");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTxs();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || !description) return;
    try {
      await apiClient.post('/transactions/', {
        accountId,
        amount: parseFloat(amount),
        category,
        description,
        type,
        date: new Date().toISOString()
      });
      // Reset form
      setAmount('');
      setDescription('');
      setShowAddForm(false);
      fetchTxs();
    } catch (err) {
      console.error(err);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setScanStatus('Uploading image to secure storage...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await apiClient.post('/transactions/upload-receipt', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const ocr = response.data.ocr_data;
      setScanStatus(`Gemini OCR Processed: Found ${ocr.merchant} matching total $${ocr.total_amount}. Transaction added!`);
      
      // Refresh list
      fetchTxs();
      setTimeout(() => {
        setShowScanner(false);
        setScanStatus('');
      }, 4000);
    } catch (err) {
      console.error(err);
      setScanStatus('OCR process failed. Please input details manually.');
    } finally {
      setUploading(false);
    }
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Transactions</h1>
          <p className="text-slate-400">Track and categorize your incomes and outflows.</p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => { setShowScanner(true); setShowAddForm(false); }}
            className="flex items-center gap-2 px-5 py-3 bg-slate-900 border border-slate-800 text-slate-200 font-bold rounded-xl hover:bg-slate-900/60 active:scale-95 transition-all duration-300"
          >
            <Camera size={18} />
            <span>Scan Receipt</span>
          </button>
          <button 
            onClick={() => { setShowAddForm(true); setShowScanner(false); }}
            className="flex items-center gap-2 px-5 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold rounded-xl hover:brightness-110 active:scale-95 transition-all duration-300"
          >
            <Plus size={18} />
            <span>Add Transaction</span>
          </button>
        </div>
      </div>

      {/* SCANNER MODAL SECTION */}
      {showScanner && (
        <div className="glass-card p-6 rounded-3xl border border-emerald-500/20 flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <span className="font-bold text-white text-lg">AI Receipt Scanner (OCR)</span>
            <button onClick={() => setShowScanner(false)} className="text-slate-500 hover:text-slate-300 text-sm">Cancel</button>
          </div>
          <div className="border border-dashed border-slate-800 bg-slate-900/20 rounded-2xl p-10 flex flex-col items-center gap-4 text-center">
            <Camera size={40} className="text-emerald-400" />
            <div>
              <p className="text-sm font-semibold text-white">Upload receipt snapshot</p>
              <p className="text-xs text-slate-500 mt-1">Accepts PNG, JPG, JPEG, or WEBP up to 5MB</p>
            </div>
            <input 
              type="file" 
              accept="image/*" 
              onChange={handleFileUpload} 
              disabled={uploading}
              className="hidden" 
              id="receipt-file-input" 
            />
            <label 
              htmlFor="receipt-file-input" 
              className={`px-4 py-2.5 bg-slate-950 hover:bg-slate-900 text-slate-300 text-xs font-bold rounded-xl border border-slate-800 cursor-pointer active:scale-95 transition-all duration-300 ${uploading ? 'pointer-events-none opacity-50' : ''}`}
            >
              Select Image
            </label>
          </div>
          {scanStatus && (
            <div className="p-4 bg-emerald-950/10 border border-emerald-500/10 text-emerald-400 text-xs rounded-2xl font-medium">
              {scanStatus}
            </div>
          )}
        </div>
      )}

      {/* MANUAL TRANSACTION FORM */}
      {showAddForm && (
        <form onSubmit={handleCreate} className="glass-card p-6 rounded-3xl flex flex-col gap-5">
          <div className="flex items-center justify-between">
            <span className="font-bold text-white text-lg">Create Transaction</span>
            <button type="button" onClick={() => setShowAddForm(false)} className="text-slate-500 hover:text-slate-300 text-sm">Cancel</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Amount ($)</label>
              <input 
                type="number" 
                step="0.01" 
                required 
                value={amount} 
                onChange={(e) => setAmount(e.target.value)} 
                placeholder="42.50"
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-emerald-500/50"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Description</label>
              <input 
                type="text" 
                required 
                value={description} 
                onChange={(e) => setDescription(e.target.value)} 
                placeholder="Whole Foods Grocery"
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-emerald-500/50"
              />
            </div>
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
                <option value="SALARY">Salary</option>
                <option value="INVESTMENT">Investment</option>
                <option value="TRAVEL">Travel</option>
                <option value="ENTERTAINMENT">Entertainment</option>
                <option value="OTHER">Other</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Type</label>
              <select 
                value={type} 
                onChange={(e) => setType(e.target.value)}
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 focus:outline-none"
              >
                <option value="OUTFLOW">Outflow</option>
                <option value="INFLOW">Inflow</option>
              </select>
            </div>
          </div>
          <button 
            type="submit" 
            className="px-6 py-4.5 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold rounded-xl self-start active:scale-95 transition-all duration-300"
          >
            Save Transaction
          </button>
        </form>
      )}

      {/* TRANSACTIONS LIST */}
      <div className="glass-card rounded-3xl overflow-hidden">
        <div className="p-6 border-b border-slate-900 flex items-center justify-between">
          <span className="font-bold text-white text-lg">Transaction History</span>
          <div className="relative w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
            <input 
              type="text" 
              placeholder="Search descriptions..." 
              className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-slate-700"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-900 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                <th className="px-6 py-4">Transaction</th>
                <th className="px-6 py-4">Category</th>
                <th className="px-6 py-4">Date</th>
                <th className="px-6 py-4 text-right">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-900 text-sm">
              {transactions.map((tx) => {
                const isInflow = tx.type === 'INFLOW';
                return (
                  <tr key={tx.id} className="hover:bg-slate-900/20 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className={`h-8 w-8 rounded-lg flex items-center justify-center ${isInflow ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
                          {isInflow ? <ArrowDownLeft size={16} /> : <ArrowUpRight size={16} />}
                        </div>
                        <div>
                          <span className="font-semibold text-white block">{tx.description || 'Transaction'}</span>
                          {tx.isFraud && (
                            <span className="inline-flex items-center gap-1 text-[10px] text-rose-400 font-semibold bg-rose-950/20 border border-rose-800/20 px-2 py-0.5 rounded-full mt-1">
                              <AlertOctagon size={10} /> Potential Fraud Alert
                            </span>
                          )}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300">
                        {tx.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-slate-400">
                      {new Date(tx.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </td>
                    <td className={`px-6 py-4 font-bold text-right ${isInflow ? 'text-emerald-400' : 'text-slate-100'}`}>
                      {isInflow ? '+' : '-'}${tx.amount.toFixed(2)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
