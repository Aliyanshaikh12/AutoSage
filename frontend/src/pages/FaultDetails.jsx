import { FlowchartPanel, RecommendedChecks, RuleEvidence, StatusBadge } from "../components/Evidence.jsx";

export default function FaultDetails({ match, onBackToResults, onViewRepairGuide }) {
  if (!match) {
    return (
      <div className="p-space-lg max-w-3xl mx-auto text-center">
        <p className="font-body-md text-on-surface-variant">No fault is selected.</p>
        <button type="button" className="mt-space-md text-primary underline" onClick={onBackToResults}>Back to results</button>
      </div>
    );
  }
  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1200px] mx-auto">
      <div>
        <button type="button" onClick={onBackToResults} className="flex items-center gap-1 text-body-sm text-secondary hover:text-primary">
          <span className="material-symbols-outlined text-[16px]">arrow_back</span>Back to results
        </button>
        <div className="flex flex-wrap items-center gap-space-xs mt-space-xs">
          <StatusBadge match={match} />
          <span className="font-mono text-[11px] text-on-surface-variant">{match.rule_id}</span>
          {match.category_name && <span className="text-[12px] text-on-surface-variant">· {match.category_name}</span>}
        </div>
        <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight">{match.title || match.possible_fault}</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          <Card title="Knowledge-base rule">
            <RuleEvidence match={match} />
          </Card>
          <Card title="Inspection procedure (from dataset)">
            <RecommendedChecks steps={match.diagnosis_steps} />
          </Card>
          {match.related_flowchart && (
            <Card title="Related diagnostic flowchart">
              <FlowchartPanel flowchart={match.related_flowchart} />
            </Card>
          )}
        </div>
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          <Card title="Why it matched">
            <p className="text-body-sm text-on-surface">{match.explanation}</p>
          </Card>
          {Array.isArray(match.possible_causes) && match.possible_causes.length > 0 && (
            <Card title="Fault findings to look for">
              <ul className="list-disc pl-5 text-[13px] text-on-surface space-y-1">
                {match.possible_causes.map((c) => <li key={c}>{c}</li>)}
              </ul>
            </Card>
          )}
          {match.suggested_next_steps && (
            <Card title="Suggested next steps">
              <p className="text-[13px] text-on-surface">{match.suggested_next_steps}</p>
            </Card>
          )}
          <Card title="Safety">
            <p className="text-[13px] text-on-surface-variant">{match.safety_warning || "Follow standard workshop safety precautions."}</p>
            <button type="button" onClick={onViewRepairGuide} className="mt-space-sm w-full py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-headline-sm text-body-sm">
              Open safety guide
            </button>
          </Card>
        </div>
      </div>
    </div>
  );
}

function Card({ title, children }) {
  return (
    <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
      <h2 className="font-label-caps text-label-caps text-on-surface-variant mb-space-sm uppercase">{title}</h2>
      {children}
    </section>
  );
}
