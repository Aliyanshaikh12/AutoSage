import { useCallback, useEffect, useMemo, useState } from "react";
import {
  clearAllHistoryRecords,
  deleteHistoryRecord,
  readHistoryRecords,
} from "../utils/historyStorage.js";
import { formatDateTime, vehicleLabel } from "../stitch/dom.js";
import { SafetyBadge } from "../components/Evidence.jsx";

function topFault(result) {
  const m = Array.isArray(result?.matches) ? result.matches[0] : null;
  if (!m) return null;
  return m.possible_fault || m.title || m.label || m.rule_id || "Saved match";
}

export default function History({
  onOpenRecord,
  onOpenReport,
  onStartNewDiagnosis,
  onHistoryCountChange,
}) {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [notice, setNotice] = useState(null);
  const [confirmClear, setConfirmClear] = useState(false);
  const [query, setQuery] = useState("");
  const [outcome, setOutcome] = useState("all");

  const load = useCallback(() => {
    const res = readHistoryRecords();
    setHistory(res.records);
    onHistoryCountChange?.(res.records.length);
    if (res.storageError) setError(res.storageError);
    if (res.corrupted && res.corruptionMessage) setNotice(res.corruptionMessage);
  }, [onHistoryCountChange]);

  useEffect(load, [load]);

  const remove = (id) => {
    const res = deleteHistoryRecord(id);
    if (!res.ok) return setError(res.error || "Could not delete this record.");
    setHistory(res.records);
    onHistoryCountChange?.(res.records.length);
  };

  const clearAll = () => {
    const res = clearAllHistoryRecords();
    if (!res.ok) return setError(res.error || "Could not clear history.");
    setHistory([]);
    setConfirmClear(false);
    onHistoryCountChange?.(0);
  };

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return history.filter((h) => {
      const matched = h.result?.status === "matched";
      if (outcome === "matched" && !matched) return false;
      if (outcome === "no_match" && matched) return false;
      if (!q) return true;
      return [
        h.reportId,
        h.categoryName,
        h.categoryId,
        vehicleLabel(h.vehicleInfo),
        ...(h.symptomLabels || []),
        topFault(h.result),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase()
        .includes(q);
    });
  }, [history, query, outcome]);

  const byCategory = useMemo(() => {
    const counts = {};
    for (const h of history) {
      const k = h.categoryName || h.categoryId || "Unknown";
      counts[k] = (counts[k] || 0) + 1;
    }
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  }, [history]);

  return (
    <div className="w-full px-space-md md:px-space-lg py-space-md flex flex-col gap-space-lg max-w-[1400px] mx-auto pb-24">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-space-md">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight uppercase">
            Diagnosis History &amp; Audit Log
          </h1>
          <p className="font-body-sm text-body-sm text-on-surface-variant max-w-2xl">
            Past diagnostic evaluations stored locally in your browser (localStorage). You can reopen
            any past diagnosis session or export its technical dossier to PDF.
          </p>
        </div>
        <div className="flex flex-wrap gap-space-sm">
          {history.length > 0 && !confirmClear && (
            <button
              type="button"
              onClick={() => setConfirmClear(true)}
              className="inline-flex items-center gap-1.5 px-space-md py-2 rounded-lg bg-surface-container text-error font-headline-sm text-[13px] hover:bg-error-container/30 transition-colors"
            >
              <span className="material-symbols-outlined text-[18px]">delete_sweep</span>
              Clear all history
            </button>
          )}
          <button
            type="button"
            onClick={onStartNewDiagnosis}
            className="inline-flex items-center gap-1.5 px-space-md py-2 rounded-lg bg-primary-container text-on-primary font-headline-sm text-[13px] shadow-sm hover:bg-primary transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">add</span>
            New Diagnosis
          </button>
        </div>
      </div>

      {confirmClear && (
        <div
          role="alertdialog"
          className="rounded-xl bg-error-container/40 p-space-md flex flex-col sm:flex-row items-center justify-between gap-space-sm border border-error/20"
        >
          <span className="text-[13px] text-on-error-container font-medium">
            Delete all {history.length} saved diagnostic records from this browser? This cannot be undone.
          </span>
          <div className="flex gap-space-sm">
            <button
              type="button"
              className="px-space-md py-1.5 rounded-lg bg-surface-container-lowest text-[13px] font-medium"
              onClick={() => setConfirmClear(false)}
            >
              Cancel
            </button>
            <button
              type="button"
              className="px-space-md py-1.5 rounded-lg bg-error text-on-error text-[13px] font-medium shadow-sm hover:opacity-90"
              onClick={clearAll}
            >
              Delete All
            </button>
          </div>
        </div>
      )}

      {error && <p className="rounded-lg bg-error-container text-on-error-container p-space-sm text-[13px]">{error}</p>}
      {notice && <p className="rounded-lg bg-amber-50 text-amber-900 p-space-sm text-[13px] border border-amber-200">{notice}</p>}

      {history.length === 0 ? (
        <section className="bg-surface-container-lowest rounded-xl shadow-sm p-space-xl text-center flex flex-col items-center gap-space-sm border border-surface-container">
          <span className="material-symbols-outlined text-[44px] text-outline">history</span>
          <h2 className="font-headline-sm text-headline-sm text-on-surface">No saved diagnoses yet</h2>
          <p className="text-[13px] text-on-surface-variant max-w-md">
            When you evaluate vehicle symptoms, each completed diagnosis is automatically preserved here
            with a unique Report ID for offline review and technical report export.
          </p>
          <button
            type="button"
            onClick={onStartNewDiagnosis}
            className="mt-space-sm px-space-lg py-2.5 rounded-full bg-primary-container text-on-primary font-headline-sm text-headline-sm shadow-sm hover:bg-primary transition-all"
          >
            Start Diagnosis
          </button>
        </section>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-start">
          <section className="lg:col-span-8 flex flex-col gap-space-sm">
            <div className="flex flex-col sm:flex-row gap-space-sm">
              <input
                className="flex-1 h-9 px-3 rounded-full bg-surface-container-lowest shadow-sm text-body-sm focus:outline-none focus:ring-2 focus:ring-primary/20 border border-surface-container"
                placeholder="Search by Report ID, vehicle, category, fault, or symptom…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                aria-label="Search history"
              />
              <select
                className="h-9 px-3 rounded-lg bg-surface-container-lowest shadow-sm text-body-sm border border-surface-container"
                value={outcome}
                onChange={(e) => setOutcome(e.target.value)}
                aria-label="Filter by outcome"
              >
                <option value="all">All outcomes</option>
                <option value="matched">Fault Candidates Found</option>
                <option value="no_match">No Matching Rule</option>
              </select>
            </div>

            {filtered.length === 0 && (
              <p className="text-[13px] text-on-surface-variant py-space-md">No records match your filters.</p>
            )}

            {filtered.map((h) => {
              const fault = topFault(h.result);
              const count = (h.result?.matches || []).length;
              const repId = h.reportId || `HIST-${h.id.slice(-6).toUpperCase()}`;
              return (
                <article
                  key={h.id}
                  className="bg-surface-container-lowest rounded-xl shadow-sm p-space-md flex flex-col sm:flex-row sm:items-center justify-between gap-space-md border border-surface-container hover:border-outline-variant/60 transition-all"
                >
                  <div className="min-w-0 space-y-1">
                    <div className="flex items-center gap-space-xs flex-wrap">
                      <span className="font-mono text-[10px] font-bold text-primary bg-primary-fixed/40 px-2 py-0.5 rounded">
                        {repId}
                      </span>
                      <span className="text-[11px] text-on-surface-variant">
                        {formatDateTime(h.timestamp)}
                      </span>
                      <span className="text-outline-variant text-[11px]">·</span>
                      <span className="text-[11px] font-semibold text-on-surface">
                        {h.categoryName || h.categoryId || "Unknown category"}
                      </span>
                      {h.result?.overall_safety_level && (
                        <>
                          <span className="text-outline-variant text-[11px]">·</span>
                          <SafetyBadge level={h.result.overall_safety_level} />
                        </>
                      )}
                    </div>

                    <div className="font-headline-sm text-[14px] text-on-surface font-bold truncate">
                      {fault ? `${fault}${count > 1 ? ` (+${count - 1} more candidate${count > 2 ? "s" : ""})` : ""}` : "No matching rule"}
                    </div>

                    {h.result?.matches?.[0]?.affected_component && (
                      <div className="text-[11px] text-primary font-medium flex items-center gap-1">
                        <span className="material-symbols-outlined text-[13px]">build</span>
                        <span>Component: {h.result.matches[0].affected_component}</span>
                      </div>
                    )}

                    <div className="text-[11px] text-on-surface-variant flex items-center gap-2">
                      <span className="truncate max-w-xs sm:max-w-md">
                        {vehicleLabel(h.vehicleInfo)}
                      </span>
                      <span className="text-outline-variant">·</span>
                      <span>{(h.symptomLabels || []).length} symptom(s)</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-space-xs shrink-0 self-end sm:self-center">
                    <button
                      type="button"
                      onClick={() => onOpenRecord(h)}
                      className="px-space-md py-1.5 rounded-lg bg-surface-container text-on-surface text-[12px] font-headline-sm hover:bg-surface-container-high transition-colors"
                      title="Open diagnostic results"
                    >
                      View Results
                    </button>
                    {onOpenReport && (
                      <button
                        type="button"
                        onClick={() => onOpenReport(h)}
                        className="px-space-md py-1.5 rounded-lg bg-primary-container text-on-primary text-[12px] font-headline-sm hover:bg-primary transition-colors flex items-center gap-1"
                        title="Open technical report dossier"
                      >
                        <span className="material-symbols-outlined text-[15px]">description</span>
                        Report
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => remove(h.id)}
                      aria-label="Delete record"
                      className="p-1.5 rounded-lg text-error hover:bg-error-container/40 transition-colors"
                      title="Delete record"
                    >
                      <span className="material-symbols-outlined text-[18px]">delete</span>
                    </button>
                  </div>
                </article>
              );
            })}
          </section>

          <aside className="lg:col-span-4 bg-surface-container-lowest rounded-xl shadow-sm p-space-md border border-surface-container">
            <h2 className="font-label-caps text-label-caps text-on-surface-variant mb-space-sm uppercase tracking-wider">
              SAVED BY SUBSYSTEM
            </h2>
            <ul className="flex flex-col gap-space-xs">
              {byCategory.map(([name, n]) => (
                <li key={name}>
                  <div className="flex justify-between text-[12px]">
                    <span className="truncate pr-2">{name}</span>
                    <span className="font-mono font-medium">{n}</span>
                  </div>
                  <div className="h-1.5 rounded-full bg-surface-container mt-1 overflow-hidden">
                    <div
                      className="h-1.5 rounded-full bg-primary"
                      style={{ width: `${Math.round((n / history.length) * 100)}%` }}
                    />
                  </div>
                </li>
              ))}
            </ul>
            <div className="mt-space-md pt-space-xs border-t border-surface-container flex justify-between text-[11px] text-on-surface-variant">
              <span>Total Sessions Saved:</span>
              <strong className="text-on-surface font-mono">{history.length}</strong>
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
