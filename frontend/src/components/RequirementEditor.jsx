import React, { useState } from 'react';
import { Plus, Trash2, Edit3, Check, RefreshCw } from 'lucide-react';

export default function RequirementEditor({ extracted, onRequirementsUpdated }) {
  const [params, setParams] = useState(extracted.technical_parameters || {});
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');

  const handleValueChange = (key, val) => {
    const updated = { ...params, [key]: val };
    setParams(updated);
    onRequirementsUpdated(updated);
  };

  const handleRemoveKey = (key) => {
    const updated = { ...params };
    delete updated[key];
    setParams(updated);
    onRequirementsUpdated(updated);
  };

  const handleAddParam = (e) => {
    e.preventDefault();
    if (!newKey.trim() || !newValue.trim()) return;
    const updated = { ...params, [newKey.trim()]: newValue.trim() };
    setParams(updated);
    setNewKey('');
    setNewValue('');
    onRequirementsUpdated(updated);
  };

  return (
    <div className="bg-white border border-slate-300 rounded-lg p-5 space-y-4">
      <div className="flex justify-between items-center border-b border-slate-200 pb-3">
        <div>
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Edit3 className="w-4 h-4 text-amber-600" />
            Extracted Technical Specifications & Parameters
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Review and modify extracted attributes before running Indian Standards matching.
          </p>
        </div>
        <span className="text-xs bg-slate-100 text-slate-700 font-mono px-2 py-1 rounded border border-slate-200">
          {Object.keys(params).length} Parameters Detected
        </span>
      </div>

      {/* Editable Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-100 border-y border-slate-300 text-slate-700 font-bold uppercase tracking-wider text-[11px]">
              <th className="py-2.5 px-3">Attribute Name</th>
              <th className="py-2.5 px-3">Specification Value</th>
              <th className="py-2.5 px-3 w-16 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {Object.keys(params).length === 0 ? (
              <tr>
                <td colSpan={3} className="py-4 text-center text-slate-400 italic">
                  No technical parameters extracted yet. Add parameters below.
                </td>
              </tr>
            ) : (
              Object.entries(params).map(([k, v]) => (
                <tr key={k} className="hover:bg-slate-50/80">
                  <td className="py-2 px-3 font-semibold text-slate-800 font-mono">
                    {k}
                  </td>
                  <td className="py-2 px-3">
                    <input
                      type="text"
                      value={v}
                      onChange={(e) => handleValueChange(k, e.target.value)}
                      className="w-full bg-white border border-slate-300 rounded px-2.5 py-1 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600 font-mono"
                    />
                  </td>
                  <td className="py-2 px-3 text-center">
                    <button
                      type="button"
                      onClick={() => handleRemoveKey(k)}
                      className="text-slate-400 hover:text-rose-600 p-1 rounded hover:bg-rose-50 transition"
                      title="Remove Parameter"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Add New Parameter Form */}
      <form onSubmit={handleAddParam} className="flex gap-2 pt-2 border-t border-slate-200">
        <input
          type="text"
          placeholder="New Parameter Name (e.g. pressure)"
          value={newKey}
          onChange={(e) => setNewKey(e.target.value)}
          className="flex-1 bg-slate-50 border border-slate-300 rounded px-3 py-1.5 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600"
        />
        <input
          type="text"
          placeholder="Value (e.g. 16 bar)"
          value={newValue}
          onChange={(e) => setNewValue(e.target.value)}
          className="flex-1 bg-slate-50 border border-slate-300 rounded px-3 py-1.5 text-xs text-slate-900 focus:outline-hidden focus:border-amber-600"
        />
        <button
          type="submit"
          className="bg-slate-800 text-slate-100 hover:bg-slate-900 font-bold px-3 py-1.5 rounded text-xs flex items-center space-x-1 shrink-0"
        >
          <Plus className="w-4 h-4" />
          <span>Add</span>
        </button>
      </form>
    </div>
  );
}
