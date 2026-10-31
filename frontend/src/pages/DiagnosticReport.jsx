import { useMemo, useRef, useState } from "react";
import autoSageLogo from "../assets/auto-sage-brand-logo.png";
import Stepper from "../components/Stepper.jsx";
import { formatDateTime, vehicleLabel, vehicleSecondary } from "../stitch/dom.js";
import { createReportId } from "../utils/historyStorage.js";
import { exportElementToPdf } from "../utils/pdfExport.js";

export default function DiagnosticReport({
  results,
  vehicleInfo,
  reviewedTimestamp,
  onBackToResults,
}) {
  const [notes, setNotes] = useState("");
  const [downloading, setDownloading] = useState(false);
  const [downloadStatus, setDownloadStatus] = useState(null);
  const reportRef = useRef(null);

  const matches = useMemo(
    () => [...(results?.matches || []), ...(results?.cross_category_matches || [])],
    [results]
  );
  const primaryMatch = matches[0] || null;
  const secondaryMatches = matches.slice(1);

  const symptoms = (results?.selected_symptom_details || []).map((s) => s.label || s.text);
  const generatedTime = reviewedTimestamp || results?.timestamp || new Date().toISOString();
  const followUpAnswers = results?.follow_up_answers || {};

  const reportId = useMemo(
    () => results?.report_id || createReportId(generatedTime),
    [results, generatedTime]
  );

  const filename = `Auto_Sage_Diagnostic_Report_${reportId.replace(/[^A-Za-z0-9_-]/g, "_")}.pdf`;

  const handleDownloadPdf = async () => {
    if (!reportRef.current || downloading) return;
    setDownloading(true);
    setDownloadStatus("Generating official PDF document…");
    try {
      const outcome = await exportElementToPdf(reportRef.current, filename);
      if (outcome.ok) {
        setDownloadStatus(`PDF downloaded: ${filename}`);
      } else {
        setDownloadStatus(outcome.error || "Opened print dialog.");
      }
    } catch {
      setDownloadStatus("PDF generation encountered an error; using print dialog.");
      window.print();
    } finally {
      setDownloading(false);
      setTimeout(() => setDownloadStatus(null), 5000);
    }
  };

  const scrollToSection = (id) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <div className="w-full min-h-screen bg-slate-100/70 pb-32 animate-fade-in">
      {/* Top Application Navigation Stepper */}
      <div className="max-w-[1200px] mx-auto px-4 sm:px-6 pt-4 no-print">
        <Stepper currentStep={5} onStepClick={(page) => page === "results" && onBackToResults?.()} />
      </div>

      {/* Document Workspace Control Bar */}
      <div className="sticky top-16 z-30 bg-surface-container-lowest/95 backdrop-blur shadow-sm border-b border-surface-container no-print mb-6">
        <div className="max-w-[1200px] mx-auto px-4 sm:px-6 py-2.5 flex flex-col md:flex-row items-center justify-between gap-3">
          {/* Left: Back & Document Metadata */}
          <div className="flex items-center gap-3 w-full md:w-auto">
            <button
              type="button"
              onClick={onBackToResults}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-semibold transition-colors btn-press-fx"
            >
              <span className="material-symbols-outlined text-[16px]">arrow_back</span>
              <span>Back to Results</span>
            </button>
            <div className="h-4 w-px bg-surface-container-highest hidden sm:block" />
            <div className="flex items-center gap-2">
              <img
                src={autoSageLogo}
                alt="Auto Sage"
                className="h-5 sm:h-6 w-auto object-contain hidden sm:block select-none"
                onError={(e) => {
                  e.currentTarget.src = "/images/auto-sage-brand-logo.png";
                }}
              />
              <span className="text-xs font-bold text-on-surface uppercase tracking-wide">
                Vehicle Diagnostic Report
              </span>
              <span className="font-mono text-[11px] font-semibold text-primary bg-primary/10 px-2 py-0.5 rounded">
                {reportId}
              </span>
            </div>
          </div>

          {/* Center: Quick Jump Navigation Tabs */}
          <div className="hidden lg:flex items-center gap-1 text-[11px] font-medium text-on-surface-variant">
            <button
              type="button"
              onClick={() => scrollToSection("sec-vehicle")}
              className="px-2 py-1 rounded hover:bg-surface-container hover:text-on-surface transition-colors"
            >
              Vehicle
            </button>
            <span>&bull;</span>
            <button
              type="button"
              onClick={() => scrollToSection("sec-summary")}
              className="px-2 py-1 rounded hover:bg-surface-container hover:text-on-surface transition-colors"
            >
              Summary
            </button>
            <span>&bull;</span>
            <button
              type="button"
              onClick={() => scrollToSection("sec-symptoms")}
              className="px-2 py-1 rounded hover:bg-surface-container hover:text-on-surface transition-colors"
            >
              Symptoms
            </button>
            <span>&bull;</span>
            <button
              type="button"
              onClick={() => scrollToSection("sec-verification")}
              className="px-2 py-1 rounded hover:bg-surface-container hover:text-on-surface transition-colors"
            >
              Verification
            </button>
            <span>&bull;</span>
            <button
              type="button"
              onClick={() => scrollToSection("sec-directives")}
              className="px-2 py-1 rounded hover:bg-surface-container hover:text-on-surface transition-colors"
            >
              Directives
            </button>
            <span>&bull;</span>
            <button
              type="button"
              onClick={() => scrollToSection("sec-signoff")}
              className="px-2 py-1 rounded hover:bg-surface-container hover:text-on-surface transition-colors"
            >
              Sign-Off
            </button>
          </div>

          {/* Right: Export & Print Actions */}
          <div className="flex items-center gap-2 w-full md:w-auto justify-end">
            {downloadStatus && (
              <span className="text-[11px] text-primary font-medium hidden sm:inline animate-fade-in">
                {downloadStatus}
              </span>
            )}
            <button
              type="button"
              onClick={() => window.print()}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-semibold transition-colors btn-press-fx"
              title="Print document or save using browser dialog"
            >
              <span className="material-symbols-outlined text-[16px]">print</span>
              <span>Print / System PDF</span>
            </button>
            <button
              type="button"
              onClick={handleDownloadPdf}
              disabled={downloading}
              className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-primary text-on-primary text-xs font-semibold shadow-sm hover:bg-primary-container transition-all disabled:opacity-50 btn-press-fx"
            >
              {downloading ? (
                <>
                  <span className="material-symbols-outlined text-[16px] animate-spin">progress_activity</span>
                  <span>Rendering PDF…</span>
                </>
              ) : (
                <>
                  <span className="material-symbols-outlined text-[16px]">download</span>
                  <span>Download PDF Report</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* A4 Document Workspace Canvas */}
      <main className="max-w-[900px] mx-auto px-2 sm:px-4">
        <article
          ref={reportRef}
          id="diagnostic-report-document"
          className="report-document w-full bg-white text-slate-900 shadow-xl rounded-none sm:rounded-lg border border-slate-200 p-6 sm:p-10 md:p-12 flex flex-col gap-6 text-[13px] leading-relaxed print:shadow-none print:border-none print:p-0 print:m-0"
        >
          {/* =========================================================================
              SECTION A: FORMAL DOCUMENT HEADER
             ========================================================================= */}
          <header className="border-b-2 border-slate-900 pb-5 flex flex-col sm:flex-row sm:items-start justify-between gap-4 report-avoid-break">
            <div className="space-y-2">
              <div className="flex items-center gap-3">
                <img
                  src={autoSageLogo}
                  alt="Auto Sage Logo"
                  className="h-10 sm:h-12 w-auto object-contain select-none shrink-0"
                  onError={(e) => {
                    e.currentTarget.src = "/images/auto-sage-brand-logo.png";
                  }}
                />
                <div className="h-8 w-px bg-slate-300 hidden sm:block" />
                <div>
                  <div className="font-extrabold text-xs sm:text-sm tracking-wider uppercase text-slate-900 leading-tight">
                    Diagnostic Systems
                  </div>
                  <div className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">
                    Automotive Engineering &bull; Inspection Division
                  </div>
                </div>
              </div>

              <div className="pt-1">
                <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight uppercase">
                  Vehicle Diagnostic Report
                </h1>
                <p className="text-xs text-slate-600 font-medium">
                  Preliminary Symptom-Based Diagnostic Evaluation &bull; Physical Verification Directive
                </p>
              </div>
            </div>

            {/* Formal Report Metadata Block */}
            <div className="sm:text-right shrink-0 bg-slate-50 border border-slate-200 p-3 rounded space-y-1 min-w-[210px]">
              <div>
                <span className="block text-[9px] font-bold uppercase tracking-wider text-slate-500">
                  Document Reference
                </span>
                <span className="font-mono text-xs font-black text-slate-900">
                  {reportId}
                </span>
              </div>
              <div>
                <span className="block text-[9px] font-bold uppercase tracking-wider text-slate-500">
                  Date / Time Issued
                </span>
                <span className="text-xs font-medium text-slate-800">
                  {formatDateTime(generatedTime)}
                </span>
              </div>
              <div>
                <span className="block text-[9px] font-bold uppercase tracking-wider text-slate-500">
                  Assessment Status
                </span>
                <span className="inline-block text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-100 text-blue-900">
                  Preliminary Assessment
                </span>
              </div>
            </div>
          </header>

          {/* =========================================================================
              SECTION B: VEHICLE SPECIFICATIONS & INTAKE INFORMATION
             ========================================================================= */}
          <section id="sec-vehicle" className="report-avoid-break">
            <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2.5">
              <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                1. Vehicle Intake Specifications
              </h2>
              <span className="text-[10px] font-bold text-slate-500 uppercase">
                Subsystem: {results?.category_name || "General Subsystem"}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs bg-slate-50 p-3 rounded border border-slate-200">
              <div>
                <span className="block text-[10px] font-bold uppercase text-slate-500">
                  Vehicle Make &amp; Model
                </span>
                <strong className="text-slate-900 block truncate">
                  {vehicleLabel(vehicleInfo)}
                </strong>
              </div>
              <div>
                <span className="block text-[10px] font-bold uppercase text-slate-500">
                  Model Year
                </span>
                <span className="text-slate-800 block">
                  {vehicleInfo?.year || "Not recorded"}
                </span>
              </div>
              <div>
                <span className="block text-[10px] font-bold uppercase text-slate-500">
                  Powertrain / Fuel
                </span>
                <span className="text-slate-800 block truncate">
                  {vehicleInfo?.engine ? `${vehicleInfo.engine} · ` : ""}
                  {vehicleInfo?.energy || "Universal ICE / Hybrid"}
                </span>
              </div>
              <div>
                <span className="block text-[10px] font-bold uppercase text-slate-500">
                  Transmission / Odometer
                </span>
                <span className="text-slate-800 block truncate">
                  {vehicleInfo?.transmission || "Automatic"}
                  {vehicleInfo?.odometer ? ` · ${vehicleInfo.odometer}` : ""}
                </span>
              </div>
            </div>
          </section>

          {/* =========================================================================
              SECTION C: DIAGNOSTIC SUMMARY & HYPOTHESIS
             ========================================================================= */}
          <section id="sec-summary" className="report-avoid-break">
            <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2.5">
              <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                2. Diagnostic Assessment Summary
              </h2>
              <span className="text-[10px] font-bold text-slate-500 uppercase">
                Automated Rule Evaluation
              </span>
            </div>

            {primaryMatch ? (
              <div className="border border-slate-300 rounded overflow-hidden">
                {/* Summary Title & Badges Bar */}
                <div className="bg-slate-100 p-3 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <span className="text-[10px] font-mono font-bold text-slate-500 block">
                      Ref Code: {primaryMatch.rule_id ? primaryMatch.rule_id.replace(/^RULE_/, "") : "N/A"}
                    </span>
                    <h3 className="text-base font-extrabold text-slate-900">
                      {primaryMatch.possible_fault || primaryMatch.title}
                    </h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <FormalStatusBadge status={primaryMatch.diagnosis_status} />
                    {primaryMatch.safety_level && (
                      <FormalSafetyBadge level={primaryMatch.safety_level} />
                    )}
                  </div>
                </div>

                {/* Subsystem & Target Component Strip */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3 bg-white border-b border-slate-200 text-xs">
                  <div>
                    <span className="block text-[10px] font-bold uppercase text-slate-500">
                      Primary Affected Component
                    </span>
                    <strong className="text-slate-900 text-sm">
                      {primaryMatch.affected_component || "Subsystem Assembly"}
                    </strong>
                  </div>
                  <div>
                    <span className="block text-[10px] font-bold uppercase text-slate-500">
                      Subsystem Domain
                    </span>
                    <span className="text-slate-800 font-medium">
                      {primaryMatch.subsystem || primaryMatch.category_name || results?.category_name}
                    </span>
                  </div>
                </div>

                {/* Explanation Prose */}
                <div className="p-3 bg-slate-50/70 text-xs text-slate-800 space-y-1.5">
                  <span className="block text-[10px] font-bold uppercase text-slate-500">
                    Reasoning &amp; Clinical Correlation
                  </span>
                  <p className="leading-relaxed">
                    {primaryMatch.explanation ||
                      `Reported symptoms are consistent with an operational anomaly in the ${primaryMatch.affected_component}. Standard diagnostic checks are required to confirm physical defect.`}
                  </p>
                </div>

                {/* Triage Warning Notice */}
                <div className="p-2.5 bg-amber-50/80 border-t border-amber-200 text-[11px] text-amber-900 flex items-start gap-2">
                  <span className="material-symbols-outlined text-amber-700 text-[16px] shrink-0 mt-0.5">
                    warning
                  </span>
                  <div>
                    <strong>Triage Notice:</strong> The potential fault identified above represents an unverified
                    diagnostic hypothesis. Component replacement or teardown must not take place until bench
                    measurements corroborate abnormal test criteria specified in Section 4.
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-4 rounded border border-slate-200 bg-slate-50 text-center text-slate-600">
                <p className="font-semibold text-slate-800">No Matching Fault Identified</p>
                <p className="text-xs mt-1">
                  The reported symptoms did not satisfy any known failure pattern in the diagnostic database.
                  Manual physical inspection by an automotive technician is recommended.
                </p>
              </div>
            )}
          </section>

          {/* =========================================================================
              SECTION D: REPORTED SYMPTOMS & INTAKE INQUIRY
             ========================================================================= */}
          <section id="sec-symptoms" className="report-avoid-break">
            <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2.5">
              <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                3. Customer-Reported Symptoms &amp; Diagnostic Inquiry
              </h2>
              <span className="text-[10px] font-bold text-slate-500 uppercase">
                {symptoms.length} Observed Condition(s)
              </span>
            </div>

            {symptoms.length > 0 ? (
              <div className="overflow-x-auto border border-slate-200 rounded">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="bg-slate-100 text-slate-700 font-bold uppercase text-[10px] border-b border-slate-200">
                      <th className="py-2 px-3 w-10">#</th>
                      <th className="py-2 px-3">Reported Symptom Description</th>
                      <th className="py-2 px-3 w-44">Subsystem Domain</th>
                      <th className="py-2 px-3 w-32">Intake Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200">
                    {symptoms.map((sym, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/60">
                        <td className="py-2 px-3 font-mono font-bold text-slate-500">{idx + 1}</td>
                        <td className="py-2 px-3 font-medium text-slate-900">{sym}</td>
                        <td className="py-2 px-3 text-slate-600">{results?.category_name || "Vehicle Chassis"}</td>
                        <td className="py-2 px-3">
                          <span className="inline-block text-[10px] font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                            Customer Confirmed
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">No specific symptoms recorded for this intake session.</p>
            )}

            {/* Follow-up Questions Table if present */}
            {Object.keys(followUpAnswers).length > 0 && (
              <div className="mt-3 pt-2">
                <span className="block text-[10px] font-bold uppercase text-slate-500 mb-1.5">
                  Targeted Clarification Inquiry Responses:
                </span>
                <div className="border border-slate-200 rounded overflow-hidden">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="bg-slate-100 text-slate-700 font-bold uppercase text-[10px] border-b border-slate-200">
                        <th className="py-1.5 px-3">Diagnostic Clarification Check</th>
                        <th className="py-1.5 px-3 w-36">Response Recorded</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200">
                      {Object.entries(followUpAnswers).map(([qid, ans], i) => (
                        <tr key={i} className="hover:bg-slate-50/60">
                          <td className="py-1.5 px-3 font-medium text-slate-800">
                            Check {qid.replace(/^Q_/, "")}: Condition observed during operation?
                          </td>
                          <td className="py-1.5 px-3 font-mono font-bold uppercase text-slate-900">
                            {String(ans) === "yes" ? (
                              <span className="text-emerald-700 font-bold">YES &bull; Confirmed</span>
                            ) : String(ans) === "no" ? (
                              <span className="text-rose-700 font-bold">NO &bull; Not Present</span>
                            ) : (
                              <span className="text-slate-600 font-medium">Uncertain / Skipped</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </section>

          {/* =========================================================================
              SECTION E: RECOMMENDED PHYSICAL BENCH VERIFICATION (TIER A)
             ========================================================================= */}
          {primaryMatch && primaryMatch.diagnosis_steps?.length > 0 && (
            <section id="sec-verification" className="report-avoid-break">
              <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2">
                <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                  4. Recommended Physical Verification Procedures (Tier A Checks)
                </h2>
                <span className="text-[10px] font-bold text-slate-500 uppercase">
                  {primaryMatch.diagnosis_steps.length} Bench Step(s)
                </span>
              </div>
              <p className="text-xs text-slate-600 mb-2">
                Technicians must perform these bench checks in sequence before servicing or replacing components.
                Compare observed multimeter or gauge readings against standard OEM criteria:
              </p>

              <div className="overflow-x-auto border border-slate-300 rounded">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="bg-slate-100 text-slate-800 font-bold uppercase text-[10px] border-b border-slate-300">
                      <th className="py-2 px-2.5 w-8">#</th>
                      <th className="py-2 px-3">Physical Inspection / Bench Test</th>
                      <th className="py-2 px-3 w-52">Expected Abnormal Finding (Fault)</th>
                      <th className="py-2 px-3 w-52">Expected Normal Finding (Pass)</th>
                      <th className="py-2 px-2.5 w-24">Technician Result</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200">
                    {primaryMatch.diagnosis_steps.map((s, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/70 align-top">
                        <td className="py-2.5 px-2.5 font-mono font-bold text-slate-600">{s.step_number || idx + 1}</td>
                        <td className="py-2.5 px-3 font-semibold text-slate-900 leading-snug">
                          {s.step}
                        </td>
                        <td className="py-2.5 px-3 text-red-900 font-medium bg-red-50/40">
                          {s.abnormal_result}
                        </td>
                        <td className="py-2.5 px-3 text-emerald-900 font-medium bg-emerald-50/40">
                          {s.normal_result}
                        </td>
                        <td className="py-2.5 px-2.5 text-slate-400 font-mono text-[11px]">
                          [ &nbsp; ] Pass<br />[ &nbsp; ] Fail
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* =========================================================================
              SECTION F: POSSIBLE CAUSES & ROOT CAUSE TAXONOMY
             ========================================================================= */}
          {primaryMatch && Array.isArray(primaryMatch.possible_causes) && primaryMatch.possible_causes.length > 0 && (
            <section className="report-avoid-break">
              <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2">
                <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                  5. Documented Failure Modes &amp; Known Root Causes
                </h2>
                <span className="text-[10px] font-bold text-slate-500 uppercase">
                  Engineering Taxonomy
                </span>
              </div>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                {primaryMatch.possible_causes.map((cause, i) => (
                  <li key={i} className="p-2 rounded bg-slate-50 border border-slate-200 flex items-start gap-2">
                    <span className="material-symbols-outlined text-[15px] text-blue-700 shrink-0 mt-0.5">
                      check_circle
                    </span>
                    <span className="text-slate-800 leading-snug">{cause}</span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* =========================================================================
              SECTION G: REPAIR & MITIGATION RECOMMENDATIONS (TIER B)
             ========================================================================= */}
          {primaryMatch && (
            <section id="sec-directives" className="report-avoid-break">
              <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2">
                <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                  6. Structured Maintenance Directives &amp; Repair Guidance (Tier B)
                </h2>
                <span className="text-[10px] font-bold text-slate-500 uppercase">
                  Service Manual Directives
                </span>
              </div>

              {primaryMatch.maintenance_actions ? (
                <div className="space-y-2.5">
                  {/* Corrective and Preventive Row */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div className="p-3 rounded border border-slate-200 bg-slate-50">
                      <span className="block text-[10px] font-bold uppercase text-blue-800 mb-0.5">
                        Recommended Corrective Action
                      </span>
                      <p className="text-slate-900 leading-relaxed">
                        {primaryMatch.maintenance_actions.corrective_action}
                      </p>
                    </div>

                    <div className="p-3 rounded border border-slate-200 bg-slate-50">
                      <span className="block text-[10px] font-bold uppercase text-slate-700 mb-0.5">
                        Preventive Maintenance Protocol
                      </span>
                      <p className="text-slate-900 leading-relaxed">
                        {primaryMatch.maintenance_actions.preventive_measure}
                      </p>
                    </div>
                  </div>

                  {/* Replacement Criteria */}
                  {primaryMatch.maintenance_actions.replacement_criteria && (
                    <div className="p-3 rounded border border-slate-200 bg-slate-50 text-xs">
                      <span className="block text-[10px] font-bold uppercase text-slate-600 mb-0.5">
                        Objective Component Replacement Criteria
                      </span>
                      <p className="text-slate-900 leading-relaxed font-medium">
                        {primaryMatch.maintenance_actions.replacement_criteria}
                      </p>
                    </div>
                  )}

                  {/* Anti-Mistake Warning */}
                  {primaryMatch.maintenance_actions.do_not_replace_warning && (
                    <div className="p-3 rounded border border-red-300 bg-red-50 text-xs text-red-950 flex items-start gap-2">
                      <span className="material-symbols-outlined text-red-700 text-[18px] shrink-0 mt-0.5">
                        cancel
                      </span>
                      <div>
                        <strong className="block text-[10px] uppercase font-bold text-red-900 tracking-wide">
                          Anti-Mistake Directive (Avoid Premature Replacement):
                        </strong>
                        <p className="leading-snug mt-0.5 text-red-900">
                          {primaryMatch.maintenance_actions.do_not_replace_warning}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Required Expertise & Tools Strip */}
                  <div className="flex flex-wrap items-center justify-between gap-2 p-2 bg-slate-100 rounded border border-slate-200 text-[11px] text-slate-700">
                    <div>
                      <strong className="text-slate-900">Required Expertise:</strong>{" "}
                      {primaryMatch.required_expertise || "Certified Automotive Service Technician"}
                    </div>
                    {Array.isArray(primaryMatch.required_tools) && primaryMatch.required_tools.length > 0 && (
                      <div>
                        <strong className="text-slate-900">Tooling:</strong>{" "}
                        {primaryMatch.required_tools.join(", ")}
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <p className="text-xs text-slate-700 bg-slate-50 p-3 rounded border border-slate-200">
                  {primaryMatch.suggested_next_steps ||
                    "Follow standard workshop service manual procedures. Do not replace components before physical testing confirms failure."}
                </p>
              )}
            </section>
          )}

          {/* =========================================================================
              SECTION H: DIFFERENTIAL CANDIDATES (IF MULTIPLE MATCHES EXIST)
             ========================================================================= */}
          {secondaryMatches.length > 0 && (
            <section className="report-avoid-break">
              <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2">
                <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  <span className="w-1.5 h-3.5 bg-slate-500 rounded-xs inline-block" />
                  7. Secondary Differential Hypotheses
                </h2>
                <span className="text-[10px] font-bold text-slate-500 uppercase">
                  {secondaryMatches.length} Additional Possibility
                </span>
              </div>
              <div className="overflow-x-auto border border-slate-200 rounded">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="bg-slate-100 text-slate-700 font-bold uppercase text-[10px] border-b border-slate-200">
                      <th className="py-2 px-3">Potential Fault</th>
                      <th className="py-2 px-3">Target Component</th>
                      <th className="py-2 px-3 w-32">Status</th>
                      <th className="py-2 px-3 w-28">Safety Priority</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200">
                    {secondaryMatches.map((m, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/60">
                        <td className="py-2 px-3 font-semibold text-slate-900">{m.possible_fault || m.title}</td>
                        <td className="py-2 px-3 text-slate-700">{m.affected_component}</td>
                        <td className="py-2 px-3"><FormalStatusBadge status={m.diagnosis_status} /></td>
                        <td className="py-2 px-3"><FormalSafetyBadge level={m.safety_level} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* =========================================================================
              SECTION I: SAFETY PRECAUTIONS & OPERATIONAL ADVISORY
             ========================================================================= */}
          <section className="report-avoid-break">
            <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2">
              <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <span className="w-1.5 h-3.5 bg-red-700 rounded-xs inline-block" />
                8. Operational Safety &amp; Roadworthiness Advisory
              </h2>
              <span className="text-[10px] font-bold text-slate-500 uppercase">
                Hazard Assessment
              </span>
            </div>

            <div className="p-3.5 rounded border border-slate-300 bg-slate-50 text-xs space-y-2">
              <div className="flex items-start gap-2.5">
                <span className="material-symbols-outlined text-[20px] text-red-700 shrink-0 mt-0.5">
                  shield
                </span>
                <div>
                  <strong className="block text-slate-900 text-xs font-bold uppercase tracking-wide">
                    Operational Driving Advisory:
                  </strong>
                  <p className="text-slate-800 leading-relaxed mt-0.5">
                    {primaryMatch?.safety_level?.toUpperCase() === "CRITICAL"
                      ? "CRITICAL LIFE-SAFETY HAZARD — CEASE OPERATION IMMEDIATELY. Continued operation compromises primary vehicle control or stopping distance. Flatbed towing to an authorized service facility is strongly recommended."
                      : primaryMatch?.safety_level?.toUpperCase() === "HIGH"
                      ? "HIGH SAFETY RISK — OPERATE WITH EXTREME CAUTION. Avoid highway speeds or heavy driving loads. Schedule immediate workshop inspection within 24–48 hours."
                      : "MODERATE TECHNICAL RISK. Vehicle may be operated with caution for short trips. Schedule inspection at your earliest service appointment."}
                  </p>
                </div>
              </div>

              {primaryMatch?.safety_warning && (
                <div className="pt-2 border-t border-slate-200 text-slate-800 font-medium">
                  <strong>Component Specific Hazard:</strong> {primaryMatch.safety_warning}
                </div>
              )}
            </div>
          </section>

          {/* =========================================================================
              SECTION J: PROFESSIONAL DIAGNOSTIC CONCLUSION
             ========================================================================= */}
          <section className="report-avoid-break">
            <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2">
              <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                9. Report Conclusion &amp; Recommended Next Steps
              </h2>
              <span className="text-[10px] font-bold text-slate-500 uppercase">
                Technical Conclusion
              </span>
            </div>
            <div className="p-3.5 bg-slate-100 rounded border border-slate-200 text-xs text-slate-800 leading-relaxed">
              {primaryMatch ? (
                <>
                  The reported vehicle symptom evidence is consistent with a potential anomaly in the{" "}
                  <strong>{primaryMatch.affected_component || "subsystem assembly"}</strong>. Because this computerized
                  assessment is based purely on observed symptoms and non-invasive input, a confirmed physical diagnosis
                  requires the execution of the bench verification checks listed in Section 4. Component replacement
                  is contraindicated until abnormal readings are physically verified by a qualified technician.
                </>
              ) : (
                <>
                  No conclusive fault hypothesis was satisfied by the reported symptoms. A qualified automotive technician
                  should conduct an interactive road test and manual physical inspection across the chassis.
                </>
              )}
            </div>
          </section>

          {/* =========================================================================
              SECTION K: TECHNICIAN SIGN-OFF & FIELD NOTES
             ========================================================================= */}
          <section id="sec-signoff" className="report-avoid-break">
            <div className="flex items-center justify-between border-b border-slate-300 pb-1 mb-2">
              <h2 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <span className="w-1.5 h-3.5 bg-blue-700 rounded-xs inline-block" />
                10. Workshop Service Authorization &amp; Sign-Off
              </h2>
              <span className="text-[10px] font-bold text-slate-500 uppercase">
                Field Sign-Off
              </span>
            </div>

            <div className="border border-slate-300 rounded p-3.5 bg-slate-50/50 space-y-3">
              {/* Optional Technician Notes Area */}
              <div>
                <label
                  htmlFor="tech-notes"
                  className="block text-[10px] font-bold uppercase text-slate-600 mb-1"
                >
                  Diagnostic Observations &amp; Physical Bench Measurements:
                </label>
                <textarea
                  id="tech-notes"
                  className="w-full rounded bg-white p-2.5 text-xs border border-slate-300 focus:outline-none focus:ring-1 focus:ring-blue-600 min-h-[65px] no-print"
                  placeholder="Record multimeter values, vacuum gauge readings, visual wear remarks, or repair authorizations…"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
                {notes ? (
                  <p className="hidden print:block text-xs text-slate-800 p-2.5 bg-white border border-slate-200 rounded whitespace-pre-wrap">
                    {notes}
                  </p>
                ) : (
                  <div className="hidden print:block h-14 border border-dashed border-slate-300 rounded bg-white p-2 text-slate-400 text-[11px] italic">
                    (No technician notes recorded)
                  </div>
                )}
              </div>

              {/* Signatures & Bay Details */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-3 border-t border-slate-200 text-xs">
                <div>
                  <span className="block text-[10px] font-bold uppercase text-slate-500">Service Facility</span>
                  <div className="flex items-center gap-1.5 my-1">
                    <img
                      src={autoSageLogo}
                      alt="Auto Sage"
                      className="h-4 w-auto object-contain select-none opacity-85"
                      onError={(e) => {
                        e.currentTarget.src = "/images/auto-sage-brand-logo.png";
                      }}
                    />
                  </div>
                  <span className="block text-[10px] text-slate-500">Bay 04 &bull; Triage</span>
                </div>
                <div>
                  <span className="block text-[10px] font-bold uppercase text-slate-500">Work Order Status</span>
                  <span className="text-blue-800 font-bold">Pending Verification</span>
                  <span className="block text-[10px] text-slate-500">Bench Test Required</span>
                </div>
                <div>
                  <div className="h-7 border-b border-dashed border-slate-400 mb-1" />
                  <span className="block text-[10px] uppercase font-bold text-slate-600">
                    Inspecting Technician
                  </span>
                </div>
                <div>
                  <div className="h-7 border-b border-dashed border-slate-400 mb-1" />
                  <span className="block text-[10px] uppercase font-bold text-slate-600">
                    Inspection Date
                  </span>
                </div>
              </div>
            </div>
          </section>

          {/* =========================================================================
              SECTION L: DISCLAIMER & FORMAL CITATION FOOTER
             ========================================================================= */}
          <footer className="pt-4 border-t border-slate-300 text-[10px] text-slate-600 space-y-2 report-avoid-break">
            <div className="flex items-center justify-between pb-1 border-b border-slate-200">
              <div className="flex items-center gap-2">
                <img
                  src={autoSageLogo}
                  alt="Auto Sage"
                  className="h-3.5 w-auto object-contain select-none opacity-75"
                  onError={(e) => {
                    e.currentTarget.src = "/images/auto-sage-brand-logo.png";
                  }}
                />
                <span className="text-[9px] uppercase tracking-wider font-bold text-slate-500">
                  Automotive Diagnostic &amp; Inspection Systems
                </span>
              </div>
              <span className="font-mono text-[9px] text-slate-400">
                Document Ref: {reportId}
              </span>
            </div>
            <p className="leading-snug">
              <strong>Diagnostic Disclaimer:</strong> This document is generated by Auto Sage for preliminary vehicle fault
              triage and inspection planning. Diagnostic hypotheses are derived strictly from user-reported symptom observations
              and do not constitute certified physical confirmation. Physical verification must be conducted by certified
              personnel prior to parts purchase or mechanical teardown.
            </p>
            <p className="leading-snug text-slate-500">
              <strong>Knowledge Base Grounding:</strong> Grounded in the peer-reviewed research dataset:{" "}
              <em>Automotive Faults Dataset for Diagnostic and Maintenance Systems</em> (Obike &amp; Obot), Zenodo DOI:{" "}
              <a
                className="text-blue-700 underline"
                href="https://doi.org/10.5281/zenodo.15626055"
                target="_blank"
                rel="noreferrer"
              >
                10.5281/zenodo.15626055
              </a>
              , CC BY 4.0. Document ID: {reportId}.
            </p>
          </footer>
        </article>
      </main>
    </div>
  );
}

function FormalStatusBadge({ status }) {
  const st = String(status || "Possible Fault Identified");
  if (st.includes("Evidence Supports") || st.includes("Corroborated")) {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-900 border border-emerald-300">
        <span className="material-symbols-outlined text-[13px]">verified</span>
        Evidence Supports Fault
      </span>
    );
  }
  if (st.includes("Not Supported")) {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-rose-100 text-rose-900 border border-rose-300">
        <span className="material-symbols-outlined text-[13px]">cancel</span>
        Not Supported
      </span>
    );
  }
  if (st.includes("Further") || st.includes("Requires")) {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-950 border border-amber-300">
        <span className="material-symbols-outlined text-[13px]">hourglass_top</span>
        Further Inspection Required
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-blue-100 text-blue-900 border border-blue-300">
      <span className="material-symbols-outlined text-[13px]">rule</span>
      Possible Fault Identified
    </span>
  );
}

function FormalSafetyBadge({ level }) {
  const lev = String(level || "Moderate").toUpperCase();
  if (lev === "CRITICAL") {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-red-100 text-red-950 border border-red-300">
        <span className="material-symbols-outlined text-[13px] text-red-700">emergency</span>
        Critical Safety Alert
      </span>
    );
  }
  if (lev === "HIGH") {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-950 border border-amber-300">
        <span className="material-symbols-outlined text-[13px] text-amber-700">warning</span>
        High Risk
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-800 border border-slate-300">
      <span className="material-symbols-outlined text-[13px] text-slate-600">info</span>
      Moderate Risk
    </span>
  );
}
