import React from 'react';
import { X, HelpCircle, CheckCircle, ShieldAlert, Award, FileText, Link as LinkIcon } from 'lucide-react';

export default function WhyRecommendedModal({ card, onClose }) {
  if (!card) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto text-slate-900">
        
        {/* Header */}
        <div className="bg-slate-900 text-white px-6 py-4 flex justify-between items-center border-b-2 border-amber-600">
          <div>
            <div className="flex items-center space-x-2">
              <HelpCircle className="w-5 h-5 text-amber-400" />
              <h3 className="text-lg font-bold font-serif">Why Recommended?</h3>
            </div>
            <p className="text-xs text-slate-300 mt-0.5">
              Evidence-backed justification for <span className="font-mono text-amber-300">{card.is_number}</span>
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded hover:bg-slate-800 transition"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5">
          {/* Summary Box */}
          <div className="bg-slate-50 border border-slate-200 rounded p-4">
            <div className="text-sm font-bold text-slate-900">{card.title}</div>
            <div className="flex items-center gap-3 mt-2 text-xs">
              <span className="bg-slate-800 text-slate-100 font-mono px-2 py-0.5 rounded font-bold">
                {card.is_number}
              </span>
              <span className="bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded">
                Classification: {card.classification}
              </span>
              <span className="text-slate-600 font-mono">
                Relevance: {Math.round(card.confidence_score * 100)}%
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-3 leading-relaxed border-t border-slate-200 pt-2">
              <span className="font-semibold text-slate-800">Scope: </span> {card.scope}
            </p>
          </div>

          {/* Reasoning Steps */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center gap-1.5">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              Algorithmic Reason Trace
            </h4>
            <div className="space-y-2">
              {card.reason && card.reason.map((r, i) => (
                <div key={i} className="bg-emerald-50/60 border border-emerald-200 rounded p-2.5 text-xs text-emerald-950 flex items-start gap-2">
                  <span className="bg-emerald-700 text-white rounded-full w-4 h-4 text-[10px] flex items-center justify-center shrink-0 mt-0.5">
                    {i + 1}
                  </span>
                  <span>{r}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Evidence Grounding */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center gap-1.5">
              <FileText className="w-4 h-4 text-indigo-600" />
              Grounding & Source Evidence
            </h4>
            <div className="space-y-2">
              {card.evidence && card.evidence.map((ev, i) => (
                <div key={i} className="bg-slate-100 border border-slate-300 rounded p-3 text-xs space-y-1">
                  <div className="flex justify-between items-center text-slate-700 font-medium">
                    <span className="font-bold text-slate-900">{ev.source}</span>
                    <span className="uppercase text-[10px] bg-slate-200 px-1.5 py-0.5 rounded font-mono">{ev.type}</span>
                  </div>
                  <div className="text-slate-600 font-mono text-[11px] bg-white p-2 rounded border border-slate-200">
                    {ev.reference}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Certification Rules */}
          {card.certification_info && (
            <div className="bg-amber-50 border border-amber-200 rounded p-4 text-xs">
              <div className="flex items-center space-x-2 text-amber-900 font-bold mb-1">
                <Award className="w-4 h-4 text-amber-600" />
                <span>Regulatory Mandate / QCO Rule</span>
              </div>
              <div className="text-amber-950 space-y-1">
                <div><span className="font-semibold">Scheme:</span> {card.certification_info.scheme}</div>
                <div><span className="font-semibold">Mandatory:</span> {card.certification_info.mandatory ? "YES (Mandatory Public Procurement Compliance)" : "NO"}</div>
                <div><span className="font-semibold">Conditions:</span> {card.certification_info.conditions}</div>
                <div className="text-[11px] text-amber-800 italic mt-1">Source: {card.certification_info.source}</div>
              </div>
            </div>
          )}

          {/* Lifecycle Warnings */}
          {card.lifecycle_alert && (
            <div className="bg-rose-50 border border-rose-300 rounded p-3.5 text-xs text-rose-950 flex items-start gap-2.5">
              <ShieldAlert className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
              <div>
                <div className="font-bold text-rose-900">Version & Amendment Alert</div>
                <div className="mt-0.5">{card.lifecycle_alert}</div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-slate-100 px-6 py-3 border-t border-slate-300 flex justify-between items-center text-xs text-slate-500">
          <span>Grounding Mode: Deterministic BIS Knowledge Base</span>
          <button
            onClick={onClose}
            className="bg-slate-900 text-white font-semibold px-4 py-1.5 rounded hover:bg-slate-800 transition"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}
