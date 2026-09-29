import React, { useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import {
  Download,
  Printer,
  Copy,
  Check,
  FileCheck,
  ShieldCheck,
  Award,
  AlertTriangle,
  FileText
} from 'lucide-react';

export default function Reports() {
  const location = useLocation();

  // Support both the older reportData payload and the newer resultData payload.
  const passedData =
    location.state?.reportData ||
    location.state?.resultData;

  const [copied, setCopied] = useState(false);

  // Mock report state if accessed directly
  const data = passedData || {
    analysis_id: "REP-2026-001",
    request_id: "TENDER-2026-GeM-9921",
    product_title: "Horizontal Centrifugal Pump Sets for Municipal Water Supply",
    language: "en",
    created_at: "2026-09-27 21:00:00",

    canonical_requirements: {
      product: {
        name: "Centrifugal Pump",
        category: "Pumps & Fluid Handling"
      },
      application: "Industrial & Municipal Water Supply",
      technical_parameters: {
        flow_rate: "100 m3/hr",
        head: "50 m",
        power: "75 kW"
      }
    },

    primary_standards: [
      {
        id: "std-1520",
        is_number: "IS 1520:1980",
        title: "Horizontal Centrifugal Pumps for Clear, Cold, Fresh Water",
        scope:
          "Specifies technical requirements, hydraulic performance limits, materials, and testing protocols for horizontal centrifugal pumps.",
        status: "ACTIVE",
        category: "Pumps & Fluid Handling",
        classification: "PRIMARY",
        confidence_score: 0.95,
        reason: [
          "Direct matching product category",
          "Defines performance tolerances and hydraulic design requirements"
        ],
        certification_info: {
          status: "Applicable",
          scheme: "BIS Product Certification (ISI Mark)",
          conditions:
            "Mandatory ISI marking required under QCO."
        }
      }
    ],

    supporting_standards: [
      {
        id: "std-12615",
        is_number: "IS 12615:2018",
        title:
          "Energy Efficient Three Phase Squirrel Cage Induction Motors (IE3)",
        scope:
          "Specifies energy efficiency classes (IE2, IE3, IE4) for 3-phase induction motors.",
        status: "ACTIVE",
        category: "Electrical Motors & Drives",
        classification: "NORMATIVE_REFERENCE",
        confidence_score: 0.90,
        reason: [
          "Coupled electric drive motor must satisfy minimum IE3 efficiency class"
        ],
        certification_info: {
          status: "Applicable",
          scheme: "Mandatory QCO + BIS Certification",
          conditions:
            "Mandatory IE3 class under Ministry Order."
        }
      }
    ],

    version_alerts: [
      {
        title: "Outdated Tender Reference Detected: IS 325:1996",
        message:
          "This tender refers to IS 325:1996 which is SUPERSEDED by IS 12615:2018.",
        action_required:
          "Replace IS 325:1996 with IS 12615:2018 in tender specification."
      }
    ],

    certification_summary: [
      {
        is_number: "IS 1520:1980",
        scheme: "BIS Product Certification (ISI Mark)",
        status: "Applicable",
        conditions:
          "Mandatory ISI marking required for public procurement under QCO.",
        source: "Gazette Order S.O. 2481(E)"
      }
    ],

    missing_requirements: [
      {
        attribute: "Operating Temperature",
        importance: "HIGH",
        impact:
          "Impeller cavitation and seal material selection under IS 1520.",
        message:
          "Fluid temperature missing. High temperatures require Viton seals."
      }
    ]
  };

  /*
   * Creates a safe filename from the actual product title.
   *
   * Example:
   * "Line Operated Three Phase AC Motor — IE3"
   * becomes:
   * "Line Operated Three Phase AC Motor — IE3"
   */
  const getPdfFilename = (title) => {
    return String(
      title || "Procurement Technical Compliance Report"
    )
      .replace(/[<>:"/\\|?*\x00-\x1F]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 180);
  };

  /*
   * Print / Export PDF
   *
   * The browser uses document.title when generating the
   * default PDF filename in many print-to-PDF flows.
   */
  const handlePrint = () => {
    const originalTitle = document.title;

    const productTitle =
      data?.product_title ||
      data?.canonical_requirements?.product?.name ||
      "Procurement Technical Compliance Report";

    const pdfTitle = getPdfFilename(productTitle);

    // Temporarily change the browser document title.
    document.title = pdfTitle;

    // Give the browser a moment to register the new title
    // before opening the print dialog.
    setTimeout(() => {
      window.print();

      // Restore the original browser title after printing.
      setTimeout(() => {
        document.title = originalTitle;
      }, 1000);
    }, 100);
  };

  const handleExportJSON = () => {
    const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(
      JSON.stringify(data, null, 2)
    )}`;

    const downloadAnchor = document.createElement('a');

    downloadAnchor.setAttribute('href', jsonString);

    downloadAnchor.setAttribute(
      'download',
      `Procurement_Report_${data.request_id}.json`
    );

    document.body.appendChild(downloadAnchor);

    downloadAnchor.click();

    downloadAnchor.remove();
  };

  const handleCopySummary = () => {
    const text = `MANAK ANVESHAN PROCUREMENT COMPLIANCE REPORT
Tender ID: ${data.request_id}
Product: ${data.product_title}
Date: ${data.created_at}

RECOMMENDED PRIMARY STANDARDS:
${(data.primary_standards || [])
  .map(
    (p) =>
      `- ${p.is_number}: ${p.title} (Status: ${p.status})`
  )
  .join('\n')}

QCO MANDATES:
${(data.certification_summary || [])
  .map(
    (c) =>
      `- ${c.is_number}: ${c.scheme} (${c.conditions})`
  )
  .join('\n')}`;

    navigator.clipboard.writeText(text);

    setCopied(true);

    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">

      {/* Top Action Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-300 pb-4 no-print">

        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-serif flex items-center gap-2">
            <Download className="w-6 h-6 text-amber-600" />

            Procurement Compliance Report Generator
          </h1>

          <p className="text-xs text-slate-600 mt-0.5">
            Export or print procurement-ready Indian Standards decision-support assessment document.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">

          {/* Copy Summary */}
          <button
            onClick={handleCopySummary}
            className="bg-slate-800 text-slate-100 font-bold px-3 py-1.5 rounded text-xs flex items-center space-x-1 hover:bg-slate-900 transition"
          >
            {copied ? (
              <Check className="w-4 h-4 text-emerald-400" />
            ) : (
              <Copy className="w-4 h-4" />
            )}

            <span>
              {copied ? 'Copied Summary' : 'Copy Summary'}
            </span>
          </button>

          {/* Export JSON */}
          <button
            onClick={handleExportJSON}
            className="bg-slate-800 text-slate-100 font-bold px-3 py-1.5 rounded text-xs flex items-center space-x-1 hover:bg-slate-900 transition"
          >
            <Download className="w-4 h-4 text-amber-400" />

            <span>Export JSON</span>
          </button>

          {/* Print / Export PDF */}
          <button
            onClick={handlePrint}
            className="bg-amber-600 hover:bg-amber-700 text-slate-950 font-bold px-4 py-1.5 rounded text-xs flex items-center space-x-1.5 shadow-xs transition"
          >
            <Printer className="w-4 h-4" />

            <span>Print / Export PDF</span>
          </button>

        </div>
      </div>

      {/* Printable Report Document Card */}
      <div className="bg-white border-2 border-slate-900 rounded-lg p-8 space-y-6 shadow-md print:shadow-none print:border-none print:p-0 text-slate-900">

        {/* Document Header */}
        <div className="border-b-2 border-slate-900 pb-4 flex justify-between items-start">

          <div>
            <div className="text-xs font-mono font-bold text-slate-500 uppercase tracking-wider">
              INDIAN STANDARDS INTELLIGENCE ASSESSMENT
            </div>

            <h2 className="text-2xl font-bold font-serif text-slate-900 mt-1">
              Procurement Technical Compliance Report
            </h2>

            <div className="text-xs font-medium text-slate-700 mt-1">
              Ref ID:{' '}
              <span className="font-mono font-bold text-slate-900">
                {data.request_id}
              </span>{' '}
              | Date: {data.created_at}
            </div>
          </div>

          <div className="text-right text-xs font-mono">
            <div className="font-bold text-slate-900">
              MANAK ANVESHAN
            </div>

            <div className="text-slate-500 text-[10px]">
              SIH 2026 Decision Support Prototype
            </div>

            <div className="text-emerald-700 font-bold text-[10px] mt-1">
              Grounded in BIS Data
            </div>
          </div>

        </div>

        {/* Executive Summary */}
        <div>
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">
            1. Procurement Item Overview
          </h3>

          <div className="bg-slate-50 border border-slate-200 p-3 rounded text-xs space-y-1">

            <div>
              <span className="font-bold">Item Title:</span>{' '}
              {data.product_title}
            </div>

            <div>
              <span className="font-bold">Category:</span>{' '}
              {data.canonical_requirements?.product?.category}
            </div>

            <div>
              <span className="font-bold">Application:</span>{' '}
              {data.canonical_requirements?.application}
            </div>

            <div>
              <span className="font-bold">
                Extracted Parameters:{' '}
              </span>

              {Object.entries(
                data.canonical_requirements?.technical_parameters || {}
              )
                .map(([k, v]) => `${k}: ${v}`)
                .join(' | ')}
            </div>

          </div>
        </div>

        {/* Version & Superseded Alerts */}
        {data.version_alerts &&
          data.version_alerts.length > 0 && (
            <div>

              <h3 className="text-xs font-bold uppercase tracking-wider text-rose-800 border-b border-rose-300 pb-1 mb-2">
                2. Lifecycle & Outdated Reference Warnings
              </h3>

              <div className="space-y-2">

                {data.version_alerts.map((va, i) => (
                  <div
                    key={i}
                    className="bg-rose-50 border border-rose-300 p-3 rounded text-xs text-rose-950"
                  >

                    <div className="font-bold text-rose-900">
                      {va.title}
                    </div>

                    <div className="mt-0.5">
                      {va.message}
                    </div>

                    <div className="font-mono font-bold text-rose-900 bg-rose-100 p-1.5 rounded mt-1">
                      Action: {va.action_required}
                    </div>

                  </div>
                ))}

              </div>
            </div>
          )}

        {/* Recommended Primary & Normative Standards */}
        <div>

          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">
            3. Recommended Indian Standards Classification Table
          </h3>

          <table className="w-full text-left text-xs border-collapse border border-slate-300">

            <thead>
              <tr className="bg-slate-100 text-slate-900 font-bold border-b border-slate-300 text-[11px]">

                <th className="p-2 border-r border-slate-300">
                  IS Number
                </th>

                <th className="p-2 border-r border-slate-300">
                  Standard Title
                </th>

                <th className="p-2 border-r border-slate-300">
                  Classification
                </th>

                <th className="p-2 border-r border-slate-300">
                  Status
                </th>

                <th className="p-2">
                  Reason / Justification
                </th>

              </tr>
            </thead>

            <tbody className="divide-y divide-slate-300">

              {[
                ...(data.primary_standards || []),
                ...(data.supporting_standards || [])
              ].map((std, i) => (
                <tr key={i} className="align-top">

                  <td className="p-2 font-mono font-bold border-r border-slate-300">
                    {std.is_number}
                  </td>

                  <td className="p-2 border-r border-slate-300 font-medium">
                    {std.title}
                  </td>

                  <td className="p-2 font-bold border-r border-slate-300 uppercase text-[10px]">
                    {std.classification}
                  </td>

                  <td className="p-2 font-bold border-r border-slate-300">
                    {std.status}
                  </td>

                  <td className="p-2 text-[11px] text-slate-700">
                    {std.reason
                      ? std.reason.join('; ')
                      : 'Scope match.'}
                  </td>

                </tr>
              ))}

            </tbody>
          </table>
        </div>

        {/* QCO Matrix */}
        {data.certification_summary &&
          data.certification_summary.length > 0 && (
            <div>

              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 border-b border-slate-300 pb-1 mb-2">
                4. Mandatory Quality Control Order (QCO) Compliance Matrix
              </h3>

              <table className="w-full text-left text-xs border-collapse border border-slate-300">

                <thead>
                  <tr className="bg-slate-100 text-slate-900 font-bold border-b border-slate-300 text-[11px]">

                    <th className="p-2 border-r border-slate-300">
                      Standard
                    </th>

                    <th className="p-2 border-r border-slate-300">
                      Certification Scheme
                    </th>

                    <th className="p-2 border-r border-slate-300">
                      Status
                    </th>

                    <th className="p-2">
                      Mandatory Gazette Order Conditions
                    </th>

                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-300 font-mono text-[11px]">

                  {data.certification_summary.map((cs, i) => (
                    <tr key={i}>

                      <td className="p-2 font-bold border-r border-slate-300">
                        {cs.is_number}
                      </td>

                      <td className="p-2 border-r border-slate-300">
                        {cs.scheme}
                      </td>

                      <td className="p-2 font-bold border-r border-slate-300 text-emerald-700">
                        {cs.status}
                      </td>

                      <td className="p-2 text-slate-800 font-sans text-xs">
                        {cs.conditions}
                      </td>

                    </tr>
                  ))}

                </tbody>
              </table>
            </div>
          )}

        {/* Missing Requirements Gap Checklist */}
        {data.missing_requirements &&
          data.missing_requirements.length > 0 && (
            <div>

              <h3 className="text-xs font-bold uppercase tracking-wider text-amber-900 border-b border-amber-300 pb-1 mb-2">
                5. Specification Gap Audit Checklist
              </h3>

              <div className="space-y-1.5 text-xs">

                {data.missing_requirements.map((mr, i) => (
                  <div
                    key={i}
                    className="bg-amber-50 p-2 rounded border border-amber-200"
                  >

                    <span className="font-bold text-amber-950">
                      ⚠ {mr.attribute}:{' '}
                    </span>

                    <span className="text-amber-900">
                      {mr.message} ({mr.impact})
                    </span>

                  </div>
                ))}

              </div>
            </div>
          )}

        {/* Signatures & Disclaimers */}
        <div className="pt-8 border-t border-slate-300 flex justify-between items-end text-xs text-slate-500">

          <div>

            <div className="font-bold text-slate-800">
              Decision-Support System Verification
            </div>

            <div>
              Generated by MANAK ANVESHAN Engine v1.0
            </div>

            <div className="text-[10px] mt-1 text-slate-400">
              SIH 2026 Prototype • Grounded in Authoritative Data
            </div>

          </div>

          <div className="text-right border-t border-slate-400 pt-2 w-48 font-mono text-[11px]">

            <div className="text-slate-700">
              Procurement Officer / Technical Auditor Signature
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}