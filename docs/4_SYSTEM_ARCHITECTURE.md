# Auto Sage KBS — 4. System Architecture & Engineering Design

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Intelligent Automotive Fault Diagnosis System  

---

## 1. High-Level Architecture Overview

Auto Sage is engineered as a decoupled, professional web application following clean architectural separation of concerns:

```
┌───────────────────────────────────────────────────────────────────┐
│                     FRONTEND APPLICATION LAYER                    │
│   React 18 + Vite + Tailwind CSS + Google Stitch Design System    │
│                                                                   │
│  [Step 1: Vehicle] ──► [Step 2: Symptoms] ──► [Step 3: Questions] │
│                                                      │            │
│  [Step 5: Report]  ◄── [Step 4: Results]   ◄─────────┘            │
│                                                                   │
│  Local Session Management (historyStorage.js with Quota Recovery) │
│  Client-Side PDF Generation (html2pdf.js + Native Print Fallback) │
└─────────────────────────────────┬─────────────────────────────────┘
                                  │ JSON / REST HTTP API
                                  ▼
┌───────────────────────────────────────────────────────────────────┐
│                     BACKEND APPLICATION LAYER                     │
│                  Python 3.12 + Flask REST Engine                  │
│                                                                   │
│  [app.py] ── Flask API Routes & Input Validation                  │
│  [inference_engine.py] ── Deterministic Propositional Logic Engine│
│  [rule_enrichment.py] ── Domain Ontology & Maintenance Metadata   │
│  [build_kbs.py] ── Knowledge Base Builder & Schema Compiler       │
│  [validate_knowledge_base.py] ── Integrity & Schema Test Harness  │
└─────────────────────────────────┬─────────────────────────────────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE PERSISTENCE LAYER                    │
│                                                                   │
│  - kbs_knowledge_base.json (93 rules, 120 symptoms, 8 categories) │
│  - Flowchart PNG Assets (4 decision tree pathways)                │
│  - Zenodo Source Dataset (DOI: 10.5281/zenodo.15626055)           │
└───────────────────────────────────────────────────────────────────┘
```

---

## 2. REST API Specification

The backend exposes a deterministic, stateless REST API on `http://127.0.0.1:5000`:

### 2.1 Health Check
- **Endpoint:** `GET /api/health`
- **Response:**
  ```json
  {
    "status": "healthy",
    "engine": "Auto Sage KBS Deterministic Engine",
    "rules_loaded": 93,
    "categories_loaded": 8
  }
  ```

### 2.2 Subsystems Catalog
- **Endpoint:** `GET /api/categories`
- **Response:** Array of 8 subsystem objects containing `category_id`, `name`, `short_name`, `icon`, `rule_count`, `symptom_count`, `flowchart_id`, and `safety_note`.

### 2.3 Observable Symptoms
- **Endpoint:** `GET /api/symptoms?category=CAT_BRAKES`
- **Response:** Array of canonical symptom definitions for the requested category, each with `symptom_id`, `label`, and `category_id`.

### 2.4 Dynamic Follow-Up Questions (CLO 2)
- **Endpoint:** `POST /api/follow-up-questions`
- **Payload:**
  ```json
  {
    "category_id": "CAT_BRAKES",
    "symptom_ids": ["SYM_HARD_BRAKE_PEDAL"]
  }
  ```
- **Response:**
  ```json
  {
    "category_id": "CAT_BRAKES",
    "symptom_count": 1,
    "questions": [
      {
        "question_id": "q_booster_hiss",
        "question": "Do you hear an audible hissing sound near the driver footwell when the brake pedal is depressed?",
        "options": ["Yes", "No", "Not Sure"],
        "context": "An audible hiss inside the cabin indicates an internal booster vacuum seal rupture.",
        "relevant_faults": ["Possible brake booster vacuum or diaphragm failure"],
        "target_rule_ids": ["RULE_BRK_003"]
      }
    ],
    "candidate_count": 1
  }
  ```

### 2.5 Deterministic Diagnosis (CLO 3)
- **Endpoint:** `POST /api/diagnose`
- **Payload:**
  ```json
  {
    "category_id": "CAT_BRAKES",
    "symptom_ids": ["SYM_HARD_BRAKE_PEDAL"],
    "follow_up_answers": {
      "q_booster_hiss": "yes"
    }
  }
  ```
- **Response:**
  Returns full evaluation object with `matches`, `cross_category_matches`, `evaluated_rule_count`, `overall_safety_level`, `next_recommended_test`, `candidates_comparison`, and 9-step `reasoning_trail`.

### 2.6 Knowledge Base Introspection
- **Endpoint:** `GET /api/knowledge-base`
- **Response:** Full ontology dictionary including dataset provenance, exclusions, categories, canonical symptoms, and all 93 rules.

### 2.7 Flowchart Image Service
- **Endpoint:** `GET /api/flowcharts/<flowchart_id>`
- **Response:** Raw PNG image stream served from disk with caching headers.

---

## 3. Frontend Architecture & 5-Step Guided Stepper

The frontend is architected as an interactive Single-Page Application (SPA) driven by an intuitive 5-step stepper:

```
[01 Vehicle Info] ──► [02 Symptoms] ──► [03 Diagnostic Inquiry] ──► [04 Results] ──► [05 Report]
```

1. **Step 1: Vehicle Information (`VehicleInformation.jsx`):**
   Allows the user to input year, make, model, engine displacement, fuel type, transmission, and odometer reading. Fully optional with an explicit "Skip" action.
2. **Step 2: Category & Symptom Selection (`SymptomSelection.jsx`):**
   Categorized symptom picker with quick search filtering and review modal. Enforces minimum 1 symptom requirement.
3. **Step 3: Dynamic Follow-Up Inquiry (`FollowUpQuestions.jsx`):**
   Presents 1 to 5 dynamic questions tailored to candidate hypotheses matching the selected symptoms. Provides Yes / No / Not Sure options and a "Skip Questions" escape hatch.
4. **Step 4: Diagnosis Results (`DiagnosisResults.jsx`):**
   Presents candidate cards with Affected Components, Safety Badges, Evidence Breakdown, Tier A verification steps, Tier B maintenance actions, and candidate comparison tabs. **Crucially hides raw IF–THEN strings in an expandable Technical Details block.**
5. **Step 5: Diagnostic Technical Dossier (`DiagnosticReport.jsx`):**
   Printable and downloadable PDF work order featuring unique Report ID (`AS-YYYYMMDD-XXXX`), technician sign-off block, and complete provenance.

---

## 4. Local Storage Resilience & Session Isolation

The history subsystem in [`frontend/src/utils/historyStorage.js`](file:///d:/CARFAULTDIA/frontend/src/utils/historyStorage.js) implements robust storage guarantees:
- **Unique Report Identifiers:** Every diagnostic run receives a collision-proof ID based on timestamp and cryptographic random hex.
- **Strict Session Isolation:** Data from sequential vehicle diagnoses (e.g., car 1 Honda Civic vs. car 2 Ford F-150) never bleed into one another.
- **QuotaExceededError Recovery:** If browser `localStorage` approaches capacity, the manager progressively trims the oldest records (50 $\rightarrow$ 25 $\rightarrow$ 10 $\rightarrow$ 5 $\rightarrow$ 1) to ensure the current diagnosis is never lost.
- **Zero Telemetry / Total Privacy:** Runs entirely local to the user's browser without tracking or external servers.
