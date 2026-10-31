import { useEffect, useMemo, useState } from "react";
import { getKnowledgeBase } from "../services/api.js";
import { Chip, FlowchartPanel, MaintenancePlanPanel, RecommendedChecks, SafetyBadge } from "../components/Evidence.jsx";

const TABS = [
  ["rules", "Fault Rules"],
  ["flowcharts", "Flowcharts"],
  ["provenance", "Dataset & Exclusions"],
];

export default function KnowledgeBase({ initialQuery = "", onStartDiagnosis }) {
  const [kb, setKb] = useState(null);
  const [error, setError] = useState("");
  const [query, setQuery] = useState(initialQuery);
  const [cat, setCat] = useState("all");
  const [tab, setTab] = useState("rules");
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => setQuery(initialQuery), [initialQuery]);
  useEffect(() => {
    let active = true;
    getKnowledgeBase()
      .then((d) => active && setKb(d))
      .catch((e) => active && setError(e.message));
    return () => {
      active = false;
    };
  }, []);

  const rules = useMemo(() => {
    if (!kb) return [];
    const q = query.trim().toLowerCase();
    return kb.rules.filter(
      (r) =>
        (cat === "all" || r.category_id === cat) &&
        (!q || [r.title, r.rule_id, r.subcategory, ...r.symptom_labels].join(" ").toLowerCase().includes(q))
    );
  }, [kb, query, cat]);
  const selected = rules.find((r) => r.rule_id === selectedId) || rules[0] || null;
  const fcById = Object.fromEntries((kb?.flowcharts || []).map((f) => [f.flowchart_id, f]));

  if (error) return <div className="p-space-lg"><p className="rounded-lg bg-error-container text-on-error-container p-space-md">{error}</p></div>;
  if (!kb) return <div className="p-space-lg text-on-surface-variant">Loading knowledge base…</div>;
  const ds = kb.dataset;

  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1600px] mx-auto">
      <div>
        <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight uppercase">Knowledge Base Explorer</h1>
        <p className="font-body-sm text-body-sm text-on-surface-variant">
          {ds.integrated_rule_count} fault rules · {ds.category_count} categories · {ds.canonical_symptom_count} symptoms · {ds.flowchart_count} flowcharts
        </p>
      </div>
      <div className="flex flex-wrap gap-space-xs">
        {TABS.map(([id, label]) => (
          <button key={id} type="button" onClick={() => setTab(id)} className={`px-space-md py-1.5 rounded-full text-[13px] font-headline-sm ${tab === id ? "bg-primary-container text-on-primary" : "bg-surface-container text-on-surface"}`}>
            {label}
          </button>
        ))}
      </div>

      {tab === "rules" && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-start">
          <section className="lg:col-span-5 bg-surface-container-lowest rounded-xl shadow-sm p-space-md flex flex-col gap-space-sm">
            <input className="h-9 px-3 rounded-full bg-surface-container-low text-body-sm focus:outline-none focus:ring-2 focus:ring-primary/20" placeholder="Search faults, symptoms, or rule IDs…" value={query} onChange={(e) => setQuery(e.target.value)} aria-label="Search rules" />
            <select className="h-9 px-3 rounded-lg bg-surface-container-low text-body-sm" value={cat} onChange={(e) => setCat(e.target.value)} aria-label="Filter by category">
              <option value="all">All categories</option>
              {kb.categories.map((c) => <option key={c.category_id} value={c.category_id}>{c.name} ({c.rule_count})</option>)}
            </select>
            <p className="text-[12px] text-on-surface-variant">{rules.length} rule(s)</p>
            <ul className="flex flex-col gap-1 max-h-[60vh] overflow-y-auto">
              {rules.map((r) => (
                <li key={r.rule_id}>
                  <button type="button" onClick={() => setSelectedId(r.rule_id)} className={`w-full text-left rounded-lg px-space-sm py-1.5 ${selected?.rule_id === r.rule_id ? "bg-primary-fixed" : "hover:bg-surface-container-low"}`}>
                    <div className="text-[13px] text-on-surface font-medium">{r.title}</div>
                    <div className="text-[11px] text-on-surface-variant font-mono">{r.rule_id} · {r.logic_mode}</div>
                  </button>
                </li>
              ))}
            </ul>
          </section>
          <section className="lg:col-span-7 bg-surface-container-lowest rounded-xl shadow-sm p-space-md flex flex-col gap-space-sm lg:sticky lg:top-20">
            {!selected ? (
              <p className="text-on-surface-variant">No rules match your search.</p>
            ) : (
              <>
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-surface-container pb-2">
                  <div className="font-mono text-[11px] text-on-surface-variant">{selected.rule_id} · {selected.category_name}</div>
                  {selected.safety_level && <SafetyBadge level={selected.safety_level} />}
                </div>

                <h2 className="font-headline-md text-headline-md text-on-surface">{selected.title}</h2>

                {selected.affected_component && (
                  <div className="p-2.5 rounded-lg bg-surface-container-low border border-surface-container text-xs flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary text-[18px]">build</span>
                    <span>Component: <strong>{selected.affected_component}</strong> ({selected.subsystem || selected.category_name})</span>
                  </div>
                )}

                <div className="rounded-lg bg-inverse-surface text-inverse-on-surface p-space-sm font-mono text-[12px] break-words">
                  {selected.rule_expression}
                </div>

                <div>
                  <span className="font-label-caps text-[10px] text-on-surface-variant uppercase font-bold tracking-wider block mb-1">
                    Canonical Symptom Conditions
                  </span>
                  <div className="flex flex-wrap gap-1.5">{selected.symptom_labels.map((l) => <Chip key={l}>{l}</Chip>)}</div>
                </div>

                {selected.diagnostic_questions && selected.diagnostic_questions.length > 0 && (
                  <div className="p-2.5 rounded-lg bg-primary/5 border border-primary/20 text-xs space-y-1">
                    <span className="font-label-caps text-[10px] text-primary uppercase font-bold tracking-wider block">
                      Targeted Follow-Up Diagnostic Inquiry
                    </span>
                    {selected.diagnostic_questions.map((q, idx) => (
                      <div key={idx} className="text-on-surface">
                        &bull; <strong>{q.question}</strong>
                        {q.context && <span className="block text-[11px] text-on-surface-variant italic">{q.context}</span>}
                      </div>
                    ))}
                  </div>
                )}

                <div>
                  <span className="font-label-caps text-[10px] text-primary uppercase font-bold tracking-wider block mb-1">
                    Physical Verification Checks (Tier A)
                  </span>
                  <RecommendedChecks steps={selected.diagnosis_steps} />
                </div>

                {selected.maintenance_actions && (
                  <div>
                    <span className="font-label-caps text-[10px] text-on-surface-variant uppercase font-bold tracking-wider block mb-1">
                      Maintenance Directives (Tier B)
                    </span>
                    <MaintenancePlanPanel match={selected} />
                  </div>
                )}

                <p className="text-[11px] text-on-surface-variant pt-2 border-t border-surface-container">
                  Source records: {selected.source_reference.source_record_ids.join(", ")} (raw category: {selected.source_reference.raw_categories.join(", ")} → {selected.source_reference.raw_subcategory})
                </p>
                {selected.related_flowchart_id && <FlowchartPanel flowchart={fcById[selected.related_flowchart_id]} />}
                <button type="button" onClick={() => onStartDiagnosis(selected.category_id)} className="self-start mt-space-xs inline-flex items-center gap-1.5 px-space-md py-2 rounded-lg bg-primary-container text-on-primary font-headline-sm text-[13px]">
                  <span className="material-symbols-outlined text-[18px]">troubleshoot</span>Diagnose in this category
                </button>
              </>
            )}
          </section>
        </div>
      )}

      {tab === "flowcharts" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-space-lg">
          {kb.flowcharts.map((f) => (
            <section key={f.flowchart_id} className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
              <FlowchartPanel flowchart={f} defaultOpen />
              <p className="text-[11px] text-on-surface-variant mt-space-xs">Branches shown in the image: {f.top_level_branches.join(", ")}</p>
            </section>
          ))}
        </div>
      )}

      {tab === "provenance" && (
        <div className="flex flex-col gap-space-md">
          <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md text-[13px] text-on-surface flex flex-col gap-1">
            <h2 className="font-headline-sm text-headline-sm">{ds.title}</h2>
            <p>{ds.authors.join(", ")}</p>
            <p>DOI: <a className="text-primary underline" href={ds.url} target="_blank" rel="noreferrer">{ds.doi}</a> · {ds.license}</p>
            <p className="text-on-surface-variant">{ds.related_publication}</p>
            <p className="text-on-surface-variant">
              {ds.raw_record_count} raw records → {ds.integrated_rule_count} rules ({ds.merged_duplicate_count} duplicate merged, {ds.excluded_record_count} excluded).
            </p>
          </section>
          <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
            <h2 className="font-label-caps text-label-caps text-on-surface-variant mb-space-sm">RECORDS NOT USED AS RULES</h2>
            <ul className="flex flex-col gap-space-sm">
              {kb.excluded_source_records.map((x) => (
                <li key={x.source_record_id} className="text-[12px]">
                  <span className="font-mono">{x.source_record_id}</span> — {x.raw_category} → {x.raw_subcategory}
                  <div className="text-on-surface-variant">{x.reason}</div>
                </li>
              ))}
            </ul>
          </section>
        </div>
      )}
    </div>
  );
}
