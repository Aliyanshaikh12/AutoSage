import { useEffect, useMemo, useState } from "react";
import { getKnowledgeBase } from "../services/api.js";
import { formatNumber, formatRelativeTime, vehicleLabel } from "../stitch/dom.js";
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
  onOpenVehicle,
  onOpenHistoryRecord,
  onOpenHistory,
  onOpenSafetyGuide,
  vehicleInfo,
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
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1720px] mx-auto pb-24">
      {/* Hero Welcome Section */}
      <section className="w-full bg-surface-container-lowest rounded-xl shadow-sm p-space-lg md:p-space-xl relative overflow-hidden border border-surface-container">
        <div className="absolute inset-0 pointer-events-none opacity-35 bg-[radial-gradient(#c3c6d7_1px,transparent_1px)] [background-size:20px_20px]" />
        <div className="absolute right-0 top-0 w-2/3 h-full bg-gradient-to-l from-primary/5 via-transparent to-transparent pointer-events-none" />
        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-space-xl items-center min-h-[420px]">
          <div className="lg:col-span-5 flex flex-col justify-center gap-space-md">
            <span className="inline-flex self-start items-center gap-1.5 px-space-sm py-1 rounded-full bg-surface-container-low text-on-surface-variant font-label-caps text-label-caps">
              <span className={`inline-flex rounded-full h-2 w-2 ${error ? "bg-error" : "bg-primary"}`} />
              {loading ? "INITIALIZING KBS ENGINE" : error ? "ENGINE OFFLINE" : "DIAGNOSTIC ENGINE READY"}
            </span>

            <div>
              <h1 className="font-display-hero text-3xl sm:text-4xl lg:text-5xl font-extrabold text-on-surface tracking-tight uppercase select-none">
                Auto Sage
              </h1>
              <span className="text-primary font-bold text-sm tracking-wider uppercase block mt-1">
                Intelligent Car Fault Diagnosis System
              </span>
              <p className="font-body-md text-sm md:text-base text-on-surface-variant mt-space-sm max-w-lg leading-relaxed">
                An explainable, symptom-based Knowledge-Based System designed to help vehicle owners and
                technicians isolate mechanical defects, perform physical bench verification, and follow
                structured maintenance directives.
              </p>
            </div>

            {/* Workflow steps overview */}
            <div className="flex items-center gap-space-xs flex-wrap">
              {["Vehicle Info", "Select Symptoms", "Diagnostic Inquiry", "Results & Actions"].map((label, i) => (
                <div key={label} className="flex items-center gap-space-xs">
                  <span className="flex items-center gap-1.5 px-space-sm py-1 rounded-lg bg-surface-container-low text-on-surface-variant text-xs font-medium">
                    <span className="flex items-center justify-center w-4 h-4 rounded-full text-[10px] font-bold bg-primary text-on-primary">
                      {i + 1}
                    </span>
                    {label}
                  </span>
                  {i < 3 && (
                    <span className="material-symbols-outlined text-outline-variant text-[14px]">
                      chevron_right
                    </span>
                  )}
                </div>
              ))}
            </div>

            {/* Action buttons */}
            <div className="flex flex-wrap items-center gap-space-sm pt-space-xs">
              <button
                className="inline-flex items-center gap-space-sm px-space-lg py-3 rounded-full bg-primary-container text-on-primary font-headline-sm text-sm hover:bg-primary shadow-[0_8px_20px_rgba(37,99,235,0.3)] transition-all hover:-translate-y-0.5"
                type="button"
                onClick={() => onStartDiagnosis(null)}
              >
                <span>Start New Diagnosis</span>
                <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
              </button>

              <button
                className="inline-flex items-center gap-1.5 px-space-md py-3 rounded-full bg-surface-container text-on-surface font-headline-sm text-sm hover:bg-surface-container-high transition-colors"
                type="button"
                onClick={onOpenVehicle}
              >
                <span className="material-symbols-outlined text-[18px]">directions_car</span>
                <span>{vehicleInfo ? vehicleLabel(vehicleInfo) : "Vehicle Profile"}</span>
              </button>
            </div>

            {error && (
              <p className="rounded-lg bg-error-container text-on-error-container p-space-sm text-xs">
                {error}
              </p>
            )}
          </div>

          {/* Interactive vehicle hotspot graphic */}
          <div className="lg:col-span-7 relative flex items-center justify-center min-h-[300px]">
            <div className="relative w-full max-w-2xl">
              <div className="absolute w-4/5 h-24 bg-gradient-to-r from-primary/10 via-primary/20 to-primary/10 blur-2xl rounded-full -bottom-2 left-[10%] pointer-events-none" />
              <img
                className="relative z-10 w-full object-contain max-h-[340px] drop-shadow-[0_20px_30px_rgba(0,23,75,0.12)] select-none"
                src="/images/vehicle-hero.jpg"
                alt="Vehicle system diagram"
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
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block pointer-events-none z-30">
                      <div className="px-space-sm py-1 rounded-lg bg-inverse-surface text-inverse-on-surface shadow-xl whitespace-nowrap text-center">
                        <div className="font-label-caps text-[11px] uppercase text-primary-fixed font-bold">
                          {cat.short_name}
                        </div>
                        <div className="text-[11px] text-inverse-on-surface/90">Click to diagnose subsystem</div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Feature & Activity Cards (Real data only, no fake statistics) */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-space-md">
        <StatCard
          icon="category"
          title="SYSTEM SUBSYSTEMS"
          value={ds ? `${formatNumber(ds.category_count)} Subsystems` : "8 Subsystems"}
          onClick={() => onStartDiagnosis(null)}
          action="Choose Subsystem"
        >
          Covers Brakes, Engine, Cooling, Electrical, Transmission, Emissions, HVAC, and Steering.
        </StatCard>

        <StatCard
          icon="directions_car"
          title="ACTIVE VEHICLE"
          value={vehicleInfo ? vehicleLabel(vehicleInfo) : "Unspecified"}
          onClick={onOpenVehicle}
          action={vehicleInfo ? "Edit Vehicle" : "Set Vehicle Profile"}
        >
          {vehicleInfo
            ? `${vehicleInfo.year || ""} ${vehicleInfo.make || ""} ${vehicleInfo.model || ""} · Odometer: ${vehicleInfo.odometer || "Not set"}`
            : "Enter optional make, model, year, and mileage to tag work orders and reports."}
        </StatCard>

        <StatCard
          icon="history"
          title="RECENT DIAGNOSIS"
          value={latest ? latest.categoryName || "Saved session" : "No Sessions Yet"}
          onClick={latest ? () => onOpenHistoryRecord(latest) : onOpenHistory}
          action={latest ? "Review Result" : "Open History"}
        >
          {latest
            ? `${formatRelativeTime(latest.timestamp)} · ${(latest.symptomLabels || []).length} symptom(s) recorded`
            : "Past diagnoses are saved locally in this browser for review or re-printing."}
        </StatCard>

        <StatCard
          icon="health_and_safety"
          title="SAFETY PROTOCOLS"
          value="Workshop Triage"
          onClick={onOpenSafetyGuide}
          action="View Safety Guide"
        >
          Critical precautions for braking, steering, overheating, electrical shorts, and fuel hazards.
        </StatCard>
      </div>

      {ds && (
        <footer className="pt-2 border-t border-surface-container text-[11px] text-on-surface-variant flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            Knowledge Base grounded in peer-reviewed research dataset (Obike &amp; Obot), DOI:{" "}
            <a className="text-primary underline" href={ds.url} target="_blank" rel="noreferrer">
              {ds.doi}
            </a>{" "}
            (CC BY 4.0).
          </span>
          <span className="font-mono text-outline">Deterministic Propositional Inference &bull; CT-359 KBS</span>
        </footer>
      )}
    </div>
  );
}

function StatCard({ icon, title, value, children, onClick, action }) {
  return (
    <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md flex flex-col justify-between border border-surface-container hover:border-primary/20 transition-all">
      <div>
        <div className="flex items-center gap-space-xs mb-space-sm">
          <span className="material-symbols-outlined text-primary text-[20px]">{icon}</span>
          <h2 className="font-label-caps text-[11px] text-on-surface-variant font-bold uppercase tracking-wider">
            {title}
          </h2>
        </div>
        <div className="font-headline-md text-base md:text-lg text-on-surface font-bold truncate">
          {value}
        </div>
        <p className="font-body-sm text-[12px] text-on-surface-variant mt-1.5 leading-relaxed">{children}</p>
      </div>
      {onClick && (
        <button
          className="mt-space-md w-full inline-flex items-center justify-center gap-1.5 px-space-sm py-2 rounded-lg bg-surface-container text-on-surface font-headline-sm text-xs hover:bg-surface-container-high transition-all"
          type="button"
          onClick={onClick}
        >
          <span>{action}</span>
          <span className="material-symbols-outlined text-[15px]">arrow_forward</span>
        </button>
      )}
    </section>
  );
}
