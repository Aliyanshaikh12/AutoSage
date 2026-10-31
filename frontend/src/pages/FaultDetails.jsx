import { FlowchartPanel, RecommendedChecks, RuleEvidence, SafetyBadge, StatusBadge } from "../components/Evidence.jsx";

export default function FaultDetails({ match, onBackToResults, onViewRepairGuide }) {
  if (!match) {
    return (
      <div className="p-space-lg max-w-xl mx-auto text-center space-y-4">
        <p className="font-body-md text-on-surface-variant">No fault candidate is currently selected.</p>
        <button
          type="button"
          className="px-4 py-2 bg-primary text-on-primary rounded-lg text-xs font-semibold"
          onClick={onBackToResults}
        >
          Back to Results
        </button>
      </div>
    );
  }

  const consequences = [
    "Continued operation may induce progressive thermal or mechanical stress on adjacent assemblies.",
    "Compromised vehicle handling, degraded braking efficiency, or elevated tailpipe emissions.",
    "Potential escalation into high-cost catastrophic component failure if left uninspected.",
  ];

  return (
    <div className="w-full px-4 sm:px-6 lg:px-8 py-6 flex flex-col gap-6 max-w-[1300px] mx-auto pb-28 animate-fade-in">
      {/* Top Header Card */}
      <section className="bg-surface-container-lowest rounded-2xl shadow-sm p-4 sm:p-6 border border-surface-container space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-surface-container">
          <button
            type="button"
            onClick={onBackToResults}
            className="flex items-center gap-1.5 text-xs text-secondary hover:text-primary transition-colors font-semibold self-start"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            <span>Back to Diagnosis Results</span>
          </button>

          <div className="flex items-center gap-2">
            {match.safety_level && <SafetyBadge level={match.safety_level} />}
            <StatusBadge match={match} />
          </div>
        </div>

        <div>
          {match.rule_id && (
            <span className="font-mono text-[11px] text-on-surface-variant font-medium bg-surface-container px-2 py-0.5 rounded">
              Ref: {match.rule_id.replace(/^RULE_/, "")}
            </span>
          )}
          <h1 className="text-2xl sm:text-3xl font-extrabold text-on-surface tracking-tight mt-1">
            {match.possible_fault || match.title}
          </h1>
          <p className="text-xs sm:text-sm text-on-surface-variant mt-1">
            Subsystem: <strong>{match.subsystem || match.category_name}</strong> &bull; Target Component:{" "}
            <strong>{match.affected_component || "Subsystem Assembly"}</strong>
          </p>
        </div>
      </section>

      {/* Main Grid: Left 7 cols (Evidence & Tests), Right 5 cols (Guidance & Safety) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-start">
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          {/* Component & Evidence Dossier */}
          <Card title="Component & Diagnostic Evidence Breakdown">
            <RuleEvidence match={match} />
          </Card>

          {/* Diagnostic Verification Bench Checks */}
          <Card title="Recommended Bench Verification Checks (Dataset Procedures)">
            <p className="text-xs text-on-surface-variant mb-2">
              Physical tests that must be conducted to corroborate or refute this fault candidate before disassembling components:
            </p>
            <RecommendedChecks steps={match.diagnosis_steps} />
          </Card>

          {/* Flowchart if available */}
          {match.related_flowchart && (
            <Card title="Associated Diagnostic Decision Tree">
              <FlowchartPanel flowchart={match.related_flowchart} />
            </Card>
          )}
        </div>

        <div className="lg:col-span-5 flex flex-col gap-space-md">
          {/* Why it was suggested */}
          <Card title="Diagnostic Explanation">
            <p className="text-xs text-on-surface leading-relaxed">
              {match.explanation || "Isolated based on matching observed vehicle operating conditions."}
            </p>
          </Card>

          {/* Root causes */}
          <Card title="Known Root Causes & Findings to Look For">
            <ul className="space-y-1.5 text-xs text-on-surface">
              {(Array.isArray(match.possible_causes) && match.possible_causes.length > 0
                ? match.possible_causes
                : [
                    "Mechanical wear or fatigue of internal moving components.",
                    "Loss of hydraulic or pneumatic seal pressure.",
                    "Electrical contact corrosion or sensor signal drift.",
                  ]
              ).map((cause, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="material-symbols-outlined text-primary text-[16px] shrink-0 mt-0.5">check_circle</span>
                  <span>{cause}</span>
                </li>
              ))}
            </ul>
          </Card>

          {/* Consequences */}
          <Card title="Possible Consequences If Unaddressed">
            <ul className="space-y-1 text-xs text-on-surface-variant">
              {consequences.map((c, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="material-symbols-outlined text-amber-700 text-[14px] shrink-0 mt-0.5">warning</span>
                  <span>{c}</span>
                </li>
              ))}
            </ul>
          </Card>

          {/* Safety & Action Button */}
          <Card title="Safety Advisory & Workshop Guidance">
            <p className="text-xs text-on-surface-variant leading-relaxed">
              {match.safety_warning || "Adhere to standard workshop safety procedures. Never replace components without bench verification."}
            </p>
            <div className="pt-2 border-t border-surface-container mt-2">
              <button
                type="button"
                onClick={onViewRepairGuide}
                className="w-full py-2.5 px-3 rounded-lg bg-primary-container text-on-primary font-headline-sm text-xs font-semibold hover:bg-primary transition-all shadow-sm flex items-center justify-center gap-1.5"
              >
                <span className="material-symbols-outlined text-[16px]">build_circle</span>
                <span>Open Full Repair &amp; Mitigation Guide</span>
              </button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

function Card({ title, children }) {
  return (
    <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md border border-surface-container">
      <h2 className="font-label-caps text-[11px] text-on-surface-variant mb-space-sm uppercase font-bold tracking-wider">
        {title}
      </h2>
      {children}
    </section>
  );
}
