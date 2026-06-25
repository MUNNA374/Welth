"use client";

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Sidebar from '@/components/layout/sidebar';
import { Menu } from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [authorized, setAuthorized] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    } else {
      setAuthorized(true);
    }
  }, [router]);

  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [pathname]);

  if (!authorized) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="h-10 w-10 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="flex flex-col md:flex-row h-screen bg-slate-950 text-slate-100 overflow-hidden relative">
      {/* Mobile Top Header */}
      <header className="flex md:hidden items-center justify-between px-6 py-4 bg-slate-950/80 backdrop-blur-xl border-b border-slate-900 z-40 sticky top-0">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 bg-gradient-to-tr from-emerald-400 to-indigo-500 rounded-lg flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <span className="font-extrabold text-white text-md">W</span>
          </div>
          <span className="text-lg font-bold tracking-tight text-white font-geist-sans">Welth</span>
        </div>
        <button
          onClick={() => setIsMobileMenuOpen(true)}
          className="p-2 text-slate-400 hover:text-slate-200 focus:outline-none"
        >
          <Menu size={24} />
        </button>
      </header>

      {/* Sidebar (handles both desktop and mobile drawer internally) */}
      <Sidebar 
        isOpen={isMobileMenuOpen} 
        onClose={() => setIsMobileMenuOpen(false)} 
      />

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-slate-950 p-6 md:p-8">
        <div className="max-w-7xl mx-auto w-full">
          {children}
        </div>
      </main>
    </div>
  );
}
