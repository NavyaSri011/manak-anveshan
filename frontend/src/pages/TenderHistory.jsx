import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { History, FileText, ArrowRight, Database, Search } from 'lucide-react';
import { listAnalyses } from '../services/api';

export default function TenderHistory() {
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listAnalyses()
      .then((res) => setTenders(res || []))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Page Title */}
      <div className="border-b border-slate-300 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-serif flex items-center gap-2">
            <History className="w-6 h-6 text-amber-600" />
            Tender Analysis History
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Review past procurement tender specification analyses, standard recommendations, and audit logs.
          </p>
        </div>

        <Link to="/new-analysis" className="bg-amber-600 hover:bg-amber-700 text-slate-950 font-bold px-4 py-2 rounded text-xs">
          + New Analysis
        </Link>
      </div>

      {/* History Table */}
      <div className="bg-white border border-slate-300 rounded-lg p-5 shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-100 border-y border-slate-200 text-slate-700 font-bold uppercase tracking-wider text-[11px]">
                <th className="py-3 px-4">Tender ID</th>
                <th className="py-3 px-4">Product Title</th>
                <th className="py-3 px-4">Analysis Date</th>
                <th className="py-3 px-4">Language</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500">
                    Loading history logs from server...
                  </td>
                </tr>
              ) : tenders.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-slate-500 italic">
                    No past analyses found. Start your first analysis from the New Analysis page.
                  </td>
                </tr>
              ) : (
                tenders.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50">
                    <td className="py-3 px-4 font-mono font-bold text-slate-900">
                      {t.request_id}
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-900">
                      {t.product_title}
                    </td>
                    <td className="py-3 px-4 text-slate-600 font-mono text-[11px]">
                      {t.created_at}
                    </td>
                    <td className="py-3 px-4 uppercase text-slate-700 font-mono text-[10px]">
                      {t.language}
                    </td>
                    <td className="py-3 px-4">
                      <span className="bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded text-[10px]">
                        COMPLETED
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <Link
                        to={`/results?id=${t.id}`}
                        className="bg-slate-900 hover:bg-slate-800 text-amber-400 font-bold px-3 py-1.5 rounded text-xs inline-flex items-center space-x-1"
                      >
                        <span>View Results</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
