========================================================================================
AUTO SAGE — INTELLIGENT CAR FAULT DIAGNOSIS SYSTEM
COMPLEX COMPUTING PROBLEM (CCP) FINAL PROJECT SUBMISSION PACKAGE
========================================================================================

DEPARTMENT OF COMPUTER SCIENCE AND INFORMATION TECHNOLOGY
NED UNIVERSITY OF ENGINEERING AND TECHNOLOGY, KARACHI

Course Code & Title: CT-359 — Knowledge-Based Systems (KBS)
Academic Year:       2026

STUDENT DETAILS:
----------------------------------------------------------------------------------------
1. Name: ALIYAN SHAIKH      Roll Number: CT-24252
2. Name: TALAL TARIQ        Roll Number: CT-24298
3. Name: MUHAMMAD HASAN     Roll Number: CT-24291

PROJECT OVERVIEW:
----------------------------------------------------------------------------------------
Auto Sage is a symptom-based automotive fault diagnosis Knowledge-Based System (KBS).
It models vehicle subsystems, mechanical/electrical components, symptoms, faults, 
and guided repair interventions using propositional logic rules and a deterministic,
explainable forward-chaining inference engine.

The system addresses Course Learning Outcomes (CLOs):
- CLO 1: Knowledge Representation (Automotive Subsystems, Components, Symptoms, Rules)
- CLO 2: Knowledge Engineering, Inference Engine Design & Forward-Chaining Architecture
- CLO 3: Explainable Reasoning, Evidence Breakdown, and Safety & Repair Guidance

DELIVERABLE FILES IN THIS PACKAGE:
----------------------------------------------------------------------------------------
1. Auto_Sage_Final_Project_Report.pdf (1.89 MB, Exactly 20 Pages)
   - Final submission-ready, print-quality PDF compiled via Microsoft Word rendering engine.
   - Formatted strictly according to 'KBS CCP Report Template.pdf'.
   - Page-by-Page Layout Structure:
     * Page 01: Cover / Title Page with NED Logo, Title Box & Student Details Table
     * Page 02: Executive Summary & Section 1: Project Instructions
     * Page 03: Section 2: Problem Statement (CLO 1, CLO 2, CLO 3 Mappings)
     * Page 04: Section 3: Problem Description / Project Context (Two Formal Paragraphs)
     * Page 05: Section 4: Problem Analysis (4.1 to 4.5: Understanding, Stakeholders, FR/NFR, Assumptions)
     * Page 06: Section 5: Knowledge Representation Formalism & Table 1 (All 8 Subsystems)
     * Page 07: Section 5.3–5.5: Inference Mechanism, 9-Step Reasoning Trail, Evidence Formula, Explanation
     * Page 08: Section 5.6: Architectural Modeling (Figure 1 Architecture & Figure 2 Inference Flowchart)
     * Page 09: Section 5.6: Architectural Modeling (Figure 3 UML Use Case & Figure 4 DFD Level-1)
     * Page 10: Section 6: Dataset Attribution (Table 2 AKTC/Zenodo) & Section 7.1–7.2 Implementation Stack
     * Page 11: Section 7.3: UX Modules 1 & 2 (Figure 5 Dashboard & Figure 6 Vehicle Intake)
     * Page 12: Section 7.3: UX Modules 3 & 4 (Figure 7 Symptom Selection & Figure 8 Clarification Inquiries)
     * Page 13: Section 7.3: UX Modules 5 & 6 (Figure 9 Diagnosis Results & Figure 10 Evidence Breakdown)
     * Page 14: Section 7.3: UX Modules 7 & 8 (Figure 11 Component Details & Figure 12 Repair Guide)
     * Page 15: Section 7.3: UX Modules 9 & 10 (Figure 13 Safety Guide & Figure 14 Session History)
     * Page 16: Section 7.3–7.4: UX Module 11 (Figure 15 Printable Report Dossier) & Explainability Facility
     * Page 17: Section 8: Testing & Results (8.1 42 Automated Tests & Table 3 Subsystem Verification Matrix)
     * Page 18: Section 8.3: Three Real Diagnosis Scenarios (Full Match, Partial/Refutation, No-Match)
     * Page 19: Section 9: Evaluation, Limitations (4 items), Future Work (3 items), and Conclusion
     * Page 20: Section 10: References ([1] to [8] IEEE) & Academic Project Viva Evaluation Rubric Grid

2. Auto_Sage_Final_Project_Report.docx (2.18 MB)
   - Fully editable Microsoft Word document matching the exact template layout,
     academic styles (NED Deep Navy Headings #0F294A, Charcoal Body Text #1E293B,
     0.9" margins, 1.12 line spacing, running header/footer with dynamic 'Page X of 20').

3. screenshots/ (11 genuine high-resolution UI captures of the running application):
   - 01_dashboard.png               : Home dashboard with system health & category tiles
   - 02_vehicle_information.png     : Year/Make/Model intake form with skip fallback
   - 03_symptom_selection.png       : Interactive symptom picker with category filtering
   - 04_followup_questions.png      : Dynamic clarification questions with reasoning
   - 05_diagnosis_results.png       : Deterministic fault diagnosis ranking & tier badges
   - 06_evidence_breakdown.png      : Explanations (supporting, missing, contradictory)
   - 07_fault_details.png           : Detailed component view, severity, driving risk
   - 08_repair_mitigation_guide.png : Step-by-step repair steps & anti-mistake warnings
   - 09_safety_guide.png            : Roadside emergency protocol & driving hazard warnings
   - 10_diagnostic_report.png       : Multi-page printable diagnostic report
   - 11_diagnosis_history.png       : LocalStorage session history with past queries

4. diagrams/ (8 technical architectural and decision flowchart diagrams):
   - 01_system_architecture.png     : Multi-tier architectural overview (React + Flask)
   - 02_inference_flowchart.png     : 9-step forward-chaining inference pipeline
   - 03_use_case_diagram.png        : UML use cases for vehicle owners & technicians
   - 04_dfd_diagram.png             : Level-1 Data Flow Diagram (DFD)
   - brake_faults_flowchart.png     : Decision tree flowchart for braking system faults
   - electrical_faults_flowchart.png: Decision tree flowchart for battery/alternator
   - engine_overheating_flowchart.png: Decision tree flowchart for cooling system faults
   - transmission_faults_flowchart.png: Decision tree flowchart for transmission faults
   - ned_logo_0.png                 : Official NED University emblem extracted from template

SOURCE CODE & RUNNING INSTRUCTIONS:
----------------------------------------------------------------------------------------
Prerequisites:
- Python 3.10+ (with virtual environment at .venv/)
- Node.js 18+ & npm

To Run the Backend:
  cd D:\AUTOSAGE
  .\.venv\Scripts\activate
  python backend/app.py
  (Runs on http://127.0.0.1:5000)

To Run the Frontend:
  cd D:\AUTOSAGE
  npm run dev
  (Runs on http://localhost:5173)

To Run Automated KBS Test Suite:
  cd D:\AUTOSAGE
  .\.venv\Scripts\python.exe -m pytest tests/test_inference.py tests/test_kb_integrity.py -v

KNOWLEDGE BASE & DATASET ATTRIBUTION:
----------------------------------------------------------------------------------------
Primary Empirical Dataset:
- Title: Automotive Faults Dataset for Diagnostic and Maintenance Systems
- Authors: Obike, C., & Obot, O. (2024)
- DOI: 10.5281/zenodo.15626055
- Open-access research corpus covering engine, electrical, cooling, brake, and transmission
  subsystems across real-world automotive failure modes.

========================================================================================
Generated on: November 1, 2026
========================================================================================
