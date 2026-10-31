import { useMemo, useRef, useState } from "react";
import Stepper from "../components/Stepper.jsx";
import { FlowchartPanel, RecommendedChecks, SafetyBadge, StatusBadge } from "../components/Evidence.jsx";
import { formatDateTime, vehicleLabel } from "../stitch/dom.js";
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
  const symptoms = (results?.selected_symptom_details || []).map((s) => s.label || s.text);
  const generatedTime = reviewedTimestamp || results?.timestamp || new Date().toISOString();
  const followUpAnswers = results?.follow_up_answers || {};

  const reportId = useMemo(
    () => results?.report_id || createReportId(generatedTime),
    [results, generatedTime]
  );

  const filename = `Auto_Sage_Report_${reportId.replace(/[^A-Za-z0-9_-]/g, "_")}.pdf`;

  const handleDownloadPdf = async () => {
    if (!reportRef.current || downloading) return;
    setDownloading(true);
    setDownloadStatus("Preparing PDF document…");
    try {
      const outcome = await exportElementToPdf(reportRef.current, filename);
      if (outcome.ok) {
        setDownloadStatus(`PDF downloaded: ${filename}`);
      } else {
        setDownloadStatus(outcome.error || "Opened browser print window.");
      }
    } catch {
      setDownloadStatus("PDF generation encountered an error; using print dialog.");
      window.print();
    } finally {
      setDownloading(false);
      setTimeout(() => setDownloadStatus(null), 5000);
    }
  };

  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1100px] mx-auto pb-24">
      <Stepper currentStep={5} onStepClick={(page) => page === "results" && onBackToResults?.()} />

      {/* Top Action Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-space-sm bg-surface-container-lowest rounded-xl p-space-sm shadow-sm border border-surface-container no-print">
        <button
          type="button"
          onClick={onBackToResults}
          className="inline-flex items-center gap-1.5 px-space-md py-2 rounded-lg bg-surface-container text-on-surface font-headline-sm text-[13px] hover:bg-surface-container-high transition-colors"
        >
          <span className="material-symbols-outlined text-[18px]">arrow_back</span>
          Back to Results
        </button>

        <div className="flex items-center gap-space-sm">
          {downloadStatus && (
            <span className="text-[12px] text-primary font-medium">{downloadStatus}</span>
          )}
          <button
            type="button"
            onClick={() => window.print()}
            className="inline-flex items-center gap-1.5 px-space-md py-2 rounded-lg bg-surface-container text-on-surface font-headline-sm text-[13px] hover:bg-surface-container-high transition-colors"
          >
            <span className="material-symbols-outlined text-[18px]">print</span>
            Print / System PDF
          </button>
          <button
            type="button"
            onClick={handleDownloadPdf}
            disabled={downloading}
            className="inline-flex items-center gap-1.5 px-space-lg py-2 rounded-lg bg-primary-container text-on-primary font-headline-sm text-[13px] shadow-sm hover:bg-primary transition-all disabled:opacity-50"
          >
            {downloading ? (
              <>
                <span className="material-symbols-outlined text-[18px] animate-spin">progress_activity</span>
                Rendering PDF…
              </>
            ) : (
              <>
                <span className="material-symbols-outlined text-[18px]">download</span>
                Download Official PDF
              </>
            )}
          </button>
        </div>
      </div>

      {/* Printable Work Order Dossier Article */}
      <article
        ref={reportRef}
        id="diagnostic-report-content"
        className="bg-surface-container-lowest rounded-2xl shadow-sm p-space-lg md:p-space-xl flex flex-col gap-space-lg border border-surface-container print:border-none print:shadow-none print:p-0"
      >
        {/* Dossier Header */}
        <header className="border-b-2 border-primary/20 pb-space-md flex flex-col sm:flex-row sm:items-start justify-between gap-space-md">
          <div>
            <div className="flex items-center gap-2 text-primary font-bold tracking-wider text-label-caps uppercase">
              <span className="material-symbols-outlined text-[20px]">token</span>
              <span>AUTO SAGE KBS &bull; UNIVERSITY DIAGNOSTIC SYSTEM (CT-359)</span>
            </div>
            <h1 className="font-headline-lg text-[24px] md:text-[28px] text-on-surface font-extrabold tracking-tight mt-1">
              Technical Work Order &amp; Diagnostic Dossier
            </h1>
            <p className="font-body-sm text-[12px] text-on-surface-variant">
              Deterministic Propositional Logic Knowledge-Based System Evaluation &bull; Component Verification Directive
            </p>
          </div>

          <div className="flex flex-col sm:items-end gap-1">
            <span className="font-mono text-[13px] font-bold text-on-surface bg-surface-container-low px-3 py-1 rounded-lg border border-surface-container">
              REPORT ID: {reportId}
            </span>
            <span className="text-[11px] text-on-surface-variant">
              Issued: {formatDateTime(generatedTime)}
            </span>
            {results?.overall_safety_level && (
              <SafetyBadge level={results.overall_safety_level} />
            )}
          </div>
        </header>

        {/* Section 1: Vehicle Profile */}
        <section className="bg-surface-container-low p-space-md rounded-xl border border-surface-container">
          <h2 className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider mb-2">
            1. VEHICLE PROFILE &amp; INTAKE SPECIFICATIONS
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-space-sm text-[12px]">
            <div>
              <span className="text-on-surface-variant block text-[10px] uppercase font-semibold">
                Vehicle Name
              </span>
              <strong className="text-on-surface text-[13px]">{vehicleLabel(vehicleInfo)}</strong>
            </div>
            <div>
              <span className="text-on-surface-variant block text-[10px] uppercase font-semibold">
                Model Year
              </span>
              <span className="text-on-surface">{vehicleInfo?.year || "Not recorded"}</span>
            </div>
            <div>
              <span className="text-on-surface-variant block text-[10px] uppercase font-semibold">
                Powertrain / Fuel
              </span>
              <span className="text-on-surface">
                {vehicleInfo?.engine ? `${vehicleInfo.engine} · ` : ""}
                {vehicleInfo?.energy || "Universal ICE/EV"}
              </span>
            </div>
            <div>
              <span className="text-on-surface-variant block text-[10px] uppercase font-semibold">
                Transmission / Odo
              </span>
              <span className="text-on-surface">
                {vehicleInfo?.transmission || "Automatic"}
                {vehicleInfo?.odometer ? ` · ${vehicleInfo.odometer}` : ""}
              </span>
            </div>
          </div>
        </section>

        {/* Section 2: Observed Symptoms & Follow-Up Inquiry */}
        <section className="border border-surface-container p-space-md rounded-xl space-y-3">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <h2 className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider">
                2. PRIMARY OBSERVED SYMPTOMS &amp; DIAGNOSTIC INQUIRY
              </h2>
              <span className="font-body-sm text-[11px] text-on-surface-variant">
                Subsystem: <strong>{results?.category_name || "—"}</strong>
              </span>
            </div>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-1.5 text-[12px]">
              {symptoms.map((s, idx) => (
                <li key={idx} className="flex items-center gap-2 p-1.5 rounded bg-surface-container-low">
                  <span className="material-symbols-outlined text-[16px] text-primary">check_circle</span>
                  <span className="font-medium text-on-surface">{s}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Follow-up answers if present */}
          {Object.keys(followUpAnswers).length > 0 && (
            <div className="pt-2 border-t border-surface-container">
              <span className="text-[11px] font-bold text-on-surface-variant uppercase tracking-wider block mb-1">
                Recorded Dynamic Follow-Up Answers:
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-[11px]">
                {Object.entries(followUpAnswers).map(([qid, ans]) => (
                  <div key={qid} className="p-1.5 rounded bg-surface-container-low flex items-center justify-between">
                    <span className="font-mono text-outline">{qid}:</span>
                    <span className="font-bold uppercase text-primary">{String(ans)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        {/* Section 3: Diagnostic Findings & Components */}
        <section className="border border-surface-container p-space-md rounded-xl">
          <h2 className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider mb-2">
            3. DETERMINISTIC FAULT HYPOTHESES &amp; AFFECTED COMPONENTS
          </h2>
          {matches.length === 0 ? (
            <p className="text-[13px] text-on-surface-variant">
              No matching diagnostic rule was satisfied in the knowledge base.
              {results?.no_match_reason ? ` Reason: ${results.no_match_reason}` : ""}
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-[12px] border-collapse">
                <thead>
                  <tr className="border-b border-surface-container text-on-surface-variant font-label-caps text-[10px] uppercase">
                    <th className="py-2 pr-2">#</th>
                    <th className="py-2 pr-2">Hypothesis / Fault</th>
                    <th className="py-2 pr-2">Target Component</th>
                    <th className="py-2 pr-2">Diagnosis Status</th>
                    <th className="py-2 pr-2">Safety</th>
                    <th className="py-2">Evidence Tally</th>
                  </tr>
                </thead>
                <tbody>
                  {matches.map((m, idx) => (
                    <tr key={`${m.rule_id}-${idx}`} className="border-b border-surface-container/60 align-top">
                      <td className="py-2 pr-2 font-bold text-on-surface">{idx + 1}</td>
                      <td className="py-2 pr-2">
                        <strong className="text-on-surface">{m.possible_fault || m.title}</strong>
                        <div className="text-[11px] text-on-surface-variant">{m.explanation}</div>
                      </td>
                      <td className="py-2 pr-2 font-medium text-on-surface">
                        {m.affected_component || "Subsystem Assembly"}
                        {m.subsystem && <span className="block text-[10px] text-outline">{m.subsystem}</span>}
                      </td>
                      <td className="py-2 pr-2">
                        <StatusBadge match={m} />
                      </td>
                      <td className="py-2 pr-2">
                        <SafetyBadge level={m.safety_level} />
                      </td>
                      <td className="py-2 font-mono text-[11px] text-outline">
                        {m.evidence_tally?.matched_count || 0} / {m.evidence_tally?.total_rule_symptoms || 0} symptoms
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Section 4: Physical Verification Checks Table (Tier A) */}
        <section className="border border-surface-container p-space-md rounded-xl">
          <h2 className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider mb-1">
            4. TIER A: PHYSICAL COMPONENT VERIFICATION PROCEDURES
          </h2>
          <p className="text-[11px] text-on-surface-variant mb-2">
            Technicians must verify these physical checks in order. Compare observed bench readings against normal ranges before servicing components:
          </p>
          {matches.map((m, idx) => (
            <div key={`${m.rule_id}-checks-${idx}`} className="mb-3 last:mb-0">
              <div className="font-headline-sm text-[12px] font-bold text-on-surface mb-1 flex items-center justify-between">
                <span>
                  <span className="text-primary font-mono">{m.rule_id}:</span> {m.possible_fault || m.title} ({m.affected_component})
                </span>
                {m.required_expertise && (
                  <span className="text-[10px] text-outline font-normal">Expertise: {m.required_expertise}</span>
                )}
              </div>
              <RecommendedChecks steps={m.diagnosis_steps} />
            </div>
          ))}
        </section>

        {/* Section 5: Structured Maintenance Actions & Directives (Tier B) */}
        <section className="bg-surface-container-low p-space-md rounded-xl border border-surface-container space-y-3">
          <h2 className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider">
            5. TIER B: STRUCTURED MAINTENANCE DIRECTIVES &amp; REPAIR GUIDANCE
          </h2>
          <div className="space-y-3">
            {matches.map((m) => {
              const act = m.maintenance_actions;
              return (
                <div key={`maint-${m.rule_id}`} className="p-3 rounded-lg bg-surface-container-lowest border border-surface-container space-y-2">
                  <div className="flex items-center justify-between border-b border-surface-container pb-1 text-xs">
                    <strong className="text-primary">{m.possible_fault || m.title}</strong>
                    <span className="text-outline text-[11px]">Component: {m.affected_component}</span>
                  </div>

                  {act ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px]">
                      <div>
                        <strong className="text-on-surface uppercase block text-[10px]">Corrective Action:</strong>
                        <p className="text-on-surface-variant">{act.corrective_action}</p>
                      </div>
                      <div>
                        <strong className="text-on-surface uppercase block text-[10px]">Preventive Measure:</strong>
                        <p className="text-on-surface-variant">{act.preventive_measure}</p>
                      </div>
                      {act.replacement_criteria && (
                        <div className="md:col-span-2">
                          <strong className="text-on-surface uppercase block text-[10px]">Replacement Criteria:</strong>
                          <p className="text-on-surface-variant">{act.replacement_criteria}</p>
                        </div>
                      )}
                      {act.do_not_replace_warning && (
                        <div className="md:col-span-2 p-1.5 rounded bg-red-50 text-red-900 border border-red-200">
                          <strong className="uppercase block text-[10px] text-red-950 font-bold">
                            Do-Not-Replace Directive (Avoid Premature Replacement):
                          </strong>
                          <p>{act.do_not_replace_warning}</p>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-[12px] text-on-surface-variant">{m.suggested_next_steps}</p>
                  )}
                </div>
              );
            })}
          </div>

          <div className="pt-1 text-[11px] text-on-surface-variant leading-relaxed">
            <strong>Escalation Threshold:</strong> If fault verification reveals high-voltage bus faults,
            internal brake master cylinder bypass, engine oil metallic debris, or fuel leaks, cease testing
            and escalate to an ASE Master Technician.
          </div>
        </section>

        {/* Section 6: Sequential Decision Flowchart */}
        {results?.related_flowchart && (
          <section className="border border-surface-container p-space-md rounded-xl">
            <h2 className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider mb-2">
              6. SEQUENTIAL DECISION TREE (EXPERT FLOWCHART PATHWAY)
            </h2>
            <FlowchartPanel flowchart={results.related_flowchart} defaultOpen={false} />
          </section>
        )}

        {/* Section 7: Academic Propositional Rule Trace Appendix (For Examiners) */}
        <section className="border border-surface-container p-space-md rounded-xl bg-surface-container-low/50">
          <h2 className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider mb-2">
            7. ACADEMIC EVALUATION APPENDIX: FORMAL PROPOSITIONAL LOGIC RULES (CLO 1 / CLO 3)
          </h2>
          <div className="space-y-1.5 font-mono text-[11px]">
            {matches.map((m, idx) => (
              <div key={idx} className="p-2 rounded bg-surface-container-lowest border border-outline-variant/20 break-words">
                <span className="text-primary font-bold">{m.rule_id}:</span> {m.rule_expression}
              </div>
            ))}
          </div>
        </section>

        {/* Technician Notes & Sign-off Block */}
        <section className="border border-surface-container p-space-md rounded-xl grid grid-cols-1 md:grid-cols-2 gap-space-md">
          <div>
            <label
              htmlFor="technician-notes-input"
              className="font-label-caps text-[10px] text-on-surface-variant uppercase font-bold block mb-1"
            >
              Diagnostic Notes &amp; Shop Observations
            </label>
            <textarea
              id="technician-notes-input"
              className="w-full rounded-lg bg-surface-container-low p-2 text-[12px] border border-surface-container-high focus:outline-none focus:ring-1 focus:ring-primary min-h-[70px] no-print"
              placeholder="Record multimeter readings, visual inspection findings, or technician remarks…"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
            {notes && (
              <p className="hidden print:block text-[12px] whitespace-pre-wrap p-2 border border-surface-container rounded">
                {notes}
              </p>
            )}
          </div>

          <div className="flex flex-col justify-between border-t md:border-t-0 md:border-l border-surface-container-high pt-2 md:pt-0 md:pl-space-md text-[11px]">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-on-surface-variant block text-[10px] uppercase">Service Bay</span>
                <span className="font-mono text-on-surface">Bay 04 — Mechanical Triage</span>
              </div>
              <div>
                <span className="text-on-surface-variant block text-[10px] uppercase">Status</span>
                <span className="font-semibold text-primary">Pending Physical Verification</span>
              </div>
            </div>
            <div className="border-t border-surface-container pt-3 mt-3 flex justify-between items-end">
              <div>
                <div className="h-6 w-36 border-b border-dashed border-on-surface-variant mb-1" />
                <span className="text-[10px] text-on-surface-variant uppercase">
                  Inspecting Technician Signature
                </span>
              </div>
              <div>
                <div className="h-6 w-24 border-b border-dashed border-on-surface-variant mb-1" />
                <span className="text-[10px] text-on-surface-variant uppercase">Date</span>
              </div>
            </div>
          </div>
        </section>

        {/* Legal & Academic Attribution Footer */}
        <footer className="border-t border-surface-container pt-space-sm text-[10px] text-on-surface-variant space-y-1">
          <p>
            <strong>Diagnostic Disclaimer:</strong> This dossier is produced by Auto Sage, a deterministic rule-based
            Knowledge-Based System (KBS), solely for university educational triage and workshop guidance. Fault candidates
            are unconfirmed hypotheses requiring physical inspection. Auto Sage provides no mechanical warranties.
          </p>
          <p>
            <strong>Academic Provenance:</strong> Knowledge rules grounded in the open-access dataset:{" "}
            <em>Automotive Faults Dataset for Diagnostic and Maintenance Systems</em> (Obike, Peter &amp; Obot, Okure),
            Zenodo DOI:{" "}
            <a
              className="text-primary underline"
              href="https://doi.org/10.5281/zenodo.15626055"
              target="_blank"
              rel="noreferrer"
            >
              10.5281/zenodo.15626055
            </a>
            , licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
          </p>
        </footer>
      </article>
    </div>
  );
}
