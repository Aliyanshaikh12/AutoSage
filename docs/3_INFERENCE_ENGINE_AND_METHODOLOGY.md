# Auto Sage KBS — 3. Inference Engine & Diagnostic Methodology

**Course:** Knowledge-Based Systems (CT-359)  
**Project:** Auto Sage — Intelligent Automotive Fault Diagnosis System  
**Academic Alignment:** CLO 3 — Method & Algorithm Assessment  

---

## 1. Algorithmic Foundation: Pure Deterministic Deduction

The Auto Sage inference engine ([`backend/inference_engine.py`](file:///d:/CARFAULTDIA/backend/inference_engine.py)) operates strictly via **deterministic forward-chaining propositional deduction**.

### Modus Ponens in Automotive Diagnostics
The fundamental inference rule applied is classical **Modus Ponens**:
$$\frac{P \implies Q, \quad P}{Q}$$

Where:
- $P$: The premise conjunction of observed physical vehicle symptoms ($\bigwedge s_i$).
- $Q$: The unconfirmed fault candidate hypothesis ($H_k$) targeting component $C_k$.

### Rejection of Statistical / Probabilistic Black Boxes
In university course **CT-359**, students must demonstrate rigorous knowledge engineering rather than invoking opaque statistical heuristics. Auto Sage deliberately rejects:
- Random forest classifiers
- Neural network latent embeddings
- Invented "confidence percentages" (e.g. 84.7%) that lack empirical calibration and violate ISO 26262 functional safety guidelines.

---

## 2. The 9-Step Deterministic Reasoning Trail

Every invocation of `diagnose()` executes a structured 9-stage pipeline, generating a verifiable audit trail returned in `results["reasoning_trail"]`:

```
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: Intake Validation & Input Set Canonicalization     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 2: Subsystem Boundary Filtering (Category Isolation)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 3: Propositional Premise Evaluation (Modus Ponens)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 4: Candidate Partitioning (Full vs Partial Matches)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 5: Follow-Up Inquiry Integration (Dynamic Tests)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 6: Contradiction & Corroboration Refutation Engine    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 7: Deterministic Evidence Tally Calculation           │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 8: Safety Stratification & Bench Test Selection       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Stage 9: Technical Dossier Assembly & Cross-Subsystem Audit │
└─────────────────────────────────────────────────────────────┘
```

### Detailed Trace of Each Stage:
1. **Intake Validation:** Validates that `category_id` exists in the knowledge base and that `symptom_ids` is a non-empty array of valid canonical identifiers. Strips duplicates and invalid entries.
2. **Subsystem Isolation:** Restricts candidate rule evaluation to the user's active vehicle subsystem ($R_{\text{active}} \subset R_{\text{universe}}$).
3. **Propositional Premise Evaluation:** Compares the active symptom set against rule premises using each rule's defined logic mode (`ALL`, `ANY`, or `PRIMARY_OR_PARTIAL`).
4. **Candidate Partitioning:**
   - **Full Match:** All required antecedent symptoms observed.
   - **Partial Match:** A subset of symptoms observed ($S_{\text{observed}} \cap S_{\text{rule}} \neq \emptyset$), designating a hypothesis requiring further verification.
5. **Follow-Up Inquiry Integration:** Ingests user responses to dynamic diagnostic questions ($q_i \in \{\text{Yes}, \text{No}, \text{Not Sure}\}$).
6. **Contradiction Detection:**
   - If user answer matches `supporting_answer`: Adds to `supporting_evidence` and elevates status to **Suspected Fault (Corroborated by Follow-up Evidence)**.
   - If user answer matches `contradictory_answer`: Triggers refutation logic, marking the candidate as **Fault Not Supported by Evidence**.
7. **Evidence Tally Formulation:** Calculates honest evidence counts (e.g., *2 of 2 symptoms observed; 1 follow-up confirmation*), strictly avoiding fake probabilities.
8. **Bench Test Selection:** Dynamically extracts the primary physical test for the top candidate from Tier A inspection steps (`results["next_recommended_test"]`).
9. **Dossier Assembly:** Attaches vehicle profile, cross-category matches, related decision tree flowcharts, and maintenance directives.

---

## 3. Evidence Tally vs. Pseudo-Probabilities

To maintain academic integrity under assessment rubrics, Auto Sage calculates an **Evidence Tally** rather than a fake probability:

$$\text{Evidence Tally} = \left\langle M, N, C_{\text{supp}}, C_{\text{cont}} \right\rangle$$

Where:
- $M = |S_{\text{rule}} \cap S_{\text{observed}}|$ (Number of matched canonical symptoms)
- $N = |S_{\text{rule}}|$ (Total symptoms defined in rule premise)
- $C_{\text{supp}}$ = Number of corroborating follow-up questions answered affirmatively
- $C_{\text{cont}}$ = Number of contradictory findings recorded

### Explicit Rejection of Confidence Scores
If an AI assistant generates "85% confidence" for a cracked cylinder head, a consumer might spend \$2,500 on an engine teardown when the true culprit was a \$15 stuck thermostat. Auto Sage outputs:
> *"2 of 2 primary symptoms observed. Status: Suspected Fault &bull; Unconfirmed. Required: Perform Block Tester chemical test (blue fluid turns yellow if exhaust gases present). Never replace cylinder head without physical bench test."*

---

## 4. Contradiction Detection & Refutation Logic

One of the key requirements of **CLO 2 & CLO 3** is handling conflicting evidence. 

### The Refutation Principle
Let $H_k$ be a fault hypothesis targeting Component $C_k$, and let $E_{\text{anti}}$ be a physical observation known to be mutually exclusive with $H_k$:

$$H_k \implies \neg E_{\text{anti}} \quad \equiv \quad E_{\text{anti}} \implies \neg H_k$$

**Real Automotive Example:**
- **Hypothesis:** Starter Motor Solenoid Contact Failure (`RULE_ELEC_003`).
- **Initial Symptom:** Vehicle fails to crank.
- **Dynamic Follow-Up Question:** *"When turning key to start, do headlights dim noticeably and battery voltage drop below 9.6V?"*
- **User Answer:** *"Yes, headlights dim significantly and voltage drops to 8.2V."*
- **Inference Refutation:** A bad starter solenoid with open contacts draws *zero* current, meaning headlights would *not* dim! Heavy voltage drop indicates a discharged battery or starter motor short circuit.
- **Outcome:** Starter Solenoid hypothesis is marked **Fault Not Supported by Evidence**, preventing the user from buying an unnecessary starter.

---

## 5. Multi-Candidate Differential Comparison

When multiple fault candidates share overlapping symptoms, Auto Sage provides a side-by-side differential comparison table (`results["candidates_comparison"]`):

| Candidate Fault | Target Component | Status | Safety Priority | Evidence Tally | Discriminating Bench Test |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Worn Brake Pads** | Semi-Metallic Brake Friction Pads | Suspected Fault | Medium | 1 / 1 | Measure pad lining thickness ($> 3\text{ mm}$ normal; $< 2\text{ mm}$ replace). |
| **Warped Brake Rotor** | Cast Iron Vented Brake Disc | Suspected Fault | High | 1 / 1 | Measure rotor lateral runout with dial indicator ($< 0.05\text{ mm}$ normal). |
| **Brake Booster Failure** | Vacuum Brake Power Booster | Unconfirmed | Critical | 1 / 2 | Perform manifold vacuum supply & pedal drop-down test. |

This multi-candidate comparison empowers technicians to order physical tests efficiently from least invasive to most invasive.
