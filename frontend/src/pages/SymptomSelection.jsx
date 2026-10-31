import { useEffect, useMemo, useRef, useState } from "react";
import Stepper from "../components/Stepper.jsx";
import { diagnose, getCategories, getSymptoms } from "../services/api.js";
import { vehicleLabel } from "../stitch/dom.js";

export default function SymptomSelection({
  categoryId,
  onCategoryChange,
  selectedSymptomIds,
  setSelectedSymptomIds,
  vehicleInfo,
  onEditVehicle,
  onProceedToQuestions,
  onDiagnosisComplete,
  onBack,
  initialSearchQuery = "",
  onSearchClear,
}) {
  const [categories, setCategories] = useState([]);
  const [symptoms, setSymptoms] = useState([]);
  const [loadingCats, setLoadingCats] = useState(true);
  const [loadingSyms, setLoadingSyms] = useState(false);
  const [loadError, setLoadError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [filter, setFilter] = useState(initialSearchQuery || "");
  const [reloadKey, setReloadKey] = useState(0);
  const [showReview, setShowReview] = useState(false);
  const inFlight = useRef(false);

  useEffect(() => {
    if (initialSearchQuery) setFilter(initialSearchQuery);
  }, [initialSearchQuery]);

  useEffect(() => {
    let active = true;
    setLoadingCats(true);
    getCategories()
      .then((data) => active && (setCategories(data), setLoadError("")))
      .catch((err) => active && setLoadError(err.message))
      .finally(() => active && setLoadingCats(false));
    return () => {
      active = false;
    };
  }, [reloadKey]);

  useEffect(() => {
    if (!categoryId) {
      setSymptoms([]);
      return undefined;
    }
    let active = true;
    setLoadingSyms(true);
    setFilter("");
    getSymptoms(categoryId)
      .then((data) => active && (setSymptoms(data), setLoadError("")))
      .catch((err) => active && (setSymptoms([]), setLoadError(err.message)))
      .finally(() => active && setLoadingSyms(false));
    return () => {
      active = false;
    };
  }, [categoryId, reloadKey]);

  const activeCategory = categories.find((c) => c.category_id === categoryId) || null;
  const symptomById = useMemo(() => Object.fromEntries(symptoms.map((s) => [s.symptom_id, s])), [symptoms]);
  const visible = useMemo(() => {
    const q = filter.trim().toLowerCase();
    return q ? symptoms.filter((s) => s.label.toLowerCase().includes(q)) : symptoms;
  }, [filter, symptoms]);
  const validSelected = selectedSymptomIds.filter((id) => symptomById[id]);

  const toggle = (id) => {
    setSubmitError("");
    setSelectedSymptomIds((cur) => (cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id]));
  };

  const handleOpenReview = () => {
    if (!categoryId) {
      setSubmitError("Select a problem category first.");
      return;
    }
    if (!validSelected.length) {
      setSubmitError("Select at least one symptom before analyzing.");
      return;
    }
    setSubmitError("");
    setShowReview(true);
  };

  const handleProceed = () => {
    if (!categoryId) {
      setSubmitError("Select a problem category first.");
      return;
    }
    if (!validSelected.length) {
      setSubmitError("Select at least one symptom before analyzing.");
      return;
    }
    setShowReview(false);
    if (onProceedToQuestions) {
      onProceedToQuestions({
        categoryId,
        categoryName: activeCategory?.name,
        symptomIds: validSelected,
        symptoms: validSelected.map((id) => symptomById[id]).filter(Boolean),
      });
    } else {
      analyze();
    }
  };

  const analyze = async () => {
    if (inFlight.current) return;
    if (!categoryId) {
      setSubmitError("Select a problem category first.");
      return;
    }
    if (!validSelected.length) {
      setSubmitError("Select at least one symptom before analyzing.");
      return;
    }
    inFlight.current = true;
    setSubmitting(true);
    setSubmitError("");
    setShowReview(false);
    try {
      const result = await diagnose(categoryId, validSelected);
      onDiagnosisComplete?.(result);
    } catch (err) {
      setSubmitError(err.message || "Diagnosis failed. Please try again.");
    } finally {
      inFlight.current = false;
      setSubmitting(false);
    }
  };

  const hasOnlyBroadIndicator =
    validSelected.length === 1 && Boolean(symptomById[validSelected[0]]?.broad_indicator);

  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1600px] mx-auto pb-32">
      <Stepper currentStep={2} onStepClick={(page) => page === "vehicle" && onEditVehicle?.()} />

      <div className="flex flex-col md:flex-row md:items-end justify-between gap-space-md">
        <div>
          <button
            type="button"
            onClick={onBack}
            className="flex items-center gap-1 text-body-sm font-body-sm text-secondary hover:text-primary transition-colors"
          >
            <span className="material-symbols-outlined text-[16px]">arrow_back</span>
            Back to Vehicle Information
          </button>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight uppercase mt-1">
            Select Vehicle Symptoms
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-2xl">
            Choose a problem category, then select every symptom you have noticed on the vehicle.
          </p>
        </div>
        <button
          type="button"
          onClick={onEditVehicle}
          className="inline-flex items-center gap-1.5 px-space-md py-2 rounded-lg bg-surface-container-low hover:bg-surface-container text-on-surface font-body-sm text-body-sm self-start md:self-auto transition-colors"
        >
          <span className="material-symbols-outlined text-primary text-[18px]">directions_car</span>
          {vehicleInfo ? vehicleLabel(vehicleInfo) : "Add vehicle details"}
        </button>
      </div>

      {loadError && (
        <div className="rounded-xl bg-error-container text-on-error-container p-space-md flex items-center justify-between gap-space-md">
          <span className="font-body-sm text-body-sm">{loadError}</span>
          <button
            type="button"
            className="px-space-md py-1.5 rounded-lg bg-surface-container-lowest text-on-surface font-headline-sm text-[12px]"
            onClick={() => setReloadKey((k) => k + 1)}
          >
            Retry
          </button>
        </div>
      )}

      {/* Step 1: Category selection */}
      <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
        <h2 className="font-label-caps text-label-caps text-on-surface-variant mb-space-sm uppercase tracking-wider">
          STEP 1 — SELECT A PROBLEM CATEGORY
        </h2>
        {loadingCats ? (
          <p className="font-body-sm text-body-sm text-on-surface-variant">Loading categories…</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-space-sm">
            {categories.map((c) => {
              const active = c.category_id === categoryId;
              return (
                <button
                  key={c.category_id}
                  type="button"
                  onClick={() => {
                    setSubmitError("");
                    if (!active) onCategoryChange(c.category_id);
                  }}
                  aria-pressed={active}
                  className={`text-left rounded-xl p-space-sm transition-all border ${
                    active
                      ? "bg-primary-container text-on-primary border-primary shadow-md"
                      : "bg-surface-container-low hover:bg-surface-container border-transparent text-on-surface"
                  }`}
                >
                  <div className="flex items-center gap-space-xs">
                    <span className="material-symbols-outlined text-[20px]">{c.icon}</span>
                    <span className="font-headline-sm text-[14px]">{c.name}</span>
                  </div>
                  <div
                    className={`font-body-sm text-[11px] mt-1 ${
                      active ? "text-on-primary/80" : "text-on-surface-variant"
                    }`}
                  >
                    {c.rule_count} rules · {c.symptom_count} symptoms
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </section>

      {/* Step 2: Symptom selection */}
      {activeCategory && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-start">
          <section className="lg:col-span-8 bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm mb-space-sm">
              <div>
                <h2 className="font-label-caps text-label-caps text-on-surface-variant uppercase tracking-wider">
                  STEP 2 — SELECT SYMPTOMS ({activeCategory.name})
                </h2>
                <p className="font-body-sm text-[12px] text-on-surface-variant">{activeCategory.description}</p>
              </div>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-2.5 top-2 text-on-surface-variant text-[18px]">
                  search
                </span>
                <input
                  className="w-full sm:w-64 h-9 pl-9 pr-3 rounded-full bg-surface-container-low text-body-sm focus:outline-none focus:ring-2 focus:ring-primary/20"
                  placeholder="Filter symptoms…"
                  value={filter}
                  onChange={(e) => setFilter(e.target.value)}
                  aria-label="Filter symptoms"
                />
              </div>
            </div>
            {loadingSyms ? (
              <p className="font-body-sm text-body-sm text-on-surface-variant py-space-md">Loading symptoms…</p>
            ) : visible.length === 0 ? (
              <p className="font-body-sm text-body-sm text-on-surface-variant py-space-md">
                {symptoms.length ? "No symptoms match your filter." : "No symptoms are available for this category."}
              </p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-space-sm">
                {visible.map((s) => {
                  const on = selectedSymptomIds.includes(s.symptom_id);
                  return (
                    <button
                      key={s.symptom_id}
                      type="button"
                      onClick={() => toggle(s.symptom_id)}
                      aria-pressed={on}
                      className={`text-left rounded-xl p-space-sm flex items-start gap-space-sm border transition-all ${
                        on
                          ? "bg-primary-fixed border-primary shadow-sm"
                          : "bg-surface-container-low border-transparent hover:bg-surface-container"
                      }`}
                    >
                      <span className={`material-symbols-outlined text-[20px] ${on ? "text-primary" : "text-outline"}`}>
                        {on ? "check_box" : "check_box_outline_blank"}
                      </span>
                      <span>
                        <span className="block font-headline-sm text-[13px] text-on-surface">{s.label}</span>
                        <span className="block font-body-sm text-[11px] text-on-surface-variant">
                          {s.broad_indicator ? "General warning sign — combine with specific symptoms. " : ""}
                          {s.description}
                        </span>
                      </span>
                    </button>
                  );
                })}
              </div>
            )}
          </section>

          <aside className="lg:col-span-4 lg:sticky lg:top-20 flex flex-col gap-space-md">
            <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md">
              <div className="flex items-center justify-between mb-space-sm">
                <h2 className="font-headline-sm text-[14px] text-on-surface font-semibold">
                  Selected Symptoms ({validSelected.length})
                </h2>
                {validSelected.length > 0 && (
                  <button
                    type="button"
                    className="text-[12px] text-primary hover:underline"
                    onClick={() => setSelectedSymptomIds([])}
                  >
                    Clear all
                  </button>
                )}
              </div>
              {validSelected.length === 0 ? (
                <p className="font-body-sm text-[12px] text-on-surface-variant">
                  No symptoms selected yet. Pick one or more observed symptoms from the left.
                </p>
              ) : (
                <ul className="flex flex-wrap gap-1.5">
                  {validSelected.map((id) => (
                    <li key={id}>
                      <button
                        type="button"
                        onClick={() => toggle(id)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[12px] hover:bg-primary-fixed-dim transition-colors"
                        title="Click to remove"
                      >
                        {symptomById[id].label}
                        <span className="material-symbols-outlined text-[14px]">close</span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
              <div className="mt-space-md pt-space-xs border-t border-surface-container">
                <span className="font-label-caps text-[10px] text-on-surface-variant uppercase tracking-wider block mb-1">
                  Subsystem Safety Note
                </span>
                <p className="font-body-sm text-[11px] text-on-surface-variant">{activeCategory.safety_note}</p>
              </div>
            </section>
          </aside>
        </div>
      )}

      {/* Review Pre-Flight Modal */}
      {showReview && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-space-md"
        >
          <div className="w-full max-w-lg bg-surface-container-lowest rounded-2xl shadow-xl p-space-lg flex flex-col gap-space-md border border-surface-container-high">
            <div className="flex items-center justify-between border-b border-surface-container pb-space-sm">
              <div className="flex items-center gap-space-xs">
                <span className="material-symbols-outlined text-primary text-[22px]">checklist</span>
                <h3 className="font-headline-md text-headline-md text-on-surface">Review Symptoms</h3>
              </div>
              <button
                type="button"
                className="text-on-surface-variant hover:text-on-surface p-1 rounded-lg"
                onClick={() => setShowReview(false)}
                aria-label="Close review"
              >
                <span className="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <div>
              <span className="font-label-caps text-label-caps text-on-surface-variant uppercase">
                Active Category
              </span>
              <p className="font-headline-sm text-body-md text-on-surface font-semibold">
                {activeCategory?.name}
              </p>
            </div>

            <div>
              <span className="font-label-caps text-label-caps text-on-surface-variant uppercase">
                Vehicle Label
              </span>
              <p className="font-body-sm text-body-sm text-on-surface">
                {vehicleInfo ? vehicleLabel(vehicleInfo) : "Unspecified Vehicle"}
              </p>
            </div>

            <div>
              <span className="font-label-caps text-label-caps text-on-surface-variant uppercase block mb-1.5">
                Symptoms To Analyze ({validSelected.length})
              </span>
              <div className="flex flex-wrap gap-1.5 max-h-48 overflow-y-auto p-1">
                {validSelected.map((id) => (
                  <span
                    key={id}
                    className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[12px]"
                  >
                    <span>{symptomById[id]?.label}</span>
                    <button
                      type="button"
                      onClick={() => toggle(id)}
                      className="hover:text-error"
                      title="Remove"
                    >
                      <span className="material-symbols-outlined text-[14px]">close</span>
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {hasOnlyBroadIndicator && (
              <div className="rounded-xl bg-amber-50 text-amber-900 p-space-sm flex items-start gap-space-xs text-[12px]">
                <span className="material-symbols-outlined text-[18px] text-amber-700 shrink-0 mt-0.5">warning</span>
                <span>
                  <strong>Note:</strong> You selected only a broad warning indicator. The knowledge base
                  requires at least one corroborating physical symptom to identify candidate faults.
                </span>
              </div>
            )}

            <div className="flex items-center justify-end gap-space-sm pt-space-xs border-t border-surface-container">
              <button
                type="button"
                className="px-space-md py-2 rounded-lg bg-surface-container text-on-surface font-headline-sm text-[13px] hover:bg-surface-container-high transition-colors"
                onClick={() => setShowReview(false)}
              >
                Modify Symptoms
              </button>
              <button
                type="button"
                className="inline-flex items-center gap-1.5 px-space-lg py-2 rounded-lg bg-primary-container text-on-primary font-headline-sm text-[13px] shadow-sm hover:bg-primary transition-all"
                onClick={handleProceed}
              >
                Continue to Diagnostic Questions
                <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Sticky Bottom Bar */}
      <div className="fixed bottom-16 md:bottom-0 left-0 md:left-20 right-0 bg-surface-container-lowest/95 backdrop-blur shadow-[0_-1px_8px_rgba(0,0,0,0.06)] px-space-md md:px-space-lg py-space-sm z-30 no-print">
        <div className="max-w-[1600px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-space-sm">
          <span
            className={`font-body-sm text-body-sm ${submitError ? "text-error" : "text-on-surface-variant"}`}
            role={submitError ? "alert" : undefined}
          >
            {submitError ||
              (activeCategory
                ? `${validSelected.length} symptom(s) selected in ${activeCategory.short_name}`
                : "Select a problem category above to begin.")}
          </span>
          <div className="flex items-center gap-space-sm">
            <button
              type="button"
              onClick={handleProceed}
              disabled={submitting || !categoryId || validSelected.length === 0}
              className="inline-flex items-center gap-space-xs px-space-lg py-2.5 rounded-full bg-primary-container text-on-primary font-headline-sm text-headline-sm shadow-md hover:bg-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <>
                  <span className="material-symbols-outlined text-[18px] animate-spin">
                    progress_activity
                  </span>
                  Processing Symptoms…
                </>
              ) : (
                <>
                  Continue to Diagnostic Questions
                  <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
