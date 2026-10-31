import { useEffect, useMemo, useState } from "react";
import { getKnowledgeBase } from "../services/api.js";
import { formatRelativeTime, vehicleLabel } from "../stitch/dom.js";
import { readHistoryRecords } from "../utils/historyStorage.js";

const HOTSPOTS = [
  { id: "CAT_ENGINE", name: "Engine", icon: "engineering", top: "30%", left: "30%" },
  { id: "CAT_COOLING", name: "Cooling", icon: "thermostat", top: "40%", left: "16%" },
  { id: "CAT_ELECTRICAL", name: "Electrical", icon: "bolt", top: "26%", left: "48%" },
  { id: "CAT_TRANSMISSION", name: "Transmission", icon: "settings", top: "52%", left: "52%" },
  { id: "CAT_BRAKES", name: "Brakes", icon: "disc_full", top: "66%", left: "28%" },
];

const HOW_IT_WORKS = [
  {
    step: "01",
    title: "Select Symptoms",
    desc: "Choose what you hear, feel, or observe on your vehicle from organized categories.",
    icon: "checklist",
  },
  {
    step: "02",
    title: "Identify Possible Faults",
    desc: "Evaluate your symptoms against automotive diagnostic rules to identify potential causes.",
    icon: "troubleshoot",
  },
  {
    step: "03",
    title: "Get Repair Guidance",
    desc: "Follow physical verification checks, maintenance recommendations, and safety alerts.",
    icon: "build_circle",
  },
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
  const categories = kb?.categories || [];
  const catById = Object.fromEntries(categories.map((c) => [c.category_id, c]));

  return (
    <div className="w-full px-4 sm:px-6 lg:px-8 py-6 flex flex-col gap-8 max-w-[1500px] mx-auto pb-28 animate-fade-in">
      {/* Hero Section */}
      <section className="w-full bg-surface-container-lowest rounded-2xl shadow-sm p-6 sm:p-8 lg:p-10 relative overflow-hidden border border-surface-container">
        {/* Subtle decorative background pattern */}
        <div className="absolute inset-0 pointer-events-none opacity-40 bg-[radial-gradient(#c3c6d7_1px,transparent_1px)] [background-size:24px_24px]" />
        <div className="absolute -right-24 -top-24 w-96 h-96 bg-primary/5 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          {/* Left Hero Content */}
          <div className="lg:col-span-6 flex flex-col justify-center gap-5">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-low text-on-surface-variant text-xs font-semibold self-start border border-surface-container">
              <span className={`inline-block w-2 h-2 rounded-full ${error ? "bg-error" : "bg-emerald-500 animate-pulse"}`} />
              <span>{loading ? "Initializing Diagnostic System…" : error ? "System Offline" : "Diagnostic System Ready"}</span>
            </div>

            <div>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-on-surface tracking-tight leading-tight">
                Your Car. <span className="text-primary">Our Diagnosis.</span>
              </h1>
              <p className="text-lg sm:text-xl font-medium text-on-surface-variant mt-2">
                Find the problem. Know what to do next.
              </p>
              <p className="text-sm sm:text-base text-on-surface-variant/90 mt-3 max-w-xl leading-relaxed">
                Identify possible car problems through symptoms and get helpful inspection and repair guidance before heading to the shop.
              </p>
            </div>

            {/* Primary Action Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <button
                type="button"
                onClick={() => onStartDiagnosis(null)}
                className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-primary text-on-primary font-semibold text-sm sm:text-base shadow-lg shadow-primary/25 hover:bg-primary-container hover:shadow-primary/35 transition-all duration-150 active:scale-[0.98]"
              >
                <span>Start Diagnosis</span>
                <span className="material-symbols-outlined text-[20px]">arrow_forward</span>
              </button>

              <button
                type="button"
                onClick={onOpenVehicle}
                className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-surface-container-low text-on-surface hover:bg-surface-container font-semibold text-sm transition-all border border-surface-container-high"
              >
                <span className="material-symbols-outlined text-primary text-[20px]">directions_car</span>
                <span>{vehicleInfo ? vehicleLabel(vehicleInfo) : "Add Vehicle Details"}</span>
              </button>
            </div>

            {error && (
              <div className="rounded-xl bg-error-container/30 border border-error/30 p-3 text-xs text-error flex items-center gap-2">
                <span className="material-symbols-outlined text-[16px]">error</span>
                <span>{error}</span>
              </div>
            )}
          </div>

          {/* Right Hero Graphic with Subsystem Hotspots */}
          <div className="lg:col-span-6 relative flex items-center justify-center">
            <div className="relative w-full max-w-lg">
              <div className="absolute w-4/5 h-28 bg-gradient-to-r from-primary/10 via-primary/20 to-primary/10 blur-2xl rounded-full -bottom-4 left-[10%] pointer-events-none" />
              <img
                className="relative z-10 w-full object-contain max-h-[320px] drop-shadow-[0_15px_25px_rgba(0,23,75,0.12)] select-none transition-transform duration-300 hover:scale-[1.02]"
                src="/images/vehicle-hero.jpg"
                alt="Automotive diagnostic diagram"
              />

              {HOTSPOTS.map((h) => {
                const cat = catById[h.id];
                return (
                  <div key={h.id} className="absolute z-20 group" style={{ top: h.top, left: h.left }}>
                    <button
                      aria-label={`Diagnose ${h.name}`}
                      type="button"
                      onClick={() => onStartDiagnosis(h.id)}
                      className="relative flex items-center justify-center w-8 h-8 rounded-full bg-primary text-on-primary shadow-md hover:scale-125 hover:bg-primary-container transition-all"
                    >
                      <span className="material-symbols-outlined text-[17px]">{h.icon}</span>
                    </button>
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block pointer-events-none z-30">
                      <div className="px-2.5 py-1 rounded-md bg-inverse-surface text-inverse-on-surface text-[11px] font-semibold whitespace-nowrap shadow-xl">
                        Diagnose {cat ? cat.short_name || cat.name : h.name}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      {/* How Auto Sage Works */}
      <section className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-1">
          <div>
            <span className="text-xs font-bold text-primary uppercase tracking-wider block">
              Simple 3-Step Process
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-on-surface tracking-tight">
              How Auto Sage Works
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-on-surface-variant max-w-md">
            Structured diagnostic workflow designed to guide you from observed symptoms to verified solutions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {HOW_IT_WORKS.map((item) => (
            <div
              key={item.step}
              className="bg-surface-container-lowest rounded-xl p-5 border border-surface-container shadow-sm card-hover-fx flex flex-col justify-between gap-4"
            >
              <div className="flex items-center justify-between">
                <span className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                  <span className="material-symbols-outlined text-[22px]">{item.icon}</span>
                </span>
                <span className="text-xs font-extrabold text-outline-variant font-mono">
                  {item.step}
                </span>
              </div>
              <div>
                <h3 className="text-base font-bold text-on-surface">{item.title}</h3>
                <p className="text-xs text-on-surface-variant mt-1.5 leading-relaxed">
                  {item.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Subsystems Quick Access Grid */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <span className="text-xs font-bold text-primary uppercase tracking-wider block">
              Vehicle Subsystems
            </span>
            <h2 className="text-xl sm:text-2xl font-bold text-on-surface tracking-tight">
              Select a Problem Area
            </h2>
          </div>
          <button
            type="button"
            onClick={() => onStartDiagnosis(null)}
            className="text-xs font-semibold text-primary hover:underline flex items-center gap-1"
          >
            <span>View All</span>
            <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
          {categories.map((cat) => (
            <button
              key={cat.category_id}
              type="button"
              onClick={() => onStartDiagnosis(cat.category_id)}
              className="bg-surface-container-lowest rounded-xl p-4 border border-surface-container text-left card-hover-fx flex flex-col justify-between min-h-[110px] group"
            >
              <div className="flex items-center justify-between">
                <span className="w-9 h-9 rounded-lg bg-surface-container-low text-primary flex items-center justify-center group-hover:bg-primary group-hover:text-on-primary transition-colors">
                  <span className="material-symbols-outlined text-[20px]">{cat.icon || "build"}</span>
                </span>
                <span className="text-[11px] font-medium text-on-surface-variant">
                  {cat.symptom_count} symptoms
                </span>
              </div>
              <div className="mt-2">
                <h4 className="text-sm font-bold text-on-surface group-hover:text-primary transition-colors">
                  {cat.name}
                </h4>
                <p className="text-[11px] text-on-surface-variant line-clamp-1 mt-0.5">
                  {cat.description || "Diagnose vehicle faults"}
                </p>
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Recent Activity & Safety Guide Strip */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Recent Activity Card */}
        <div className="bg-surface-container-lowest rounded-xl p-5 border border-surface-container shadow-sm flex flex-col justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="material-symbols-outlined text-primary text-[20px]">history</span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                Recent Diagnostic Activity
              </h3>
            </div>
            {latest ? (
              <div className="space-y-1">
                <h4 className="text-base font-bold text-on-surface">
                  {latest.categoryName || "Diagnostic Session"}
                </h4>
                <p className="text-xs text-on-surface-variant">
                  {vehicleLabel(latest.vehicleInfo)} &bull; {formatRelativeTime(latest.timestamp)}
                </p>
                <div className="flex flex-wrap gap-1 pt-1.5">
                  {(latest.symptomLabels || []).slice(0, 3).map((sym, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 rounded-full bg-surface-container text-on-surface text-[11px]"
                    >
                      {sym}
                    </span>
                  ))}
                  {(latest.symptomLabels || []).length > 3 && (
                    <span className="px-2 py-0.5 rounded-full bg-surface-container-high text-on-surface-variant text-[11px]">
                      +{(latest.symptomLabels || []).length - 3} more
                    </span>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-xs text-on-surface-variant leading-relaxed">
                No past diagnoses recorded yet. Your diagnostic sessions and reports will automatically be saved here for offline access.
              </p>
            )}
          </div>

          <div className="pt-2 border-t border-surface-container flex items-center justify-between">
            {latest ? (
              <button
                type="button"
                onClick={() => onOpenHistoryRecord(latest)}
                className="text-xs font-semibold text-primary hover:underline flex items-center gap-1"
              >
                <span>Review Latest Result</span>
                <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
              </button>
            ) : (
              <span className="text-xs text-outline">Offline Local Storage</span>
            )}
            <button
              type="button"
              onClick={onOpenHistory}
              className="text-xs font-medium text-on-surface-variant hover:text-on-surface"
            >
              All Records ({history.length})
            </button>
          </div>
        </div>

        {/* Safety Guide Card */}
        <div className="bg-surface-container-lowest rounded-xl p-5 border border-surface-container shadow-sm flex flex-col justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="material-symbols-outlined text-amber-600 text-[20px]">health_and_safety</span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                Emergency &amp; Safety Protocols
              </h3>
            </div>
            <h4 className="text-base font-bold text-on-surface">
              Workshop &amp; Roadside Safety Guide
            </h4>
            <p className="text-xs text-on-surface-variant leading-relaxed mt-1">
              Critical precautions for sudden brake failures, steering loss, overheating steam hazards, fuel leaks, and high-voltage electrical components.
            </p>
          </div>

          <div className="pt-2 border-t border-surface-container flex items-center justify-between">
            <span className="text-[11px] text-on-surface-variant">
              Covers 6 Critical Hazard Domains
            </span>
            <button
              type="button"
              onClick={onOpenSafetyGuide}
              className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline"
            >
              <span>Open Safety Guide</span>
              <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
            </button>
          </div>
        </div>
      </div>

      {/* Clean Product Footer */}
      <footer className="pt-4 border-t border-surface-container text-xs text-on-surface-variant flex flex-col sm:flex-row items-center justify-between gap-2 text-center sm:text-left">
        <span>
          Auto Sage &bull; Intelligent Car Fault Diagnosis Platform
        </span>
        <span className="text-outline">
          All data and session history remain securely stored in your local browser.
        </span>
      </footer>
    </div>
  );
}
