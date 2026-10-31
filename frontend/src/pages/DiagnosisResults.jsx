import { useState } from "react";
import Stepper from "../components/Stepper.jsx";
import {
  FlowchartPanel,
  MaintenancePlanPanel,
  RecommendedChecks,
  RuleEvidence,
  SafetyBadge,
  StatusBadge,
} from "../components/Evidence.jsx";
import { formatDateTime, vehicleLabel, vehicleSecondary } from "../stitch/dom.js";

const NO_MATCH_TEXT =
  "No matching fault was identified for your reported symptoms in the current diagnostic knowledge base. Review your selected symptoms or consult a certified automotive technician.";

export default function DiagnosisResults({
  results,
  vehicleInfo,
  reviewedTimestamp,
  onModifySymptoms,
  onNewDiagnosis,
  onOpenFaultDetails,
  onViewRepairGuide,
  onViewReport,
}) {
  const [showComparison, setShowComparison] = useState(false);
  const matches = Array.isArray(results?.matches) ? results.matches : [];
  const cross = Array.isArray(results?.cross_category_matches) ? results.cross_category_matches : [];
  const isNoMatch = results?.status === "no_match" || (matches.length === 0 && cross.length === 0);
  const symptomLabels = (results?.selected_symptom_details || []).map((s) => s.label || s.text);
  const isLegacy =
    !results?.category_id?.startsWith?.("CAT_") ||
    matches.some((m) => !m.rule_expression && !m.diagnosis_steps);

  const nextTest = results?.next_recommended_test;
  const comparison = Array.isArray(results?.candidates_comparison) ? results.candidates_comparison : [];

  return (
    <div className="w-full px-4 sm:px-6 lg:px-8 py-6 flex flex-col gap-6 max-w-[1450px] mx-auto pb-32 animate-fade-in">
      <Stepper
        currentStep={4}
        onStepClick={(page) => {
          if (page === "symptoms" || page === "vehicle" || page === "questions") onModifySymptoms?.();
          else if (page === "report") onViewReport?.();
        }}
      />

      {/* Header & Session Profile Card */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg flex flex-col gap-space-md border border-surface-container">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-space-md">
          <div className="space-y-1">
            <div className="flex items-center gap-space-xs flex-wrap">
              <span className="font-label-caps text-label-caps text-primary uppercase font-bold tracking-wider">
                {reviewedTimestamp
                  ? `Saved Session · ${formatDateTime(reviewedTimestamp)}`
                  : `Active Session · ${formatDateTime(new Date())}`}
              </span>
              <span className="text-outline-variant">|</span>
              <span className="font-mono text-[11px] text-on-surface-variant">
                ID: {results?.report_id || "AS-SESSION"}
              </span>
              {results?.overall_safety_level && (
                <>
                  <span className="text-outline-variant">|</span>
                  <SafetyBadge level={results.overall_safety_level} />
                </>
              )}
            </div>
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight uppercase">
              {isNoMatch
                ? "No Matching Fault Identified"
                : `${matches.length + cross.length} Potential Fault${
                    matches.length + cross.length === 1 ? "" : "s"
                  } Identified`}
            </h1>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              Subsystem Under Diagnosis: <strong className="text-on-surface">{results?.category_name || "—"}</strong>
            </p>
          </div>

          <div className="flex flex-wrap gap-space-sm no-print self-start md:self-auto">
            <Btn icon="edit" onClick={onModifySymptoms}>
              Modify Symptoms
            </Btn>
            {!isNoMatch && (
              <Btn icon="description" primary onClick={onViewReport}>
                Generate Diagnostic Report
              </Btn>
            )}
            <Btn icon="add" onClick={onNewDiagnosis}>
              New Diagnosis
            </Btn>
          </div>
        </div>

        {/* Vehicle & Input Metadata Strip */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-space-md p-space-sm rounded-xl bg-surface-container-low border border-surface-container-high">
          <div className="md:col-span-4 flex items-start gap-space-sm">
            <span className="material-symbols-outlined text-primary text-[22px] mt-0.5">
              directions_car
            </span>
            <div>
              <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider block">
                Vehicle Profile
              </span>
              <span className="font-headline-sm text-[13px] text-on-surface font-semibold block">
                {vehicleLabel(vehicleInfo)}
              </span>
              <span className="font-body-sm text-[11px] text-on-surface-variant block">
                {vehicleSecondary(vehicleInfo)}
              </span>
            </div>
          </div>

          <div className="md:col-span-8 flex flex-col gap-1 border-t md:border-t-0 md:border-l border-surface-container-high pt-space-xs md:pt-0 md:pl-space-md">
            <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider">
              Selected Observed Symptoms ({symptomLabels.length})
            </span>
            <div className="flex flex-wrap gap-1.5">
              {symptomLabels.map((l) => (
                <span
                  key={l}
                  className="px-2.5 py-0.5 rounded-full bg-surface-container text-on-surface text-[12px] font-medium"
                >
                  {l}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Recommended Physical Verification Banner */}
      {nextTest && (
        <section className="bg-primary/5 border border-primary/20 rounded-xl p-space-md flex flex-col md:flex-row items-start md:items-center justify-between gap-space-md">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0">
              <span className="material-symbols-outlined text-2xl">biotech</span>
            </div>
            <div>
              <span className="font-label-caps text-[10px] text-primary uppercase font-bold tracking-wider block">
                Primary Recommended Verification Test
              </span>
              <h2 className="text-sm font-bold text-on-surface">
                {nextTest.test_name} &bull; Target Component: {nextTest.target_component}
              </h2>
              <p className="text-xs text-on-surface-variant mt-0.5">
                <strong>Procedure:</strong> {nextTest.procedure}
              </p>
            </div>
          </div>
          <div className="text-xs shrink-0 bg-surface-container-lowest px-3 py-2 rounded-lg border border-outline-variant/20">
            <span className="text-error font-medium block">Abnormal: {nextTest.abnormal_criteria}</span>
            <span className="text-emerald-700 font-medium block">Normal: {nextTest.normal_criteria}</span>
          </div>
        </section>
      )}

      {/* Important Diagnostic Notice */}
      <div className="rounded-xl bg-amber-50 text-amber-900 p-space-md flex items-start gap-space-sm border border-amber-200">
        <span className="material-symbols-outlined text-amber-700 text-[22px] shrink-0 mt-0.5">
          warning
        </span>
        <div className="text-[13px] leading-relaxed">
          <strong>Important Diagnostic Notice:</strong> The issues listed below are potential causes based on your reported vehicle symptoms. Do not replace any parts before performing physical bench tests to confirm the fault. {results?.safety_note}
        </div>
      </div>

      {isLegacy && (
        <p className="rounded-lg bg-surface-container-low p-space-sm font-body-sm text-[12px] text-on-surface-variant">
          Historical diagnostic session: some structured metadata fields have been reconstructed.
        </p>
      )}

      {/* No Match State */}
      {isNoMatch ? (
        <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-xl text-center flex flex-col items-center gap-space-md border border-surface-container">
          <div className="w-16 h-16 rounded-full bg-surface-container flex items-center justify-center">
            <span className="material-symbols-outlined text-[36px] text-outline">search_off</span>
          </div>
          <div className="space-y-1">
            <h2 className="font-headline-md text-headline-md text-on-surface">
              No Matching Fault Identified
            </h2>
            <p className="font-body-md text-body-md text-on-surface-variant max-w-xl mx-auto">
              {NO_MATCH_TEXT}
            </p>
          </div>
          {results?.no_match_reason && (
            <div className="p-space-sm rounded-lg bg-surface-container-low text-on-surface text-[13px] max-w-lg">
              <strong>Diagnostic Note:</strong> {results.no_match_reason}
            </div>
          )}
          <div className="flex gap-space-sm pt-space-xs">
            <Btn icon="edit" onClick={onModifySymptoms}>
              Change Selected Symptoms
            </Btn>
            <Btn icon="add" primary onClick={onNewDiagnosis}>
              Start New Diagnosis
            </Btn>
          </div>
        </section>
      ) : (
        <>
          {/* Comparison Bar if multiple candidates exist */}
          {comparison.length > 1 && (
            <div className="flex items-center justify-between gap-space-sm no-print">
              <span className="text-xs font-medium text-on-surface-variant">
                {matches.length} potential issue{matches.length === 1 ? "" : "s"} identified for review
              </span>
              <button
                type="button"
                onClick={() => setShowComparison(!showComparison)}
                className="px-3 py-1.5 rounded-lg text-[12px] font-semibold bg-surface-container hover:bg-surface-container-high text-on-surface transition-colors flex items-center gap-1.5"
              >
                <span className="material-symbols-outlined text-[16px]">compare_arrows</span>
                <span>{showComparison ? "Hide Comparison" : "Compare Candidates Side-by-Side"}</span>
              </button>
            </div>
          )}

          {/* Multi-Candidate Side-by-Side Comparison Table */}
          {showComparison && comparison.length > 0 && (
            <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md border border-primary/20 overflow-x-auto">
              <div className="flex items-center gap-2 mb-3">
                <span className="material-symbols-outlined text-primary text-[20px]">table_chart</span>
                <h2 className="text-sm font-bold text-on-surface uppercase tracking-wide">
                  Differential Diagnostic Comparison
                </h2>
              </div>
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-surface-container text-on-surface-variant font-label-caps uppercase">
                    <th className="py-2 pr-3">Potential Fault</th>
                    <th className="py-2 pr-3">Affected Component</th>
                    <th className="py-2 pr-3">Status</th>
                    <th className="py-2 pr-3">Safety Risk</th>
                    <th className="py-2 pr-3">Supporting Evidence</th>
                    <th className="py-2">Primary Verification Test</th>
                  </tr>
                </thead>
                <tbody>
                  {comparison.map((c, idx) => (
                    <tr key={idx} className="border-b border-surface-container hover:bg-surface-container-low transition-colors">
                      <td className="py-2.5 pr-3 font-semibold text-on-surface">{c.fault}</td>
                      <td className="py-2.5 pr-3 text-on-surface-variant">{c.component}</td>
                      <td className="py-2.5 pr-3">
                        <span className="font-mono text-[11px] font-medium">{c.status}</span>
                      </td>
                      <td className="py-2.5 pr-3">
                        <SafetyBadge level={c.safety_level} />
                      </td>
                      <td className="py-2.5 pr-3 font-medium text-outline">
                        {c.evidence_tally?.matched_count || 0} matching symptom(s)
                      </td>
                      <td className="py-2.5 text-on-surface-variant">
                        {c.key_discriminating_check?.step || "Visual & bench check"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}

          {/* Fault Candidate Cards */}
          {matches.map((m, i) => (
            <CandidateCard
              key={m.rule_id || i}
              match={m}
              rank={i + 1}
              onDetails={() => onOpenFaultDetails(m)}
              onGuide={() => onViewRepairGuide(m)}
              onModifySymptoms={onModifySymptoms}
              onViewReport={onViewReport}
            />
          ))}

          {/* Cross-Category Section */}
          {cross.length > 0 && (
            <section className="space-y-space-md">
              <div className="border-t border-surface-container pt-space-md">
                <h2 className="font-headline-sm text-headline-sm text-on-surface font-semibold">
                  Related Cross-Subsystem Findings ({cross.length})
                </h2>
                <p className="font-body-sm text-[12px] text-on-surface-variant">
                  Your selected symptoms are also associated with related faults in adjacent vehicle subsystems:
                </p>
              </div>
              {cross.map((m) => (
                <CandidateCard
                  key={`x-${m.rule_id}`}
                  match={m}
                  onDetails={() => onOpenFaultDetails(m)}
                  onGuide={() => onViewRepairGuide(m)}
                  onModifySymptoms={onModifySymptoms}
                  onViewReport={onViewReport}
                />
              ))}
            </section>
          )}
        </>
      )}

      {/* Flowchart Pathway Section */}
      {results?.related_flowchart && (
        <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container">
          <div className="flex items-center gap-space-xs mb-space-sm">
            <span className="material-symbols-outlined text-primary text-[22px]">account_tree</span>
            <h2 className="font-headline-sm text-headline-sm text-on-surface font-semibold">
              Diagnostic Decision Tree Pathway
            </h2>
          </div>
          <FlowchartPanel flowchart={results.related_flowchart} defaultOpen={false} />
        </section>
      )}

      {/* Floating Bottom Action Strip */}
      {!isNoMatch && (
        <div className="fixed bottom-16 md:bottom-0 left-0 md:left-20 right-0 bg-surface-container-lowest/95 backdrop-blur shadow-[0_-1px_8px_rgba(0,0,0,0.06)] px-space-md md:px-space-lg py-space-sm z-30 no-print flex items-center justify-between">
          <span className="font-body-sm text-[12px] text-on-surface-variant hidden sm:inline">
            Diagnosis analysis completed. Review the suggested inspection steps before proceeding.
          </span>
          <div className="flex items-center gap-space-sm ml-auto">
            <Btn icon="edit" onClick={onModifySymptoms}>
              Modify Symptoms
            </Btn>
            <Btn icon="description" primary onClick={onViewReport}>
              Generate Diagnostic Report
            </Btn>
          </div>
        </div>
      )}
    </div>
  );
}

function CandidateCard({ match, rank, onDetails, onGuide, onModifySymptoms, onViewReport }) {
  const refCode = match.rule_id ? match.rule_id.replace(/^RULE_/, "") : null;

  return (
    <article className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
      {/* Left Column: Fault Identification & Supporting Evidence (7 cols) */}
      <div className="lg:col-span-7 flex flex-col gap-space-sm">
        {/* Header Badges Strip */}
        <div className="flex flex-wrap items-center gap-space-xs">
          {rank && (
            <span className="font-label-caps text-label-caps px-2 py-0.5 rounded bg-surface-container text-on-surface font-bold">
              #{rank}
            </span>
          )}
          <StatusBadge match={match} />
          {match.safety_level && <SafetyBadge level={match.safety_level} />}
          {refCode && (
            <span className="font-mono text-[11px] text-on-surface-variant font-medium">
              Ref: {refCode}
            </span>
          )}
          {match.category_name && (
            <span className="text-[11px] text-on-surface-variant">&bull; {match.category_name}</span>
          )}
        </div>

        {/* Fault Name */}
        <h3 className="font-headline-md text-headline-md text-on-surface font-bold">
          {match.possible_fault || match.title}
        </h3>

        {/* Natural English Explanation */}
        <div>
          <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider block mb-0.5 font-bold">
            Why This Problem May Be Occurring
          </span>
          <p className="font-body-sm text-body-sm text-on-surface leading-relaxed">
            {match.explanation ||
              `Your reported symptoms suggest a potential issue with the ${match.affected_component || "vehicle system"}. Follow the inspection checks to confirm.`}
          </p>
        </div>

        {/* Supporting Evidence & Symptoms Breakdown */}
        <div>
          <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider block mb-1 font-bold">
            Diagnostic Evidence
          </span>
          <RuleEvidence match={match} />
        </div>
      </div>

      {/* Right Column: Recommended Checks & Directives (5 cols) */}
      <div className="lg:col-span-5 flex flex-col gap-space-sm border-t lg:border-t-0 lg:border-l border-surface-container pt-space-sm lg:pt-0 lg:pl-space-md">
        {/* Tier A Checks */}
        <div>
          <div className="flex items-center justify-between mb-1">
            <span className="font-label-caps text-[10px] text-primary uppercase font-bold tracking-wider">
              Recommended Inspection Checks (Tier A)
            </span>
            <span className="text-[11px] text-on-surface-variant font-mono">
              {match.diagnosis_steps?.length || 0} step(s)
            </span>
          </div>
          <RecommendedChecks steps={match.diagnosis_steps} />
        </div>

        {/* Tier B Directives */}
        <div>
          <span className="font-label-caps text-[10px] text-on-surface-variant uppercase font-bold tracking-wider block mb-1">
            Possible Findings &amp; Next Steps (Tier B Directives)
          </span>
          {match.maintenance_actions ? (
            <MaintenancePlanPanel match={match} />
          ) : (
            <p className="font-body-sm text-[12px] text-on-surface leading-relaxed">
              {match.suggested_next_steps ||
                "Do not replace components before verifying abnormal test findings with physical bench checks. Follow workshop service manual procedures."}
            </p>
          )}
        </div>

        {/* Safety Warning if present */}
        {match.safety_warning && (
          <div className="rounded-lg bg-error-container/50 text-on-error-container p-space-xs text-[11px] flex items-start gap-1.5">
            <span className="material-symbols-outlined text-[16px] text-error shrink-0 mt-0.5">
              shield
            </span>
            <span>{match.safety_warning}</span>
          </div>
        )}

        {/* 4 Action Buttons */}
        <div className="flex flex-wrap gap-2 mt-auto pt-space-xs no-print">
          <Btn icon="build_circle" primary onClick={onGuide}>
            Repair &amp; Mitigation Guide
          </Btn>
          <Btn icon="info" onClick={onDetails}>
            Component Details
          </Btn>
          {onModifySymptoms && (
            <Btn icon="edit" onClick={onModifySymptoms}>
              Modify Symptoms
            </Btn>
          )}
          {onViewReport && (
            <Btn icon="description" onClick={onViewReport}>
              Generate Report
            </Btn>
          )}
        </div>
      </div>
    </article>
  );
}

function Btn({ icon, children, onClick, primary }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer btn-press-fx ${
        primary
          ? "bg-primary text-on-primary hover:bg-primary-container shadow-sm hover:shadow"
          : "bg-surface-container text-on-surface hover:bg-surface-container-high border border-surface-container-highest"
      }`}
    >
      <span className="material-symbols-outlined text-[17px]">{icon}</span>
      <span>{children}</span>
    </button>
  );
}
