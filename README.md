# Auto Sage — Intelligent Automotive Fault Diagnosis System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-lightgrey.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0%2B-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4%2B-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Dataset DOI](https://img.shields.io/badge/Dataset-10.5281%2Fzenodo.15626055-0298c3.svg?logo=zenodo&logoColor=white)](https://doi.org/10.5281/zenodo.15626055)
[![License](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Repository Visibility](https://img.shields.io/badge/Visibility-Public-green.svg)](https://github.com/Aliyanshaikh12/AutoSage)

> **Auto Sage** is an explainable, deterministic **Knowledge-Based System (KBS)** for automotive fault diagnosis and workshop maintenance planning. Developed for the **Knowledge-Based Systems (CT-359)** course at **NED University of Engineering & Technology**, it combines an empirical peer-reviewed automotive dataset with forward-chaining propositional logic deduction (*Modus Ponens*) and dynamic technician inquiry to isolate mechanical and electrical root causes with transparent verification checks.

---

## Table of Contents

1. [System Overview & Philosophy](#1-system-overview--philosophy)
2. [Key Capabilities & Innovations](#2-key-capabilities--innovations)
3. [Knowledge-Based System Architecture](#3-knowledge-based-system-architecture)
4. [Supported Subsystems & Knowledge Base](#4-supported-subsystems--knowledge-base)
5. [User Workflow & Guided Stepper](#5-user-workflow--guided-stepper)
6. [Technology Stack](#6-technology-stack)
7. [Project Directory Layout](#7-project-directory-layout)
8. [REST API Specification](#8-rest-api-specification)
9. [Installation & Getting Started](#9-installation--getting-started)
10. [Automated Testing & Verification](#10-automated-testing--verification)
11. [Academic Dataset Attribution & Provenance](#11-academic-dataset-attribution--provenance)
12. [Project Contributors](#12-project-contributors)
13. [Limitations & Ethical Disclaimers](#13-limitations--ethical-disclaimers)

---

## 1. System Overview & Philosophy

Modern automotive systems are complex assemblies of interdependent mechanical, electrical, and hydraulic subsystems. When vehicle owners or apprentice technicians face abnormal noises, fluid leaks, or performance drops, traditional diagnostic approaches often suffer from two extremes:

- **Trial-and-Error Component Swapping:** Costly and dangerous replacement of parts without root cause confirmation.
- **Opaque Black-Box Machine Learning:** Neural network models that output probability numbers without physical explanations, audit trails, or verifiable bench testing procedures.

### Core Engineering Principles

1. **Deterministic Propositional Deduction:** Auto Sage applies classical propositional logic ($$P \land Q \implies R$$) via forward chaining (*Modus Ponens*). Every diagnostic conclusion is mathematically derived from explicit premise satisfaction.
2. **Strictly Zero Black-Box ML / Fake Probabilities:** Auto Sage rejects synthetic confidence percentages. Diagnoses are formulated as **unconfirmed candidate hypotheses** paired with an exact tally of observed physical evidence ($k / n$ matching symptoms).
3. **Hypothesis Formulation vs. Final Judgment:** A software system cannot turn a wrench. Auto Sage provides an initial triage and issues mandatory **Tier A physical verification checks** that must be physically performed on the vehicle before ordering parts.
4. **Contradiction Refutation:** Follow-up technician inquiries can actively refute competing candidates through negative evidence rules ($E \implies \neg H$), eliminating false positives.

---

## 2. Key Capabilities & Innovations

- **8 Automotive Subsystems:** Covers engine mechanical, cooling, electrical/charging, brakes/ABS, transmission/driveline, emissions/exhaust, HVAC, and steering/suspension.
- **93 Empirical Production Rules:** Derived directly from real-world repair workshop cases published in peer-reviewed automotive research.
- **120 Canonical Physical Symptoms:** High-precision driver-observable symptoms mapped to specific mechanical phenomena.
- **4 Integrated Decision Tree Flowcharts:** Complete sequential diagnostic pathways for critical systems:
  - `FC_BRAKES` — Brake hydraulic and booster fault resolution.
  - `FC_ELECTRICAL` — Dead battery, parasitic draw, and alternator charging circuit.
  - `FC_OVERHEATING` — Engine cooling circuit and thermostat isolation.
  - `FC_TRANSMISSION` — Automatic/manual transmission slip and shudder analysis.
- **Two-Tier Guidance Architecture:**
  - **Tier A (Diagnostic Bench Verification):** Quantitative, step-by-step physical test procedures with specified normal vs. abnormal thresholds (multimeter readings, pressure tests, visual checks).
  - **Tier B (Maintenance & Repair Directives):** Corrective actions, preventive maintenance measures, replacement criteria, and anti-mistake *"Do-Not-Replace"* directives.
- **4-Tier Roadworthiness Hierarchy:** Transparent safety risk classification (`Critical`, `High`, `Moderate`, `Low`) indicating whether the vehicle may be safely operated or must be towed.
- **Professional Diagnostic Dossier Export:** One-click generation of an official printable service report (`AS-YYYYMMDD-XXXX`) with technician signature blocks and complete Q&A audit records.

---

## 3. Knowledge-Based System Architecture

Auto Sage adheres strictly to the classic tripartite architecture of Knowledge-Based Systems:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          1. KNOWLEDGE BASE                             │
│       (backend/data/kbs_knowledge_base.json + Flowchart Assets)        │
│   • 8 Subsystem Categories (Brakes, Cooling, Electrical, Engine, etc.) │
│   • 93 Propositional Rules grounded in Zenodo research dataset         │
│   • 120 Canonical Driver-Observable Physical Symptoms                  │
│   • 4 Expert Sequential Diagnostic Decision Tree Flowcharts            │
│   • Component Ontologies, Safety Tiers & Anti-Mistake Directives       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         2. INFERENCE ENGINE                            │
│                    (backend/inference_engine.py)                       │
│   • Forward Chaining Deduction via Propositional Modus Ponens          │
│   • Dynamic Follow-Up Question Formulation (Discriminating Inquiry)    │
│   • Contradiction Refutation Engine (E => ~H refutes hypothesis)       │
│   • Deterministic Evidence Tally (No synthetic probabilities)          │
│   • Multi-Candidate Differential Comparison Matrix                     │
│   • 9-Step Verifiable Reasoning Audit Trail                            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        3. EXPLAINABLE USER UI                          │
│               (React 18 + Vite + Tailwind CSS + Google Stitch)         │
│   • 5-Step Guided Stepper Workflow (Intake to Official Work Order)     │
│   • Human-Centered Diagnosis Cards (Raw logic in expandable panels)    │
│   • Interactive Follow-Up Questions (Yes / No / Not Sure / Skip)       │
│   • Quantitative Bench Check Tables & Maintenance Directives           │
│   • One-Click Official PDF Generation (html2pdf.js + print fallback)   │
│   • Session Isolation & LocalStorage Quota Resilience                  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Supported Subsystems & Knowledge Base

| Category ID | Subsystem Name | Rules | Canonical Symptoms | Decision Flowchart |
| :--- | :--- | :---: | :---: | :---: |
| `CAT_BRAKES` | Braking & ABS System | 10 | 14 | `FC_BRAKES` (Available) |
| `CAT_COOLING` | Engine Cooling System | 9 | 12 | `FC_OVERHEATING` (Available) |
| `CAT_ELECTRICAL` | Electrical & Charging System | 13 | 16 | `FC_ELECTRICAL` (Available) |
| `CAT_EMISSIONS` | Exhaust & Emissions System | 9 | 11 | Sequential Logic |
| `CAT_ENGINE` | Engine Performance & Mechanical | 25 | 32 | Sequential Logic |
| `CAT_HVAC` | Heating, Ventilation & A/C | 6 | 8 | Sequential Logic |
| `CAT_STEERING` | Steering, Suspension & Tires | 6 | 9 | Sequential Logic |
| `CAT_TRANSMISSION` | Transmission & Driveline | 15 | 18 | `FC_TRANSMISSION` (Available) |
| **Total** | **8 Subsystems** | **93 Rules** | **120 Symptoms** | **4 Flowcharts** |

---

## 5. User Workflow & Guided Stepper

Auto Sage guides users through an intuitive 5-step diagnostic process:

```text
[01 Vehicle Info] ──> [02 Symptoms] ──> [03 Dynamic Inquiry] ──> [04 Diagnosis Results] ──> [05 Report & Resolution]
```

1. **Vehicle Intake (`VehicleInformation.jsx`):** Enter optional vehicle specifications (Year, Make, Model, Mileage, Engine, Transmission, Fuel Type) or proceed immediately with one-click quick triage.
2. **Symptom Selection (`SymptomSelection.jsx`):** Select observable anomalies categorized by system with real-time text filtering and multi-symptom staging.
3. **Dynamic Follow-Up Inquiry (`FollowUpQuestions.jsx`):** System generates 1 to 5 dynamic questions targeting competing candidate rules to gather corroborating or refuting evidence.
4. **Diagnosis & Component Isolation (`DiagnosisResults.jsx`):** Presents ranked candidate fault hypotheses, affected components, roadworthiness safety badge, structured evidence breakdown, Tier A verification protocols, and side-by-side differential comparison.
5. **Dossier & Work Order Export (`DiagnosticReport.jsx`):** Generates an automotive service report complete with Report ID, vehicle details, inquiry log, checklist, and PDF export.

---

## 6. Technology Stack

- **Backend:**
  - **Runtime:** Python 3.10+
  - **Web Framework:** Flask 3.0+
  - **CORS Support:** Flask-CORS
  - **Inference Engine:** Pure standard-library Python (deterministic forward chaining, zero heavy external ML dependencies)
- **Frontend:**
  - **Framework:** React 18.3
  - **Build Tool:** Vite 5.0+
  - **Styling:** Tailwind CSS 3.4
  - **Icons:** Lucide React
  - **PDF Generation:** html2pdf.js with native CSS `@media print` fallback
- **Data & Standards:**
  - JSON-based knowledge base (`kbs_knowledge_base.json`)
  - RESTful HTTP API with JSON payloads
  - CC BY 4.0 open scientific data provenance

---

## 7. Project Directory Layout

```text
AutoSage/
├── backend/
│   ├── app.py                      # Flask REST API server and route handlers
│   ├── inference_engine.py         # Forward-chaining deduction engine & Modus Ponens
│   ├── validate_knowledge_base.py  # Standalone KB integrity and rule validator
│   ├── requirements.txt            # Python backend dependencies
│   ├── data/
│   │   ├── kbs_knowledge_base.json # 93 rules, 120 symptoms, 8 subsystems, ontologies
│   │   └── flowcharts/             # High-resolution decision flowchart PNG assets
│   └── tests/
│       └── test_inference_engine.py# 29 automated unittests covering all engine paths
├── frontend/
│   ├── index.html                  # Single Page Application HTML shell
│   ├── package.json                # Node.js dependencies & scripts
│   ├── vite.config.js              # Vite bundler configuration & local proxy
│   ├── tailwind.config.js          # Tailwind CSS styling design system
│   ├── public/
│   │   ├── favicon.ico
│   │   └── images/                 # Automotive HUD visuals and system branding
│   └── src/
│       ├── App.jsx                 # Root component, routing, and shared state
│       ├── main.jsx                # Application DOM entrypoint
│       ├── index.css               # Global typography and print stylesheet
│       ├── api.js                  # Frontend-to-backend REST API integration
│       ├── components/             # Reusable UI components (Navbar, Stepper, Modal, etc.)
│       ├── pages/                  # 5-step diagnostic workflow pages & views
│       └── tests/                  # Headless Node.js unit tests (13 tests)
├── docs/                           # Comprehensive academic documentation (CLO 1-3)
│   ├── 1_PROBLEM_ANALYSIS.md
│   ├── 2_KNOWLEDGE_REPRESENTATION.md
│   ├── 3_INFERENCE_ENGINE_AND_METHODOLOGY.md
│   ├── 4_SYSTEM_ARCHITECTURE.md
│   ├── 5_SAFETY_AND_MAINTENANCE_GUIDE.md
│   ├── 6_TESTING_AND_VALIDATION_REPORT.md
│   ├── 7_VIVA_PREPARATION_AND_DEFENSE.md
│   └── 8_RUBRIC_COMPLIANCE_MATRIX.md
├── final_report/                   # University Project Report Submission
│   ├── Auto_Sage_Final_Project_Report.docx  # Formatted Word submission
│   ├── Auto_Sage_Final_Project_Report.pdf   # Print-ready master PDF report
│   ├── diagrams/                   # Architectural, DFD, and Use Case diagrams
│   └── screenshots/                # High-fidelity system screenshots
├── start.bat                       # One-click Windows development startup script
├── .gitignore                      # Git exclusion rules for clean version control
└── README.md                       # Master project overview and engineering manual
```

---

## 8. REST API Specification

The Flask backend runs on `http://127.0.0.1:5000` and exposes the following endpoints:

| Method | Endpoint | Description | Request Body / Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status, KB loadability, and dataset metadata | None |
| `GET` | `/api/categories` | Lists all 8 vehicle subsystems with descriptions and rule counts | None |
| `GET` | `/api/symptoms` | Retrieves canonical symptoms (filter by `?category=CAT_ID`) | `?category=` (Optional) |
| `POST` | `/api/follow-up-questions` | Generates discriminating questions for candidate rules | `{"category_id": "...", "symptom_ids": [...]}` |
| `POST` | `/api/diagnose` | Executes forward-chaining deduction and returns fault hypotheses | `{"category_id": "...", "symptom_ids": [...], "follow_up_answers": {...}}` |
| `GET` | `/api/knowledge-base` | Returns complete schema, rule definitions, and metadata | None |
| `GET` | `/api/flowcharts/<id>` | Serves diagnostic decision tree PNG (`FC_BRAKES`, etc.) | URL path parameter |

---

## 9. Installation & Getting Started

### Prerequisites

- **Python:** Version 3.10 or higher
- **Node.js:** Version 18.0 or higher (with `npm`)
- **Git:** Version 2.40 or higher

### Option A: One-Click Startup (Recommended on Windows)

Double-click `start.bat` in the project root directory. The script automatically:
1. Validates Python and Node.js environments.
2. Installs required packages if missing.
3. Launches the Flask backend on port `5000`.
4. Launches the Vite development server on port `5173`.
5. Opens the application in your default web browser.

### Option B: Manual Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Aliyanshaikh12/AutoSage.git
cd AutoSage
```

#### 2. Configure Backend
```bash
# Create and activate Python virtual environment
python -m venv .venv

# Windows activation
.\.venv\Scripts\activate

# Linux / macOS activation
# source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Start the Flask API server
python backend/app.py
```
*Backend runs at `http://127.0.0.1:5000`.*

#### 3. Configure Frontend
```bash
# Open a new terminal in the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```
*Frontend runs at `http://127.0.0.1:5173`.*

---

## 10. Automated Testing & Verification

Auto Sage includes comprehensive multi-layer automated test suites for both backend logic and frontend presentation:

### Backend Test Suite (29 Unit Tests)
```bash
# 1. Run the Knowledge Base validation suite:
python backend/validate_knowledge_base.py

# 2. Run the unittest engine test suite:
python -B -m unittest discover -s backend/tests -v
```

### Frontend Test Suite (13 Headless Tests) & Production Bundle
```bash
# 1. Run headless frontend component tests:
npm --prefix frontend test

# 2. Verify production bundle compilation:
npm --prefix frontend run build
```

---

## 11. Academic Dataset Attribution & Provenance

The rules, symptom definitions, and fault taxonomies in Auto Sage are grounded in open scientific automotive research:

- **Dataset Title:** *Automotive Faults Dataset for Diagnostic and Maintenance Systems*
- **Authors & Curators:** Peter Obike (Data Collector), Okure Obot (Data Curator)
- **Repository:** Zenodo
- **Digital Object Identifier (DOI):** [`10.5281/zenodo.15626055`](https://doi.org/10.5281/zenodo.15626055)
- **Primary Scientific Paper:**  
  Obot, O., & Obike, P. (2024). *An Integrated Fuzzy-Rule and Case-Based Reasoning System for Enhanced Automobile Maintenance and Repair*. *Journal of Engineering Research and Reports*, 26(8), 433–445. [DOI: 10.9734/jerr/2024/v26i81256](https://doi.org/10.9734/jerr/2024/v26i81256)
- **Licensing:** Creative Commons Attribution 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/))

---

## 12. Project Contributors

This system was engineered as a semester capstone project for **CT-359 Knowledge-Based Systems** at **NED University of Engineering & Technology**, Karachi:

- **Aliyan Shaikh** (Lead Engineer & Knowledge Architect) — [@Aliyanshaikh12](https://github.com/Aliyanshaikh12)
- **Talal Tariq** (Systems & UI/UX Engineer)
- **Muhammad Hasan** (Research & Diagnostics Specialist)

*Department of Computer Science & Information Technology, NED University of Engineering & Technology.*

---

## 13. Limitations & Ethical Disclaimers

1. **Software Hypotheses vs. Official Diagnosis:** Fault candidates identified by Auto Sage represent logical hypotheses derived from reported symptoms. They do not substitute for on-site physical inspection by certified automotive technicians.
2. **Mandatory Physical Verification:** Component replacement must never occur based solely on algorithmic output. Mandatory Tier A bench tests (e.g., multimeter voltage drop, pressure testing, fluid visual inspection) must corroborate the hypothesis.
3. **Safety-Critical Hazards:** Working on vehicles carries inherent hazards including high voltage (EV/HEV circuits), boiling pressurized coolant, flammable petroleum products, and hydraulic pressure. Strictly follow workshop safety protocols.
4. **Scope of Deduction:** The system operates strictly within its verified 93-rule knowledge base. Rare, novel, or multi-compound cascading failures outside the knowledge graph are escalated to human master technician review.
