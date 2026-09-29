import React, { useEffect, useState } from 'react';
import { useLocation, useSearchParams, Link } from 'react-router-dom';
import { ShieldCheck, Award, AlertTriangle, Download, Network, CheckCircle, HelpCircle, ArrowLeft, RefreshCw, FileCheck } from 'lucide-react';
import { getAnalysisDetail } from '../services/api';
import StandardCard from '../components/StandardCard';

export default function AnalysisResults() {
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const analysisIdFromQuery = searchParams.get('id');

  const [data, setData] = useState(location.state?.resultData || null);
  const [loading, setLoading] = useState(!location.state?.resultData && !!analysisIdFromQuery);
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    if (!data && analysisIdFromQuery) {
      getAnalysisDetail(analysisIdFromQuery)
        .then((res) => setData(res))
        .catch((err) => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [analysisIdFromQuery, data]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-slate-600">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-amber-600 border-t-transparent mb-4"></div>
        <p className="text-sm font-semibold">Loading Analysis Results from Knowledge Base...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-amber-600 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900 font-serif">No Analysis Results Selected</h2>
        <p className="text-xs text-slate-500">Please start a new tender analysis or pick a tender from analysis history.</p>
        <Link to="/new-analysis" className="bg-amber-600 text-slate-950 font-bold px-4 py-2 rounded text-xs inline-block">
          Start New Analysis
        </Link>
      </div>
    );
  }

  const {
    analysis_id,
    request_id,
    product_title,
    language,
    created_at,
    canonical_requirements,
    primary_standards = [],
    supporting_standards = [],
    normative_references = [],
    test_methods = [],
    safety_standards = [],
    installation_standards = [],
    related_standards = [],
    version_alerts = [],
    certification_summary = [],
    missing_requirements = [],
    summary_counts = {}
  } = data;

  const totalAllStandards = [
    ...primary_standards,
    ...supporting_standards,
    ...normative_references,
    ...test_methods,
    ...safety_standards,
    ...installation_standards,
    ...related_standards
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Top Header Summary */}
      <div className="bg-slate-900 text-white rounded-lg p-6 border-b-4 border-amber-600 shadow-md">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center space-x-2 text-xs font-mono">
              <span className="bg-amber-600 text-slate-950 font-bold px-2 py-0.5 rounded">{request_id}</span>
              <span className="text-slate-400">Created: {created_at}</span>
              <span className="text-slate-400 uppercase">Lang: {language}</span>
            </div>
            <h1 className="text-2xl font-bold font-serif text-white mt-1">
              {product_title}
            </h1>
            <p className="text-xs text-slate-300 mt-1">
              Category: <span className="font-semibold text-amber-400">{canonical_requirements?.product?.category || 'General'}</span> | Application: {canonical_requirements?.application}
            </p>
          </div>

          <div className="flex flex-wrap gap-2">
            <Link
              to="/graph"
              state={{ graphData: data.graph_data }}
              className="bg-slate-800 hover:bg-slate-700 text-amber-400 border border-slate-700 font-bold px-3 py-2 rounded text-xs flex items-center space-x-1.5 transition"
            >
              <Network className="w-4 h-4" />
              <span>Interactive Graph</span>
            </Link>

            <Link
              to="/reports"
              state={{ reportData: data }}
              className="bg-amber-600 hover:bg-amber-700 text-slate-950 font-bold px-3 py-2 rounded text-xs flex items-center space-x-1.5 transition shadow-xs"
            >
              <Download className="w-4 h-4" />
              <span>Generate Procurement Report</span>
            </Link>
          </div>
        </div>

        {/* Summary Counter Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3 mt-4 text-xs font-mono">
          <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700">
            <div className="text-slate-400 text-[10px] uppercase">Primary</div>
            <div className="text-lg font-bold text-blue-400">{primary_standards.length}</div>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700">
            <div className="text-slate-400 text-[10px] uppercase">Supporting</div>
            <div className="text-lg font-bold text-indigo-400">{supporting_standards.length}</div>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700">
            <div className="text-slate-400 text-[10px] uppercase">Normative</div>
            <div className="text-lg font-bold text-amber-400">{normative_references.length}</div>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700">
            <div className="text-slate-400 text-[10px] uppercase">Test Methods</div>
            <div className="text-lg font-bold text-emerald-400">{test_methods.length}</div>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700">
            <div className="text-slate-400 text-[10px] uppercase">Safety</div>
            <div className="text-lg font-bold text-rose-400">{safety_standards.length}</div>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700">
            <div className="text-slate-400 text-[10px] uppercase">Installation</div>
            <div className="text-lg font-bold text-cyan-400">{installation_standards.length}</div>
          </div>
          <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700">
            <div className="text-slate-400 text-[10px] uppercase">QCO Rules</div>
            <div className="text-lg font-bold text-emerald-300">{certification_summary.length}</div>
          </div>
        </div>
      </div>

      {/* Version & Superseded Alerts Banner */}
      {version_alerts && version_alerts.length > 0 && (
        <div className="space-y-3">
          {version_alerts.map((al, idx) => (
            <div key={idx} className="bg-rose-50 border-l-4 border-rose-600 p-4 rounded-r shadow-xs text-xs space-y-1">
              <div className="flex items-center space-x-2 text-rose-900 font-bold">
                <AlertTriangle className="w-5 h-5 text-rose-600" />
                <span>{al.title}</span>
              </div>
              <p className="text-rose-950 leading-relaxed font-medium">
                {al.message}
              </p>
              {al.action_required && (
                <div className="text-[11px] font-mono font-bold text-rose-900 bg-rose-100 p-2 rounded mt-1 border border-rose-200">
                  Recommended Action: {al.action_required}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Missing Requirements Specification Gap Alerts */}
      {missing_requirements && missing_requirements.length > 0 && (
        <div className="bg-amber-50 border border-amber-300 rounded-lg p-5 text-xs space-y-3">
          <div className="flex items-center space-x-2 text-amber-900 font-bold text-sm">
            <AlertTriangle className="w-5 h-5 text-amber-600" />
            <span>Missing Technical Requirement Gaps Identified ({missing_requirements.length})</span>
          </div>
          <p className="text-amber-950 text-xs">
            Additional specification details may be required to verify full applicability under Bureau of Indian Standards codes:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
            {missing_requirements.map((mr, i) => (
              <div key={i} className="bg-white border border-amber-200 rounded p-3 text-xs space-y-1">
                <div className="flex justify-between items-center font-bold text-slate-900">
                  <span>⚠ {mr.attribute}</span>
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${mr.importance === 'HIGH' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'}`}>
                    {mr.importance} GAP
                  </span>
                </div>
                <div className="text-slate-600">{mr.message}</div>
                <div className="text-[11px] text-slate-500 font-mono italic">Impact: {mr.impact}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Mandatory QCO Regulatory Matrix */}
      {certification_summary && certification_summary.length > 0 && (
        <div className="bg-white border border-slate-300 rounded-lg p-5 space-y-3 shadow-xs">
          <div className="flex items-center space-x-2 text-slate-900 font-bold text-sm border-b border-slate-200 pb-2">
            <Award className="w-5 h-5 text-amber-600" />
            <span>Mandatory QCO & BIS Product Certification Compliance Matrix</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-100 border-y border-slate-200 text-slate-700 font-bold uppercase tracking-wider text-[10px]">
                  <th className="py-2.5 px-3">Standard Number</th>
                  <th className="py-2.5 px-3">Certification Scheme</th>
                  <th className="py-2.5 px-3">Compliance Status</th>
                  <th className="py-2.5 px-3">Mandatory Conditions</th>
                  <th className="py-2.5 px-3">Authority Gazette Source</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 font-mono text-[11px]">
                {certification_summary.map((cs, idx) => (
                  <tr key={idx} className="hover:bg-slate-50">
                    <td className="py-2.5 px-3 font-bold text-slate-900">{cs.is_number}</td>
                    <td className="py-2.5 px-3 font-medium text-slate-800">{cs.scheme}</td>
                    <td className="py-2.5 px-3">
                      <span className="bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded text-[10px]">
                        {cs.status}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 font-sans text-xs text-slate-700">{cs.conditions}</td>
                    <td className="py-2.5 px-3 text-slate-500">{cs.source}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Filter Tabs for Classifications */}
      <div className="flex space-x-2 border-b border-slate-300 pb-2 overflow-x-auto text-xs font-semibold">
        {[
          { key: 'all', label: `All Standards (${totalAllStandards.length})` },
          { key: 'primary', label: `Primary (${primary_standards.length})` },
          { key: 'supporting', label: `Supporting (${supporting_standards.length})` },
          { key: 'normative', label: `Normative (${normative_references.length})` },
          { key: 'test', label: `Test Methods (${test_methods.length})` },
          { key: 'safety', label: `Safety (${safety_standards.length})` },
          { key: 'installation', label: `Installation (${installation_standards.length})` }
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-3 py-1.5 rounded transition ${
              activeTab === tab.key
                ? 'bg-slate-900 text-amber-400 font-bold'
                : 'text-slate-600 hover:bg-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Primary Standards Section */}
      {(activeTab === 'all' || activeTab === 'primary') && primary_standards.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 uppercase tracking-wider">
            <span className="w-3 h-3 bg-blue-900 rounded-full"></span>
            <span>Primary & Applicable Product Standards</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {primary_standards.map((card) => (
              <StandardCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      )}

      {/* Supporting Standards Section */}
      {(activeTab === 'all' || activeTab === 'supporting') && supporting_standards.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 uppercase tracking-wider">
            <span className="w-3 h-3 bg-indigo-700 rounded-full"></span>
            <span>Supporting & Allied Technical Standards</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {supporting_standards.map((card) => (
              <StandardCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      )}

      {/* Normative References Section */}
      {(activeTab === 'all' || activeTab === 'normative') && normative_references.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 uppercase tracking-wider">
            <span className="w-3 h-3 bg-amber-700 rounded-full"></span>
            <span>Normative Reference Standards</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {normative_references.map((card) => (
              <StandardCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      )}

      {/* Test Methods Section */}
      {(activeTab === 'all' || activeTab === 'test') && test_methods.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 uppercase tracking-wider">
            <span className="w-3 h-3 bg-emerald-800 rounded-full"></span>
            <span>Acceptance Test & Performance Standards</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {test_methods.map((card) => (
              <StandardCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      )}

      {/* Safety Standards Section */}
      {(activeTab === 'all' || activeTab === 'safety') && safety_standards.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 uppercase tracking-wider">
            <span className="w-3 h-3 bg-rose-800 rounded-full"></span>
            <span>Electrical & Environmental Safety Standards</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {safety_standards.map((card) => (
              <StandardCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      )}

      {/* Installation Standards Section */}
      {(activeTab === 'all' || activeTab === 'installation') && installation_standards.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center space-x-2 text-sm font-bold text-slate-900 uppercase tracking-wider">
            <span className="w-3 h-3 bg-cyan-800 rounded-full"></span>
            <span>Code of Practice for Installation & Maintenance</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {installation_standards.map((card) => (
              <StandardCard key={card.id} card={card} />
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
