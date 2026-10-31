import { useEffect, useMemo, useState } from "react";
import { getKnowledgeBase } from "../services/api.js";
import { formatNumber, formatRelativeTime } from "../stitch/dom.js";
import { readHistoryRecords } from "../utils/historyStorage.js";

const HOTSPOTS = [
  { id: "CAT_ENGINE", icon: "engineering", top: "30%", left: "30%" },
  { id: "CAT_COOLING", icon: "thermostat", top: "40%", left: "16%" },
  { id: "CAT_ELECTRICAL", icon: "bolt", top: "26%", left: "48%" },
  { id: "CAT_TRANSMISSION", icon: "settings", top: "52%", left: "52%" },
  { id: "CAT_BRAKES", icon: "disc_full", top: "66%", left: "28%" },
];

export default function Dashboard({
  onStartDiagnosis,
  onOpenHistoryRecord,
  onOpenKnowledgeBase,
  onOpenHistory,
  historyCount = 0,
}) {
  const [kb, setKb] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    getKnowledgeBase()
      .then((data) => active && (setKb(data), setError("")))
      .catch((err) => active && setError(err.message))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  const history = useMemo(() => readHistoryRecords().records, [historyCount]);
  const latest = history[0] || null;
  const ds = kb?.dataset;
  const categories = kb?.categories || [];
  const catById = Object.fromEntries(categories.map((c) => [c.category_id, c]));

  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1720px] mx-auto">
      <section className="w-full bg-surface-container-lowest rounded-xl shadow-sm p-space-lg md:p-space-xl relative overflow-hidden">
        <div className="absolute inset-0 pointer-events-none opacity-35 bg-[radial-gradient(#c3c6d7_1px,transparent_1px)] [background-size:20px_20px]" />
        <div className="absolute right-0 top-0 w-2/3 h-full bg-gradient-to-l from-primary/5 via-transparent to-transparent pointer-events-none" />
        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-space-xl items-center min-h-[420px]">
          <div className="lg:col-span-5 flex flex-col justify-center gap-space-md">
            <span className="inline-flex self-start items-center gap-1.5 px-space-sm py-1 rounded-full bg-surface-container-low text-on-surface-variant font-label-caps text-label-caps">
              <span className={`inline-flex rounded-full h-2 w-2 ${error ? "bg-error" : "bg-primary"}`} />
              {loading ? "LOADING KNOWLEDGE BASE" : error ? "BACKEND UNAVAILABLE" : "KNOWLEDGE BASE READY"}
            </span>
            <div>
              <h1 className="font-display-hero text-display-hero text-on-surface tracking-tight uppercase select-none">
                Diagnostics
              </h1>
              <p className="font-body-md text-body-md text-on-surface-variant mt-space-xs max-w-md">
                Select the problems your vehicle is experiencing to identify possible faults
                using our automotive knowledge base.
              </p>
            </div>
            <div className="flex items-center gap-space-xs flex-wrap">
              {["Choose category", "Select symptoms", "Review possible faults"].map((label, i) => (
                <div key={label} className="flex items-center gap-space-xs">
                  <span className="flex items-center gap-1.5 px-space-sm py-1.5 rounded-lg bg-surface-container-low text-on-surface-variant font-body-sm text-body-sm">
                    <span className="flex items-center justify-center w-4 h-4 rounded-full text-[10px] font-bold bg-primary text-on-primary">
                      {i + 1}
                    </span>
                    {label}
                  </span>
                  {i < 2 && <span className="material-symbols-outlined text-outline-variant text-[16px]">chevron_right</span>}
                </div>
              ))}
            </div>
            <div className="flex flex-wrap items-center gap-space-md pt-space-xs">
              <button
                className="inline-flex items-center gap-space-sm px-space-lg py-3 rounded-full bg-primary-container text-on-primary font-headline-sm text-headline-sm hover:bg-primary shadow-[0_10px_25px_-5px_rgba(37,99,235,0.35)] transition-all hover:-translate-y-0.5"
                type="button"
                onClick={() => onStartDiagnosis(null)}
              >
                Start Diagnosis
                <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
              </button>
            </div>
            {error && (
              <p className="rounded-lg bg-error-container text-on-error-container p-space-sm font-body-sm text-body-sm">
                {error}
              </p>
            )}
          </div>

          <div className="lg:col-span-7 relative flex items-center justify-center min-h-[300px]">
            <div className="relative w-full max-w-2xl">
              <div className="absolute w-4/5 h-24 bg-gradient-to-r from-primary/10 via-primary/20 to-primary/10 blur-2xl rounded-full -bottom-2 left-[10%] pointer-events-none" />
              <img
                className="relative z-10 w-full object-contain max-h-[340px] drop-shadow-[0_20px_30px_rgba(0,23,75,0.12)] select-none"
                src="/images/vehicle-hero.jpg"
                alt="Vehicle studio view"
              />
              {HOTSPOTS.map((h) => {
                const cat = catById[h.id];
                if (!cat) return null;
                return (
                  <div key={h.id} className="absolute z-20 group" style={{ top: h.top, left: h.left }}>
                    <button
                      aria-label={`Diagnose ${cat.name}`}
                      className="relative flex items-center justify-center w-8 h-8 rounded-full bg-primary text-on-primary shadow-lg hover:scale-110 transition-transform"
                      type="button"
                      onClick={() => onStartDiagnosis(h.id)}
                    >
                      <span className="material-symbols-outlined text-[18px]">{h.icon}</span>
                    </button>
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block pointer-events-none">
                      <div className="px-space-sm py-1 rounded-lg bg-inverse-surface text-inverse-on-surface shadow-xl whitespace-nowrap text-center">
                        <div className="font-label-caps text-label-caps uppercase text-primary-fixed">{cat.short_name}</div>
                        <div className="font-body-sm text-body-sm">{cat.rule_count} fault rules</div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-space-md">
        <StatCard icon="category" title="PROBLEM CATEGORIES" value={ds ? formatNumber(ds.category_count) : "—"}>
          Engine, electrical, brakes, cooling, transmission, emissions, AC and steering/tires.
        </StatCard>
        <StatCard icon="rule" title="FAULT RULES" value={ds ? formatNumber(ds.integrated_rule_count) : "—"} onClick={onOpenKnowledgeBase} action="Browse rules">
          IF–THEN rules built from {ds ? ds.raw_record_count : "the"} dataset records,
          plus {ds ? ds.flowchart_count : ""} diagnostic flowcharts.
        </StatCard>
        <StatCard
          icon="history"
          title="RECENT DIAGNOSIS"
          value={latest ? latest.categoryName || "Saved session" : "None yet"}
          onClick={latest ? () => onOpenHistoryRecord(latest) : onOpenHistory}
          action={latest ? "Review" : "Open history"}
        >
          {latest
            ? `${formatRelativeTime(latest.timestamp)} · ${(latest.symptomLabels || []).length} symptom(s)`
            : "Your diagnoses are saved in this browser only."}
        </StatCard>
        <StatCard icon="account_tree" title="HOW IT WORKS" value="Rule engine">
          Deterministic rule matching. No machine learning and no confidence scores. Results are
          possible faults that need a physical inspection.
        </StatCard>
      </div>

      {ds && (
        <p className="font-body-sm text-[12px] text-on-surface-variant">
          Knowledge source: {ds.title} (Obike &amp; Obot), DOI{" "}
          <a className="text-primary underline" href={ds.url} target="_blank" rel="noreferrer">
            {ds.doi}
          </a>
          , {ds.license}.
        </p>
      )}
    </div>
  );
}

function StatCard({ icon, title, value, children, onClick, action }) {
  return (
    <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md flex flex-col justify-between">
      <div>
        <div className="flex items-center gap-space-xs mb-space-sm">
          <span className="material-symbols-outlined text-primary text-[20px]">{icon}</span>
          <h2 className="font-label-caps text-label-caps text-on-surface-variant">{title}</h2>
        </div>
        <div className="font-headline-md text-headline-md text-on-surface truncate">{value}</div>
        <p className="font-body-sm text-[12px] text-on-surface-variant mt-1">{children}</p>
      </div>
      {onClick && (
        <button
          className="mt-space-md w-full inline-flex items-center justify-center gap-1 px-space-sm py-space-sm rounded-lg bg-surface-container text-on-surface font-headline-sm text-[12px] hover:bg-surface-container-high transition-all"
          type="button"
          onClick={onClick}
        >
          {action}
          <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
        </button>
      )}
    </section>
  );
}
