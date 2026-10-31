import test from "node:test";
import assert from "node:assert/strict";

import {
  HISTORY_STORAGE_KEY,
  buildReviewPayloadFromEntry,
  clearAllHistoryRecords,
  deleteHistoryRecord,
  readHistoryRecords,
  saveDiagnosisToHistory,
} from "../src/utils/historyStorage.js";

function createMemoryStorage({ maxBytes = Infinity } = {}) {
  const store = new Map();
  return {
    getItem(key) {
      return store.has(key) ? store.get(key) : null;
    },
    setItem(key, value) {
      const strValue = String(value);
      if (strValue.length > maxBytes) {
        const quotaErr = new Error("Storage quota exceeded");
        quotaErr.name = "QuotaExceededError";
        quotaErr.code = 22;
        throw quotaErr;
      }
      store.set(key, strValue);
    },
    removeItem(key) {
      store.delete(key);
    },
    rawMap: store,
  };
}

const SAMPLE_MATCH_RESULT = {
  status: "matched",
  category_id: "CAT_STARTING",
  category_name: "Starting Problems",
  selected_symptoms: ["SYM_START_CLICK_OR_SILENCE"],
  selected_symptom_details: [
    {
      symptom_id: "SYM_START_CLICK_OR_SILENCE",
      text: "Clicking sound or complete silence when turning the key",
    },
  ],
  match_count: 1,
  matches: [
    {
      rule_id: "R_START_001",
      title: "Dead or dying battery",
      possible_fault: "Battery is dead or dying",
      possible_causes: ["Battery older than 3-5 years"],
      recommended_action: "Try jump-starting the car.",
      explanation:
        "AAA lists a clicking noise or silence when turning the key as a sign of a dead or dying battery.",
      source: [
        {
          title: "AAA - 14 Reasons Why Your Car Won't Start",
          url: "https://www.aaa.com/autorepair/articles/14-reasons-why-your-car-wont-start",
        },
      ],
      matched_symptoms: ["SYM_START_CLICK_OR_SILENCE"],
    },
  ],
};

const SAMPLE_NO_MATCH_RESULT = {
  status: "no_match",
  category_id: "CAT_STARTING",
  category_name: "Starting Problems",
  selected_symptoms: ["SYM_START_NO_CRANK_NO_CLICK"],
  matches: [],
  match_count: 0,
};

test("saves real matched and no_match responses with unique IDs and symptom labels", () => {
  const storage = createMemoryStorage();

  const first = saveDiagnosisToHistory(
    {
      categoryId: "CAT_STARTING",
      categoryName: "Starting Problems",
      symptomIds: ["SYM_START_CLICK_OR_SILENCE"],
      symptomLabels: [
        "Clicking sound or complete silence when turning the key",
      ],
      result: SAMPLE_MATCH_RESULT,
    },
    storage
  );

  assert.equal(first.saved, true);
  assert.ok(first.record.id);
  assert.ok(first.record.timestamp);
  assert.equal(first.record.categoryId, "CAT_STARTING");
  assert.deepEqual(first.record.symptomLabels, [
    "Clicking sound or complete silence when turning the key",
  ]);

  const second = saveDiagnosisToHistory(
    {
      categoryId: "CAT_STARTING",
      categoryName: "Starting Problems",
      symptomIds: ["SYM_START_NO_CRANK_NO_CLICK"],
      symptomLabels: ["Engine does not crank and makes no clicking noise"],
      result: SAMPLE_NO_MATCH_RESULT,
    },
    storage
  );

  assert.equal(second.saved, true);
  assert.notEqual(first.record.id, second.record.id);
  assert.equal(second.records.length, 2);
});

test("rejects error or malformed diagnosis responses without saving fake records", () => {
  const storage = createMemoryStorage();

  for (const invalidResult of [
    null,
    undefined,
    { status: "error", message: "Invalid input." },
    { status: "matched", matches: [] },
    "not an object",
  ]) {
    const res = saveDiagnosisToHistory(
      {
        categoryId: "CAT_BRAKES",
        categoryName: "Brake Problems",
        symptomIds: ["SYM_BRAKE_SPONGY"],
        symptomLabels: ["Brake pedal feels spongy"],
        result: invalidResult,
      },
      storage
    );
    assert.equal(res.saved, false);
  }

  assert.equal(readHistoryRecords(storage).records.length, 0);
});

test("returns recent records first regardless of stored array order", () => {
  const storage = createMemoryStorage();
  storage.setItem(
    HISTORY_STORAGE_KEY,
    JSON.stringify([
      {
        id: "older-rec",
        timestamp: "2026-01-10T09:00:00.000Z",
        categoryId: "CAT_STARTING",
        categoryName: "Starting Problems",
        symptomLabels: ["Old symptom"],
        result: SAMPLE_NO_MATCH_RESULT,
      },
      {
        id: "newer-rec",
        timestamp: "2026-06-15T14:30:00.000Z",
        categoryId: "CAT_STARTING",
        categoryName: "Starting Problems",
        symptomLabels: ["Recent symptom"],
        result: SAMPLE_MATCH_RESULT,
      },
    ])
  );

  const loaded = readHistoryRecords(storage);
  assert.deepEqual(
    loaded.records.map((r) => r.id),
    ["newer-rec", "older-rec"]
  );
});

test("deletes a single record and clears all records cleanly", () => {
  const storage = createMemoryStorage();

  const r1 = saveDiagnosisToHistory(
    {
      categoryId: "CAT_STARTING",
      categoryName: "Starting Problems",
      symptomIds: ["SYM_START_CLICK_OR_SILENCE"],
      symptomLabels: ["Clicking sound"],
      result: SAMPLE_MATCH_RESULT,
    },
    storage
  );
  const r2 = saveDiagnosisToHistory(
    {
      categoryId: "CAT_STARTING",
      categoryName: "Starting Problems",
      symptomIds: ["SYM_START_NO_CRANK_NO_CLICK"],
      symptomLabels: ["No crank, no click"],
      result: SAMPLE_NO_MATCH_RESULT,
    },
    storage
  );

  const afterDelete = deleteHistoryRecord(r1.record.id, storage);
  assert.equal(afterDelete.ok, true);
  assert.deepEqual(
    afterDelete.records.map((r) => r.id),
    [r2.record.id]
  );

  const afterClear = clearAllHistoryRecords(storage);
  assert.equal(afterClear.ok, true);
  assert.equal(afterClear.records.length, 0);
  assert.equal(storage.getItem(HISTORY_STORAGE_KEY), null);
});

test("recovers safely from corrupted JSON, non-array payloads, and mixed invalid entries", () => {
  const storage = createMemoryStorage();

  // 1. Malformed JSON string
  storage.setItem(HISTORY_STORAGE_KEY, "{not-valid-json");
  const badJson = readHistoryRecords(storage);
  assert.equal(badJson.corrupted, true);
  assert.deepEqual(badJson.records, []);
  assert.equal(storage.getItem(HISTORY_STORAGE_KEY), null);

  // 2. Non-array JSON value
  storage.setItem(HISTORY_STORAGE_KEY, JSON.stringify({ unexpected: true }));
  const nonArray = readHistoryRecords(storage);
  assert.equal(nonArray.corrupted, true);
  assert.deepEqual(nonArray.records, []);

  // 3. Array containing one valid record and two invalid records
  storage.setItem(
    HISTORY_STORAGE_KEY,
    JSON.stringify([
      null,
      {
        id: "err-entry",
        timestamp: "2026-05-01T10:00:00.000Z",
        categoryId: "CAT_BRAKES",
        result: { status: "error", message: "Bad request" },
      },
      {
        id: "valid-entry",
        timestamp: "2026-05-02T10:00:00.000Z",
        categoryId: "CAT_STARTING",
        categoryName: "Starting Problems",
        symptomLabels: ["Clicking sound"],
        result: SAMPLE_MATCH_RESULT,
      },
    ])
  );

  const mixed = readHistoryRecords(storage);
  assert.equal(mixed.corrupted, true);
  assert.equal(mixed.records.length, 1);
  assert.equal(mixed.records[0].id, "valid-entry");
});

test("handles QuotaExceededError by trimming older records or failing safely", () => {
  // Tight storage cap: fits ~1-2 records, not 6.
  const tightStorage = createMemoryStorage({ maxBytes: 2200 });

  for (let i = 0; i < 6; i += 1) {
    saveDiagnosisToHistory(
      {
        categoryId: "CAT_STARTING",
        categoryName: "Starting Problems",
        symptomIds: ["SYM_START_CLICK_OR_SILENCE"],
        symptomLabels: [`Observed symptom #${i + 1}`],
        result: SAMPLE_MATCH_RESULT,
      },
      tightStorage
    );
  }

  const trimmedCheck = readHistoryRecords(tightStorage);
  assert.ok(trimmedCheck.records.length >= 1);
  assert.equal(trimmedCheck.records[0].symptomLabels[0], "Observed symptom #6");

  // Zero-byte storage cap: fails gracefully without throwing.
  const fullStorage = createMemoryStorage({ maxBytes: 10 });
  const blocked = saveDiagnosisToHistory(
    {
      categoryId: "CAT_STARTING",
      categoryName: "Starting Problems",
      symptomIds: ["SYM_START_CLICK_OR_SILENCE"],
      symptomLabels: ["Clicking sound"],
      result: SAMPLE_MATCH_RESULT,
    },
    fullStorage
  );
  assert.equal(blocked.saved, false);
  assert.equal(blocked.quotaExceeded, true);
  assert.equal(typeof blocked.error, "string");
});

test("reconstructs selected_symptom_details when reviewing legacy saved entries", () => {
  const legacyEntry = {
    id: "legacy-1",
    timestamp: "2026-03-01T12:00:00.000Z",
    categoryId: "CAT_BRAKES",
    categoryName: "Brake Problems",
    symptomLabels: ["Brake pedal feels low or spongy"],
    result: {
      status: "matched",
      category_id: "CAT_BRAKES",
      selected_symptoms: ["SYM_BRAKE_SPONGY"],
      match_count: 1,
      matches: [
        {
          rule_id: "R_BRAKE_003",
          title: "Spongy brake pedal",
          possible_fault: "Potential problem in the brake system",
        },
      ],
    },
  };

  const payload = buildReviewPayloadFromEntry(legacyEntry);
  assert.equal(payload.category_name, "Brake Problems");
  assert.deepEqual(payload.selected_symptom_details, [
    {
      symptom_id: "SYM_BRAKE_SPONGY",
      text: "Brake pedal feels low or spongy",
    },
  ]);
  assert.equal(payload.matches[0].rule_id, "R_BRAKE_003");
});
