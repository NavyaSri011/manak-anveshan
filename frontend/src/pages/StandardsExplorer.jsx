import React, { useEffect, useState } from 'react';
import { Search, Filter, BookOpen, AlertTriangle, CheckCircle, ShieldCheck, Award, X } from 'lucide-react';
import { listStandards, getStandardDetail, validateStandard } from '../services/api';

export default function StandardsExplorer() {
  const [standards, setStandards] = useState([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(true);

  // Validate IS Number Tool
  const [validateQuery, setValidateQuery] = useState('');
  const [validationResult, setValidationResult] = useState(null);
  const [validating, setValidating] = useState(false);

  // Selected Detail Modal
  const [selectedStandardDetail, setSelectedStandardDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  useEffect(() => {
    fetchStandards();
  }, [category]);

  const fetchStandards = async (searchTerm = search) => {
    setLoading(true);
    try {
      const res = await listStandards({ search: searchTerm, category });
      setStandards(res || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchStandards(search);
  };

  const handleValidateSubmit = async (e) => {
    e.preventDefault();
    if (!validateQuery.trim()) return;
    setValidating(true);
    try {
      const res = await validateStandard(validateQuery);
      setValidationResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setValidating(false);
    }
  };

  const handleOpenDetail = async (stdId) => {
    setLoadingDetail(true);
    try {
      const res = await getStandardDetail(stdId);
      setSelectedStandardDetail(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingDetail(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Page Title */}
      <div className="border-b border-slate-300 pb-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-serif flex items-center gap-2">
            <Search className="w-6 h-6 text-amber-600" />
            Indian Standards Explorer
          </h1>
          <p className="text-xs text-slate-600 mt-1">
            Search Bureau of Indian Standards catalog by IS number, ICS codes, title, scope keywords, and QCO mandates.
          </p>
        </div>

        {/* Quick Validate Standard Tool */}
        <form onSubmit={handleValidateSubmit} className="bg-slate-900 p-2 rounded-md flex items-center space-x-2 text-xs text-white">
          <span className="font-bold text-amber-400 text-[11px] whitespace-nowrap pl-1">IS Lookup:</span>
          <input
            type="text"
            placeholder="e.g. IS 325"
            value={validateQuery}
            onChange={(e) => setValidateQuery(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded px-2.5 py-1 text-xs text-slate-100 font-mono focus:outline-hidden focus:border-amber-500 w-28"
          />
          <button
            type="submit"
            disabled={validating}
            className="bg-amber-600 text-slate-950 font-bold px-2.5 py-1 rounded hover:bg-amber-500 transition text-[11px]"
          >
            {validating ? 'Checking...' : 'Check Status'}
          </button>
        </form>
      </div>

      {/* Validation Result Alert */}
      {validationResult && (
        <div className={`p-4 rounded border text-xs flex justify-between items-start gap-4 ${
          validationResult.status === 'SUPERSEDED'
            ? 'bg-rose-50 border-rose-300 text-rose-950'
            : validationResult.valid
            ? 'bg-emerald-50 border-emerald-300 text-emerald-950'
            : 'bg-amber-50 border-amber-300 text-amber-950'
        }`}>
          <div>
            <div className="font-bold text-sm flex items-center gap-2 font-mono">
              {validationResult.status === 'SUPERSEDED' ? (
                <AlertTriangle className="w-4 h-4 text-rose-600" />
              ) : (
                <CheckCircle className="w-4 h-4 text-emerald-600" />
              )}
              {validationResult.is_number} — Status: {validationResult.status}
            </div>
            {validationResult.warning_message && (
              <div className="mt-1 font-medium">{validationResult.warning_message}</div>
            )}
            {validationResult.standard && (
              <div className="mt-1 text-slate-600">
                Title: {validationResult.standard.title} (Category: {validationResult.standard.category})
              </div>
            )}
          </div>
          <button onClick={() => setValidationResult(null)} className="text-slate-400 hover:text-slate-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Search & Filter Bar */}
      <form onSubmit={handleSearchSubmit} className="bg-white border border-slate-300 rounded-lg p-4 flex flex-col md:flex-row gap-3 shadow-xs">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="Search IS number, scope keyword, or title (e.g. Centrifugal Pump, IS 1520, Motor)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-50 border border-slate-300 rounded pl-9 pr-3 py-2 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600"
          />
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
        </div>

        <div className="w-full md:w-64">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full bg-slate-50 border border-slate-300 rounded px-3 py-2 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600 font-medium"
          >
            <option value="">All Categories</option>
            <option value="Pumps & Fluid Handling">Pumps & Fluid Handling</option>
            <option value="Electrical Motors & Drives">Electrical Motors & Drives</option>
            <option value="Electrical Power Systems">Electrical Power Systems</option>
            <option value="Electrical Safety & Wiring">Electrical Safety & Wiring</option>
            <option value="Solar Energy Systems">Solar Energy Systems</option>
            <option value="Pipes, Valves & Fittings">Pipes, Valves & Fittings</option>
            <option value="Water & Environment">Water & Environment</option>
          </select>
        </div>

        <button
          type="submit"
          className="bg-slate-900 hover:bg-slate-800 text-amber-400 font-bold px-5 py-2 rounded text-xs transition"
        >
          Filter Catalog
        </button>
      </form>

      {/* Standards List Table / Grid */}
      {loading ? (
        <div className="py-12 text-center text-slate-500 text-xs">Loading Standards Catalog...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {standards.map((std) => (
            <div key={std.id} className="bg-white border border-slate-300 rounded-lg p-5 flex flex-col justify-between space-y-3 shadow-xs hover:border-slate-400 transition">
              <div>
                <div className="flex justify-between items-start gap-2 mb-2">
                  <span className="font-mono text-sm font-bold bg-slate-900 text-amber-400 px-2.5 py-0.5 rounded border border-slate-800">
                    {std.is_number}
                  </span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                    std.status === 'ACTIVE' ? 'bg-emerald-100 text-emerald-800 border-emerald-300' : 'bg-rose-100 text-rose-800 border-rose-300'
                  }`}>
                    {std.status}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-slate-900 line-clamp-2 leading-snug">
                  {std.title}
                </h3>

                <p className="text-xs text-slate-600 mt-2 line-clamp-3 leading-relaxed">
                  {std.scope}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-200 flex justify-between items-center text-xs">
                <span className="text-[11px] text-slate-500 font-mono">ICS: {std.ics_codes || 'N/A'}</span>
                <button
                  onClick={() => handleOpenDetail(std.id)}
                  className="bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold px-3 py-1 rounded text-xs transition"
                >
                  View Relationships
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Standard Detail Popover Modal */}
      {selectedStandardDetail && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white border border-slate-300 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-4 shadow-xl">
            <div className="flex justify-between items-start border-b border-slate-200 pb-3">
              <div>
                <span className="font-mono text-sm font-bold bg-slate-900 text-amber-400 px-2 py-0.5 rounded">
                  {selectedStandardDetail.standard.is_number}
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-1 font-serif">
                  {selectedStandardDetail.standard.title}
                </h3>
              </div>
              <button onClick={() => setSelectedStandardDetail(null)} className="text-slate-400 hover:text-slate-700">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="text-xs text-slate-700 space-y-2">
              <div><span className="font-bold text-slate-900">Category:</span> {selectedStandardDetail.standard.category}</div>
              <div><span className="font-bold text-slate-900">ICS Code:</span> {selectedStandardDetail.standard.ics_codes}</div>
              <div><span className="font-bold text-slate-900">Status:</span> {selectedStandardDetail.standard.status}</div>
              <div><span className="font-bold text-slate-900">Scope:</span> {selectedStandardDetail.standard.scope}</div>
            </div>

            {/* Amendments */}
            {selectedStandardDetail.standard.amendments?.length > 0 && (
              <div className="border-t border-slate-200 pt-3">
                <div className="font-bold text-xs uppercase text-slate-800 mb-2">Gazette Amendments ({selectedStandardDetail.standard.amendments.length})</div>
                <div className="space-y-2">
                  {selectedStandardDetail.standard.amendments.map((am) => (
                    <div key={am.id} className="bg-slate-50 border border-slate-200 p-2.5 rounded text-xs">
                      <div className="font-bold text-slate-900">Amendment #{am.amendment_number} ({am.date || 'N/A'})</div>
                      <div className="text-slate-600 mt-0.5">{am.description}</div>
                      <div className="text-[10px] text-slate-400 mt-1">Source: {am.source}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Relationships */}
            {selectedStandardDetail.relationships?.length > 0 && (
              <div className="border-t border-slate-200 pt-3">
                <div className="font-bold text-xs uppercase text-slate-800 mb-2">Target Standard Relationships</div>
                <div className="space-y-2">
                  {selectedStandardDetail.relationships.map((rel) => (
                    <div key={rel.id} className="bg-indigo-50/50 border border-indigo-200 p-2.5 rounded text-xs space-y-1">
                      <div className="flex justify-between items-center font-bold">
                        <span className="font-mono text-indigo-950">{rel.target_is_number}</span>
                        <span className="bg-indigo-200 text-indigo-900 px-1.5 py-0.5 rounded text-[10px] font-mono">{rel.relationship_type}</span>
                      </div>
                      <div className="text-indigo-900 font-medium">{rel.target_title}</div>
                      <div className="text-[11px] text-slate-600 italic">{rel.evidence}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="border-t border-slate-200 pt-3 flex justify-end">
              <button
                onClick={() => setSelectedStandardDetail(null)}
                className="bg-slate-900 text-white font-bold px-4 py-1.5 rounded text-xs"
              >
                Close Window
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
