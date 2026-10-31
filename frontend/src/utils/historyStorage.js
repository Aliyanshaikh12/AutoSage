export const HISTORY_STORAGE_KEY = "auto_sage_history";
export const MAX_HISTORY_RECORDS = 50;

function getDefaultStorage() {
  try {
    if (typeof window !== "undefined" && window.localStorage) {
      return window.localStorage;
    }
    if (typeof globalThis !== "undefined" && globalThis.localStorage) {
      return globalThis.localStorage;
    }
  } catch {
    return null;
  }
  return null;
}

export function isQuotaExceededError(err) {
  if (!err || typeof err !== "object") return false;
  const name = typeof err.name === "string" ? err.name : "";
  const code = typeof err.code === "number" ? err.code : 0;
  return (
    name === "QuotaExceededError" ||
    name === "NS_ERROR_DOM_QUOTA_REACHED" ||
    name === "QuotaExceeded" ||
    code === 22 ||
    code === 1014
  );
}

export function createHistoryRecordId() {
  try {
    if (
      typeof globalThis !== "undefined" &&
      globalThis.crypto &&
      typeof globalThis.crypto.randomUUID === "function"
    ) {
      return globalThis.crypto.randomUUID();
    }
  } catch {
    // Fall back to timestamp + random suffix below.
  }
  const randomPart = Math.random().toString(36).slice(2, 10);
  return `hist-${Date.now()}-${randomPart}`;
}

export function createReportId(timestamp = new Date()) {
  const d = timestamp instanceof Date ? timestamp : new Date(timestamp);
  const dateStr = !Number.isNaN(d.getTime())
    ? d.toISOString().slice(0, 10).replace(/-/g, "")
    : new Date().toISOString().slice(0, 10).replace(/-/g, "");
  const randomSuffix = Math.random().toString(36).slice(2, 6).toUpperCase();
  return `AS-${dateStr}-${randomSuffix}`;
}

export function isSuccessfulDiagnosisResponse(result) {
  if (!result || typeof result !== "object" || Array.isArray(result)) {
    return false;
  }
  if (result.status === "matched" || result.status === "normal") {
    return (
      (Array.isArray(result.matches) && result.matches.length > 0) ||
      (Array.isArray(result.cross_category_matches) &&
        result.cross_category_matches.length > 0)
    );
  }
  if (result.status === "no_match") {
    return result.matches === undefined || Array.isArray(result.matches);
  }
  return false;
}

function sanitizeStringArray(list) {
  if (!Array.isArray(list)) return [];
  return list
    .filter((item) => typeof item === "string" && item.trim().length > 0)
    .map((item) => item.trim());
}

export function normalizeHistoryRecord(rawItem) {
  if (!rawItem || typeof rawItem !== "object" || Array.isArray(rawItem)) {
    return null;
  }

  const id =
    typeof rawItem.id === "string" && rawItem.id.trim().length > 0
      ? rawItem.id.trim()
      : typeof rawItem.id === "number" && Number.isFinite(rawItem.id)
      ? String(rawItem.id)
      : null;

  const result = rawItem.result;
  if (!id || !isSuccessfulDiagnosisResponse(result)) {
    return null;
  }

  const categoryId =
    (typeof rawItem.categoryId === "string" && rawItem.categoryId.trim()) ||
    (typeof result.category_id === "string" && result.category_id.trim()) ||
    null;

  if (!categoryId) {
    return null;
  }

  const parsedTime =
    typeof rawItem.timestamp === "string"
      ? Date.parse(rawItem.timestamp)
      : Number.NaN;
  if (Number.isNaN(parsedTime)) {
    return null;
  }
  const timestamp = new Date(parsedTime).toISOString();

  const reportId =
    (typeof rawItem.reportId === "string" && rawItem.reportId.trim()) ||
    (typeof result.report_id === "string" && result.report_id.trim()) ||
    createReportId(timestamp);

  const categoryName =
    (typeof rawItem.categoryName === "string" && rawItem.categoryName.trim()) ||
    (typeof result.category_name === "string" &&
      result.category_name.trim()) ||
    categoryId;

  const symptomIdsFromRecord = sanitizeStringArray(rawItem.symptomIds);
  const symptomIdsFromResult = sanitizeStringArray(result.selected_symptoms);
  const symptomIds =
    symptomIdsFromRecord.length > 0
      ? symptomIdsFromRecord
      : symptomIdsFromResult;

  let symptomLabels = sanitizeStringArray(rawItem.symptomLabels);
  if (
    symptomLabels.length === 0 &&
    Array.isArray(result.selected_symptom_details)
  ) {
    symptomLabels = result.selected_symptom_details
      .filter((d) => d && typeof d === "object")
      .map((d) =>
        typeof d.text === "string" && d.text.trim()
          ? d.text.trim()
          : typeof d.symptom_id === "string"
          ? d.symptom_id.trim()
          : ""
      )
      .filter(Boolean);
  }
  if (symptomLabels.length === 0 && symptomIds.length > 0) {
    symptomLabels = [...symptomIds];
  }

  const symptomCount =
    symptomLabels.length > 0
      ? symptomLabels.length
      : typeof rawItem.symptomCount === "number" && rawItem.symptomCount >= 0
      ? rawItem.symptomCount
      : symptomIds.length;

  const vehicleInfo =
    rawItem.vehicleInfo && typeof rawItem.vehicleInfo === "object"
      ? rawItem.vehicleInfo
      : result.vehicle && typeof result.vehicle === "object"
      ? result.vehicle
      : null;

  return {
    id,
    reportId,
    timestamp,
    categoryId,
    categoryName,
    symptomIds,
    symptomLabels,
    symptomCount,
    vehicleInfo,
    result,
  };
}

export function sortRecordsRecentFirst(records) {
  return [...records].sort((a, b) => {
    const timeA = Date.parse(a.timestamp);
    const timeB = Date.parse(b.timestamp);
    if (Number.isNaN(timeA) && Number.isNaN(timeB)) return 0;
    if (Number.isNaN(timeA)) return 1;
    if (Number.isNaN(timeB)) return -1;
    return timeB - timeA;
  });
}

export function readHistoryRecords(storage = getDefaultStorage()) {
  if (!storage) {
    return {
      records: [],
      corrupted: false,
      corruptionMessage: null,
      storageError:
        "Browser localStorage is unavailable in this environment.",
    };
  }

  let raw = null;
  try {
    raw = storage.getItem(HISTORY_STORAGE_KEY);
  } catch {
    return {
      records: [],
      corrupted: false,
      corruptionMessage: null,
      storageError:
        "Browser localStorage could not be accessed (check browser privacy or site-storage settings).",
    };
  }

  if (raw === null || raw.trim() === "") {
    return {
      records: [],
      corrupted: false,
      corruptionMessage: null,
      storageError: null,
    };
  }

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    try {
      storage.removeItem(HISTORY_STORAGE_KEY);
    } catch {
      // Ignore secondary storage errors during cleanup.
    }
    return {
      records: [],
      corrupted: true,
      corruptionMessage:
        "Corrupted diagnosis history data was detected in browser storage and has been safely reset.",
      storageError: null,
    };
  }

  if (!Array.isArray(parsed)) {
    try {
      storage.removeItem(HISTORY_STORAGE_KEY);
    } catch {
      // Ignore secondary storage errors during cleanup.
    }
    return {
      records: [],
      corrupted: true,
      corruptionMessage:
        "Stored diagnosis history had an invalid structure and has been safely reset.",
      storageError: null,
    };
  }

  const seenIds = new Set();
  const validRecords = [];
  let droppedCount = 0;

  for (const rawEntry of parsed) {
    const normalized = normalizeHistoryRecord(rawEntry);
    if (!normalized || seenIds.has(normalized.id)) {
      droppedCount += 1;
      continue;
    }
    seenIds.add(normalized.id);
    validRecords.push(normalized);
  }

  const sorted = sortRecordsRecentFirst(validRecords).slice(
    0,
    MAX_HISTORY_RECORDS
  );

  if (droppedCount > 0) {
    try {
      if (sorted.length === 0) {
        storage.removeItem(HISTORY_STORAGE_KEY);
      } else {
        storage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(sorted));
      }
    } catch {
      // Non-fatal if cleanup write-back fails.
    }
  }

  return {
    records: sorted,
    corrupted: droppedCount > 0,
    corruptionMessage:
      droppedCount > 0
        ? `${droppedCount} invalid or corrupted history record${
            droppedCount === 1 ? " was" : "s were"
          } skipped and cleaned from browser storage.`
        : null,
    storageError: null,
  };
}

export function saveDiagnosisToHistory(
  {
    reportId,
    categoryId,
    categoryName,
    symptomIds,
    symptomLabels,
    vehicleInfo,
    result,
  },
  storage = getDefaultStorage()
) {
  if (!isSuccessfulDiagnosisResponse(result)) {
    const current = readHistoryRecords(storage);
    return {
      saved: false,
      trimmedForQuota: false,
      quotaExceeded: false,
      record: null,
      records: current.records,
      warning: null,
      error: null,
    };
  }

  if (!storage) {
    return {
      saved: false,
      trimmedForQuota: false,
      quotaExceeded: false,
      record: null,
      records: [],
      warning: null,
      error:
        "Browser localStorage is unavailable, so this diagnosis could not be saved to history.",
    };
  }

  const resolvedReportId =
    reportId || result?.report_id || createReportId();

  const entry = normalizeHistoryRecord({
    id: createHistoryRecordId(),
    reportId: resolvedReportId,
    timestamp: new Date().toISOString(),
    categoryId,
    categoryName,
    symptomIds,
    symptomLabels,
    symptomCount: Array.isArray(symptomLabels) ? symptomLabels.length : 0,
    vehicleInfo: vehicleInfo || null,
    result: {
      ...result,
      report_id: resolvedReportId,
    },
  });

  if (!entry) {
    const current = readHistoryRecords(storage);
    return {
      saved: false,
      trimmedForQuota: false,
      quotaExceeded: false,
      record: null,
      records: current.records,
      warning: null,
      error: null,
    };
  }

  const existing = readHistoryRecords(storage).records.filter(
    (item) => item.id !== entry.id
  );
  const combined = sortRecordsRecentFirst([entry, ...existing]);
  const primarySlice = combined.slice(0, MAX_HISTORY_RECORDS);

  try {
    storage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(primarySlice));
    return {
      saved: true,
      trimmedForQuota: false,
      quotaExceeded: false,
      record: entry,
      records: primarySlice,
      warning: null,
      error: null,
    };
  } catch (err) {
    if (!isQuotaExceededError(err)) {
      return {
        saved: false,
        trimmedForQuota: false,
        quotaExceeded: false,
        record: null,
        records: existing,
        warning: null,
        error:
          "Browser localStorage blocked saving this record (check browser privacy settings).",
      };
    }

    // QuotaExceededError recovery: progressively trim older records to fit.
    const fallbackLimits = [25, 10, 5, 1];
    for (const limit of fallbackLimits) {
      if (limit >= primarySlice.length && primarySlice.length > 1) {
        continue;
      }
      const smallerSlice = combined.slice(0, limit);
      try {
        storage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(smallerSlice));
        return {
          saved: true,
          trimmedForQuota: true,
          quotaExceeded: false,
          record: entry,
          records: smallerSlice,
          warning:
            "Browser storage was nearly full, so older history entries were trimmed to save this diagnosis.",
          error: null,
        };
      } catch (retryErr) {
        if (!isQuotaExceededError(retryErr)) {
          break;
        }
      }
    }

    return {
      saved: false,
      trimmedForQuota: false,
      quotaExceeded: true,
      record: null,
      records: existing,
      warning: null,
      error:
        "Browser localStorage quota is full. Your diagnosis results are shown below, but could not be saved locally. Delete older entries in Diagnosis History to free space.",
    };
  }
}

export function deleteHistoryRecord(recordId, storage = getDefaultStorage()) {
  if (!storage) {
    return {
      ok: false,
      records: [],
      error: "Browser localStorage is unavailable.",
    };
  }

  const current = readHistoryRecords(storage);
  if (current.storageError) {
    return {
      ok: false,
      records: [],
      error: current.storageError,
    };
  }

  const filtered = current.records.filter((item) => item.id !== recordId);

  try {
    if (filtered.length === 0) {
      storage.removeItem(HISTORY_STORAGE_KEY);
    } else {
      storage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(filtered));
    }
    return {
      ok: true,
      records: filtered,
      error: null,
    };
  } catch (err) {
    return {
      ok: false,
      records: current.records,
      error: isQuotaExceededError(err)
        ? "Browser storage quota prevented updating history. Try clearing all history."
        : "Failed to update browser localStorage when deleting this record.",
    };
  }
}

export function clearAllHistoryRecords(storage = getDefaultStorage()) {
  if (!storage) {
    return {
      ok: false,
      records: [],
      error: "Browser localStorage is unavailable.",
    };
  }

  try {
    storage.removeItem(HISTORY_STORAGE_KEY);
    return {
      ok: true,
      records: [],
      error: null,
    };
  } catch {
    return {
      ok: false,
      records: readHistoryRecords(storage).records,
      error: "Unable to clear browser localStorage.",
    };
  }
}

export function buildReviewPayloadFromEntry(entry) {
  if (!entry || typeof entry !== "object" || !entry.result) {
    return null;
  }

  const baseResult = entry.result;
  const enriched = { ...baseResult };

  if (!enriched.report_id && entry.reportId) {
    enriched.report_id = entry.reportId;
  }
  if (!enriched.category_id && entry.categoryId) {
    enriched.category_id = entry.categoryId;
  }
  if (!enriched.category_name && entry.categoryName) {
    enriched.category_name = entry.categoryName;
  }
  if (!enriched.vehicle && entry.vehicleInfo) {
    enriched.vehicle = entry.vehicleInfo;
  }

  if (
    (!Array.isArray(enriched.selected_symptom_details) ||
      enriched.selected_symptom_details.length === 0) &&
    Array.isArray(entry.symptomLabels) &&
    entry.symptomLabels.length > 0
  ) {
    const ids = Array.isArray(enriched.selected_symptoms)
      ? enriched.selected_symptoms
      : Array.isArray(entry.symptomIds)
      ? entry.symptomIds
      : [];
    enriched.selected_symptom_details = entry.symptomLabels.map(
      (label, index) => ({
        symptom_id:
          typeof ids[index] === "string" && ids[index].trim()
            ? ids[index].trim()
            : `SAVED_SYM_${index + 1}`,
        text: label,
      })
    );
  }

  return enriched;
}
