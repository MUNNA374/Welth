"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import apiClient from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await apiClient.post('/auth/register', {
        email,
        password,
        firstName,
        lastName,
      });

      setSuccess('Account created successfully! Redirecting to login page...');
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-emerald-500/5 rounded-full blur-[100px] pointer-events-none -z-10" />

      <div className="w-full max-w-md glass-card p-10 rounded-3xl shadow-2xl relative">
        {/* LOGO */}
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="h-9 w-9 bg-gradient-to-tr from-emerald-400 to-indigo-500 rounded-xl flex items-center justify-center">
            <span className="font-extrabold text-white text-lg">W</span>
          </div>
          <span className="text-xl font-bold tracking-tight text-white">Welth</span>
        </div>

        <h2 className="text-2xl font-bold text-center text-white mb-2">Create Account</h2>
        <p className="text-slate-400 text-sm text-center mb-8">Build your smart finance dashboard</p>

        {error && (
          <div className="mb-6 p-4 bg-rose-950/20 border border-rose-800/40 rounded-2xl text-rose-400 text-sm">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-emerald-950/20 border border-emerald-800/40 rounded-2xl text-emerald-400 text-sm">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">First Name</label>
              <input
                type="text"
                required
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="Alex"
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl focus:border-emerald-500/50 focus:outline-none transition-colors text-slate-100"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Last Name</label>
              <input
                type="text"
                required
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Finance"
                className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl focus:border-emerald-500/50 focus:outline-none transition-colors text-slate-100"
              />
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl focus:border-emerald-500/50 focus:outline-none transition-colors text-slate-100"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl focus:border-emerald-500/50 focus:outline-none transition-colors text-slate-100"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-4 bg-gradient-to-r from-emerald-400 to-teal-500 text-slate-950 font-bold rounded-xl shadow-lg shadow-emerald-500/10 hover:brightness-110 active:scale-95 transition-all duration-300 disabled:opacity-50"
          >
            {loading ? 'Registering...' : 'Create Account'}
          </button>
        </form>

        <p className="text-slate-500 text-sm text-center mt-8">
          Already have an account?{' '}
          <Link href="/login" className="text-emerald-400 hover:text-emerald-300 font-semibold">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
