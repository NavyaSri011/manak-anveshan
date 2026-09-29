import React from 'react';
import { Shield, FileCheck, Info } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-400 text-xs border-t border-slate-800 mt-12 py-8 no-print">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <div className="text-sm font-bold text-slate-200 font-serif mb-2">MANAK ANVESHAN</div>
          <p className="text-slate-400 text-xs leading-relaxed">
            AI-powered Indian Standards recommendation decision-support system designed for public procurement officials, tender evaluation committees, and technical auditors.
          </p>
        </div>

        <div>
          <div className="text-sm font-bold text-slate-200 mb-2">Core Workflow</div>
          <ul className="space-y-1 text-slate-400 text-xs">
            <li>• Document Parsing & Requirement Normalization</li>
            <li>• Hybrid Retrieval & Applicability Classification</li>
            <li>• Version Alerting & Outdated Standard Warning</li>
            <li>• Mandatory QCO / BIS Certification Verification</li>
          </ul>
        </div>

        <div className="bg-slate-950 p-3.5 rounded border border-slate-800">
          <div className="flex items-center space-x-1.5 text-amber-400 font-bold mb-1.5">
            <Info className="w-4 h-4" />
            <span>Prototype Disclaimer</span>
          </div>
          <p className="text-[11px] leading-snug text-slate-400">
            This application is an SIH 2026 prototype submission. It is a decision-support tool and does not claim official affiliation with the Bureau of Indian Standards (BIS) or government authorities.
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6 pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row justify-between text-[11px] text-slate-500">
        <div>© 2026 MANAK ANVESHAN • Smart India Hackathon Prototype</div>
        <div>Indian Standards Intelligence for Procurement</div>
      </div>
    </footer>
  );
}
