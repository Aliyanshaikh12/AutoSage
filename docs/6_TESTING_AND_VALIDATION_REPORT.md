# Auto Sage KBS — 6. Testing, Verification & Validation Report

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Intelligent Automotive Fault Diagnosis System  

---

## 1. Quality Assurance & Verification Methodology

To verify adherence to the university assignment requirements, Auto Sage underwent multi-layer automated testing across knowledge validation, backend inference deduction, REST API endpoints, frontend state management, and production bundling.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUALITY ASSURANCE MATRIX                        │
├───────────────────────────────┬────────────────────────────────────────┤
│ Layer 1: Knowledge Base       │ validate_knowledge_base.py (0 errors)  │
│ Layer 2: Inference Deduction  │ test_inference_engine.py (13 tests)    │
│ Layer 3: REST API Integration │ test_api.py (16 tests)                 │
│ Layer 4: Frontend State       │ node --test frontend/tests (13 tests)  │
│ Layer 5: Production Bundling  │ vite build (0 errors, code 0)          │
└───────────────────────────────┴────────────────────────────────────────┘
```

---

## 2. Test Execution & Evidence

### 2.1 Layer 1: Knowledge Base Schema & Integrity Validation
Command: `python backend/validate_knowledge_base.py`
- **Result:** PASSED with 0 errors.
- **Verification Checks:**
  - 93 unique rules with valid identifiers matching regex `^RULE_[A-Z]+_\d{3}$`.
  - 8 valid categories with active flowcharts where applicable.
  - 120 unique canonical symptoms with non-empty labels.
  - Every rule specifies non-empty `affected_component`, `subsystem`, `safety_level`, `required_expertise`, `required_tools`, `diagnostic_questions`, and `maintenance_actions`.
  - Every maintenance action defines `corrective_action`, `preventive_measure`, `replacement_criteria`, and `do_not_replace_warning`.
  - 4 flowchart image assets exist on disk in `backend/data/flowcharts/`.

### 2.2 Layer 2 & 3: Backend Unit & Integration Tests
Command: `python -m unittest backend/tests/test_inference_engine.py backend/tests/test_api.py`
- **Result:** `Ran 29 tests in 1.670s. OK`
- **Summary of Key Test Cases:**

| Test Identifier | Category | Verified Behavior | Status |
| :--- | :--- | :--- | :---: |
| `test_deterministic_full_match` | Inference | Returns exact full match for valid symptom set without variance. | **PASS** |
| `test_partial_match_partitioning` | Inference | Properly isolates partial candidate when only subset of symptoms observed. | **PASS** |
| `test_no_match_honest_reporting` | Inference | Accurately returns `status: "no_match"` when symptoms satisfy no rules. | **PASS** |
| `test_no_confidence_scores` | Ethics/Safety | Strictly asserts that no key containing `confidence` or `score` exists in response. | **PASS** |
| `test_enriched_attributes_present` | Ontology | Asserts presence of `affected_component`, `safety_level`, `maintenance_actions`, etc. | **PASS** |
| `test_get_follow_up_questions` | Inquiry | Extracts up to 5 discriminating questions matching candidate rules. | **PASS** |
| `test_follow_up_corroboration` | Inquiry | Elevates status to `Suspected Fault (Corroborated by Follow-up Evidence)` on affirmative answer. | **PASS** |
| `test_follow_up_contradiction` | Refutation | Refutes hypothesis to `Fault Not Supported by Evidence` on conflicting answer. | **PASS** |
| `test_reasoning_trail_generation` | Audit | Verifies 9 discrete logical stages in reasoning trail. | **PASS** |
| `test_multi_candidate_comparison` | Comparison | Generates side-by-side comparison matrix when multiple candidates exist. | **PASS** |
| `test_api_categories_and_symptoms`| REST API | `GET /api/categories` and `GET /api/symptoms` return compliant JSON. | **PASS** |
| `test_api_follow_up_endpoint` | REST API | `POST /api/follow-up-questions` validates input and returns questions. | **PASS** |
| `test_api_diagnose_endpoint` | REST API | `POST /api/diagnose` processes symptoms and follow-up answers cleanly. | **PASS** |
| `test_api_flowchart_image` | REST API | `GET /api/flowcharts/FC_BRAKES` streams PNG image with 200 OK. | **PASS** |

### 2.3 Layer 4: Frontend State & Storage Resilience Tests
Command: `npm --prefix frontend test`
- **Result:** `pass 13, fail 0, duration: 231ms`
- **Key Behaviors Verified:**
  - `historyStorage.test.js`: Verified saving of matched and no-match records, recent-first sorting, deletion, corrupted JSON recovery, and `QuotaExceededError` trimming fallback.
  - `kbsWorkflow.test.js`: Verified session isolation between sequential diagnoses, unique `AS-YYYYMMDD-XXXX` report ID generation, and full preservation of enriched academic fields (`affected_component`, `safety_level`, `maintenance_actions`, and `follow_up_answers`).

### 2.4 Layer 5: Production Build Verification
Command: `npm --prefix frontend run build`
- **Result:** `✓ built in 9.46s (code 0)`.
- **Assets Produced:**
  - `dist/index.html` (0.80 kB)
  - `dist/assets/index.css` (60.50 kB)
  - `dist/assets/index.js` (284.81 kB)
  - `dist/assets/html2pdf.js` (982.47 kB)

---

## 3. Boundary & Edge Case Analysis

1. **Empty / Null Input:**
   - Passing `symptom_ids: []` to `POST /api/diagnose` raises `HTTP 400 Bad Request` with message *"symptom_ids must be a non-empty list of valid symptom IDs."*
2. **Invalid Category:**
   - Passing an unmapped category (e.g. `CAT_ROCKET_PROPULSION`) raises `HTTP 400 Bad Request` with message *"Unknown category_id."*
3. **Contradictory Follow-Up Finding:**
   - When a user reports symptoms for a brake booster failure but indicates "No" to the cabin hissing question, the engine accurately demotes the candidate to `Fault Not Supported by Evidence`, listing the finding in `contradictory_evidence`.
4. **Browser Storage Exhaustion:**
   - Under simulated 5MB `localStorage` exhaustion, `saveDiagnosisToHistory()` progressively reduces older entries (from 50 down to 25, 10, 5, 1) rather than crashing or discarding the current diagnosis.
