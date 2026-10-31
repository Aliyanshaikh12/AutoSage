import { useState } from "react";
import { flowchartUrl } from "../services/api.js";

export function Chip({ children, tone = "primary" }) {
  const tones = {
    primary: "bg-primary-fixed text-on-primary-fixed",
    muted: "bg-surface-container text-on-surface-variant",
    warn: "bg-amber-100 text-amber-900 border border-amber-300",
    error: "bg-error-container text-on-error-container border border-error/30",
    success: "bg-emerald-100 text-emerald-900 border border-emerald-300",
  };
  return <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-medium ${tones[tone]}`}>{children}</span>;
}

export function SafetyBadge({ level }) {
  const lev = String(level || "Medium").toUpperCase();
  if (lev === "CRITICAL") {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-label-caps text-[11px] font-bold uppercase bg-red-100 text-red-800 border border-red-300">
        <span className="material-symbols-outlined text-[13px] text-red-600">emergency</span>
        Critical Safety
      </span>
    );
  }
  if (lev === "HIGH") {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-label-caps text-[11px] font-bold uppercase bg-amber-100 text-amber-900 border border-amber-300">
        <span className="material-symbols-outlined text-[13px] text-amber-700">warning</span>
        High Risk
      </span>
    );
  }
  if (lev === "LOW") {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-label-caps text-[11px] font-medium uppercase bg-slate-100 text-slate-700 border border-slate-300">
        <span className="material-symbols-outlined text-[13px] text-slate-500">info</span>
        Low Risk
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-label-caps text-[11px] font-medium uppercase bg-yellow-50 text-yellow-800 border border-yellow-300">
      <span className="material-symbols-outlined text-[13px] text-yellow-600">report_problem</span>
      Moderate Risk
    </span>
  );
}

export function StatusBadge({ match }) {
  const status = match?.diagnosis_status || (match?.match_type === "partial" ? "Requires Further Inspection" : "Suspected Fault");
  
  if (status.includes("Corroborated")) {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-label-caps text-[11px] font-bold uppercase bg-emerald-100 text-emerald-900 border border-emerald-300">
        <span className="material-symbols-outlined text-[14px] text-emerald-700">verified</span>
        Corroborated Hypothesis
      </span>
    );
  }
  if (status.includes("Not Supported")) {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-label-caps text-[11px] font-medium uppercase bg-rose-50 text-rose-800 border border-rose-300">
        <span className="material-symbols-outlined text-[14px] text-rose-600">cancel</span>
        Contradicted by Findings
      </span>
    );
  }
  if (status.includes("Requires Further") || match?.match_type === "partial") {
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-label-caps text-[11px] font-medium uppercase bg-amber-100 text-amber-900 border border-amber-300">
        <span className="material-symbols-outlined text-[14px] text-amber-700">hourglass_top</span>
        Partial Match · Needs Inspection
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-label-caps text-[11px] font-bold uppercase bg-primary-fixed text-on-primary-fixed border border-primary/20">
      <span className="material-symbols-outlined text-[14px] text-primary">rule</span>
      Suspected Fault · Unconfirmed
    </span>
  );
}

export function RuleEvidence({ match }) {
  if (!match) return null;
  const ref = match.source_reference || {};
  const supporting = Array.isArray(match.supporting_evidence) ? match.supporting_evidence : [];
  const missing = Array.isArray(match.missing_evidence) ? match.missing_evidence : [];
  const contradictory = Array.isArray(match.contradictory_evidence) ? match.contradictory_evidence : [];

  return (
    <div className="flex flex-col gap-space-sm">
      {/* Affected Component Spotlight */}
      {match.affected_component && (
        <div className="p-space-sm rounded-lg bg-surface-container-low border border-surface-container-high flex items-start gap-2.5">
          <span className="material-symbols-outlined text-primary text-[20px] mt-0.5">build</span>
          <div>
            <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider block">
              Primary Affected Component &amp; Subsystem
            </span>
            <span className="text-[13px] font-semibold text-on-surface">
              {match.affected_component}
            </span>
            {match.subsystem && (
              <span className="text-[11px] text-outline block">Subsystem: {match.subsystem}</span>
            )}
          </div>
        </div>
      )}

      {/* Structured Evidence Breakdown (CLO 1 & CLO 2) */}
      <div className="space-y-2">
        {/* Supporting Evidence */}
        {supporting.length > 0 && (
          <div>
            <span className="font-label-caps text-[10px] text-emerald-800 font-bold uppercase tracking-wider block mb-1 flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px] text-emerald-600">check_circle</span>
              Supporting Evidence ({supporting.length})
            </span>
            <div className="flex flex-wrap gap-1.5">
              {supporting.map((ev, i) => (
                <Chip key={i} tone="success">
                  {ev.label || ev.description || ev.question}
                </Chip>
              ))}
            </div>
          </div>
        )}

        {/* Missing / Unverified Evidence */}
        {missing.length > 0 && (
          <div>
            <span className="font-label-caps text-[10px] text-amber-900 font-bold uppercase tracking-wider block mb-1 flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px] text-amber-700">help</span>
              Unconfirmed / Missing Evidence ({missing.length})
            </span>
            <div className="flex flex-wrap gap-1.5">
              {missing.map((ev, i) => (
                <Chip key={i} tone="warn">
                  {ev.label || ev.description || ev.question}
                </Chip>
              ))}
            </div>
          </div>
        )}

        {/* Contradictory Evidence */}
        {contradictory.length > 0 && (
          <div>
            <span className="font-label-caps text-[10px] text-error font-bold uppercase tracking-wider block mb-1 flex items-center gap-1">
              <span className="material-symbols-outlined text-[14px] text-error">cancel</span>
              Contradictory Evidence ({contradictory.length})
            </span>
            <div className="flex flex-wrap gap-1.5">
              {contradictory.map((ev, i) => (
                <Chip key={i} tone="error">
                  {ev.label || ev.description || ev.question}
                </Chip>
              ))}
            </div>
          </div>
        )}

        {/* Unaccounted Symptoms */}
        {Array.isArray(match.unaccounted_symptom_labels) && match.unaccounted_symptom_labels.length > 0 && (
          <div>
            <span className="font-label-caps text-[10px] text-on-surface-variant font-medium uppercase tracking-wider block mb-1">
              Selected but Unrelated to This Component ({match.unaccounted_symptom_labels.length})
            </span>
            <div className="flex flex-wrap gap-1.5">
              {match.unaccounted_symptom_labels.map((l) => (
                <Chip key={l} tone="muted">
                  {l}
                </Chip>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Collapsible Technical Propositional Logic Block (CLO 1 / CLO 3 Academic Evaluation) */}
      <details className="group border border-outline-variant/30 rounded-lg overflow-hidden bg-surface-container-lowest mt-1">
        <summary className="cursor-pointer px-3 py-2 bg-surface-container-low text-on-surface font-label-caps text-[11px] font-semibold flex items-center justify-between hover:bg-surface-container transition-colors">
          <span className="flex items-center gap-1.5">
            <span className="material-symbols-outlined text-[16px] text-primary">code</span>
            Formal Propositional Rule &amp; Inference Trace (CLO 1 / CLO 3)
          </span>
          <span className="material-symbols-outlined text-[16px] group-open:rotate-180 transition-transform">
            expand_more
          </span>
        </summary>
        <div className="p-3 space-y-2 bg-inverse-surface text-inverse-on-surface font-mono text-[11px]">
          <div>
            <span className="text-secondary-fixed block text-[10px] uppercase font-bold tracking-wider">
              Logical Rule Expression:
            </span>
            <code className="text-primary-fixed break-words block mt-0.5">
              {match.rule_expression || `Rule ${match.rule_id}`}
            </code>
          </div>
          <div className="grid grid-cols-2 gap-2 pt-1 border-t border-inverse-on-surface/20 text-[10px]">
            <div>
              <span className="text-outline-variant">Logic Mode:</span>{" "}
              <span className="text-inverse-on-surface font-bold">{match.logic_mode || "ALL"}</span>
            </div>
            <div>
              <span className="text-outline-variant">Match Status:</span>{" "}
              <span className="text-inverse-on-surface font-bold">{match.match_type}</span>
            </div>
          </div>
          {ref.doi && (
            <div className="pt-1 border-t border-inverse-on-surface/20 text-[10px] text-inverse-on-surface/80">
              Corpus Origin: {ref.source_file} · DOI: {ref.doi} ({ref.license})
            </div>
          )}
        </div>
      </details>
    </div>
  );
}

function Row({ label, children }) {
  return (
    <div>
      <div className="font-label-caps text-label-caps text-on-surface-variant mb-1">{label}</div>
      <div className="flex flex-wrap gap-1.5">{children}</div>
    </div>
  );
}

export function RecommendedChecks({ steps }) {
  if (!Array.isArray(steps) || steps.length === 0) {
    return <p className="font-body-sm text-[12px] text-on-surface-variant">No inspection steps are stored for this rule.</p>;
  }
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-[12px]">
        <thead>
          <tr className="text-on-surface-variant font-label-caps text-label-caps">
            <th className="py-1 pr-2">#</th>
            <th className="py-1 pr-2">Check</th>
            <th className="py-1 pr-2">Fault finding</th>
            <th className="py-1">Normal finding</th>
          </tr>
        </thead>
        <tbody>
          {steps.map((s, i) => (
            <tr key={i} className="border-t border-surface-container">
              <td className="py-1.5 pr-2 align-top font-mono font-bold text-on-surface-variant">{s.step_number || i + 1}</td>
              <td className="py-1.5 pr-2 align-top text-on-surface">{s.step}</td>
              <td className="py-1.5 pr-2 align-top text-error font-medium">{s.abnormal_result}</td>
              <td className="py-1.5 align-top text-emerald-700">{s.normal_result}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function MaintenancePlanPanel({ match }) {
  const m = match?.maintenance_actions;
  if (!m) return null;

  return (
    <div className="space-y-3 pt-2">
      {/* Corrective & Preventive Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-[12px]">
        <div className="p-2.5 rounded-lg bg-surface-container-low border border-surface-container-high">
          <span className="font-label-caps text-[10px] text-primary uppercase font-bold tracking-wider block mb-1 flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px]">handyman</span>
            Corrective Action
          </span>
          <p className="text-on-surface leading-snug">{m.corrective_action}</p>
        </div>

        <div className="p-2.5 rounded-lg bg-surface-container-low border border-surface-container-high">
          <span className="font-label-caps text-[10px] text-secondary uppercase font-bold tracking-wider block mb-1 flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px]">published_with_changes</span>
            Preventive Measure
          </span>
          <p className="text-on-surface leading-snug">{m.preventive_measure}</p>
        </div>
      </div>

      {/* Replacement Criteria */}
      {m.replacement_criteria && (
        <div className="p-2.5 rounded-lg bg-surface-container-low border border-surface-container-high text-[12px]">
          <span className="font-label-caps text-[10px] text-on-surface-variant uppercase font-bold tracking-wider block mb-1 flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px]">find_replace</span>
            Replacement Criteria
          </span>
          <p className="text-on-surface leading-snug">{m.replacement_criteria}</p>
        </div>
      )}

      {/* Do Not Replace Warning (Anti-Mistake Directives) */}
      {m.do_not_replace_warning && (
        <div className="p-2.5 rounded-lg bg-red-50 text-red-950 border border-red-200 text-[11px] flex items-start gap-2">
          <span className="material-symbols-outlined text-red-700 text-[18px] shrink-0 mt-0.5">
            cancel
          </span>
          <div>
            <strong className="block text-[11px] text-red-900 uppercase tracking-wide">
              Do-Not-Replace Directive (Avoid Premature Replacement):
            </strong>
            <p className="leading-snug mt-0.5 text-red-900">{m.do_not_replace_warning}</p>
          </div>
        </div>
      )}

      {/* Required Tools & Expertise */}
      <div className="flex flex-wrap items-center justify-between gap-2 pt-1 text-[11px] text-on-surface-variant border-t border-surface-container">
        {match.required_expertise && (
          <span className="flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px] text-primary">engineering</span>
            <span>Expertise: <strong>{match.required_expertise}</strong></span>
          </span>
        )}
        {Array.isArray(match.required_tools) && match.required_tools.length > 0 && (
          <span className="flex items-center gap-1">
            <span className="material-symbols-outlined text-[14px] text-secondary">home_repair_service</span>
            <span>Tools: <strong>{match.required_tools.join(", ")}</strong></span>
          </span>
        )}
      </div>
    </div>
  );
}

export function FlowchartPanel({ flowchart, defaultOpen = false }) {
  const [showImage, setShowImage] = useState(defaultOpen);
  if (!flowchart) return null;
  return (
    <div className="rounded-xl bg-surface-container-low p-space-sm flex flex-col gap-space-sm">
      <div className="flex items-center justify-between gap-space-sm">
        <div className="flex items-center gap-space-xs">
          <span className="material-symbols-outlined text-primary text-[18px]">account_tree</span>
          <span className="font-headline-sm text-[13px] text-on-surface">{flowchart.title}</span>
        </div>
        <button type="button" className="text-[12px] text-primary hover:underline no-print" onClick={() => setShowImage((v) => !v)}>
          {showImage ? "Hide diagram" : "View diagram"}
        </button>
      </div>
      <ol className="flex flex-col gap-1 text-[12px]">
        {(flowchart.decision_steps || []).map((s) => (
          <li key={s.order} className="flex gap-space-xs">
            <span className="font-bold text-primary">{s.order}.</span>
            <span>
              <span className="text-on-surface font-medium">{s.check}</span>
              <span className="text-on-surface-variant"> — {s.if_abnormal}; {s.if_normal}</span>
            </span>
          </li>
        ))}
      </ol>
      <p className="font-body-sm text-[11px] text-on-surface-variant">{flowchart.coverage_note}</p>
      {showImage && (
        <img
          className="w-full rounded-lg bg-white"
          src={flowchartUrl(flowchart.flowchart_id)}
          alt={flowchart.title}
          loading="lazy"
        />
      )}
    </div>
  );
}
