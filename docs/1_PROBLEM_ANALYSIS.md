# Auto Sage KBS — 1. Problem Analysis & Domain Specification

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Intelligent Automotive Fault Diagnosis System  
**Academic Alignment:** CLO 2 — Problem Analysis & Solution Design  

---

## 1. Executive Summary & Problem Context

Modern passenger automobiles are complex cyber-physical systems consisting of interconnected mechanical assemblies, hydraulic circuits, electromechanical actuators, and electronic control units (ECUs). When a vehicle develops an operational fault, drivers typically observe macroscopic symptoms:
- Uncharacteristic acoustic signatures (squealing brakes, engine clicking, metallic grinding)
- Tactile and haptic feedback (vibrations through steering wheel, pulsating brake pedal, hard pedal feel)
- Visual cues (tailpipe smoke color, instrument cluster warning indicators, leaking fluids)
- Performance anomalies (engine stalling, hesitation under load, delayed gear engagement, overheating)

### The Diagnostic Challenge
1. **Symptom Ambiguity:** A single high-level symptom (e.g., *engine hesitation under load*) may stem from distinct subsystems—fuel starvation (clogged fuel filter), ignition breakdown (fouled spark plugs), or unmetered air intrusion (vacuum leak).
2. **Component Interdependence:** In automotive engineering, failure in one subsystem cascades into adjacent assemblies. For example, a failing alternator leads to battery depletion, which subsequently triggers spurious transmission shift errors due to low ECU reference voltage.
3. **Risks of Premature Component Replacement:** Amateur mechanics and inexperienced drivers frequently engage in "parts-cannon" diagnostics—replacing costly components (such as starters, fuel pumps, or catalytic converters) without performing physical bench verification, resulting in unnecessary expense and persistent root causes.
4. **Safety-Critical Nature:** Flawed diagnosis in braking, steering, or fuel systems poses direct life-safety hazards.

---

## 2. Why Machine Learning is Inappropriate for Safety-Critical Automotive Triage

While black-box machine learning (deep neural networks, random forests, statistical classifiers) has gained widespread popularity in computer science, its application to safety-critical automotive triage suffers from fatal drawbacks:

| Evaluation Criterion | Statistical / Black-Box ML | Deterministic Knowledge-Based System (KBS) |
| :--- | :--- | :--- |
| **Explainability** | Opacity; latent feature weights cannot be interpreted by a workshop technician. | Complete transparent audit trail; every conclusion is mathematically traced to explicit IF–THEN propositional rules. |
| **Hallucination Risk** | Generative models invent plausible-sounding but mechanically catastrophic instructions. | Zero hallucination; inference is strictly bounded by peer-reviewed automotive domain rules. |
| **Confidence Scoring** | Outputs pseudo-probabilities (e.g., "87% confident") that give users a false sense of certainty without verifying physical parameters. | Explicit **Evidence Tally** strictly separated from probabilities; outputs unconfirmed hypotheses requiring physical bench checks. |
| **Verification Steps** | Recommends parts to swap without sequential test procedures. | Prescribes explicit **Tier A Bench Checks** (multimeter voltages, vacuum pressures, fluid clarity) before repair. |
| **Contradiction Handling** | Conflicting features yield noisy probabilities without explicit refutation. | Formal refutation logic; answers that conflict with a fault candidate mark it as **Fault Not Supported by Evidence**. |

---

## 3. Target User Personas & Operational Scope

Auto Sage is engineered for two distinct user personas:

### Persona A: Independent Vehicle Owner / DIY Enthusiast
- **Needs:** Non-technical symptom reporting interface, clear plain-English explanation of why a fault is suspected, realistic safety warnings, and explicit anti-mistake directives ("Do not replace this component before checking the \$5 fuse").
- **Experience:** Needs guided stepper workflow without overwhelming propositional logic jargon.

### Persona B: Apprentice Technician / University Evaluator (CT-359)
- **Needs:** Full transparent access to formal propositional logic expressions ($P \land Q \implies R$), multi-candidate differential comparison tables, structured maintenance directives (corrective, preventive, replacement criteria), and a 9-step reasoning audit trail.
- **Experience:** Needs downloadable PDF technical dossiers and complete rule traceability to peer-reviewed sources.

---

## 4. Operational Boundaries and Assumptions

1. **Deterministic Triage Hypothesis:** Auto Sage generates **possible fault candidates** requiring physical inspection; it never claims to execute a physical repair remotely.
2. **Bounded Subsystems:** Covers 8 core automotive subsystems:
   - Braking & Hydraulic Control Subsystem
   - Engine Cooling Subsystem
   - Electrical & Power Distribution Subsystem
   - Exhaust & Emissions Control Subsystem
   - Engine Mechanical & Fuel Delivery Subsystem
   - Heating, Ventilation & Air Conditioning (HVAC) Subsystem
   - Steering, Suspension & Tire Dynamics Subsystem
   - Transmission & Driveline Subsystem
3. **Verified Knowledge Provenance:** Grounded in the open-access dataset by Obike & Obot (*Automotive Faults Dataset for Diagnostic and Maintenance Systems*, Zenodo DOI: 10.5281/zenodo.15626055), augmented with domain expertise from ASE guidelines and SAE engineering standards.
