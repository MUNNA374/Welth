"use client";

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { 
  LayoutDashboard, 
  ArrowLeftRight, 
  PieChart, 
  TrendingUp, 
  MessageSquare, 
  Settings, 
  LogOut, 
  ShieldAlert,
  X
} from 'lucide-react';

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Transactions', path: '/transactions', icon: ArrowLeftRight },
    { name: 'Budgets', path: '/budgets', icon: PieChart },
    { name: 'Investments', path: '/investments', icon: TrendingUp },
    { name: 'AI Advisor', path: '/ai-chat', icon: MessageSquare },
  ];

  const handleLogout = () => {
    localStorage.removeItem('token');
    document.cookie = "csrf_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    router.push('/login');
  };

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {isOpen && (
        <div 
          onClick={onClose}
          className="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 md:hidden transition-opacity duration-300"
        />
      )}

      <aside className={`
        fixed inset-y-0 left-0 z-50 md:relative md:translate-x-0
        w-64 bg-slate-950/80 backdrop-blur-xl border-r border-slate-800 text-slate-200 h-screen flex flex-col justify-between p-6
        transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        <div className="flex flex-col gap-8">
          {/* LOGO */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 bg-gradient-to-tr from-emerald-400 to-indigo-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/20">
                <span className="font-extrabold text-white text-lg">W</span>
              </div>
              <span className="text-xl font-bold tracking-tight text-white font-geist-sans">Welth</span>
            </div>
            {onClose && (
              <button 
                onClick={onClose}
                className="md:hidden p-1 text-slate-400 hover:text-slate-200 focus:outline-none"
              >
                <X size={20} />
              </button>
            )}
          </div>

          {/* NAVIGATION */}
          <nav className="flex flex-col gap-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.path;
              return (
                <Link 
                  key={item.name} 
                  href={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 font-medium ${
                    isActive 
                      ? 'bg-gradient-to-r from-emerald-500/10 to-indigo-500/10 border border-slate-700/50 text-emerald-400' 
                      : 'hover:bg-slate-900/60 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <Icon size={20} />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* FOOTER */}
        <div className="flex flex-col gap-2">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-4 py-3 rounded-xl transition-all duration-300 font-medium text-slate-400 hover:text-rose-400 hover:bg-rose-950/10"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
}
