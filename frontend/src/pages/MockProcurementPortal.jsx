import React, { useState } from 'react';
import { Building2, ShieldCheck, Award, ArrowRight, Loader2, FileText, CheckCircle2, AlertTriangle, ExternalLink } from 'lucide-react';
import { analyzeTender } from '../services/api';
import StandardCard from '../components/StandardCard';

export default function MockProcurementPortal() {
  const [tenderId] = useState('GEM/2026/B/9928104');
  const [productTitle, setProductTitle] = useState('Procurement of Horizontal Centrifugal Pump Sets for Municipal Water Works');
  const [productDesc, setProductDesc] = useState('Supply, delivery, installation, testing and commissioning of horizontal split casing centrifugal pump sets with 3-phase electric motor drive for city water treatment plant.');
  const [flowRate, setFlowRate] = useState('120 m3/hr');
  const [head, setHead] = useState('60 m');
  const [power, setPower] = useState('90 kW');
  const [motorSpec, setMotorSpec] = useState('3-Phase Squirrel Cage Induction Motor per IS 325');

  const [portalAnalysisResult, setPortalAnalysisResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  const handleRunPortalAnalysis = async () => {
    setAnalyzing(true);
    try {
      const payload = {
        request_id: tenderId,
        product_title: productTitle,
        product_description: `${productDesc} Note: Specification mentions ${motorSpec}`,
        technical_specification: {
          flow_rate: flowRate,
          head: head,
          power: power,
          motor_reference: motorSpec
        },
        language: 'en'
      };

      const res = await analyzeTender(payload);
      setPortalAnalysisResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* GeM Portal Banner Header */}
      <div className="bg-slate-900 text-white p-5 rounded-lg border-b-4 border-amber-600 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-amber-400 font-bold mb-1">
            <Building2 className="w-4 h-4" />
            <span>Mock Government e-Marketplace (GeM) & CPPP Integration Portal</span>
          </div>
          <h1 className="text-xl font-bold font-serif">
            Central Public Procurement Portal - Tender Draft # {tenderId}
          </h1>
          <p className="text-xs text-slate-300 mt-0.5">
            Simulated procurement portal interface demonstrating embedded API integration for automated Indian Standards intelligence decision-support.
          </p>
        </div>

        <span className="bg-emerald-950 border border-emerald-700 text-emerald-300 font-mono text-xs px-3 py-1 rounded">
          INTEGRATION API ACTIVE
        </span>
      </div>

      {/* Tender Specification Form Layout */}
      <div className="bg-white border border-slate-300 rounded-lg p-6 space-y-6 shadow-xs">
        <div className="border-b border-slate-200 pb-3 flex justify-between items-center">
          <h2 className="text-base font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-700" />
            Procurement Item Specifications (Drafting Stage)
          </h2>
          <span className="text-xs font-mono text-slate-500">Draft ID: {tenderId}</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="space-y-1">
            <label className="font-bold text-slate-800 uppercase">Product / Tender Item Name</label>
            <input
              type="text"
              value={productTitle}
              onChange={(e) => setProductTitle(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs font-medium"
            />
          </div>

          <div className="space-y-1">
            <label className="font-bold text-slate-800 uppercase">Coupled Motor Reference</label>
            <input
              type="text"
              value={motorSpec}
              onChange={(e) => setMotorSpec(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs font-mono"
            />
          </div>

          <div className="md:col-span-2 space-y-1">
            <label className="font-bold text-slate-800 uppercase">Procurement Scope Description</label>
            <textarea
              rows={2}
              value={productDesc}
              onChange={(e) => setProductDesc(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs"
            />
          </div>

          {/* Technical Specs Inputs */}
          <div className="space-y-1">
            <label className="font-bold text-slate-800 uppercase">Design Flow Rate</label>
            <input
              type="text"
              value={flowRate}
              onChange={(e) => setFlowRate(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-1.5 text-xs font-mono"
            />
          </div>

          <div className="space-y-1">
            <label className="font-bold text-slate-800 uppercase">Design Head</label>
            <input
              type="text"
              value={head}
              onChange={(e) => setHead(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-1.5 text-xs font-mono"
            />
          </div>
        </div>

        {/* Embedded Call to Action Button */}
        <div className="bg-slate-100 p-4 rounded-lg border border-slate-300 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="text-xs text-slate-700">
            <div className="font-bold text-slate-900">MANAK ANVESHAN Decision-Support Service</div>
            Clicking will invoke <code className="bg-slate-200 px-1 py-0.5 rounded text-[11px] font-mono">POST /api/v1/standards/analyze</code> to audit specifications against Indian Standards.
          </div>

          <button
            onClick={handleRunPortalAnalysis}
            disabled={analyzing}
            className="bg-amber-600 hover:bg-amber-700 text-slate-950 font-bold px-6 py-2.5 rounded text-xs flex items-center space-x-2 transition shrink-0 cursor-pointer shadow-sm"
          >
            {analyzing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
                <span>Auditing BIS Standards...</span>
              </>
            ) : (
              <>
                <ShieldCheck className="w-4 h-4 text-slate-950" />
                <span>Analyze Indian Standards</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Embedded Decision Support Results Display */}
      {portalAnalysisResult && (
        <div className="bg-white border-2 border-slate-900 rounded-lg p-6 space-y-6 shadow-md">
          
          <div className="border-b-2 border-amber-600 pb-3 flex justify-between items-center">
            <div>
              <div className="flex items-center space-x-2 text-xs font-bold text-emerald-700 uppercase">
                <CheckCircle2 className="w-4 h-4" />
                <span>MANAK ANVESHAN Intelligence Decision Support Report Attached</span>
              </div>
              <h3 className="text-lg font-bold text-slate-900 font-serif mt-1">
                Authoritative Indian Standards Compliance Assessment
              </h3>
            </div>
            <span className="bg-slate-900 text-amber-400 font-mono text-xs px-3 py-1 rounded font-bold">
              {portalAnalysisResult.summary_counts.total_analyzed} Standards Evaluated
            </span>
          </div>

          {/* Superseded Alerts Banner */}
          {portalAnalysisResult.version_alerts && portalAnalysisResult.version_alerts.length > 0 && (
            <div className="space-y-2">
              {portalAnalysisResult.version_alerts.map((va, idx) => (
                <div key={idx} className="bg-rose-50 border-l-4 border-rose-600 p-3.5 rounded-r text-xs text-rose-950 space-y-1">
                  <div className="font-bold text-rose-900 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-rose-600" />
                    {va.title}
                  </div>
                  <div>{va.message}</div>
                  <div className="font-mono font-bold text-rose-900 bg-rose-100 p-1.5 rounded mt-1">
                    Required Fix: {va.action_required}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Mandatory QCO Compliance Summary */}
          {portalAnalysisResult.certification_summary && (
            <div className="bg-amber-50 border border-amber-300 rounded p-4 text-xs space-y-2">
              <div className="font-bold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
                <Award className="w-4 h-4 text-amber-600" />
                Mandatory Gazette Quality Control Orders (QCO)
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 font-mono">
                {portalAnalysisResult.certification_summary.map((cs, i) => (
                  <div key={i} className="bg-white p-2.5 rounded border border-amber-200">
                    <div className="font-bold text-slate-900">{cs.is_number} — {cs.scheme}</div>
                    <div className="text-slate-600 text-[11px] font-sans mt-0.5">{cs.conditions}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Primary Recommended Standards Grid */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800 mb-3">
              Primary Governing Indian Standards:
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {portalAnalysisResult.primary_standards.map((card) => (
                <StandardCard key={card.id} card={card} />
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
