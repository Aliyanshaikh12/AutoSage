# Auto Sage KBS — 7. Viva Voce Preparation & Technical Defense Guide

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Intelligent Automotive Fault Diagnosis System  

---

## 1. Core Viva Questions & Model Answers

### Q1: What is Auto Sage, and what makes it a Knowledge-Based System (KBS)?
**Model Answer:**
> *"Auto Sage is a deterministic, rule-based Knowledge-Based System designed for automotive fault diagnosis and maintenance planning. It qualifies as a KBS because its intelligence does not derive from statistical pattern recognition or neural network weights; rather, it possesses an explicit **Knowledge Base** containing a formalized automotive ontology and 93 propositional rules, cleanly separated from a domain-independent **Inference Engine** that executes forward-chaining deduction via Modus Ponens. Furthermore, it incorporates an interactive **Explanation Subsystem** that produces a 9-step reasoning audit trail and printable diagnostic dossiers."*

---

### Q2: Why did you choose a deterministic expert system over Machine Learning or Deep Learning?
**Model Answer:**
> *"In safety-critical domains such as automotive repair, black-box machine learning models suffer from three fatal flaws:
> 1. **Lack of Explainability:** A deep neural network cannot explain to a workshop technician *why* it suspects a component failure.
> 2. **Hallucination Risk:** Generative AI models frequently invent plausible-sounding but mechanically dangerous instructions.
> 3. **Uncalibrated Confidence:** Statistical models output deceptive confidence scores (e.g., '92% sure') that encourage premature component replacement.
> 
> Auto Sage operates deterministically: every candidate hypothesis is mathematically grounded in verified engineering rules from peer-reviewed literature (DOI: 10.5281/zenodo.15626055), and every diagnosis is strictly an unconfirmed hypothesis requiring physical bench verification."*

---

### Q3: How is knowledge represented in Auto Sage? (CLO 1 Defense)
**Model Answer:**
> *"Knowledge in Auto Sage is formalized using classical propositional logic across an 8-level ontology:
> $$\text{Subsystem} \implies \text{Component} \implies \text{Symptoms} \implies \text{Cause} \implies \text{Fault} \implies \text{Evidence} \implies \text{Test} \implies \text{Maintenance}$$
> 
> Each rule's antecedent is evaluated under one of three formal logic modes:
> - **`ALL` (Strict Conjunction):** $s_1 \land s_2 \land \dots \land s_n$. Requires all symptoms for a full match; otherwise yields a partial candidate.
> - **`ANY` (Disjunction):** $s_1 \lor s_2 \lor \dots \lor s_n$. Any canonical symptom triggers the triage hypothesis.
> - **`PRIMARY_OR_PARTIAL`:** Anchored on core primary symptoms while secondary symptoms provide corroboration."*

---

### Q4: How does your inference engine work step by step? (CLO 3 Defense)
**Model Answer:**
> *"The inference engine follows a 9-stage deterministic reasoning trail:
> 1. Validates and canonicalizes the input symptom IDs.
> 2. Isolates the candidate rule universe to the selected vehicle subsystem.
> 3. Evaluates rule premises using propositional logic.
> 4. Partitions candidates into Full Matches and Partial Candidates.
> 5. Formulates dynamic follow-up inquiry questions.
> 6. Evaluates user answers for corroboration ($E \implies H$) or contradiction ($E \implies \neg H$).
> 7. Computes an honest Evidence Tally (matched count vs total symptoms).
> 8. Assigns safety risk priority (Critical, High, Medium, Low) and selects the primary bench test.
> 9. Assembles the final technical dossier and links decision tree flowcharts."*

---

### Q5: How do you handle contradictory evidence and missing symptoms? (CLO 2 Defense)
**Model Answer:**
> *"Auto Sage implements formal refutation logic. If a user selects symptoms suggesting a fault, but responds to a follow-up question with an answer that directly contradicts that fault's physical operating profile, the inference engine marks the candidate as **'Fault Not Supported by Evidence'** and records the finding in `contradictory_evidence`.
> 
> Similarly, if a rule requires multiple symptoms but only one was observed, Auto Sage does not hallucinate a complete diagnosis; it honestly classifies it as a **'Partial Match &bull; Requires Further Inspection'**, explicitly detailing which symptoms are missing."*

---

### Q6: Why did you eliminate confidence percentages from your system?
**Model Answer:**
> *"Confidence percentages in diagnostic software are fundamentally misleading. If software claims '85% confidence' that an alternator is dead, a customer may waste \$400 replacing it when the true defect was a \$5 blown fuse or loose belt.
> 
> Instead of pseudo-probabilities, Auto Sage calculates an **Evidence Tally**—stating plainly: 'Matched 2 of 2 canonical symptoms; 1 corroborating follow-up test confirmed.' It then mandates a physical bench test (e.g. measuring charging voltage and voltage drop across the B+ cable) before any part replacement occurs."*

---

### Q7: Explain the difference between Tier A and Tier B in your resolution guide.
**Model Answer:**
> *"Auto Sage enforces a strict two-tier resolution framework:
> - **Tier A (Diagnostic Verification Checks):** Physical, sequential tests performed with calibrated workshop tools (multimeters, vacuum gauges, dial indicators) before taking anything apart. Each check defines the exact procedure, normal finding, and abnormal finding.
> - **Tier B (Structured Maintenance Directives):** Actionable guidance executed only after Tier A confirms the defect. It comprises four parts: Corrective Action, Preventive Measure, Objective Discard Criteria, and a Do-Not-Replace Directive."*

---

### Q8: What are 'Do-Not-Replace Directives', and why are they necessary?
**Model Answer:**
> *"Do-Not-Replace Directives are anti-mistake guidelines designed to prevent 'parts-cannon' diagnostics. For example, for an oxygen sensor fault, our directive warns: 'Do NOT replace the O2 sensor without checking for exhaust manifold leaks or misfire codes, as unmetered air or raw fuel will falsely trigger O2 sensor codes.' This directly addresses the university requirement for realistic, professional maintenance advice."*

---

### Q9: What happens if a user selects symptoms from two different categories?
**Model Answer:**
> *"The inference engine primary pass evaluates rules within the user's active category. Simultaneously, it executes a cross-subsystem correlation pass. If the selected symptoms also fully satisfy rules in adjacent subsystems (for example, low battery causing transmission solenoid codes), Auto Sage surfaces them in a dedicated **'Cross-Category Correlation Matches'** section."*

---

### Q10: What are the current limitations of Auto Sage, and how could it be improved?
**Model Answer:**
> *"Currently, Auto Sage relies on human observation for symptom intake. In future extensions, the system could integrate with an **OBD-II CAN bus scanner** (ELM327 / SAE J1979) to read real-time diagnostic trouble codes (DTCs) and freeze-frame sensor telemetry directly, bridging human-reported acoustic/tactile symptoms with ECU electronic fault codes."*
