# Auto Sage — Intelligent Car Fault Diagnosis System

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Rule-Based Automotive Fault Diagnosis & Maintenance Planning KBS  
**Domain:** Automotive Systems Diagnostics & Component Verification Engineering  

Auto Sage is an explainable, symptom-based **Knowledge-Based System (KBS)** for automotive fault diagnosis and workshop maintenance planning. Built for university demonstration and practical mechanical triage, it combines the original **Google Stitch** design system with a peer-reviewed automotive diagnostic dataset to isolate root causes through deterministic **propositional logic deduction** (Modus Ponens) and dynamic technician inquiry.

Auto Sage uses **strictly zero black-box machine learning**, **no opaque neural networks**, **no fabricated telemetry**, and **no fake confidence percentages**. Every diagnosis is formulated as an **unconfirmed candidate hypothesis** with explicit evidence tallies, requiring physical bench verification before component replacement.

---

## 1. System Architecture: A 3-Part Knowledge-Based System

Auto Sage adheres strictly to the classic separation of concerns defining expert systems:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          1. KNOWLEDGE BASE                             │
│       (backend/data/kbs_knowledge_base.json + Flowchart Assets)        │
│   • 8 Subsystem Categories (Brakes, Cooling, Electrical, Engine, etc.) │
│   • 93 Propositional Rules grounded in Zenodo research dataset         │
│   • 120 Canonical Driver-Observable Physical Symptoms                  │
│   • 4 Expert Sequential Diagnostic Decision Tree Flowcharts            │
│   • Complete Component Ontology, Safety Levels & Maintenance Directives│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         2. INFERENCE ENGINE                            │
│                    (backend/inference_engine.py)                       │
│   • Forward Chaining Deduction via Propositional Modus Ponens          │
│   • Dynamic Follow-Up Question Formulation (Discriminating Inquiry)    │
│   • Contradiction Refutation Engine (E => ~H refutes hypothesis)       │
│   • Deterministic Evidence Tally (No fake percentages or probabilities)│
│   • Multi-Candidate Differential Comparison Matrix                     │
│   • 9-Step Verifiable Reasoning Audit Trail                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        3. EXPLAINABLE USER UI                          │
│               (React 18 + Vite + Tailwind + Google Stitch)             │
│   • 5-Step Guided Stepper Workflow (Intake to Official Work Order)     │
│   • Clean Diagnosis Summary (Raw IF-THEN hidden in expandable details) │
│   • Interactive Follow-Up Questions (Yes / No / Not Sure / Skip)       │
│   • Tier A Verification Check Tables & Tier B Maintenance Directives   │
│   • One-Click Official PDF Generation & Browser Print Fallback         │
│   • Session Isolation & LocalStorage Quota Resilience                  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. University Academic Documentation (`docs/`)

Comprehensive academic documentation has been authored specifically for the **CT-359 Knowledge-Based Systems** course and examiners:

1. [**`docs/1_PROBLEM_ANALYSIS.md`**](file:///d:/CARFAULTDIA/docs/1_PROBLEM_ANALYSIS.md): Problem domain, automotive diagnostic challenges, safety-critical justification, and why black-box ML is rejected.
2. [**`docs/2_KNOWLEDGE_REPRESENTATION.md`**](file:///d:/CARFAULTDIA/docs/2_KNOWLEDGE_REPRESENTATION.md): (CLO 1) 8-level formal ontology, propositional logic syntax/semantics, rule modes (`ALL`, `ANY`, `PRIMARY_OR_PARTIAL`), and JSON schema.
3. [**`docs/3_INFERENCE_ENGINE_AND_METHODOLOGY.md`**](file:///d:/CARFAULTDIA/docs/3_INFERENCE_ENGINE_AND_METHODOLOGY.md): (CLO 3) Pure deterministic inference, Modus Ponens, dynamic follow-up questioning, contradiction handling, and 9-step reasoning trail.
4. [**`docs/4_SYSTEM_ARCHITECTURE.md`**](file:///d:/CARFAULTDIA/docs/4_SYSTEM_ARCHITECTURE.md): Client-server separation, REST API endpoints, 5-step stepper state machine, and session isolation.
5. [**`docs/5_SAFETY_AND_MAINTENANCE_GUIDE.md`**](file:///d:/CARFAULTDIA/docs/5_SAFETY_AND_MAINTENANCE_GUIDE.md): Risk stratification matrix, Tier A diagnostic bench check protocols, Tier B structured maintenance directives, and anti-mistake directives.
6. [**`docs/6_TESTING_AND_VALIDATION_REPORT.md`**](file:///d:/CARFAULTDIA/docs/6_TESTING_AND_VALIDATION_REPORT.md): Multi-layer testing matrix, test logs, edge case handling, and verification evidence.
7. [**`docs/7_VIVA_PREPARATION_AND_DEFENSE.md`**](file:///d:/CARFAULTDIA/docs/7_VIVA_PREPARATION_AND_DEFENSE.md): Top 10 viva questions and model answers tailored to CT-359 examiners.
8. [**`docs/8_RUBRIC_COMPLIANCE_MATRIX.md`**](file:///d:/CARFAULTDIA/docs/8_RUBRIC_COMPLIANCE_MATRIX.md): Point-by-point mapping of the implementation against CT-359 Course Learning Outcomes (CLO 1, CLO 2, CLO 3).

---

## 3. Dataset Provenance & Academic Citation

The knowledge base is built deterministically from the open research dataset:

- **Dataset Title**: *Automotive Faults Dataset for Diagnostic and Maintenance Systems*
- **Creators**: Peter Obike (Data Collector), Okure Obot (Data Curator)
- **Repository**: Zenodo
- **DOI**: `10.5281/zenodo.15626055` ([https://doi.org/10.5281/zenodo.15626055](https://doi.org/10.5281/zenodo.15626055))
- **Related Paper**: Obot, O., & Obike, P. (2024). *An Integrated Fuzzy-Rule and Case-Based Reasoning System for Enhanced Automobile Maintenance and Repair*. Journal of Engineering Research and Reports, 26(8), 433–445. DOI: `10.9734/jerr/2024/v26i81256`.
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Integrated Diagnostic Flowcharts**:
  1. `FC_BRAKES` (`brake_faults_flowchart.png`) — Brake Faults Diagnostic Flowchart
  2. `FC_ELECTRICAL` (`electrical_faults_flowchart.png`) — Dead Battery & Charging Circuit Flowchart
  3. `FC_OVERHEATING` (`engine_overheating_flowchart.png`) — Engine Overheating Decision Flowchart
  4. `FC_TRANSMISSION` (`transmission_faults_flowchart.png`) — Transmission Faults Diagnostic Flowchart

---

## 4. The 8 Supported Vehicle Subsystems

Auto Sage encompasses 93 distinct fault rules across 8 core automotive subsystems:

| Subsystem ID | System Name | Rules | Canonical Symptoms | Flowchart Available |
| :--- | :--- | :---: | :---: | :---: |
| `CAT_BRAKES` | Braking & ABS System | 10 | 14 | Yes (`FC_BRAKES`) |
| `CAT_COOLING` | Engine Cooling System | 9 | 12 | Yes (`FC_OVERHEATING`) |
| `CAT_ELECTRICAL` | Electrical & Charging System | 13 | 16 | Yes (`FC_ELECTRICAL`) |
| `CAT_EMISSIONS` | Exhaust & Emissions System | 9 | 11 | No |
| `CAT_ENGINE` | Engine Performance & Mechanical | 25 | 32 | No |
| `CAT_HVAC` | Heating, Ventilation & A/C | 6 | 8 | No |
| `CAT_STEERING` | Steering, Suspension & Tires | 6 | 9 | No |
| `CAT_TRANSMISSION`| Transmission & Driveline | 15 | 18 | Yes (`FC_TRANSMISSION`) |
| **Total** | **8 Subsystems** | **93 Rules** | **120 Canonical Symptoms** | **4 Flowcharts** |

---

## 5. The 5-Step Professional Diagnostic Workflow

Auto Sage features a guided 5-step diagnostic pipeline complete with a persistent Google Stitch progress stepper:

```text
[01 Vehicle Info] ──> [02 Symptoms] ──> [03 Dynamic Inquiry] ──> [04 Diagnosis Results] ──> [05 Report & Resolution]
```

### Step 1: Vehicle Information Intake (`VehicleInformation.jsx`)
- Entering vehicle details (Year, Make, Model, Mileage, Engine, Transmission, Fuel Type) is completely **optional**.
- Users can click **"Save & Continue to Symptoms"** or **"Skip vehicle details"** for instant diagnosis.
- Client-side validation prevents invalid year entries (accepts 1950 through current year + 1).

### Step 2: Problem Category & Symptom Selection (`SymptomSelection.jsx`)
- Categorized symptom picker with quick search filtering and pre-flight review modal.
- Enforces minimum 1 symptom requirement. Warns if only broad indicators (like "Check engine light") are selected.

### Step 3: Dynamic Follow-Up Inquiry (`FollowUpQuestions.jsx`)
- **Simulates a master technician asking targeted questions.**
- Generates 1 to 5 dynamic questions tailored to candidate rules matching the selected symptoms.
- Interactive Yes / No / Not Sure selection with a "Skip Questions" escape hatch.
- Answers provide corroborating or contradictory evidence to disambiguate competing root causes.

### Step 4: Diagnosis Results & Component Isolation (`DiagnosisResults.jsx`)
- **Clean Human-Centered Interface:** Hides raw propositional expressions inside an expandable technical block for evaluators.
- **Affected Component Spotlight:** Displays the primary affected mechanical/electrical component and subsystem.
- **Safety Priority Badges:** Categorizes risk into `Critical`, `High`, `Moderate`, or `Low`.
- **Structured Evidence Breakdown:** Categorizes findings into Supporting, Missing/Unverified, and Contradictory evidence.
- **Tier A Verification Checks:** Quantitative bench check procedures with normal and abnormal criteria.
- **Tier B Maintenance Directives:** Corrective actions, preventive measures, replacement criteria, and anti-mistake Do-Not-Replace directives.
- **Multi-Candidate Differential Comparison:** Side-by-side comparison matrix for competing candidates.
- **9-Step Reasoning Trail:** Collapsible audit trail of every stage evaluated by the inference engine.

### Step 5: Technical Work Order Dossier & PDF Export (`DiagnosticReport.jsx`)
- Printable workshop dossier featuring unique Report ID (`AS-YYYYMMDD-XXXX`).
- Follow-up inquiry Q&A record, component verification checklist, and technician signature block.
- **One-Click Official PDF Export** via `html2pdf.js` with auto-page breaks and clean styling.
- Native browser print fallback optimized for `@media print`.

---

## 6. Quick Start (Windows)

### Option A: One-Click Startup (Recommended)
Double-click `start.bat` in the project root folder. It will:
1. Verify Python and Node.js.
2. Install dependencies if missing.
3. Start the Flask backend on `http://127.0.0.1:5000`.
4. Start the Vite frontend on `http://127.0.0.1:5173`.
5. Open your default web browser to the dashboard once ready.

### Option B: Manual Startup in Two Terminals

#### Terminal 1 — Start the Python Flask Backend
```powershell
# Open terminal in project root: D:\CARFAULTDIA
.\.venv\Scripts\python.exe backend\app.py
```
Backend runs on `http://127.0.0.1:5000`.

#### Terminal 2 — Start the React/Vite Frontend
```powershell
cd frontend
npm install   # (only needed first time)
npm run dev
```
Frontend runs on `http://127.0.0.1:5173`.

---

## 7. Running Tests & Automated Validation

Auto Sage includes automated test suites for both backend and frontend:

### Backend Test Suite (29 Tests)
```powershell
# 1. Validate knowledge-base schema, attributes, and rule firings:
.\.venv\Scripts\python.exe backend\validate_knowledge_base.py

# 2. Run the Python unittest suite:
.\.venv\Scripts\python.exe -B -m unittest discover -s backend/tests -v
```

### Frontend Test Suite (13 Tests) & Production Bundling
```powershell
# 1. Run the headless Node.js test suite:
npm --prefix frontend test

# 2. Compile production bundle with Vite:
npm --prefix frontend run build
```

---

## 8. Safety & Ethical Disclaimers

1. **Unconfirmed Fault Candidates**: All faults identified by Auto Sage are hypotheses derived from symptom rules and dataset records. They do not constitute an official mechanical diagnosis.
2. **Mandatory Physical Inspection**: Never replace automotive parts solely based on software recommendations. Always perform the recommended physical checks or consult an ASE-certified technician.
3. **High Voltage & Safety Risks**: High-voltage electrical circuits (hybrid/EV), pressurized cooling systems, and brake hydraulic systems present severe injury risks. Adhere strictly to the safety precautions outlined in the Repair & Safety Guide.
