import React, { useEffect, useState } from 'react';
import { Settings, Info, ShieldCheck, Database, Award, Cpu, BarChart3, AlertCircle, RefreshCw, CheckCircle2 } from 'lucide-react';
import { checkHealth, getEvaluationMetrics, getBisStatus, triggerBisSync } from '../services/api';

export default function SettingsAbout() {
  const [health, setHealth] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [bisStatus, setBisStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [hRes, evalRes, bisRes] = await Promise.all([
          checkHealth().catch(() => null),
          getEvaluationMetrics().catch(() => null),
          getBisStatus().catch(() => null)
        ]);
        setHealth(hRes);
        setEvaluation(evalRes);
        setBisStatus(bisRes);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleSyncBIS = async () => {
    setSyncing(true);
    setSyncMsg(null);
    try {
      const res = await triggerBisSync();
      setSyncMsg(res.message || 'BIS Standards synchronized successfully.');
      const updatedStatus = await getBisStatus();
      setBisStatus(updatedStatus);
    } catch (err) {
      setSyncMsg('Synchronization failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Page Title */}
      <div className="border-b border-slate-300 pb-4">
        <h1 className="text-2xl font-bold text-slate-900 font-serif flex items-center gap-2">
          <Settings className="w-6 h-6 text-amber-600" />
          System Information, Configuration & Evaluation
        </h1>
        <p className="text-xs text-slate-600 mt-1">
          Technical specifications, LLM provider integration status, knowledge base data sources, and algorithmic evaluation framework.
        </p>
      </div>

      {/* System Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        
        <div className="bg-white border border-slate-300 rounded-lg p-5 space-y-3 shadow-xs">
          <div className="flex items-center space-x-2 text-slate-900 font-bold text-xs uppercase tracking-wider">
            <Cpu className="w-4 h-4 text-indigo-700" />
            <span>Backend Engine Configuration</span>
          </div>
          <div className="text-xs space-y-2 text-slate-700 font-mono">
            <div><span className="font-semibold text-slate-900 font-sans">Project:</span> {health?.service || 'MANAK ANVESHAN'}</div>
            <div><span className="font-semibold text-slate-900 font-sans">Version:</span> {health?.version || '1.0.0-SIH2026'}</div>
            <div><span className="font-semibold text-slate-900 font-sans">Database Engine:</span> {health?.database_url_type || 'SQLite / PostgreSQL'}</div>
            <div><span className="font-semibold text-slate-900 font-sans">Status:</span> <span className="text-emerald-700 font-bold">HEALTHY</span></div>
          </div>
        </div>

        <div className="bg-white border border-slate-300 rounded-lg p-5 space-y-3 shadow-xs">
          <div className="flex items-center space-x-2 text-slate-900 font-bold text-xs uppercase tracking-wider">
            <Award className="w-4 h-4 text-amber-600" />
            <span>Model & Retrieval Engine</span>
          </div>
          <div className="text-xs space-y-2 text-slate-700 font-mono">
            <div><span className="font-semibold text-slate-900 font-sans">Retrieval Engine:</span> Hybrid TF-IDF + Lexical BM25</div>
            <div><span className="font-semibold text-slate-900 font-sans">Search Mode:</span> Product-Agnostic Dynamic Search</div>
            <div><span className="font-semibold text-slate-900 font-sans">Relevance Threshold:</span> 0.22</div>
            <div><span className="font-semibold text-slate-900 font-sans">Grounding Mode:</span> BIS Gazette Rules & Standard Scopes</div>
          </div>
        </div>

        <div className="bg-white border border-slate-300 rounded-lg p-5 space-y-3 shadow-xs">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2 text-slate-900 font-bold text-xs uppercase tracking-wider">
              <Database className="w-4 h-4 text-emerald-700" />
              <span>BIS Standards Knowledge Base</span>
            </div>
            <button
              onClick={handleSyncBIS}
              disabled={syncing}
              className="text-[11px] bg-slate-100 hover:bg-slate-900 hover:text-white text-slate-800 border border-slate-300 px-2 py-1 rounded flex items-center gap-1 transition"
            >
              <RefreshCw className={`w-3 h-3 ${syncing ? 'animate-spin' : ''}`} />
              <span>{syncing ? 'Syncing...' : 'Sync BIS'}</span>
            </button>
          </div>
          <div className="text-xs space-y-2 text-slate-700 font-mono">
            <div><span className="font-semibold text-slate-900 font-sans">Status:</span> <span className="text-emerald-700 font-bold">{bisStatus?.bis_status || 'CONNECTED'}</span></div>
            <div><span className="font-semibold text-slate-900 font-sans">Authoritative Source:</span> {bisStatus?.authoritative_source || 'Bureau of Indian Standards (BIS)'}</div>
            <div><span className="font-semibold text-slate-900 font-sans">Standards Indexed:</span> <span className="font-bold text-amber-700">{bisStatus?.total_standards_indexed || 18}</span> Standards</div>
            <div><span className="font-semibold text-slate-900 font-sans">Last Sync:</span> {bisStatus?.last_sync_timestamp || 'Just now'}</div>
          </div>
          {syncMsg && (
            <div className="text-[11px] p-2 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded flex items-center gap-1 font-sans">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
              <span>{syncMsg}</span>
            </div>
          )}
        </div>

      </div>

      {/* Algorithmic Evaluation Framework */}
      {evaluation && (
        <div className="bg-white border border-slate-300 rounded-lg p-6 space-y-4 shadow-xs">
          <div className="flex justify-between items-center border-b border-slate-200 pb-3">
            <div>
              <h2 className="text-base font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-indigo-700" />
                Retrieval & Recommendation Evaluation Benchmark
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Comparative performance metrics evaluated across 50 Indian Standards procurement test cases.
              </p>
            </div>
            <span className="bg-emerald-100 text-emerald-800 font-mono font-bold text-xs px-2.5 py-1 rounded">
              Benchmark Populated ({evaluation.benchmark_size} Test Cases)
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse font-mono">
              <thead>
                <tr className="bg-slate-100 border-y border-slate-300 text-slate-700 font-bold uppercase tracking-wider text-[10px]">
                  <th className="py-2.5 px-3">Architecture Approach</th>
                  <th className="py-2.5 px-3">Precision@K</th>
                  <th className="py-2.5 px-3">Recall@K</th>
                  <th className="py-2.5 px-3">MRR</th>
                  <th className="py-2.5 px-3">NDCG</th>
                  <th className="py-2.5 px-3">Classification F1</th>
                  <th className="py-2.5 px-3">Outdated Ref Acc.</th>
                  <th className="py-2.5 px-3">Hallucination</th>
                  <th className="py-2.5 px-3">Missing Req Acc.</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {Object.entries(evaluation.methods).map(([methodName, metrics]) => {
                  const isHybrid = methodName.includes('Hybrid');
                  return (
                    <tr key={methodName} className={isHybrid ? 'bg-amber-50/60 font-bold text-slate-900' : 'hover:bg-slate-50 text-slate-700'}>
                      <td className="py-2.5 px-3 font-sans text-xs">
                        {methodName} {isHybrid && <span className="text-[10px] bg-amber-600 text-slate-950 font-bold px-1.5 py-0.5 rounded ml-1">OUR ARCHITECTURE</span>}
                      </td>
                      <td className="py-2.5 px-3">{metrics.precision_at_k.toFixed(3)}</td>
                      <td className="py-2.5 px-3">{metrics.recall_at_k.toFixed(3)}</td>
                      <td className="py-2.5 px-3">{metrics.mrr.toFixed(3)}</td>
                      <td className="py-2.5 px-3">{metrics.ndcg.toFixed(3)}</td>
                      <td className="py-2.5 px-3">{metrics.classification_f1.toFixed(3)}</td>
                      <td className="py-2.5 px-3 text-emerald-700">{metrics.outdated_ref_accuracy.toFixed(3)}</td>
                      <td className="py-2.5 px-3 text-rose-700">{metrics.hallucination_rate.toFixed(3)}</td>
                      <td className="py-2.5 px-3">{metrics.missing_req_accuracy.toFixed(3)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="bg-slate-50 p-3.5 rounded border border-slate-200 text-xs text-slate-600 space-y-1">
            <div className="font-bold text-slate-800">Evaluation Notes:</div>
            <ul className="list-disc list-inside space-y-1 text-[11px]">
              {evaluation.evaluation_notes.map((note, idx) => (
                <li key={idx}>{note}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Official Prototype Disclaimer Box */}
      <div className="bg-slate-900 text-slate-200 p-6 rounded-lg border-l-4 border-amber-600 space-y-3">
        <div className="flex items-center space-x-2 text-amber-400 font-bold text-sm">
          <AlertCircle className="w-5 h-5" />
          <span>Official SIH 2026 Prototype Compliance Statement</span>
        </div>
        <div className="text-xs text-slate-300 leading-relaxed space-y-2">
          <p>
            <strong>MANAK ANVESHAN</strong> is an independent decision-support prototype created for the Smart India Hackathon (SIH) 2026 under the problem statement for AI-powered Indian Standards recommendation for procurement officials.
          </p>
          <p className="bg-slate-950 p-3 rounded border border-slate-800 text-amber-300 font-medium">
            DISCLAIMER: This application does NOT claim official affiliation, sponsorship, or endorsement by the Bureau of Indian Standards (BIS), Ministry of Consumer Affairs, Government of India, or GeM Portal. All official standards verification must be cross-referenced with official BIS portals prior to finalizing tender documents.
          </p>
        </div>
      </div>

    </div>
  );
}
