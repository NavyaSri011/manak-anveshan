import React, { useState } from 'react';
import { Award, AlertTriangle, HelpCircle, CheckCircle2, BookOpen, ShieldCheck } from 'lucide-react';
import WhyRecommendedModal from './WhyRecommendedModal';

export default function StandardCard({ card }) {
  const [showWhyModal, setShowWhyModal] = useState(false);

  const getClassificationBadge = (cls) => {
    switch (cls) {
      case 'PRIMARY':
        return 'bg-blue-900 text-white border-blue-950';
      case 'SUPPORTING':
        return 'bg-indigo-700 text-white border-indigo-900';
      case 'NORMATIVE_REFERENCE':
        return 'bg-amber-700 text-white border-amber-900';
      case 'TEST_METHOD':
        return 'bg-emerald-800 text-white border-emerald-950';
      case 'SAFETY':
        return 'bg-rose-800 text-white border-rose-950';
      case 'INSTALLATION':
        return 'bg-cyan-800 text-white border-cyan-950';
      default:
        return 'bg-slate-700 text-white border-slate-900';
    }
  };

  const getStatusBadge = (st) => {
    if (st === 'ACTIVE') return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    if (st === 'SUPERSEDED') return 'bg-rose-100 text-rose-800 border-rose-300 font-bold';
    return 'bg-amber-100 text-amber-800 border-amber-300';
  };

  return (
    <>
      <div className="bg-white border border-slate-300 rounded-lg p-5 shadow-xs hover:border-slate-400 transition-colors flex flex-col justify-between space-y-4">
        <div>
          {/* Header row */}
          <div className="flex flex-wrap items-start justify-between gap-2 mb-2">
            <div className="flex items-center space-x-2">
              <span className="font-mono text-sm font-bold bg-slate-900 text-amber-400 px-2.5 py-1 rounded border border-slate-800">
                {card.is_number}
              </span>
              <span className={`text-[11px] font-bold px-2 py-0.5 rounded border ${getStatusBadge(card.status)}`}>
                {card.status}
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded border uppercase tracking-wide ${getClassificationBadge(card.classification)}`}>
                {card.classification.replace('_', ' ')}
              </span>
              <span className="text-xs font-mono font-semibold bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200">
                Score: {Math.round(card.confidence_score * 100)}%
              </span>
            </div>
          </div>

          {/* Title */}
          <h3 className="text-base font-bold text-slate-900 leading-snug">
            {card.title}
          </h3>

          {/* Scope */}
          <p className="text-xs text-slate-600 mt-2 line-clamp-3 leading-relaxed">
            {card.scope}
          </p>

          {/* Publication and Category info */}
          <div className="mt-3 pt-2.5 border-t border-slate-100 flex flex-wrap justify-between items-center text-[11px] text-slate-500 gap-2">
            <div><span className="font-semibold text-slate-700">Category:</span> {card.category}</div>
            <div>{card.publication_info}</div>
          </div>

          {/* Superseded Warning Banner */}
          {card.lifecycle_alert && (
            <div className="mt-3 bg-rose-50 border border-rose-300 p-2.5 rounded text-xs text-rose-900 flex items-start space-x-2">
              <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <div className="leading-snug">{card.lifecycle_alert}</div>
            </div>
          )}

          {/* Certification QCO Badge */}
          {card.certification_info && card.certification_info.status === 'Applicable' && (
            <div className="mt-2.5 bg-amber-50 border border-amber-300 p-2 rounded text-xs text-amber-950 flex items-center justify-between">
              <div className="flex items-center space-x-1.5 font-semibold">
                <Award className="w-4 h-4 text-amber-600" />
                <span>Mandatory QCO Certification</span>
              </div>
              <span className="text-[10px] bg-amber-200 font-mono px-1.5 py-0.5 rounded text-amber-900 font-bold">
                {card.certification_info.scheme}
              </span>
            </div>
          )}

          {/* Key Reasons bullets */}
          {card.reason && card.reason.length > 0 && (
            <div className="mt-3 space-y-1">
              {card.reason.slice(0, 2).map((r, i) => (
                <div key={i} className="text-xs text-slate-700 flex items-start space-x-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                  <span className="line-clamp-1">{r}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="pt-3 border-t border-slate-200 flex justify-between items-center">
          <div className="flex items-center space-x-1 text-[11px] text-slate-500 font-mono">
            <BookOpen className="w-3.5 h-3.5" />
            <span>{card.evidence ? card.evidence.length : 0} Source Evidences</span>
          </div>

          <button
            onClick={() => setShowWhyModal(true)}
            className="bg-slate-900 hover:bg-slate-800 text-amber-400 text-xs font-bold px-3 py-1.5 rounded flex items-center space-x-1.5 transition-colors border border-amber-600/30"
          >
            <HelpCircle className="w-3.5 h-3.5 text-amber-400" />
            <span>Why Recommended?</span>
          </button>
        </div>
      </div>

      {showWhyModal && (
        <WhyRecommendedModal
          card={card}
          onClose={() => setShowWhyModal(false)}
        />
      )}
    </>
  );
}
