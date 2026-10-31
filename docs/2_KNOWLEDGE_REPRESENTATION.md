# Auto Sage KBS — 2. Knowledge Representation & Formal Ontology

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Intelligent Automotive Fault Diagnosis System  
**Academic Alignment:** CLO 1 — Knowledge Representation  

---

## 1. Domain Ontology Architecture

To satisfy **CLO 1**, Auto Sage models the complete domain ontology of modern automotive diagnostics across an 8-level conceptual hierarchy:

```
[Vehicle Subsystem] (e.g., Braking & Hydraulic Control)
        │
        ▼
[Affected Component] (e.g., Vacuum Brake Booster Assembly)
        │
        ▼
[Observable Symptoms] (e.g., Hard brake pedal, Hissing acoustic noise)
        │
        ▼
[Root Cause] (e.g., Ruptured rubber booster diaphragm / loss of manifold vacuum)
        │
        ▼
[Candidate Fault Hypothesis] (e.g., Brake Booster Vacuum/Diaphragm Failure)
        │
        ▼
[Diagnostic Evidence] (Supporting, Missing, Contradictory findings)
        │
        ▼
[Tier A Verification Tests] (e.g., Vacuum Decay Gauge Test: 18-22 in-Hg normal)
        │
        ▼
[Tier B Maintenance Actions] (Corrective, Preventive, Replacement Criteria, Do-Not-Replace Directive)
```

---

## 2. Formal Propositional Logic Representation

Auto Sage formalizes automotive diagnostics using classical propositional logic. Every fault candidate is evaluated against strict truth assignments:

### 2.1 Proposition Syntax and Semantics
Let $S = \{s_1, s_2, \dots, s_n\}$ represent the universe of discrete, observable vehicle symptoms where each proposition $s_i \in \{\text{True}, \text{False}\}$.
- $s_i = \text{True} \iff$ The driver/technician reports observing symptom $s_i$.
- $s_i = \text{False} \iff$ Symptom $s_i$ is unobserved or unselected.

Let $Q = \{q_1, q_2, \dots, q_m\}$ represent dynamic follow-up inquiry propositions where each $q_j \in \{\text{Yes}, \text{No}, \text{Not Sure}, \text{Unanswered}\}$.
- $q_j = \text{Supporting Answer} \implies$ Corroborates hypothesis $H_k$.
- $q_j = \text{Contradictory Answer} \implies \neg H_k$ (Refutation).

### 2.2 Logic Modes for Rule Premises

Each rule $R_k$ in the knowledge base is defined with an explicit logical premise evaluation mode:

1. **Strict Conjunction (`ALL` Mode):**
   $$P(R_k) = \bigwedge_{s \in S(R_k)} s = s_1 \land s_2 \land \dots \land s_m$$
   The candidate hypothesis is satisfied if and only if **all** antecedent symptoms are simultaneously observed. If a subset is observed, the rule yields a **Partial Candidate (`Requires Further Inspection`)**.

2. **Disjunction (`ANY` Mode):**
   $$P(R_k) = \bigvee_{s \in S(R_k)} s = s_1 \lor s_2 \lor \dots \lor s_m$$
   Observing any single canonical symptom satisfies the preliminary triage threshold for this candidate.

3. **Core Anchor with Corroboration (`PRIMARY_OR_PARTIAL` Mode):**
   $$P(R_k) = \left( \bigvee_{p \in P_{\text{core}}} p \right) \land \left( \bigwedge_{c \in S_{\text{secondary}}} c \right)$$
   Requires at least one primary direct symptom to trigger full candidacy, while secondary symptoms provide differential corroboration.

---

## 3. Knowledge Base Schema Specification

The knowledge base is codified in [`backend/data/kbs_knowledge_base.json`](file:///d:/CARFAULTDIA/backend/data/kbs_knowledge_base.json) and validated by [`backend/validate_knowledge_base.py`](file:///d:/CARFAULTDIA/backend/validate_knowledge_base.py). Each of the 93 rules adheres to the following strict schema:

```json
{
  "rule_id": "RULE_BRK_003",
  "category_id": "CAT_BRAKES",
  "category_name": "Braking & ABS System",
  "subcategory": "Brake Booster",
  "title": "Brake Booster",
  "possible_fault": "Possible brake booster vacuum or diaphragm failure",
  "affected_component": "Vacuum Brake Power Booster & Check Valve Assembly",
  "subsystem": "Braking & Hydraulic Control Subsystem",
  "safety_level": "Critical",
  "required_expertise": "Certified Brake Technician",
  "required_tools": [
    "Vacuum Gauge (0-30 in-Hg)",
    "Hand Vacuum Pump",
    "Brake Pedal Depressor"
  ],
  "logic_mode": "ALL",
  "symptom_ids": [
    "SYM_HARD_BRAKE_PEDAL"
  ],
  "symptom_labels": [
    "Hard brake pedal"
  ],
  "diagnostic_questions": [
    {
      "question_id": "q_booster_hiss",
      "question": "Do you hear an audible hissing sound near the driver footwell when the brake pedal is depressed?",
      "options": ["Yes", "No", "Not Sure"],
      "supporting_answer": "Yes",
      "contradictory_answer": "No",
      "context": "An audible hiss inside the cabin indicates an internal booster vacuum seal rupture."
    }
  ],
  "diagnosis_steps": [
    {
      "step_number": 1,
      "step": "Measure engine manifold vacuum at booster check valve inlet using calibrated vacuum gauge.",
      "abnormal_result": "Vacuum reading < 16 in-Hg at idle (indicates restricted vacuum line or engine vacuum leak).",
      "normal_result": "Steady vacuum reading between 18 and 22 in-Hg."
    },
    {
      "step_number": 2,
      "step": "Depress brake pedal 5 times with engine off, hold pedal down, then start engine.",
      "abnormal_result": "Pedal remains rigid and does not drop slightly under foot (indicates vacuum assist failure).",
      "normal_result": "Pedal drops smoothly approximately 1/4 inch as engine starts."
    }
  ],
  "maintenance_actions": {
    "corrective_action": "Perform vacuum decay test; inspect one-way check valve and intake manifold vacuum supply line. Replace booster assembly if internal diaphragm leaks.",
    "preventive_measure": "Inspect booster vacuum hose and check valve for dry-rot or oil contamination every 30,000 miles.",
    "replacement_criteria": "Replace booster assembly if diaphragm fails vacuum hold test (leaks down > 2 in-Hg in 15 seconds) or if brake fluid has entered the vacuum chamber.",
    "do_not_replace_warning": "Do not replace booster without verifying that engine produces at least 18 in-Hg manifold vacuum at the check valve."
  },
  "source_reference": {
    "dataset_title": "Automotive Faults Dataset for Diagnostic and Maintenance Systems",
    "doi": "10.5281/zenodo.15626055",
    "source_file": "automotive_faults_aktc_obike_et_al.json",
    "source_record_ids": ["SRC_JSON_003"]
  }
}
```

---

## 4. Subsystem Distribution and Corpus Coverage

The knowledge base integrates all 93 subcategories from the peer-reviewed dataset across 8 automotive subsystems:

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

## 5. Decision Tree Flowcharts Integration

In addition to propositional logic rules, Auto Sage incorporates 4 expert diagnostic flowcharts digitized from the workshop engineering corpus:
1. `FC_BRAKES`: Brake Faults Diagnostic Flowchart (pedal feel, sponginess, pulsation, ABS indicators).
2. `FC_OVERHEATING`: Engine Overheating Flowchart (thermostat cycling, coolant circulation, fan relay actuation, head gasket integrity).
3. `FC_ELECTRICAL`: Electrical Faults Flowchart (parasitic draw, charging circuit voltage drop, starter solenoid drop).
4. `FC_TRANSMISSION`: Transmission Faults Flowchart (slippage, delayed engagement, fluid burnt smell, planetary gear noise).

These flowcharts serve as secondary visual validation trees for apprentice technicians.
