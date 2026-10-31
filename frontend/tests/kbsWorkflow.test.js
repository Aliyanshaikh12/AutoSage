import test from "node:test";
import assert from "node:assert/strict";

import { flowchartUrl } from "../src/services/api.js";
import { escapeHtml, formatNumber, vehicleLabel, vehicleSecondary } from "../src/stitch/dom.js";
import {
  buildReviewPayloadFromEntry,
  createReportId,
  readHistoryRecords,
  saveDiagnosisToHistory,
} from "../src/utils/historyStorage.js";

function createMemoryStorage() {
  const store = new Map();
  return {
    getItem(key) {
      return store.has(key) ? store.get(key) : null;
    },
    setItem(key, value) {
      store.set(key, String(value));
    },
    removeItem(key) {
      store.delete(key);
    },
  };
}

test("flowchartUrl generates correct API endpoint", () => {
  assert.equal(flowchartUrl("FC_OVERHEATING"), "/api/flowcharts/FC_OVERHEATING");
  assert.equal(flowchartUrl("FC_BRAKES"), "/api/flowcharts/FC_BRAKES");
});

test("DOM formatting and vehicle helpers format correctly without fake defaults", () => {
  assert.equal(escapeHtml('<script>alert("x")</script>'), "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;");
  assert.equal(formatNumber(1250), "1,250");
  assert.equal(formatNumber(undefined), "—");

  assert.equal(vehicleLabel(null), "Vehicle not specified");
  assert.equal(vehicleLabel({ year: "2018", make: "Honda", model: "Civic" }), "2018 Honda Civic");

  assert.equal(vehicleSecondary(null), "Optional vehicle label not set.");
  assert.equal(
    vehicleSecondary({ engine: "2.0L", energy: "Gasoline", transmission: "Automatic" }),
    "2.0L • Gasoline • Automatic"
  );
});

test("saves and reloads new KBS diagnosis results with flowchart and structured evidence", () => {
  const storage = createMemoryStorage();
  const kbsResult = {
    status: "matched",
    category_id: "CAT_BRAKES",
    category_name: "Braking & ABS System",
    selected_symptoms: ["SYM_HARD_BRAKE_PEDAL"],
    selected_symptom_details: [
      { symptom_id: "SYM_HARD_BRAKE_PEDAL", label: "Hard brake pedal", text: "Hard brake pedal" },
    ],
    evaluated_rule_count: 10,
    match_count: 1,
    matches: [
      {
        rule_id: "RULE_BRK_003",
        title: "Brake Booster",
        possible_fault: "Possible brake booster issue",
        match_type: "full",
        match_strength: "strong",
        matched_symptoms: ["SYM_HARD_BRAKE_PEDAL"],
        matched_symptom_labels: ["Hard brake pedal"],
        missing_symptoms: [],
        missing_symptom_details: [],
        unaccounted_symptoms: [],
        rule_expression: 'IF "Hard brake pedal" THEN Possible Fault Candidate = "Brake Booster"',
        diagnosis_steps: [
          {
            step_number: 1,
            step: "Check brake booster vacuum hose",
            abnormal_result: "Leaking",
            normal_result: "Intact",
          },
        ],
        source_reference: {
          doi: "10.5281/zenodo.15626055",
          source_record_ids: ["SRC_JSON_003"],
        },
        related_flowchart: {
          flowchart_id: "FC_BRAKES",
          title: "Brake Faults Diagnostic Flowchart",
          image_url: "/api/flowcharts/FC_BRAKES",
        },
      },
    ],
    cross_category_matches: [],
    method: "Deterministic IF-THEN rule matching (no machine learning, no confidence scores).",
  };

  const outcome = saveDiagnosisToHistory(
    {
      categoryId: "CAT_BRAKES",
      categoryName: "Braking & ABS System",
      symptomIds: ["SYM_HARD_BRAKE_PEDAL"],
      symptomLabels: ["Hard brake pedal"],
      vehicleInfo: { year: "2015", make: "Toyota", model: "Corolla" },
      result: kbsResult,
    },
    storage
  );

  assert.equal(outcome.saved, true);
  assert.equal(outcome.records.length, 1);

  const read = readHistoryRecords(storage);
  assert.equal(read.records.length, 1);
  const entry = read.records[0];
  assert.equal(entry.categoryId, "CAT_BRAKES");
  assert.deepEqual(entry.symptomLabels, ["Hard brake pedal"]);
  assert.equal(entry.vehicleInfo.model, "Corolla");

  const reviewed = buildReviewPayloadFromEntry(entry);
  assert.equal(reviewed.status, "matched");
  assert.equal(reviewed.matches[0].rule_id, "RULE_BRK_003");
  assert.equal(reviewed.matches[0].related_flowchart.flowchart_id, "FC_BRAKES");
  assert.equal(reviewed.vehicle.make, "Toyota");
  assert.ok(entry.reportId.startsWith("AS-"));
  assert.equal(reviewed.report_id, entry.reportId);
});

test("createReportId produces valid AS-YYYYMMDD-XXXX identifiers", () => {
  const rid1 = createReportId();
  assert.match(rid1, /^AS-\d{8}-[A-Z0-9]{4}$/);

  const customDate = new Date("2026-10-29T12:00:00Z");
  const rid2 = createReportId(customDate);
  assert.match(rid2, /^AS-20261029-[A-Z0-9]{4}$/);
});

test("guarantees session isolation between sequential diagnoses", () => {
  const storage = createMemoryStorage();

  const car1 = {
    categoryId: "CAT_STARTING",
    categoryName: "Starting Problems",
    symptomIds: ["SYM_START_CLICK"],
    symptomLabels: ["Clicking sound"],
    vehicleInfo: { year: "2018", make: "Honda", model: "Civic" },
    result: {
      status: "matched",
      category_id: "CAT_STARTING",
      selected_symptoms: ["SYM_START_CLICK"],
      match_count: 1,
      matches: [{ rule_id: "RULE_START_001", possible_fault: "Weak battery" }],
    },
  };

  const car2 = {
    categoryId: "CAT_BRAKES",
    categoryName: "Brakes",
    symptomIds: ["SYM_SQUEAL"],
    symptomLabels: ["Squealing noise"],
    vehicleInfo: { year: "2021", make: "Ford", model: "F-150" },
    result: {
      status: "matched",
      category_id: "CAT_BRAKES",
      selected_symptoms: ["SYM_SQUEAL"],
      match_count: 1,
      matches: [{ rule_id: "RULE_BRK_001", possible_fault: "Worn brake pads" }],
    },
  };

  const save1 = saveDiagnosisToHistory(car1, storage);
  assert.equal(save1.saved, true);

  const save2 = saveDiagnosisToHistory(car2, storage);
  assert.equal(save2.saved, true);

  const history = readHistoryRecords(storage).records;
  assert.equal(history.length, 2);

  // Recent first: car2 is [0], car1 is [1]
  assert.equal(history[0].vehicleInfo.make, "Ford");
  assert.equal(history[0].vehicleInfo.model, "F-150");
  assert.equal(history[0].categoryId, "CAT_BRAKES");
  assert.notEqual(history[0].id, history[1].id);
  assert.notEqual(history[0].reportId, history[1].reportId);

  assert.equal(history[1].vehicleInfo.make, "Honda");
  assert.equal(history[1].vehicleInfo.model, "Civic");
  assert.equal(history[1].categoryId, "CAT_STARTING");

  // Verify review payloads preserve individual vehicle and report identities
  const review1 = buildReviewPayloadFromEntry(history[1]);
  assert.equal(review1.vehicle.make, "Honda");
  assert.equal(review1.report_id, history[1].reportId);

  const review2 = buildReviewPayloadFromEntry(history[0]);
  assert.equal(review2.vehicle.make, "Ford");
  assert.equal(review2.report_id, history[0].reportId);
});

test("preserves enriched academic fields: follow-up answers, affected component, and maintenance actions", () => {
  const storage = createMemoryStorage();
  const enrichedResult = {
    status: "matched",
    category_id: "CAT_BRAKES",
    category_name: "Braking & ABS System",
    selected_symptoms: ["SYM_HARD_BRAKE_PEDAL"],
    selected_symptom_details: [{ symptom_id: "SYM_HARD_BRAKE_PEDAL", label: "Hard brake pedal" }],
    evaluated_rule_count: 10,
    match_count: 1,
    overall_safety_level: "Critical",
    follow_up_answers: { q_booster_hiss: "yes" },
    matches: [
      {
        rule_id: "RULE_BRK_003",
        title: "Brake Booster",
        possible_fault: "Possible brake booster vacuum or diaphragm failure",
        affected_component: "Vacuum Brake Power Booster & Check Valve Assembly",
        subsystem: "Braking & Hydraulic Control Subsystem",
        safety_level: "Critical",
        required_expertise: "Certified Brake Technician",
        required_tools: ["Vacuum Gauge (0-30 in-Hg)", "Hand Vacuum Pump"],
        match_type: "full",
        diagnosis_status: "Suspected Fault (Corroborated by Follow-up Evidence)",
        maintenance_actions: {
          corrective_action: "Perform vacuum decay test; inspect one-way valve.",
          preventive_measure: "Inspect booster vacuum hose every 30,000 miles.",
          replacement_criteria: "Replace booster assembly if diaphragm leaks.",
          do_not_replace_warning: "Do not replace booster without checking vacuum supply.",
        },
      },
    ],
    candidates_comparison: [],
    reasoning_trail: [{ step: 1, name: "Intake", details: "Processed" }],
  };

  const outcome = saveDiagnosisToHistory(
    {
      categoryId: "CAT_BRAKES",
      categoryName: "Braking & ABS System",
      symptomIds: ["SYM_HARD_BRAKE_PEDAL"],
      symptomLabels: ["Hard brake pedal"],
      vehicleInfo: { year: "2018", make: "Subaru", model: "Outback" },
      followUpAnswers: { q_booster_hiss: "yes" },
      result: enrichedResult,
    },
    storage
  );

  assert.equal(outcome.saved, true);
  const reviewed = buildReviewPayloadFromEntry(outcome.records[0]);
  assert.equal(reviewed.overall_safety_level, "Critical");
  assert.equal(reviewed.matches[0].affected_component, "Vacuum Brake Power Booster & Check Valve Assembly");
  assert.equal(reviewed.matches[0].safety_level, "Critical");
  assert.equal(reviewed.matches[0].maintenance_actions.corrective_action, "Perform vacuum decay test; inspect one-way valve.");
  assert.equal(reviewed.follow_up_answers.q_booster_hiss, "yes");
});
