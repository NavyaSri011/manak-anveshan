import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import { ShieldCheck, FileText, Search, Network, History, Building2, Download, Settings, Award } from 'lucide-react';

export default function Header() {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: ShieldCheck, end: true },
    { to: '/new-analysis', label: 'New Analysis', icon: FileText },
    { to: '/explorer', label: 'Standards Explorer', icon: Search },
    { to: '/graph', label: 'Standards Graph', icon: Network },
    { to: '/history', label: 'Tender History', icon: History },
    //{ to: '/portal', label: 'Mock GeM Portal', icon: Building2 },
    { to: '/reports', label: 'Reports', icon: Download },
    { to: '/settings', label: 'Settings / About', icon: Settings },
  ];

  return (
    <header className="bg-slate-900 text-white border-b-4 border-amber-600 shadow-sm no-print">
      {/* Top Banner Notice */}
      <div className="bg-slate-950 px-4 py-1.5 text-xs text-slate-300 border-b border-slate-800 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <span className="bg-amber-600 text-slate-950 font-bold px-1.5 py-0.5 rounded text-[10px]">SIH 2026 PROTOTYPE</span>
          <span className="hidden sm:inline">Indian Standards Decision Support System for Procurement Officials</span>
        </div>
        <div className="flex items-center space-x-3 text-slate-400">
          <span>Non-Autonomous Decision Support</span>
          <span>|</span>
          <span className="text-amber-400 font-medium">No Official BIS Affiliation</span>
        </div>
      </div>

      {/* Main Header Branding */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-slate-800 border border-slate-700 rounded-md flex items-center justify-center text-amber-500 shadow-inner">
            <Award className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-baseline space-x-2">
              <h1 className="text-2xl font-bold tracking-tight text-white font-serif">
                MANAK ANVESHAN
              </h1>
              <span className="text-xs bg-emerald-950 border border-emerald-700 text-emerald-300 font-mono px-2 py-0.5 rounded">
                v1.0-SIH2026
              </span>
            </div>
            <p className="text-xs text-slate-300 tracking-wide font-medium mt-0.5">
              Indian Standards Intelligence for Procurement
            </p>
          </div>
        </div>

        {/* Quick Institutional Meta Badge */}
        <div className="hidden lg:flex items-center space-x-6 text-xs text-slate-300 bg-slate-800/80 border border-slate-700 px-4 py-2 rounded-md">
          <div>
            <div className="text-slate-400 font-mono text-[10px] uppercase tracking-wider">Target Users</div>
            <div className="font-semibold text-slate-200">Procurement & Tender Committees</div>
          </div>
          <div className="h-6 w-px bg-slate-700"></div>
          <div>
            <div className="text-slate-400 font-mono text-[10px] uppercase tracking-wider">Compliance</div>
            <div className="font-semibold text-emerald-400 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" /> Deterministic QCO Rules
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Bar */}
      <nav className="bg-slate-800 border-t border-slate-700 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex space-x-1 overflow-x-auto py-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `flex items-center space-x-2 px-3 py-2 rounded-md text-xs font-semibold whitespace-nowrap transition-colors ${
                    isActive
                      ? 'bg-slate-900 text-amber-400 border border-amber-600/40'
                      : 'text-slate-300 hover:bg-slate-700/60 hover:text-white'
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </div>
      </nav>
    </header>
  );
}
