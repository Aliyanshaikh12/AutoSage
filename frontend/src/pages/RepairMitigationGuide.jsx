import { useState } from "react";
import { RecommendedChecks, SafetyBadge, StatusBadge } from "../components/Evidence.jsx";

export default function RepairMitigationGuide({
  match,
  diagnosisResult,
  onBack,
  onStartReEvaluation,
}) {
  const [recordedRepairs, setRecordedRepairs] = useState({});
  const [repairNotes, setRepairNotes] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  const activeMatch = match || diagnosisResult?.matches?.[0] || null;

  if (!activeMatch) {
    return (
      <div className="w-full px-space-md py-space-xl max-w-xl mx-auto text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-surface-container flex items-center justify-center mx-auto text-outline">
          <span className="material-symbols-outlined text-2xl">handyman</span>
        </div>
        <h2 className="text-lg font-bold text-on-surface">No Fault Candidate Selected</h2>
        <p className="text-xs text-on-surface-variant">
          Select a fault candidate from your diagnosis results to review its specific repair and mitigation protocols.
        </p>
        <button
          type="button"
          onClick={onBack}
          className="px-4 py-2 bg-primary text-on-primary rounded-lg text-xs font-semibold hover:bg-primary/90"
        >
          Back to Diagnosis Results
        </button>
      </div>
    );
  }

  const mActions = activeMatch.maintenance_actions || {};
  const isRecorded = Boolean(recordedRepairs[activeMatch.rule_id]);

  const handleToggleRecord = () => {
    setRecordedRepairs((prev) => ({
      ...prev,
      [activeMatch.rule_id]: !prev[activeMatch.rule_id],
    }));
    setStatusMessage(
      !isRecorded
        ? "Repair action logged locally. Remember: software logging does NOT constitute physical bench verification."
        : "Repair record removed."
    );
    setTimeout(() => setStatusMessage(""), 4500);
  };

  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1300px] mx-auto pb-24">
      {/* Top Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm bg-surface-container-lowest rounded-xl p-space-sm shadow-sm border border-surface-container no-print">
        <button
          type="button"
          onClick={onBack}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-headline-sm text-xs transition-colors self-start sm:self-auto"
        >
          <span className="material-symbols-outlined text-[16px]">arrow_back</span>
          <span>Back to Diagnosis</span>
        </button>

        <div className="flex items-center gap-2">
          {activeMatch.safety_level && <SafetyBadge level={activeMatch.safety_level} />}
          <StatusBadge match={activeMatch} />
        </div>
      </div>

      {statusMessage && (
        <div className="p-3 rounded-xl bg-primary/10 border border-primary/20 text-xs text-primary font-medium flex items-center gap-2">
          <span className="material-symbols-outlined text-[18px]">info</span>
          <span>{statusMessage}</span>
        </div>
      )}

      {/* Section 1: Fault Overview */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-surface-container pb-2">
          <div>
            <span className="font-label-caps text-[10px] text-primary uppercase font-bold tracking-wider block">
              1. Fault Candidate Overview
            </span>
            <h1 className="font-headline-lg text-xl md:text-2xl font-extrabold text-on-surface tracking-tight mt-0.5">
              {activeMatch.possible_fault || activeMatch.title}
            </h1>
          </div>
          <span className="font-mono text-xs text-on-surface-variant bg-surface-container px-2.5 py-1 rounded">
            {activeMatch.rule_id}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md pt-1">
          <div className="p-3 rounded-lg bg-surface-container-low border border-surface-container">
            <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider block mb-0.5">
              Target Component &amp; Subsystem
            </span>
            <p className="text-sm font-semibold text-on-surface">
              {activeMatch.affected_component || "Subsystem Assembly"}
            </p>
            <span className="text-xs text-outline block mt-0.5">
              Subsystem: {activeMatch.subsystem || activeMatch.category_name || "Automotive Chassis"}
            </span>
          </div>

          <div className="p-3 rounded-lg bg-surface-container-low border border-surface-container">
            <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider block mb-0.5">
              Diagnostic Explanation
            </span>
            <p className="text-xs text-on-surface leading-relaxed">
              {activeMatch.explanation || "Isolated based on matching observed vehicle operating conditions."}
            </p>
          </div>
        </div>
      </section>

      {/* Section 2: Possible Causes */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container space-y-2">
        <h2 className="font-label-caps text-xs text-primary uppercase font-bold tracking-wider flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px]">psychology</span>
          <span>2. Supported Root Causes (Knowledge Base Corpus)</span>
        </h2>
        <p className="text-xs text-on-surface-variant">
          Mechanical failure modes and environmental triggers documented in the research knowledge base:
        </p>

        <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 pt-1 text-xs text-on-surface">
          {(Array.isArray(activeMatch.possible_causes) && activeMatch.possible_causes.length > 0
            ? activeMatch.possible_causes
            : [
                "Component mechanical wear or internal seal deterioration over service life.",
                "Thermal degradation, excessive operating friction, or fluid contamination.",
                "Loss of electrical reference ground, pin fretting corrosion, or low supply voltage.",
                "Associated vacuum supply leak or restricted auxiliary fluid channel.",
              ]
          ).map((cause, idx) => (
            <li key={idx} className="p-2.5 rounded-lg bg-surface-container-low flex items-start gap-2 border border-surface-container">
              <span className="material-symbols-outlined text-[16px] text-primary shrink-0 mt-0.5">check_circle</span>
              <span className="leading-snug">{cause}</span>
            </li>
          ))}
        </ul>
      </section>

      {/* Section 3: Diagnostic Verification Tests */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container space-y-3">
        <div className="flex items-center justify-between border-b border-surface-container pb-2">
          <h2 className="font-label-caps text-xs text-primary uppercase font-bold tracking-wider flex items-center gap-1.5">
            <span className="material-symbols-outlined text-[16px]">biotech</span>
            <span>3. Tier A: Physical Diagnostic Verification Tests</span>
          </h2>
          <span className="text-xs text-on-surface-variant">
            {activeMatch.diagnosis_steps?.length || 0} Test Step(s)
          </span>
        </div>
        <p className="text-xs text-on-surface-variant">
          Technicians must perform these quantitative checks before disassembling or replacing parts. Compare observed measurements against standard OEM thresholds:
        </p>
        <RecommendedChecks steps={activeMatch.diagnosis_steps} />
      </section>

      {/* Section 4: Corrective Actions & Maintenance Directives */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container space-y-3">
        <h2 className="font-label-caps text-xs text-primary uppercase font-bold tracking-wider flex items-center gap-1.5 border-b border-surface-container pb-2">
          <span className="material-symbols-outlined text-[16px]">build_circle</span>
          <span>4. Tier B: Corrective Actions &amp; Objective Discard Directives</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-space-sm text-xs">
          <div className="p-3 rounded-lg bg-surface-container-low border border-surface-container">
            <span className="font-bold text-primary uppercase text-[10px] block mb-1 flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">handyman</span>
              Corrective Action
            </span>
            <p className="text-on-surface leading-relaxed">
              {mActions.corrective_action || "Follow OEM service manual instructions to service or adjust this component."}
            </p>
          </div>

          <div className="p-3 rounded-lg bg-surface-container-low border border-surface-container">
            <span className="font-bold text-secondary uppercase text-[10px] block mb-1 flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px]">published_with_changes</span>
              Preventive Maintenance Measure
            </span>
            <p className="text-on-surface leading-relaxed">
              {mActions.preventive_measure || "Inspect component integrity during regular scheduled vehicle servicing."}
            </p>
          </div>

          {mActions.replacement_criteria && (
            <div className="p-3 rounded-lg bg-surface-container-low border border-surface-container md:col-span-2">
              <span className="font-bold text-on-surface-variant uppercase text-[10px] block mb-1 flex items-center gap-1">
                <span className="material-symbols-outlined text-[14px]">find_replace</span>
                Objective Replacement Criteria (Replace ONLY When Justified)
              </span>
              <p className="text-on-surface leading-relaxed font-medium">
                {mActions.replacement_criteria}
              </p>
            </div>
          )}

          {mActions.do_not_replace_warning && (
            <div className="p-3 rounded-lg bg-red-50 text-red-950 border border-red-200 md:col-span-2">
              <div className="flex items-start gap-2">
                <span className="material-symbols-outlined text-red-700 text-[18px] shrink-0 mt-0.5">cancel</span>
                <div>
                  <strong className="block text-[11px] text-red-900 uppercase tracking-wide font-bold">
                    Critical Anti-Mistake Directive (Do Not Prematurely Replace):
                  </strong>
                  <p className="leading-relaxed mt-0.5 text-red-900 text-xs">
                    {mActions.do_not_replace_warning}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Tools and Expertise */}
        <div className="p-3 rounded-lg bg-surface-container-low border border-surface-container flex flex-wrap items-center justify-between gap-3 text-xs">
          <div>
            <span className="text-outline uppercase text-[10px] font-bold block">Recommended Expertise:</span>
            <strong className="text-on-surface">{activeMatch.required_expertise || "Certified Automotive Technician"}</strong>
          </div>
          <div>
            <span className="text-outline uppercase text-[10px] font-bold block">Required Tools:</span>
            <span className="text-on-surface">
              {Array.isArray(activeMatch.required_tools) && activeMatch.required_tools.length > 0
                ? activeMatch.required_tools.join(", ")
                : "Standard hand tools & digital multimeter"}
            </span>
          </div>
        </div>
      </section>

      {/* Section 5: Safety Precautions */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container space-y-2">
        <h2 className="font-label-caps text-xs text-primary uppercase font-bold tracking-wider flex items-center gap-1.5">
          <span className="material-symbols-outlined text-[16px]">shield</span>
          <span>5. Safety Precautions &amp; Workshop Escalation</span>
        </h2>
        <div className="p-3 rounded-lg bg-amber-50 text-amber-950 border border-amber-200 text-xs leading-relaxed space-y-1">
          <p>
            <strong>Warning:</strong> {activeMatch.safety_warning || "Standard automotive workshop safety guidelines apply."}
          </p>
          <p>
            <strong>Escalation Threshold:</strong> If fault verification reveals high-voltage wiring breaches, severe hydraulic brake pressure drops, or fuel line leaks, cease all DIY testing immediately and arrange a certified flatbed tow truck.
          </p>
        </div>
      </section>

      {/* Section 6: Repair Outcome & Re-Evaluation */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md md:p-space-lg border border-surface-container space-y-3">
        <h2 className="font-label-caps text-xs text-primary uppercase font-bold tracking-wider flex items-center gap-1.5 border-b border-surface-container pb-2">
          <span className="material-symbols-outlined text-[16px]">task</span>
          <span>6. Repair Outcome &amp; Diagnostic Re-Evaluation</span>
        </h2>
        <p className="text-xs text-on-surface-variant">
          After performing corrective maintenance, record your service actions below for workshop audit history. Then conduct a follow-up diagnosis to verify that reported symptoms have resolved:
        </p>

        <div className="space-y-2">
          <label htmlFor="repair-action-input" className="text-[11px] font-bold text-on-surface block">
            Technician Service Remarks:
          </label>
          <textarea
            id="repair-action-input"
            className="w-full rounded-lg bg-surface-container-low p-2 text-xs border border-surface-container-high focus:outline-none focus:ring-1 focus:ring-primary min-h-[60px]"
            placeholder="Record replaced seal part numbers, calibrated torque values, or multimeter post-repair readings..."
            value={repairNotes}
            onChange={(e) => setRepairNotes(e.target.value)}
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-surface-container">
          <button
            type="button"
            onClick={handleToggleRecord}
            className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              isRecorded
                ? "bg-emerald-100 text-emerald-900 border border-emerald-300"
                : "bg-surface-container text-on-surface hover:bg-surface-container-high"
            }`}
          >
            <span className="material-symbols-outlined text-[16px]">
              {isRecorded ? "check_circle" : "check_box_outline_blank"}
            </span>
            <span>{isRecorded ? "Repair Action Recorded" : "Mark Repair Performed"}</span>
          </button>

          <button
            type="button"
            onClick={onStartReEvaluation}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-on-primary text-xs font-semibold hover:bg-primary/90 transition-all shadow-sm"
          >
            <span>Run Follow-Up Verification Diagnosis</span>
            <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
          </button>
        </div>

        <div className="p-2 rounded bg-surface-container-low text-[10px] text-outline">
          * Note: Recording a repair in Auto Sage stores an administrative audit marker in your local browser session. In accordance with KBS validation principles, software markers do not automatically certify mechanical physical compliance.
        </div>
      </section>
    </div>
  );
}
